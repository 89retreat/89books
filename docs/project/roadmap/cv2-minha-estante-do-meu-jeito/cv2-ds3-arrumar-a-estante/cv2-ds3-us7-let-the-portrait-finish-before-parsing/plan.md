# Plan — CV2.DS3.US7

## Objective

Stop Claude Sonnet 5.5 from spending the portrait's complete token allowance on
mandatory adaptive thinking before it finishes the schema-constrained JSON.
After the fix, Rafael's saved draft can retry only the portrait and receive a
complete response under the model's current API contract.

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
and no longer supports non-default sampling parameters. The existing request is
therefore undersized and uses an obsolete parameter.

## Scope

1. Make sampling temperature optional in `openrouter.complete(...)` and omit it
   from the HTTP body when absent.
2. Allow callers to send OpenRouter's `reasoning` control without changing the
   response tuple used by existing stages.
3. Send portrait requests with explicit low reasoning effort, hidden reasoning
   text, no temperature, and a 16,000-token shared allowance.
4. Keep JSON Schema output, strict portrait parsing, private failed-response
   preservation and portrait-only retry unchanged.
5. Document the Claude 5.5 request policy and the real truncation evidence.

## Non-Goals

- Do not recover a complete portrait from the truncated text.
- Do not make a paid OpenRouter call during implementation or automated
  validation.
- Do not change recognition, review, catalogue lookup, cover lookup or
  `shelf.yaml` v1.
- Do not silently retry paid calls.
- Do not pull conditional `CV2.DS3.US5`.

## Acceptance Behavior

```text
Given a large saved creation draft whose portrait must cover hundreds of books
When create retries only the portrait
Then the OpenRouter request uses JSON Schema, reasoning effort low, no temperature and max_tokens 16000
And the complete response remains subject to the same strict parser
And malformed or truncated replies are still preserved privately
And recognition, review, catalogues and covers are not repeated
```

## Implementation Sequence

1. Add failing unit tests for optional temperature/reasoning request fields and
   the exact portrait request policy.
2. Extend `openrouter.complete(...)` with optional request controls.
3. Change only `write_portrait(...)` to use the new Claude 5.5-safe policy.
4. Run focused tests, the complete suite and Ruff checks.
5. Exercise an offline E2E with the existing saved-draft fixture and a fake
   complete long portrait response; do not contact OpenRouter.
6. Stop at Navigator validation before any real paid retry.

## Validation Route

Automated:

```bash
uv run pytest tests/test_openrouter.py tests/test_recognition_and_portrait.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Offline E2E:

- retain a saved creation draft;
- replace the network completion with a long schema-valid fixture;
- run the portrait-only continuation;
- verify `shelf.yaml` is produced and the draft is removed only after success;
- verify no recognition/review/catalogue/cover path runs.

Navigator-visible route after implementation:

```bash
uv run shelf create --folder ~/89books/my-bookshelf/rafael-caceres/
```

Expected observation: the command identifies saved work and asks consent only
for another portrait. After consent, it does not recognize the 12 photos again
and either completes `shelf.yaml` or preserves the same draft if the external
service still fails.

Pass condition: the request finishes the portrait and draws Rafael's shelf while
keeping the paid recognition result intact.

Fail condition: recognition repeats, the response is cut again under the new
allowance, an obsolete sampling parameter is sent, or the draft disappears
before a valid `shelf.yaml` exists.

## Implementation Contract

- Use TDD for the OpenRouter and portrait request behavior.
- Keep the public completion return contract `(text, cost)` unchanged.
- Use `uv run` for Python commands and checks.
- Commit only story-scoped files with an English message explaining why.
- Make no paid OpenRouter request during implementation.
- Stop at Navigator validation before Rafael's real portrait-only retry.

## Cost and Consent

Implementation and automated validation are free. The final real validation is
a portrait-only paid retry and still requires the Navigator's explicit consent
at the CLI prompt. No implementation command may bypass it.

## Stop Conditions

- OpenRouter rejects the documented `reasoning` body.
- The fix requires changing model or provider rather than request controls.
- A complete response exceeds the 16,000-token allowance in an offline fixture.
- Any change would repeat or discard Rafael's saved recognition work.
- Any real paid validation lacks explicit consent.

## Approval Gate

The Navigator explicitly requested `Temos que corrigir o erro.` after authorizing
inspection of the private failed response. That request preauthorizes this exact
smallest corrective plan through implementation and free validation. Stop before
the real paid retry for Navigator validation.
