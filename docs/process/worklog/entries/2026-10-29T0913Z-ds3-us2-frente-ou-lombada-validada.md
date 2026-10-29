---
title: DS3.US2 — frente, lombada e automático validados
created: 2026-10-29T12:13:00Z
journey: 89-livros
story: CV2.DS3.US2
---

# DS3.US2 — frente, lombada e automático validados

O Navigator validou a regra de três estados numa estante descartável. O livro
citado sem campo `face` e a capa com `face: true` ficaram de frente;
`face: false` permaneceu lombada; `face: true` com `cover: none` caiu para
lombada segura. A seção “Muitas capas” trouxe as seis capas, em ordem, em
fileiras sem sobreposição.

Depois, o Navigator removeu `face: true` de “Capa forçada”, redesenhou a
página e confirmou seu retorno à lombada automática por ela não estar citada.
Tudo aconteceu com `check`, `draw` e `open`, sem chave, rede, catálogo, modelo
ou custo. A story fecha com 195 testes, lint e formatação verdes.

As novas estantes deixam decisões automáticas ausentes do YAML; `true` e
`false` permanecem escolhas explícitas e a operação pura tri-state prepara uma
interface futura. Próxima opção: **CV2.DS3.US3 — Choose the photo that
represents my shelf**.
