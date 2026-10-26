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
