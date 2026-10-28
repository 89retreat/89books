---
code: CV2.DS2.US2
level: User Story
status: Done
status_reason: validada e fechada pelo Navigator em 2026-10-28; 185 testes, E2E gratuito e CR001 concluídos
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds2-us1-hide-books-from-my-shelf/index.md
  - ../../cv2-ds1-a-estante-num-arquivo-meu/cv2-ds1-us3-never-lose-an-edit/index.md
---

[< Parent](../index.md)

# CV2.DS2.US2 — Fix titles, authors and covers

**Status:** Done
**Type:** User Story

---

## User Story

In order to a estante dizer os livros como eu os reconheço,
As uma pessoa que vê um título, autor ou capa errados,
I want corrigir esses dados diretamente no `shelf.yaml`,
So that a página mostre a minha estante, sem uma nova leitura paga das fotos.

## Outcome

A pessoa corrige `title`, `authors` e `known_as`, ou escolhe `cover` como imagem
em `covers/`, URL HTTPS ou `none`; `check` valida e `draw` mostra a correção sem
catálogo, chave ou custo. Uma imagem local segura é redimensionada, perde EXIF
e vira parte do HTML sem expor caminho local. Arquivos maiores que 5 MiB ou 25
megapixels são recusados com um aviso claro. A fonte e o histórico preservam a
edição.

## Acceptance Behavior

```text
Given a misread title or author in shelf.yaml
When I correct title, authors and known_as and run check then draw
Then the page uses exactly my corrected reader-facing data
And no catalogue, model, key or network request is used
```

```text
Given a face-out book
When cover is an HTTPS URL, `none`, or a safe image inside the shelf folder
Then draw respectively uses the URL, shows a spine, or embeds a sanitized image
And the HTML contains no local path or EXIF
```

```text
Given a missing, outside-folder, unsupported or oversized local cover
When I run check or draw
Then I get a book-specific clear error
And the previous page and draw marker remain unchanged
```

## Scope

- Correção gratuita de título, autores e nome da lombada.
- `cover` com HTTPS, `none` ou caminho local confinado à subpasta `covers/` da estante.
- Imagem local até 5 MiB e 25 MP, convertida para JPEG com lado máximo 1000.
- Operações puras de correção para uma futura interface.
- Validação compartilhada por `check` e `draw`, preservação atômica e docs.

## Out Of Scope

- Buscar uma nova capa em catálogos ou na web.
- Baixar e incorporar a URL durante `draw`; o navegador a carrega ao abrir.
- Corrigir reconhecimento automaticamente ou reler fotos.
- Mover, esconder ou virar livros de frente.
- Migrar o formato v1 ou comparar históricos reais sem consentimento.

## Validation

Gratuita: corrigir um livro conhecido, testar `cover: none` e uma imagem local
pequena numa cópia descartável. Casos grandes/inseguros usam fixtures sintéticas.
