import pytest

from shelf.config import ConfigError, load_config


def test_lists_photos_in_name_order_and_reads_key_from_env(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-env"})
    assert [p.name for p in config.photos] == ["photo-01.jpg", "photo-02.jpg"]
    assert config.api_key == "sk-env"
    assert config.name is None


def test_reads_key_and_name_from_config_toml(shelf_folder):
    (shelf_folder / "config.toml").write_text('openrouter_api_key = "sk-file"\nname = "Lula"\n')
    config = load_config(shelf_folder, env={})
    assert config.api_key == "sk-file"
    assert config.name == "Lula"


def test_missing_key_is_a_clear_error(shelf_folder):
    with pytest.raises(ConfigError, match="OPENROUTER_API_KEY"):
        load_config(shelf_folder, env={})


def test_folder_without_photos_is_a_clear_error(tmp_path):
    with pytest.raises(ConfigError, match="No photos"):
        load_config(tmp_path, env={"OPENROUTER_API_KEY": "sk"})


def test_missing_folder_is_a_clear_error(tmp_path):
    with pytest.raises(ConfigError, match="Folder not found"):
        load_config(tmp_path / "nope", env={"OPENROUTER_API_KEY": "sk"})


def test_cover_photo_from_config_comes_first(shelf_folder):
    (shelf_folder / "config.toml").write_text('cover_photo = "photo-02.jpg"\n')
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk"})
    assert [p.name for p in config.photos] == ["photo-02.jpg", "photo-01.jpg"]


def test_unknown_cover_photo_is_a_clear_error(shelf_folder):
    (shelf_folder / "config.toml").write_text('cover_photo = "nope.jpg"\n')
    with pytest.raises(ConfigError, match="cover_photo"):
        load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk"})


def test_google_books_key_is_optional_and_read_from_env_or_config(shelf_folder):
    assert load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk"}).google_books_api_key is None
    env = {"OPENROUTER_API_KEY": "sk", "GOOGLE_BOOKS_API_KEY": "gb-env"}
    assert load_config(shelf_folder, env=env).google_books_api_key == "gb-env"
    (shelf_folder / "config.toml").write_text('google_books_api_key = "gb-file"\n')
    assert load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk"}).google_books_api_key == "gb-file"


def test_a_skipped_google_books_key_means_no_key(shelf_folder):
    (shelf_folder / "config.toml").write_text('google_books_api_key = "skip"\n')
    assert load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk"}).google_books_api_key is None


def test_heic_photos_are_listed(tmp_path):
    (tmp_path / "IMG_0001.HEIC").write_bytes(b"x")
    (tmp_path / "IMG_0002.heif").write_bytes(b"x")
    config = load_config(tmp_path, env={"OPENROUTER_API_KEY": "sk"})
    assert [p.name for p in config.photos] == ["IMG_0001.HEIC", "IMG_0002.heif"]


def test_no_photos_message_names_heic_and_the_command(tmp_path):
    with pytest.raises(ConfigError, match=r"\.heic.*uv run shelf create"):
        load_config(tmp_path, env={"OPENROUTER_API_KEY": "sk"})
