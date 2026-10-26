# Product Design Proposal: A Estante num Arquivo

> Reescrito pelo Driver na promoção (2026-10-26). O documento gerado pelo
> Explorer Mode trazia só o resumo e um modelo genérico.

## Product Intent

Dar a cada pessoa do grupo, em troca de uma pasta de fotos e um comando, uma
estante bonita num arquivo HTML, com um retrato de si em que ela se
reconheça, e que ela queira mostrar.

## User-Facing Behavior

```text
minha-estante/
  config.toml        # chave do OpenRouter (ou variável de ambiente); capa opcional
  foto-01.jpg        # fotos da estante ou das prateleiras, sem distinção
  foto-02.jpg
  ...

$ uv run estante minha-estante/
Reconhecendo 7 fotos... 118 livros.
Buscando na Open Library... 86 com obra, 51 com capa.
Escrevendo o retrato...
Pronto: minha-estante/estante.html  (custo: US$ 0,21)
       minha-estante/livros.yaml   (apague o que não for seu e rode de novo)
```

O `estante.html` abre no navegador e mostra:

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
2. Roda o comando e recebe o HTML e o `livros.yaml`.
3. Abre o HTML. Se algo estiver errado, apaga linhas do `livros.yaml` e roda
   de novo; o reconhecimento vem do cache, e só o retrato e o HTML são
   refeitos.
4. Se não se reconhecer no retrato, roda com `--novo-retrato`.
5. Manda o arquivo a alguém, publica no GitHub Pages com um comando, ou as
   duas coisas.

## Product-Level States

- Pasta sem fotos ou sem chave: mensagem clara do que falta.
- Estante gerada: HTML e `livros.yaml` ao lado das fotos.
- Estante corrigida: `livros.yaml` editado e HTML refeito.
- Estante publicada: link no GitHub Pages (CV1.DS3).

## Acceptance Behavior

- Com as fotos do Lula, o comando gera um HTML que abre no celular e no
  computador, com fotos, livros e retrato.
- Apagar uma linha do `livros.yaml` e rodar de novo leva segundos e não chama
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
- Se o `livros.yaml` basta como forma de correção ou se pede algo mais leve.
