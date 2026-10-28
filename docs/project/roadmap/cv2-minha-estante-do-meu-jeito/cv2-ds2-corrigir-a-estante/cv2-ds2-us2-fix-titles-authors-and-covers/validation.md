# Validation — CV2.DS2.US2

## Status

Blocked

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 212 files formatted
- uv run pytest — 184 passed

Checks status: passed

## E2E

Decision: required

Evidence: Free local E2E passed in /tmp/89books-us2-validation: check and draw used corrected title, author, full known_as and an embedded local cover; generated HTML contained no local path or EXIF.

## Navigator Validation

Route: Run uv run shelf open --folder /tmp/89books-us2-validation and inspect the face-out book. Optionally set cover to none, run check/draw/open, observe a spine, then restore covers/capa.jpg and redraw.

Navigator accepted: no

Expected observation: The page shows Título corrigido, Autora corrigida, the full chosen known_as and the blue local cover; cover none changes it to a drawn spine without any paid action.

Pass condition: Reader corrections and each chosen cover mode visibly win after free redraw, with the previous page preserved on invalid input.

Fail condition: Any old identity wins, local cover is absent/leaks a path, cover none still shows a face, or any key/network/paid action is requested.

## Missing Evidence

- Navigator validation has not been accepted
