# Product Design Proposal: A Estante num Arquivo

> Reescrito pelo Driver na promoção (2026-10-26). O documento gerado pelo
> Explorer Mode trazia só o resumo e um modelo genérico.

## Product Intent

Dar a cada pessoa do grupo, em troca de uma pasta de fotos e um comando, uma
estante bonita num arquivo HTML, com um retrato de si em que ela se
reconheça, e que ela queira mostrar.

## User-Facing Behavior

```text
my-shelf/
  config.toml        # openrouter_api_key (or the OPENROUTER_API_KEY variable); optional name
  photo-01.jpg       # photos of the whole shelf or of single shelves, no distinction
  photo-02.jpg
  ...

$ uv run shelf my-shelf/
Recognizing books in 7 photos...
Recognized 161 books.
Looking them up on Open Library...
  108 found, 58 with covers.
Writing your portrait...
Done: shelf.html and books.yaml in my-shelf (cost: US$ 0.09)
```

O `shelf.html` abre no navegador e mostra:

- a capa da estante: a primeira foto, ou a indicada em `config.toml`;
- um carrossel com todas as fotos;
- o retrato de si: uma frase sobre a lente do leitor e de três a cinco temas
  que se repetem, cada um com livros da estante;
- os livros como conjunto: capas da Open Library e, para os que não têm,
  lombadas desenhadas com título, autor e uma cor estável por livro.

## What The Product Should Feel Like

Receber um presente, não preencher um cadastro. A estante deve parecer feita
à mão para aquela pessoa. O retrato observa com atenção e generosidade, sem
elogio, julgamento ou frase de horóscopo.

## Interaction Flow

1. A pessoa põe as fotos numa pasta e a chave na configuração.
2. Roda o comando e recebe o HTML e o `books.yaml`.
3. Abre o HTML. Se algo estiver errado, apaga linhas do `books.yaml` e roda
   de novo; o reconhecimento vem do cache, e só o retrato e o HTML são
   refeitos.
4. Se não se reconhecer no retrato, roda com `--new-portrait`.
5. Manda o arquivo a alguém, publica no GitHub Pages com um comando, ou as
   duas coisas.

## Product-Level States

- Pasta sem fotos ou sem chave: mensagem clara do que falta.
- Estante gerada: HTML e `books.yaml` ao lado das fotos.
- Estante corrigida: `books.yaml` editado e HTML refeito.
- Estante publicada: link no GitHub Pages (CV1.DS3).

## Acceptance Behavior

- Com as fotos do Lula, o comando gera um HTML que abre no celular e no
  computador, com fotos, livros e retrato.
- Apagar uma linha do `books.yaml` e rodar de novo leva segundos e não chama
  o modelo de visão.
- Livros sem capa não deixam buracos na estante.
- O HTML não contém a chave, caminhos locais nem EXIF das fotos.

## Explicit Non-Goals

- Bot, servidor, login, banco de dados.
- Editar o texto do retrato (só gerar de novo).
- A IA distinguir estante de prateleira.
- Print do Kindle, seleção manual, movimentos, grupo do Telegram.
- Sinalizar o que a IA não teve certeza.

## Open Product Questions

- Onde publicar no GitHub Pages: repositório da org ou pessoal.
- O comprimento ideal do retrato lido no celular.
- Se o `books.yaml` basta como forma de correção ou se pede algo mais leve.
