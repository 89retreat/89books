---
code: CV1.DS3.US3
level: User Story
status: Done
status_reason: validada pelo Navigator em 2026-10-27 sobre a estante do Lula; débitos adiados para a CV2.DS1
updated: 2026-10-27
related:
  - ../index.md
  - ../../cv1-ds2-a-estante-num-arquivo/cv1-ds2-us3-livros-certos-na-estante/index.md
---

[< Parent](../index.md)

# CV1.DS3.US3 — Authors by the name readers know

**Status:** Done
**Type:** User Story

---

## User Story

As uma pessoa que mostra a própria estante,
I want que cada lombada traga o autor pelo nome com que os leitores o conhecem,
So that ninguém apareça como um sobrenome solto ("Jesus", "Nascimento", "CARLOS").

## Outcome

Toda lombada traz ao menos nome e sobrenome. A revisão do modelo, na mesma
chamada que já confere a estante, diz como cada autor é conhecido
(*Carolina Maria de Jesus*, *João Ubaldo Ribeiro*, *Abdias Nascimento*).
Quando o modelo não responde por um autor, uma regra local usa o primeiro
nome e o último sobrenome, com partículas e sufixos (*Miguel de Cervantes*,
*Itamar Vieira Junior*), sem títulos e sem caixa alta.

## Acceptance Behavior

```text
Given an author the model knows by a longer name
When the shelf is made
Then the spine shows that name, e.g. "Carolina Maria de Jesus"
```

```text
Given an author the model did not name
When the spine is drawn
Then it shows first name and last surname, never a surname alone
```

```text
Given the shelf of the Lula
When it is re-rendered with the new names
Then none of its spines shows a lone surname, and the names fit the spine
```

## Out Of Scope

- Corrigir à mão o nome de um autor (CV2.DS1.US1).
- Mudar o nome dos autores no `books.yaml`: o nome completo do catálogo continua lá; o nome da lombada fica em `known_as`.
