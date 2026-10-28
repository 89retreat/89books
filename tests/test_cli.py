import pytest

from shelf import cli
from shelf.cli import CommandError, create_shelf, draw_shelf, open_shelf
from shelf.config import load_config
from shelf.shelf_file import ShelfYamlError, dump_shelf, parse_shelf
from shelf.shelves import REST_TITLE


class FakeCovers:
    def ok(self, cover):
        return cover != 42

    def save(self):
        pass


class FakeLibrary:
    def lookup(self, title, authors):
        if title == "Torto Arado":
            return {"work": "/works/OL1W", "ol_title": "Torto Arado", "cover_id": 42}
        return None

    def save(self):
        pass


def fake_recognize(image: bytes, api_key: str):
    assert api_key == "sk-secret"
    return [
        {"title": "Torto Arado", "authors": ["Itamar Vieira Junior"]},
        {"title": "Cynefin", "authors": []},
    ], 0.02


def no_review(books, api_key):
    return {}, 0.0, {}


def fake_portrait(books, api_key):
    portrait = {
        "lens": "Eu olho a terra.",
        "themes": [{"title": "Quando penso na terra", "text": "*Torto Arado*", "books": [0]}],
    }
    return portrait, 0.01


def create_with_fakes(config, **overrides):
    arguments = dict(
        recognize=fake_recognize,
        library=FakeLibrary(),
        portrait=fake_portrait,
        review=no_review,
        covers=FakeCovers(),
        log=lambda line: None,
    )
    return create_shelf(config, **{**arguments, **overrides})


def all_books(shelf):
    return [book for section in shelf.shelves for book in section.books]


