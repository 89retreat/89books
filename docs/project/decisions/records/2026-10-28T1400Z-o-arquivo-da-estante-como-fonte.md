---
status: Decided
raised: 2026-10-28
decided: 2026-10-28
deciders:
  - Navigator (Alisson)
supersedes:
related:
  - CV2
  - CV2.DS1
  - 2026-10-26T1332Z-stack-e-hospedagem.md
---

# O arquivo da estante como fonte: gerar, desenhar e guardar versões

## Question

Como a pessoa ajusta a estante sem que a próxima rodada apague o que ela fez?
Até a CV1, `uv run shelf` refazia tudo a cada rodada: lia as fotos de novo,
pagava de novo, reescrevia o `books.yaml` e escrevia um retrato novo, que só
existia dentro do `shelf.html`.

## Decision

**O `my-bookshelf/shelf.yaml` é a fonte da estante.** Ele guarda, na ordem em
que a página aparece, o nome, a foto em destaque, a abertura do retrato e as
prateleiras, cada uma com título, texto e livros. Cada livro tem título,
autores e, quando a pessoa quiser, `hidden`, `face` e `cover`. O arquivo tem
`version: 1`.

```yaml
version: 1
name: Lula
cover_photo: estante-lula-foto-03.jpeg
lens: |
  Eu olho o mundo como quem quer entender…
shelves:
  - title: Quando busco pensar o Brasil a partir da negritude
    text: |
      Esta é a prateleira que mais me move…
    books:
      - title: Quarto de Despejo
        authors: [Carolina Maria de Jesus]
        face: true
      - title: O Pai Prezado
        hidden: true
```

**Gerar e desenhar são etapas separadas.** Gerar (pago, minutos) lê as fotos,
consulta os catálogos, escreve o retrato e grava o arquivo. Desenhar (grátis,
segundos) lê o arquivo e escreve o `shelf.html`.

**Um comando por situação, com nomes explícitos:** `uv run shelf` (painel,
nunca gasta), `create`, `draw`, `check`, `recreate`, `history`, `restore`,
`open`, `setup` e, se for puxado, `portrait`. A tabela está na
[CV2](../../roadmap/cv2-minha-estante-do-meu-jeito/index.md#commands).

**Nada se perde.** `recreate`, `restore` e `portrait` guardam uma versão do
arquivo em `my-bookshelf/history/shelf-AAAA-MM-DD-HHMM.yaml` antes de
reescrevê-lo, e dizem onde ela ficou. `draw` guarda uma versão quando o
arquivo mudou desde o último desenho. Ficam as 20 mais recentes.

## Rationale

- Sem uma fonte que sobreviva às rodadas, toda edição se perde.
- Um comando para tudo deixava a pessoa sem saber se ia gastar ou o que ia
  perder. O Navigator pediu nomes explícitos para cada situação.
- `create` e `recreate` separados impedem refazer a estante por engano.
- Cópias com data no nome são recuperáveis sem saber git.

## Options Considered

- **Um único `shelf.yaml`, editado à mão** (escolhida).
- **Manter `books.yaml` e um arquivo à parte para o retrato:** a pessoa
  teria que cruzar dois arquivos para mudar um livro de prateleira.
- **Só aviso antes de refazer, sem versões:** o Navigator pediu backup
  automático e versionado.
- **Um repositório git dentro de `my-bookshelf/`:** compara versões, mas
  obriga a saber git para voltar.
- **Um comando com opções (`shelf --redo`, `shelf --render`):** menos claro
  que um verbo por situação.

## Consequences

- O `books.yaml` deixa de existir como saída separada; o `config.toml` fica
  só com o nome e as chaves, e o `cover_photo` passa para o `shelf.yaml`.
- Mudar o formato do arquivo exige subir a `version` e converter os arquivos
  antigos sem perder edições.
- O arquivo editado à mão quebra fácil: a validação aponta o erro com o número
  da linha e nunca grava nada; `draw` com erro mantém a página anterior.
- `history/` fica dentro de `my-bookshelf/`, que o git ignora.
- Juntar fotos novas a uma estante editada fica fora da CV2; até lá,
  `recreate` com versão guardada.

## Review Trigger

Retrospectiva da CV2, ou a primeira pessoa que perder uma edição.
