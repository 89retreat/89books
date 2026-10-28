---
code: CV2.DS3
level: Delivery Story
status: Active
status_reason: US1 implementada com 191 testes e aguardando validação do Navigator
updated: 2026-10-28
related:
  - ../index.md
  - ../cv2-ds1-a-estante-num-arquivo-meu/index.md
---

[< CV2](../index.md)

# CV2.DS3 — Arrumar a estante

**Status:** Active

---

## Outcome

A pessoa organiza a estante do jeito dela: em que prateleira cada livro fica
e em que ordem, quais ficam de frente, qual foto abre a página e o que dizem
os títulos e textos das prateleiras e a abertura. As regras automáticas da
CV1 (quem fica de frente, quais fileiras recolhem) valem só para o que ela não
decidiu.

Preserva o princípio "cada leitor revela a própria lógica": a organização
autoral, que estava fora da CV1, entra aqui.

## Candidate Stories

| Code | Story | Type | Outcome | Status |
|------|-------|------|---------|--------|
| [CV2.DS3.US1](cv2-ds3-us1-put-each-book-on-the-shelf-i-choose/index.md) | Put each book on the shelf I choose | User Story | Mover as linhas de um livro no arquivo muda a prateleira e a ordem dele na página; posso criar, apagar e reordenar prateleiras. | Active |
| CV2.DS3.US2 | Face out or spine, my choice | User Story | Com `face: true`, o livro fica de frente; sem a marca, mostra a lombada. Uma prateleira com livros demais de frente quebra em mais fileiras. Quem não marcou nada segue a regra automática. | Planned |
| CV2.DS3.US3 | Choose the photo that represents my shelf | User Story | `cover_photo` no `shelf.yaml` escolhe a foto em destaque no mosaico, a que representa a estante; sai do `config.toml`. | Planned |
| CV2.DS3.US4 | Write my own shelf titles and texts | User Story | Reescrevo a abertura (`lens`) e o título e o texto de cada prateleira; a página mostra o que escrevi, com itálico em `*título*` como hoje. | Planned |
| CV2.DS3.US5 | Ask for another portrait | User Story | `portrait` guarda uma versão, confirma o custo (centavos) e reescreve a abertura e as prateleiras a partir dos livros que ficaram, sem ler as fotos. Puxada só se os fundadores sentirem falta depois de editar à mão. Era parte da antiga CV2.DS1.US1. | Planned |

## Done Condition

Um fundador arrumou a própria estante (prateleiras, frente ou lombada, foto,
textos) e a mostrou a alguém como sendo a sua.
