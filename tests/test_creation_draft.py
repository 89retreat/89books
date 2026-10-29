import pytest

from shelf.core import CreationDraft
from shelf.creation_draft import DraftError, dump_draft, parse_draft


def draft():
    return CreationDraft(
        name="Rafael",
        photos=["photo-01.jpg", "photo-02.jpg"],
        books=[
            {
                "title": "Torto Arado",
                "authors": ["Itamar Vieira Junior"],
                "source": "open_library",
                "photo": "photo-01.jpg",
                "work": "/works/OL1W",
                "cover_id": 7,
            }
        ],
        left_out=[{"title": "Caneca", "reason": "not a book"}],
        cost=0.24,
        migrated=False,
    )


def test_creation_draft_round_trips_every_paid_result_without_secrets_or_paths():
    text = dump_draft(draft())

    assert parse_draft(text) == draft()
    assert "sk-or-" not in text and "/Users/" not in text
    assert "photo-01.jpg" in text and "Torto Arado" in text


def test_creation_draft_never_serializes_absolute_book_photo_provenance():
    value = draft()
    value.books[0]["photo"] = "/Users/private/photo.jpg"

    with pytest.raises(DraftError, match="provenance"):
        dump_draft(value)


def test_creation_draft_rejects_unknown_version_absolute_photos_and_invalid_books():
    with pytest.raises(DraftError, match="version"):
        parse_draft(
            "version: 2\nname: null\nphotos: [photo.jpg]\nbooks: []\nleft_out: []\ncost: 0\nmigrated: false\n"
        )
    with pytest.raises(DraftError, match="photo names"):
        parse_draft(
            "version: 1\nname: null\nphotos: [/private/photo.jpg]\nbooks: []\nleft_out: []\ncost: 0\nmigrated: false\n"
        )
    with pytest.raises(DraftError, match="books"):
        parse_draft(
            "version: 1\nname: null\nphotos: [photo.jpg]\nbooks: [{authors: []}]\nleft_out: []\ncost: 0\nmigrated: false\n"
        )
