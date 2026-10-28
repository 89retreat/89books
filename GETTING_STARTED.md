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

```bash
uv run shelf                 # show status and the next safe command; never spends
uv run shelf create          # create shelf.yaml once; paid and confirmed
uv run shelf check           # list every shelf.yaml problem with its line; free
uv run shelf draw            # redraw shelf.html; free
uv run shelf open            # open shelf.html; free
uv run shelf setup           # change your name or keys; free
```

Without `--folder`, the command uses the current directory when it already
contains shelf photos or files; otherwise it uses `my-bookshelf/`. Use an
explicit folder whenever you want to remove any ambiguity:

```bash
uv run shelf draw --folder path/to/my-shelf
```

`create --yes` skips the cost question when you have already decided to spend.
The status panel and `check` never read a key, access the network or change a
file.

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
