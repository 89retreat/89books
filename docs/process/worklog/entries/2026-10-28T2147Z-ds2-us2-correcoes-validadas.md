---
title: DS2.US2 — títulos, autores e capas corrigidos
created: 2026-10-28T21:47:00Z
journey: 89-livros
story: CV2.DS2.US2
---

# DS2.US2 — títulos, autores e capas corrigidos

O Navigator validou a correção gratuita numa estante descartável. Primeiro, a
página mostrou uma capa local incorporada sem caminho ou EXIF. Depois de mudar
para `cover: none`, a mesma entrada virou lombada e mostrou o título corrigido
e todo o `known_as` escolhido, sem chave, catálogo, modelo ou custo.

A validação revelou uma atribuição falsa no rodapé: a página dizia que todas as
capas vinham da Open Library mesmo diante de uma capa local. O CR001 trocou a
frase por “Capas de catálogos ou arquivos locais” e adicionou uma regressão. A
story fecha com 185 testes, lint e formatação verdes.

O núcleo agora expõe operações puras para corrigir identidade e capa. O cliente
local confina arquivos a `covers/`, limita bytes e pixels, remove metadata e
entrega data URIs ao núcleo; `check` e `draw` usam a mesma validação e preservam
a página anterior em erro.

Próxima story puxada pelo Navigator: **CV2.DS3.US1 — Put each book on the shelf
I choose**. Ela foi apenas aberta e preparada; implementação continua bloqueada
até um plano ser aprovado.
