# Validation — CV2.DS3.US1

## Status

Blocked

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 220 files formatted
- uv run pytest — 191 passed

Checks status: passed

## E2E

Decision: required

Evidence: Free local E2E passed in /tmp/89books-ds3-us1-validation: a complete book appears in the custom final shelf with preserved identity; the shelf is regular and numbered III; the canonical closing shelf outside the final position is regular and numbered II.

## Navigator Validation

Route: Run uv run shelf open --folder /tmp/89books-ds3-us1-validation. Confirm Livro movido inteiro and Nome escolhido appear under Uma prateleira minha with numeral III. Then optionally move that complete section earlier in shelf.yaml, run check/draw/open and confirm the numerals follow the new source order.

Navigator accepted: no

Expected observation: The authored custom shelf is numbered III rather than treated as the closing shelf, and its complete moved book remains inside it. Reordering the section changes its numeral/order after a free redraw.

Pass condition: Book and shelf positions follow shelf.yaml exactly, complete metadata survives, and no key, catalogue, model or payment is requested.

Fail condition: Automatic grouping overrides the file, metadata disappears, the custom final shelf loses its numeral, or redraw asks for a paid service.

## Missing Evidence

- Navigator validation has not been accepted
