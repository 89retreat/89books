# Validation — CV2.DS2.US1

## Status

Blocked

## Automated Checks

- uv run pytest: 163 passed
- uv run ruff check . && uv run ruff format --check .: passed

Checks status: passed

## E2E

Decision: required

Evidence: Free synthetic E2E on /tmp/estante-hide-books-e2e: check reported 2 total/1 visible; changed draw saved a version and rendered 1 book; Hidden Book, its cover and Quem mais mora aqui were absent while Visible Book remained; status reported 2 total/1 visible/1 hidden; removing the mark saved a second version, rendered 2 books and restored the frequent-author surface. No keys or network were available.

## Navigator Validation

Route: On a disposable copy, choose one visible book, add hidden: true, run check/draw/status/open and confirm absence plus counts; remove the line, draw/open and confirm the same book returns.

Navigator accepted: no

Expected observation: The selected book disappears as cover/spine and stops contributing to frequent authors while staying in shelf.yaml/history; removing the mark returns it in place.

Pass condition: Navigator sees reversible free hide/show behavior, correct counts and preserved source/history.

Fail condition: Book remains visual, author aggregation is wrong, order/data is lost, prose is rewritten, or any key/network/paid call occurs.

## Missing Evidence

- Navigator validation has not been accepted
