---
code: CV2.DS1.US1
level: User Story
status: Validated
status_reason: Navigator validou em 2026-10-28 create, draw, open, edição, proteção contra erro e página no celular
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds1-ts1-a-shelf-core/index.md
  - ../cv2-ds1-ts2-shelf-yaml-v1/index.md
  - ../../../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md
  - ../../../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md
---

[< Parent](../index.md)

# CV2.DS1.US1 — Create once, draw for free

**Status:** Validated
**Type:** User Story

---

## User Story

In order to ajustar minha estante sem pagar de novo,
As uma pessoa que já tem as fotos ou uma estante da CV1,
I want criar o `shelf.yaml` uma vez e redesenhar a página a partir dele,
So that minhas escolhas sobrevivem e eu sei quando uma operação custa.

## Outcome

`uv run shelf create` cria `shelf.yaml` e nunca substitui um existente.
Quando encontra `books.yaml` da CV1, reaproveita os livros e as capas, escreve
somente um novo retrato e não reconhece foto nem consulta catálogo. Sem essa
saída antiga, executa a geração completa já existente.

`uv run shelf draw` lê e valida `shelf.yaml`, redesenha `shelf.html` sem chave,
rede ou chamada paga e mantém a página anterior se houver qualquer erro.
`uv run shelf open` abre a página existente. O comando sem verbo nunca gasta:
até o painel completo da US2, apenas informa o próximo comando seguro.

## Acceptance Behavior

```text
Given photos and no shelf.yaml or books.yaml
When I run `uv run shelf create` and confirm the estimated cost
Then shelf.yaml is created from the existing generation core
And no shelf.html is written until I run `uv run shelf draw`
```

```text
Given a CV1 folder with books.yaml and no shelf.yaml
When I run `uv run shelf create`
Then the saved books and covers become shelf.yaml without recognizing photos or calling catalogues
And only the portrait cost is shown and confirmed
And the old books.yaml is left untouched
```

```text
Given an existing shelf.yaml
When I run `uv run shelf create`
Then the command refuses before setup, confirmation or any paid call
And the file is unchanged
```

```text
Given a valid shelf.yaml and its photos
When I run `uv run shelf draw`
Then shelf.html is replaced from that file without reading a key or making a network call
And `uv run shelf open` opens it in my browser
```

```text
Given an invalid shelf.yaml and a valid shelf.html from an earlier draw
When I run `uv run shelf draw`
Then every validation problem is shown with line and path
And the earlier shelf.html is unchanged
```

## Scope

- Verbos `create`, `draw`, `open` e a mudança do setup existente para
  `shelf setup`; `--folder` é comum e `--yes` pula somente confirmação paga.
- Um estado mínimo, gratuito e sem verbo, que sugere `create`, `draw` ou
  `open`; contagens, datas e versões ficam na US2.
- Criação nova pelo núcleo atual e migração automática do `books.yaml` da CV1.
- Conversão do resultado gerado para `ShelfFile`, com prateleiras e livros na
  ordem da página e capa como URL ou `none`.
- Desenho do HTML a partir de `ShelfFile`, sem serviço externo.
- Escrita atômica de `shelf.yaml` e `shelf.html`.
- Atualização do guia e do README para o vocabulário novo.

## Out Of Scope

- Painel completo e `check` (US2).
- `history`, `restore` e `recreate` (US3).
- Interface orientada para esconder, corrigir, mover ou reescrever partes da
  estante (DS2 e DS3), ainda que o arquivo já seja a fonte.
- Capas locais autocontidas e validação de tamanho de imagem (DS2.US2).
- Acrescentar fotos a uma estante já criada.

## Validation

Automática mais rota real do Navigator sobre uma cópia descartável de uma
estante da CV1. A migração real usa os livros salvos e paga apenas por um novo
retrato; não haverá nova leitura integral de fotos.
