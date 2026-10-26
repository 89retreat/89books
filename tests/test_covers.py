from io import BytesIO

from PIL import Image, ImageDraw

from shelf.covers import CoverCheck, looks_like_cover


def jpeg(size, color, ink=None):
    image = Image.new("RGB", size, color)
    if ink:
        draw = ImageDraw.Draw(image)
        for y in range(20, size[1] - 20, 12):
            draw.line((15, y, size[0] - 15, y), fill=ink, width=2)
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    return buffer.getvalue()


def test_a_scanned_page_of_text_is_not_a_cover():
    assert not looks_like_cover(jpeg((128, 196), (250, 250, 250), ink=(40, 40, 40)))


def test_a_landscape_scan_is_not_a_cover():
    assert not looks_like_cover(jpeg((180, 128), (200, 120, 60)))


def test_coloured_covers_pass_even_when_mostly_white():
    assert looks_like_cover(jpeg((180, 270), (30, 60, 120)))
    assert looks_like_cover(jpeg((180, 240), (250, 250, 250), ink=(220, 40, 40)))


def test_a_white_cover_with_a_faint_tint_passes():
    # like the first edition of Extreme Programming Explained: white, grey letters, a warm cast
    assert looks_like_cover(jpeg((128, 161), (251, 249, 244), ink=(150, 148, 145)))


def test_a_dark_grey_cover_passes():
    assert looks_like_cover(jpeg((180, 270), (60, 60, 60), ink=(230, 230, 230)))


def test_cover_check_downloads_once_and_caches(tmp_path):
    calls = []

    def fetch(cover_id):
        calls.append(cover_id)
        return (
            jpeg((128, 196), (250, 250, 250), ink=(40, 40, 40))
            if cover_id == 1
            else jpeg((180, 270), (30, 60, 120))
        )

    check = CoverCheck(tmp_path / "covers.json", fetch=fetch)
    assert check.ok(1) is False and check.ok(2) is True
    check.save()
    again = CoverCheck(tmp_path / "covers.json", fetch=fetch)
    assert again.ok(1) is False and again.ok(2) is True
    assert calls == [1, 2]


def test_cover_that_cannot_be_downloaded_is_kept_for_the_browser_to_decide(tmp_path):
    def fetch(cover_id):
        raise OSError("offline")

    check = CoverCheck(tmp_path / "covers.json", fetch=fetch)
    assert check.ok(5) is True
    check.save()
    assert "5" not in (tmp_path / "covers.json").read_text()
