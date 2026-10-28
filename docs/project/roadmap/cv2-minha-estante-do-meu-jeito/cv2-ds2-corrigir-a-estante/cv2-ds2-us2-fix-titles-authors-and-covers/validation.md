# Validation — CV2.DS2.US2

## Status

Passed

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 213 files formatted
- uv run pytest — 185 passed

Checks status: passed

## E2E

Decision: required

Evidence: Navigator screenshots showed the embedded blue local cover, then cover: none falling back to a spine with the full explicit known_as and corrected title. CR001 fixed the misleading Open Library-only footer; the disposable page was redrawn and verified.

## Navigator Validation

Route: Navigator ran check, draw and open in /tmp/89books-us2-validation and supplied screenshots for both local-cover and none/spine states.

Navigator accepted: yes

Expected observation: Corrected identity is visible, a local cover embeds safely, none produces a spine, and provenance is truthful.

Pass condition: Reader corrections and chosen cover modes visibly win after free redraw.

Fail condition: Old identity wins, local cover fails, none still shows a face, or redraw requests payment.

## Missing Evidence

- none
