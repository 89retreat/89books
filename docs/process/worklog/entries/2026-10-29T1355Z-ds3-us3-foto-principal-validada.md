---
title: DS3.US3 — foto principal escolhida na fonte
created: 2026-10-29T13:55:00Z
journey: 89-livros
story: CV2.DS3.US3
---

# DS3.US3 — foto principal escolhida na fonte

O Navigator validou que `cover_photo` em `shelf.yaml` escolhe a foto grande que
abre o mosaico, inclusive quando uma configuração legada aponta para outra
imagem. A troca passou pelo fluxo gratuito `check`, `draw` e `open`; as outras
fotos mantiveram sua ordem e a escolhida permaneceu entre as células visíveis
no celular.

A implementação também unificou a resolução de ativos entre `check` e `draw`,
preservou página, marcador e histórico quando a escolha não existe, e manteve
uma escolha válida durante `recreate`. O núcleo ganhou operações puras de
seleção e ordenação para uma interface futura. A story fecha com 201 testes,
Ruff verde, E2E offline e debt review sem ação necessária.

Por pedido do Navigator, a próxima story foi puxada: **CV2.DS3.US4 — Write my
own shelf titles and texts**. Ela entra apenas em Pull/Prepare; implementação
continua bloqueada até plano e aprovação explícita.
