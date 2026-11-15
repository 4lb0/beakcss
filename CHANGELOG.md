# Changelog

All notable changes to Beak CSS are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-11-15

### Added

- **24 full-palette themes** in `dist/themes/full/`: Dracula, Nord (dark and
  light), the four Catppuccin flavours, Tokyo Night (night and storm), Gruvbox
  (dark and light), One Dark, Monokai, the three Rosé Pine variants, Solarized
  light/dark, Everforest light/dark, Kanagawa and the three Ayu variants.
  Each file is pinned across `:root`, `prefers-color-scheme: dark` and
  `[data-theme=dark]`, so a dark-only scheme never flips with the OS.
- **7 adaptive palettes** for the families that ship both flavours — `nord-auto`,
  `catppuccin-auto`, `gruvbox-auto`, `rose-pine-auto`, `solarized-auto`,
  `everforest-auto`, `ayu-auto`. These map the light flavour to the light
  blocks and the dark flavour to `prefers-color-scheme: dark` and
  `[data-theme=dark]`, so they keep honouring the system preference and a
  theme toggle.
- `tools/themes.py`, a zero-dependency generator for those palettes. It derives
  hover, focus, surfaces, headings and shadows from each scheme's core colors,
  and keeps body text and links at WCAG AA against its own background.
- `llms.txt`, a compact generated index for LLMs, kept in sync with the theme
  table.
- Theme picker and a "Themes" usage section in the demo page.

### Changed

- README documents tints vs. full palettes, load order, and the new files.

## [0.2.0] - 2026-10-12

### Changed

- **Full-width (fluid) is now the default** build; the constrained reading
  width moved to `beak.contained.css`.
- All builds are now wrapped in `@layer beak` for predictable cascading.

### Added

- Color palettes as tiny, composable override files in `dist/themes/`
  (19 colors), instead of duplicating the whole framework per color.
- `tools/build.py`, a zero-dependency generator (no SASS) that rebuilds
  `dist/` from a Pico v2.1.1 checkout and verifies each palette.

## [0.1.0] - 2026-10-12

### Added

- Initial fork of **Pico CSS v2.1.1**.
- Classless-only builds: `beak.css`, `beak.min.css` (constrained width) and
  `beak.fluid.css`, `beak.fluid.min.css` (full width).
- All `--pico-*` CSS variables renamed to `--beak-*`.
- Kept Pico's original colors and themes (light, dark, auto/system).
- Pure CSS: no SASS, no build step, no dependencies.
- Demo page (`index.html`), README, MIT license and attribution notice.

[0.1.0]: https://github.com/USER/beakcss/releases/tag/v0.1.0
