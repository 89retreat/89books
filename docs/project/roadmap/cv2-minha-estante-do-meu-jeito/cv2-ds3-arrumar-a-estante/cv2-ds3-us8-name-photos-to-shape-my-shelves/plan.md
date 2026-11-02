# Plan: CV2.DS3.US8 Name photos to shape my shelves

## Objective

Let the reader shape the first editable shelf before any portrait interpretation
by naming section photos `NN_Título.ext`. The generated source preserves that
order, literal title, photo association and book membership while the model
contributes only the opening and prose around the fixed arrangement.

## Scope

- Recognize an intentional photo name only when its stem matches two digits, an
  underscore and a non-empty title, such as `01_Tecnologia e Produto.jpg`.
- Preserve accents and capitalization in the title. Replace additional
  underscores in the title with spaces.
- Sort named shelves by the numeric prefix and reject duplicate positions or
  duplicate normalized titles before any paid call.
- Show the detected named shelves in the terminal before spending and state
  that their names and order will be preserved.
- Keep every reviewed book in the section named by its provenance photo. Books
  from unnamed photos remain unassigned and flow to the existing closing shelf.
- Give the portrait model the fixed section titles and membership so it can
  write the lens and each section text. Enforce the human arrangement again in
  the core after the model returns.
- Add optional `photo` to `ShelfSection` in `shelf.yaml` version 2. Continue
  reading and drawing version 1 without rewriting it. New creation, recovery
  and recreation produce version 2.
- Render a section photo inside the associated shelf while retaining the
  existing top mosaic and `cover_photo` behavior.
- Reject a section photo that is not one of the root shelf photos during
  `check` and `draw`, preserving the previous page.
- Preserve named shelf information in the private creation draft through the
  existing photo names and per-book provenance, so free recovery and
  portrait-only retry keep the arrangement.
- Update public usage documentation with the naming convention and version 2
  example.

## Non-Goals

- Multiple photos for one section.
- Nested photo folders, sidecar metadata or a separate configuration file.
- Guessing titles from arbitrary camera, WhatsApp or timestamp names.
- Continuous synchronization after `shelf.yaml` exists. The YAML becomes the
  authority after creation.
- Automatic migration that rewrites an existing version 1 source merely
  because `draw` or `check` runs.
- Image captions, crop controls, focal points or removal of the top mosaic.
- A new paid portrait command or `CV2.DS3.US5`.

## Implementation Approach

Introduce a pure named-photo parser and an immutable section hint carrying
position, literal title, file name and recognized book indexes. The core derives
hints from draft photo names and reviewed book provenance. Portrait generation
receives those hints for better prose, but the core replaces returned titles and
membership with the hints before creating the source.

Evolve the source contract to read versions 1 and 2. Version 1 keeps its exact
fields. Version 2 permits an optional non-empty `photo` on each section. Dumping
a section photo as version 1 is refused rather than silently losing meaning.
New sources use version 2; existing version 1 sources stay readable, drawable,
historical and restorable.

The terminal remains a thin client. Filename interpretation, arrangement,
version semantics and photo validation live in pure core or contract functions.
The terminal only presents the detected arrangement, confirms spending and
resolves local photo assets for drawing.

## Test Strategy

Use TDD for filename parsing, duplicate rejection, fixed book membership,
portrait enforcement, recovery, version 1 compatibility, version 2 round-trip,
missing section photos, rendering and terminal preview. Run focused tests first,
then the complete suite and Ruff checks.

Exercise an offline end-to-end fixture with named and unnamed photos. Fake paid
services recognize different books per photo and attempt to return a conflicting
portrait. The resulting YAML and HTML must preserve the human names, order,
photo association and membership while leaving unnamed books in the closing
shelf.

## Validation Route

Prepare a disposable folder with two consented sample shelf photos renamed:

```text
01_Tecnologia.jpg
02_Literatura.jpg
```

Run `create` with the normal cost confirmation, then `check`, `draw` and `open`.
Use only a small subset so validation does not reread the complete founder
shelf.

Expected observation: before spending, the terminal lists Tecnologia and
Literatura in order. The resulting version 2 YAML contains those literal titles,
each section photo and the books recognized from that photo. The page shows each
photo in its section.

Pass condition: the model writes prose but cannot rename, reorder or move books
out of named sections; unnamed books go to the closing shelf; `check` and `draw`
are free and pass.

Fail condition: a generic filename becomes a shelf unexpectedly, paid work
starts before naming errors are reported, the model overrides the human
arrangement, version 1 stops drawing, or a missing section photo replaces a
valid page.

E2E decision: required. The paid Navigator route uses only a small consented
subset; all implementation checks remain offline.

## Acceptance Behavior

```text
Given photos named 01_Tecnologia.jpg and 02_Literatura.jpg
And books recognized from each photo
When create writes the first shelf.yaml
Then version 2 contains Tecnologia and Literatura in that order
And each section keeps its photo and the books recognized from it
And the generated page shows the associated photo in its section
And the portrait may write lens and section text but cannot rename or move the named shelves
```

## Product Principle Preserved

This story preserves `Cada leitor revela a própria lógica` and `A última
palavra é de quem lê`. Naming photos is not metadata cleanup; it is the first
authorial gesture. The model completes that gesture instead of replacing it.

## Implementation Contract

- Use `uv run` for Python commands and checks.
- Use TDD for every observable behavior.
- Keep human arrangement logic in the core and terminal presentation in the
  CLI.
- Never read, copy or commit Rafael's real photos or shelf source.
- Make no paid call during implementation or automated validation.
- Commit only story-scoped files with an English message explaining why.
- Stop at Navigator Validation before any real paid subset run.

## Stop Conditions

- Supporting version 2 would require silently rewriting version 1 files.
- The model cannot receive fixed sections without changing unrelated recognition
  behavior.
- Mixed named and unnamed photos cannot preserve deterministic membership.
- Section images require publishing or copying original photo paths into HTML.
- A paid validation would use the complete founder shelf or lack explicit
  consent.
- Scope expands into multiple photos per section or continuous synchronization.

## Approval Gate

The Navigator asked to create, pull and implement this exact story. Accelerated
cadence records bounded authority through local implementation and offline
validation, with a fixed stop at Navigator Validation.

- Approved by: Navigator
- Approved on: 2026-11-01
