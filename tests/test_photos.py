from io import BytesIO

from PIL import Image

from shelf.photos import MAX_SIDE, data_uri, prepare


def test_prepare_shrinks_and_strips_exif(shelf_folder):
    data = prepare(shelf_folder / "photo-01.jpg")
    image = Image.open(BytesIO(data))
    assert max(image.size) == MAX_SIDE
    assert not image.getexif()
    assert b"SecretCam" not in data


def test_data_uri_is_inline_jpeg():
    assert data_uri(b"abc") == "data:image/jpeg;base64,YWJj"


def test_iphone_heic_photos_are_read_like_any_other(tmp_path):
    import pillow_heif

    pillow_heif.register_heif_opener()
    exif = Image.Exif()
    exif[0x010F] = "iPhone"
    Image.new("RGB", (2400, 1200), (90, 60, 30)).save(tmp_path / "IMG_0001.HEIC", "HEIF", exif=exif)
    data = prepare(tmp_path / "IMG_0001.HEIC")
    image = Image.open(BytesIO(data))
    assert image.format == "JPEG" and max(image.size) == MAX_SIDE
    assert b"iPhone" not in data
