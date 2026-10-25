# Relatório — CV1.DS1.TS1 · Spike de reconhecimento

Data: 2026-10-25 · Prompt `v1` · Gasto total do spike: **US$ 0,25** (teto: US$ 3)

> **Números provisórios.** Os gabaritos foram rascunhados pelo Driver (Claude
> Opus 5.5, da mesma família dos modelos medidos) e ainda não foram revisados
> por Raphael e Lula. Este relatório só traz números agregados; as listas de
> livros ficam locais, fora do git.

## O que foi medido

Pipeline automático: imagem → modelo de visão (OpenRouter, provedores sem
retenção para treino) → busca na Open Library ligando cada livro à obra →
deduplicação entre imagens da mesma pessoa → comparação com o gabarito.

| Amostra | Dono | Imagens | Livros no gabarito |
|---|---|---|---|
| Prints da biblioteca do Kindle (610×1356) | Raphael | 3 | 32 firmes + 1 não identificado |
| Fotos de prateleira, comprimidas pelo WhatsApp (1280×720) | Lula | 7 | 135 firmes + 9 incertos |

As duas fotos gerais da estante do Lula ficaram fora da medição: servem como
capa, não para ler lombadas.

## Resultados

| Amostra | Modelo | Cobertura | Incertos achados | Fora do gabarito | Com obra na OL | Capa (das com obra) | Duplicados removidos | US$/imagem | Modelo s/imagem |
|---|---|---|---|---|---|---|---|---|---|
| Kindle | Sonnet 5.5 | **100%** (32/32) | — | 0% (0/32) | 72% | 83% | 3 | 0,014 | 7 |
| Kindle | Haiku 5.5 | **100%** (32/32) | — | 3% (1/33) | 70% | 83% | 1 | 0,0014 | 11 |
| Estante | Sonnet 5.5 | **88%** (119/135) | 5/9 | 15% (22/146) | 73% | 58% | 7 | 0,027 | 16 |
| Estante | Haiku 5.5 | **60%** (81/135) | 2/9 | 18% (18/101) | 74% | 61% | 3 | 0,0018 | 15 |

Definições: *cobertura* = livros firmes do gabarito encontrados; *fora do
gabarito* = itens devolvidos sem par no gabarito; *com obra na OL* = itens
ligados a uma obra da Open Library; *duplicados* = repetições entre imagens
sobrepostas da mesma pessoa.

O tempo total por imagem foi de 15 a 55 s, mas é dominado pela Open Library
(consultas sequenciais com novas tentativas e um cache que favoreceu a
segunda rodada). Por isso a comparação usa só o tempo do modelo.

## O que os números escondem

**"Fora do gabarito" não é o mesmo que invenção.** O gabarito da estante não é
exaustivo. Inspecionando os 22 itens extras do Sonnet: cerca de metade são
livros reais que o rascunho manual deixou passar; uns cinco são textos de
lombadas de periódicos e catálogos; um é o mesmo livro do gabarito lido de
outra forma; uns três não deu para confirmar. Os extras do Haiku incluem
**erros de leitura de verdade**, entre eles um título com o sentido invertido
e um autor trocado.

**A sobreposição entre imagens ajuda.** No Kindle, um erro de leitura do Haiku
num print foi compensado porque o mesmo livro aparecia inteiro no print
seguinte. A deduplicação removeu exatamente as repetições esperadas.

**A Open Library cobre ~72% dos livros e tem capa para ~60% desses.** Livros
brasileiros e independentes são os que mais faltam. Além disso, o primeiro
resultado com título parecido às vezes é a obra errada; a taxa "com obra" é um
teto, não a precisão.

**A resolução era baixa e mesmo assim funcionou.** As fotos chegaram
comprimidas pelo WhatsApp. Fotos originais devem render mais (hipótese, não
medida).

## Recomendação

1. **Um modelo só na CV1: Claude Sonnet 5.5**, para prints e fotos. Na estante
   ele lê 88% contra 60% do Haiku e erra menos o sentido dos títulos. O custo
   é irrelevante para o dogfood: cerca de US$ 0,02 por imagem, menos de US$ 2
   para o grupo inteiro entrar. Reavaliar o Haiku para prints do Kindle só se
   o volume crescer.
2. **Revisão obrigatória na entrada (CV1.DS2.US2 confirmada).** Mesmo o
   Sonnet deixa de ler uns 12% das lombadas legíveis e traz itens que não são
   livros (periódicos, catálogos). A revisão precisa permitir remover,
   corrigir e acrescentar por busca.
3. **Pedir fotos por prateleira, de perto, mais uma foto geral para a capa.**
   A foto geral não serve para reconhecer.
4. **A estante não pode depender de capa da Open Library.** Cerca de 40% dos
   livros não terão capa. A DS3 precisa de um visual próprio para livros sem
   capa, e vale avaliar uma segunda fonte de metadados (por exemplo, Google
   Books) na TS2.
5. **Reconhecimento em segundo plano.** O modelo leva 7 a 16 s por imagem e a
   busca de metadados é lenta; a entrada deve aceitar as fotos e avisar quando
   a estante estiver pronta para revisão.

## Limitações

- Gabaritos ainda não revisados pelos donos; a amostra é de duas pessoas.
- Um único prompt (`v1`); não houve otimização.
- Status de leitura do Kindle (lido, em leitura) foi extraído, mas não medido.

## Como reproduzir

```bash
cd spikes/reconhecimento
uv run pytest
uv run python gabarito.py amostras/kindle/gabarito-rascunho.md
uv run python gabarito.py amostras/estante/gabarito-rascunho.md
uv run python reconhecer.py --modelo anthropic/claude-sonnet-5.5
uv run python reconhecer.py --modelo anthropic/claude-haiku-5.5
uv run python resumir.py
```

As amostras e os resultados ficam em `amostras/` e `resultados/`, fora do git.
