from shelf.shelf_file import ShelfBook, ShelfSection
from shelf.shelves import (
    REST_TITLE,
    SIDE_MAX,
    build_shelves,
    frequent_authors,
    mosaic,
    roman,
    shelves_from_file,
    short_name,
    spine,
    tilt,
)


def book(title, cover_id=None):
    return {"title": title, "authors": [], "cover_id": cover_id}


def test_file_shelves_keep_literal_section_and_book_order_without_author_grouping():
    sections = [
        ShelfSection(
            title="Primeira",
            text="Texto.",
            books=[
                ShelfBook(title="A1", authors=["Autora"]),
                ShelfBook(title="Outro", authors=["Outra"]),
                ShelfBook(title="A2", authors=["Autora"]),
            ],
        ),
        ShelfSection(title="Segunda", text="Texto.", books=[ShelfBook(title="Final")]),
    ]

    visible, shelves = shelves_from_file(sections)

    assert [shelf["title"] for shelf in shelves] == ["Primeira", "Segunda"]
    assert [book["title"] for book in shelves[0]["books"]] == ["A1", "Outro", "A2"]
    assert [book["title"] for book in visible] == ["A1", "Outro", "A2", "Final"]
    assert [shelf["numeral"] for shelf in shelves] == ["I", "II"]
    assert [shelf["order"] for shelf in shelves] == [1, 2]


def test_explicit_face_spine_and_absent_face_follow_reader_precedence():
    cover = "https://example.test/cover.jpg"
    sections = [
        ShelfSection(
            title="Choices",
            text="*Automatic face* and *Forced spine*.",
            books=[
                ShelfBook(title="Automatic face", cover=cover),
                ShelfBook(title="Forced face", face=True, cover=cover),
                ShelfBook(title="Forced spine", face=False, cover=cover),
                ShelfBook(title="Automatic spine", cover=cover),
                ShelfBook(title="No cover", face=True),
                ShelfBook(title="Cover none", face=True, cover="none"),
            ],
        )
    ]

    _, shelves = shelves_from_file(sections)
    faces = {book["title"]: book["face"] for book in shelves[0]["books"]}

    assert faces == {
        "Automatic face": True,
        "Forced face": True,
        "Forced spine": False,
        "Automatic spine": False,
        "No cover": False,
        "Cover none": False,
    }


def test_rewriting_citations_recomposes_only_automatic_faces_without_reordering_books():
    cover = "https://example.test/cover.jpg"
    automatic_a = ShelfSection(
        title="My words",
        text="I begin with *Torto Arado*.",
        books=[ShelfBook(title="Torto Arado", cover=cover), ShelfBook(title="Cynefin", cover=cover)],
    )
    automatic_b = ShelfSection(
        title="My words",
        text="Now I begin with *Cynefin*.",
        books=[ShelfBook(title="Torto Arado", cover=cover), ShelfBook(title="Cynefin", cover=cover)],
    )
    explicit = ShelfSection(
        title="My words",
        text="Now I begin with *Cynefin*.",
        books=[
            ShelfBook(title="Torto Arado", face=True, cover=cover),
            ShelfBook(title="Cynefin", face=False, cover=cover),
        ],
    )

    _, shelves_a = shelves_from_file([automatic_a])
    _, shelves_b = shelves_from_file([automatic_b])
    _, shelves_explicit = shelves_from_file([explicit])

    assert [(book["title"], book["face"]) for book in shelves_a[0]["books"]] == [
        ("Torto Arado", True),
        ("Cynefin", False),
    ]
    assert [(book["title"], book["face"]) for book in shelves_b[0]["books"]] == [
        ("Torto Arado", False),
        ("Cynefin", True),
    ]
    assert [(book["title"], book["face"]) for book in shelves_explicit[0]["books"]] == [
        ("Torto Arado", True),
        ("Cynefin", False),
    ]


def test_only_the_canonical_last_section_is_the_generated_closing_shelf():
    custom = [
        ShelfSection(title="Primeira", text="Texto.", books=[]),
        ShelfSection(title="Uma prateleira minha", text="", books=[]),
    ]
    canonical = [
        ShelfSection(title="Primeira", text="Texto.", books=[]),
        ShelfSection(title=REST_TITLE, text="", books=[]),
    ]
    authored_closing = [ShelfSection(title=REST_TITLE, text="Meu fechamento.", books=[])]

    _, custom_shelves = shelves_from_file(custom)
    _, canonical_shelves = shelves_from_file(canonical)
    _, authored_shelves = shelves_from_file(authored_closing)

    assert not custom_shelves[1]["rest"]
    assert custom_shelves[1]["numeral"] == "II" and custom_shelves[1]["place"] == "side"
    assert canonical_shelves[1]["rest"]
    assert canonical_shelves[1]["numeral"] == "" and canonical_shelves[1]["place"] == "full"
    assert not authored_shelves[0]["rest"] and authored_shelves[0]["numeral"] == "I"


