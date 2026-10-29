import pytest

from shelf import portrait
from shelf.portrait import PortraitResponseError, book_list, parse_portrait, write_portrait
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


def test_write_portrait_requests_schema_constrained_json(monkeypatch):
    seen = {}

    def complete(api_key, content, max_tokens, temperature, response_format=None):
        seen.update(
            api_key=api_key,
            content=content,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
        )
        return '{"lens":"Eu leio.","themes":[]}', 0.012

    monkeypatch.setattr(portrait.openrouter, "complete", complete)

    result, cost = write_portrait([{"title": "Torto Arado", "authors": []}], "sk-secret")

    assert result == {"lens": "Eu leio.", "themes": []} and cost == 0.012
    assert seen["response_format"]["type"] == "json_schema"
    schema = seen["response_format"]["json_schema"]["schema"]
    assert schema["required"] == ["lens", "themes"]
    assert schema["properties"]["themes"]["items"]["required"] == ["title", "text", "books"]


def test_write_portrait_preserves_invalid_response_and_cost_for_private_recovery(monkeypatch):
    monkeypatch.setattr(
        portrait.openrouter,
        "complete",
        lambda *args, **kwargs: ('{"lens":"quebrou" "themes":[]}', 0.013),
    )

    with pytest.raises(PortraitResponseError) as failed:
        write_portrait([{"title": "Torto Arado", "authors": []}], "sk-secret")

    assert failed.value.response == '{"lens":"quebrou" "themes":[]}'
    assert failed.value.cost == 0.013
    assert "JSON" in str(failed.value) and "Torto Arado" not in str(failed.value)
