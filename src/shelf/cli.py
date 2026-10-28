"""The command line: explicit verbs around the shelf core.

Only `create` and `recreate` can spend. Status, check, draw, history, restore, open and setup are free.
The core receives data and returns data; this module chooses folders, asks questions, and writes files.
"""

import argparse
import hashlib
import os
import shlex
import sys
import tempfile
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from shelf import core, setup, status
from shelf import history as history_core
from shelf import photos as photo_tools
from shelf.books import read_books_yaml
from shelf.config import CONFIG_FILE, PHOTO_EXTENSIONS, Config, ConfigError, load_config, load_photos
from shelf.covers import CoverCheck
from shelf.googlebooks import GoogleBooks
from shelf.openlibrary import OpenLibrary
from shelf.portrait import write_portrait
from shelf.progress import Progress
from shelf.recognition import recognize
from shelf.review import review_books
from shelf.shelf_file import ShelfYamlError, dump_shelf, parse_shelf

CACHE_DIR = ".shelf"
SHELF_YAML = "shelf.yaml"
PAGE = "shelf.html"
LEGACY_BOOKS = "books.yaml"
HISTORY_DIR = "history"
DRAWN_HASH = "last-drawn.sha256"
HISTORY_LIMIT = 20
DEFAULT_FOLDER = Path("my-bookshelf")


class CommandError(Exception):
    """A command could not safely do what the person asked."""


@dataclass
class CreateResult:
    shelf_yaml: Path
    books: int
    cost: float
    migrated: bool


@dataclass
class DrawResult:
    html: Path
    books: int
    version: Path | None = None


@dataclass
class RecreateResult:
    shelf_yaml: Path
    version: Path
    books: int
    cost: float


@dataclass
class RestoreResult:
    shelf_yaml: Path
    version: Path
    saved_current: Path | None
    changed: bool


@dataclass
class CheckResult:
    books: int
    visible_books: int
    shelves: int


def create_shelf(
    config: Config,
    legacy_books: str | None = None,
    recognize: Callable = recognize,
    library=None,
    portrait: Callable = write_portrait,
    covers=None,
    second=None,
    review: Callable = review_books,
    log: Callable[[str], None] = print,
    progress=None,
) -> CreateResult:
    """Calls the paid core once and safely creates shelf.yaml without replacing one."""
    path = config.folder / SHELF_YAML
    if path.exists():
        raise CommandError(f"{SHELF_YAML} already exists. `create` never replaces your shelf.")
    created = _generate_shelf(
        config,
        legacy_books=legacy_books,
        recognize=recognize,
        library=library,
        portrait=portrait,
        covers=covers,
        second=second,
        review=review,
        log=log,
        progress=progress,
    )
    _write_new(path, dump_shelf(created.shelf))
    log(
        f"Created {path.name} with {created.books} books "
        f"(cost: US$ {created.cost:.2f}{'; reused books.yaml' if created.migrated else ''})."
    )
    return CreateResult(path, created.books, created.cost, created.migrated)


def _generate_shelf(
    config: Config,
    legacy_books: str | None = None,
    recognize: Callable = recognize,
    library=None,
    portrait: Callable = write_portrait,
    covers=None,
    second=None,
    review: Callable = review_books,
    log: Callable[[str], None] = print,
    progress=None,
) -> core.Creation:
    cache = config.folder / CACHE_DIR
    if second is None and config.google_books_api_key:
        second = GoogleBooks(cache / "googlebooks.json", config.google_books_api_key)
    services = core.Services(
        recognize=recognize,
        review=review,
        portrait=portrait,
        library=library or OpenLibrary(cache / "openlibrary.json"),
        covers=covers or CoverCheck(cache / "covers.json"),
        second=second,
    )
    return core.create(
        config.photos,
        config.api_key,
        config.name,
        services,
        legacy_books=legacy_books,
        log=log,
        progress=progress or Progress(),
    )


