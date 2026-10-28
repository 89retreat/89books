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

Everything in this folder is ignored by git except this README: photos,
`config.toml`, `shelf.yaml`, `shelf.html`, a legacy `books.yaml` and the
`.shelf/` cache.
