# Validation — CV2.DS1.TS1

## Status

Blocked

## Automated Checks

- uv run pytest (106 passed); ruff clean; architecture test fails on purpose-added import sys and print in core.py; real uv run shelf with one photo (US$0.03): same messages and files as before

Checks status: passed

## E2E

Decision: required

Evidence: Tests with fake services and one real run with one photo

## Navigator Validation

Route: Review the boundary between src/shelf/core.py and src/shelf/cli.py in the diff

Navigator accepted: no

Expected observation: core.generate returns the shelf as data, core.draw returns the HTML; cli only builds services, writes files and talks to the person

Pass condition: The command works as before and the core does not talk to the terminal

Fail condition: A visible change for the person, or product logic left in cli

## Missing Evidence

- Navigator validation has not been accepted
