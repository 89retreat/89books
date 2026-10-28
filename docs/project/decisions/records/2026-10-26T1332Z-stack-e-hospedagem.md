---
status: Decided
raised: 2026-10-26
decided: 2026-10-26
deciders:
  - Navigator (Alisson), por delegação ao Driver em cadência accelerated; aceite na validação da CV1.DS1.TS2
supersedes:
related:
  - CV1.DS1.TS2
  - CV1.DS2
  - CV4.DS1.TS1
  - ../../exploration/es-002-a-estante-num-arquivo/index.md
---

# Stack, hospedagem e metadados

## Question

Com que tecnologia o MVP da CV1 é construído, quanto custa por estante e de
onde vêm os metadados dos livros? E o que fica registrado para a CV4, que
precisa de servidor?

## Decision

**CV1: um projeto Python na raiz do repositório.**

- Python, gerenciado com `uv`; testes com `pytest`; lint e formatação com
  `ruff`.
- Um comando de linha (por exemplo `uv run shelf <folder>`) lê as fotos de
  uma pasta e um arquivo de configuração com a chave, e grava ao lado das
  fotos um arquivo de livros editável e o `shelf.html`.
- Reconhecimento e retrato com Claude Sonnet 5.5 via OpenRouter, só
  provedores sem retenção para treino
  ([reconhecimento de livros](2026-10-24T2013Z-reconhecimento-de-livros.md)).
- Metadados e capas da Open Library, ligando cada livro à obra.
- Cache local do reconhecimento e das buscas, para que corrigir e gerar de
  novo leve segundos.
- HTML autocontido gerado por template, com CSS e fotos embutidas
  (comprimidas, sem EXIF). Sem framework de frontend nem etapa de build.
- Sem hospedagem. A publicação opcional usa o GitHub Pages
  ([publicação](2026-10-26T1830Z-publicacao-no-github-pages.md)).
- O código do spike (`spikes/reconhecimento/`) é a base, reescrito como
  projeto com testes; o spike continua descartável.

**CV4 (direção, a rever ao planejar):** Django + HTMX servindo o webhook do
bot e as estantes, SQLite e fotos num volume, fila de reconhecimento no
próprio banco, uma máquina no Fly.io em São Paulo e deploy pelo GitHub
Actions. Foi a primeira proposta desta decisão, antes da ES-002.

## Rationale

- O spike já resolveu em Python a chamada ao modelo, a busca na Open Library
  e o casamento de títulos.
- Sem servidor, não há custo fixo, segredo em produção, backup nem
  disponibilidade a cuidar no dogfood.
- Um HTML autocontido funciona igual aberto do disco, mandado como arquivo ou
  servido pelo GitHub Pages.
- Todos os colaboradores rodam Python com `uv` sem esforço.

## Options Considered

- **Script Python local gerando HTML autocontido** (escolhida para a CV1).
- **Gerador de site estático (Astro, Eleventy)**: mais bonito por padrão, mas
  soma uma segunda stack e uma etapa de build ao fluxo de quem roda.
- **Notebook**: ruim de compartilhar e de testar.
- **Django + HTMX no Fly.io**: necessário quando houver bot; guardado para a
  CV4.
- **TypeScript full-stack**: combina com parte dos colaboradores, mas reescreve
  o spike.

## Consequences

- **Custo por estante:** cerca de US$ 0,02 por foto no reconhecimento e uns
  US$ 0,02 por retrato (medidos no spike e no experimento). Uma estante de
  sete fotos custa por volta de US$ 0,20. Cada pessoa usa a própria chave.
- **Custo fixo:** zero na CV1.
- A chave fica num arquivo de configuração local, ignorado pelo git, ou no
  ambiente. Nunca vai para o HTML.
- **Segunda fonte de metadados não medida.** A API anônima do Google Books
  respondeu 429 já na primeira consulta (2026-10-26). O script
  `spikes/reconhecimento/segunda_fonte.py` mede a cobertura com uma chave
  gratuita (`GOOGLE_BOOKS_API_KEY`). Medir antes da CV1.DS2.US2, que cuida dos
  livros sem capa.
- A CV1.DS1.TS3 (esqueleto implantado) foi descartada; a CV4.DS1.TS1 retoma o
  servidor quando chegar a hora.

## Revisão de 2026-10-28

O "arquivo de livros editável" e o cache que deixaria corrigir em segundos
não chegaram a existir na CV1: cada rodada refazia tudo. A
[CV2](../../roadmap/cv2-minha-estante-do-meu-jeito/index.md) os entrega como o
`shelf.yaml`, fonte da estante, conforme
[o arquivo da estante como fonte](2026-10-28T1400Z-o-arquivo-da-estante-como-fonte.md).
O custo medido ao fim da CV1 foi de cerca de US$ 0,17 a 0,18 por estante de
sete fotos, com a revisão e o Google Books incluídos.

## Review Trigger

Início da CV4, ou o HTML autocontido ficando pesado demais para mandar por
mensagem.