def test_themes_become_shelves_and_leftovers_go_to_the_last_one():
    books = [book("Torto Arado", 1), book("Cynefin"), book("Kanban", 2)]
    portrait = {
        "lens": "x",
        "themes": [{"title": "Quando penso na terra", "text": "*Torto Arado*", "books": [0]}],
    }
    shelves = build_shelves(books, portrait)
    assert [s["title"] for s in shelves] == ["Quando penso na terra", REST_TITLE]
    assert [s["numeral"] for s in shelves] == ["I", ""]
    assert [b["title"] for b in shelves[0]["books"]] == ["Torto Arado"]
    assert [b["title"] for b in shelves[1]["books"]] == ["Cynefin", "Kanban"]
    assert shelves[1]["rest"] and shelves[1]["text"] == ""


def test_no_last_shelf_when_every_book_has_a_theme():
    shelves = build_shelves([book("A")], {"lens": "x", "themes": [{"title": "T", "text": "", "books": [0]}]})
    assert [s["title"] for s in shelves] == ["T"]


def test_cited_books_with_cover_face_out():
    books = [book("Torto Arado", 1), book("Angola Janga"), book("Kanban", 2)]
    portrait = {
        "lens": "x",
        "themes": [{"title": "T", "text": "*Torto Arado* e *Angola Janga*", "books": [0, 1, 2]}],
    }
    faces = {b["title"]: b["face"] for b in build_shelves(books, portrait)[0]["books"]}
    assert faces == {"Torto Arado": True, "Angola Janga": False, "Kanban": False}


def test_small_shelves_go_to_the_side_and_the_last_shelf_spans_the_page():
    books = [book(f"Livro {i}") for i in range(20)]
    portrait = {
        "lens": "x",
        "themes": [
            {"title": "Grande", "text": "", "books": list(range(SIDE_MAX + 1))},
            {"title": "Pequena", "text": "", "books": [SIDE_MAX + 1]},
        ],
    }
    assert [s["place"] for s in build_shelves(books, portrait)] == ["wide", "side", "full"]


def test_spines_and_tilts_are_stable_and_varied():
    assert spine("Torto Arado") == spine("Torto Arado")
    assert len({spine(f"Livro {i}")["color"] for i in range(40)}) > 5
    angles = [tilt(f"Livro {i}")[0] for i in range(40)]
    assert any(a < 0 for a in angles) and any(a > 0 for a in angles)
    assert all(1 <= abs(a) <= 4.5 for a in angles)
    long = spine("Um título bem comprido que não cabe inteiro na lombada do livro")
    assert long["width"] > spine("Scrum")["width"]
    assert long["label"].endswith("…")


def test_roman_numerals():
    assert [roman(n) for n in (1, 4, 6, 9, 12)] == ["I", "IV", "VI", "IX", "XII"]


def test_mosaic_fills_four_columns_for_any_number_of_photos():
    for n in range(1, 13):
        tiles = mosaic(n)
        assert len(tiles) == n
        assert tiles[0]["cols"] in (2, 4) and tiles[0]["rows"] == 2
        assert sum(t["cols"] * t["rows"] for t in tiles) % 4 == 0
    assert [t["cols"] for t in mosaic(7)] == [2, 1, 1, 1, 1, 2, 2]


def test_mosaic_shows_at_most_five_photos_on_phones():
    tiles = mosaic(7)
    assert [t["phone"] for t in tiles] == [True] * 5 + [False] * 2
    assert tiles[4]["more"] == 2


def test_first_shelf_stays_in_the_main_column_even_when_small():
    books = [book(f"Livro {i}") for i in range(3)]
    portrait = {
        "lens": "x",
        "themes": [{"title": "A", "text": "", "books": [0]}, {"title": "B", "text": "", "books": [1]}],
    }
    assert [s["place"] for s in build_shelves(books, portrait)] == ["wide", "side", "full"]


