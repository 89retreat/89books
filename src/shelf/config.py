"""Reads the shelf folder: photos, API key and optional settings."""

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}  # HEIC: iPhone photos
CONFIG_FILE = "config.toml"


class ConfigError(Exception):
    """Something the person must fix before the shelf can be generated."""


@dataclass
class Config:
    folder: Path
    photos: list[Path]
    api_key: str
    name: str | None = None
    google_books_api_key: str | None = None


def load_photos(folder: Path) -> list[Path]:
    """Lists shelf photos without reading configuration or requiring a key."""
    folder = Path(folder)
    if not folder.is_dir():
        raise ConfigError(
            f"Folder not found: {folder}. Put photos of your shelf in my-bookshelf/ and run `uv run shelf create`."
        )
    photos = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in PHOTO_EXTENSIONS)
    if not photos:
        raise ConfigError(
            f"No photos in {folder}. Put photos of your shelf in it (.jpg, .heic, .png or .webp) "
            "and run `uv run shelf create`."
        )
    return photos


def _settings(folder: Path) -> dict:
    config_file = Path(folder) / CONFIG_FILE
    if not config_file.exists():
        return {}
    try:
        return tomllib.loads(config_file.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Could not read {CONFIG_FILE}: {exc}") from exc


def load_config(folder: Path, env: Mapping[str, str] = os.environ) -> Config:
    folder = Path(folder)
    photos = load_photos(folder)
    settings = _settings(folder)

    api_key = (env.get("OPENROUTER_API_KEY") or settings.get("openrouter_api_key") or "").strip()
    if not api_key:
        raise ConfigError(
            "No OpenRouter API key. Run `uv run shelf setup` in a terminal, or set OPENROUTER_API_KEY."
        )
    cover = settings.get("cover_photo")
    if cover:
        match = [p for p in photos if p.name == cover]
        if not match:
            raise ConfigError(
                f'cover_photo = "{cover}" in {CONFIG_FILE} is not one of the photos in {folder}.'
            )
        photos = match + [p for p in photos if p.name != cover]
    google = (env.get("GOOGLE_BOOKS_API_KEY") or settings.get("google_books_api_key") or "").strip()
    google = (
        None if google in ("", "skip") else google
    )  # "skip" records that setup asked and the person declined
    return Config(
        folder=folder,
        photos=photos,
        api_key=api_key,
        name=settings.get("name") or None,
        google_books_api_key=google,
    )