def draw_shelf(folder: Path, now: datetime | None = None) -> DrawResult:
    """Validates the editable source, renders in memory, then safely replaces the page."""
    folder = Path(folder)
    source = folder / SHELF_YAML
    if not source.exists():
        raise CommandError(f"No {SHELF_YAML} in {folder}. Run `uv run shelf create --folder {folder}` first.")
    source_bytes = source.read_bytes()
    shelf = parse_shelf(source_bytes.decode("utf-8"))
    photos = load_photos(folder)
    cover = next((photo for photo in photos if photo.name == shelf.cover_photo), None)
    if cover is None:
        raise CommandError(f'cover_photo "{shelf.cover_photo}" is not one of the photos in {folder}.')
    ordered = [cover] + [photo for photo in photos if photo != cover]
    images = [photo_tools.data_uri(photo_tools.prepare(photo, photo_tools.PAGE_SIDE)) for photo in ordered]
    html = core.draw(shelf, images)
    digest = hashlib.sha256(source_bytes).hexdigest()
    marker = folder / CACHE_DIR / DRAWN_HASH
    previous = marker.read_text(encoding="utf-8").strip() if marker.exists() else None
    version = save_version(folder, source_bytes, now=now) if previous != digest else None
    page = folder / PAGE
    _replace(page, html)
    _replace(marker, digest + "\n")
    books = sum(1 for section in shelf.shelves for book in section.books if book.hidden is not True)
    return DrawResult(page, books, version)


def list_history(folder: Path) -> list[history_core.HistoryEntry]:
    """Lists managed version metadata without opening version contents."""
    directory = Path(folder) / HISTORY_DIR
    if not directory.is_dir():
        return []
    entries = []
    for path in directory.iterdir():
        if path.is_file() and history_core.is_managed_name(path.name):
            stat = path.stat()
            entries.append(history_core.HistoryEntry(path.name, stat.st_mtime, stat.st_size))
    return sorted(entries, key=lambda entry: (entry.modified_at, entry.name), reverse=True)


def save_version(folder: Path, source: bytes, now: datetime | None = None) -> Path:
    """Atomically stores exact source bytes and prunes only managed old versions."""
    folder = Path(folder)
    entries = list_history(folder)
    plan = history_core.plan_snapshot(entries, now or datetime.now().astimezone(), HISTORY_LIMIT)
    path = folder / HISTORY_DIR / plan.name
    _write_new(path, source, exists_message=f"Could not save version: {path.name} already exists.")
    for name in plan.remove:
        (folder / HISTORY_DIR / name).unlink()
    return path


def restore_shelf(folder: Path, version: str, now: datetime | None = None) -> RestoreResult:
    """Validates one selected version, snapshots the current bytes, then atomically restores it."""
    folder = Path(folder)
    entries = {entry.name for entry in list_history(folder)}
    if not history_core.is_managed_name(version) or version not in entries:
        raise CommandError(f'Unknown version "{version}". Run `uv run shelf history --folder {folder}`.')
    selected_path = folder / HISTORY_DIR / version
    selected = selected_path.read_bytes()
    parse_shelf(selected.decode("utf-8"))
    source = folder / SHELF_YAML
    if not source.exists():
        raise CommandError(f"No {SHELF_YAML} in {folder}.")
    current = source.read_bytes()
    if current == selected:
        return RestoreResult(source, selected_path, None, False)
    saved = save_version(folder, current, now=now)
    _replace(source, selected)
    return RestoreResult(source, selected_path, saved, True)


def recreate_shelf(
    config: Config,
    recognize: Callable = recognize,
    library=None,
    portrait: Callable = write_portrait,
    covers=None,
    second=None,
    review: Callable = review_books,
    log: Callable[[str], None] = print,
    progress=None,
    now: datetime | None = None,
) -> RecreateResult:
    """Generates from photos, then snapshots and replaces an existing source without drawing."""
    source = config.folder / SHELF_YAML
    if not source.exists():
        raise CommandError(f"No {SHELF_YAML} in {config.folder}. Run `create` first.")
    current = source.read_bytes()
    created = _generate_shelf(
        config,
        recognize=recognize,
        library=library,
        portrait=portrait,
        covers=covers,
        second=second,
        review=review,
        log=log,
        progress=progress,
    )
    replacement = dump_shelf(created.shelf).encode("utf-8")
    version = save_version(config.folder, current, now=now)
    _replace(source, replacement)
    return RecreateResult(source, version, created.books, created.cost)


