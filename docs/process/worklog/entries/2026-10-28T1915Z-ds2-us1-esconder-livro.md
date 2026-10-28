---
title: DS2.US1 — esconder um livro sem apagá-lo
created: 2026-10-28T19:15:00Z
journey: 89-livros
story: CV2.DS2.US1
---

# DS2.US1 — esconder um livro sem apagá-lo

O Navigator escolheu um livro numa cópia descartável de uma estante real e
adicionou `hidden: true`. `check` mostrou 11 livros totais e 10 visíveis;
`draw` guardou a fonte e desenhou 10 livros; a página aberta confirmou que o
livro desapareceu sem quebrar a estante.

Ao remover a marca e desenhar novamente, o mesmo livro voltou. Não houve chave,
rede ou custo. A story fecha com 163 testes, lint e formatação verdes.

A operação pura hide/show prepara uma futura interface sem criar um comando de
terminal para uma ação que a edição do YAML já exprime claramente. Próxima
story: **CV2.DS2.US2 — Fix titles, authors and covers**.
