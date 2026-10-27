import tomllib

import pytest

from shelf.setup import estimate, needs_setup, run_setup, write_config


class FakeTerminal:
    def __init__(self, answers):
        self.answers = list(answers)
        self.questions = []
        self.lines = []

    def ask(self, question):
        self.questions.append(question)
        return self.answers.pop(0)

    secret = ask

    def say(self, line=""):
        self.lines.append(line)

    @property
    def text(self):
        return "\n".join(self.lines + self.questions)


def openrouter(key):
    return (True, 12.5) if key == "sk-or-good" else (False, None)


def google(key):
    return key == "AIza-good"


def read(folder):
    return tomllib.loads((folder / "config.toml").read_text())


def test_first_setup_explains_asks_checks_and_saves(shelf_folder):
    terminal = FakeTerminal(["Lula", "sk-or-good", "AIza-good"])
    assert needs_setup(shelf_folder, env={})
    run_setup(shelf_folder, env={}, terminal=terminal, check_openrouter=openrouter, check_google=google)
    assert read(shelf_folder) == {
        "name": "Lula",
        "openrouter_api_key": "sk-or-good",
        "google_books_api_key": "AIza-good",
    }
    assert "openrouter.ai/keys" in terminal.text and "credit" in terminal.text
    assert "US$ 12.50" in terminal.text
    assert not needs_setup(shelf_folder, env={})


def test_a_rejected_key_is_asked_again_before_anything_is_spent(shelf_folder):
    terminal = FakeTerminal(["Lula", "sk-or-typo", "sk-or-good", ""])
    run_setup(shelf_folder, env={}, terminal=terminal, check_openrouter=openrouter, check_google=google)
    assert read(shelf_folder)["openrouter_api_key"] == "sk-or-good"
    assert "did not work" in terminal.text


def test_three_rejected_keys_stop_the_setup(shelf_folder):
    terminal = FakeTerminal(["Lula", "a", "b", "c"])
    with pytest.raises(SystemExit):
        run_setup(shelf_folder, env={}, terminal=terminal, check_openrouter=openrouter, check_google=google)
    assert not (shelf_folder / "config.toml").exists()


def test_skipping_google_books_is_remembered(shelf_folder):
    terminal = FakeTerminal(["Lula", "sk-or-good", ""])
    run_setup(shelf_folder, env={}, terminal=terminal, check_openrouter=openrouter, check_google=google)
    assert read(shelf_folder)["google_books_api_key"] == "skip"
    assert not needs_setup(shelf_folder, env={})


def test_existing_settings_are_kept_and_only_missing_answers_are_asked(shelf_folder):
    (shelf_folder / "config.toml").write_text('cover_photo = "photo-02.jpg"\nname = "Lula"\n')
    terminal = FakeTerminal(["sk-or-good", ""])
    run_setup(shelf_folder, env={}, terminal=terminal, check_openrouter=openrouter, check_google=google)
    config = read(shelf_folder)
    assert config["cover_photo"] == "photo-02.jpg" and config["name"] == "Lula"
    assert len(terminal.questions) == 2


def test_keys_from_the_environment_are_not_asked(shelf_folder):
    env = {"OPENROUTER_API_KEY": "sk-or-good", "GOOGLE_BOOKS_API_KEY": "AIza-good"}
    assert needs_setup(shelf_folder, env=env)  # the name is still missing
    terminal = FakeTerminal(["Lula"])
    run_setup(shelf_folder, env=env, terminal=terminal, check_openrouter=openrouter, check_google=google)
    assert read(shelf_folder) == {"name": "Lula"}


def test_write_config_escapes_quotes(tmp_path):
    write_config(tmp_path, {"name": 'Lula "o leitor" \\ Rodrigues'})
    assert read(tmp_path)["name"] == 'Lula "o leitor" \\ Rodrigues'


def test_estimate_grows_with_photos():
    cost, minutes = estimate(7)
    assert 0.10 <= cost <= 0.25 and 3 <= minutes <= 8
    assert estimate(14)[0] > cost
