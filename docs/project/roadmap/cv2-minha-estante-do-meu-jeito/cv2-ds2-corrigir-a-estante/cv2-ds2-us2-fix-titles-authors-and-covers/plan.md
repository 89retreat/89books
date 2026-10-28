[< Story](index.md)

# Plan — CV2.DS2.US2 Fix titles, authors and covers

## Pull

Puxada em 2026-10-28 depois de o Navigator esconder e trazer de volta um livro.
A validação da primeira estante de uma foto registrou um livro reconhecido
incorretamente; esta story permite consertar a leitura em vez de reler e pagar
pelas fotos.

## Prepare

### Estado atual

- O contrato v1 já guarda `title`, `authors`, `known_as` e `cover`.
- Título e autores editados já chegam à página; `known_as` só vence o nome
  automático quando tem até 24 caracteres, portanto uma escolha explícita mais
  longa pode ser ignorada silenciosamente.
- `cover: none` já resulta em lombada; URLs já chegam ao `src` da capa.
- Um caminho local hoje chegaria cru ao HTML: não é incorporado, pode quebrar
  ao compartilhar e expõe a estrutura relativa da pasta.
- `check` valida tipos do YAML, mas não existência, confinamento, tamanho ou
  formato de uma capa local.
- `draw` já renderiza antes de substituir a página, então um erro de capa pode
  preservar a página anterior se for detectado nessa fase.

### Decisões da fatia

1. **A edição vence o catálogo:** `title`, `authors` e `known_as` atuais são os
   dados da página; nenhuma fonte externa é consultada no redraw.
2. **`known_as` explícito é literal:** depois de normalizar espaços, o valor
   escolhido pela pessoa aparece na lombada e em “Quem mais mora aqui”, mesmo
   acima do limite usado para encurtamento automático.
3. **Três escolhas de capa:**
   - `cover: https://…` — referência remota, não baixada por check/draw;
   - `cover: none` — lombada, mesmo quando `face: true`;
   - `cover: caminho/relativo.jpg` — arquivo dentro da pasta da estante,
     sanitizado e embutido como data URI.
4. **Segurança local:** caminho absoluto, traversal, symlink para fora,
   esquema não HTTPS, extensão não suportada, arquivo ausente, mais de 5 MiB
   ou mais de 25 megapixels são erros claros.
5. **HTML sem rastros locais:** imagem local vira JPEG sem EXIF, lado máximo
   1000 px; nem caminho nem metadata chegam à página.

## Scope

### Operações puras para futura UI

Adicionar ao núcleo:

- `correct_book_identity(shelf, shelf_index, book_index, *, title, authors,
  known_as) -> ShelfFile`;
- `set_book_cover(shelf, shelf_index, book_index, cover) -> ShelfFile`.

As duas retornam cópias, preservam ordem, `hidden`, `face`, `read_as`, `source`,
`photo` e `work`, e não escolhem pasta nem fazem I/O. Identidade rejeita título
vazio e autores vazios; `known_as=None` remove a escolha. Capa aceita string ou
`None`, mantendo `none` como escolha explícita.

### Cover asset boundary

No cliente local, uma única função compartilhada por `check` e `draw` resolve
capas sem rede:

- `none` e ausência não geram asset;
- HTTPS é aceito como referência sem fetch;
- texto sem esquema é caminho relativo à pasta da estante;
- o caminho resolvido deve permanecer dentro da pasta e não pode escapar por
  symlink;
- extensões aceitas: `.jpg`, `.jpeg`, `.png`, `.webp`, `.heic`, `.heif`;
- limite bruto: 5 MiB; limite decodificado: 25.000.000 pixels;
- a imagem é orientada por EXIF, convertida para RGB, reduzida para no máximo
  1000 px, codificada em JPEG e entregue ao núcleo como data URI.

O núcleo recebe um mapa de assets por posição do livro. Não conhece `Path`, não
abre imagens e pode receber o mesmo mapa de um servidor.

### Rendering

- Estender `core.draw`, `page.render_file` e `shelves_from_file` para receber
  assets já resolvidos.
- Um asset local substitui somente o valor de renderização; o YAML continua com
  o caminho legível escolhido pela pessoa.
- URL HTTPS permanece URL; `none` força `_has_cover=False` e lombada.
- Falha de imagem no navegador continua caindo para a lombada existente.
- `display_name` usa `known_as` explícito integralmente; só encurta quando o
  campo não existe.

### Check and draw behavior

- `check` chama `parse_shelf` e a mesma resolução local usada por `draw`;
  continua sem chave, rede ou escrita.
- Erros citam título e campo, por exemplo:
  `Book "…": cover "…" is outside the shelf folder`.
- `draw` resolve e renderiza tudo antes de snapshot, página ou marcador. Em
  erro, esses três permanecem byte a byte intactos.
