from shelf import cli
from tests.test_setup import FakeTerminal, google, openrouter


def run(argv, terminal, interactive=True, built=None):
    built = [] if built is None else built
    code = cli.main(
        argv,
        terminal=terminal,
        interactive=interactive,
        build=lambda config, **kw: built.append(config),
        check_openrouter=openrouter,
        check_google=google,
    )
    return code, built


def test_default_folder_is_my_bookshelf(tmp_path, monkeypatch, shelf_folder):
    monkeypatch.chdir(tmp_path)
    shelf_folder.rename(tmp_path / "my-bookshelf")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_BOOKS_API_KEY", raising=False)
    terminal = FakeTerminal(["Lula", "sk-or-good", "", "y"])
    code, built = run([], terminal)
    assert code == 0 and built[0].folder.name == "my-bookshelf" and built[0].name == "Lula"
    assert "2 photos" in terminal.text and "US$" in terminal.text


def test_declining_the_cost_spends_nothing(shelf_folder, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-good")
    (shelf_folder / "config.toml").write_text('name = "Lula"\ngoogle_books_api_key = "skip"\n')
    terminal = FakeTerminal(["n"])
    code, built = run([str(shelf_folder)], terminal)
    assert code == 0 and built == []
    assert "Nothing was spent" in terminal.text


def test_configured_folder_only_asks_for_the_cost_and_yes_skips_it(shelf_folder, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-good")
    (shelf_folder / "config.toml").write_text('name = "Lula"\ngoogle_books_api_key = "skip"\n')
    terminal = FakeTerminal([""])
    assert run([str(shelf_folder)], terminal)[1]
    assert len(terminal.questions) == 1
    terminal = FakeTerminal([])
    assert run([str(shelf_folder), "--yes"], terminal)[1]
    assert terminal.questions == []


def test_setup_flag_asks_again(shelf_folder, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    (shelf_folder / "config.toml").write_text(
        'name = "Lula"\nopenrouter_api_key = "sk-or-good"\ngoogle_books_api_key = "skip"\n'
    )
    terminal = FakeTerminal(["Lula Rodrigues", "sk-or-good", "", "y"])
    built = run([str(shelf_folder), "--setup"], terminal)[1]
    assert built[0].name == "Lula Rodrigues"


def test_without_a_terminal_nothing_is_asked(shelf_folder, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    terminal = FakeTerminal([])
    code, built = run([str(shelf_folder)], terminal, interactive=False)
    assert code == 2 and built == [] and terminal.questions == []
    assert "OPENROUTER_API_KEY" in capsys.readouterr().err


def test_missing_folder_points_to_my_bookshelf(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    code, _ = run([], FakeTerminal([]))
    assert code == 2 and "my-bookshelf" in capsys.readouterr().err


def test_an_empty_folder_is_reported_before_any_question(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    folder = tmp_path / "my-bookshelf"
    folder.mkdir()
    (folder / "README.md").write_text("put photos here")
    terminal = FakeTerminal([])
    code, built = run([str(folder)], terminal)
    assert code == 2 and terminal.questions == [] and built == []
    assert "Put photos of your shelf" in capsys.readouterr().err


def test_the_end_says_where_the_shelf_is_and_how_to_share_it(shelf_folder, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-good")
    (shelf_folder / "config.toml").write_text('name = "Lula"\ngoogle_books_api_key = "skip"\n')
    terminal = FakeTerminal([])
    run([str(shelf_folder), "--yes"], terminal)
    assert "shelf.html" in terminal.text and "browser" in terminal.text and "share" in terminal.text.lower()
