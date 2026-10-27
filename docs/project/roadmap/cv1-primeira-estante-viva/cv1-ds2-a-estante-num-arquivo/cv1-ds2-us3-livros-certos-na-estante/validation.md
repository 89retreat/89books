# Validation — CV1.DS2.US3

## Status

Passed

## Automated Checks

- uv run pytest (64 passed); ruff clean; real runs on Lula's photos with both keys; author-first spines, same-author grouping and 'Quem mais mora aqui' checked at 1440, 900 and 390 px, including window resize

Checks status: passed

## E2E

Decision: required

Evidence: Automated end-to-end tests with simulated network; real generations by the Driver

## Navigator Validation

Route: Open ~/Downloads/estante-lula-us3.html, sent to Lula

Navigator accepted: yes

Expected observation: Corrected titles, author-first spines, same-author groups, closing shelf 'E mais livros que já me acompanharam'

Pass condition: Navigator and Lula recognize titles and authors

Fail condition: Right books turned wrong, books missing without reason, closing shelf reads as leftovers

## Missing Evidence

- none
