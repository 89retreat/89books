[< Story](index.md)

# Test Guide — CV1.DS2.US2

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Os testes rodam sem rede e cobrem:

- leitura do retrato: títulos em forma de situação, livros por tema, números
  inválidos ou repetidos descartados;
- módulo `shelves`: temas viram prateleiras, sobras vão para a última,
  livros citados com capa ficam de frente, a primeira prateleira fica na
  coluna principal, cores e inclinações estáveis e variadas, numerais romanos
  e o mosaico para qualquer número de fotos;
- `cover_photo` no `config.toml`, inclusive o erro quando a foto não existe;
- página: escape, prateleiras, capas de frente, fonte embutida e, no teste de
  ponta a ponta, privacidade (sem chave, caminhos locais ou EXIF).

## E2E Decision

Ponta a ponta automatizado com rede simulada. O layout depende do navegador
e é conferido pelo Driver com o navegador automatizado; a execução real custa
dinheiro e usa fotos pessoais.

## Navigator Validation

1. Gere uma estante com `uv run shelf <pasta>` ou abra a estante do Lula
   gerada pelo Driver (`~/Downloads/estante-lula-us2.html`).
2. Abra no Chrome do computador, numa janela larga e numa estreita, e no
   celular.

Observação esperada: mosaico das fotos com ampliação e navegação; nome e
lente em primeira pessoa; prateleiras numeradas com títulos "Quando…",
parágrafo e livros em lombadas sobre tábuas, com os citados de frente; em
tela larga, duas colunas equilibradas que começam pela prateleira I.

Passa: você reconhece o design aprovado nos protótipos, agora gerado pelo
comando.
Falha: prateleira sem livros ou sem título, layout quebrado em alguma
largura, ou texto que não está em primeira pessoa.

## Validation Evidence

2026-10-26, Driver:

- `uv run pytest`: 33 testes passando. `ruff check` e `ruff format --check`
  limpos.
- Execução real com as 7 fotos do Lula: 152 livros, 105 com obra e 60 com
  capa na Open Library, US$ 0,09, cerca de 2 minutos e meio (o cache da Open
  Library ajudou). O retrato veio em primeira pessoa, com seis prateleiras
  "Quando…" e 136 livros distribuídos entre elas; 16 ficaram na última.
- A primeira geração mostrou um problema: com a distribuição generosa, todas
  as prateleiras passaram de oito livros e a coluna lateral ficou vazia. O
  balanceamento passou a mover prateleiras nos dois sentidos, sem tirar a I da
  coluna principal. O ajuste foi conferido aplicando o JavaScript novo ao
  arquivo já gerado, sem uma segunda chamada paga.
- No navegador: 1440 e 1200 px com I, IV, V e VI na principal e II e III na
  lateral; 900 px com I, III, V e VI na principal; 390 px numa coluna, de I a
  VII. Nenhuma fileira sem tábua. Mosaico no celular com cinco fotos e "+2";
  ampliação com navegação ("6 / 7"). As 13 capas de frente carregam.
- `shelf.html` com 1,1 MB, sem a chave, sem caminhos locais e com as 7 fotos
  sem EXIF.
- Na validação, o Navigator apontou duas capas que eram fotos do miolo do
  livro: o sumário de *A urbanização brasileira* e duas páginas abertas, de
  lado, de *Manuscritos econômico-filosóficos*. A geração passou a baixar cada
  capa uma vez (cache em `.shelf/covers.json`) e a descartar imagens mais
  largas que altas ou em cinza exato e quase brancas, que é como o miolo
  escaneado chega. Uma capa descartada vira lombada. Entre as 60 capas do
  Lula, só essas duas são descartadas; a do *Extreme Programming Explained*,
  branca com letras cinza, passa porque guarda um leve tom de cor. 41 testes
  passando. O arquivo de validação recebeu a mesma decisão sem uma nova
  geração paga.
