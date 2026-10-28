---
code: CV2.DS1.US2
level: User Story
status: Implemented
status_reason: painel, check e resolução de pasta passaram em 137 testes e E2E gratuito; aguarda validação do Navigator
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds1-us1-create-once-draw-for-free/index.md
  - ../cv2-ds1-ts2-shelf-yaml-v1/index.md
  - ../../../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md
---

[< Parent](../index.md)

# CV2.DS1.US2 — Know where my shelf stands

**Status:** Implemented
**Type:** User Story

---

## User Story

In order to não precisar lembrar qual comando vem agora,
As uma pessoa com fotos, um arquivo editável ou uma página já desenhada,
I want ver o estado da minha estante sem gastar e conferir o arquivo antes de desenhar,
So that eu sei o que existe, o que mudou e qual é o próximo gesto seguro.

## Outcome

`uv run shelf` sem verbo mostra um painel gratuito: pasta usada, fotos,
livros, quando `shelf.yaml` foi editado e `shelf.html` desenhado, quantas
versões existem e o próximo comando. Ele distingue ainda não criada, arquivo
inválido, página ausente, página desatualizada e estante pronta.

`uv run shelf check` executa a única validação do contrato e lista todos os
erros com linha e caminho, sem chave, rede ou alteração de arquivo.

Sem `--folder`, o comando usa a pasta atual quando ela já parece uma estante;
caso contrário, preserva `my-bookshelf/` como fallback do clone. `--folder`
sempre vence.

## Acceptance Behavior

```text
Given photos but no shelf.yaml
When I run `uv run shelf`
Then I see the folder, photo count and `create` as the next command
And no setup, key, confirmation or paid service is touched
```

```text
Given a valid shelf.yaml newer than shelf.html
When I run `uv run shelf`
Then I see book count, edit and draw times, version count and that the page is out of date
And the suggested next command is `draw`
```

```text
Given an invalid shelf.yaml with several problems
When I run `uv run shelf check`
Then every problem is printed with line and path
And shelf.yaml and shelf.html remain byte-identical
```

```text
Given I am inside a folder that contains shelf.yaml or shelf photos
When I run `uv run shelf` without --folder
Then that current folder is inspected
But from the repository root the existing my-bookshelf fallback still works
```

## Scope

- Painel gratuito para os estados `not_created`, `invalid`, `not_drawn`,
  `stale` e `ready`.
- Fotos, livros totais e visíveis, horários de edição/desenho e número de
  arquivos em `history/`.
- Próximo comando seguro e explícito para cada estado.
- `check` reutilizando `parse_shelf`, sem outra implementação de validação.
- Resolução de pasta: explícita; pasta atual quando parece uma estante;
  fallback `my-bookshelf/`.
- Atualização de ajuda e guias.

## Out Of Scope

- Criar, desenhar ou abrir automaticamente a partir do painel.
- Gravar versões em `history/`, comparar conteúdo ou restaurar (US3).
- Corrigir erros, abrir editor ou alterar `shelf.yaml`.
- Status remoto, publicação ou múltiplas estantes cadastradas.

## Validation

Automática e manual, usando a área descartável já criada para a US1. Nenhuma
chamada paga é necessária.
