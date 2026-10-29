# Plan — CV2.DS3.US7

## Objective

Stop Claude Sonnet 5.5 from exhausting the portrait's token allowance before it
finishes the schema-constrained JSON, and explain any future external failure in
plain language while keeping the reader's paid work safe.

The change applies only to the portrait-writing call. Photo recognition keeps
its current request and therefore its reading effectiveness is not changed by
this story.

## Diagnosis

The authorized failed response is 1,725 characters long and ends inside a JSON
string. Its prefix is structurally valid through two complete themes and part of
the third. This is truncation, not a punctuation mistake inside a complete
response.

`write_portrait(...)` currently sends:

- `max_tokens=4000`;
- `temperature=0.7`;
- no reasoning effort.

OpenRouter's Claude Sonnet 5.5 migration guide says that adaptive thinking is
mandatory, defaults to high effort, shares `max_tokens` with the visible reply,
and no longer supports non-default sampling parameters.

The 237 books contributed to the failure because the portrait response grows
with the number of book indexes assigned to themes. They were not the sole
cause: the small shared limit and high default reasoning left too little room
for the visible JSON. The photos themselves had already been read successfully.

## Scope

1. Make sampling temperature optional in `openrouter.complete(...)` and omit it
   from the HTTP body when absent.
2. Allow callers to send OpenRouter's `reasoning` control and optionally require
   a complete response, without changing the normal `(text, cost)` return tuple.
3. Send only portrait requests with:
   - explicit low reasoning effort;
   - reasoning text excluded from the response;
   - no temperature;
   - a 64,000-token shared ceiling;
   - the existing strict JSON Schema.
4. Inspect OpenRouter's `finish_reason`. If it reports a token cutoff, preserve
   the partial response and classify the portrait as unfinished before parsing.
5. Keep strict parsing for responses that claim to be complete. Preserve any
   unusable response privately as today.
6. Replace the technical CLI error with a reader-facing message that says:
   - what happened in plain language;
   - how many reviewed books remain safe;
   - that photo recognition and catalogue lookup will not repeat;
   - whether free `recover` or portrait-only `create` is the next choice;
   - the cost of the failed portrait attempt when OpenRouter reports it.
7. Keep portrait-only retry, draft compatibility and `shelf.yaml` v1 unchanged.

## Why This Does Not Merely Move the Same Bottleneck

Every model request has a finite limit, so no fixed ceiling can mathematically
support an unlimited shelf. This story removes the actual bottleneck in three
layers:

1. low reasoning prevents a simple formatting task from consuming most tokens
   before writing;
2. 64,000 tokens gives the bounded 3–6-theme portrait ample room for realistic
   personal shelves and is not billed merely because it is available;
3. `finish_reason` detection turns any future size limit into an explicit,
   recoverable product state instead of presenting truncated JSON as a parsing
   mystery.

A fundamentally unbounded shelf would require a different portrait protocol,
such as hierarchical summarization. That is not justified by the current
237-book evidence and is outside this corrective story.

## Non-Goals

- Do not change photo recognition prompts, reasoning, model or token limits.
- Do not recover a complete portrait from the truncated text.
- Do not make a paid OpenRouter call during implementation or automated
  validation.
- Do not change review, catalogue lookup, cover lookup or `shelf.yaml` v1.
- Do not silently retry paid calls.
- Do not pull conditional `CV2.DS3.US5`.

## Acceptance Behavior

```text
Given a large saved creation draft whose portrait must cover hundreds of books
When create retries only the portrait
Then recognition and catalogue stages do not run again
And the portrait request uses JSON Schema, reasoning effort low, no temperature and max_tokens 64000
And OpenRouter token truncation is detected from finish_reason before JSON parsing
And a complete response remains subject to the same strict parser
And every unusable response remains private and recoverable
And the terminal explains the failure without exposing JSON terminology
```

## Implementation Sequence

1. Add failing unit tests for optional temperature/reasoning fields, completion
   enforcement and the exact portrait request policy.
2. Add failing CLI tests for separate unfinished-response and unusable-response
   messages, including safe book count, no-repeat assurance and reported cost.
3. Extend `openrouter.complete(...)` with optional request controls and a typed
   incomplete-response exception carrying partial text and cost.
4. Change only `write_portrait(...)` to use the Claude 5.5-safe policy and map
   incomplete responses into `PortraitResponseError` with a reason category.
5. Improve the CLI message while retaining private draft and failed-response
   writes.
6. Run focused tests, the complete suite and Ruff checks.
7. Exercise an offline E2E with the saved-draft fixture and both truncated and
   complete fake responses; do not contact OpenRouter.
8. Stop at Navigator validation before any real paid retry.

## Validation Route

Automated:

```bash
uv run pytest tests/test_openrouter.py tests/test_recognition_and_portrait.py tests/test_cli.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Offline E2E:

- retain a saved creation draft;
- return a fake response with `finish_reason=length` and verify the friendly
  message plus preserved draft/partial response;
- return a long schema-valid response with `finish_reason=stop`;
- verify `shelf.yaml` is produced and the draft is removed only after success;
- verify no recognition/review/catalogue/cover path runs.

Navigator-visible route after implementation:

```bash
uv run shelf create --folder ~/89books/my-bookshelf/rafael-caceres/
```

Expected observation: the command identifies 237 saved books and asks consent
only for another portrait. After consent, it does not recognize the 12 photos
again. A successful response creates `shelf.yaml`; another external failure
explains the outcome plainly and leaves the same draft recoverable.

Pass condition: the request finishes the portrait and draws Rafael's shelf while
keeping the paid recognition result intact.

Fail condition: recognition repeats, the response is cut again without a clear
unfinished-response message, an obsolete sampling parameter is sent, technical
JSON language reaches the reader, or the draft disappears before a valid
`shelf.yaml` exists.

## Implementation Contract

- Use TDD for OpenRouter, portrait and CLI behavior.
- Keep ordinary completion calls and photo recognition behavior unchanged.
- Keep the public normal return contract `(text, cost)` unchanged.
- Use `uv run` for Python commands and checks.
- Commit only story-scoped files with an English message explaining why.
- Make no paid OpenRouter request during implementation.
- Stop at Navigator validation before Rafael's real portrait-only retry.

## Cost and Consent

Implementation and automated validation are free. A 64,000-token ceiling does
not charge 64,000 tokens; OpenRouter charges actual input, reasoning and output.
Low reasoning should reduce waste relative to the failed high-effort request.

The final real validation is a portrait-only paid retry and still requires the
Navigator's explicit consent at the CLI prompt. No implementation command may
bypass it.

## Stop Conditions

- OpenRouter rejects the documented `reasoning` body.
- The response does not expose a usable `finish_reason`.
- The fix requires changing model or provider rather than request controls.
- Any change affects photo recognition request behavior.
- Any change would repeat or discard Rafael's saved recognition work.
- Any real paid validation lacks explicit consent.

## Approval Gate

Pending explicit Navigator approval of this revised plan. Implementation stops
at Navigator validation and cannot perform Rafael's real paid retry.
