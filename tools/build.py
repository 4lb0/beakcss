#!/usr/bin/env python3
"""
Beak CSS generator.

Fork of Pico CSS v2.1.1, classless only, pure CSS (no SASS).

It produces, in `dist/`:
  - beak.css / beak.min.css            -> FLUID (default), wrapped in @layer beak
  - beak.contained.css / *.min         -> constrained reading width
  - themes/<color>.css                 -> tiny palette override, @layer beak

Everything is renamed from --pico-* to --beak-*.

Usage:
    python3 tools/build.py /path/to/pico/css

`/path/to/pico/css` is the `css/` folder of a checkout of the Pico CSS
repository at v2.1.1 (https://github.com/picocss/pico).
"""

import re
import sys
import pathlib

VERSION = "0.2.0"
LAYER = "beak"

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

COLORS = [
    "amber", "blue", "cyan", "fuchsia", "green", "grey", "indigo", "jade",
    "lime", "orange", "pink", "pumpkin", "purple", "red", "sand", "slate",
    "violet", "yellow", "zinc",
]

HEADER = (
    "/*!\n"
    f" * Beak CSS \U0001f426 v{VERSION} — a classless fork of Pico CSS\n"
    f" * Classless · @layer {LAYER} · no SASS · CSS variables for colors and measures\n"
    " * Based on Pico CSS \u2728 v2.1.1 (https://picocss.com)\n"
    " * Copyright 2019-2025 Pico — Copyright 2026 Beak — Licensed under MIT\n"
    " */"
)

HEADER_MIN = (
    "/*!"
    f" Beak CSS v{VERSION} — classless fork of Pico CSS v2.1.1 "
    "(https://picocss.com) — MIT. Copyright 2019-2025 Pico, 2026 Beak. */"
)

THEME_HEADER = (
    "/*!\n"
    f" * Beak CSS theme — {{color}} \U0001f3a8\n"
    " * Palette override. Load *after* beak.css.\n"
    " * Generated from Pico CSS v2.1.1 color \"{color}\".\n"
    " */"
)

VAR_RE = re.compile(r"--pico-([a-z0-9-]+)")


def strip_leading(css: str) -> str:
    """Remove a leading @charset and the leading banner comment (/*! ... */)."""
    css = css.lstrip("\ufeff")
    if css.startswith('@charset "UTF-8";'):
        css = css[len('@charset "UTF-8";'):]
    css = css.lstrip("\n")
    if css.startswith("/*!"):
        css = css[css.index("*/") + 2:].lstrip("\n")
    return css


def rename(css: str) -> str:
    css = VAR_RE.sub(r"--beak-\1", css)
    assert "--pico-" not in css, "leftover --pico- variables"
    return css


def layered(css: str) -> str:
    return f"@layer {LAYER} {{\n{css}\n}}\n"


def build_base(pico_css: pathlib.Path, src: str, out: str):
    body = rename(strip_leading((pico_css / src).read_text()))

    # minified variant (Pico ships it already minified)
    min_src = src.replace(".css", ".min.css")
    min_body = rename(strip_leading((pico_css / min_src).read_text()))
    min_out = out.replace(".css", ".min.css")

    (DIST / out).write_text(
        '@charset "UTF-8";\n' + HEADER + "\n" + layered(body)
    )
    (DIST / min_out).write_text(
        '@charset "UTF-8";' + HEADER_MIN + "\n" + f"@layer {LAYER}{{" + min_body + "}\n"
    )
    return out, min_out


# --- color override extraction ---------------------------------------------

DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")


def parse_decls(css: str):
    """
    Return {(stack, var): value} where `stack` is the tuple of enclosing
    preludes (at-rules + selectors), outermost first.
    """
    out = {}
    buf = ""
    stack = []
    for ch in css:
        if ch == "{":
            stack.append(buf.strip())
            buf = ""
        elif ch == "}":
            if stack:
                for name, val in DECL_RE.findall(buf):
                    out[(tuple(stack), name)] = val.strip()
                stack.pop()
            buf = ""
        else:
            buf += ch
    return out


def indent(text: str, pad: str = "  ") -> str:
    return "\n".join(pad + line if line.strip() else line for line in text.split("\n"))


def render_theme(changes, base_decls, color: str) -> str:
    grouped = {}
    for (stack, name), val in changes:
        grouped.setdefault(stack, []).append((name, val))

    rules = []
    for stack, decls in grouped.items():
        inner = "\n".join(f"    {n}: {v};" for n, v in decls)
        block = f"{stack[-1]} {{\n{inner}\n  }}"
        for at in reversed(stack[:-1]):
            block = f"{at} {{\n{indent(block)}\n}}"
        rules.append(block)

    body = "\n\n".join(rules)
    return (
        THEME_HEADER.replace("{color}", color)
        + "\n"
        + layered(body)
    )


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    pico_css = pathlib.Path(sys.argv[1])
    if not pico_css.is_dir():
        sys.exit(f"not a directory: {pico_css}")

    # clean dist
    if DIST.exists():
        for p in DIST.iterdir():
            if p.is_file():
                p.unlink()
    (DIST / "themes").mkdir(parents=True, exist_ok=True)

    fluid = build_base(pico_css, "pico.fluid.classless.css", "beak.css")
    contained = build_base(pico_css, "pico.classless.css", "beak.contained.css")
    print("built:", *fluid, *contained)

    base_decls = parse_decls(
        rename(strip_leading((pico_css / "pico.classless.css").read_text()))
    )

    for color in COLORS:
        color_decls = parse_decls(
            rename(
                strip_leading(
                    (pico_css / f"pico.classless.{color}.css").read_text()
                )
            )
        )
        changes = [
            (k, v) for k, v in color_decls.items() if base_decls.get(k) != v
        ]
        # verify the overrides reconstruct the original palette exactly
        merged = dict(base_decls)
        merged.update(dict(changes))
        assert merged == color_decls, f"palette reconstruction failed for {color}"

        (DIST / "themes" / f"{color}.css").write_text(
            render_theme(changes, base_decls, color)
        )
    print(f"built: themes/*.css ({len(COLORS)} colors)")


if __name__ == "__main__":
    main()
