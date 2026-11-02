[< Story](index.md)

# Test Guide: CV2.DS3.US8 Name photos to shape my shelves

## Automated Validation

```bash
uv run pytest tests/test_named_shelves.py tests/test_shelf_file.py tests/test_core.py tests/test_cli.py tests/test_page.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The focused tests cover:

- intentional `NN_Título.ext` parsing and generic-name rejection;
- position and title collision errors before paid work;
- fixed section order, literal title, photo and book membership;
- model conflict being overridden by human arrangement;
- unnamed-photo books reaching the closing shelf;
- free recovery retaining named shelves;
- version 1 compatibility and version 2 stable round-trip;
- refusal to dump a section photo as version 1;
- terminal preview before consent;
- missing section photo rejection without replacing the page;
- section photo rendering in wide, side and phone layouts.

## Offline E2E

Create a disposable fixture with three synthetic photos:

```text
01_Tecnologia.jpg
02_Literatura.jpg
photo-03.jpg
```

Fake recognition returns distinct books for each photo. The fake portrait tries
to rename and reorder the named sections. Run the real creation, check and draw
paths without network. Assert that version 2 YAML and HTML preserve the named
sections and that the unnamed book reaches the closing shelf.

## Navigator Validation

Use two consented sample photos copied into a disposable folder and renamed:

```text
01_Tecnologia.jpg
02_Literatura.jpg
```

From the repository root:

```bash
uv run shelf create --folder /tmp/89books-us8-validation
uv run shelf check --folder /tmp/89books-us8-validation
uv run shelf draw --folder /tmp/89books-us8-validation
uv run shelf open --folder /tmp/89books-us8-validation
```

Expected observation: before confirmation, the terminal lists the two named
shelves and says their names and order will be preserved. `shelf.yaml` uses
version 2, associates each section with its photo and keeps the books recognized
from that photo. The HTML shows the matching photo inside each section.

Pass condition: the human titles, order, photos and membership survive the model
response; unnamed behavior and version 1 compatibility remain intact.

Fail condition: a paid call begins before naming errors, the model changes human
arrangement, section photos are missing from the page, or an existing version 1
shelf cannot check and draw.

The create step is paid and requires the Navigator's explicit CLI confirmation.
Use only the small disposable subset.

## Validation Evidence

Pending implementation and validation.
