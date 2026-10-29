# Plan — CV2.DS3.US6

## Objective

A paid creation must not become all-or-nothing at the final portrait call. Save
the reviewed books before asking for the portrait, make malformed portrait JSON
recoverable, and let the person finish with no further OpenRouter spend or retry
only the portrait with a new, explicit cost.

This preserves **Nada se perde**, **Gastar é sempre uma escolha** and the thin
client premise: resumable creation state and fallback composition belong to the
core; the terminal only persists the private draft, asks and explains.

## Scope

### Durable private draft

- Introduce a core `CreationDraft` containing the reader name, ordered photo
  names, final reviewed books, `left_out`, accumulated cost and migration state.
- Split creation into a core preparation step and a finishing step so any client
  can persist the draft before the portrait call.
- Persist the draft atomically as `.shelf/create-draft.yaml`; it contains no API
  keys, image bytes or local absolute paths and remains ignored by Git.
- Keep the draft until `shelf.yaml` has been written successfully. A failed
  portrait or failed source write never removes it.

### Portrait failure and retry

- Ask OpenRouter for a schema-constrained portrait response to reduce malformed
  JSON at the source.
- When parsing still fails, preserve the raw response privately under `.shelf/`
  together with the draft and report two explicit next actions instead of a bare
  JSON exception.
- Running `create` again with a compatible draft skips photo recognition,
  catalogue review and cover checks; it asks consent and cost for the portrait
  only.
- A stale or incompatible draft is never used silently. It reports why and
  leaves every file untouched.

### Free completion

- Add `uv run shelf recover [--folder PATH]`, a free command requiring neither
  keys nor network.
- `recover` creates `shelf.yaml` atomically from the saved draft, with an empty
  opening and one editable `Meus livros` section containing every preserved
  book in order. It does not pretend that an AI portrait succeeded.
- After successful recovery, the normal free `check`, `draw` and `open` route
  applies and the draft is removed only after `shelf.yaml` exists.

### Current Rafael run

- Do not infer an exact reviewed list from catalogue caches: they preserve query
  results, not the model's full review decisions or photo provenance.
- Investigate no-cost recovery through OpenRouter generation history. Their
  documented generation-content endpoint can return a stored prompt and
  completion when the generation ID/content is available. The failed portrait
  prompt contains the exact reviewed book list.
- If Rafael can obtain that failed request from OpenRouter Activity, prepare a
  private draft locally and use the same free recovery path. Do not commit,
  publish or print its book data.
- If generation content was not retained, report that exact recovery of this
  already-failed run is unavailable; an approximate cache reconstruction is not
  performed without a separate explicit decision.

## Non-Goals

- Do not pull or implement US5 (`Ask for another portrait`).
- Do not repair arbitrary malformed JSON with speculative text rewriting.
- Do not reconstruct or commit Rafael's real books, photos, keys, portrait or
  catalogue-cache contents.
- Do not change `shelf.yaml` version 1 or the existing free edit/draw/history
  contract.
- Do not make any OpenRouter request during automated or E2E validation.
- Do not automatically choose a generic portrait on the reader's behalf.

## Acceptance Behavior

```text
Given create has finished recognition, catalogue checks, review and covers
When the private creation draft is persisted
And the portrait response is malformed
Then no paid preparation is lost
And the error names the saved draft and the free recover route
And a later create retries only the portrait after explicit consent
```

```text
Given a valid saved creation draft and no shelf.yaml
When I run `uv run shelf recover --folder PATH`
Then shelf.yaml is created without API keys, network or OpenRouter
And every saved book appears once, in order, under an editable starter section
And check, draw and open can continue for free
```

```text
Given a saved draft no longer matches the shelf photos or source state
When create or recover examines it
Then the command refuses to use it silently
And preserves the draft, photos, caches and any existing source unchanged
```

```text
Given a normal successful create
When shelf.yaml has been written atomically
Then no stale creation draft or failed portrait response remains
And the existing create result and cost reporting remain compatible
```

## Design Decisions

- **Checkpoint before portrait, not after each photo.** The observed loss occurs
  after the complete reviewed list exists. This smallest checkpoint protects the
  expensive result without creating a general job engine.
- **Private draft rather than premature `shelf.yaml`.** The versioned source
  remains the reader's actual shelf. An unfinished paid run is explicit internal
  state, not a source that falsely claims a portrait exists.
- **Free starter shelf rather than automatic prose.** Empty lens and section text
  are already valid reader choices. Recovery preserves books without inventing
  a portrait or spending again.
- **Retry only the failed stage.** Repeating recognition would violate both cost
  choice and the user's expectation that completed paid work survives.
- **Schema-constrained output plus recovery.** Structured output reduces the
  probability of invalid JSON; the durable draft remains the safety guarantee.

## Implementation Contract

- TDD: characterize the current all-or-nothing failure first.
- Core owns draft construction, compatibility checks, starter composition and
  finishing a portrait; it performs no file I/O, input or printing.
- CLI owns atomic private-draft persistence, confirmation, messages and command
  dispatch.
- Private draft parsing is strict and versioned independently from `shelf.yaml`.
- Never log keys, raw photos, full real book lists or failed portrait contents.
- Use `uv run` for tests and checks.

Expected files:

- `src/shelf/core.py`
- `src/shelf/portrait.py`
- `src/shelf/openrouter.py`
- `src/shelf/cli.py`
- a small private-draft codec module if keeping it separate is clearer
- `tests/test_core.py`
- `tests/test_cli.py`
- `tests/test_main.py`
- `tests/test_recognition_and_portrait.py`
- user-facing command documentation and this story package

## Validation Route

1. Use a disposable folder with fake photos and local fake services.
2. Run a creation whose recognition/review succeeds and whose portrait returns
   malformed JSON.
3. Confirm no `shelf.yaml` exists, `.shelf/create-draft.yaml` exists, and the
   terminal offers both portrait-only retry and free recovery.
4. Run `recover` with API keys removed and network calls forbidden.
5. Run `check`, `draw` and `open`; confirm all saved books are present in the
   starter shelf.
6. In a second disposable folder, rerun `create` from the draft and confirm only
   the portrait fake is called and its portrait-only cost is confirmed.
7. For Rafael's existing folder, inspect only whether OpenRouter Activity exposes
   the failed generation content. Read or import the private content only after
   explicit consent; make no paid request.

**Expected observation:** paid preparation survives a broken portrait; the free
route produces an editable starter shelf, while the paid retry repeats only the
portrait.

**Pass condition:** no recognition/review call repeats after the draft exists;
free recovery works without keys/network; successful source creation cleans up
only its own draft; Rafael receives a truthful answer about exact no-cost
recovery.

**Fail condition:** the command spends before consent, rereads photos after a
saved draft, loses or exposes private data, writes an incomplete source as if it
were a portrait, or silently reconstructs a founder shelf from lossy caches.

## E2E Decision

Required, fully offline. Real OpenRouter calls are forbidden. The current Rafael
folder is recovery evidence, not a fixture and never enters tests or Git.

## Approval Gate

- Approved by the Navigator on 2026-10-29.
- Approval authorizes only CV2.DS3.US6 through the automated/E2E evidence and
  Navigator Validation checkpoint.
- Push remains a separate explicit authorization.
