# Validation — CV1.DS2.US3

## Status

Blocked

## Automated Checks

- uv run pytest (53 passed); ruff clean; real run on Lula's photos without a Google Books key: 164 books, 19 titles corrected, 2 duplicates merged, books without author 31/164 (was 71/152), US$0.16; 'Continuo Preta' still wrong without Google Books

Checks status: passed

## E2E

Decision: required

Evidence: Automated end-to-end test with simulated network (misread title corrected before the page); real run by the Driver

## Navigator Validation

Route: Open ~/Downloads/estante-lula-us3.html with Lula; ideally regenerate with GOOGLE_BOOKS_API_KEY

Navigator accepted: no

Expected observation: Corrected titles, author surnames on spines, closing shelf without numeral titled as books that once caught my attention

Pass condition: Lula recognizes titles and authors and the closing shelf no longer reads as leftovers

Fail condition: A right book turned wrong, books missing without reason, or the closing shelf still reads as leftovers

## Missing Evidence

- Navigator validation has not been accepted
