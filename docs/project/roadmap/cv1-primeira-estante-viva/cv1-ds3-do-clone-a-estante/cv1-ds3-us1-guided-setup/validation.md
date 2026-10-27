# Validation — CV1.DS3.US1

## Status

Blocked

## Automated Checks

- uv run pytest (79 passed); ruff clean; clean clone in /tmp driven through a pseudo-terminal: wrong key refused before any photo, balance shown, config saved, estimate US$0.17 matched the spend; git status clean; no keys or paths in the HTML

Checks status: passed

## E2E

Decision: required

Evidence: Automated tests with simulated input and network; real setup and generation by the Driver in a clean clone

## Navigator Validation

Route: In a clean clone with your own photos in my-bookshelf/, run uv run shelf (together with US2, in the DS3 validation)

Navigator accepted: yes (2026-10-27, with US2, as the DS3 validation)

Expected observation: Asks name and keys with instructions, checks keys, saves config, confirms cost, generates the shelf

Pass condition: Reaches the shelf without editing files or asking for help; announced cost matches the spend

Fail condition: Confusing question, bad key found mid-generation, surprise cost, or key or photo in git status

## Missing Evidence

- none
