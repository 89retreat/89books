from shelf.page import render


def test_page_escapes_text_and_marks_book_titles():
    html = render(
        name=None,
        photos=["data:image/jpeg;base64,AAA"],
        books=[{"title": "<script>x</script>", "authors": ["A & B"], "cover_id": 7}],
        portrait={"lens": "Você lê *Torto Arado* <b>", "themes": [{"name": "Terra", "text": "ok"}]},
    )
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;" in html
    assert "<em>Torto Arado</em>" in html
    assert "&lt;b&gt;" in html
    assert "https://covers.openlibrary.org/b/id/7-M.jpg" in html
    assert "data:image/jpeg;base64,AAA" in html


def test_page_without_cover_shows_title_card_and_uses_name():
    html = render(
        name="Lula",
        photos=[],
        books=[{"title": "Cynefin", "authors": []}],
        portrait={"lens": "x", "themes": []},
    )
    assert "A estante de Lula" in html
    assert "Cynefin" in html
    assert "covers.openlibrary.org" not in html
