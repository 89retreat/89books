from shelf.googlebooks import GoogleBooks


def volume(title, authors, thumbnail=None):
    info = {"title": title, "authors": authors}
    if thumbnail:
        info["imageLinks"] = {"thumbnail": thumbnail}
    return {"volumeInfo": info}


def test_lookup_searches_free_text_with_the_author_and_takes_the_closest_title(tmp_path):
    calls = []

    def fetch(params):
        calls.append(params)
        cover = "http://books.google.com/books/content?id=A&printsec=frontcover&img=1&zoom=1&edge=curl"
        return {"items": [volume("Outro livro", ["X"]), volume("Continuo preta", ["Bianca Santana"], cover)]}

    books = GoogleBooks(tmp_path / "gb.json", "key", fetch=fetch)
    found = books.lookup("Continuo Preto: A Vida de Sueli Carneiro", ["Bianca Santana"])
    assert found == {
        "gb_title": "Continuo preta",
        "gb_authors": ["Bianca Santana"],
        "gb_cover": "https://books.google.com/books/content?id=A&printsec=frontcover&img=1&zoom=1",
    }
    assert calls[0]["q"] == "Continuo Preto Bianca Santana" and "intitle" not in calls[0]["q"]
    assert calls[0]["key"] == "key"
    books.save()
    again = GoogleBooks(tmp_path / "gb.json", "key", fetch=fetch)
    assert again.lookup("Continuo Preto: A Vida de Sueli Carneiro", ["Bianca Santana"]) == found
    assert len(calls) == 1


def test_a_similar_title_by_another_author_is_not_the_same_book(tmp_path):
    books = GoogleBooks(
        tmp_path / "gb.json",
        "key",
        fetch=lambda p: {"items": [volume("Imagens da branquitude", ["Lilia Schwarcz"])]},
    )
    assert books.lookup("Imagens da Branquitude", ["Lia Vainer Schucman"]) is None
    assert books.lookup("Imagens da Branquitude", []) is not None


def test_lookup_without_a_similar_title_is_none_and_errors_are_not_cached(tmp_path):
    books = GoogleBooks(tmp_path / "gb.json", "key", fetch=lambda params: {"items": [volume("Cozinha", [])]})
    assert books.lookup("Continuo Preto", []) is None

    def offline(params):
        raise OSError("offline")

    failing = GoogleBooks(tmp_path / "gb2.json", "key", fetch=offline)
    assert failing.lookup("Continuo Preto", []) is None
    failing.save()
    assert failing.cache == {}


def test_without_an_author_only_a_near_identical_spelling_is_accepted(tmp_path):
    def fetch_of(*titles):
        return lambda params: {"items": [volume(t, ["Alguém"]) for t in titles]}

    assert (
        GoogleBooks(tmp_path / "a.json", "k", fetch=fetch_of("Continuum")).lookup("Continuum Preta", [])
        is None
    )
    assert (
        GoogleBooks(tmp_path / "b.json", "k", fetch=fetch_of("SUELI CARNEIRO")).lookup(
            "A Vida de Sueli Carneiro", []
        )
        is None
    )
    bioethics = fetch_of("Introdução geral à bioética")
    assert (
        GoogleBooks(tmp_path / "c.json", "k", fetch=bioethics).lookup("Introdução geral à filosofia", [])
        is None
    )
    assert GoogleBooks(tmp_path / "d.json", "k", fetch=fetch_of("Pobreza urbana")).lookup(
        "Pobreza e Urbana", []
    )


def test_with_an_author_the_result_must_name_the_same_author(tmp_path):
    no_author = GoogleBooks(tmp_path / "e.json", "k", fetch=lambda p: {"items": [volume("Continuum", [])]})
    assert no_author.lookup("Continuum", ["Bianca Santana"]) is None
