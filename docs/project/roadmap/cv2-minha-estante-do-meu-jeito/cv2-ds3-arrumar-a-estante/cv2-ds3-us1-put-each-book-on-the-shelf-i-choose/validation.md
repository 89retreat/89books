# Validation — CV2.DS3.US1

## Status

Passed

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 220 files formatted
- uv run pytest — 191 passed

Checks status: passed

## E2E

Decision: required

Evidence: Navigator screenshot of /tmp/89books-ds3-us1-validation confirmed literal source order I/II/III, the complete moved book and known_as in Uma prateleira minha, and the former canonical closing shelf rendered as regular II when it was not final.

## Navigator Validation

Route: Navigator ran check, draw and open in /tmp/89books-ds3-us1-validation and supplied a screenshot of the three authored shelf sections.

Navigator accepted: yes

Expected observation: The custom shelf is numbered III, the moved book retains identity, and order follows shelf.yaml.

Pass condition: Book and shelf positions follow the source exactly, metadata survives, and redraw remains free.

Fail condition: Automatic grouping or closing-shelf heuristics override authored order, metadata disappears, or redraw requests payment.

## Missing Evidence

- none
