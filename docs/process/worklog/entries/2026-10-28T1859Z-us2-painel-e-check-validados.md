---
title: US2 — painel e check validados
created: 2026-10-28T18:59:00Z
journey: 89-livros
story: CV2.DS1.US2
---

# US2 — painel e check validados

O Navigator validou passo a passo os três comportamentos da story:

- o painel gratuito mostrou a pasta, 1 foto, 11 livros, datas de edição e
  desenho, zero versões e `open` como próximo gesto;
- `check` confirmou um `shelf.yaml` válido com 11 livros visíveis em 5
  prateleiras;
- executado a partir da pasta da estante, o comando escolheu essa pasta sem
  `--folder`.

O E2E do Driver também cobriu os estados stale e invalid, preservação da página
anterior, fallback `my-bookshelf/` e ausência de chave, rede paga ou mutação em
painel e check. A suíte fechou com 137 testes e lint/formatação verdes.

A pedido do Navigator, `GETTING_STARTED.md` ganhou uma tabela de todos os
comandos, custos, acessos de rede e arquivos alterados. O guia esclarece que
`--project` é uma opção de desenvolvimento do `uv`, não parte da experiência
do 89 Livros.

O debt review decidiu `no_action`: o núcleo de status continua reutilizável por
um servidor; empacotamento e entrada não terminal permanecem no roadmap e não
são dívida introduzida pela US2.

Próxima candidata: **CV2.DS1.US3 — Never lose an edit**.
