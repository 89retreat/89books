import os
from datetime import datetime
from pathlib import Path

import pytest

from shelf import cli
from shelf.shelf_file import ShelfBook, ShelfFile, ShelfSection, dump_shelf
from tests.test_setup import FakeTerminal, google, openrouter


def fake_create(calls):
    def create(config, legacy_books=None, log=None, **kwargs):
        calls.append(("create", config, legacy_books))
        return cli.CreateResult(
            shelf_yaml=config.folder / "shelf.yaml",
            books=12,
            cost=0.02 if legacy_books else 0.05,
            migrated=legacy_books is not None,
        )

    return create


def fake_draw(calls):
    def draw(folder, **kwargs):
        calls.append(("draw", Path(folder)))
        return cli.DrawResult(html=Path(folder) / "shelf.html", books=12)

    return draw


def fake_open(calls):
    def open_page(folder, **kwargs):
        calls.append(("open", Path(folder)))
        return Path(folder) / "shelf.html"

    return open_page


def run(argv, terminal, interactive=True):
    calls = []
    code = cli.main(
        argv,
        terminal=terminal,
        interactive=interactive,
        create_action=fake_create(calls),
        draw_action=fake_draw(calls),
        open_action=fake_open(calls),
        check_openrouter=openrouter,
        check_google=google,
    )
    return code, calls


def configured(folder, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-good")
    (folder / "config.toml").write_text('name = "Lula"\ngoogle_books_api_key = "skip"\n')


def test_help_never_calls_an_action():
    calls = []
    with pytest.raises(SystemExit) as stopped:
        cli.main(
            ["--help"],
            terminal=FakeTerminal([]),
            interactive=False,
            create_action=fake_create(calls),
            draw_action=fake_draw(calls),
            open_action=fake_open(calls),
        )
    assert stopped.value.code == 0 and calls == []


def test_without_a_verb_nothing_is_asked_or_spent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    terminal = FakeTerminal([])

    code, calls = run([], terminal)

    assert code == 0 and calls == [] and terminal.questions == []
    assert f"Shelf: {tmp_path / 'my-bookshelf'}" in terminal.text
    assert "Photos: 0" in terminal.text and "Next:" in terminal.text
    assert "create" in terminal.text.lower()


def test_folder_resolution_prefers_explicit_then_current_shelf_then_fallback(tmp_path):
    current = tmp_path / "current"
    current.mkdir()
    explicit = tmp_path / "explicit"
    assert cli.resolve_folder(explicit, current) == explicit

    (current / "shelf.yaml").write_text("source")
    assert cli.resolve_folder(None, current) == current
    (current / "shelf.yaml").unlink()
    (current / "photo.jpeg").write_bytes(b"photo")
    assert cli.resolve_folder(None, current) == current
    (current / "photo.jpeg").unlink()

    assert cli.resolve_folder(None, current) == current / "my-bookshelf"
    named = tmp_path / "my-bookshelf"
    named.mkdir()
    assert cli.resolve_folder(None, named) == named


def test_status_panel_shows_ready_counts_dates_versions_and_next_open(tmp_path, monkeypatch):
    folder = tmp_path / "shelf"
    folder.mkdir()
    (folder / "photo.jpg").write_bytes(b"photo")
    source = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                books=[ShelfBook(title="Visível"), ShelfBook(title="Oculto", hidden=True)],
            )
        ],
    )
    (folder / "shelf.yaml").write_text(dump_shelf(source))
    (folder / "shelf.html").write_text("page")
    os.utime(folder / "shelf.yaml", (1000, 1000))
    os.utime(folder / "shelf.html", (2000, 2000))
    history = folder / "history"
    history.mkdir()
    (history / "shelf-1.yaml").write_text("one")
    (history / "notes.txt").write_text("not a version")
    monkeypatch.chdir(folder)
    terminal = FakeTerminal([])

    code, calls = run([], terminal)

    assert code == 0 and calls == []
    assert f"Shelf: {folder}" in terminal.text
    assert "Photos: 1" in terminal.text
    assert "2 books (1 visible, 1 hidden)" in terminal.text
    assert datetime.fromtimestamp(1000).strftime("%Y-%m-%d %H:%M") in terminal.text
    assert datetime.fromtimestamp(2000).strftime("%Y-%m-%d %H:%M") in terminal.text
    assert "up to date" in terminal.text and "Versions: 1" in terminal.text
    assert "open" in terminal.text.lower()


def test_status_panel_reports_invalid_summary_and_check_prints_all_errors(tmp_path, monkeypatch, capsys):
    folder = tmp_path / "shelf"
    folder.mkdir()
    source = folder / "shelf.yaml"
    page = folder / "shelf.html"
    source.write_text("version: two\ncover_photo: 9\nlens: ok\nshelves: []\n")
    page.write_text("valid page")
    source_before, page_before = source.read_bytes(), page.read_bytes()
    source_mtime, page_mtime = source.stat().st_mtime_ns, page.stat().st_mtime_ns
    monkeypatch.chdir(folder)

    terminal = FakeTerminal([])
    code, calls = run([], terminal)
    assert code == 0 and calls == []
    assert "invalid (2 errors)" in terminal.text and "check" in terminal.text.lower()

    terminal = FakeTerminal([])
    code, calls = run(["check"], terminal)
    error = capsys.readouterr().err
    assert code == 2 and calls == []
    assert "line 1: version" in error and "line 2: cover_photo" in error
    assert source.read_bytes() == source_before and page.read_bytes() == page_before
    assert source.stat().st_mtime_ns == source_mtime and page.stat().st_mtime_ns == page_mtime


