from shelf.page import render
from shelf.shelves import REST_TITLE

PORTRAIT = {
    "lens": "Eu leio *Torto Arado* <b>",
    "themes": [{"title": "Quando penso <na> terra", "text": "Começa por *Torto Arado*.", "books": [0]}],
}


def test_page_escapes_text_and_marks_book_titles():
    html = render(
        name=None,
        photos=["data:image/jpeg;base64,AAA"],
        books=[{"title": "<script>x</script>", "authors": ["A & B"], "cover_id": 7}],
        portrait={"lens": "Eu leio *Torto Arado* <b>", "themes": []},
    )
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;" in html
    assert "<em>Torto Arado</em>" in html
    assert "&lt;b&gt;" in html
    assert "data:image/jpeg;base64,AAA" in html


def test_page_shows_themes_as_shelves_with_cited_cover_face_out():
    html = render(
        name="Lula",
        photos=["data:image/jpeg;base64,AAA", "data:image/jpeg;base64,BBB"],
        books=[{"title": "Torto Arado", "authors": [], "cover_id": 7}, {"title": "Cynefin", "authors": []}],
        portrait=PORTRAIT,
    )
    assert "Lula" in html and "A estante de" in html
    assert "Quando penso &lt;na&gt; terra" in html
    assert "https://covers.openlibrary.org/b/id/7-M.jpg?default=false" in html
    assert REST_TITLE in html
    assert "Cynefin" in html
    assert html.count('class="tile') == 2


def test_page_embeds_the_title_font():
    html = render(name=None, photos=[], books=[], portrait={"lens": "x", "themes": []})
    assert "font-family: 'Newsreader'" in html or 'font-family:"Newsreader"' in html
    assert "data:font/woff2;base64," in html


def test_page_names_who_lives_on_the_shelf_and_puts_the_author_first():
    books = [{"title": f"Livro {i}", "authors": ["Milton Santos"]} for i in range(2)]
    html = render(name=None, photos=[], books=books, portrait={"lens": "x", "themes": []})
    assert "Quem mais mora aqui" in html and "Milton Santos" in html
    spine = html[html.index('class="spine') :]
    assert spine.index("<b>Milton Santos</b>") < spine.index("<span>Livro")
