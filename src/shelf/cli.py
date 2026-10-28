"""Command line: asks, confirms and shows; the shelf itself is made by shelf.core.

`shelf <folder>` writes shelf.html and books.yaml into the folder.
"""

import argparse
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from shelf import core, setup
from shelf import photos as photo_tools
from shelf.books import write_books_yaml
from shelf.config import PHOTO_EXTENSIONS, Config, ConfigError, load_config
from shelf.covers import CoverCheck
from shelf.googlebooks import GoogleBooks
from shelf.openlibrary import OpenLibrary
from shelf.portrait import write_portrait
from shelf.progress import Progress
from shelf.recognition import recognize
from shelf.review import review_books

CACHE_DIR = ".shelf"


@dataclass
class Result:
    html: Path
    books_yaml: Path
    books: int
    cost: float


def build_shelf(
    config: Config,
    recognize: Callable = recognize,
    library=None,
    portrait: Callable = write_portrait,
    covers=None,
    second=None,
    review: Callable = review_books,
    log: Callable[[str], None] = print,
    progress=None,
) -> Result:
    """Generates the shelf with the core and writes it into the folder, with its caches in .shelf/."""
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
    shelf = core.generate(config.photos, config.api_key, config.name, services, log, progress or Progress())
    images = [photo_tools.data_uri(photo_tools.prepare(p, photo_tools.PAGE_SIDE)) for p in config.photos]
    html_path = config.folder / "shelf.html"
    html_path.write_text(core.draw(shelf, images), encoding="utf-8")
    yaml_path = config.folder / "books.yaml"
    write_books_yaml(yaml_path, shelf.books, shelf.left_out)
    log(f"Done: {html_path.name} and {yaml_path.name} in {config.folder} (cost: US$ {shelf.cost:.2f})")
    return Result(html=html_path, books_yaml=yaml_path, books=len(shelf.books), cost=shelf.cost)


DEFAULT_FOLDER = Path("my-bookshelf")


def main(
    argv: list[str] | None = None,
    terminal: setup.Terminal | None = None,
    interactive: bool | None = None,
    build: Callable = build_shelf,
    check_openrouter: Callable = setup.check_openrouter,
    check_google: Callable = setup.check_google,
) -> int:
    parser = argparse.ArgumentParser(
        prog="shelf",
        description="Turn photos of your bookshelf into a shareable HTML page with a reader portrait.",
    )
    parser.add_argument(
        "folder",
        type=Path,
        nargs="?",
        default=DEFAULT_FOLDER,
        help="folder with your shelf photos (default: my-bookshelf)",
    )
    parser.add_argument("--setup", action="store_true", help="ask for your name and keys again")
    parser.add_argument("--yes", action="store_true", help="do not ask before spending")
    args = parser.parse_args(argv)
    terminal = terminal or setup.Terminal()
    interactive = setup.is_interactive() if interactive is None else interactive

    # photos come first: asking for keys only to find an empty folder would waste the person's time
    if args.folder.is_dir() and not any(
        p.suffix.lower() in PHOTO_EXTENSIONS for p in args.folder.iterdir() if p.is_file()
    ):
        print(
            f"shelf: No photos in {args.folder}. Put photos of your shelf in it (.jpg, .heic, .png or .webp) "
            "and run `uv run shelf` again.",
            file=sys.stderr,
        )
        return 2
    if interactive and args.folder.is_dir() and (args.setup or setup.needs_setup(args.folder, os.environ)):
        setup.run_setup(
            args.folder,
            os.environ,
            terminal,
            check_openrouter=check_openrouter,
            check_google=check_google,
            again=args.setup,
        )
    try:
        config = load_config(args.folder)
    except ConfigError as exc:
        print(f"shelf: {exc}", file=sys.stderr)
        return 2
    if interactive and not args.yes and not setup.confirm_cost(len(config.photos), terminal):
        terminal.say("Nothing was spent.")
        return 0
    build(config)
    page = config.folder / "shelf.html"
    opener = "open" if sys.platform == "darwin" else "start" if os.name == "nt" else "xdg-open"
    terminal.say()
    terminal.say(f"Your shelf is ready: {page}")
    terminal.say(f"Open it in your browser with `{opener} {page}`.")
    terminal.say("To share it, send the file itself (WhatsApp, AirDrop, email) and open it in a browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
