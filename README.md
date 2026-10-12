# Beak CSS 🐦

A **classless-only** fork of [Pico CSS](https://picocss.com) (v2.1.1).

> *pico* (español) → *beak* (english). Same tiny, semantic framework, rebranded.

Pico is [no longer maintained](https://picocss.com) and explicitly invites
forks. Beak takes it forward as a **pure-CSS, classless** project.

- **Classless only** — style plain HTML. No `.class` names to learn.
- **Full-width (fluid) by default** — no forced max-width on the content.
- **Wrapped in `@layer beak`** — your own CSS always wins, no specificity wars.
- **No SASS, no build step, no dependencies** — the CSS you ship is the source.
- **CSS variables** for every color and measure (`--beak-*`).
- **Keeps Pico's colors and themes** — light, dark and auto (system), plus the
  full Pico color palette (19 optional themes).

## Files

```
beakcss/
├── dist/
│   ├── beak.css              # FULL-WIDTH (default), @layer beak
│   ├── beak.min.css          # minified
│   ├── beak.contained.css    # constrained reading width, @layer beak
│   ├── beak.contained.min.css
│   └── themes/               # tiny palette overrides (load after beak.css)
│       ├── blue.css  amber.css  red.css  …   (19 colors)
├── index.html                # demo / landing (works on GitHub Pages)
├── CNAME                     # beakcss.dev.ar (GitHub Pages custom domain)
├── tools/build.py            # regenerates dist/ from a Pico checkout
├── README.md
├── LICENSE.md                # MIT (Pico + Beak)
├── NOTICE.md                 # fork + trademark notice
└── CHANGELOG.md
```

- Use **`beak.css`** (fluid) for apps, dashboards and full-width layouts.
- Use **`beak.contained.css`** when you want a centered, readable column
  (blog / docs / landing). It's the *only* difference between the two: the
  contained build adds `max-width` breakpoints (510 → 700 → 950 → 1200 → 1450px).
- In production use the `.min.css` files.

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

Three color schemes, same as Pico: **light**, **dark** and **auto** (follows
the OS via `prefers-color-scheme`).

```html
<html lang="en">                 <!-- auto (default) -->
<html lang="en" data-theme="light">
<html lang="en" data-theme="dark">
```

### Color palettes

Beak ships Pico's color palettes as **tiny override files** (about 1.4 KB each)
instead of 19 full copies of the framework. Load your base first, then the
color:

```html
<link rel="stylesheet" href="dist/beak.min.css">
<link rel="stylesheet" href="dist/themes/blue.css">
```

Available colors: `amber blue cyan fuchsia green grey indigo jade lime orange
pink pumpkin purple red sand slate violet yellow zinc`.

Switch palettes at runtime by swapping that second `<link>`'s `href`, or just
override the primary variables yourself (see below).

## Cascade layers

Every Beak file is wrapped in `@layer beak`, so the cascade is predictable:
**layered framework styles lose to unlayered app styles.** You can be explicit
about the order too:

```css
/* in your own stylesheet, loaded before or after beak.css */
@layer beak, app;

/* register your theme under a later layer */
@layer app {
  :root { --beak-primary: #7c3aed; }
}
```

Prefer no layer? Strip the first `@layer beak {` line and the final matching
`}` from a `dist` file.

## Adding Beak to a new project (recommended)

| Approach | When to use it | Update flow |
| --- | --- | --- |
| **Copy the files** | Zero coupling (one static site). | Re-copy `beak.min.css` (+ theme). |
| **Git submodule** | You want to pull updates easily. | `git submodule update --remote` |
| **npm `file:` dep** | Monorepo / JS toolchain. | `npm install` |

**1. Copy (simplest).** Drop `beak.min.css` (and a theme, if any) into
`vendor/beak/` and pin the version in the filename:

```html
<link rel="stylesheet" href="vendor/beak/beak-0.2.0.min.css">
```

**2. Git submodule.**

```sh
git submodule add <this-repo-url> vendor/beak
git commit -m "Add Beak CSS as a submodule"
```

Then link `vendor/beak/dist/beak.min.css`.

**3. npm (JS projects / monorepos).**

```sh
npm install file:../beakcss     # local
# later: npm install beakcss    # once published
```

```js
import "beakcss";                    // dist/beak.min.css
import "beakcss/themes/blue.css";    // optional palette
```

### Best practices

- **Pin a version.** Reference a tag/commit or a versioned filename, so updates
  are explicit and reviewable.
- **Never edit files in `dist/`.** Regenerate with `tools/build.py`, and put all
  customization in your own stylesheet loaded *after* Beak.
- **Load order:** base → theme → your CSS. Colors and measures are variables, so
  prefer overriding `--beak-*` over hardcoding hex values.
- **`@layer` gives you the cascade** for free (see above).
- **Ship the license.** Keep `LICENSE.md` and `NOTICE.md` next to the CSS.

## Customizing

### Colors

Each theme defines its own palette. Override for both themes in `:root`, or per
theme with the `data-theme` selector.

```css
:root {
  --beak-primary: #7c3aed;
  --beak-primary-background: #7c3aed;
  --beak-primary-hover: #6d28d9;
  --beak-primary-hover-background: #6d28d9;
  --beak-primary-focus: rgba(124, 58, 237, 0.5);
  --beak-primary-inverse: #fff;
}

[data-theme="dark"] {
  --beak-background-color: #0b0b0f;
  --beak-color: #e7e9ee;
}
```

Main color variables:

| Variable | Purpose |
| --- | --- |
| `--beak-primary*` | Accent / interactive elements |
| `--beak-secondary*` | Secondary buttons/roles |
| `--beak-contrast*` | High-contrast variant |
| `--beak-background-color`, `--beak-color` | Page background and text |
| `--beak-muted-color`, `--beak-muted-border-color` | Muted text and borders |
| `--beak-h1-color` … `--beak-h6-color` | Heading colors |
| `--beak-form-element-*` | Inputs, selects, textareas |

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
`dist/beak.css`; each theme's palette lives in the `[data-theme=…]` blocks
below it.

## Regenerating `dist/`

No SASS required — just Python 3 and a checkout of Pico v2.1.1:

```sh
git clone https://github.com/picocss/pico /tmp/pico
python3 tools/build.py /tmp/pico/css
```

The script renames `--pico-*` → `--beak-*`, wraps everything in `@layer beak`,
builds the fluid (default) and contained variants, and generates the color
override themes (verified to reconstruct each Pico palette exactly).

## Credit & license

Beak is a fork of **Pico CSS v2.1.1** by the Pico team (https://picocss.com),
used under the MIT license. Beak keeps Pico's original colors and themes. The
Pico name and logo are not part of the MIT grant — Beak ships its own name and
no Pico brand assets. See `LICENSE.md` and `NOTICE.md`.