def test_check_valid_source_is_a_read_only_summary(tmp_path, monkeypatch):
    folder = tmp_path / "shelf"
    folder.mkdir()
    (folder / "shelf.yaml").write_text(
        dump_shelf(
            ShelfFile(
                cover_photo="photo.jpg",
                lens="Eu leio.",
                shelves=[
                    ShelfSection(title="Quando penso", books=[ShelfBook(title="Livro")]),
                    ShelfSection(title="Quando sinto", books=[ShelfBook(title="Outro")]),
                ],
            )
        )
    )
    before = (folder / "shelf.yaml").read_bytes()
    monkeypatch.chdir(folder)
    terminal = FakeTerminal([])

    code, calls = run(["check"], terminal)

    assert code == 0 and calls == []
    assert "valid" in terminal.text.lower() and "2 books" in terminal.text and "2 shelves" in terminal.text
    assert (folder / "shelf.yaml").read_bytes() == before


def test_default_folder_create_runs_setup_confirms_cost_and_creates_once(tmp_path, monkeypatch, shelf_folder):
    monkeypatch.chdir(tmp_path)
    shelf_folder.rename(tmp_path / "my-bookshelf")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_BOOKS_API_KEY", raising=False)
    terminal = FakeTerminal(["Lula", "sk-or-good", "", "y"])

    code, calls = run(["create"], terminal)

    assert code == 0 and calls[0][0] == "create"
    assert calls[0][1].folder.name == "my-bookshelf" and calls[0][1].name == "Lula"
    assert calls[0][2] is None
    assert "2 photos" in terminal.text and "US$" in terminal.text
    assert "draw" in terminal.text.lower()


def test_create_refuses_existing_shelf_before_setup_or_confirmation(shelf_folder, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    (shelf_folder / "shelf.yaml").write_text("mine\n")
    terminal = FakeTerminal([])

    code, calls = run(["create", "--folder", str(shelf_folder)], terminal)

    assert code == 2 and calls == [] and terminal.questions == []
    assert "already exists" in capsys.readouterr().err
    assert (shelf_folder / "shelf.yaml").read_text() == "mine\n"


def test_declining_full_generation_spends_nothing(shelf_folder, monkeypatch):
    configured(shelf_folder, monkeypatch)
    terminal = FakeTerminal(["n"])

    code, calls = run(["create", "--folder", str(shelf_folder)], terminal)

    assert code == 0 and calls == []
    assert "Nothing was spent" in terminal.text


def test_yes_skips_the_paid_confirmation(shelf_folder, monkeypatch):
    configured(shelf_folder, monkeypatch)
    terminal = FakeTerminal([])

    code, calls = run(["create", "--folder", str(shelf_folder), "--yes"], terminal)

    assert code == 0 and calls[0][0] == "create"
    assert terminal.questions == []


def test_cv1_migration_confirms_only_a_new_portrait_and_passes_the_legacy_text(shelf_folder, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-good")
    (shelf_folder / "config.toml").write_text('name = "Lula"\n')
    legacy = "books:\n  - title: Torto Arado\n"
    (shelf_folder / "books.yaml").write_text(legacy)
    terminal = FakeTerminal(["y"])

    code, calls = run(["create", "--folder", str(shelf_folder)], terminal)

    assert code == 0 and calls[0][2] == legacy
    assert "books.yaml" in terminal.text and "portrait" in terminal.text.lower()
    assert "US$ 0.03" in terminal.text
    assert len(terminal.questions) == 1  # no Google Books setup; only cost confirmation


def test_draw_and_open_need_no_key_or_setup(shelf_folder, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    terminal = FakeTerminal([])

    draw_code, draw_calls = run(["draw", "--folder", str(shelf_folder)], terminal)
    open_code, open_calls = run(["open", "--folder", str(shelf_folder)], terminal)

    assert draw_code == open_code == 0
    assert draw_calls == [("draw", shelf_folder)] and open_calls == [("open", shelf_folder)]
    assert terminal.questions == []
    assert "free" in terminal.text.lower()


def test_setup_is_an_explicit_free_verb(shelf_folder, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    (shelf_folder / "config.toml").write_text(
        'name = "Lula"\nopenrouter_api_key = "sk-or-good"\ngoogle_books_api_key = "skip"\n'
    )
    terminal = FakeTerminal(["Lula Rodrigues", "sk-or-good", ""])

    code, calls = run(["setup", "--folder", str(shelf_folder)], terminal)

    assert code == 0 and calls == []
    assert 'name = "Lula Rodrigues"' in (shelf_folder / "config.toml").read_text()


def test_an_empty_folder_is_reported_before_any_create_question(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    folder = tmp_path / "my-bookshelf"
    folder.mkdir()
    terminal = FakeTerminal([])

    code, calls = run(["create", "--folder", str(folder)], terminal)

    assert code == 2 and calls == [] and terminal.questions == []
    assert "Put photos" in capsys.readouterr().err
