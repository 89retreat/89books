[< Story](index.md)

# Plan — CV2.DS3.US2 Face out or spine, my choice

## Pull

Puxada pelo Navigator em 2026-10-29, logo após o fechamento de CV2.DS3.US1. A ordem já
pertence à pessoa; agora ela decide quais livros chamam atenção pela capa e
quais permanecem como lombada.

## Prepare

### Estado atual

- O contrato v1 já aceita `face: true`, `face: false` ou ausência do campo.
- `shelves_from_file` já usa a escolha explícita quando existe e a regra
  automática quando `face is None`.
- `_book` só materializa uma face quando também existe capa; sem capa, o livro
  vira lombada.
- O JavaScript já troca uma capa remota quebrada por sua lombada e recalcula a
  fileira.
- O layout mede capas como itens mais largos e quebra fileiras conforme o
  espaço disponível.
- O núcleo não oferece uma operação nomeada para escolher frente/lombada.
- A criação atual materializa o resultado automático em todos os livros como
  `face: true` ou `face: false`, congelando uma decisão que deveria continuar
  automática até a pessoa escolher.

### Decisões da fatia

1. **Três estados, sem novo schema:**
   - `true`: pedir capa de frente;
   - `false`: pedir lombada;
   - campo ausente / `None`: regra automática.
2. **Capa é pré-requisito visual:** `cover: none`, ausência de capa ou falha de
   carregamento vence a intenção de frente e cai para lombada segura.
3. **Automático não vira escolha:** novas criações e recriações não escrevem
   `face` derivado pelo algoritmo; o renderer continua calculando-o.
4. **Arquivos existentes não são migrados:** marcas já presentes continuam
   explícitas. A pessoa remove a linha para voltar ao automático.
5. **Ordem continua autoral:** várias faces ocupam mais espaço e mais fileiras,
   mas não reordenam livros.
6. **Sem novo comando:** edição direta, `check`, `draw` e `open` continuam a
   superfície do produto.

## Scope

### Precedence characterization

Provar no renderer de arquivo:

- `face: true` + capa válida gera `.face`, mesmo sem citação no texto;
- `face: false` gera `.spine`, mesmo quando o título é citado;
- ausência usa a regra automática existente;
- automático sem capa gera lombada;
- `face: true` com `cover: none` ou sem capa gera lombada;
- livro oculto continua ausente independentemente de `face`;
- ordem dos itens permanece a ordem da fonte.

### Pure operation

Adicionar:

```python
set_book_face(
    shelf,
    shelf_index,
    book_index,
    face: bool | None,
) -> ShelfFile
```

Contrato:

- retorna cópia sem mutar a fonte;
- `True` e `False` são escolhas explícitas;
- `None` remove a escolha e reativa o automático;
- preserva todos os outros campos e livros;
- índices inválidos levantam `IndexError`;
- valor diferente de bool/None levanta `ValueError`.

### Creation semantics

Na conversão do resultado gerado para `ShelfFile`, não copiar o `face`
derivado por `build_shelves`. A página recém-criada permanece visualmente igual
porque `draw` recalcula a mesma regra a partir de seções/textos/capas, mas o
YAML não confunde algoritmo com decisão da pessoa.

Caracterizar tanto criação nova quanto migração CV1, pois ambas usam o mesmo
arranjo automático e não contêm uma escolha humana de `face`.

### Multiple-face layout

- Renderizar uma fixture com várias capas explícitas e provar que todas chegam
  ao HTML na ordem da fonte.
- Manter o algoritmo JS existente de largura/fileiras e o fallback de imagem.
- Validar visualmente num browser estreito ou prateleira lateral que itens
  quebram em fileiras sem sobreposição.

Não alterar CSS/JS se a caracterização passar.

### Documentation

Documentar em `GETTING_STARTED.md` e `my-bookshelf/README.md`:

```yaml
face: true   # capa de frente, se houver capa
face: false  # lombada
# sem face   # automático
```

Explicar `cover: none`, fallback de URL quebrada, remoção da linha para voltar
ao automático e redraw gratuito.

## Non-Goals

