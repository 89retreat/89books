# Validation — CV2.DS3.US6

## Status

Blocked

## Automated Checks

- uv run pytest — 221 passed
- uv run ruff check . — passed
- uv run ruff format --check . — 257 files formatted

Checks status: passed

## E2E

Decision: required

Evidence: Offline E2E in /tmp/89books-ds3-us6-validation proved malformed portrait preservation, free keyless recovery, exact three-book order, free check/draw/open, and portrait-only retry without repeating recognition or review.

## Navigator Validation

Route: From the project checkout, inspect /tmp/89books-ds3-us6-validation/navigator with `uv run shelf --folder ...`; run `uv run shelf recover --folder ...`, then check, draw and open the same folder. No key or network is needed.

Navigator accepted: no

Expected observation: Status first says paid work saved privately and recommends recover. Recover creates shelf.yaml with three books in Meus livros, empty authored lens, then check/draw/open work for free.

Pass condition: Recovery asks no questions, makes no paid/network call, preserves all three books in order, removes only recovery files after source creation, and produces a drawable page.

Fail condition: Recover asks for a key, contacts OpenRouter, loses/reorders a book, invents portrait prose, removes the draft before writing shelf.yaml, or cannot draw the recovered source.

## Missing Evidence

- Navigator validation has not been accepted
