import pytest

from shelf.named_shelves import (
    NamedShelfError,
    apply_named_shelves,
    named_shelves,
    parse_named_photo,
)


def test_intentional_photo_names_define_literal_ordered_shelves():
    assert parse_named_photo("02_Literatura_Brasileira.jpeg") == (2, "Literatura Brasileira")
    assert parse_named_photo("01_Tecnologia e Produto.jpg") == (1, "Tecnologia e Produto")

    for generic in ("photo-01.jpg", "IMG_4382.jpeg", "WhatsApp Image 2026.jpeg", "1_Tema.jpg"):
        assert parse_named_photo(generic) is None


def test_named_shelves_keep_photo_membership_and_sort_by_position():
    photos = ["02_Literatura.jpg", "photo-03.jpg", "01_Tecnologia.jpg"]
    books = [
        {"title": "Código", "photo": "01_Tecnologia.jpg"},
        {"title": "Romance", "photo": "02_Literatura.jpg"},
        {"title": "Sem tema", "photo": "photo-03.jpg"},
    ]

    shelves = named_shelves(photos, books)

    assert [(s.position, s.title, s.photo, list(s.book_indexes)) for s in shelves] == [
        (1, "Tecnologia", "01_Tecnologia.jpg", [0]),
        (2, "Literatura", "02_Literatura.jpg", [1]),
    ]


@pytest.mark.parametrize(
    "photos,message",
    [
        (["01_Tecnologia.jpg", "01_Literatura.jpg"], "position 01"),
        (["01_Tecnologia.jpg", "02_tecnologia.jpg"], 'title "tecnologia"'),
        (["01_.jpg"], "non-empty title"),
    ],
)
def test_invalid_named_shelves_are_rejected_before_generation(photos, message):
    with pytest.raises(NamedShelfError, match=message):
        named_shelves(photos, [])


def test_human_arrangement_overrides_model_titles_order_and_membership():
    fixed = named_shelves(
        ["01_Tecnologia.jpg", "02_Literatura.jpg", "photo-03.jpg"],
        [
            {"title": "Código", "photo": "01_Tecnologia.jpg"},
            {"title": "Romance", "photo": "02_Literatura.jpg"},
            {"title": "Sem tema", "photo": "photo-03.jpg"},
        ],
    )
    model = {
        "lens": "Eu atravesso mundos.",
        "themes": [
            {"title": "Inventado", "text": "Texto tecnológico.", "books": [2]},
            {"title": "Outra ordem", "text": "Texto literário.", "books": [0]},
        ],
    }

    arranged = apply_named_shelves(model, fixed)

    assert arranged == {
        "lens": "Eu atravesso mundos.",
        "themes": [
            {
                "title": "Tecnologia",
                "text": "Texto tecnológico.",
                "books": [0],
                "photo": "01_Tecnologia.jpg",
            },
            {
                "title": "Literatura",
                "text": "Texto literário.",
                "books": [1],
                "photo": "02_Literatura.jpg",
            },
        ],
    }
