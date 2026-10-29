# Validation — CV2.DS3.US7

## Status

Blocked

## Automated Checks

- uv run pytest tests/test_openrouter.py tests/test_recognition_and_portrait.py tests/test_cli.py -q — 47 passed
- uv run pytest -q — 225 passed
- uv run ruff check . — passed
- uv run ruff format --check . — 265 files formatted

Checks status: passed

## E2E

Decision: required

Evidence: Offline 237-book E2E simulated finish_reason=length and finish_reason=stop through the real OpenRouter client path. The first kept the draft and partial response with a friendly message; the second wrote all 237 books, removed recovery files only after success, sent high reasoning with max_tokens 64000 and no temperature, and never repeated paid preparation.

## Navigator Validation

Route: uv run shelf create --folder ~/89books/my-bookshelf/rafael-caceres/

Navigator accepted: no

Expected observation: The CLI finds 237 saved books, asks consent only for another portrait, does not recognize photos or query catalogues again, and either creates shelf.yaml or reports plainly that the portrait did not finish while preserving the draft.

Pass condition: No recognition/review/catalogue/cover stage repeats; a complete portrait creates shelf.yaml with the saved books; any external failure keeps the draft and avoids JSON/parser language.

Fail condition: Any paid preparation repeats, the portrait is truncated without a clear message, reasoning quality is lowered, temperature is sent, or recovery files disappear before shelf.yaml is valid.

## Missing Evidence

- Navigator validation has not been accepted