def check_shelf(folder: Path) -> CheckResult:
    """Validates the one source contract without changing or drawing anything."""
    path = Path(folder) / SHELF_YAML
    if not path.exists():
        raise CommandError(f"No {SHELF_YAML} in {folder}. Run `uv run shelf create --folder {folder}` first.")
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    books = sum(len(section.books) for section in shelf.shelves)
    hidden = sum(book.hidden is True for section in shelf.shelves for book in section.books)
    return CheckResult(books, books - hidden, len(shelf.shelves))


def open_shelf(folder: Path, opener: Callable[[str], object] = webbrowser.open) -> Path:
    """Opens an existing page without using a shell command."""
    page = Path(folder) / PAGE
    if not page.exists():
        raise CommandError(f"No {PAGE} in {folder}. Run `uv run shelf draw --folder {folder}` first.")
    opener(page.resolve().as_uri())
    return page


def _write_new(path: Path, content: str | bytes, exists_message: str | None = None) -> None:
    """Creates a complete file atomically and fails if another writer created it first."""
    temporary = _temporary(path, content)
    try:
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            message = exists_message or f"{path.name} already exists. `create` never replaces your shelf."
            raise CommandError(message) from exc
    finally:
        temporary.unlink(missing_ok=True)


def _replace(path: Path, content: str | bytes) -> None:
    """Replaces an artifact only after its complete replacement exists."""
    temporary = _temporary(path, content)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _temporary(path: Path, content: str | bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content.encode("utf-8") if isinstance(content, str) else content)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        Path(name).unlink(missing_ok=True)
        raise
    return Path(name)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shelf",
        description="Create an editable bookshelf once, then draw and open it for free.",
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default=None,
        help="shelf folder (default: current shelf folder, then my-bookshelf)",
    )
    commands = parser.add_subparsers(dest="command")

    def command(name: str, help_text: str) -> argparse.ArgumentParser:
        sub = commands.add_parser(name, help=help_text)
        sub.add_argument("--folder", type=Path, default=argparse.SUPPRESS, help="shelf folder")
        return sub

    create = command("create", "create shelf.yaml once (paid)")
    create.add_argument("--yes", action="store_true", help="do not ask before spending")
    recreate = command("recreate", "replace shelf.yaml from photos after saving it (paid)")
    recreate.add_argument("--yes", action="store_true", help="do not ask before spending")
    command("draw", "draw shelf.html and save changed source (free)")
    command("check", "check shelf.yaml and show every error (free)")
    command("history", "list saved shelf.yaml versions (free)")
    restore = command("restore", "restore one saved shelf.yaml version (free)")
    restore.add_argument("version", help="exact version name printed by history")
    command("open", "open the generated page (free)")
    command("setup", "change your name or API keys (free)")
    return parser


