#!/usr/bin/env python3
"""
Beak CSS full-palette themes.

The 19 files in `dist/themes/*.css` are Pico *tints*: they only swap the
primary/secondary/contrast ramps and stay light/dark aware. The themes
generated here are *complete palettes* — background, text, muted text,
borders, code, forms, shadows — modelled on popular terminal/editor schemes.

Outputs:
  dist/themes/full/<id>.css   one file per flavour, pinned in the three selector
                              groups (light, system, dark) so a dark-only scheme
                              never flips with the OS, plus one `<family>-auto`
                              file per family that has both flavours, where the
                              light palette fills the light block and the dark
                              palette fills the system + [data-theme=dark] blocks.
  llms.txt                    index for LLMs, kept in sync with the theme list.

Usage:
    python3 tools/themes.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = DIST / "themes" / "full"
VERSION = "0.3.0"

# --- color helpers ----------------------------------------------------------


def rgb(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def hexof(t):
    return "#%02x%02x%02x" % tuple(round(c) for c in t)


def mix(a, b, amount):
    """Linear sRGB mix: amount=0 -> a, amount=1 -> b."""
    ca, cb = rgb(a), rgb(b)
    return hexof(tuple(ca[i] + (cb[i] - ca[i]) * amount for i in range(3)))


def rgba(color, alpha):
    r, g, b = rgb(color)
    return "rgba(%d, %d, %d, %s)" % (r, g, b, fmt_alpha(alpha))


def fmt_alpha(a):
    return ("%.4f" % a).rstrip("0").rstrip(".")


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(color):
    r, g, b = rgb(color)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def ensure_contrast(color, against, minimum, toward, max_shift=0.45, step=0.03):
    """Nudge `color` toward `toward` until it reaches `minimum` contrast."""
    out, shift = color, 0.0
    while contrast(out, against) < minimum and shift < max_shift:
        shift += step
        out = mix(color, toward, shift)
    return out


def best_on(background, candidates):
    """Pick the candidate with the highest contrast against `background`."""
    return max(candidates, key=lambda c: contrast(c, background))


# --- palettes ---------------------------------------------------------------
#
# Every entry is a minimal spec: bg, text, muted text, border, accent and the
# three semantic colors. Everything else (hover, focus, surfaces, headings,
# shadows) is derived so the files stay consistent across all flavours.

THEMES = [
    dict(
        id="dracula",
        name="Dracula",
        family="Dracula",
        mode="dark",
        bg="#282a36",
        text="#f8f8f2",
        muted="#6272a4",
        border="#44475a",
        primary="#bd93f9",
        success="#50fa7b",
        danger="#ff5555",
        warning="#f1fa8c",
        credit="Dracula Theme · MIT · https://draculatheme.com",
    ),
    dict(
        id="nord",
        name="Nord",
        family="Nord",
        mode="dark",
        bg="#2e3440",
        text="#d8dee9",
        muted="#81a1c1",
        border="#3b4252",
        primary="#88c0d0",
        success="#a3be8c",
        danger="#bf616a",
        warning="#ebcb8b",
        credit="Nord · MIT · https://www.nordtheme.com",
    ),
    dict(
        id="nord-light",
        name="Nord Light",
        family="Nord",
        mode="light",
        bg="#eceff4",
        text="#2e3440",
        muted="#4c566a",
        border="#d8dee9",
        primary="#5e81ac",
        success="#a3be8c",
        danger="#bf616a",
        warning="#ebcb8b",
        credit="Nord · MIT · https://www.nordtheme.com",
    ),
    dict(
        id="catppuccin-latte",
        name="Catppuccin Latte",
        family="Catppuccin",
        mode="light",
        bg="#eff1f5",
        text="#4c4f69",
        muted="#6c6f85",
        border="#ccd0da",
        primary="#1e66f5",
        success="#40a02b",
        danger="#d20f39",
        warning="#df8e1d",
        credit="Catppuccin · MIT · https://catppuccin.com",
    ),
    dict(
        id="catppuccin-frappe",
        name="Catppuccin Frappé",
        family="Catppuccin",
        mode="dark",
        bg="#303446",
        text="#c6d0f5",
        muted="#838ba7",
        border="#414559",
        primary="#8caaee",
        success="#a6d189",
        danger="#e78284",
        warning="#e5c890",
        credit="Catppuccin · MIT · https://catppuccin.com",
    ),
    dict(
        id="catppuccin-macchiato",
        name="Catppuccin Macchiato",
        family="Catppuccin",
        mode="dark",
        bg="#24273a",
        text="#cad3f5",
        muted="#8087a2",
        border="#363a4f",
        primary="#8aadf4",
        success="#a6da95",
        danger="#ed8796",
        warning="#eed49f",
        credit="Catppuccin · MIT · https://catppuccin.com",
    ),
    dict(
        id="catppuccin-mocha",
        name="Catppuccin Mocha",
        family="Catppuccin",
        mode="dark",
        bg="#1e1e2e",
        text="#cdd6f4",
        muted="#7f849c",
        border="#313244",
        primary="#89b4fa",
        success="#a6e3a1",
        danger="#f38ba8",
        warning="#f9e2af",
        credit="Catppuccin · MIT · https://catppuccin.com",
    ),
    dict(
        id="tokyo-night",
        name="Tokyo Night",
        family="Tokyo Night",
        mode="dark",
        bg="#1a1b26",
        text="#c0caf5",
        muted="#565f89",
        border="#292e42",
        primary="#7aa2f7",
        success="#9ece6a",
        danger="#f7768e",
        warning="#e0af68",
        credit="Tokyo Night · MIT · https://github.com/folke/tokyonight.nvim",
    ),
    dict(
        id="tokyo-night-storm",
        name="Tokyo Night Storm",
        family="Tokyo Night",
        mode="dark",
        bg="#24283b",
        text="#c0caf5",
        muted="#565f89",
        border="#292e42",
        primary="#7aa2f7",
        success="#9ece6a",
        danger="#f7768e",
        warning="#e0af68",
        credit="Tokyo Night · MIT · https://github.com/folke/tokyonight.nvim",
    ),
    dict(
        id="gruvbox-dark",
        name="Gruvbox Dark",
        family="Gruvbox",
        mode="dark",
        bg="#282828",
        text="#ebdbb2",
        muted="#928374",
        border="#3c3836",
        primary="#fe8019",
        success="#b8bb26",
        danger="#fb4934",
        warning="#fabd2f",
        credit="Gruvbox · MIT · https://github.com/morhetz/gruvbox",
    ),
    dict(
        id="gruvbox-light",
        name="Gruvbox Light",
        family="Gruvbox",
        mode="light",
        bg="#fbf1c7",
        text="#3c3836",
        muted="#7c6f64",
        border="#ebdbb2",
        primary="#076678",
        success="#79740e",
        danger="#9d0006",
        warning="#b57614",
        credit="Gruvbox · MIT · https://github.com/morhetz/gruvbox",
    ),
    dict(
        id="one-dark",
        name="One Dark",
        family="One Dark",
        mode="dark",
        bg="#282c34",
        text="#abb2bf",
        muted="#5c6370",
        border="#3e4451",
        primary="#61afef",
        success="#98c379",
        danger="#e06c75",
        warning="#e5c07b",
        credit="One Dark (Atom) · MIT · https://github.com/atom/atom",
    ),
    dict(
        id="monokai",
        name="Monokai",
        family="Monokai",
        mode="dark",
        bg="#272822",
        text="#f8f8f2",
        muted="#75715e",
        border="#3e3d32",
        primary="#66d9ef",
        success="#a6e22e",
        danger="#f92672",
        warning="#e6db74",
        credit="Monokai · MIT · https://monokai.pro",
    ),
    dict(
        id="rose-pine",
        name="Rosé Pine",
        family="Rosé Pine",
        mode="dark",
        bg="#191724",
        text="#e0def4",
        muted="#908caa",
        border="#26233a",
        primary="#c4a7e7",
        success="#9ccfd8",
        danger="#eb6f92",
        warning="#f6c177",
        credit="Rosé Pine · MIT · https://rosepinetheme.com",
    ),
    dict(
        id="rose-pine-moon",
        name="Rosé Pine Moon",
        family="Rosé Pine",
        mode="dark",
        bg="#232136",
        text="#e0def4",
        muted="#908caa",
        border="#393552",
        primary="#c4a7e7",
        success="#9ccfd8",
        danger="#eb6f92",
        warning="#f6c177",
        credit="Rosé Pine · MIT · https://rosepinetheme.com",
    ),
    dict(
        id="rose-pine-dawn",
        name="Rosé Pine Dawn",
        family="Rosé Pine",
        mode="light",
        bg="#faf4ed",
        text="#464261",
        muted="#797593",
        border="#f2e9e1",
        primary="#286983",
        success="#56949f",
        danger="#b4637a",
        warning="#ea9d34",
        credit="Rosé Pine · MIT · https://rosepinetheme.com",
    ),
    dict(
        id="solarized-light",
        name="Solarized Light",
        family="Solarized",
        mode="light",
        bg="#fdf6e3",
        text="#657b83",
        muted="#93a1a1",
        border="#eee8d5",
        primary="#268bd2",
        success="#859900",
        danger="#dc322f",
        warning="#b58900",
        credit="Solarized · MIT · https://ethanschoonover.com/solarized",
    ),
    dict(
        id="solarized-dark",
        name="Solarized Dark",
        family="Solarized",
        mode="dark",
        bg="#002b36",
        text="#839496",
        muted="#586e75",
        border="#073642",
        primary="#268bd2",
        success="#859900",
        danger="#dc322f",
        warning="#b58900",
        credit="Solarized · MIT · https://ethanschoonover.com/solarized",
    ),
    dict(
        id="everforest-dark",
        name="Everforest Dark",
        family="Everforest",
        mode="dark",
        bg="#2d353b",
        text="#d3c6aa",
        muted="#859289",
        border="#3d484d",
        primary="#7fbbb3",
        success="#a7c080",
        danger="#e67e80",
        warning="#dbbc7f",
        credit="Everforest · MIT · https://github.com/sainnhe/everforest",
    ),
    dict(
        id="everforest-light",
        name="Everforest Light",
        family="Everforest",
        mode="light",
        bg="#fdf6e3",
        text="#5c6a72",
        muted="#939f91",
        border="#efebd4",
        primary="#3a94c5",
        success="#8da101",
        danger="#f85552",
        warning="#dfa000",
        credit="Everforest · MIT · https://github.com/sainnhe/everforest",
    ),
    dict(
        id="kanagawa",
        name="Kanagawa",
        family="Kanagawa",
        mode="dark",
        bg="#1f1f28",
        text="#dcd7ba",
        muted="#727169",
        border="#2a2a37",
        primary="#7e9cd8",
        success="#98bb6c",
        danger="#e46876",
        warning="#e6c384",
        credit="Kanagawa · MIT · https://github.com/rebelot/kanagawa.nvim",
    ),
    dict(
        id="ayu-dark",
        name="Ayu Dark",
        family="Ayu",
        mode="dark",
        bg="#0b0e14",
        text="#bfbdb6",
        muted="#565b66",
        border="#1b1f28",
        primary="#59c2ff",
        success="#aad94c",
        danger="#f07178",
        warning="#e6b450",
        credit="Ayu · MIT · https://github.com/ayu-theme",
    ),
    dict(
        id="ayu-mirage",
        name="Ayu Mirage",
        family="Ayu",
        mode="dark",
        bg="#1f2430",
        text="#cbccc6",
        muted="#707a8c",
        border="#2a3140",
        primary="#73d0ff",
        success="#bae67e",
        danger="#f28779",
        warning="#ffd580",
        credit="Ayu · MIT · https://github.com/ayu-theme",
    ),
    dict(
        id="ayu-light",
        name="Ayu Light",
        family="Ayu",
        mode="light",
        bg="#fafafa",
        text="#5c6773",
        muted="#8a9199",
        border="#e7eaed",
        primary="#399ee6",
        success="#86b300",
        danger="#f07171",
        warning="#f2ae49",
        credit="Ayu · MIT · https://github.com/ayu-theme",
    ),
]

ICON = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='{color}' "
    "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E{body}"
    "%3C/svg%3E\")"
)
ICON_VALID = ICON.format(
    color="{color}",
    body="%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E",
)
ICON_INVALID = ICON.format(
    color="{color}",
    body="%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E"
    "%3Cline x1='12' y1='8' x2='12' y2='12'%3E%3C/line%3E"
    "%3Cline x1='12' y1='16' x2='12.01' y2='16'%3E%3C/line%3E",
)

# Families that publish (or that we map to) both a light and a dark flavour get
# an extra adaptive file: the light palette fills the light blocks and the dark
# palette fills `prefers-color-scheme: dark` + `[data-theme=dark]`.
ADAPTIVE = [
    dict(id="nord-auto", name="Nord", light="nord-light", dark="nord"),
    dict(
        id="catppuccin-auto",
        name="Catppuccin",
        light="catppuccin-latte",
        dark="catppuccin-mocha",
    ),
    dict(id="gruvbox-auto", name="Gruvbox", light="gruvbox-light", dark="gruvbox-dark"),
    dict(id="rose-pine-auto", name="Rosé Pine", light="rose-pine-dawn", dark="rose-pine"),
    dict(
        id="solarized-auto",
        name="Solarized",
        light="solarized-light",
        dark="solarized-dark",
    ),
    dict(
        id="everforest-auto",
        name="Everforest",
        light="everforest-light",
        dark="everforest-dark",
    ),
    dict(id="ayu-auto", name="Ayu", light="ayu-light", dark="ayu-dark"),
]

SHADOW_LAYERS = [
    ("0.0145rem 0.029rem 0.174rem", 0.01698),
    ("0.0335rem 0.067rem 0.402rem", 0.024),
    ("0.0625rem 0.125rem 0.75rem", 0.03),
    ("0.1125rem 0.225rem 1.35rem", 0.036),
    ("0.2085rem 0.417rem 2.502rem", 0.04302),
    ("0.5rem 1rem 6rem", 0.06),
    ("0 0 0 0.0625rem", 0.015),
]


def vars_for(t):
    """Return the full ordered list of --beak-* declarations for a theme."""
    dark = t["mode"] == "dark"
    border = t["border"]
    away = "#ffffff" if dark else "#000000"

    bg = t["bg"]
    text = ensure_contrast(t["text"], bg, 4.5, away)
    muted = ensure_contrast(t["muted"], bg, 3.5, away)
    primary = ensure_contrast(t["primary"], bg, 4.5, away)
    success = ensure_contrast(t["success"], bg, 4.0, away)
    danger = ensure_contrast(t["danger"], bg, 4.0, away)
    warning = t["warning"]  # paints mark backgrounds
    warning_text = ensure_contrast(t["warning"], bg, 4.5, away)  # readable as text

    on_primary = max([bg, "#ffffff"], key=lambda c: contrast(c, primary))

    # neutral ramp
    secondary_text = mix(muted, text, 0.5)
    secondary_bg = mix(bg, text, 0.18 if dark else 0.1)
    on_secondary = best_on(secondary_bg, [text, bg])
    code_bg = mix(bg, text, 0.06)
    form_bg = mix(bg, text, 0.04)
    selected_bg = mix(bg, text, 0.12)

    primary_hover = mix(primary, away, 0.22)
    primary_hover_bg = mix(primary, away, 0.16)
    contrast_color = ensure_contrast(text, bg, 9, away)
    contrast_hover = mix(contrast_color, away, 0.2)

    shadow = ", ".join(
        "%s rgba(0, 0, 0, %s)" % (geom, fmt_alpha(alpha * (2.5 if dark else 1)))
        for geom, alpha in SHADOW_LAYERS
    )

    headings = [
        mix(text, muted, i / 5) for i in range(6)
    ]

    v = [
        ("color-scheme", "dark" if dark else "light"),
        ("--beak-background-color", bg),
        ("--beak-color", text),
        ("--beak-text-selection-color", rgba(primary, 0.1875 if dark else 0.25)),
        ("--beak-muted-color", muted),
        ("--beak-muted-border-color", border),
        ("--beak-primary", primary),
        ("--beak-primary-background", primary),
        ("--beak-primary-border", "var(--beak-primary-background)"),
        ("--beak-primary-underline", rgba(primary, 0.5)),
        ("--beak-primary-hover", primary_hover),
        ("--beak-primary-hover-background", primary_hover_bg),
        ("--beak-primary-hover-border", "var(--beak-primary-hover-background)"),
        ("--beak-primary-hover-underline", "var(--beak-primary-hover)"),
        ("--beak-primary-focus", rgba(primary, 0.375 if dark else 0.5)),
        ("--beak-primary-inverse", on_primary),
        ("--beak-secondary", secondary_text),
        ("--beak-secondary-background", secondary_bg),
        ("--beak-secondary-border", "var(--beak-secondary-background)"),
        ("--beak-secondary-underline", rgba(secondary_text, 0.5)),
        ("--beak-secondary-hover", mix(secondary_text, text, 0.25)),
        ("--beak-secondary-hover-background", mix(secondary_bg, text, 0.08)),
        ("--beak-secondary-hover-border", "var(--beak-secondary-hover-background)"),
        ("--beak-secondary-hover-underline", "var(--beak-secondary-hover)"),
        ("--beak-secondary-focus", rgba(secondary_text, 0.25 if dark else 0.3)),
        ("--beak-secondary-inverse", on_secondary),
        ("--beak-contrast", contrast_color),
        ("--beak-contrast-background", contrast_color),
        ("--beak-contrast-border", "var(--beak-contrast-background)"),
        ("--beak-contrast-underline", rgba(contrast_color, 0.5)),
        ("--beak-contrast-hover", contrast_hover),
        ("--beak-contrast-hover-background", contrast_hover),
        ("--beak-contrast-hover-border", "var(--beak-contrast-hover-background)"),
        ("--beak-contrast-hover-underline", "var(--beak-contrast-hover)"),
        ("--beak-contrast-focus", rgba(contrast_color, 0.25)),
        ("--beak-contrast-inverse", bg),
        ("--beak-box-shadow", shadow),
    ]
    v += [("--beak-h%d-color" % (i + 1), c) for i, c in enumerate(headings)]
    v += [
        ("--beak-mark-background-color", rgba(warning, 0.4 if dark else 0.35)),
        ("--beak-mark-color", text),
        ("--beak-ins-color", success),
        ("--beak-del-color", danger),
        ("--beak-warning", warning_text),
        ("--beak-blockquote-border-color", "var(--beak-muted-border-color)"),
        ("--beak-blockquote-footer-color", "var(--beak-muted-color)"),
        ("--beak-button-box-shadow", "0 0 0 rgba(0, 0, 0, 0)"),
        ("--beak-button-hover-box-shadow", "0 0 0 rgba(0, 0, 0, 0)"),
        ("--beak-table-border-color", "var(--beak-muted-border-color)"),
        ("--beak-table-row-stripped-background-color", rgba(text, 0.04)),
        ("--beak-code-background-color", code_bg),
        ("--beak-code-color", muted),
        ("--beak-code-kbd-background-color", "var(--beak-color)"),
        ("--beak-code-kbd-color", "var(--beak-background-color)"),
        ("--beak-form-element-background-color", form_bg),
        ("--beak-form-element-selected-background-color", selected_bg),
        ("--beak-form-element-border-color", border),
        ("--beak-form-element-color", text),
        ("--beak-form-element-placeholder-color", "var(--beak-muted-color)"),
        ("--beak-form-element-active-background-color", form_bg),
        ("--beak-form-element-active-border-color", "var(--beak-primary-border)"),
        ("--beak-form-element-focus-color", "var(--beak-primary-border)"),
        ("--beak-form-element-disabled-opacity", "0.5"),
        ("--beak-form-element-invalid-border-color", mix(danger, bg, 0.4)),
        ("--beak-form-element-invalid-active-border-color", danger),
        (
            "--beak-form-element-invalid-focus-color",
            "var(--beak-form-element-invalid-active-border-color)",
        ),
        ("--beak-form-element-valid-border-color", mix(success, bg, 0.4)),
        ("--beak-form-element-valid-active-border-color", success),
        (
            "--beak-form-element-valid-focus-color",
            "var(--beak-form-element-valid-active-border-color)",
        ),
        ("--beak-switch-background-color", border),
        ("--beak-switch-checked-background-color", "var(--beak-primary-background)"),
        ("--beak-switch-color", on_primary),
        (
            "--beak-switch-thumb-box-shadow",
            "0 0 0.5rem rgba(0, 0, 0, 0.25)" if not dark else "0 0 0 rgba(0, 0, 0, 0)",
        ),
        ("--beak-range-border-color", border),
        ("--beak-range-active-border-color", mix(bg, text, 0.25)),
        ("--beak-range-thumb-border-color", "var(--beak-background-color)"),
        ("--beak-range-thumb-color", "var(--beak-secondary-background)"),
        ("--beak-range-thumb-active-color", "var(--beak-primary-background)"),
        ("--beak-accordion-border-color", "var(--beak-muted-border-color)"),
        ("--beak-accordion-active-summary-color", "var(--beak-primary-hover)"),
        ("--beak-accordion-close-summary-color", "var(--beak-color)"),
        ("--beak-accordion-open-summary-color", "var(--beak-muted-color)"),
        ("--beak-card-background-color", "var(--beak-background-color)"),
        ("--beak-card-border-color", "var(--beak-muted-border-color)"),
        ("--beak-card-box-shadow", "var(--beak-box-shadow)"),
        ("--beak-card-sectioning-background-color", form_bg),
        ("--beak-loading-spinner-opacity", "0.5"),
        ("--beak-modal-overlay-background-color", rgba(bg, 0.75)),
        ("--beak-progress-background-color", border),
        ("--beak-progress-color", "var(--beak-primary-background)"),
        ("--beak-tooltip-background-color", "var(--beak-contrast-background)"),
        ("--beak-tooltip-color", "var(--beak-contrast-inverse)"),
        ("--beak-icon-valid", ICON_VALID.format(color=success.replace("#", "%23"))),
        ("--beak-icon-invalid", ICON_INVALID.format(color=danger.replace("#", "%23"))),
    ]
    return v


HEADER = """\
/*!
 * Beak CSS theme — {name} {emoji}
 * {kind} Load *after* beak.css.
 * {credit}
 * Palette © its respective project — see NOTICE.md.
 */"""

ADAPTIVE_HEADER = """\
/*!
 * Beak CSS theme — {name} (adaptive) 🌗
 * Follows prefers-color-scheme and data-theme: light = {light}, dark = {dark}.
 * Load *after* beak.css.
 * {credit}
 * Palette © its respective project — see NOTICE.md.
 */"""

LIGHT_SELECTORS = """[data-theme=light],
:root:not([data-theme=dark]),
:host(:not([data-theme=dark]))"""

SYSTEM_SELECTORS = """:root:not([data-theme]),
  :host(:not([data-theme]))"""

DARK_SELECTORS = """[data-theme=dark]"""


def block(selector, decls, indent=""):
    body = "\n".join(f"{indent}  {n}: {v};" for n, v in decls)
    return f"{indent}{selector} {{\n{body}\n{indent}}}"


def wrap(header, light_decls, dark_decls):
    inner = "\n\n".join(
        [
            block(LIGHT_SELECTORS, light_decls),
            "@media only screen and (prefers-color-scheme: dark) {\n"
            + block(SYSTEM_SELECTORS, dark_decls, "  ")
            + "\n}",
            block(DARK_SELECTORS, dark_decls),
        ]
    )
    return f"{header}\n@layer beak {{\n{inner}\n}}\n"


def render(t):
    """A single-flavour palette, pinned in all three selector groups."""
    decls = vars_for(t)
    emoji = "🌑" if t["mode"] == "dark" else "☀️"
    header = HEADER.format(
        name=t["name"],
        emoji=emoji,
        kind=f"Full palette ({t['mode']}).",
        credit=t["credit"],
    )
    return wrap(header, decls, decls)


def render_adaptive(pair, light_t, dark_t):
    """A family that has both flavours, following the OS and data-theme."""
    header = ADAPTIVE_HEADER.format(
        name=pair["name"],
        light=light_t["name"],
        dark=dark_t["name"],
        credit=light_t["credit"],
    )
    return wrap(header, vars_for(light_t), vars_for(dark_t))


# --- llms.txt ---------------------------------------------------------------

LLMS_HEAD = """\
# Beak CSS

