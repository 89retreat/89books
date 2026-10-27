from shelf.shelves import REST_TITLE, SIDE_MAX, build_shelves, frequent_authors, mosaic, roman, spine, tilt


def book(title, cover_id=None):
    return {"title": title, "authors": [], "cover_id": cover_id}


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


def test_spine_names_the_author_in_full_when_short_and_by_surname_when_long():
    assert spine("Continuo Preta", ["Bianca Santana"])["author"] == "Bianca Santana"
    assert spine("The Will to Change", ["bell hooks"])["author"] == "bell hooks"
    assert spine("Leviatã", ["Thomas Hobbes"])["author"] == "Thomas Hobbes"
    assert spine("Torto Arado", ["Itamar Vieira Junior"])["author"] == "Vieira Junior"
    assert spine("Decolonialidade", ["Joaze Bernardino-Costa"])["author"] == "Bernardino-Costa"
    assert spine("Cynefin", [])["author"] == ""
    assert spine("Cynefin", ["Dave Snowden"])["width"] > spine("Cynefin", [])["width"]


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