def main(
    argv: list[str] | None = None,
    terminal: setup.Terminal | None = None,
    interactive: bool | None = None,
    create_action: Callable = create_shelf,
    recreate_action: Callable = recreate_shelf,
    draw_action: Callable = draw_shelf,
    open_action: Callable = open_shelf,
    check_action: Callable = check_shelf,
    history_action: Callable = list_history,
    restore_action: Callable = restore_shelf,
    check_openrouter: Callable = setup.check_openrouter,
    check_google: Callable = setup.check_google,
) -> int:
    args = _parser().parse_args(argv)
    terminal = terminal or setup.Terminal()
    interactive = setup.is_interactive() if interactive is None else interactive
    folder = resolve_folder(args.folder, Path.cwd())

    if args.command is None:
        _show_status(folder, terminal)
        return 0

    if args.command == "setup":
        if not folder.is_dir():
            return _error(ConfigError(f"Folder not found: {folder}."))
        if not interactive:
            return _error(CommandError("`shelf setup` needs an interactive terminal."))
        setup.run_setup(
            folder,
            os.environ,
            terminal,
            check_openrouter=check_openrouter,
            check_google=check_google,
            again=True,
        )
        return 0

    if args.command == "check":
        try:
            result = check_action(folder)
        except (CommandError, ShelfYamlError, OSError, ValueError) as exc:
            return _error(exc)
        terminal.say(
            f"{SHELF_YAML} is valid: {_count(result.books, 'book')} "
            f"({result.visible_books} visible) on {_count(result.shelves, 'shelf')}."
        )
        return 0

    if args.command == "history":
        try:
            versions = history_action(folder)
        except OSError as exc:
            return _error(exc)
        if not versions:
            terminal.say("No saved versions yet. The next draw after a change will save one.")
            return 0
        terminal.say("Versions (newest first):")
        for version in versions:
            terminal.say(f"  {version.name} — {_time(version.modified_at)} — {_size(version.size)}")
        return 0

    if args.command == "restore":
        try:
            result = restore_action(folder, args.version)
        except (CommandError, ShelfYamlError, OSError, ValueError) as exc:
            return _error(exc)
        if not result.changed:
            terminal.say(f"{args.version} is already the current {SHELF_YAML}. Nothing changed.")
            return 0
        terminal.say(f"Saved current source: {result.saved_current}")
        terminal.say(f"Restored {result.version.name} to {result.shelf_yaml}.")
        terminal.say(f"Next: `uv run shelf draw --folder {folder}` (free).")
        return 0

    if args.command == "draw":
        try:
            result = draw_action(folder)
        except (CommandError, ConfigError, ShelfYamlError, OSError, ValueError) as exc:
            return _error(exc)
        if result.version is not None:
            terminal.say(f"Saved version: {result.version}")
        terminal.say(f"Drawn for free: {result.html} ({result.books} books).")
        terminal.say(f"Open it with `uv run shelf open --folder {folder}`.")
        return 0

    if args.command == "open":
        try:
            page = open_action(folder)
        except (CommandError, OSError) as exc:
            return _error(exc)
        terminal.say(f"Opened {page}.")
        return 0

    # Paid commands establish replacement policy before setup, confirmation, or any service.
    source = folder / SHELF_YAML
    recreating = args.command == "recreate"
    if recreating and not source.exists():
        return _error(CommandError(f"No {SHELF_YAML} in {folder}. Run `create` first."))
    if not recreating and source.exists():
        return _error(CommandError(f"{SHELF_YAML} already exists. `create` never replaces your shelf."))
    if not interactive and not args.yes:
        return _error(CommandError(f"`shelf {args.command}` can spend. Run it interactively or pass --yes."))

    try:
        load_photos(folder)  # photos come first: do not ask for keys for an empty folder
        legacy_path = folder / LEGACY_BOOKS
        legacy_text = None
        if not recreating and legacy_path.exists():
            legacy_text = legacy_path.read_text(encoding="utf-8")
        legacy_count = len(read_books_yaml(legacy_text)[0]) if legacy_text is not None else 0
        include_google = recreating or legacy_text is None
        if interactive and setup.needs_setup(folder, os.environ, include_google=include_google):
            setup.run_setup(
                folder,
                os.environ,
                terminal,
                check_openrouter=check_openrouter,
                check_google=check_google,
                include_google=include_google,
            )
        config = load_config(folder)
    except (ConfigError, OSError, ValueError) as exc:
        return _error(exc)

    if interactive and not args.yes:
        confirmed = (
            setup.confirm_portrait_cost(legacy_count, terminal)
            if legacy_text is not None
            else setup.confirm_cost(len(config.photos), terminal)
        )
        if not confirmed:
            terminal.say("Nothing was spent.")
            return 0

    try:
        if recreating:
            recreated = recreate_action(config, log=terminal.say)
        else:
            result = create_action(config, legacy_books=legacy_text, log=terminal.say)
    except (CommandError, ShelfYamlError, OSError, ValueError) as exc:
        return _error(exc)
    terminal.say()
    if recreating:
        terminal.say(f"Saved current source: {recreated.version}")
        terminal.say(
            f"Recreated {recreated.shelf_yaml} with {recreated.books} books (cost: US$ {recreated.cost:.2f})."
        )
    else:
        terminal.say(f"Your editable shelf is ready: {result.shelf_yaml}")
        if result.migrated:
            terminal.say("Reused books.yaml; no photos or catalogues were read again.")
    terminal.say(f"Next: `uv run shelf draw --folder {folder}` (free).")
    return 0


