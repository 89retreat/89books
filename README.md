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
[OpenRouter](https://openrouter.ai/) account with some credit. A shelf of
seven photos costs about US$ 0.17.

1. Put photos of your shelf, or of single shelves, in `my-bookshelf/` at the
   root of the repository (`.jpg`, `.jpeg`, `.png` or `.webp`). Close-ups of
   each shelf read best. Git ignores this folder.
2. Run:

   ```bash
   uv run shelf
   ```

   The first time, it asks for your name as it should appear on the shelf,
   explains how to get an OpenRouter key and an optional Google Books key,
   checks each key and saves your answers in `my-bookshelf/config.toml`.
   Before reading the photos it tells you the estimated cost and time and
   asks you to confirm.

Options: `uv run shelf --setup` asks for your name and keys again;
`--yes` skips the cost question; `uv run shelf path/to/folder` uses another
folder. Keys can also come from `OPENROUTER_API_KEY` and
`GOOGLE_BOOKS_API_KEY`. In `config.toml`, `cover_photo = "photo-03.jpg"`
chooses the photo that opens the page.

The command writes into the same folder:

- `shelf.html`: a self-contained page that presents your shelf in your own
  voice. It opens with a mosaic of your photos and a sentence about how you
  read the world, then shows your books on drawn shelves, one for each
  situation that takes you to them ("Quando busco…"). Books mentioned in the
  text stand face out with their Open Library covers. Open it in a browser
  (Chrome or Safari); file previews such as Quick Look do not run the
  layout.
- `books.yaml`: the list of books. Before the page is built, the model
  reviews the whole list to fix misread titles and authors and to merge
  books read twice. When a title changed, `read_as` keeps what the photo
  said and `source` says where the title came from; books dropped as
  duplicates or as not being books are listed under `left_out`.
- `.shelf/`: a local cache of catalogue lookups and cover checks.

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
