# Validation — CV2.DS3.US3

## Status

Blocked

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 236 files formatted
- uv run pytest — 201 passed

Checks status: passed

## E2E

Decision: required

Evidence: Free offline E2E passed in /tmp/89books-ds3-us3-validation. With six colored photos, shelf.yaml chose photo 04 then photo 02 and produced exact mosaic orders [4,1,2,3,5,6] and [2,1,3,4,5,6], while legacy config.toml kept pointing at photo 01. An absent choice made check and draw exit 2 without changing page bytes, marker or history. Desktop rendering was captured at desktop.png.

## Navigator Validation

Route: Run uv run shelf open --folder /tmp/89books-ds3-us3-validation. Confirm blue PHOTO 2 fills the large first mosaic cell although config.toml points at photo 01. Narrow the browser to phone width and confirm PHOTO 2 remains visible with only five cells and +1. Edit /tmp/89books-ds3-us3-validation/shelf.yaml to cover_photo: photo-05.jpg, then run check, draw and open and confirm the purple PHOTO 5 becomes the large cell while the others remain ordered. Finally use missing.jpg and confirm check/draw fail while the previous page still opens; restore photo-05.jpg afterward.

Navigator accepted: no

Expected observation: The exact shelf.yaml filename alone selects the large first image on desktop and phone; remaining images retain order; a missing name reports an error and preserves the prior page.

Pass condition: Photo 2 then photo 5 visibly become the featured cell without config influence, the selected photo remains mobile-visible, and invalid selection leaves the previous page intact with no key, network or cost.

Fail condition: Photo 1 from config or alphabetical order wins, non-selected photos reorder, the chosen photo is hidden on mobile, invalid draw replaces the page, or any paid/network service is requested.

## Missing Evidence

- Navigator validation has not been accepted
