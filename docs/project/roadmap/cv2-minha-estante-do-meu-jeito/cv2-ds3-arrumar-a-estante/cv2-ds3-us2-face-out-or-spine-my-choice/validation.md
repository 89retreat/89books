# Validation — CV2.DS3.US2

## Status

Blocked

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 228 files formatted
- uv run pytest — 195 passed

Checks status: passed

## E2E

Decision: required

Evidence: Free local E2E passed in /tmp/89books-ds3-us2-validation: an absent face on a cited book and explicit true produced two faces; explicit false and cover none produced spines; six more explicit faces reached the second shelf in authored order; nine local images were embedded without network.

## Navigator Validation

Route: Run uv run shelf open --folder /tmp/89books-ds3-us2-validation. In Três escolhas confirm two covers followed by Lombada forçada and Sem capa as spines. In Muitas capas confirm six covers wrap into rows without overlap. Optionally remove face: true from Capa forçada, run check/draw/open and confirm it returns to an automatic spine because it is not cited.

Navigator accepted: no

Expected observation: True, false and absent visibly mean cover, spine and automatic; none falls back to spine; multiple covers keep order and wrap safely.

Pass condition: All precedence states and multi-row layout are visible after free redraw with no missing or reordered books.

Fail condition: False is ignored, automatic remains frozen, a no-cover book disappears, faces overlap/reorder, or a paid/network service is requested.

## Missing Evidence

- Navigator validation has not been accepted
