# Validation — CV2.DS3.US3

## Status

Passed

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 236 files formatted
- uv run pytest — 201 passed

Checks status: passed

## E2E

Decision: required

Evidence: Free offline E2E passed in /tmp/89books-ds3-us3-validation. Automated inspection proved photo orders [4,1,2,3,5,6] and [2,1,3,4,5,6], legacy config did not win, and missing selection preserved page, marker and history. Navigator exercised the route and reported that validation succeeded.

## Navigator Validation

Route: Navigator opened the disposable shelf, changed cover_photo and redrew through check/draw/open.

Navigator accepted: yes

Expected observation: The exact shelf.yaml filename alone selects the large first image on desktop and phone; remaining images retain order; a missing name preserves the prior page.

Pass condition: Chosen photos visibly become the featured cell without config influence and redraw remains free and safe.

Fail condition: Legacy config wins, photos reorder, the selected photo disappears, invalid draw replaces the page, or a paid/network service is requested.

## Missing Evidence

- none