def resolve_folder(explicit: Path | None, current: Path) -> Path:
    """An explicit path wins; otherwise use a current shelf or the clone's my-bookshelf fallback."""
    if explicit is not None:
        return Path(explicit)
    current = Path(current)
    if current.name == DEFAULT_FOLDER.name or _looks_like_shelf(current):
        return current
    return current / DEFAULT_FOLDER


def _looks_like_shelf(folder: Path) -> bool:
    if not folder.is_dir():
        return False
    names = {SHELF_YAML, LEGACY_BOOKS, CONFIG_FILE}
    return any(
        path.is_file() and (path.name in names or path.suffix.lower() in PHOTO_EXTENSIONS)
        for path in folder.iterdir()
    )


def _show_status(folder: Path, terminal: setup.Terminal) -> None:
    facts = _facts(folder)
    result = status.inspect(facts)
    terminal.say(f"Shelf: {folder.resolve()}")
    terminal.say(f"Photos: {result.photo_count}")
    if result.state == "not_created":
        terminal.say(f"Source: no {SHELF_YAML}")
    elif result.state == "invalid":
        terminal.say(
            f"Source: {SHELF_YAML} — invalid ({_count(len(result.errors), 'error')})"
            f" — edited {_time(result.source_modified)}"
        )
    else:
        terminal.say(
            f"Source: {SHELF_YAML} — {_count(result.books or 0, 'book')} "
            f"({result.visible_books} visible, {result.hidden_books} hidden)"
            f" — edited {_time(result.source_modified)}"
        )
    if result.page_modified is None:
        terminal.say(f"Page: no {PAGE}")
    else:
        page_state = {
            "invalid": "source invalid; previous page kept",
            "stale": "out of date",
            "ready": "up to date",
        }.get(result.state, "drawn")
        terminal.say(f"Page: {PAGE} — drawn {_time(result.page_modified)} — {page_state}")
    terminal.say(f"Versions: {result.versions}")
    terminal.say(f"Next: {_command(result.next_command, folder)}")


def _facts(folder: Path) -> status.ShelfFacts:
    folder = Path(folder)
    photos = 0
    if folder.is_dir():
        photos = sum(path.is_file() and path.suffix.lower() in PHOTO_EXTENSIONS for path in folder.iterdir())
    source = folder / SHELF_YAML
    page = folder / PAGE
    source_bytes = source.read_bytes() if source.exists() else None
    marker = folder / CACHE_DIR / DRAWN_HASH
    return status.ShelfFacts(
        photo_count=photos,
        versions=len(list_history(folder)),
        source_text=source_bytes.decode("utf-8") if source_bytes is not None else None,
        source_modified=source.stat().st_mtime if source.exists() else None,
        page_modified=page.stat().st_mtime if page.exists() else None,
        source_hash=hashlib.sha256(source_bytes).hexdigest() if source_bytes is not None else None,
        last_drawn_hash=marker.read_text(encoding="utf-8").strip() if marker.exists() else None,
    )


def _time(timestamp: float | None) -> str:
    return (
        datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M") if timestamp is not None else "unknown"
    )


def _command(verb: str, folder: Path) -> str:
    return f"uv run shelf {verb} --folder {shlex.quote(str(folder))}"


def _size(size: int) -> str:
    return f"{size} B" if size < 1024 else f"{size / 1024:.1f} KB"


def _count(number: int, noun: str) -> str:
    plural = {"shelf": "shelves"}.get(noun, noun + "s")
    return f"{number} {noun if number == 1 else plural}"


def _error(error: Exception) -> int:
    print(f"shelf: {error}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
