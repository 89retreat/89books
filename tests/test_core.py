import ast
from pathlib import Path

from shelf import core
from shelf.core import Services, Shelf, draw, generate
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


def test_draw_needs_no_service_and_returns_the_page():
    shelf = Shelf(
        name="Lula",
        photos=["photo-01.jpg"],
        books=[{"title": "Torto Arado", "authors": ["Itamar Vieira Junior"]}],
        left_out=[],
        portrait={"lens": "Eu olho a terra.", "themes": []},
        cost=0.0,
    )
    html = draw(shelf, ["data:image/jpeg;base64,YWJj"])
    assert "A estante de <span>Lula</span>" in html and "Torto Arado" in html


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
