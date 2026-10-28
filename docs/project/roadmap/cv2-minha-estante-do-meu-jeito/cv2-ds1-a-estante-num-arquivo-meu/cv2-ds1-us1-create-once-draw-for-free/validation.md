# Validation — CV2.DS1.US1

## Status

Passed

## Automated Checks

- uv run pytest (128 passed); ruff check and format clean; unit coverage for create refusal, CV1 migration service isolation, free draw, atomic preservation and open; synthetic no-key draw E2E

Checks status: passed

## E2E

Decision: required

Evidence: Real CV1 migration on a disposable Lula copy: 160 saved books to 7 shelves, only portrait call, 0.03 US dollars, books.yaml and caches unchanged, free no-key draw, lens edit reflected, no local paths; copy deleted

## Navigator Validation

Route: On a disposable copy: run create, draw and open; edit lens and draw again on desktop and mobile; introduce a YAML error and confirm the previous page remains

Navigator accepted: yes

Expected observation: create reuses books.yaml and confirms only portrait cost; draw is free and reflects the edit; open opens the page; line-numbered error leaves prior page unchanged

Pass condition: No recognition or catalogue calls, no replacement of shelf.yaml, no key or spend during draw, desktop/mobile page matches the file, and invalid YAML preserves the page

Fail condition: Implicit spend, lost file/page, photo reread, ignored edit, missing line number, or desktop/mobile page mismatch

## Missing Evidence

- none