- Campo `face: auto` ou versão nova do YAML.
- Download, busca ou validação remota de capas.
- Escolher crop, tamanho, inclinação ou dimensão da capa.
- Comando CLI para selecionar livro.
- Mover livros ou editar prateleiras/textos/foto principal.
- Reescrever o algoritmo responsivo de fileiras/colunas.

## Implementation Approach

1. Caracterizar os três estados e precedência com capa/hidden no renderer.
2. Escrever testes vermelhos para `set_book_face` e implementar pela operação
   pura de substituição já usada por hide/correction.
3. Escrever teste de criação mostrando que o YAML novo não materializa `face`
   automático; remover essa cópia na conversão.
4. Caracterizar HTML com várias faces e ordem literal; manter JS/CSS se passar.
5. Adicionar E2E gratuito com automático, true, false, none e várias faces.
6. Atualizar docs e parar no checkpoint de validação do Navigator.

## Test Strategy

```bash
uv run pytest tests/test_core.py tests/test_shelves.py tests/test_page.py tests/test_cli.py tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Casos obrigatórios:

- true com capa fica de frente sem depender de citação;
- false fica lombada apesar de citação;
- None segue citação automática;
- true/None sem capa ou com `none` fica lombada;
- hidden nunca reaparece por causa de face;
- operação pura alterna True → False → None e preserva metadata;
- operação rejeita string/número e posições inválidas;
- criação nova e migração não escrevem decisões automáticas em `face`;
- parse/dump continuam preservando true e false explícitos;
- múltiplas faces aparecem no HTML na ordem da fonte;
- fallback JS conserva template de lombada e relayout;
- draw válido cria snapshot e continua sem serviços pagos;
- core continua sem terminal/ambiente.

## Validation Route

Criar `/tmp/89books-ds3-us2-validation` com uma foto e capas locais pequenas:

1. na primeira seção, citar no texto `Livro automático` e `Lombada forçada`;
2. deixar `Livro automático` sem `face` e com capa;
3. pôr `face: true` em `Capa forçada`, não citada;
4. pôr `face: false` em `Lombada forçada`, embora citada;
5. incluir `face: true` + `cover: none` para confirmar fallback;
6. adicionar várias capas `face: true` numa seção lateral/viewport estreito;
7. rodar `check`, `draw`, `open` e observar duas faces iniciais, duas lombadas
   por precedência e quebra segura em fileiras;
8. remover `face: true` de `Capa forçada`, redesenhar e confirmar que volta à
   lombada automática por não ser citada.

- **Observação esperada:** true/false/ausente produzem frente/lombada/automático;
  nenhuma escolha muda ordem ou apaga livro.
- **Passa:** comportamento visual e fallback corretos, fileiras sem sobreposição,
  snapshot e zero chave/rede/custo.
- **Falha:** false é ignorado, ausência fica congelada, livro sem capa some,
  faces sobrepõem/reordenam ou draw chama serviço pago.

## Product Principles Preserved

- **A última palavra é de quem lê:** true/false vencem o algoritmo.
- **Cada leitor revela a própria lógica:** automático só ocupa o silêncio.
- **Nada se perde:** fallback sempre conserva a lombada.
- **Gastar é escolha:** toda a story usa check/draw/open gratuitos.
- **Terminal como protótipo:** operação tri-state serve a controles futuros.

## Risks and Ambiguities

- Uma capa HTTPS pode falhar só no browser; o fallback JS é a garantia possível
  sem transformar draw numa operação de rede.
- `face: true` com `cover: none` expressa intenções incompatíveis; a escolha de
  não ter capa vence e a lombada permanece, como validado na DS2.US2.
- Arquivos já gerados podem conter `face` automático materializado. Não há
  migração silenciosa; remover a linha devolve o automático.
- Muitas capas deixam a página mais alta. Isso é consequência da escolha, não
  motivo para esconder ou reordenar livros.

## Stop Conditions

- A solução exigir migração ou novo valor no schema.
- A story começar a buscar capas ou mexer em `cover`.
- O layout precisar esconder/reordenar faces para caber.
- A criação perder equivalência visual ao deixar `face` ausente.
- A validação exigir rede, catálogo, modelo ou pagamento.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Navigator (Alisson)
- Approved on: 2026-10-29