> Beak CSS is a classless, pure-CSS fork of Pico CSS v2.1.1. It styles plain
> semantic HTML with no classes, no SASS and no build step. Every token is a
> CSS custom property named `--beak-*`, and the whole framework ships inside
> `@layer beak`, so your own CSS always wins without specificity fights.

## Start here

- [README](https://beakcss.dev.ar/README.md): install, usage, variables, theming, regenerating `dist/`.
- [Demo](https://beakcss.dev.ar/): live classless demo with the theme picker.
- [Source](https://github.com/4lb0/beakcss): repository, issues, releases.
- [Changelog](https://github.com/4lb0/beakcss/blob/main/CHANGELOG.md): release history.

## Files

- [beak.min.css](https://beakcss.dev.ar/dist/beak.min.css): full-width build, the default. Use this in apps and dashboards.
- [beak.contained.min.css](https://beakcss.dev.ar/dist/beak.contained.min.css): same, plus a centered reading column for docs and blogs.
- [beak.css](https://beakcss.dev.ar/dist/beak.css): unminified, human-readable source.
- [beak.contained.css](https://beakcss.dev.ar/dist/beak.contained.css): unminified constrained build.

## Usage

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/beakcss/dist/beak.min.css">
<!-- optional, exactly one theme, after the base: -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/beakcss/dist/themes/full/dracula.css">
```

- npm: `npm install beakcss`, then `import "beakcss"` (JS bundler) or link `node_modules/beakcss/dist/beak.min.css`.
- Light, dark and system mode come from the base: `data-theme="light|dark"` on `<html>`, or omit it to follow `prefers-color-scheme`.
- Load order: base → theme → your CSS. Never edit the shipped files; override the `--beak-*` variables instead.

## Themes

Two kinds, both loaded *after* the base stylesheet:

1. **Tints** (`dist/themes/{{name}}.css`) — Pico's 19 color palettes. They only
   swap the accent ramps and stay light/dark aware, so they follow the OS.
2. **Full palettes** (`dist/themes/full/{{name}}.css`) — complete schemes with
   their own background, text, borders, code and form colors. A single-flavour
   file is *pinned* across light, system and dark, so a dark-only scheme never
   flips. Families with both flavours also ship an `{{family}}-auto.css` that
   follows `prefers-color-scheme` and `data-theme` instead.

Tints: {tints}.

Full palettes:

{full}

### Adaptive (follows light/dark)

{adaptive}

## Notes for LLMs

- There are no classes. Style the elements themselves: `header`, `main`, `nav`, `section`, `article`, `aside`, `footer`, `figure`, `table`, `form`, `fieldset`, `label`, `input`, `select`, `textarea`, `button`, `details`, `dialog`.
- Semantic attributes drive components: `role="switch"` on a checkbox renders a switch, `role="button"` styles a link as a button, `<details>` renders an accordion.
- Colors and measures are variables, not values to hardcode: `--beak-primary`, `--beak-background-color`, `--beak-color`, `--beak-spacing`, `--beak-border-radius`. Full list in the color-scheme blocks of `dist/beak.css`.
- Common aliases resolve out of the box: `--beak-accent` (= `--beak-primary`), `--beak-text-color` (= `--beak-color`), `--beak-bg` (= `--beak-background-color`), `--beak-link-color`, `--beak-success`, `--beak-danger`, `--beak-warning`, `--beak-info`, `--beak-font`, `--beak-radius`, `--beak-shadow`, `--beak-space`. Aliases are read-only: override the canonical name (e.g. `--beak-primary`, not `--beak-accent`).
- Themes are additive files inside the same `@layer beak`; import one at a time.
- `dist/` is generated by `tools/build.py` (base builds) and `tools/themes.py` (full palettes). Do not hand-edit.
"""


def write_llms():
    tints = ", ".join(
        ["amber", "blue", "cyan", "fuchsia", "green", "grey", "indigo", "jade",
         "lime", "orange", "pink", "pumpkin", "purple", "red", "sand", "slate",
         "violet", "yellow", "zinc"]
    )
    lines = []
    last_family = None
    for t in THEMES:
        if t["family"] != last_family:
            if lines:
                lines.append("")
            lines.append("### " + t["family"])
            lines.append("")
            last_family = t["family"]
        lines.append(
            "- [{}](https://beakcss.dev.ar/dist/themes/full/{}.css): {} palette."
            .format(t["name"], t["id"], t["mode"])
        )

    by_id = {t["id"]: t for t in THEMES}
    adaptive = [
        "- [{} (auto)](https://beakcss.dev.ar/dist/themes/full/{}.css): light = {}, dark = {}."
        .format(
            p["name"],
            p["id"],
            by_id[p["light"]]["name"],
            by_id[p["dark"]]["name"],
        )
        for p in ADAPTIVE
    ]

    text = LLMS_HEAD.format(
        tints=tints, full="\n".join(lines), adaptive="\n".join(adaptive)
    )
    (ROOT / "llms.txt").write_text(text)
    return "llms.txt"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    seen = set()
    for t in THEMES:
        assert t["id"] not in seen, "duplicate theme id: " + t["id"]
        seen.add(t["id"])
        assert re.fullmatch(r"[a-z0-9-]+", t["id"])
        (OUT / f"{t['id']}.css").write_text(render(t))

    by_id = {t["id"]: t for t in THEMES}
    for p in ADAPTIVE:
        assert p["id"] not in seen, "duplicate theme id: " + p["id"]
        seen.add(p["id"])
        light_t, dark_t = by_id[p["light"]], by_id[p["dark"]]
        assert light_t["mode"] == "light", p["id"]
        assert dark_t["mode"] == "dark", p["id"]
        (OUT / f"{p['id']}.css").write_text(render_adaptive(p, light_t, dark_t))

    print(
        f"built: dist/themes/full/*.css "
        f"({len(THEMES)} palettes + {len(ADAPTIVE)} adaptive)"
    )
    print("built:", write_llms())


if __name__ == "__main__":
    main()