- Uma correção válida cria snapshot por ser mudança do YAML e substitui apenas
  a página/marker já existentes.

### Documentation

Documentar exemplos em `GETTING_STARTED.md` e `my-bookshelf/README.md`:

```yaml
- title: Título corrigido
  authors: [Nome completo]
  known_as: Nome da lombada
  cover: minha-capa.jpg   # or https://… or none
```

Explicar limites, ausência de busca automática, URL carregada ao abrir e
redraw gratuito.

## Non-Goals

- Busca de capas, autocomplete ou chamada a Open Library/Google Books.
- Download/caching de URL durante check/draw.
- Editor de imagem, crop ou escolha automática da melhor capa.
- Comando terminal `fix` ou seletor por título.
- Alterar prateleira, ordem, `hidden` ou `face`.
- Corrigir automaticamente `read_as`/`source` ou migrar o formato v1.

## Implementation Approach

1. TDD das operações puras de identidade/capa e imutabilidade.
2. Caracterizar título/autores/known_as na página e fazer `known_as` explícito
   vencer sem limite silencioso.
3. TDD do resolvedor de capa: none, HTTPS, local, traversal, symlink, extensão,
   ausente, bytes, pixels, EXIF e erro por livro.
4. Passar mapa de assets pelo núcleo até a página sem filesystem no core.
5. Integrar a mesma validação em `check` e `draw`; provar preservação de página,
   marker e histórico em falha.
6. E2E sintético sem rede para URL/none/local e limites.
7. Atualizar documentação e validar numa cópia descartável com uma correção
   real e uma pequena capa local.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_shelves.py tests/test_page.py tests/test_cli.py tests/test_main.py tests/test_photos.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- título/autores corrigidos aparecem e os antigos não aparecem como livro;
- `known_as` explícito, inclusive longo, vence o encurtamento automático e
  participa de autores frequentes;
- operações puras retornam cópia e preservam provenance/posição/display;
- `cover: none` força lombada; HTTPS chega sem fetch; esquema inseguro falha;
- capa local segura é data URI, redimensionada, sem EXIF e sem caminho no HTML;
- caminho absoluto, traversal, symlink externo, arquivo ausente e extensão
  desconhecida falham;
- limites de 5 MiB e 25 MP são testados sem fixtures gigantes reais;
- check e draw usam a mesma resolução e não tocam chave/rede;
- erro preserva página, marker, histórico e fonte;
- correção válida salva versão e draw continua gratuito;
- arquitetura rejeita `Path`, PIL, ambiente e terminal no núcleo.

## Validation Route

Usar uma cópia descartável da estante de uma foto:

1. Corrigir o livro que a leitura identificou errado: `title`, `authors` e, se
   necessário, `known_as`; rodar `check`, `draw` e `open`.
2. Num livro já de frente, usar `cover: none`; desenhar e observar a lombada.
3. Copiar uma capa pequena preparada para a pasta, definir seu nome em `cover`,
   desenhar e observar a capa voltar.
4. Confirmar no painel/histórico que as mudanças foram guardadas e nada custou.

Fixtures automatizadas cobrem HTTPS, arquivo inseguro e limites. Não há nova
leitura de foto, catálogo ou modelo.

- **Observação esperada:** a página usa exatamente identidade/capa escolhidas;
  local é portátil e seguro; none vira lombada.
- **Passa:** correção visual, snapshot e zero rede/custo; HTML sem caminho/EXIF.
- **Falha:** dado antigo vence, local path vaza, imagem insegura substitui a
  página, ou qualquer catálogo/modelo é chamado.

## Product Principles Preserved

- **A última palavra é de quem lê:** dado editado sempre vence catálogo.
- **Nada se perde:** draw guarda a correção antes de substituir a página.
- **Gastar é escolha:** toda a story é gratuita e offline no redraw.
- **Terminal como protótipo:** operações e assets são reutilizáveis por servidor.

## Risks and Ambiguities

- URL HTTPS torna a página dependente de rede ao abrir; isso é explícito. Uma
  capa local é a opção portátil.
- Nome conhecido muito longo pode exigir CSS futuro; nesta story a escolha não
  é ignorada silenciosamente.
- Limites de 5 MiB/25 MP são proteção inicial. Uso real pode justificar revisão
  sem mudar o formato do YAML.
- Subpastas são aceitas se permanecerem dentro da pasta; symlinks externos não.

## Stop Conditions

- Resolver capa exigir rede durante check/draw.
- Núcleo precisar de filesystem ou PIL.
- A story começar a buscar/corrigir livros automaticamente.
- Precisar mudar o formato v1.
- Validação exigir nova leitura paga das fotos.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: pending
- Approved on: pending
