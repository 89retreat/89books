from shelf.googlebooks import GoogleBooks


def volume(title, authors, thumbnail=None):
    info = {"title": title, "authors": authors}
    if thumbnail:
        info["imageLinks"] = {"thumbnail": thumbnail}
    return {"volumeInfo": info}


def test_lookup_takes_the_first_similar_title_with_an_https_cover(tmp_path):
    calls = []

    def fetch(params):
        calls.append(params)
        return {
            "items": [
                volume("Outro livro", ["X"]),
                volume(
                    "Continuo Preta",
                    ["Sueli Carneiro"],
                    "http://books.google.com/books/content?id=A&printsec=frontcover&img=1&zoom=1&edge=curl",
                ),
            ]
        }

    books = GoogleBooks(tmp_path / "gb.json", "key", fetch=fetch)
    found = books.lookup("Continuo Preto", [])
    assert found == {
        "gb_title": "Continuo Preta",
        "gb_authors": ["Sueli Carneiro"],
        "gb_cover": "https://books.google.com/books/content?id=A&printsec=frontcover&img=1&zoom=1",
    }
    assert calls[0]["key"] == "key"
    books.save()
    again = GoogleBooks(tmp_path / "gb.json", "key", fetch=fetch)
    assert again.lookup("Continuo Preto", []) == found
    assert len(calls) == 1


def test_lookup_without_a_similar_title_is_none_and_errors_are_not_cached(tmp_path):
    books = GoogleBooks(tmp_path / "gb.json", "key", fetch=lambda params: {"items": [volume("Cozinha", [])]})
    assert books.lookup("Continuo Preto", []) is None

    def offline(params):
        raise OSError("offline")

    failing = GoogleBooks(tmp_path / "gb2.json", "key", fetch=offline)
    assert failing.lookup("Continuo Preto", []) is None
    failing.save()
    assert failing.cache == {}
