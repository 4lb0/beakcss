# Changelog

All notable changes to Beak CSS are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
