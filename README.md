# Beak CSS 🐦

A **classless-only** fork of [Pico CSS](https://picocss.com) (v2.1.1).

> *pico* (español) → *beak* (english). Same tiny, semantic framework, rebranded.

Pico is [no longer maintained](https://picocss.com) and explicitly invites
forks. Beak takes it forward as a **pure-CSS, classless** project.

- **Classless only** — style plain HTML. No `.class` names to learn.
- **No SASS, no build step, no dependencies** — the CSS you ship is the source.
- **CSS variables** for every color and measure (`--beak-*`).
- **Keeps Pico's colors and themes** — light, dark and auto (system), unchanged.

## Files

```
beakcss/
├── dist/                     # everything you <link> to
│   ├── beak.css              # classless, constrained width (default)
│   ├── beak.min.css          # minified
│   ├── beak.fluid.css        # classless, full width
│   └── beak.fluid.min.css    # minified
├── index.html                # demo / landing (works on GitHub Pages)
├── README.md
├── LICENSE.md                # MIT (Pico + Beak)
├── NOTICE.md                 # fork + trademark notice
└── CHANGELOG.md
```

Use `beak.css` unless you want the content to span the full viewport width,
in which case use `beak.fluid.css`. In production, use the `.min.css` files.

## Usage

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="dist/beak.min.css">
    <title>Hello Beak</title>
  </head>
  <body>
    <header>…</header>
    <main>
      <h1>Hello, Beak</h1>
      <p>Write plain HTML, get a styled page.</p>
    </main>
  </body>
</html>
```

## Themes

Beak ships the same three schemes as Pico: **light**, **dark** and **auto**
(follows the OS via `prefers-color-scheme`).

```html
<!-- auto (default): follows the operating system -->
<html lang="en">

<!-- force light -->
<html lang="en" data-theme="light">

<!-- force dark -->
<html lang="en" data-theme="dark">
```

## Adding Beak to a new project (recommended)

Pick the option that matches how much you care about updates:

| Approach | When to use it | Update flow |
| --- | --- | --- |
| **Copy the file** | You want zero coupling. | Re-copy `beak.min.css`. |
| **Git submodule** | You want to pull updates easily. | `git submodule update --remote` |
| **npm `file:` dep** | Monorepo / JS toolchain. | `npm install` |

**1. Copy (simplest, recommended for a single static site).**
Drop `beak.min.css` into `vendor/beak/` and pin the version in the filename:

```html
<link rel="stylesheet" href="vendor/beak/beak.min.css">
```

**2. Git submodule (keeps a link to this repo).**

```sh
git submodule add <this-repo-url> vendor/beak
git commit -m "Add Beak CSS as a submodule"
```

Then link `vendor/beak/dist/beak.min.css`.

**3. npm (for JS projects / monorepos).**

```sh
npm install <path-to-this-repo-or-package>
# or, while local: npm install file:../beakcss
```

```js
import "beakcss"; // → dist/beak.min.css
```

### Best practices

- **Pin a version.** Reference a tag/commit (or a versioned filename) so an
  update is always an explicit, reviewable change.
- **Load Beak first, your theme second.** Never edit files in `dist/`; put every
  customization in your own stylesheet loaded *after* Beak.
- **Cascade layers (optional).** To make your app styles beat Beak without
  specificity wars, wrap the import in a layer:

  ```css
  @layer beak, app;
  @import url("dist/beak.min.css") layer(beak);
  /* your app CSS then always wins */
  ```

- **Keep it minified in production**, keep colors/measures overridable via
  variables (see below). Avoid hardcoding hex values in your app.
- **Ship the license.** Keep `LICENSE.md` and `NOTICE.md` next to the CSS.

## Customizing

Everything is a CSS variable, so you can retheme without touching Beak.
Override the variables in your own stylesheet, loaded **after** `beak.css`.

### Colors

Each theme defines its own palette. To override for both themes, target
`:root`; to target one theme, use the `data-theme` selector.

```css
/* brand color for every theme */
:root {
  --beak-primary: #7c3aed;
  --beak-primary-background: #7c3aed;
  --beak-primary-hover: #6d28d9;
  --beak-primary-hover-background: #6d28d9;
  --beak-primary-focus: rgba(124, 58, 237, 0.5);
  --beak-primary-inverse: #fff;
}

/* only in dark mode */
[data-theme="dark"] {
  --beak-background-color: #0b0b0f;
  --beak-color: #e7e9ee;
}
```

Main color variables:

| Variable | Purpose |
| --- | --- |
| `--beak-primary`, `--beak-primary-background`, `--beak-primary-border` | Accent / interactive elements |
| `--beak-primary-hover`, `--beak-primary-focus`, `--beak-primary-inverse` | Accent states |
| `--beak-secondary-*` | Secondary buttons/roles |
| `--beak-contrast-*` | High-contrast variant |
| `--beak-background-color`, `--beak-color` | Page background and text |
| `--beak-muted-color`, `--beak-muted-border-color` | Muted text and borders |
| `--beak-h1-color` … `--beak-h6-color` | Heading colors |
| `--beak-form-element-*` | Inputs, selects, textareas |
| `--beak-mark-*`, `--beak-ins-color`, `--beak-del-color`, `--beak-code-*` | Inline elements |

### Measures

```css
:root {
  --beak-font-family: "Inter", system-ui, sans-serif;
  --beak-font-size: 100%;
  --beak-line-height: 1.5;
  --beak-spacing: 1rem;
  --beak-border-radius: 0.5rem;
  --beak-border-width: 0.0625rem;
  --beak-outline-width: 0.125rem;
  --beak-transition: 0.2s ease-in-out;
  --beak-typography-spacing-vertical: 1rem;
  --beak-form-element-spacing-vertical: 0.75rem;
  --beak-form-element-spacing-horizontal: 1rem;
}
```

### Available variables

All `--beak-*` variables are declared in the `:root` block at the top of
`dist/beak.css`, and each theme's palette lives in the `[data-theme=…]` blocks
below it. Inspect those blocks to see every knob.

## Credit & license

Beak is a fork of **Pico CSS v2.1.1** by the Pico team (https://picocss.com),
used under the MIT license. Beak keeps Pico's original colors and themes. The
Pico name and logo are not part of the MIT grant — Beak ships its own name and
no Pico brand assets. See `LICENSE.md` and `NOTICE.md`.
