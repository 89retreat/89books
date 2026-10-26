import yaml

from shelf.books import dedupe, write_books_yaml


def test_dedupe_merges_same_title_across_photos():
    books = [
        {"title": "Pensando em Sistemas", "authors": ["Donella Meadows"], "photo": "photo-01.jpg"},
        {"title": "Pensando em sistemas", "authors": [], "photo": "photo-02.jpg"},
        {"title": "Torto Arado", "authors": ["Itamar Vieira Junior"], "photo": "photo-02.jpg"},
    ]
    assert [b["title"] for b in dedupe(books)] == ["Pensando em Sistemas", "Torto Arado"]


def test_books_yaml_lists_books_without_local_paths(tmp_path):
    path = tmp_path / "books.yaml"
    write_books_yaml(
        path,
        [
            {
                "title": "Torto Arado",
                "authors": ["Itamar Vieira Junior"],
                "photo": "photo-02.jpg",
                "work": "/works/OL1W",
                "cover_id": 42,
            }
        ],
    )
    text = path.read_text(encoding="utf-8")
    assert text.startswith("#")
    assert str(tmp_path) not in text
    data = yaml.safe_load(text)
    assert data["books"][0] == {
        "title": "Torto Arado",
        "authors": ["Itamar Vieira Junior"],
        "photo": "photo-02.jpg",
        "work": "/works/OL1W",
        "cover_id": 42,
    }
