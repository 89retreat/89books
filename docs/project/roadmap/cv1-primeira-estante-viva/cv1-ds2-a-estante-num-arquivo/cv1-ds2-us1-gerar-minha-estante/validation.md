# Validation — CV1.DS2.US1

## Status

Blocked

## Automated Checks

- uv run pytest (20 passed); uv run ruff check and ruff format --check clean; real run on 7 shelf photos: 161 books, US$0.09, HTML without key, local paths or EXIF, checked at 1280 and 390 px

Checks status: passed

## E2E

Decision: required

Evidence: Automated end-to-end test with simulated OpenRouter and Open Library (tests/test_cli.py); real run by the Driver with Lula's photos

## Navigator Validation

Route: Run uv run shelf <folder> with photos of your own shelf, open shelf.html on computer and phone

Navigator accepted: no

Expected observation: Command reports books and cost; page shows photo carousel, lens, themes and books

Pass condition: Page opens on its own on both devices and the portrait sounds like you

Fail condition: Unclear error, page broken on phone, missing books or portrait, or private data in the file

## Missing Evidence

- Navigator validation has not been accepted
