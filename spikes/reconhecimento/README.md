# Spike de reconhecimento (CV1.DS1.TS1)

Código descartável que mede se prints do Kindle e fotos de estante viram uma
lista de obras da Open Library. Resultado em [relatorio.md](relatorio.md).
Plano em
[docs/project/roadmap/.../cv1-ds1-ts1-.../plan.md](../../docs/project/roadmap/cv1-primeira-estante-viva/cv1-ds1-fundacao/cv1-ds1-ts1-spike-da-foto-da-estante-a-lista-de-livros/plan.md).

| Arquivo | Papel |
|---|---|
| `reconhecer.py` | Orquestra: extrair → normalizar → deduplicar → comparar |
| `openrouter.py` | Chamada ao modelo de visão e leitura da resposta |
| `openlibrary.py` | Busca da obra na Open Library, com cache |
| `metricas.py` | Deduplicação, casamento com o gabarito, métricas |
| `texto.py` | Normalização e similaridade de títulos |
| `gabarito.py` | Converte o rascunho Markdown em `gabarito.json` |
| `prompts.py` | Versões do prompt |
| `resumir.py` / `recomparar.py` | Tabela da última rodada / recálculo sem chamar o modelo |
| `retrato.py` | Gera o retrato de si a partir dos livros extraídos (experimento da exploração do Telegram); saída local em `resultados/retratos/` |
| `segunda_fonte.py` | Mede o Google Books como segunda fonte (CV1.DS1.TS2); exige `GOOGLE_BOOKS_API_KEY` |

A chave vem de `OPENROUTER_API_KEY` ou, se ausente, só dessa linha em
`~/mirror/.env`. Amostras (`amostras/`) e resultados (`resultados/`) são
pessoais e ficam fora do git.
