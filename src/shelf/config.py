"""Reads the shelf folder: photos, API key and optional settings."""

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CONFIG_FILE = "config.toml"


class ConfigError(Exception):
    """Something the person must fix before the shelf can be generated."""


@dataclass
class Config:
    folder: Path
    photos: list[Path]
    api_key: str
    name: str | None = None


def load_config(folder: Path, env: Mapping[str, str] = os.environ) -> Config:
    folder = Path(folder)
    if not folder.is_dir():
        raise ConfigError(f"Folder not found: {folder}")
    photos = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in PHOTO_EXTENSIONS)
    if not photos:
        raise ConfigError(f"No photos in {folder}. Add .jpg, .jpeg, .png or .webp files of your shelf.")

    settings: dict = {}
    config_file = folder / CONFIG_FILE
    if config_file.exists():
        try:
            settings = tomllib.loads(config_file.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            raise ConfigError(f"Could not read {CONFIG_FILE}: {exc}") from exc

    api_key = (env.get("OPENROUTER_API_KEY") or settings.get("openrouter_api_key") or "").strip()
    if not api_key:
        raise ConfigError(
            "No OpenRouter API key. Set OPENROUTER_API_KEY or add "
            f'openrouter_api_key = "..." to {CONFIG_FILE} in the photos folder.'
        )
    cover = settings.get("cover_photo")
    if cover:
        match = [p for p in photos if p.name == cover]
        if not match:
            raise ConfigError(
                f'cover_photo = "{cover}" in {CONFIG_FILE} is not one of the photos in {folder}.'
            )
        photos = match + [p for p in photos if p.name != cover]
    return Config(folder=folder, photos=photos, api_key=api_key, name=settings.get("name") or None)
