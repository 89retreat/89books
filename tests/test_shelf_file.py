import ast
from pathlib import Path

import pytest

from shelf import shelf_file
from shelf.shelf_file import (
    LeftOutBook,
    ShelfBook,
    ShelfFile,
    ShelfSection,
    ShelfYamlError,
    dump_shelf,
    parse_shelf,
)

MODULE = Path(shelf_file.__file__)

VALID = """\
version: 1
name: Lula
cover_photo: estante-lula-foto-03.jpeg
lens: |
  Eu olho o mundo como quem quer entender.
  A terra também me olha.
shelves:
  - title: Quando penso o Brasil
    text: |
      Esta é a prateleira que mais me move.
    books:
      - title: Quarto de Despejo
        authors: [Carolina Maria de Jesus]
        known_as: Carolina Maria de Jesus
        face: true
        cover: https://example.test/quarto.jpg
        read_as: Quarto de Desejo
        source: review
        photo: foto-03.jpeg
        work: /works/OL123W
      - title: O Pai Prezado
        hidden: true
      - title: Manual de Lombada
        authors: []
        face: false
        hidden: false
        cover: none
left_out:
  - title: Companhia das Letras
    reason: not a book
"""


def test_parse_shelf_returns_typed_data_in_page_order():
    shelf = parse_shelf(VALID)

    assert shelf == ShelfFile(
        version=1,
        name="Lula",
        cover_photo="estante-lula-foto-03.jpeg",
        lens="Eu olho o mundo como quem quer entender.\nA terra também me olha.\n",
        shelves=[
            ShelfSection(
                title="Quando penso o Brasil",
                text="Esta é a prateleira que mais me move.\n",
                books=[
                    ShelfBook(
                        title="Quarto de Despejo",
                        authors=["Carolina Maria de Jesus"],
                        known_as="Carolina Maria de Jesus",
                        face=True,
                        cover="https://example.test/quarto.jpg",
                        read_as="Quarto de Desejo",
                        source="review",
                        photo="foto-03.jpeg",
                        work="/works/OL123W",
                    ),
                    ShelfBook(title="O Pai Prezado", hidden=True),
                    ShelfBook(
                        title="Manual de Lombada",
                        authors=[],
                        face=False,
                        hidden=False,
                        cover="none",
                    ),
                ],
            )
        ],
        left_out=[LeftOutBook(title="Companhia das Letras", reason="not a book")],
    )


def test_dump_is_stable_readable_and_preserves_explicit_choices():
    shelf = parse_shelf(VALID)
    dumped = dump_shelf(shelf)

    assert dumped.startswith("version: 1\nname: Lula\ncover_photo:")
    assert "lens: |" in dumped and "text: |" in dumped
    assert "face: false" in dumped and "hidden: false" in dumped and "cover: none" in dumped
    assert dump_shelf(parse_shelf(dumped)) == dumped
    assert parse_shelf(dumped) == shelf


def test_optional_name_text_authors_and_left_out_may_be_absent():
    shelf = parse_shelf(
        """\
version: 1
cover_photo: shelf.jpg
lens: ''
shelves:
  - title: Só os livros
    books:
      - title: Sem autoria conhecida
"""
    )

    assert shelf.name is None
    assert shelf.lens == ""
    assert shelf.shelves[0].text == ""
    assert shelf.shelves[0].books[0].authors == []
    assert shelf.left_out == []
    assert parse_shelf(dump_shelf(shelf)) == shelf


def test_parse_reports_every_detectable_problem_with_line_and_path():
    text = """\
version: 2
cover_photo: 3
lens: tudo certo
shelves:
  - title: 7
    books:
      - title: Um livro
        fcae: true
      - authors: Ana
        hidden: talvez
left_out:
  - title: Objeto
"""

    with pytest.raises(ShelfYamlError) as caught:
        parse_shelf(text)

    issues = caught.value.issues
    assert [(i.line, i.path) for i in issues] == [
        (1, "version"),
        (2, "cover_photo"),
        (5, "shelves[0].title"),
        (8, "shelves[0].books[0].fcae"),
        (9, "shelves[0].books[1].title"),
        (9, "shelves[0].books[1].authors"),
        (10, "shelves[0].books[1].hidden"),
        (12, "left_out[0].reason"),
    ]
    assert "unsupported version" in issues[0].message
    assert "unknown field" in issues[3].message
    assert all(str(issue).startswith(f"line {issue.line}: {issue.path}:") for issue in issues)


def test_duplicate_keys_are_rejected_at_the_second_occurrence():
    text = """\
version: 1
cover_photo: first.jpg
cover_photo: second.jpg
lens: Eu leio.
shelves: []
"""

    with pytest.raises(ShelfYamlError) as caught:
        parse_shelf(text)

    assert [(i.line, i.path, i.message) for i in caught.value.issues] == [
        (3, "cover_photo", "duplicate field"),
    ]


def test_yaml_boolean_shorthands_stay_available_as_titles_and_names():
    shelf = parse_shelf(
        """\
version: 1
name: Yes
cover_photo: shelf.jpg
lens: Eu leio.
shelves:
  - title: On
    books:
      - title: No
        authors: [Off]
"""
    )

    assert shelf.name == "Yes"
    assert shelf.shelves[0].title == "On"
    assert shelf.shelves[0].books[0] == ShelfBook(title="No", authors=["Off"])


def test_booleans_are_written_as_true_or_false_not_yaml_shorthands():
    text = """\
version: 1
cover_photo: shelf.jpg
lens: Eu leio.
shelves:
  - title: Uma prateleira
    books:
      - title: Um livro
        face: yes
"""

    with pytest.raises(ShelfYamlError) as caught:
        parse_shelf(text)

    assert [(i.line, i.path, i.message) for i in caught.value.issues] == [
        (8, "shelves[0].books[0].face", "must be true or false"),
    ]


def test_yaml_syntax_error_has_a_line_and_returns_no_document():
    with pytest.raises(ShelfYamlError) as caught:
        parse_shelf("version: 1\ncover_photo: shelf.jpg\nlens: [broken\nshelves: []\n")

    assert caught.value.issues[0].line == 4
    assert caught.value.issues[0].path == "$"
    assert "YAML syntax" in caught.value.issues[0].message


def test_missing_or_future_version_is_never_guessed():
    base = "cover_photo: shelf.jpg\nlens: Eu leio.\nshelves: []\n"

    with pytest.raises(ShelfYamlError) as missing:
        parse_shelf(base)
    with pytest.raises(ShelfYamlError) as future:
        parse_shelf("version: 9\n" + base)

    assert missing.value.issues[0].path == "version"
    assert "required" in missing.value.issues[0].message
    assert future.value.issues[0].path == "version"
    assert "unsupported version 9" in future.value.issues[0].message


def test_empty_document_and_non_mapping_root_are_clear_errors():
    for text in ("", "- version\n- 1\n"):
        with pytest.raises(ShelfYamlError) as caught:
            parse_shelf(text)
        assert caught.value.issues[0].path == "$"
        assert caught.value.issues[0].line == 1


def test_shelf_file_module_never_talks_to_the_terminal_or_filesystem():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert not calls & {"print", "input", "open"}

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    forbidden = ("pathlib", "os", "sys", "getpass", "shelf.cli", "shelf.setup", "shelf.config")
    assert not {module for module in imported if module.startswith(forbidden)}
