# Validation — CV1.DS3.US3

## Status

Blocked

## Automated Checks

- uv run pytest (98 passed); ruff clean; real review over Lula's saved books (US$0.047): 6 long names answered by the model, the other 37 lone surnames fixed by the rule; spines checked in the browser, title keeps at least 58px

Checks status: passed

## E2E

Decision: required

Evidence: Real model review over Lula's saved books and the re-rendered page in the browser

## Navigator Validation

Route: Open ~/Downloads/estante-lula-nomes.html

Navigator accepted: no

Expected observation: Every spine shows first name and surname, long names in two columns, titles visible

Pass condition: No lone surname; names fit without hiding the title

Fail condition: A lone surname, a name that was right and became wrong, or a name hiding the title

## Missing Evidence

- Navigator validation has not been accepted
