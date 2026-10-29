---
date: 2026-10-29T17:02:00Z
author: Driver
kind: milestone
related:
  - CV2.DS3.US6
verification:
  - uv run pytest — 221 passed
  - uv run ruff check .
  - uv run ruff format --check .
  - Navigator screenshot of the recovered starter shelf
---

# Paid creation recovery validated

## What changed

The first founder run exposed an all-or-nothing boundary: recognition, review,
catalogues and covers completed for 12 photos, but malformed JSON in the final
portrait call left no `shelf.yaml`. Creation now persists a strict private draft
before that call. A failed portrait preserves its raw response locally and
offers two explicit routes: `shelf recover`, which creates an editable starter
source for free, or another `create`, which repeats only the portrait after cost
confirmation.

Portrait requests now use OpenRouter JSON Schema. The core owns preparation,
finishing and order-preserving starter composition; the CLI owns atomic private
persistence, consent and cleanup. `shelf.yaml` remains version 1.

## Why it matters

Paid recognition is no longer silently discarded by a final formatting error.
The behavior gives operational meaning to **Nada se perde** and **Gastar é
sempre uma escolha**: the person can keep every prepared book without another
model call and no generic portrait is invented on their behalf.

## Verification

The complete suite passed with 221 tests and Ruff green. Offline E2E proved
both free recovery and portrait-only retry without repeating recognition or
review. The Navigator then ran `recover`, `check`, `draw` and `open` against a
disposable failed creation and supplied a screenshot showing an empty opening,
one `Meus livros` section and the three books in preserved order.

## Follow-up

Rafael's original failure predates the new private draft. Exact no-cost recovery
of that already-failed run is possible only if OpenRouter Activity retained the
failed generation prompt/completion, whose prompt contains the final reviewed
book list. Catalogue caches alone are intentionally not treated as an exact
source. CV2.DS3 returns to founder validation; US5 remains conditional and
unpulled.
