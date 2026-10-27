from shelf.review import apply_review, book_lines, parse_review, settle


def test_book_lines_show_what_was_read_and_what_the_catalogues_found():
    books = [
        {"title": "Continuo Preto", "authors": []},
        {
            "title": "Torto Arado",
            "authors": ["Itamar"],
            "ol_title": "Torto arado",
            "ol_authors": ["Itamar Vieira Junior"],
        },
        {"title": "Cntinuo", "authors": [], "gb_title": "Continuo Preta", "gb_authors": ["Sueli Carneiro"]},
    ]
    lines = book_lines(books).splitlines()
    assert lines[0] == "1. lido: Continuo Preto"
    assert lines[1] == "2. lido: Torto Arado — Itamar | Open Library: Torto arado — Itamar Vieira Junior"
    assert lines[2] == "3. lido: Cntinuo | Google Books: Continuo Preta — Sueli Carneiro"


def test_parse_review_keeps_valid_entries_and_the_first_for_each_book():
    text = """```json
    {"books": [
      {"n": 1, "title": "Continuo Preta", "authors": ["Sueli Carneiro"]},
      {"n": 1, "title": "outra"},
      {"n": 2, "same_as": 3},
      {"n": 4, "not_a_book": true},
      {"n": 9, "title": "fora da lista"},
      {"n": 3, "same_as": 3},
      {"n": "2", "title": "texto"}
    ]}```"""
    entries = parse_review(text, book_count=4)
    assert entries == {
        0: {"title": "Continuo Preta", "authors": ["Sueli Carneiro"]},
        1: {"same_as": 2},
        3: {"not_a_book": True},
    }


def test_apply_review_corrects_merges_and_leaves_out_with_a_reason():
    books = [
        {"title": "Continuo Preto", "authors": []},
        {"title": "O Pai Prezado", "authors": []},
        {"title": "Ó pa í, Prezada!", "authors": ["Carla Akotirene"]},
        {"title": "Caneca", "authors": []},
    ]
    entries = {
        0: {"title": "Continuo Preta", "authors": ["Sueli Carneiro"]},
        1: {"same_as": 2},
        3: {"not_a_book": True},
    }
    kept, left_out = apply_review(books, entries)
    assert [b["title"] for b in kept] == ["Continuo Preta", "Ó pa í, Prezada!"]
    assert kept[0]["authors"] == ["Sueli Carneiro"] and kept[0]["read_as"] == "Continuo Preto"
    assert kept[0]["source"] == "review"
    assert left_out == [
        {"title": "O Pai Prezado", "reason": "same book as Ó pa í, Prezada!"},
        {"title": "Caneca", "reason": "not a book"},
    ]


def test_a_merged_book_gives_its_authors_to_the_one_kept():
    books = [{"title": "Ó pa í", "authors": []}, {"title": "O Pai Prezado", "authors": ["Carla Akotirene"]}]
    kept, _ = apply_review(books, {1: {"same_as": 0}})
    assert kept == [{"title": "Ó pa í", "authors": ["Carla Akotirene"]}]


def test_settle_prefers_review_then_open_library_then_google_books():
    reviewed = settle(
        {"title": "Continuo Preta", "source": "review", "ol_title": "Outro", "authors": ["Sueli"]}
    )
    assert reviewed["title"] == "Continuo Preta" and "ol_title" not in reviewed
    from_ol = settle(
        {"title": "torto arado", "authors": [], "ol_title": "Torto Arado", "ol_authors": ["Itamar"]}
    )
    assert (from_ol["title"], from_ol["authors"], from_ol["source"]) == (
        "Torto Arado",
        ["Itamar"],
        "open_library",
    )
    assert from_ol["read_as"] == "torto arado"
    from_gb = settle(
        {"title": "Continuo Preto", "authors": [], "gb_title": "Continuo Preta", "gb_authors": ["S"]}
    )
    assert (from_gb["title"], from_gb["source"]) == ("Continuo Preta", "google_books")
    as_read = settle({"title": "Cynefin", "authors": []})
    assert as_read == {"title": "Cynefin", "authors": [], "source": "photo"}
