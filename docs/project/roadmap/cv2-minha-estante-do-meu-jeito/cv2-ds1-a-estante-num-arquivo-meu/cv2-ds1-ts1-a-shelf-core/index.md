---
code: CV2.DS1.TS1
level: Technical Story
status: Done
status_reason: validada pelo Navigator em 2026-10-28; núcleo separado do terminal com 106 testes e rodada real de uma foto
updated: 2026-10-28
related:
  - ../index.md
  - ../../../../decisions/records/2026-10-28T1400Z-terminal-como-cliente-fino.md
---

[< Parent](../index.md)

# CV2.DS1.TS1 — A shelf core a server could run

**Status:** Done
**Type:** Technical Story

---

## Technical Story

In order to fazer do terminal um cliente fino, como decidido em 2026-10-28,
As o código da estante,
I want separar as operações (gerar e desenhar) num núcleo que recebe dados e devolve resultado,
So that o terminal só pergunta, confirma e mostra, e um servidor rode o mesmo núcleo sem mudança.

## Outcome

Um módulo `shelf.core` com duas operações:

- `generate`: das fotos, dos serviços (modelo, catálogos, capas) e das
  configurações, devolve a estante como dados (livros, deixados de fora,
  retrato, nomes das fotos, custo), sem gravar a estante nem imprimir;
- `draw`: da estante como dados e das fotos, devolve o HTML.

O comando `uv run shelf` continua fazendo exatamente o que faz hoje, agora
chamando o núcleo e gravando os arquivos ele mesmo. A revisão do modelo passa
a ter uma só forma de resposta.

## Acceptance Behavior

```text
Given fake services and two photos
When core.generate runs
Then it returns the books, the portrait and the cost
And it writes no shelf file and calls no print, input or getpass
```

```text
Given a shelf as data
When core.draw runs
Then it returns the same HTML the command writes today, without any model or catalogue call
```

```text
Given the photos of a real shelf
When the person runs `uv run shelf`
Then the terminal shows the same steps and writes the same shelf.html and books.yaml as before
```

## Scope

- `shelf.core` com `generate` e `draw`; `Shelf` (dados) e `Services` (o que o
  núcleo chama de fora).
- `cli` fica só com argumentos, configuração, confirmação, mensagens e
  gravação de arquivos.
- A revisão devolve sempre `(entries, cost, names)`; sai o `*rest` do pipeline.
- Um teste de arquitetura: o núcleo não importa `cli`, `setup`, `builtins.input`
  nem `getpass`, e não usa `print`.

## Out Of Scope

- O `shelf.yaml` e os novos comandos (CV2.DS1.TS2 e US1 a US3).
- Mudar o comportamento visível do comando, o layout ou os prompts.

## Validation

Automática, mais uma rodada real com uma foto só.
