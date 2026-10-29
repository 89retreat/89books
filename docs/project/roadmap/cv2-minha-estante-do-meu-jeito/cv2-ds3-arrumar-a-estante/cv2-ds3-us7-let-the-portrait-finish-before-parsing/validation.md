# Validation — CV2.DS3.US7

## Status

Passed

## Automated Checks

- uv run pytest tests/test_openrouter.py tests/test_recognition_and_portrait.py tests/test_cli.py -q — 47 passed
- uv run pytest -q — 225 passed
- uv run ruff check . — passed
- uv run ruff format --check . — 265 files formatted

Checks status: passed

## E2E

Decision: required

Evidence: Offline 237-book E2E covered both cutoff and complete responses. Navigator then ran the real portrait-only retry against Rafael saved 237-book draft and reported success.

## Navigator Validation

Route: uv run shelf create --folder ~/89books/my-bookshelf/rafael-caceres/

Navigator accepted: yes

Expected observation: The CLI reuses 237 saved books, performs only the portrait call, and creates shelf.yaml without repeating photo recognition, review, catalogues or covers.

Pass condition: The real portrait completes with high reasoning, the saved books become shelf.yaml, and paid preparation is not repeated.

Fail condition: Any preparation stage repeats, the portrait is truncated again, or the saved draft is lost before shelf.yaml is valid.

## Missing Evidence

- none
