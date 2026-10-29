import os
from datetime import datetime, timedelta

import pytest

from shelf import cli
from shelf.cli import (
    CommandError,
    check_shelf,
    create_shelf,
    draw_shelf,
    list_history,
    open_shelf,
    recreate_shelf,
    restore_shelf,
    save_version,
)
from shelf.config import load_config
from shelf.shelf_file import ShelfSection, ShelfYamlError, dump_shelf, parse_shelf
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


def recreate_with_fakes(config, **overrides):
    arguments = dict(
        recognize=fake_recognize,
        library=FakeLibrary(),
        portrait=fake_portrait,
        review=no_review,
        covers=FakeCovers(),
        log=lambda line: None,
    )
    return recreate_shelf(config, **{**arguments, **overrides})


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
    assert all(book.face is None for book in all_books(shelf))
    assert "face:" not in shelf_path.read_text(encoding="utf-8")
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


def test_check_and_draw_put_the_reader_chosen_photo_first_without_reordering_the_rest(
    shelf_folder, monkeypatch
):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.cover_photo = "photo-02.jpg"
    path.write_text(dump_shelf(shelf), encoding="utf-8")
    monkeypatch.setattr(cli.photo_tools, "prepare", lambda path, max_side: path.name.encode())
    monkeypatch.setattr(cli.photo_tools, "data_uri", lambda image: image.decode())

    checked = check_shelf(shelf_folder)
    result = draw_shelf(shelf_folder)
    html = result.html.read_text(encoding="utf-8")

    assert checked.books == 2
    assert html.index('src="photo-02.jpg"') < html.index('src="photo-01.jpg"')


def test_check_and_draw_reject_a_cover_photo_outside_the_root_photo_set(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.cover_photo = "covers/photo-02.jpg"
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    with pytest.raises(CommandError, match='cover_photo "covers/photo-02.jpg"'):
        check_shelf(shelf_folder)
    with pytest.raises(CommandError, match='cover_photo "covers/photo-02.jpg"'):
        draw_shelf(shelf_folder)


def test_check_and_draw_use_corrected_identity_and_embed_a_safe_local_cover(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    covers = shelf_folder / "covers"
    covers.mkdir()
    (covers / "capa.jpg").write_bytes((shelf_folder / "photo-01.jpg").read_bytes())
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    book = next(book for section in shelf.shelves for book in section.books if book.title == "Cynefin")
    book.title = "Cynefin corrigido"
    book.authors = ["Autora corrigida"]
    book.known_as = "Um nome conhecido que eu escolhi por inteiro"
    book.face = True
    book.cover = "covers/capa.jpg"
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    checked = check_shelf(shelf_folder)
    result = draw_shelf(shelf_folder)
    html = result.html.read_text(encoding="utf-8")

    assert checked.books == 2 and result.books == 2
    assert "Cynefin corrigido" in html and "Autora corrigida" in html
    assert "Um nome conhecido que eu escolhi por inteiro" in html
    assert html.count("data:image/jpeg;base64,") == 3
    assert "covers/capa.jpg" not in html and "SecretCam" not in html


def test_invalid_local_cover_never_changes_page_marker_or_history(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 19, 30))
    page = (shelf_folder / "shelf.html").read_bytes()
    marker = (shelf_folder / ".shelf" / "last-drawn.sha256").read_bytes()
    versions = [entry.name for entry in list_history(shelf_folder)]
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.shelves[0].books[0].cover = "covers/missing.jpg"
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    with pytest.raises(CommandError, match='Book ".+": cover "covers/missing.jpg"'):
        check_shelf(shelf_folder)
    with pytest.raises(CommandError, match='Book ".+": cover "covers/missing.jpg"'):
        draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 19, 31))

    assert (shelf_folder / "shelf.html").read_bytes() == page
    assert (shelf_folder / ".shelf" / "last-drawn.sha256").read_bytes() == marker
    assert [entry.name for entry in list_history(shelf_folder)] == versions


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


