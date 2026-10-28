# my-bookshelf

Put the photos of your bookshelf here, then run these commands from the root
of the repository:

```bash
uv run shelf create   # once; paid and confirmed
uv run shelf draw     # whenever you edit shelf.yaml; free
uv run shelf open
```

See [GETTING_STARTED.md](../GETTING_STARTED.md) for the full path.

- One shelf per photo, taken straight on, in good light, reads best.
- `.jpg`, `.heic` (iPhone), `.png` and `.webp` all work.
- `create` never replaces an existing `shelf.yaml`.

Everything in this folder is ignored by git except this README: photos,
`config.toml`, `shelf.yaml`, `shelf.html`, a legacy `books.yaml` and the
`.shelf/` cache.
