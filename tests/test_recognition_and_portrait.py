import pytest

from shelf.portrait import book_list, parse_portrait
from shelf.recognition import parse_books


def test_parse_books_ignores_text_around_json_and_empty_titles():
    text = 'Here: {"books": [{"title": "Torto Arado", "authors": ["Itamar"]}, {"title": " "}]} done'
    assert parse_books(text) == [{"title": "Torto Arado", "authors": ["Itamar"]}]


def test_book_list_prefers_open_library_title_and_skips_repeats():
    books = [
        {
            "title": "quarto de despejo",
            "ol_title": "Quarto de Despejo",
            "authors": ["Carolina Maria de Jesus"],
        },
        {"title": "Cynefin", "authors": []},
        {"title": "Cynefin", "authors": []},
    ]
    assert book_list(books) == "- Quarto de Despejo — Carolina Maria de Jesus\n- Cynefin"


def test_parse_portrait_reads_lens_and_themes():
    text = '```json\n{"lens": "Você olha estruturas.", "themes": [{"name": "Cidade", "text": "*O direito à cidade*"}]}\n```'
    portrait = parse_portrait(text)
    assert portrait["lens"] == "Você olha estruturas."
    assert portrait["themes"][0]["name"] == "Cidade"


def test_parse_portrait_rejects_missing_lens():
    with pytest.raises(ValueError):
        parse_portrait('{"themes": []}')
