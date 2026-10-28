# Validation — CV2.DS1.US3

## Status

Blocked

## Automated Checks

- uv run pytest: 157 passed
- uv run ruff check . && uv run ruff format --check .: passed

Checks status: passed

## E2E

Decision: required

Evidence: Free driver E2E on /tmp/estante-alisson-validacao-us3: first changed draw saved exact source, unchanged draw added no version, metadata-only history listed one entry, a deliberately broken source was backed up and restored from the selected valid version, shelf.html hash survived, check passed, and the panel reported two versions. Automated fakes cover successful and failed paid recreation, backup-before-replace, confirmation refusal, --yes, retention 20 and write failures.

## Navigator Validation

Route: Use /tmp/estante-alisson-validacao-us3 step by step: edit and draw, draw unchanged, history, break and restore, then check. Finally run recreate, first decline, then inspect the one-photo estimate and continue only after explicit approval; restore the pre-recreate version and draw.

Navigator accepted: no

Expected observation: Every changed or replaced source has a named backup; unchanged draw adds none; history shows metadata only; broken current bytes survive restore; recreate does not mutate or spend when declined and preserves the old source before a confirmed replacement.

Pass condition: The Navigator can recover the edit, accepts metadata-only history and retention, and observes at most one explicitly confirmed one-photo paid recreation.

Fail condition: Any edit disappears, history content is compared without consent, an unknown file is deleted, restore installs invalid YAML, page changes outside draw, or paid work begins without confirmation.

## Missing Evidence

- Navigator validation has not been accepted