def test_create_writes_only_the_versioned_source(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    lines = []
    result = create_with_fakes(config, log=lines.append)

    shelf_path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(shelf_path.read_text(encoding="utf-8"))
    assert result.books == 2 and result.cost == 0.05 and result.migrated is False
    assert shelf.name is None and shelf.cover_photo == "photo-01.jpg"
    assert [section.title for section in shelf.shelves] == ["Quando penso na terra", REST_TITLE]
    assert not (shelf_folder / "shelf.html").exists()
    assert not (shelf_folder / "books.yaml").exists()
    assert any("2 books" in line for line in lines)


def test_create_moves_the_legacy_cover_photo_choice_into_shelf_yaml(shelf_folder):
    (shelf_folder / "config.toml").write_text('cover_photo = "photo-02.jpg"\n')
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    create_with_fakes(config)

    shelf = parse_shelf((shelf_folder / "shelf.yaml").read_text(encoding="utf-8"))
    assert shelf.cover_photo == "photo-02.jpg"


def test_create_refuses_to_replace_an_existing_shelf(shelf_folder):
    existing = shelf_folder / "shelf.yaml"
    existing.write_text("do not replace\n", encoding="utf-8")
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    with pytest.raises(CommandError, match="already exists"):
        create_with_fakes(config)

    assert existing.read_text(encoding="utf-8") == "do not replace\n"


def test_review_and_catalogues_are_preserved_in_shelf_yaml(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    def recognize(image, api_key):
        return [{"title": "Continuo Preto", "authors": []}, {"title": "Caneca", "authors": []}], 0.02

    def review(books, api_key):
        titles = [b["title"] for b in books]
        return (
            {
                titles.index("Continuo Preto"): {"title": "Continuo Preta", "authors": ["Sueli Carneiro"]},
                titles.index("Caneca"): {"not_a_book": True},
            },
            0.01,
            {},
        )

    def portrait(books, api_key):
        return {
            "lens": "Eu.",
            "themes": [{"title": "Quando penso", "text": "*Continuo Preta*", "books": [0]}],
        }, 0.0

    result = create_with_fakes(config, recognize=recognize, review=review, portrait=portrait)
    shelf = parse_shelf((shelf_folder / "shelf.yaml").read_text(encoding="utf-8"))
    book = all_books(shelf)[0]
    assert result.books == 1
    assert book.title == "Continuo Preta" and book.authors == ["Sueli Carneiro"]
    assert book.read_as == "Continuo Preto" and book.source == "review"
    assert shelf.left_out[0].title == "Caneca" and shelf.left_out[0].reason == "not a book"


def test_google_books_progress_and_known_author_name_reach_the_file(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    def recognize(image, api_key):
        return [{"title": "Contínuo Preto", "authors": ["Carolina Maria de Jesus Silva"]}], 0.0

    def review(books, api_key):
        return (
            {0: {"title": "Continuo Preto: A Vida", "authors": ["Carolina Maria de Jesus Silva"]}},
            0.0,
            {"carolina silva": "Carolina Maria de Jesus"},
        )

    class Second:
        seen = []

        def lookup(self, title, authors):
            self.seen.append((title, authors))
            return {
                "gb_title": "Continuo preta",
                "gb_authors": ["Carolina Maria de Jesus Silva"],
                "gb_cover": None,
            }

        def save(self):
            pass

    class Steps:
        def __init__(self):
            self.calls = []

        def start(self, total):
            self.calls.append(("start", total))

        def step(self, title):
            self.calls.append(("step", title))

        def finish(self):
            self.calls.append(("finish",))

    second, steps = Second(), Steps()
    create_with_fakes(config, recognize=recognize, review=review, second=second, progress=steps)
    book = all_books(parse_shelf((shelf_folder / "shelf.yaml").read_text(encoding="utf-8")))[0]
    assert second.seen[0][0] == "Continuo Preto: A Vida"
    assert book.title == "Continuo preta" and book.source == "google_books"
    assert book.known_as == "Carolina Maria de Jesus"
    assert steps.calls.count(("finish",)) == sum(1 for call in steps.calls if call[0] == "start")


def test_migration_writes_shelf_yaml_and_leaves_books_yaml_untouched(shelf_folder):
    legacy_path = shelf_folder / "books.yaml"
    legacy = """\
books:
  - title: Torto Arado
    authors: [Itamar Vieira Junior]
    cover_url: https://example.test/torto.jpg
    source: open_library
left_out:
  - title: Caneca
    reason: not a book
"""
    legacy_path.write_text(legacy, encoding="utf-8")
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    def forbidden(*args, **kwargs):
        raise AssertionError("migration called recognition or review")

    class Forbidden:
        def __getattr__(self, name):
            raise AssertionError(f"migration called {name}")

    result = create_shelf(
        config,
        legacy_books=legacy,
        recognize=forbidden,
        review=forbidden,
        library=Forbidden(),
        second=Forbidden(),
        covers=Forbidden(),
        portrait=fake_portrait,
        log=lambda line: None,
    )
    shelf = parse_shelf((shelf_folder / "shelf.yaml").read_text(encoding="utf-8"))
    assert result.migrated is True and result.cost == 0.01
    assert all_books(shelf)[0].cover == "https://example.test/torto.jpg"
    assert legacy_path.read_text(encoding="utf-8") == legacy


def test_draw_is_free_self_contained_and_uses_only_shelf_yaml(shelf_folder, monkeypatch):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_BOOKS_API_KEY", raising=False)

    source = (shelf_folder / "shelf.yaml").read_bytes()
    result = draw_shelf(shelf_folder)
    html = result.html.read_text(encoding="utf-8")
    assert result.books == 2
    assert "Eu olho a terra." in html and "Torto Arado" in html
    assert html.count("data:image/jpeg;base64,") == 2
    assert str(shelf_folder) not in html and "SecretCam" not in html
    assert "sk-secret" not in html
    assert (shelf_folder / "shelf.yaml").read_bytes() == source


def test_draw_reflects_file_edits_and_shelf_order(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.lens = "Eu escolho como esta página me apresenta."
    shelf.shelves.reverse()
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    draw_shelf(shelf_folder)
    html = (shelf_folder / "shelf.html").read_text(encoding="utf-8")
    assert "Eu escolho como esta página me apresenta." in html
    assert html.index(REST_TITLE) < html.index("Quando penso na terra")


def test_invalid_yaml_or_missing_cover_photo_never_replaces_the_page(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    draw_shelf(shelf_folder)
    page = shelf_folder / "shelf.html"
    before = page.read_bytes()
    shelf_path = shelf_folder / "shelf.yaml"

    shelf_path.write_text("version: 1\nlens: [broken\n", encoding="utf-8")
    with pytest.raises(ShelfYamlError):
        draw_shelf(shelf_folder)
    assert page.read_bytes() == before


def test_render_failure_never_replaces_the_page(shelf_folder, monkeypatch):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    draw_shelf(shelf_folder)
    page = shelf_folder / "shelf.html"
    before = page.read_bytes()

    def broken_render(*args, **kwargs):
        raise RuntimeError("template broke")

    monkeypatch.setattr(cli.core, "draw", broken_render)
    with pytest.raises(RuntimeError, match="template broke"):
        draw_shelf(shelf_folder)
    assert page.read_bytes() == before


def test_missing_cover_photo_never_replaces_the_page(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    draw_shelf(shelf_folder)
    page = shelf_folder / "shelf.html"
    before = page.read_bytes()
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.cover_photo = "missing.jpg"
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    with pytest.raises(CommandError, match="cover_photo"):
        draw_shelf(shelf_folder)
    assert page.read_bytes() == before


def test_open_uses_a_file_uri_and_requires_a_page(shelf_folder):
    seen = []
    with pytest.raises(CommandError, match="draw"):
        open_shelf(shelf_folder, opener=seen.append)

    page = shelf_folder / "shelf.html"
    page.write_text("page", encoding="utf-8")
    assert open_shelf(shelf_folder, opener=seen.append) == page
    assert seen == [page.resolve().as_uri()]
