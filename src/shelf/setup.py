"""Guided setup: asks for what the shelf folder is missing, checks each key and saves config.toml.

Everything here is in English, as is the whole terminal surface; the shelf itself is in Portuguese.
"""

import getpass
import sys
import time
import tomllib
from collections.abc import Callable, Mapping
from pathlib import Path

import httpx

from shelf.config import CONFIG_FILE

SKIP = "skip"
ATTEMPTS = 3
COST_PER_PHOTO = 0.015  # recognition of one photo
COST_PER_SHELF = 0.07  # review of the whole list and the portrait
COST_PER_PORTRAIT = 0.03  # measured on the 160-book CV1 migration
SECONDS_PER_PHOTO = 40  # recognition plus catalogue lookups for the books in it
SECONDS_PER_SHELF = 60

OPENROUTER_HELP = """\
An OpenRouter key lets the command read your photos and write your portrait.
  1. Sign in at https://openrouter.ai and add some credit (US$ 5 is plenty: a shelf costs cents).
  2. Create a key at https://openrouter.ai/keys and copy it (it starts with sk-or-).
The key is saved only in my-bookshelf/config.toml, which git ignores."""

GOOGLE_HELP = """\
A Google Books key is optional. It lets the command check titles and authors in a second catalogue,
which knows more Brazilian editions. It is free:
  1. At https://console.cloud.google.com create a project and enable the "Books API".
  2. Under "APIs & Services > Credentials", create an API key and restrict it to the Books API.
Press Enter to skip; run `uv run shelf setup` later to add it."""


class Terminal:
    def ask(self, question: str) -> str:
        return input(question).strip()

    def secret(self, question: str) -> str:
        return getpass.getpass(question).strip()

    def say(self, line: str = "") -> None:
        print(line)


def check_openrouter(key: str) -> tuple[bool, float | None]:
    """Whether OpenRouter accepts the key, and the credit left on the account when it says so."""
    headers = {"Authorization": f"Bearer {key}"}
    try:
        response = httpx.get("https://openrouter.ai/api/v1/key", headers=headers, timeout=20)
        if response.status_code != 200:
            return False, None
        credits = httpx.get("https://openrouter.ai/api/v1/credits", headers=headers, timeout=20)
        data = credits.json().get("data", {}) if credits.status_code == 200 else {}
        balance = data.get("total_credits", 0) - data.get("total_usage", 0) if data else None
        return True, balance
    except (httpx.HTTPError, ValueError):
        return False, None


def check_google(key: str, get: Callable = httpx.get, wait: Callable = time.sleep) -> bool:
    """False only when Google refuses the key. The API answers 503 now and then and 429 when the day's
    quota is used up; neither says anything about the key, so they do not send the person to paste it again."""
    for attempt in range(4):
        try:
            response = get(
                "https://www.googleapis.com/books/v1/volumes",
                params={"q": "Torto Arado", "maxResults": 1, "key": key},
                timeout=20,
            )
        except httpx.HTTPError:
            wait(1 + attempt)
            continue
        if response.status_code < 500:
            return response.status_code not in (400, 401, 403)
        wait(1 + attempt)
    return True


def read_config(folder: Path) -> dict:
    path = Path(folder) / CONFIG_FILE
    return tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _quote(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return str(value)
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_config(folder: Path, settings: dict) -> None:
    lines = ["# Settings for this shelf. Keep this file private: it holds your keys."]
    lines += [f"{key} = {_quote(value)}" for key, value in settings.items()]
    (Path(folder) / CONFIG_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _missing(settings: dict, env: Mapping[str, str], include_google: bool = True) -> list[str]:
    missing = []
    if not settings.get("name"):
        missing.append("name")
    if not (env.get("OPENROUTER_API_KEY") or settings.get("openrouter_api_key")):
        missing.append("openrouter")
    if include_google and not (env.get("GOOGLE_BOOKS_API_KEY") or settings.get("google_books_api_key")):
        missing.append("google")
    return missing


def needs_setup(folder: Path, env: Mapping[str, str], include_google: bool = True) -> bool:
    return bool(_missing(read_config(folder), env, include_google))


def run_setup(
    folder: Path,
    env: Mapping[str, str],
    terminal: Terminal,
    check_openrouter: Callable[[str], tuple[bool, float | None]] = check_openrouter,
    check_google: Callable[[str], bool] = check_google,
    again: bool = False,
    include_google: bool = True,
) -> None:
    """Asks only for what is missing, or for everything the folder holds when `again` is set."""
    settings = read_config(folder)
    if again:
        for key in ("name", "openrouter_api_key", "google_books_api_key"):
            settings.pop(key, None)
    missing = _missing(settings, env, include_google)
    terminal.say("Let's set up your shelf. This happens once; answers are saved in my-bookshelf/config.toml.")
    terminal.say()

    if "name" in missing:
        settings["name"] = terminal.ask("Your name, as it should appear on the shelf: ") or "Minha"

    if "openrouter" in missing:
        terminal.say(OPENROUTER_HELP)
        for _attempt in range(ATTEMPTS):
            key = terminal.secret("OpenRouter key (hidden as you type): ")
            ok, balance = check_openrouter(key)
            if ok:
                settings["openrouter_api_key"] = key
                if balance is not None:
                    terminal.say(f"  Key works. Credit left: US$ {balance:.2f}.")
                    if balance < 1:
                        terminal.say("  That is low: add credit at https://openrouter.ai/settings/credits.")
                break
            terminal.say("  That key did not work. Check that it was copied whole.")
        else:
            terminal.say(
                "No working OpenRouter key, so nothing was saved. Run `uv run shelf setup` to try again."
            )
            raise SystemExit(2)
        terminal.say()

    if "google" in missing:
        terminal.say(GOOGLE_HELP)
        while True:
            key = terminal.secret("Google Books key (Enter to skip): ")
            if not key:
                settings["google_books_api_key"] = SKIP
                terminal.say("  Skipped.")
                break
            if check_google(key):
                settings["google_books_api_key"] = key
                terminal.say("  Key works.")
                break
            terminal.say("  That key did not work. Paste it again, or press Enter to skip.")
        terminal.say()

    write_config(folder, settings)
    terminal.say(f"Saved {Path(folder).name}/{CONFIG_FILE}.")
    terminal.say()


def estimate(photos: int) -> tuple[float, int]:
    """Estimated cost in US dollars and time in minutes for a shelf with this many photos."""
    cost = COST_PER_PHOTO * photos + COST_PER_SHELF
    minutes = max(1, round((SECONDS_PER_PHOTO * photos + SECONDS_PER_SHELF) / 60))
    return round(cost, 2), minutes


def confirm_cost(photos: int, terminal: Terminal) -> bool:
    cost, minutes = estimate(photos)
    terminal.say(
        f"Found {photos} photos. Making your shelf costs about US$ {cost:.2f} and takes about {minutes} minutes."
    )
    answer = terminal.ask("Continue? [Y/n] ").lower()
    return answer in ("", "y", "yes")


def confirm_portrait_cost(books: int, terminal: Terminal) -> bool:
    terminal.say(
        f"Found books.yaml with {books} books. Reusing it avoids reading the photos again. "
        f"Writing a new portrait costs about US$ {COST_PER_PORTRAIT:.2f} and takes about 1 minute."
    )
    answer = terminal.ask("Continue? [Y/n] ").lower()
    return answer in ("", "y", "yes")


def is_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()
