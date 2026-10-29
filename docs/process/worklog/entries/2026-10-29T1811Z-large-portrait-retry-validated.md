---
date: 2026-10-29T18:11:00Z
author: Driver
kind: milestone
related:
  - CV2.DS3.US7
verification:
  - uv run pytest — 225 passed
  - uv run ruff check .
  - uv run ruff format --check .
  - Offline E2E with 237 books and finish_reason length/stop
  - Navigator real portrait-only retry for Rafael
---

# Large portrait retry validated

## What changed

The first protected retry exposed the cause behind the malformed portrait: the
Claude Sonnet 5.5 reply was a valid JSON prefix cut inside its third theme.
Portrait requests now preserve high reasoning quality, omit the obsolete
sampling temperature, share a 64,000-token allowance between reasoning and
answer, and require OpenRouter to report a complete finish before parsing.

An unfinished completion keeps its partial response and cost inside the private
recovery area. The terminal no longer talks about JSON or parsers: it says that
OpenRouter stopped before finishing, names how many reviewed books remain safe,
confirms that photos and catalogues will not run again, and offers the free
starter or portrait-only retry routes.

## Why it matters

The recovery path now works as a complete product loop rather than only a safety
net. A large shelf can retain the portrait quality the founders expect without
silently trading it for a smaller reasoning budget. If an external limit is met
again, the reader sees a clear choice instead of an implementation detail.

## Verification

Focused tests passed with 47 checks; the complete suite passed with 225 tests
and Ruff remained green. An offline E2E sent a synthetic 237-book draft through
the real OpenRouter client path: `finish_reason=length` preserved the draft and
showed the friendly message, while `finish_reason=stop` produced all 237 books
without repeating recognition, review, catalogues or covers.

The Navigator then updated Rafael's clone and ran the real portrait-only retry.
It succeeded and was explicitly accepted. The story passed validation, debt
review found no action, coherence passed and `CV2.DS3.US7` closed as Done.

## Follow-up

Rafael's generated shelf is now real founder material for the aggregate
`CV2.DS3` validation. The Delivery Story remains active until a founder uses
order, face/spine, cover photo and authored language together, then shows the
result as “minha estante”. `CV2.DS3.US5` remains conditional and unpulled.
