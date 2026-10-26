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
