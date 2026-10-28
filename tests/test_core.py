import ast
from pathlib import Path

import pytest

from shelf import core
from shelf.core import Services, Shelf, create, draw, generate, hide_book, show_book
from shelf.shelf_file import ShelfBook, ShelfFile, ShelfSection
from shelf.shelves import REST_TITLE
from tests.test_cli import FakeCovers, FakeLibrary, fake_portrait, fake_recognize, no_review

CORE = Path(core.__file__)


def services(**overrides):
    base = dict(
        recognize=fake_recognize,
        review=no_review,
        portrait=fake_portrait,
        library=FakeLibrary(),
        second=None,
        covers=FakeCovers(),
    )
    return Services(**{**base, **overrides})


def test_generate_returns_the_shelf_as_data_and_writes_no_shelf_file(shelf_folder):
    photos = sorted(shelf_folder.glob("*.jpg"))
    before = set(shelf_folder.iterdir())
    shelf = generate(photos, "sk-secret", "Lula", services())
    assert isinstance(shelf, Shelf)
    assert shelf.name == "Lula"
    assert shelf.photos == [p.name for p in photos]
    assert [b["title"] for b in shelf.books] == ["Torto Arado", "Cynefin"]  # duplicates across photos merged
    assert shelf.portrait["lens"] == "Eu olho a terra."
    assert shelf.left_out == []
    assert shelf.cost == 0.05
    assert set(shelf_folder.iterdir()) == before


def test_generate_reports_through_the_log_it_is_given(shelf_folder):
    lines = []
    generate(sorted(shelf_folder.glob("*.jpg")), "sk-secret", None, services(), log=lines.append)
    assert lines[0].startswith("Recognizing books in 2 photos")
    assert any("Writing your portrait" in line for line in lines)


def test_generate_is_silent_by_default(shelf_folder, capsys):
    generate(sorted(shelf_folder.glob("*.jpg")), "sk-secret", None, services())
    out = capsys.readouterr()
    assert out.out == "" and out.err == ""


def test_create_turns_paid_generation_into_the_versioned_file(shelf_folder):
    photos = sorted(shelf_folder.glob("*.jpg"))
    created = create(photos, "sk-secret", "Lula", services())

    assert created.migrated is False
    assert created.cost == 0.05 and created.books == 2
    assert created.shelf.version == 1
    assert created.shelf.cover_photo == "photo-01.jpg"
    assert created.shelf.lens == "Eu olho a terra."
    assert [section.title for section in created.shelf.shelves] == [
        "Quando penso na terra",
        REST_TITLE,
    ]
    assert [book.title for section in created.shelf.shelves for book in section.books] == [
        "Torto Arado",
        "Cynefin",
    ]


def test_create_migrates_cv1_books_by_calling_only_the_portrait(shelf_folder):
    class Forbidden:
        def __getattr__(self, name):
            raise AssertionError(f"migration called {name}")

    def forbidden(*args, **kwargs):
        raise AssertionError("migration called a generation service")

    calls = []

    def portrait(books, api_key):
        calls.append(([book["title"] for book in books], api_key))
        return {
            "lens": "Eu volto aos livros.",
            "themes": [{"title": "Quando volto", "text": "*Torto Arado*", "books": [0]}],
        }, 0.0123

    migration_services = Services(
        recognize=forbidden,
        review=forbidden,
        portrait=portrait,
        library=Forbidden(),
        second=Forbidden(),
        covers=Forbidden(),
    )
    legacy = """\
books:
  - title: Torto Arado
    authors: [Itamar Vieira Junior]
    cover_id: 7
    source: open_library
left_out:
  - title: Caneca
    reason: not a book
"""
    before = set(shelf_folder.iterdir())
    created = create(
        sorted(shelf_folder.glob("*.jpg")),
        "sk-secret",
        "Lula",
        migration_services,
        legacy_books=legacy,
    )

    assert calls == [(["Torto Arado"], "sk-secret")]
    assert created.migrated is True and created.cost == 0.0123 and created.books == 1
    book = created.shelf.shelves[0].books[0]
    assert book.cover == "https://covers.openlibrary.org/b/id/7-M.jpg?default=false"
    assert book.source == "open_library"
    assert created.shelf.left_out[0].reason == "not a book"
    assert set(shelf_folder.iterdir()) == before


def test_draw_needs_no_service_and_returns_the_page_from_shelf_file():
    shelf = ShelfFile(
        name="Lula",
        cover_photo="photo-01.jpg",
        lens="Eu olho a terra.",
        shelves=[
            ShelfSection(
                title="Quando penso na terra",
                text="Começo por *Torto Arado*.",
                books=[
                    ShelfBook(
                        title="Torto Arado",
                        authors=["Itamar Vieira Junior"],
                        face=True,
                        cover="https://example.test/torto.jpg",
                    ),
                    ShelfBook(title="Livro escondido", hidden=True),
                ],
            )
        ],
    )
    html = draw(shelf, ["data:image/jpeg;base64,YWJj"])
    assert "A estante de <span>Lula</span>" in html and "Torto Arado" in html
    assert "https://example.test/torto.jpg" in html and "Livro escondido" not in html


def test_hide_and_show_book_are_pure_named_operations_that_preserve_everything_else():
    original = ShelfFile(
        name="Lula",
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                text="Meu texto.",
                books=[
                    ShelfBook(
                        title="Torto Arado",
                        authors=["Itamar Vieira Junior"],
                        known_as="Itamar Vieira Junior",
                        face=True,
                        cover="https://example.test/cover.jpg",
                        source="open_library",
                        photo="photo.jpg",
                        work="/works/1",
                    ),
                    ShelfBook(title="Outro"),
                ],
            )
        ],
    )

    hidden = hide_book(original, 0, 0)
    shown = show_book(hidden, 0, 0)

    assert original.shelves[0].books[0].hidden is None
    assert hidden is not original and hidden.shelves[0] is not original.shelves[0]
    assert hidden.shelves[0].books[0].hidden is True
    assert hidden.shelves[0].books[0].title == "Torto Arado"
    assert hidden.shelves[0].books[0].cover == "https://example.test/cover.jpg"
    assert hidden.shelves[0].books[1] is original.shelves[0].books[1]
    assert shown.shelves[0].books[0].hidden is None
    assert [book.title for book in shown.shelves[0].books] == ["Torto Arado", "Outro"]


def test_hide_and_show_reject_negative_or_missing_positions():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="x",
        shelves=[ShelfSection(title="One", books=[ShelfBook(title="Book")])],
    )
    for operation in (hide_book, show_book):
        for shelf_index, book_index in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            with pytest.raises(IndexError):
                operation(shelf, shelf_index, book_index)


def test_the_core_never_talks_to_the_terminal():
    tree = ast.parse(CORE.read_text(encoding="utf-8"))
    calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert not calls & {"print", "input"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
            imported |= {f"{node.module}.{a.name}" for a in node.names}
    terminal = ("sys", "os", "getpass", "shelf.cli", "shelf.setup", "shelf.progress", "shelf.config")
    assert not {m for m in imported if m == "" or m.startswith(terminal)} - {""}
