# Getting started: from clone to your shelf

Turn photos of your bookshelf into an editable shelf and a page with your
books, their authors and a portrait of you as a reader. The paid creation
happens once; drawing the page again is free.

## 1. What you need

- **git**, to clone the repository. On a Mac, `git --version` offers to
  install it if it is missing.
- **uv**, which runs the project and installs Python for you:

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

  Then open a new terminal window.
- **An OpenRouter account with some credit.** A shelf of seven photos costs
  about US$ 0.17; US$ 5 of credit is plenty. You will create the key during
  setup, so you only need to sign up and add credit at
  [openrouter.ai](https://openrouter.ai).

## 2. Clone the repository

```bash
git clone https://github.com/89retreat/89books.git
cd 89books
```

## 3. Photograph your shelf

- One shelf per photo, taken straight on, close enough to read the spines.
- Good light, no flash glare on glossy spines.
- Books lying flat count too, if the title is readable.
- iPhone photos (`.heic`) work as they are; so do `.jpg`, `.png` and `.webp`.

Copy the photos into `my-bookshelf/`. Git ignores everything you put there.
During `create`, resized copies with metadata removed are sent to the model;
the original files remain local.

## 4. Create the editable shelf once

```bash
uv run shelf create
```

The first time, it asks for:

1. your name, as it should appear on the shelf;
2. your OpenRouter key, with instructions to create one. It checks the key
   and shows your credit before reading any photo;
3. a Google Books key, optional, which helps get titles and authors right.
   Press Enter to skip.

Your answers are saved in `my-bookshelf/config.toml`. The command then shows
the estimated cost and time and waits for confirmation. It creates
`my-bookshelf/shelf.yaml`, the source of your shelf. It does not draw the page
yet, and it will never replace an existing `shelf.yaml`.

Already generated a shelf with the older command? If `books.yaml` exists,
`create` reuses its books and covers. It does not recognize the photos or call
the catalogues again; it asks for the much smaller cost of writing a new
portrait. The old `books.yaml` and `shelf.html` are left untouched.

## 5. Draw and open it for free

```bash
uv run shelf draw
uv run shelf open
```

`draw` reads `shelf.yaml` and writes `my-bookshelf/shelf.html` without a key,
network call or cost. If the YAML has an error, the command shows its line and
keeps the previous page.

`open` opens the page in your browser. To share it, send `shelf.html` through
WhatsApp, AirDrop or email. Whoever receives it should open it in a browser:
previews inside apps may show it incomplete.

After editing `shelf.yaml`, run `uv run shelf draw` again. Drawing takes
seconds and does not call the model.

## Commands

| Command | What it does | Cost or network | Files changed |
| --- | --- | --- | --- |
| `uv run shelf` | Shows the selected folder, photos, books, edit/draw times, versions and next safe command. | None. | None. |
| `uv run shelf create` | Reads the photos and creates `shelf.yaml` once. A CV1 shelf reuses its saved catalogue and pays only for a new portrait. | Paid and confirmed before the model call. | Creates `shelf.yaml` and local caches; never replaces an existing source. |
| `uv run shelf check` | Validates `shelf.yaml` and lists every problem with its line and path. | None; no key or network. | None. |
| `uv run shelf draw` | Draws `shelf.html` from the current `shelf.yaml`. | None; no key or network. | Creates or atomically replaces `shelf.html`. |
| `uv run shelf open` | Opens the generated page in the default browser. | None. | None. |
| `uv run shelf setup` | Saves your name and keys and checks whether the keys work. | Free key-check requests; no model call. | May change the local `config.toml`. |
| `uv run shelf --help` | Shows the available commands and options. | None. | None. |

### Folder and confirmation options

| Option | Meaning |
| --- | --- |
| `--folder PATH` | Uses that shelf folder explicitly. It always wins over automatic selection. |
| no `--folder` | Uses the current directory when it already looks like a shelf; otherwise uses `my-bookshelf/`. |
| `create --yes` | Skips a cost confirmation you have already decided, but creation remains paid. |

For example:

```bash
uv run shelf draw --folder path/to/my-shelf
```

### What `--project` means

`--project` is an option of `uv`, not of 89 Books. You normally do not need it.
It is useful only when running the development copy from outside the repository:

```bash
uv run --project /path/to/89books shelf
```

This means “run `shelf` using the Python environment from `/path/to/89books`.”
A packaged installation should let people run `shelf` without knowing about
`uv` or `--project`.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `That key did not work` | Copy the key again from [openrouter.ai/keys](https://openrouter.ai/keys), whole, and paste it. |
| `Credit left` is low, or creation stops with a payment error | Add credit at [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits). |
| `No photos in my-bookshelf` | Copy the photos into `my-bookshelf/` at the root of the repository. |
| `shelf.yaml already exists` | This is protection, not an error in your shelf. Run `draw`; `create` never replaces your edits. |
| An error names a line in `shelf.yaml` | Correct that line and run `draw` again. The previous page was preserved. |
| `command not found: uv` | Open a new terminal window after installing uv. |
| You want another name or key | Run `uv run shelf setup`. |
