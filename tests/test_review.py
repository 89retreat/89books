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


def test_confirm_takes_the_catalogue_spelling_of_a_reviewed_title():
    from shelf.review import confirm

    book = {
        "title": "Continuo Preto: A Vida de Sueli Carneiro",
        "authors": ["Bianca Santana"],
        "read_as": "Contínuo Preto",
        "source": "review",
    }
    found = {"gb_title": "Continuo preta", "gb_authors": ["Bianca Santana"], "gb_cover": "https://x"}
    confirmed = confirm(book, found)
    assert confirmed["title"] == "Continuo preta"
    assert confirmed["read_as"] == "Contínuo Preto" and confirmed["source"] == "google_books"
    assert confirmed["gb_cover"] == "https://x"


def test_confirm_gives_authors_to_a_book_read_from_the_photo_only():
    from shelf.review import confirm

    confirmed = confirm(
        {"title": "Fumo sem Cortes", "authors": [], "source": "photo"},
        {"gb_title": "Fumo sem cortes", "gb_authors": ["Autora"], "gb_cover": None},
    )
    assert confirmed["authors"] == ["Autora"] and confirmed["title"] == "Fumo sem Cortes"
    assert "read_as" not in confirmed


def test_confirm_keeps_the_title_when_only_case_or_accents_differ():
    from shelf.review import confirm

    confirmed = confirm(
        {"title": "Regras para Radicais", "authors": ["Saul Alinsky"], "source": "photo"},
        {"gb_title": "Regras para radicais", "gb_authors": ["Saul Alinsky"], "gb_cover": None},
    )
    assert confirmed["title"] == "Regras para Radicais" and "read_as" not in confirmed
    assert confirmed["source"] == "google_books"


def test_a_broken_answer_keeps_every_item_that_can_be_read():
    text = """{"books": [
      {"n": 1, "title": "Continuo preta", "authors": ["Bianca Santana"]},
      {"n": 2, "title": "Homens Pretos "(Não)" Choram", "authors": ["X"]},
      {"n": 3, "not_a_book": true}
    ]}"""
    assert parse_review(text, book_count=3) == {
        0: {"title": "Continuo preta", "authors": ["Bianca Santana"]},
        2: {"not_a_book": True},
    }
