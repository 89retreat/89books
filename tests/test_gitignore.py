import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ignored(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT)
    return result.returncode == 0


def test_my_bookshelf_keeps_only_its_readme_in_git():
    assert ignored("my-bookshelf/IMG_0001.HEIC")
    assert ignored("my-bookshelf/config.toml")
    assert ignored("my-bookshelf/shelf.html")
    assert ignored("my-bookshelf/shelf.yaml")
    assert ignored("my-bookshelf/.shelf/covers.json")
    assert not ignored("my-bookshelf/README.md")
    assert ignored("another-shelf/shelf.yaml")
    assert ignored("another-shelf/history/shelf-2026-10-28-1900.yaml")
    assert not ignored("another-shelf/history/notes.yaml")
