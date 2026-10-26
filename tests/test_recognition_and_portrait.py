import pytest

from shelf.portrait import book_list, parse_portrait
from shelf.recognition import parse_books


def test_parse_books_ignores_text_around_json_and_empty_titles():
    text = 'Here: {"books": [{"title": "Torto Arado", "authors": ["Itamar"]}, {"title": " "}]} done'
    assert parse_books(text) == [{"title": "Torto Arado", "authors": ["Itamar"]}]


def test_book_list_numbers_books_and_prefers_open_library_title():
    books = [
        {
            "title": "quarto de despejo",
            "ol_title": "Quarto de Despejo",
            "authors": ["Carolina Maria de Jesus"],
        },
        {"title": "Cynefin", "authors": []},
    ]
    assert book_list(books) == "1. Quarto de Despejo — Carolina Maria de Jesus\n2. Cynefin"


def test_parse_portrait_reads_lens_situation_titles_and_books_per_theme():
    text = (
        '```json\n{"lens": "Eu olho estruturas.", "themes": ['
        '{"title": "Quando penso a cidade", "text": "*O direito à cidade*", "books": [2, 1]}]}\n```'
    )
    portrait = parse_portrait(text, book_count=3)
    assert portrait["lens"] == "Eu olho estruturas."
    assert portrait["themes"] == [
        {"title": "Quando penso a cidade", "text": "*O direito à cidade*", "books": [1, 0]}
    ]


def test_parse_portrait_drops_invalid_and_repeated_books():
    text = (
        '{"lens": "x", "themes": ['
        '{"title": "A", "text": "a", "books": [1, 1, 9, 0, "2"]},'
        '{"title": "B", "text": "b", "books": [1, 3]},'
        '{"title": " ", "text": "sem título", "books": [2]}]}'
    )
    themes = parse_portrait(text, book_count=3)["themes"]
    assert [t["books"] for t in themes] == [[0], [2]]
    assert [t["title"] for t in themes] == ["A", "B"]


def test_parse_portrait_rejects_missing_lens():
    with pytest.raises(ValueError):
        parse_portrait('{"themes": []}', book_count=0)
