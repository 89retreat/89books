---
title: US3 — nenhuma edição se perde
created: 2026-10-28T19:05:00Z
journey: 89-livros
story: CV2.DS1.US3
---

# US3 — nenhuma edição se perde

O Navigator validou a recuperação completa numa cópia descartável de uma
estante de uma foto:

- editou a lente e `draw` salvou uma versão exata;
- repetiu `draw` sem edição e não criou duplicata;
- `history` mostrou somente nome, data e tamanho;
- quebrou a fonte de propósito, e `restore` guardou seus 32 bytes antes de
  devolver uma versão válida;
- recusou `recreate` e não houve gasto ou mudança;
- autorizou uma única recriação de uma foto: estimativa de US$ 0,09, custo real
  de US$ 0,03;
- restaurou a estante anterior, desenhou explicitamente e abriu a página
  correta.

A US3 fecha com 157 testes, lint e formatação verdes. As 20 versões gerenciadas
são deliberadamente locais e listadas só por metadados. Histórico em nuvem,
concorrência de servidor e UX de comparação permanecem fora do escopo, não como
dívida criada aqui.

A DS1 tem todas as cinco stories concluídas, mas seu resultado agregado ainda
pede fundadores ajustando a própria estante sem acompanhamento, conforme a
condição de fechamento da DS. A próxima story operacional é
**CV2.DS2.US1 — Hide books from my shelf**.
