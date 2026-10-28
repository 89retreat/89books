import base64
import re
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from shelf import local_covers
from shelf.local_covers import MAX_BYTES, MAX_PIXELS, CoverAssetError, resolve_cover_assets
from shelf.shelf_file import ShelfBook, ShelfFile, ShelfSection


def source(cover: str | None, title: str = "Livro corrigido") -> ShelfFile:
    return ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[ShelfSection(title="Quando penso", books=[ShelfBook(title=title, face=True, cover=cover)])],
    )


def make_cover(path: Path, size=(900, 1500), exif_make="PrivateCamera") -> Path:
    image = Image.new("RGB", size, (50, 90, 130))
    exif = Image.Exif()
    exif[0x010F] = exif_make
    image.save(path, "JPEG", exif=exif)
    return path


def jpeg_from_data_uri(value: str) -> bytes:
    encoded = re.fullmatch(r"data:image/jpeg;base64,(.+)", value).group(1)
    return base64.b64decode(encoded)


def test_none_and_https_need_no_local_asset_or_network(tmp_path):
    assert resolve_cover_assets(tmp_path, source(None)) == {}
    assert resolve_cover_assets(tmp_path, source("none")) == {}
    assert resolve_cover_assets(tmp_path, source("https://example.test/capa.jpg")) == {}


@pytest.mark.parametrize(
    "cover", ["http://example.test/capa.jpg", "data:image/png;base64,abc", "https:///capa.jpg"]
)
def test_only_complete_https_urls_are_remote_covers(tmp_path, cover):
    with pytest.raises(CoverAssetError, match='Book "Livro corrigido"'):
        resolve_cover_assets(tmp_path, source(cover))


def test_local_cover_is_bounded_sanitized_and_embedded(tmp_path):
    covers = tmp_path / "covers"
    covers.mkdir()
    make_cover(covers / "capa.jpg")

    assets = resolve_cover_assets(tmp_path, source("covers/capa.jpg"))
    jpeg = jpeg_from_data_uri(assets[(0, 0)])
    image = Image.open(BytesIO(jpeg))

    assert image.format == "JPEG" and max(image.size) == 1000
    assert not image.getexif()
    assert b"PrivateCamera" not in jpeg


@pytest.mark.parametrize(
    "cover", ["capa.jpg", "covers/missing.jpg", "covers/notes.txt", "/tmp/capa.jpg", "covers/../capa.jpg"]
)
def test_invalid_local_cover_names_are_book_specific_errors(tmp_path, cover):
    covers = tmp_path / "covers"
    covers.mkdir()
    (covers / "notes.txt").write_text("not an image")
    with pytest.raises(CoverAssetError, match='Book "Livro corrigido"'):
        resolve_cover_assets(tmp_path, source(cover))


def test_symlink_cannot_escape_the_cover_folder(tmp_path):
    outside = make_cover(tmp_path.parent / "outside.jpg")
    covers = tmp_path / "covers"
    covers.mkdir()
    (covers / "linked.jpg").symlink_to(outside)

    with pytest.raises(CoverAssetError, match="outside the covers folder"):
        resolve_cover_assets(tmp_path, source("covers/linked.jpg"))


def test_raw_file_size_is_bounded_without_reading_the_file(tmp_path):
    covers = tmp_path / "covers"
    covers.mkdir()
    path = covers / "huge.jpg"
    with path.open("wb") as stream:
        stream.seek(MAX_BYTES)
        stream.write(b"x")

    with pytest.raises(CoverAssetError, match="5 MiB"):
        resolve_cover_assets(tmp_path, source("covers/huge.jpg"))


def test_decoded_pixel_count_is_bounded_before_preparing(monkeypatch, tmp_path):
    covers = tmp_path / "covers"
    covers.mkdir()
    path = covers / "compressed.jpg"
    path.write_bytes(b"small")

    class HugeImage:
        size = (MAX_PIXELS + 1, 1)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(local_covers.Image, "open", lambda unused: HugeImage())
    with pytest.raises(CoverAssetError, match="25 megapixels"):
        resolve_cover_assets(tmp_path, source("covers/compressed.jpg"))
