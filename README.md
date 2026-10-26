# 89books

Um produto para leitores ávidos, nascido da frustração de um grupo de amigos
com o Goodreads. O ponto de partida é a estante: visitar a estante de alguém
é uma forma de encontrá-lo.

O primeiro experimento é a
[CV1 A Primeira Estante Viva](docs/project/roadmap/cv1-primeira-estante-viva/index.md):
um comando que transforma fotos da sua estante numa página com os seus livros
e um retrato de você como leitor.

## Generate your shelf

Requirements: [uv](https://docs.astral.sh/uv/) and an
[OpenRouter](https://openrouter.ai/) API key with some credit. A shelf of
seven photos costs about US$ 0.10.

1. Put photos of your shelf, or of single shelves, in a folder
   (`.jpg`, `.jpeg`, `.png` or `.webp`). Close-ups of each shelf read best.
2. Provide the API key, either as an environment variable:

   ```bash
   export OPENROUTER_API_KEY=sk-or-...
   ```

   or in a `config.toml` inside the photos folder, which can also set your
   name for the page title:

   ```toml
   openrouter_api_key = "sk-or-..."
   name = "Lula"
   ```

3. Run:

   ```bash
   uv sync
   uv run shelf path/to/my-shelf
   ```

The command writes into the same folder:

- `shelf.html`: a self-contained page with your photos, your books and a
  portrait of you as a reader. Open it in a browser or send the file to
  anyone. Book covers load from Open Library when online.
- `books.yaml`: the list of recognized books.
- `.shelf/`: a local cache of Open Library lookups.

Photos are resized and stripped of metadata (EXIF) before they are sent to
the model or embedded in the page. The page never contains your API key or
local paths. The model is called through OpenRouter only on providers that do
not keep data for training.

Run `uv run shelf --help` for options.

## Por onde começar

- [Briefing](docs/project/briefing.md): o que é o projeto e onde está.
- [Princípios de produto](docs/product/principles.md).
- [Canvas](canvas.md): visão rápida do roadmap, das decisões em aberto e das
  próximas opções.

## Como trabalhamos

O projeto segue o método [Ariad](https://github.com/mirror-mind-ai/ariad).
Use qualquer agente de código: ele deve ler o [AGENTS.md](AGENTS.md) (o
`CLAUDE.md` aponta para ele). As regras locais estão no
[guia de desenvolvimento](docs/process/development-guide.md).
