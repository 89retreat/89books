# my-bookshelf

Put the photos of your bookshelf here, then run these commands from the root
of the repository:

```bash
uv run shelf          # status and next safe command; free
uv run shelf create   # once; paid and confirmed
uv run shelf check    # validate shelf.yaml; free
uv run shelf draw     # save a changed source and redraw; free
uv run shelf history  # list saved source versions; free
uv run shelf restore VERSION
uv run shelf recreate # save the source and rebuild from photos; paid and confirmed
uv run shelf open
```

See [GETTING_STARTED.md](../GETTING_STARTED.md) for the full path.

- One shelf per photo, taken straight on, in good light, reads best.
- `.jpg`, `.heic` (iPhone), `.png` and `.webp` all work.
- `create` never replaces an existing `shelf.yaml`.
- `draw` snapshots changed source bytes; `restore` and `recreate` save the current source before replacement.
- At most 20 managed files stay in `history/`, which git ignores.
- Add `hidden: true` to a book and draw to omit it without deleting it; remove the line to show it again.
- Correct `title`, the `authors` list or optional `known_as` directly in `shelf.yaml`; redraw never consults a catalogue.
- Set `cover` to an HTTPS URL, `none`, or `covers/capa.jpg`. Put local book covers in a `covers/` subfolder; they are sanitized and embedded in the page.
- Shelf and book list order is page order. Move the complete YAML book block so authors, cover and provenance travel with it; remove a shelf only after moving its books.
- Use `face: true` for a cover, `face: false` for a spine, or remove `face` to return to the automatic composition. A missing/`none` cover always falls back to a spine.
- Set root-level `cover_photo` to the exact filename of the shelf photo that should open the mosaic. `check` rejects missing names; once `shelf.yaml` exists, it wins over any legacy choice in `config.toml`.
- Rewrite root-level `lens` plus each shelf's `title` and optional `text` in your own words. Single `*asterisks*` add italics only in `lens` and `text`; HTML stays escaped, and cited titles guide only automatic face-out choices.

Everything in this folder is ignored by git except this README: photos,
`config.toml`, `shelf.yaml`, `shelf.html`, a legacy `books.yaml` and the
`.shelf/` cache.
