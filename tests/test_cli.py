from shelf.cli import build_shelf, main
from shelf.config import load_config


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
        config, recognize=fake_recognize, library=FakeLibrary(), portrait=fake_portrait, log=lines.append
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
    assert "Quando não procuro nada em particular" in html  # Cynefin has no theme
    assert "books:" in (shelf_folder / "books.yaml").read_text(encoding="utf-8")
    assert any("2 books" in line for line in lines)
    assert any("US$ 0.05" in line for line in lines)


def test_main_reports_missing_key_without_calling_the_model(shelf_folder, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    assert main([str(shelf_folder)]) == 2
    assert "OPENROUTER_API_KEY" in capsys.readouterr().err
    assert not (shelf_folder / "shelf.html").exists()
