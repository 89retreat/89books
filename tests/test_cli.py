from shelf.cli import build_shelf, main
from shelf.config import load_config
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


def test_build_shelf_writes_private_self_contained_html_and_books_yaml(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    lines = []
    result = build_shelf(
        config,
        recognize=fake_recognize,
        library=FakeLibrary(),
        portrait=fake_portrait,
        review=no_review,
        covers=FakeCovers(),
        log=lines.append,
    )

    html = (shelf_folder / "shelf.html").read_text(encoding="utf-8")
    assert result.books == 2  # duplicates across the two photos are merged
    assert result.cost == 0.05
    assert "sk-secret" not in html
    assert str(shelf_folder) not in html
    assert "SecretCam" not in html
    assert html.count("data:image/jpeg;base64,") == 2
    assert "Eu olho a terra." in html
    assert "Quando penso na terra" in html
    assert REST_TITLE in html  # Cynefin has no theme
    assert "books:" in (shelf_folder / "books.yaml").read_text(encoding="utf-8")
    assert any("2 books" in line for line in lines)
    assert any("US$ 0.05" in line for line in lines)


def test_main_reports_missing_key_without_calling_the_model(shelf_folder, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    assert main([str(shelf_folder)]) == 2
    assert "OPENROUTER_API_KEY" in capsys.readouterr().err
    assert not (shelf_folder / "shelf.html").exists()


def test_a_cover_that_is_not_a_cover_becomes_a_spine(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    build_shelf(
        config,
        recognize=fake_recognize,
        library=FakeLibrary(),
        portrait=fake_portrait,
        review=no_review,
        covers=FakeCovers(),
        log=lambda line: None,
    )
    html = (shelf_folder / "shelf.html").read_text(encoding="utf-8")
    assert "covers.openlibrary.org" not in html
    assert "Torto Arado" in html


def test_the_review_corrects_a_misread_title_before_the_page(shelf_folder):
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

    lines = []
    result = build_shelf(
        config,
        recognize=recognize,
        library=FakeLibrary(),
        portrait=portrait,
        review=review,
        covers=FakeCovers(),
        log=lines.append,
    )
    html = (shelf_folder / "shelf.html").read_text(encoding="utf-8")
    books_yaml = (shelf_folder / "books.yaml").read_text(encoding="utf-8")
    assert result.books == 1
    assert "Continuo Preta" in html and "Carneiro" in html and "Caneca" not in html
    assert "read_as: Continuo Preto" in books_yaml and "not a book" in books_yaml
    assert any("Google Books" in line and "GOOGLE_BOOKS_API_KEY" in line for line in lines)
    assert any("1 corrected" in line for line in lines)


def test_google_books_confirms_titles_after_the_review(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    def recognize(image, api_key):
        return [{"title": "Contínuo Preto", "authors": []}], 0.0

    def review(books, api_key):
        return (
            {0: {"title": "Continuo Preto: A Vida de Sueli Carneiro", "authors": ["Bianca Santana"]}},
            0.0,
            {},
        )

    class Second:
        seen = []

        def lookup(self, title, authors):
            self.seen.append((title, authors))
            return {"gb_title": "Continuo preta", "gb_authors": ["Bianca Santana"], "gb_cover": None}

        def save(self):
            pass

    def portrait(books, api_key):
        return {"lens": "Eu.", "themes": []}, 0.0

    second = Second()
    build_shelf(
        config,
        recognize=recognize,
        library=FakeLibrary(),
        portrait=portrait,
        review=review,
        second=second,
        covers=FakeCovers(),
        log=lambda line: None,
    )
    assert second.seen[0] == ("Continuo Preto: A Vida de Sueli Carneiro", ["Bianca Santana"])
    books_yaml = (shelf_folder / "books.yaml").read_text(encoding="utf-8")
    assert "title: Continuo preta" in books_yaml and "source: google_books" in books_yaml


class Steps:
    def __init__(self):
        self.calls = []

    def start(self, total):
        self.calls.append(("start", total))

    def step(self, title):
        self.calls.append(("step", title))

    def finish(self):
        self.calls.append(("finish",))


def test_every_catalogue_lookup_moves_the_progress(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    steps = Steps()
    build_shelf(
        config,
        recognize=fake_recognize,
        library=FakeLibrary(),
        portrait=fake_portrait,
        review=no_review,
        covers=FakeCovers(),
        log=lambda line: None,
        progress=steps,
    )
    assert steps.calls[0] == ("start", 2)  # two books after merging duplicates
    first = steps.calls[1 : steps.calls.index(("finish",))]
    assert len(first) == 2 and all(c[0] == "step" for c in first)
    assert steps.calls.count(("finish",)) == sum(1 for c in steps.calls if c[0] == "start")


def test_spines_use_the_name_the_review_gave(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})

    def recognize(jpeg, api_key):
        return [{"title": "Quarto de Despejo", "authors": ["Carolina Maria de Jesus Silva"]}], 0.0

    def review(books, api_key):
        return {}, 0.01, {"carolina silva": "Carolina Maria de Jesus"}

    build_shelf(
        config,
        recognize=recognize,
        library=FakeLibrary(),
        portrait=fake_portrait,
        review=review,
        covers=FakeCovers(),
        log=lambda line: None,
    )
    html = (shelf_folder / "shelf.html").read_text(encoding="utf-8")
    assert "<b>Carolina Maria de Jesus</b>" in html
    assert "known_as: Carolina Maria de Jesus" in (shelf_folder / "books.yaml").read_text(encoding="utf-8")
