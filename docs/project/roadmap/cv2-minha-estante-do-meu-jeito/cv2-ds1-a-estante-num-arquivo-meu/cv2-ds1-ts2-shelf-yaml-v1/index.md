---
code: CV2.DS1.TS2
level: Technical Story
status: Active
status_reason: puxada em 2026-10-28; plano aguarda aprovação do Navigator
updated: 2026-10-28
related:
  - ../index.md
  - ../../../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md
  - ../../../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md
---

[< Parent](../index.md)

# CV2.DS1.TS2 — shelf.yaml, version 1

**Status:** Active
**Type:** Technical Story

---

## Technical Story

In order to tratar a estante como um arquivo que sobrevive às rodadas,
As o núcleo da estante,
I want um contrato versionado, legível por pessoas e validado num só lugar,
So that o terminal e um servidor leiam a mesma estante sem perder escolhas nem gravar um arquivo inválido.

## Outcome

O formato `shelf.yaml` versão 1 existe como contrato executável. Ele guarda o
nome, a foto de capa, a abertura, as prateleiras na ordem da página e os livros
na ordem de cada prateleira, inclusive escolhas opcionais (`hidden`, `face`,
`cover`) e a proveniência que já existe no `books.yaml`.

Uma única entrada pública recebe texto YAML e devolve dados tipados ou todos os
erros encontrados, cada um com número da linha e caminho. Ela nunca abre nem
grava arquivo. Outra entrada transforma os dados tipados em YAML estável e
legível.

## Acceptance Behavior

```text
Given a valid version 1 shelf.yaml
When the core parses it
Then it returns the name, cover photo, lens, shelves and books in file order
And optional reader choices and recognition provenance survive a dump-and-parse round trip
```

```text
Given a shelf.yaml with a duplicate key, an unknown field and wrong field types
When the core parses it
Then it reports every detectable problem with its line number and field path
And it returns no partial shelf and writes nothing
```

```text
Given a shelf.yaml without version 1
When the core parses it
Then it rejects the file with a version error instead of guessing or migrating it
```

## Scope

- `ShelfFile`, `ShelfSection`, `ShelfBook` e `LeftOutBook` como dados tipados.
- `parse_shelf(text)` como única validação do contrato.
- `dump_shelf(shelf)` como serialização determinística e legível.
- Erros de sintaxe, chaves duplicadas, campos desconhecidos, tipos inválidos,
  campos obrigatórios e versão não suportada, todos com linha e caminho.
- Testes como especificação completa do formato v1.

## Out Of Scope

- Ler ou gravar `my-bookshelf/shelf.yaml`.
- Converter a saída da CV1 ou o `core.Shelf` para o novo formato.
- Fazer `draw` usar o arquivo.
- Conferir se a foto de capa ou uma capa local existe na pasta.
- Migrar uma versão futura.

## Validation

Automática. Como Technical Story, os checks definidos no plano bastam; não há
checkpoint de validação manual.
