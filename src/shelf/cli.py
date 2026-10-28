"""The command line: explicit verbs around the shelf core.

Only `create` can spend. `draw`, `open`, `setup`, and the command without a verb are free.
The core receives data and returns data; this module chooses folders, asks questions, and writes files.
"""

import argparse
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
    created = core.create(
        config.photos,
        config.api_key,
        config.name,
        services,
        legacy_books=legacy_books,
        log=log,
        progress=progress or Progress(),
    )
    _write_new(path, dump_shelf(created.shelf))
    log(
        f"Created {path.name} with {created.books} books "
        f"(cost: US$ {created.cost:.2f}{'; reused books.yaml' if created.migrated else ''})."
    )
    return CreateResult(path, created.books, created.cost, created.migrated)


def draw_shelf(folder: Path) -> DrawResult:
    """Validates the editable source, renders in memory, then safely replaces the page."""
    folder = Path(folder)
    source = folder / SHELF_YAML
    if not source.exists():
        raise CommandError(f"No {SHELF_YAML} in {folder}. Run `uv run shelf create --folder {folder}` first.")
    shelf = parse_shelf(source.read_text(encoding="utf-8"))
    photos = load_photos(folder)
    cover = next((photo for photo in photos if photo.name == shelf.cover_photo), None)
    if cover is None:
        raise CommandError(f'cover_photo "{shelf.cover_photo}" is not one of the photos in {folder}.')
    ordered = [cover] + [photo for photo in photos if photo != cover]
    images = [photo_tools.data_uri(photo_tools.prepare(photo, photo_tools.PAGE_SIDE)) for photo in ordered]
    html = core.draw(shelf, images)
    page = folder / PAGE
    _replace(page, html)
    books = sum(1 for section in shelf.shelves for book in section.books if book.hidden is not True)
    return DrawResult(page, books)


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


def _write_new(path: Path, text: str) -> None:
    """Creates a complete file atomically and fails if another writer created it first."""
    temporary = _temporary(path, text)
    try:
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            raise CommandError(f"{path.name} already exists. `create` never replaces your shelf.") from exc
    finally:
        temporary.unlink(missing_ok=True)


def _replace(path: Path, text: str) -> None:
    """Replaces a generated artifact only after its complete replacement exists."""
    temporary = _temporary(path, text)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _temporary(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
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
    command("draw", "draw shelf.html from shelf.yaml (free)")
    command("check", "check shelf.yaml and show every error (free)")
    command("open", "open the generated page (free)")
    command("setup", "change your name or API keys (free)")
    return parser


def main(
    argv: list[str] | None = None,
    terminal: setup.Terminal | None = None,
    interactive: bool | None = None,
    create_action: Callable = create_shelf,
    draw_action: Callable = draw_shelf,
    open_action: Callable = open_shelf,
    check_action: Callable = check_shelf,
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

    if args.command == "draw":
        try:
            result = draw_action(folder)
        except (CommandError, ConfigError, ShelfYamlError, OSError, ValueError) as exc:
            return _error(exc)
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

    # create: refuse replacement before setup, confirmation, or any paid service
    source = folder / SHELF_YAML
    if source.exists():
        return _error(CommandError(f"{SHELF_YAML} already exists. `create` never replaces your shelf."))
    try:
        load_photos(folder)  # photos come first: do not ask for keys for an empty folder
        legacy_path = folder / LEGACY_BOOKS
        legacy_text = legacy_path.read_text(encoding="utf-8") if legacy_path.exists() else None
        legacy_count = len(read_books_yaml(legacy_text)[0]) if legacy_text is not None else 0
        include_google = legacy_text is None
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
        result = create_action(config, legacy_books=legacy_text, log=terminal.say)
    except (CommandError, ShelfYamlError, OSError, ValueError) as exc:
        return _error(exc)
    terminal.say()
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
    history = folder / "history"
    versions = sum(path.is_file() for path in history.glob("*.yaml")) if history.is_dir() else 0
    return status.ShelfFacts(
        photo_count=photos,
        versions=versions,
        source_text=source.read_text(encoding="utf-8") if source.exists() else None,
        source_modified=source.stat().st_mtime if source.exists() else None,
        page_modified=page.stat().st_mtime if page.exists() else None,
    )


def _time(timestamp: float | None) -> str:
    return (
        datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M") if timestamp is not None else "unknown"
    )


def _command(verb: str, folder: Path) -> str:
    return f"uv run shelf {verb} --folder {shlex.quote(str(folder))}"


def _count(number: int, noun: str) -> str:
    plural = {"shelf": "shelves"}.get(noun, noun + "s")
    return f"{number} {noun if number == 1 else plural}"


def _error(error: Exception) -> int:
    print(f"shelf: {error}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