def test_reader_authored_shelf_language_is_checked_snapshotted_drawn_and_restored(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    first = draw_shelf(shelf_folder, now=datetime(2026, 10, 29, 11, 0))
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.lens = "Minha *voz* <segura>."
    shelf.shelves[0].title = "Minha *prateleira* <autoral>"
    shelf.shelves[0].text = "Agora escolho *Cynefin* <script>não executar</script>."
    path.write_text(dump_shelf(shelf), encoding="utf-8")
    authored_source = path.read_bytes()

    checked = check_shelf(shelf_folder)
    authored = draw_shelf(shelf_folder, now=datetime(2026, 10, 29, 11, 1))
    html = authored.html.read_text(encoding="utf-8")

    assert checked.books == 2 and authored.version.read_bytes() == authored_source
    assert "Minha <em>voz</em> &lt;segura&gt;." in html
    assert "Minha *prateleira* &lt;autoral&gt;" in html
    assert "Agora escolho <em>Cynefin</em> &lt;script&gt;não executar&lt;/script&gt;." in html
    assert "<script>não executar</script>" not in html

    restored = restore_shelf(
        shelf_folder,
        first.version.name,
        now=datetime(2026, 10, 29, 11, 2),
    )
    redrawn = draw_shelf(shelf_folder, now=datetime(2026, 10, 29, 11, 3))
    restored_html = redrawn.html.read_text(encoding="utf-8")

    assert restored.changed and restored.saved_current.read_bytes() == authored_source
    assert "Eu olho a terra." in restored_html and "Quando penso na terra" in restored_html
    assert "Minha *prateleira*" not in restored_html


def test_draw_respects_explicit_face_spine_and_return_to_automatic(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    torto = next(book for book in all_books(shelf) if book.title == "Torto Arado")
    cynefin = next(book for book in all_books(shelf) if book.title == "Cynefin")
    torto.cover = "https://example.test/torto.jpg"
    torto.face = False
    cynefin.cover = "https://example.test/cynefin.jpg"
    cynefin.face = True
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    explicit = draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 20, 10))
    explicit_html = explicit.html.read_text(encoding="utf-8")
    torto.face = None
    path.write_text(dump_shelf(shelf), encoding="utf-8")
    automatic = draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 20, 11))
    automatic_html = automatic.html.read_text(encoding="utf-8")

    assert explicit_html.count('class="face"') == 1
    assert "https://example.test/cynefin.jpg" in explicit_html
    assert "https://example.test/torto.jpg" not in explicit_html
    assert automatic_html.count('class="face"') == 2
    assert "https://example.test/torto.jpg" in automatic_html
    assert explicit.version is not None and automatic.version is not None


def test_draw_follows_a_complete_book_move_into_a_custom_last_shelf(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    origin = next(
        section for section in shelf.shelves if any(book.title == "Torto Arado" for book in section.books)
    )
    book = next(book for book in origin.books if book.title == "Torto Arado")
    origin.books.remove(book)
    shelf.shelves.append(ShelfSection(title="Uma prateleira minha", books=[book]))
    path.write_text(dump_shelf(shelf), encoding="utf-8")
    source = path.read_bytes()

    result = draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 20, 0))
    html = result.html.read_text(encoding="utf-8")
    title = html.index("Uma prateleira minha")
    section = html[html.rfind("<section", 0, title) : html.index("</section>", title)]

    assert 'class="bay side"' in section and '<span class="num">III</span>' in section
    assert "Torto Arado" in section and "Itamar Vieira Junior" in section
    assert result.version.read_bytes() == source
    moved = parse_shelf(source.decode("utf-8")).shelves[-1].books[0]
    assert moved.source == "open_library" and moved.work == "/works/OL1W"


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


def test_missing_cover_photo_never_replaces_page_marker_or_history(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    draw_shelf(shelf_folder)
    page = shelf_folder / "shelf.html"
    marker = shelf_folder / ".shelf" / "last-drawn.sha256"
    before = page.read_bytes()
    marker_before = marker.read_bytes()
    versions_before = [entry.name for entry in list_history(shelf_folder)]
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    shelf.cover_photo = "missing.jpg"
    path.write_text(dump_shelf(shelf), encoding="utf-8")

    with pytest.raises(CommandError, match='cover_photo "missing.jpg"'):
        check_shelf(shelf_folder)
    with pytest.raises(CommandError, match='cover_photo "missing.jpg"'):
        draw_shelf(shelf_folder)
    assert page.read_bytes() == before
    assert marker.read_bytes() == marker_before
    assert [entry.name for entry in list_history(shelf_folder)] == versions_before


def test_draw_hides_book_without_deleting_it_and_snapshots_the_choice(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    path = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(path.read_text(encoding="utf-8"))
    cynefin = next(book for section in shelf.shelves for book in section.books if book.title == "Cynefin")
    cynefin.hidden = True
    path.write_text(dump_shelf(shelf), encoding="utf-8")
    source = path.read_bytes()

    result = draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 19, 30))

    assert result.books == 1 and result.version.read_bytes() == source
    assert b"hidden: true" in source and b"Cynefin" in source
    assert "Cynefin" not in result.html.read_text(encoding="utf-8")


