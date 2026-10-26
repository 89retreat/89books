---
code: CV1.DS2.US1
level: User Story
status: Active
status_reason: puxada pelo Navigator; aguarda o plano
updated: 2026-10-26
related:
  - ../../../../exploration/es-002-a-estante-num-arquivo/artifacts/product-design-proposal.md
  - ../../../../decisions/records/2026-10-26T1332Z-stack-e-hospedagem.md
  - ../../../../decisions/records/2026-10-24T2013Z-reconhecimento-de-livros.md
---

[< Parent](../index.md)

# CV1.DS2.US1 — Gerar minha estante a partir de uma pasta de fotos

**Status:** Active
**Type:** User Story

---

## User Story

As uma pessoa do grupo com fotos da minha estante,
I want to rodar um comando numa pasta de fotos,
So that eu receba a minha estante pronta, com um retrato de si, num arquivo
que posso abrir e mostrar.

## Outcome

`uv run estante <pasta>` lê as fotos e a chave do OpenRouter, reconhece os
livros, liga cada um a uma obra da Open Library e grava ao lado das fotos um
`estante.html` autocontido: as fotos embutidas, os livros reconhecidos e o
retrato (a lente e os temas que se repetem). Grava também o `livros.yaml`
com a lista de livros, base da correção na US3.

## Acceptance Behavior

```text
Given uma pasta com fotos de estante ou prateleira e a chave do OpenRouter configurada
When rodo `uv run estante <pasta>`
Then recebo `estante.html` e `livros.yaml` dentro da pasta
And o HTML abre sozinho no navegador, sem internet além das capas, com as fotos, os livros e o retrato
And o HTML não contém a chave, caminhos locais nem EXIF das fotos
And o comando informa quantos livros reconheceu e quanto custou
```

```text
Given uma pasta sem fotos ou sem chave configurada
When rodo o comando
Then recebo uma mensagem clara do que falta, sem chamar o modelo
```

## Scope

- Projeto Python na raiz do repositório (`uv`, `pytest`, `ruff`), com o
  comando `estante`.
- Reconhecimento e retrato reaproveitando a lógica do spike, reescrita com
  testes.
- Busca na Open Library com cache local.
- HTML autocontido gerado por template, com fotos comprimidas e sem EXIF.
- Apresentação simples e legível; a beleza fica para a US2.

## Out Of Scope

- Visual para livros sem capa e escolha da capa da estante (US2).
- Correção pelo `livros.yaml`, cache do reconhecimento e `--novo-retrato`
  (US3).
- Publicação no GitHub Pages (DS3).

## Validation

Navigator: rodar o comando com fotos reais da própria estante, abrir o
`estante.html` no computador e no celular e reconhecer ali as fotos, os
livros e o retrato.
