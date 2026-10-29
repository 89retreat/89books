---
title: DS3.US4 — linguagem autoral validada
created: 2026-10-29T16:02:00Z
journey: 89-livros
story: CV2.DS3.US4
---

# DS3.US4 — linguagem autoral validada

O Navigator validou por captura que a abertura, o título e o texto da
prateleira vêm literalmente de `shelf.yaml`. `voz` e `Cynefin` apareceram em
itálico; os asteriscos do título permaneceram visíveis; `<segura>`, `<autoral>`
e `<script>` apareceram como texto inerte. Torto Arado continuou primeiro e a
citação colocou a capa azul de Cynefin de frente sem reordenar os livros.

O E2E offline completou a evidência: `face: false` venceu a citação, remover a
marca devolveu o automático, e versões descartáveis recuperaram tanto a
linguagem inicial quanto a autoral. O núcleo ganhou operações puras para
reescrever abertura e seção, e renderização e composição passaram a compartilhar
uma gramática estrita de pares simples de asteriscos. A story fecha com 206
testes, Ruff verde e debt review sem ação necessária.

Com US1 a US4 concluídas, CV2.DS3 já entrega organização, frente/lombada, foto
principal e linguagem autoral. A US5 continua condicional: só deve ser puxada
se fundadores pedirem outro retrato por IA. O próximo checkpoint recomendado é
avaliar o fechamento agregado da Delivery Story sem puxá-la por padrão.