def test_draw_snapshots_exact_changed_bytes_and_does_not_repeat_unchanged_source(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = shelf_folder / "shelf.yaml"
    first_bytes = source.read_bytes()
    now = datetime(2026, 10, 28, 19, 30)

    first = draw_shelf(shelf_folder, now=now)
    unchanged = draw_shelf(shelf_folder, now=now)
    source.write_bytes(first_bytes.replace(b"Eu olho a terra.", b"Eu escolho a terra."))
    changed_bytes = source.read_bytes()
    changed = draw_shelf(shelf_folder, now=now)

    assert first.version.name == "shelf-2026-10-28-1930.yaml"
    assert first.version.read_bytes() == first_bytes
    assert unchanged.version is None
    assert changed.version.name == "shelf-2026-10-28-1930-02.yaml"
    assert changed.version.read_bytes() == changed_bytes
    assert len(list_history(shelf_folder)) == 2
    assert (shelf_folder / ".shelf" / "last-drawn.sha256").exists()


def test_invalid_draw_does_not_snapshot_or_change_page_or_marker(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 19, 30))
    page = (shelf_folder / "shelf.html").read_bytes()
    marker = (shelf_folder / ".shelf" / "last-drawn.sha256").read_bytes()
    versions = [entry.name for entry in list_history(shelf_folder)]
    (shelf_folder / "shelf.yaml").write_text("version: one\n", encoding="utf-8")

    with pytest.raises(ShelfYamlError):
        draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 19, 31))

    assert (shelf_folder / "shelf.html").read_bytes() == page
    assert (shelf_folder / ".shelf" / "last-drawn.sha256").read_bytes() == marker
    assert [entry.name for entry in list_history(shelf_folder)] == versions


def test_history_lists_metadata_without_opening_version_contents(shelf_folder, monkeypatch):
    version = shelf_folder / "history" / "shelf-2026-10-28-1930.yaml"
    version.parent.mkdir()
    version.write_text("private contents", encoding="utf-8")
    (version.parent / "notes.yaml").write_text("unmanaged", encoding="utf-8")

    monkeypatch.setattr(type(version), "read_bytes", lambda self: (_ for _ in ()).throw(AssertionError()))
    entries = list_history(shelf_folder)

    assert [(entry.name, entry.size) for entry in entries] == [(version.name, len(b"private contents"))]


