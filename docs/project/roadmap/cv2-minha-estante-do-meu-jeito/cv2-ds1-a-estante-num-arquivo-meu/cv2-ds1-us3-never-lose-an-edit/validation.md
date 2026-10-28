# Validation — CV2.DS1.US3

## Status

Passed

## Automated Checks

- uv run pytest: 157 passed
- uv run ruff check . && uv run ruff format --check .: passed

Checks status: passed

## E2E

Decision: required

Evidence: Navigator validated /tmp/estante-alisson-navigator-us3 step by step: history began empty; edited lens then draw saved shelf-2026-10-28-1729.yaml; unchanged draw added no version; history listed metadata only; a deliberately broken source was saved as shelf-2026-10-28-1731.yaml before restore; check passed; recreate was first declined with no spend, then explicitly approved for one photo (estimated US$0.09, actual US$0.03), saved shelf-2026-10-28-1736.yaml and left the page untouched; restoring it saved the recreated source as shelf-2026-10-28-1737.yaml; explicit draw and opening the page showed the recovered shelf correct.

## Navigator Validation

Route: Completed by the Navigator: free snapshot/unchanged/history/restore/check route, then one explicitly authorized one-photo recreate, restore and draw/open.

Navigator accepted: yes

Expected observation: Every replacement announces a backup; unchanged draw adds none; history is metadata only; restore recovers the earlier shelf; recreate requires consent and page only changes on explicit draw.

Pass condition: Navigator recovered the shelf and confirmed the final page is correct after the one-photo paid recreation and restore.

Fail condition: Any edit disappears, history exposes or compares contents, paid recreation starts without confirmation, or restored page is incorrect.

## Missing Evidence

- none
