[< Story](index.md)

# Test Guide — CV2.DS3.US7

## Automated Validation

### OpenRouter request contract

- When `temperature` is absent, the HTTP JSON body omits it.
- When `reasoning` is supplied, the body preserves it exactly.
- Existing `response_format` and `provider.data_collection=deny` remain.
- Ordinary complete responses keep returning `(text, cost)`.
- When completion enforcement is requested and `finish_reason` reports a token
  cutoff, a typed exception preserves partial text, cost and finish reason.

### Portrait request policy

`write_portrait(...)` must request:

- `max_tokens=64000`;
- no temperature;
- `reasoning={"effort": "high", "exclude": true}`;
- complete-response enforcement;
- the existing strict JSON Schema.

Valid complete responses continue through `parse_portrait(...)`. Token-cutoff
responses and complete-but-invalid responses both become `PortraitResponseError`
with distinct reason categories and preserved response/cost.

### Reader-facing failure

For a token cutoff, the CLI says that OpenRouter stopped before finishing the
portrait. For another unusable response, it says that the returned portrait
could not be used safely.

Both messages must:

- avoid JSON/parser terminology;
- state how many reviewed books are safe;
- state that photos and catalogue lookup will not repeat;
- show free `recover` and portrait-only `create` choices;
- include the failed attempt cost when positive;
- keep `.shelf/create-draft.yaml` and `.shelf/failed-portrait.txt`.

### Regression

Run the complete suite so recognition, review, draft recovery, retry, rendering,
history and direct YAML editing remain unchanged. Tests must assert that photo
recognition calls retain their existing arguments.

## E2E Decision

Required offline before Navigator validation. No paid model call is permitted in
automated E2E.

Use a saved creation draft plus fake OpenRouter responses:

1. `finish_reason=length` with partial content: friendly message and recovery
   files remain;
2. `finish_reason=stop` with a long valid portrait: `shelf.yaml` is written,
   recovery files are removed, and upstream paid stages do not repeat.

## Navigator Validation

Run:

```bash
uv run shelf create --folder ~/89books/my-bookshelf/rafael-caceres/
```

The CLI must find 237 saved books and present only the portrait retry cost. The
Navigator decides whether to authorize that paid request.

Expected: no photo recognition, title review, catalogue lookup or cover fetching
appears. A successful response creates the shelf; another external failure keeps
the draft recoverable and explains the next choices without technical parser
language.

## Validation Evidence

Pending implementation and validation.
