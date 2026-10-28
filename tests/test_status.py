import ast
from pathlib import Path

from shelf import status
from shelf.shelf_file import ShelfBook, ShelfFile, ShelfSection, dump_shelf
from shelf.status import ShelfFacts, inspect

MODULE = Path(status.__file__)


def source(hidden=False):
    return dump_shelf(
        ShelfFile(
            cover_photo="photo.jpg",
            lens="Eu leio.",
            shelves=[
                ShelfSection(
                    title="Quando penso",
                    books=[
                        ShelfBook(title="Visível"),
                        ShelfBook(title="Escondido", hidden=hidden),
                    ],
                )
            ],
        )
    )


def test_not_created_recommends_create_without_parsing_anything():
    result = inspect(ShelfFacts(photo_count=3, versions=0))
    assert result.state == "not_created"
    assert result.photo_count == 3 and result.books is None
    assert result.next_command == "create"
    assert result.errors == ()


def test_invalid_source_recommends_check_and_keeps_every_issue():
    result = inspect(
        ShelfFacts(
            photo_count=1,
            source_text="version: two\ncover_photo: 9\nlens: ok\nshelves: []\n",
            source_modified=20,
            page_modified=10,
            versions=2,
        )
    )
    assert result.state == "invalid" and result.next_command == "check"
    assert [(issue.line, issue.path) for issue in result.errors] == [(1, "version"), (2, "cover_photo")]
    assert result.versions == 2 and result.source_modified == 20 and result.page_modified == 10


def test_valid_source_without_page_recommends_draw_and_counts_hidden_books():
    result = inspect(ShelfFacts(photo_count=1, source_text=source(hidden=True), source_modified=20))
    assert result.state == "not_drawn" and result.next_command == "draw"
    assert result.books == 2 and result.visible_books == 1 and result.hidden_books == 1
    assert result.shelves == 1


def test_newer_source_is_stale_and_updated_page_is_ready():
    stale = inspect(
        ShelfFacts(photo_count=1, source_text=source(), source_modified=20, page_modified=10, versions=3)
    )
    ready = inspect(
        ShelfFacts(photo_count=1, source_text=source(), source_modified=20, page_modified=20, versions=3)
    )
    assert stale.state == "stale" and stale.next_command == "draw"
    assert ready.state == "ready" and ready.next_command == "open"
    assert ready.versions == 3


def test_status_core_has_no_filesystem_terminal_environment_or_clock_access():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not calls & {"print", "input", "open"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    forbidden = ("pathlib", "os", "sys", "time", "datetime", "getpass", "shelf.cli", "shelf.config")
    assert not {module for module in imported if module.startswith(forbidden)}
