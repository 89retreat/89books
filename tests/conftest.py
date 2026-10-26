from pathlib import Path

import pytest
from PIL import Image


def make_photo(path: Path, size=(2400, 1200), exif_make: str | None = None) -> Path:
    image = Image.new("RGB", size, (120, 80, 40))
    if exif_make:
        exif = Image.Exif()
        exif[0x010F] = exif_make  # Make
        image.save(path, "JPEG", exif=exif)
    else:
        image.save(path, "JPEG")
    return path


@pytest.fixture
def shelf_folder(tmp_path: Path) -> Path:
    folder = tmp_path / "my-shelf"
    folder.mkdir()
    make_photo(folder / "photo-02.jpg")
    make_photo(folder / "photo-01.jpg", exif_make="SecretCam")
    (folder / "notes.txt").write_text("not a photo")
    return folder
