[< Story](index.md)

# Test Guide — CV1.DS2.US3

## Automated Validation

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Os testes rodam sem rede e cobrem a conferência (linhas enviadas ao modelo,
leitura da resposta, correções, duplicatas, itens que não são livros, a
escolha final do título), o Google Books com rede simulada, a chave opcional,
o sobrenome nas lombadas, capas vindas do Google Books, a prateleira final e
o pipeline com uma leitura errada corrigida antes da página.

## E2E Decision

Ponta a ponta automatizado com rede simulada; a geração real é a rota do
Driver e do Navigator.

## Navigator Validation

1. Abra `~/Downloads/estante-lula-us3.html` no Chrome (ou gere de novo com
   `uv run shelf <pasta>`, de preferência com `GOOGLE_BOOKS_API_KEY`).
2. Confira com o Lula os títulos, os autores nas lombadas e a última
   prateleira.

Passa: o Lula reconhece títulos e autores e não se incomoda com a última
prateleira. Falha: um livro certo virou errado, livros sumiram sem motivo, ou
a última prateleira ainda soa como sobra.

## Validation Evidence

2026-10-27, Driver, sem chave do Google Books (etapa pulada com aviso):

- `uv run pytest`: 53 testes passando. `ruff` limpo.
- Geração real com as 7 fotos do Lula: 164 livros reconhecidos, 19 títulos
  corrigidos pela conferência, 2 deixados de fora como duplicatas; 110 com
  obra e 61 com capa na Open Library; 1 capa escaneada descartada. US$ 0,16,
  cerca de 8 minutos (o cache da Open Library foi apagado para trazer os
  autores).
- Livros sem autor: 31 de 164, contra 71 de 152 na estante da US2. O autor
  aparece em 116 das 145 lombadas.
- Exemplos corrigidos: "Carla Akotirene: O Pai Prezada" → *Ó Paí, Prezada*,
  de Carla Akotirene; "Design" → *Domain-Driven Design*, de Eric Evans;
  "Racionais" → *Sobrevivendo no Inferno*; "Contínuo Preto" e "A Vida de Sueli
  Carneiro", lidos separados, viraram um livro só, de Bianca Santana.
- **Não resolvido:** o título ficou "Continuo Preto: A Vida de Sueli
  Carneiro"; o certo é *Continuo preta*. O modelo sabe o título quando
  perguntado diretamente, mas na lista inteira fica preso à leitura da
  lombada. Duas variações do prompt, testadas só na etapa de conferência
  (US$ 0,10), não resolveram e foram descartadas. O Google Books, consultado
  com a leitura errada, é o caminho previsto para esse caso; a validação com a
  chave está pendente.
- Algumas autorias vêm só do conhecimento do modelo e não foram conferidas
  por mim, como *Homens Pretos (Não) Choram* atribuído a Wesley Carvalho.
- Última prateleira: "E mais livros que já me acompanharam" (escolhido pelo
  Navigator em 2026-10-27),
  sem numeral, sem parágrafo, separada por um fio. Colunas equilibradas e
  nenhuma fileira sem tábua. HTML sem chave e sem caminhos locais.
