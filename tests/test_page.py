from shelf.page import render, render_file
from shelf.shelf_file import ShelfBook, ShelfFile, ShelfSection
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


def test_file_render_uses_resolved_local_cover_without_leaking_its_source_path():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                books=[ShelfBook(title="Livro corrigido", face=True, cover="private/capa.jpg")],
            )
        ],
    )

    html = render_file(shelf, [], {(0, 0): "data:image/jpeg;base64,Y2FwYQ=="})

    assert "data:image/jpeg;base64,Y2FwYQ==" in html
    assert "private/capa.jpg" not in html


def test_file_render_never_treats_an_unresolved_local_path_as_a_browser_url():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                books=[ShelfBook(title="Livro corrigido", face=True, cover="private/capa.jpg")],
            )
        ],
    )

    html = render_file(shelf, [])

    assert "private/capa.jpg" not in html
    assert 'class="face"' not in html
    assert 'class="spine' in html


def test_multiple_explicit_faces_reach_the_page_in_authored_order_with_wrapping_layout():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Capas escolhidas",
                text="Meu texto.",
                books=[
                    ShelfBook(
                        title=f"Capa {index}",
                        authors=[f"Autora {index}"],
                        face=True,
                        cover=f"https://example.test/{index}.jpg",
                    )
                    for index in range(6)
                ],
            )
        ],
    )

    html = render_file(shelf, [])

    assert html.count('class="face"') == 6
    assert [html.index(f"Capa {index}") for index in range(6)] == sorted(
        html.index(f"Capa {index}") for index in range(6)
    )
    assert "const widthOf" in html and "rows.push" in html


def test_hidden_book_has_no_face_or_spine_and_does_not_sustain_frequent_author():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                books=[
                    ShelfBook(
                        title="Livro escondido",
                        authors=["Milton Santos"],
                        face=True,
                        cover="https://example.test/hidden.jpg",
                        hidden=True,
                    ),
                    ShelfBook(title="Livro visível", authors=["Milton Santos"]),
                ],
            )
        ],
    )

    html = render_file(shelf, [])

    assert "Livro escondido" not in html
    assert "https://example.test/hidden.jpg" not in html
    assert "Livro visível" in html
    assert "Quem mais mora aqui" not in html


def test_hidden_false_and_absent_stay_visible_in_source_order():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                books=[
                    ShelfBook(title="Primeiro", hidden=False),
                    ShelfBook(title="Oculto", hidden=True),
                    ShelfBook(title="Terceiro"),
                ],
            )
        ],
    )

    html = render_file(shelf, [])

    assert "Oculto" not in html
    assert html.index("Primeiro") < html.index("Terceiro")


def test_all_hidden_books_leave_authored_shelf_title_and_text_untouched():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Minha prateleira continua aqui",
                text="Meu texto continua exatamente aqui.",
                books=[ShelfBook(title="Livro oculto", hidden=True)],
            )
        ],
    )

    html = render_file(shelf, [])

    assert "Minha prateleira continua aqui" in html
    assert "Meu texto continua exatamente aqui." in html
    assert "Livro oculto" not in html


def test_footer_does_not_claim_that_every_cover_comes_from_open_library():
    shelf = ShelfFile(
        cover_photo="photo.jpg",
        lens="Eu leio.",
        shelves=[
            ShelfSection(
                title="Quando penso",
                books=[ShelfBook(title="Livro local", face=True, cover="covers/capa.jpg")],
            )
        ],
    )

    html = render_file(shelf, [], {(0, 0): "data:image/jpeg;base64,Y2FwYQ=="})

    assert "Capas de catálogos ou arquivos locais" in html
    assert "Capas da Open Library" not in html


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
