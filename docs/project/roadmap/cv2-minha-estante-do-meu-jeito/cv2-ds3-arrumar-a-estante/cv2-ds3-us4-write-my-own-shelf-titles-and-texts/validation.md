# Validation — CV2.DS3.US4

## Status

Blocked

## Automated Checks

- uv run ruff check . — passed
- uv run ruff format --check . — 244 files formatted
- uv run pytest — 206 passed

Checks status: passed

## E2E

Decision: required

Evidence: Free offline E2E passed in /tmp/89books-ds3-us4-validation. Reader-authored lens and paragraph rendered single-pair emphasis; the shelf title kept literal asterisks; angle-bracket and script text stayed escaped; citing Cynefin moved only the automatic face while preserving Torto Arado before it. Explicit face false overrode the citation, removing it restored automatic composition, and disposable initial/authored versions were restored and redrawn exactly.

## Navigator Validation

Route: Run uv run shelf open --folder /tmp/89books-ds3-us4-validation. Confirm Minha voz with voz italic and <segura> visible as text; title Minha *prateleira* <autoral> with literal asterisks/tags; paragraph with Cynefin italic and <script> visible as harmless text; Torto Arado remains first and blue Cynefin is face-out. Add face: false under Cynefin, run check/draw/open and confirm a spine; remove it and redraw to restore the cover. Optionally restore shelf-2026-10-29-1112.yaml then draw/open for the generated wording, and restore shelf-2026-10-29-1112-02.yaml then draw/open for the authored wording.

Navigator accepted: no

Expected observation: Exact authored words appear safely; only lens and paragraph pairs are emphasized; citations guide automatic faces without reordering or overriding face; disposable restore returns each prior wording.

Pass condition: All authored copy, safe tag display, literal title stars, Cynefin automatic/explicit transitions, order and restore are visible through free commands.

Fail condition: Generated copy overrides edits, HTML executes, title stars become markup, books reorder, citation overrides face false, restore loses wording, or any paid/network service is requested.

## Missing Evidence

- Navigator validation has not been accepted
