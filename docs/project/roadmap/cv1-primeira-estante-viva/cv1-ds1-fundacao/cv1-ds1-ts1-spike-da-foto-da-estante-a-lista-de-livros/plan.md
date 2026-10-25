[< Story](index.md)

# Plan — CV1.DS1.TS1

## Objective

Medir se um pipeline automático transforma prints do Kindle e fotos de
prateleira em uma lista confiável de obras da Open Library, com que custo e
tempo, e com qual modelo. O resultado decide a abordagem da entrada (DS2) e
fecha o registro "reconhecimento de livros".

## Pull

Puxada em 2026-10-25 como primeira story da CV1.DS1. Reconhecer livros é o
maior risco técnico da CV1. A leitura manual das amostras (rascunhos de
gabarito) deu sinal positivo; falta medir o caminho automático, sem um olhar
humano no meio.

## Prepare

- Amostras locais, fora do git (`spikes/reconhecimento/amostras/`):
  - `kindle/`: 3 prints do Kindle do Raphael Albino (33 livros no rascunho).
  - `estante/`: 7 fotos de prateleira e 2 fotos gerais da estante do Lula
    (144 livros no rascunho).
- **Consentimento:** Lula e Raphael autorizaram o uso das imagens e o envio a
  um modelo externo (Navigator, 2026-10-25).
- **Chave:** OpenRouter já configurado no Mirror. Saldo em 2026-10-25:
  R$ 8,43.
- **Modelos escolhidos pelo Navigator:** `anthropic/claude-sonnet-5.5`
  (referência de qualidade) contra `anthropic/claude-haiku-5.5` (candidato de
  custo). `google/gemini-3.7-flash` só se sobrar saldo.
- **Risco de viés:** os rascunhos de gabarito foram feitos pelo Driver com
  Claude Opus 5.5, da mesma família dos modelos medidos. Para os números
  finais, os gabaritos precisam da revisão dos donos.

## Scope

- `spikes/reconhecimento/` com um script Python, rodado com `uv run`, em
  quatro etapas:
  1. **Extrair:** envia cada imagem ao modelo pelo OpenRouter e pede uma lista
     JSON: título, autor, status de leitura (quando o Kindle mostrar),
     confiança e trecho lido. Instrui a ignorar a miniatura do player e os
     selos do Kindle e a não inventar livros ilegíveis.
  2. **Normalizar:** busca cada item na Open Library (`search.json`, por título
     e autor) e liga à obra (*work key*), com capa quando houver.
  3. **Deduplicar:** remove repetições entre imagens da mesma pessoa pela obra
     e, sem obra, por título e autor normalizados.
  4. **Comparar:** cruza com o gabarito e calcula as métricas.
- Gabaritos convertidos dos rascunhos para um formato que o script lê
  (`gabarito.json` na pasta de cada amostra, local).
- Roteamento do OpenRouter restrito a provedores que não guardam dados para
  treino (`provider.data_collection: deny`).
- Leitura da chave: `OPENROUTER_API_KEY` do ambiente ou, se ausente, só essa
  linha de `~/mirror/.env`. Nada de chave no repositório.
- Saídas por rodada em `spikes/reconhecimento/resultados/` (local, fora do
  git): JSON bruto do modelo, lista normalizada, comparação.
- `spikes/reconhecimento/relatorio.md` (versionado) só com números agregados
  e a recomendação, sem títulos de livros das pessoas.
- Testes da lógica que não depende de rede: normalização de títulos,
  deduplicação, casamento com o gabarito e cálculo de métricas.
- Atualizar o registro `2026-10-24T2013Z-reconhecimento-de-livros.md` para
  `Decided` com a abordagem recomendada, depois da aprovação do Navigator.

## Métricas, por tipo de imagem (print do Kindle, foto de prateleira) e por modelo

