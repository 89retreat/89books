[< Story](index.md)

# Test Guide — CV2.DS3.US6

## Automated Validation

```bash
uv run pytest tests/test_core.py tests/test_cli.py tests/test_main.py tests/test_recognition_and_portrait.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Required coverage:

- post-review draft is complete and pure core data;
- malformed portrait preserves draft and cost context;
- normal success removes private recovery artifacts only after `shelf.yaml`;
- retry from draft calls portrait only;
- free recovery calls no paid/network service;
- starter shelf preserves every book exactly once and in order;
- incompatible/corrupt drafts fail without changing source or draft;
- help/status/messages distinguish free recovery from paid portrait retry;
- portrait request uses schema-constrained output.

## E2E Decision

Required and offline. Use disposable photos and fake service responses. Any
OpenRouter request during E2E is a failure.

## Navigator Validation

In a disposable folder:

1. trigger a malformed portrait after successful fake preparation;
2. observe the saved private draft and actionable error;
3. remove API keys and run `uv run shelf recover --folder PATH`;
4. run `check`, `draw` and `open`;
5. confirm the starter page contains every prepared book and no invented
   portrait prose;
6. separately retry `create` from a draft and observe a portrait-only consent
   message with no recognition progress.

Expected: the paid work survives, free recovery is genuinely free, and a paid
retry repeats only the portrait.

Pass: all books remain available and both routes behave as labelled.

Fail: photos are reread, another paid call happens during recovery, private data
is exposed, or the draft disappears before a complete source exists.

## Existing Rafael Run

The local caches prove that catalogue and cover work was saved, but not the full
reviewed list. Exact no-cost recovery is conditional on the failed generation's
stored prompt/completion being available through OpenRouter Activity or its
documented generation-content endpoint. Inspect or import that content only with
explicit consent. Never copy it into this repository or test output.

## Validation Evidence

Pending implementation and Navigator validation.
