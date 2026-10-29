[< Story](index.md)

# Test Guide — CV2.DS3.US7

## Automated Validation

### OpenRouter request contract

- When `temperature` is absent, the HTTP JSON body omits it.
- When `reasoning` is supplied, the body preserves it exactly.
- Existing `response_format` and `provider.data_collection=deny` remain.
- The return contract remains `(text, cost)`.

### Portrait request policy

`write_portrait(...)` must request:

- `max_tokens=16000`;
- no temperature;
- `reasoning={"effort": "low", "exclude": true}`;
- the existing strict JSON Schema.

Valid responses continue through `parse_portrait(...)`. Invalid or truncated
responses continue to raise `PortraitResponseError` with response and cost for
private recovery.

### Regression

Run the complete suite so recognition, review, draft recovery, retry, rendering,
history and direct YAML editing remain unchanged.

## E2E Decision

Required offline before Navigator validation. No paid model call is permitted in
automated E2E.

Use a saved creation draft plus a fake long complete portrait response. Confirm
that portrait-only continuation writes and draws the shelf, does not repeat
upstream paid stages, and removes the draft only after success.

## Navigator Validation

Run:

```bash
uv run shelf create --folder ~/89books/my-bookshelf/rafael-caceres/
```

The CLI must find the saved work and present only the portrait retry cost. The
Navigator decides whether to authorize that paid request.

Expected: no photo recognition, title review, catalogue lookup or cover fetching
appears. A successful response creates the shelf; another external failure keeps
the draft recoverable.

## Validation Evidence

Pending implementation and validation.