| Métrica | Definição |
|---|---|
| Cobertura | itens do gabarito encontrados ÷ itens do gabarito |
| Invenções | itens devolvidos sem correspondente no gabarito ÷ itens devolvidos |
| Achados na Open Library | itens com obra encontrada ÷ itens devolvidos |
| Com capa | itens com capa ÷ itens com obra |
| Duplicados removidos | contagem entre imagens da mesma pessoa |
| Custo | US$ por imagem, pelo custo informado pelo OpenRouter |
| Tempo | segundos por imagem, incluindo a Open Library |

Casamento com o gabarito: título normalizado (minúsculas, sem acentos,
pontuação e subtítulo) com similaridade mínima; o autor desempata. Itens
`não identificado` do gabarito ficam fora da cobertura. Itens `incerto`
contam à parte.

## Non-Goals

- Interface de upload, revisão ou estante (DS2, DS3).
- Banco de dados, servidor, código de produção.
- Fotos gerais da estante (07 e 08 do Lula): só como capa, fora da medição.
- Afinidade entre estantes.
- Otimizar o prompt até o limite. No máximo três versões de prompt por
  modelo.
- Decidir interface, acesso e stack (TS2).

## Acceptance Behavior

```text
Given os 3 prints do Raphael e as 7 fotos de prateleira do Lula, com gabaritos locais
When o script roda com Sonnet 5.5 e com Haiku 5.5
Then cada imagem produz uma lista de livros ligados a obras da Open Library, com capa quando houver
And o relatório mostra, por tipo de imagem e por modelo: cobertura, invenções, achados na Open Library, com capa, duplicados removidos, custo e tempo por imagem
And o relatório recomenda um modelo (ou um por tipo de imagem) e a forma da entrada da DS2
And nenhuma imagem, lista de livros ou chave entra no git
```

## Product Principle Preserved

**Não começar vazio.** O spike mede se a entrada consegue entregar uma
estante preenchida a partir do que a pessoa já tem, e quanto de revisão a
pessoa precisará fazer.

## Implementation Approach

1. Estrutura: `spikes/reconhecimento/pyproject.toml` (dependências mínimas:
   `httpx`, `pytest`), `reconhecer.py`, `metricas.py`, `tests/`.
2. Converter os dois rascunhos de gabarito em `gabarito.json`.
3. Escrever os testes da lógica pura e implementá-la (TDD).
4. Implementar extração e normalização; fazer uma rodada curta com uma
   imagem de cada tipo para conferir o formato.
5. Rodar Sonnet 5.5 e Haiku 5.5 sobre todas as imagens.
6. Escrever o relatório e parar para a validação do Navigator.

Orçamento: cerca de US$ 0,35 por par de rodadas. Parar se o gasto total do
spike passar de US$ 3.

## Test Strategy

- Automatizados (`uv run pytest` em `spikes/reconhecimento/`): normalização,
  deduplicação, casamento com o gabarito, métricas. Sem rede.
- Integração manual: uma rodada real por modelo, registrada em
  `resultados/`.

## Validation Route

O Navigator lê `spikes/reconhecimento/relatorio.md` e confere:

- **Observação esperada:** as métricas por tipo de imagem e por modelo, o
  custo total do spike e uma recomendação justificada.
- **Passa se:** os números permitem escolher a abordagem da entrada (por
  exemplo, "Haiku para prints, Sonnet para fotos, com revisão obrigatória") e
  o Navigator aceita a recomendação.
- **Falha se:** faltam métricas, o custo não foi medido ou a recomendação não
  decorre dos números.

E2E: não se aplica a um spike sem produto. A validação é o relatório.

## Implementation Contract

- Usar `uv run` para o script e os testes.
- Commit por turno, só com arquivos do spike e da story. Nunca as amostras,
  os resultados brutos ou a chave.
- Mensagens de commit em inglês, explicando o porquê.
- Push só sob comando do Navigator.

## Stop Conditions

- Gasto do spike acima de US$ 3.
- O OpenRouter não aceitar a restrição de retenção de dados para os modelos
  escolhidos.
- Resultado que exija mudar o escopo da DS2 ou da CV1.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Alisson Vale (Navigator)
- Approved on: 2026-10-25