def test_spine_never_shows_a_surname_alone():
    assert spine("Continuo Preta", ["Bianca Santana"])["author"] == "Bianca Santana"
    assert spine("The Will to Change", ["bell hooks"])["author"] == "bell hooks"
    assert spine("Torto Arado", ["Itamar Vieira Junior"])["author"] == "Itamar Vieira Junior"
    assert spine("Decolonialidade", ["Joaze Bernardino-Costa"])["author"] == "Joaze Bernardino-Costa"
    assert spine("Cynefin", [])["author"] == ""
    assert spine("Cynefin", ["Dave Snowden"])["width"] > spine("Cynefin", [])["width"]
    assert (
        spine("Cynefin", ["Deivison Mendes Faustino"])["width"] > spine("Cynefin", ["Dave Snowden"])["width"]
    )


def test_short_name_keeps_first_name_particle_last_surname_and_suffix():
    assert short_name("Deivison Mendes Faustino") == "Deivison Mendes Faustino"
    assert short_name("Lidia Ruth Sánchez Mata") == "Lidia Ruth Sánchez Mata"
    assert short_name("Ronaldo de Oliveira Batista Ferreira") == "Ronaldo Ferreira"
    assert short_name("Matheus Gonçalves de Albuquerque Neto") == "Matheus de Albuquerque Neto"
    assert short_name("ANA FANI ALESSANDRI CARLOS") == "Ana Carlos"
    assert short_name("BIANCA SANTANA") == "Bianca Santana"
    assert short_name("Dom Paulo Evaristo Arns") == "Paulo Evaristo Arns"
    assert short_name("Gabriel José de la Concordia García Márquez") == "Gabriel Márquez"
    assert short_name("Plato") == "Plato"


def test_the_name_readers_explicitly_chose_always_wins():
    assert spine("Cem Anos", ["Gabriel José de la Concordia García Márquez"], "García Márquez")["author"] == (
        "García Márquez"
    )
    assert spine("Quarto de Despejo", ["Carolina Maria de Jesus"], "Carolina Maria de Jesus")["author"] == (
        "Carolina Maria de Jesus"
    )
    assert (
        spine("X", ["Fulano de Tal"], "Um nome longo demais para caber numa lombada")["author"]
        == "Um nome longo demais para caber numa lombada"
    )
    assert spine("X", ["Fulano de Tal"], "")["author"] == "Fulano de Tal"


def test_books_by_the_same_author_share_a_colour_and_sit_together():
    books = [
        {"title": "Mil Platôs Vol. 1", "authors": ["Gilles Deleuze"]},
        {"title": "Cynefin", "authors": []},
        {"title": "Mil Platôs Vol. 2", "authors": ["Gilles Deleuze", "Félix Guattari"]},
        {"title": "Pobreza urbana", "authors": ["Milton Santos"]},
        {"title": "Mil Platôs Vol. 3", "authors": ["Gilles  Deleuze"]},
    ]
    portrait = {"lens": "x", "themes": [{"title": "T", "text": "", "books": [0, 1, 2, 3, 4]}]}
    shelf = build_shelves(books, portrait)[0]["books"]
    assert [b["title"] for b in shelf] == [
        "Mil Platôs Vol. 1",
        "Mil Platôs Vol. 2",
        "Mil Platôs Vol. 3",
        "Cynefin",
        "Pobreza urbana",
    ]
    assert len({b["spine"]["color"] for b in shelf[:3]}) == 1


def test_frequent_authors_are_those_with_two_books_or_more_most_present_first():
    books = (
        [{"title": f"M{i}", "authors": ["Milton Santos"]} for i in range(3)]
        + [{"title": f"B{i}", "authors": ["bell hooks"]} for i in range(2)]
        + [{"title": "D", "authors": ["Gilles Deleuze"]}, {"title": "X", "authors": []}]
        + [{"title": "M3", "authors": ["Milton  Santos"]}]
    )
    assert frequent_authors(books) == ["Milton Santos", "bell hooks"]
    assert frequent_authors(books[5:]) == []


def test_a_google_books_cover_can_stand_face_out():
    books = [{"title": "Continuo Preta", "authors": [], "cover_url": "https://books.google.com/x"}]
    portrait = {"lens": "x", "themes": [{"title": "T", "text": "*Continuo Preta*", "books": [0]}]}
    assert build_shelves(books, portrait)[0]["books"][0]["face"] is True
