# Validation — CV2.DS3.US8

## Status

Blocked

## Automated Checks

- uv run pytest -q (242 passed); uv run ruff check .; uv run ruff format --check .; git diff --check

Checks status: passed

## E2E

Decision: required

Evidence: Offline disposable fixture /tmp/89books-us8-e2e used synthetic named and unnamed photos through real create, check and draw paths. A conflicting fake portrait was overridden; version 2 preserved Tecnologia and Literatura with section photos and provenance membership, an unnamed book reached the closing shelf, repeated cross-photo recognition stayed visible, and the verified HTML screenshot rendered both section photos.

## Navigator Validation

Route: Copy two consented sample photos to /tmp/89books-us8-validation as 01_Tecnologia.jpg and 02_Literatura.jpg; run uv run shelf create --folder /tmp/89books-us8-validation, approve the displayed small cost, then run shelf check, draw and open for that folder.

Navigator accepted: no

Expected observation: Before spending, the terminal lists Tecnologia then Literatura and says names and order will be preserved. The resulting version 2 shelf.yaml keeps those titles, photos and recognized books, and the page shows each photo inside its matching section while retaining the top mosaic.

Pass condition: Human titles, order, section photos and provenance membership survive the model response; check and draw pass for free; version 1 remains drawable.

Fail condition: Paid work begins before naming errors, the model renames/reorders/moves named shelves, a section photo is absent, unnamed books leave the closing shelf, or a version 1 source no longer draws.

## Missing Evidence

- Navigator validation has not been accepted
<!-- ariad-seal sha256:8a86db490a86dbbd4847ba1193b1679ca4e8f1be7150001dc897d5faa2ed4d7d — Ariad wrote this file and rewrites it only while this line matches the text above it. Edit the file and Ariad will leave it as it is. -->
