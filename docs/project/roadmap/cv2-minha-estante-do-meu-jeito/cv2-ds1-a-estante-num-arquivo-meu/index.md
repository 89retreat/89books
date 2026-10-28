---
code: CV2.DS1
level: Delivery Story
status: Active
status_reason: TS1, TS2 e US1 concluídas; US2 puxada em 2026-10-28
updated: 2026-10-28
related:
  - ../index.md
  - ../../../decisions/records/2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md
  - ../../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md
---

[< CV2](../index.md)

# CV2.DS1 — A estante num arquivo meu

**Status:** Active

---

## Outcome

O `my-bookshelf/shelf.yaml` é a fonte da estante. Gerar a partir das fotos
acontece uma vez e grava tudo nele: livros, retrato, prateleiras e a foto em
destaque. Desenhar a página a partir dele é grátis e leva segundos. A pessoa
sabe sempre em que pé está, vê os erros do arquivo com o número da linha e
nunca perde uma edição: todo comando que reescreve o arquivo guarda uma
versão antes.

Nenhuma edição nova da estante entra nesta DS. Ela prepara o terreno para a
DS2 e a DS3.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV2.DS1.TS1](cv2-ds1-ts1-a-shelf-core/index.md) | A shelf core a server could run | Technical Story | As operações da estante (gerar, desenhar, guardar versão, restaurar) ficam num núcleo que recebe dados e devolve resultado, sem perguntar nem imprimir; o comando só pergunta, confirma e mostra. A revisão passa a ter uma só forma de resposta. | Done |
| [CV2.DS1.TS2](cv2-ds1-ts2-shelf-yaml-v1/index.md) | shelf.yaml, version 1 | Technical Story | O formato do arquivo, com `version: 1`, na ordem em que a página aparece, e uma única validação que aponta cada erro com o número da linha e nunca grava nada; testes servem de contrato do formato. | Done |
| [CV2.DS1.US1](cv2-ds1-us1-create-once-draw-for-free/index.md) | Create once, draw for free | User Story | `create` gera a estante das fotos e grava o `shelf.yaml` (recusa se ele existir); `draw` redesenha o `shelf.html` em segundos, sem chamadas pagas; `open` abre a página. Uma estante da CV1 vira `shelf.yaml` sem novo reconhecimento. | Done |
| [CV2.DS1.US2](cv2-ds1-us2-know-where-my-shelf-stands/index.md) | Know where my shelf stands | User Story | `uv run shelf` sozinho nunca gasta: mostra fotos, livros, quando o arquivo foi editado e desenhado e quantas versões há, e sugere o próximo comando; `check` aponta erros do arquivo com o número da linha. | Active |
| CV2.DS1.US3 | Never lose an edit | User Story | `draw` guarda uma versão em `history/` quando o arquivo mudou; `recreate` guarda uma versão, confirma o custo e refaz das fotos; `history` lista as versões e `restore` devolve uma, guardando antes a atual. Mantém as 20 mais recentes. | Planned |

## Done Condition

O Navigator gera a estante uma vez com `create`, edita o `shelf.yaml` à mão
(por exemplo, apaga um livro ou muda um título), roda `draw` e vê a mudança
em segundos, sem custo. Estraga o arquivo de propósito, vê o erro com a linha,
e volta a uma versão guardada com `restore`.
