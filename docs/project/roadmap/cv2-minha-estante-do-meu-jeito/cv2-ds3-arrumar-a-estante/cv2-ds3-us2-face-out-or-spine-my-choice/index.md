---
code: CV2.DS3.US2
level: User Story
status: Done
status_reason: validada e fechada pelo Navigator em 2026-10-29; 195 testes e E2E gratuito aprovados
updated: 2026-10-29
related:
  - ../index.md
  - ../cv2-ds3-us1-put-each-book-on-the-shelf-i-choose/index.md
  - ../../cv2-ds2-corrigir-a-estante/cv2-ds2-us2-fix-titles-authors-and-covers/index.md
---

[< Parent](../index.md)

# CV2.DS3.US2 — Face out or spine, my choice

**Status:** Done
**Type:** User Story

---

## User Story

In order to escolher o que chama atenção quando alguém visita minha estante,
As uma pessoa arrumando os livros,
I want decidir quais aparecem com a capa de frente e quais mostram a lombada,
So that a página respeite meu gesto sem abandonar a composição automática onde eu não escolhi.

## Outcome

`face: true` mostra uma capa disponível de frente; `face: false` força a
lombada; remover `face` devolve a decisão à regra automática baseada no texto
e na seção de fechamento. `cover: none`, capa ausente ou falha no navegador
continua resultando em lombada. Várias capas de frente ocupam novas fileiras
sem sobrepor ou apagar livros.

## Acceptance Behavior

```text
Given books with valid covers
When face is true, false or absent
Then draw respectively shows a face, a spine or the existing automatic choice
And check/draw use no key, catalogue, model or payment
```

```text
Given face true but cover none, absent or broken
When the page is drawn or the browser cannot load the image
Then the book safely falls back to its spine
And no book disappears from the shelf
```

```text
Given several books explicitly face out in one shelf
When the browser lays out the page
Then they wrap into as many rows as needed
And the authored book order is preserved
```

## Scope

- Caracterizar precedência de `face: true`, `face: false` e campo ausente.
- Operação pura para definir ou remover a escolha.
- Novas criações deixam decisões automáticas sem campo `face` no YAML.
- Caracterizar fallback sem capa e layout com várias capas de frente.
- Documentar redraw gratuito e como voltar ao automático.

## Out Of Scope

- Buscar ou corrigir capas; `cover` pertence à DS2.US2.
- Mover livros, trocar foto, reescrever textos ou mudar o schema v1.
- Drag-and-drop, comando terminal ou editor visual.
- Redesenhar dimensões, inclinação ou algoritmo geral de fileiras.

## Validation

Gratuita: numa cópia descartável, observar três livros — automático, capa
forçada e lombada forçada — e uma prateleira com várias capas de frente. Depois
remover uma marca `face` e confirmar que a regra automática volta a decidir.
