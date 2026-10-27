# Getting started: from clone to your shelf

Turn photos of your bookshelf into a page with your books, their authors
and a portrait of you as a reader. It takes about 15 minutes the first time,
most of it waiting.

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

Copy the photos into the `my-bookshelf/` folder of the repository. Git
ignores everything you put there: your photos never leave your machine.

## 4. Make your shelf

```bash
uv run shelf
```

The first time, it asks for:

1. your name, as it should appear on the shelf;
2. your OpenRouter key, with instructions to create one. It checks the key
   and shows your credit before reading any photo;
3. a Google Books key, optional, which helps get titles and authors right.
   Press Enter to skip.

Your answers are saved in `my-bookshelf/config.toml`. Then it tells you the
estimated cost and time and asks you to confirm. While it works, you will see
each photo being read and the books being checked.

## 5. Open and share it

When it finishes, your shelf is at `my-bookshelf/shelf.html`:

```bash
open my-bookshelf/shelf.html
```

(On Linux, `xdg-open`; on Windows, `start`.) Open it in Chrome or Safari.

To share it, send the file itself through WhatsApp, AirDrop or email. Whoever
receives it should open it in a browser: previews inside apps may show it
incomplete.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `That key did not work` | Copy the key again from [openrouter.ai/keys](https://openrouter.ai/keys), whole, and paste it. |
| `Credit left` is low, or the run stops with a payment error | Add credit at [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits). |
| `No photos in my-bookshelf` | Copy the photos into `my-bookshelf/` at the root of the repository, not into a subfolder. |
| `command not found: uv` | Open a new terminal window after installing uv. |
| Some titles or authors are wrong | Expected now and then: the spines are read by a model. Correcting them is the next step of the project. |
| You want another name or key | `uv run shelf --setup`. |

Running `uv run shelf` again reads all the photos again and costs the same
again.