def test_restore_saves_even_broken_current_bytes_before_installing_valid_version(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    valid = (shelf_folder / "shelf.yaml").read_bytes()
    drawn = draw_shelf(shelf_folder, now=datetime(2026, 10, 28, 19, 30))
    page = (shelf_folder / "shelf.html").read_bytes()
    marker = (shelf_folder / ".shelf" / "last-drawn.sha256").read_bytes()
    broken = b"version: one\nmy unfinished edit\n"
    (shelf_folder / "shelf.yaml").write_bytes(broken)

    result = restore_shelf(
        shelf_folder,
        drawn.version.name,
        now=datetime(2026, 10, 28, 19, 31),
    )

    assert result.changed and result.saved_current.read_bytes() == broken
    assert (shelf_folder / "shelf.yaml").read_bytes() == valid
    assert (shelf_folder / "shelf.html").read_bytes() == page
    assert (shelf_folder / ".shelf" / "last-drawn.sha256").read_bytes() == marker
    assert len(list_history(shelf_folder)) == 2


def test_restore_rejects_traversal_missing_and_invalid_versions_before_backup(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = (shelf_folder / "shelf.yaml").read_bytes()
    history = shelf_folder / "history"
    history.mkdir()
    invalid = history / "shelf-2026-10-28-1930.yaml"
    invalid.write_text("version: one\n", encoding="utf-8")

    with pytest.raises(CommandError, match="Unknown version"):
        restore_shelf(shelf_folder, "../shelf-2026-10-28-1930.yaml")
    with pytest.raises(CommandError, match="Unknown version"):
        restore_shelf(shelf_folder, "shelf-2026-10-28-1940.yaml")
    with pytest.raises(ShelfYamlError):
        restore_shelf(shelf_folder, invalid.name)

    assert (shelf_folder / "shelf.yaml").read_bytes() == source
    assert [entry.name for entry in list_history(shelf_folder)] == [invalid.name]


def test_recreate_generates_first_then_saves_current_and_replaces_only_source(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = shelf_folder / "shelf.yaml"
    source.write_bytes(
        source.read_bytes().replace(b"Eu olho a terra.", "Minha edição insubstituível.".encode())
    )
    before = source.read_bytes()
    (shelf_folder / "shelf.html").write_text("previous page", encoding="utf-8")

    result = recreate_with_fakes(config, now=datetime(2026, 10, 28, 19, 30))

    assert result.version.read_bytes() == before
    assert b"Minha edi" not in source.read_bytes()
    assert (shelf_folder / "shelf.html").read_text() == "previous page"
    assert result.books == 2 and result.cost == 0.05


def test_recreate_preserves_a_valid_reader_cover_photo_over_legacy_config(shelf_folder):
    (shelf_folder / "config.toml").write_text('cover_photo = "photo-01.jpg"\n')
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(source.read_text(encoding="utf-8"))
    shelf.cover_photo = "photo-02.jpg"
    source.write_text(dump_shelf(shelf), encoding="utf-8")

    recreate_with_fakes(config, now=datetime(2026, 10, 29, 9, 30))

    recreated = parse_shelf(source.read_text(encoding="utf-8"))
    assert recreated.cover_photo == "photo-02.jpg"


def test_recreate_repairs_a_removed_or_unreadable_cover_choice(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = shelf_folder / "shelf.yaml"
    shelf = parse_shelf(source.read_text(encoding="utf-8"))
    shelf.cover_photo = "removed.jpg"
    source.write_text(dump_shelf(shelf), encoding="utf-8")

    first = recreate_with_fakes(config, now=datetime(2026, 10, 29, 9, 31))
    assert parse_shelf(source.read_text(encoding="utf-8")).cover_photo == "photo-01.jpg"
    source.write_text("not: [valid\n", encoding="utf-8")
    invalid = source.read_bytes()

    second = recreate_with_fakes(config, now=datetime(2026, 10, 29, 9, 32))

    assert first.version.exists()
    assert second.version.read_bytes() == invalid
    assert parse_shelf(source.read_text(encoding="utf-8")).cover_photo == "photo-01.jpg"


def test_failed_recreate_never_snapshots_or_replaces_source(shelf_folder):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = (shelf_folder / "shelf.yaml").read_bytes()

    def fail(*args, **kwargs):
        raise RuntimeError("model failed")

    with pytest.raises(RuntimeError, match="model failed"):
        recreate_with_fakes(config, recognize=fail)

    assert (shelf_folder / "shelf.yaml").read_bytes() == source
    assert list_history(shelf_folder) == []


def test_recreate_replace_failure_keeps_source_and_the_completed_backup(shelf_folder, monkeypatch):
    config = load_config(shelf_folder, env={"OPENROUTER_API_KEY": "sk-secret"})
    create_with_fakes(config)
    source = (shelf_folder / "shelf.yaml").read_bytes()

    monkeypatch.setattr(cli, "_replace", lambda *args: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(OSError, match="disk full"):
        recreate_with_fakes(config, now=datetime(2026, 10, 28, 19, 30))

    assert (shelf_folder / "shelf.yaml").read_bytes() == source
    assert list_history(shelf_folder)[0].name == "shelf-2026-10-28-1930.yaml"


def test_snapshot_retention_keeps_twenty_managed_and_unknown_files(shelf_folder):
    history = shelf_folder / "history"
    history.mkdir()
    start = datetime(2026, 10, 27, 0, 0)
    for index in range(20):
        moment = start + timedelta(minutes=index)
        path = history / moment.strftime("shelf-%Y-%m-%d-%H%M.yaml")
        path.write_text(str(index), encoding="utf-8")
        timestamp = moment.timestamp()
        os.utime(path, (timestamp, timestamp))
    unknown = history / "notes.yaml"
    unknown.write_text("keep me", encoding="utf-8")

    save_version(shelf_folder, b"new", now=datetime(2026, 10, 28, 19, 30))

    assert len(list_history(shelf_folder)) == 20
    assert not (history / "shelf-2026-10-27-0000.yaml").exists()
    assert unknown.read_text() == "keep me"


def test_open_uses_a_file_uri_and_requires_a_page(shelf_folder):
    seen = []
    with pytest.raises(CommandError, match="draw"):
        open_shelf(shelf_folder, opener=seen.append)

    page = shelf_folder / "shelf.html"
    page.write_text("page", encoding="utf-8")
    assert open_shelf(shelf_folder, opener=seen.append) == page
    assert seen == [page.resolve().as_uri()]
