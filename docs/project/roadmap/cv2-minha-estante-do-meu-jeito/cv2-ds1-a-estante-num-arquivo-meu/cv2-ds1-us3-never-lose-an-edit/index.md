---
code: CV2.DS1.US3
level: User Story
status: Implemented
status_reason: histórico, restore e recreate passaram em 157 testes e E2E gratuito; aguarda validação do Navigator
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds1-us1-create-once-draw-for-free/index.md
  - ../cv2-ds1-us2-know-where-my-shelf-stands/index.md
  - ../../../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md
---

[< Parent](../index.md)

# CV2.DS1.US3 — Never lose an edit

**Status:** Implemented
**Type:** User Story

---

## User Story

In order to experimentar com a estante sem medo,
As uma pessoa que edita `shelf.yaml` ou decide recriá-lo,
I want ter versões automáticas e poder voltar a uma delas,
So that nenhum comando apaga silenciosamente o que eu fiz.

## Outcome

- `draw` guarda o `shelf.yaml` atual quando seu conteúdo mudou desde o último
  desenho; repetir `draw` sem mudança não cria cópia.
- `recreate` confirma o custo, refaz a partir das fotos e guarda o arquivo
  atual antes da substituição.
- `history` lista as versões mais recentes sem ler ou comparar seu conteúdo.
- `restore VERSION` valida a versão escolhida, guarda antes o arquivo atual —
  mesmo se ele estiver inválido — e a restaura atomicamente.
- Somente as 20 versões gerenciadas mais recentes são mantidas.

## Acceptance Behavior

```text
Given a shelf that was drawn and then edited
When I run `uv run shelf draw`
Then the exact current shelf.yaml is saved in history before the page is replaced
And drawing it again unchanged creates no additional version
```

```text
Given a broken current shelf.yaml and a valid version printed by `history`
When I run `uv run shelf restore VERSION`
Then the broken current bytes are saved first
And the selected version atomically becomes shelf.yaml
And the page is left untouched and reported as needing draw
```

```text
Given an existing edited shelf
When I run `uv run shelf recreate`
Then the estimated cost is shown and the source, page and history do not change until I confirm
And after successful generation the exact current source is saved before replacement
```

```text
Given more than 20 managed snapshots
When a new one is saved
Then only the 20 newest managed versions remain
And unrelated files in history are untouched
```

## Scope

- Exact-byte snapshots under `history/` with collision-safe timestamp names.
- Content marker under `.shelf/` for changed-since-last-draw detection.
- Pure planning logic for naming and retention; filesystem and clock stay in
  the client.
- `recreate`, `history` and `restore VERSION` commands.
- Atomic source replacement, target validation and 20-version retention.
- Paid commands require an interactive confirmation or explicit `--yes`.
- Privacy-safe git ignore and user documentation.

## Out Of Scope

- Diffs, side-by-side comparisons or automatic inspection of a founder's
  version contents.
- Renaming, pinning or keeping selected versions forever.
- Cloud history, synchronization, multi-process locking or server storage.
- Merging a restored version with the current file.
- Adding new photo semantics beyond the full paid `recreate` already decided.

## Validation

Free history/restore validation uses a disposable copy of the one-photo shelf.
The successful paid path uses only that one-photo subset, after a fresh cost
estimate and explicit Navigator confirmation. No full shelf is rerun.
