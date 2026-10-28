[< Story](index.md)

# Plan — CV2.DS1.TS2 shelf.yaml, version 1

## Pull

Puxada em 2026-10-28 depois de fechar a TS1. O núcleo já separa gerar e
desenhar do terminal; agora as User Stories `create` e `draw` precisam de um
contrato comum, versionado e seguro para a estante que fica entre as duas
operações.

## Prepare

- A decisão de produto já fixa a forma humana do arquivo: `version: 1`,
  `name`, `cover_photo`, `lens`, `shelves`; cada prateleira tem `title`,
  `text`, `books`; cada livro tem `title`, `authors` e escolhas opcionais
  `hidden`, `face`, `cover`.
- `cover` será texto: caminho de imagem na pasta, URL, ou `none`. Um ID da
  Open Library vira URL na conversão que a US1 fará.
- Para não perder o que a CV1 já sabe, o livro também aceita `known_as`,
  `read_as`, `source`, `photo` e `work`; `left_out` preserva título e motivo
  dos itens excluídos pela revisão.
- Ausência de `face` significa escolha automática; `face: false` força
  lombada e `face: true` força capa. Ausência de `hidden` significa visível.
- O núcleo recebe texto e devolve dados; abrir o caminho e decidir a pasta
  pertencem ao cliente. Assim, uma validação nunca pode sobrescrever nada.
- PyYAML carrega dados, mas perde a linha dos campos e aceita chaves duplicadas
  silenciosamente. A validação precisa percorrer os nós de `yaml.compose`
  antes de converter para os dados tipados.

## Scope

- **`src/shelf/shelf_file.py`**:
  - dataclasses `ShelfFile`, `ShelfSection`, `ShelfBook`, `LeftOutBook`;
  - `ShelfYamlIssue(line, path, message)` e `ShelfYamlError(issues)`;
  - `parse_shelf(text: str) -> ShelfFile`, a única validação pública;
  - `dump_shelf(shelf: ShelfFile) -> str`, sem I/O, com chaves em ordem humana
    e blocos `|` para `lens` e textos de mais de uma linha.
- **Contrato v1 estrito**:
  - raiz: `version` (obrigatório e igual a `1`), `name` (opcional),
    `cover_photo` (texto obrigatório), `lens` (texto obrigatório), `shelves`
    (lista obrigatória), `left_out` (lista opcional);
  - prateleira: `title` (texto não vazio), `text` (texto opcional, inclusive
    vazio), `books` (lista obrigatória);
  - livro: `title` (texto não vazio), `authors` (lista opcional de textos não
    vazios), `known_as`, `read_as`, `source`, `photo`, `work` (textos
    opcionais), `hidden` e `face` (booleanos opcionais), `cover` (texto
    opcional);
  - deixado de fora: `title` e `reason` (textos obrigatórios).
- Campos desconhecidos e chaves repetidas são erros: isso faz um erro de
  digitação como `fcae` aparecer em vez de ser ignorado.
- Erros sem um valor próprio (por exemplo, campo obrigatório ausente) apontam
  para a linha do mapa que deveria contê-lo.
- Todos os problemas estruturais detectáveis são acumulados numa exceção; não
  há documento parcial.

## Non-Goals

- I/O de arquivo, comando `check`, `create`, `draw`, migração da CV1,
  histórico ou restore.
- Existência de fotos e capas locais, acesso a URLs ou validação de tamanho de
  imagem; essas regras precisam da pasta e chegam nas User Stories.
- IDs estáveis de livros ou operações de edição; mover o bloco YAML já
  expressa a ordem na versão 1.
- Aceitar versões futuras ou migrá-las silenciosamente.

## Implementation Approach

1. Escrever primeiro fixtures e testes do contrato: exemplo da decisão,
   round trip, ordem, opções e proveniência.
2. Escrever testes de falha: sintaxe, versão, chave duplicada, chave
   desconhecida, ausência, tipos e vários erros com linhas diferentes.
3. Implementar um visitante sobre os nós do PyYAML que valida e constrói as
   dataclasses numa passagem lógica; `parse_shelf` é a única porta pública.
4. Implementar o dumper determinístico com um representer local para blocos
   multilinha, sem alterar o comportamento global do PyYAML.
5. Acrescentar teste de arquitetura que impede `Path`, `open`, `write_text`,
   `print`, `input`, ambiente e imports de `cli`/`setup` no módulo.

## Test Strategy

```bash
uv run pytest tests/test_shelf_file.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Os testes são o contrato. Além dos casos válidos, um caso contém, no mesmo
arquivo, campo desconhecido, tipo errado e campo ausente em linhas distintas e
exige os três erros ordenados por linha. Outro prova que uma chave repetida é
recusada na segunda ocorrência. O teste de arquitetura prova que validação e
serialização operam só sobre texto e dados.

## Validation Route

Não requerida. Esta é uma Technical Story sem comportamento visível; as
evidências automatizadas definidas acima são o aceite, conforme a preferência
do Navigator registrada em 2026-10-28.

## Acceptance Behavior

Ver o [índice da story](index.md).

## Product Principle Preserved

**Nada se perde.** O contrato conserva as escolhas da pessoa e a proveniência
da geração; arquivo inválido produz informação para corrigir, nunca uma
reescrita. **A pessoa tem a palavra final:** ausência de uma escolha mantém o
automático, enquanto `false`, `true`, `none` e textos explícitos sobrevivem ao
round trip.

## Stop Conditions

- A forma decidida do `shelf.yaml` precisar mudar.
- A validação com linhas exigir trocar de biblioteca ou adicionar dependência.
- Uma regra depender da pasta, de rede ou da interface.
- Checks obrigatórios falharem sem correção clara.

## Checkpoint

Implementation must not start until the Navigator approves this plan.

- Approved by: Navigator (Alisson)
- Approved on: 2026-10-28
