"""A tiny SVG canvas with real font metrics and embedded, subset fonts.

GitHub serves README images in a sandbox that blocks external fonts, so every
SVG carries its own WOFF2 subsets: only the glyphs that image actually uses.
Text is measured with the real advance widths, so wrapping and centring are
exact rather than guessed.
"""

from __future__ import annotations

import base64
import io
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

import logging

from fontTools import subset

logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"

# key -> (file, css family, weight, style)
FONTS = {
    "sans": ("Geist-Regular.ttf", "G", 400, "normal"),
    "semi": ("Geist-SemiBold.ttf", "GS", 600, "normal"),
    "mono": ("GeistMono-Regular.ttf", "GM", 400, "normal"),
    "serif": ("InstrumentSerif-Italic.woff2", "IS", 400, "italic"),
}

FALLBACK = {
    "sans": "ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif",
    "semi": "ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif",
    "mono": "ui-monospace,'SF Mono',Menlo,Consolas,monospace",
    "serif": "Georgia,'Times New Roman',serif",
}


@lru_cache(maxsize=None)
def _font(key: str) -> TTFont:
    return TTFont(FONT_DIR / FONTS[key][0])


@lru_cache(maxsize=None)
def _metrics(key: str):
    f = _font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"].metrics
    upm = f["head"].unitsPerEm
    return cmap, hmtx, upm


def measure(text: str, font: str, size: float, tracking: float = 0.0) -> float:
    """Advance width of `text` in px. `tracking` is letter-spacing in em."""
    cmap, hmtx, upm = _metrics(font)
    total = 0
    for ch in text:
        glyph = cmap.get(ord(ch)) or cmap.get(ord("?"))
        total += hmtx[glyph][0] if glyph else upm * 0.5
    return total * size / upm + tracking * size * len(text)


def wrap(text: str, font: str, size: float, width: float, tracking: float = 0.0) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and measure(trial, font, size, tracking) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


@lru_cache(maxsize=None)
def _subset_b64(key: str, chars: str) -> str:
    font = TTFont(FONT_DIR / FONTS[key][0])
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    opts.hinting = False
    sub = subset.Subsetter(opts)
    sub.populate(unicodes={ord(c) for c in chars} | {0x20})
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def esc(s: str) -> str:
    return escape(str(s), {'"': "&quot;"})


def fmt(n: float) -> str:
    return f"{n:.2f}".rstrip("0").rstrip(".") if isinstance(n, float) else str(n)


class SVG:
    """Collects markup and the characters used per font, then renders."""

    def __init__(self, w: int, h: int, theme: dict, title: str, desc: str = ""):
        self.w, self.h, self.t = w, h, theme
        self.title, self.desc = title, desc
        self.parts: list[str] = []
        self.defs: list[str] = []
        self.css: list[str] = []
        self.used: dict[str, set] = defaultdict(set)
        self._ids = 0

    # -- bookkeeping -------------------------------------------------------
    def uid(self, prefix: str = "u") -> str:
        self._ids += 1
        return f"{prefix}{self._ids}"

    def use(self, font: str, text: str) -> None:
        self.used[font].update(text)

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def defn(self, markup: str) -> None:
        self.defs.append(markup)

    def style(self, css: str) -> None:
        self.css.append(css)

    # -- primitives --------------------------------------------------------
    def text(self, x, y, s, font="sans", size=16, fill=None, anchor="start",
             tracking=0.0, cls="", attrs="", upper=False) -> str:
        s = s.upper() if upper else s
        self.use(font, s)
        fill = fill or self.t["ink"]
        ls = f' letter-spacing="{fmt(tracking * size)}"' if tracking else ""
        an = f' text-anchor="{anchor}"' if anchor != "start" else ""
        c = f' class="f-{font} {cls}"'.replace(" \"", "\"")
        el = (f'<text x="{fmt(x)}" y="{fmt(y)}"{c} font-size="{fmt(size)}" '
              f'fill="{fill}"{an}{ls}{(" " + attrs) if attrs else ""}>{esc(s)}</text>')
        return el

    def runs(self, x, y, runs, size, anchor="start", cls="", attrs="", tracking=0.0) -> str:
        """Mixed-font line: runs = [(text, font, fill), ...]."""
        spans = []
        for s, font, fill in runs:
            self.use(font, s)
            spans.append(f'<tspan class="f-{font}" fill="{fill or self.t["ink"]}">{esc(s)}</tspan>')
        an = f' text-anchor="{anchor}"' if anchor != "start" else ""
        ls = f' letter-spacing="{fmt(tracking * size)}"' if tracking else ""
        c = f' class="{cls}"' if cls else ""
        return (f'<text x="{fmt(x)}" y="{fmt(y)}" font-size="{fmt(size)}"{an}{ls}{c}'
                f'{(" " + attrs) if attrs else ""} xml:space="preserve">{"".join(spans)}</text>')

    # -- output ------------------------------------------------------------
    def render(self) -> str:
        faces = []
        for key, chars in sorted(self.used.items()):
            if not chars:
                continue
            _, fam, weight, style = FONTS[key]
            data = _subset_b64(key, "".join(sorted(chars)))
            faces.append(
                f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{data}) format('woff2');"
                f"font-weight:{weight};font-style:{style};}}"
            )
            faces.append(f".f-{key}{{font-family:{fam},{FALLBACK[key]};font-weight:{weight};"
                         f"font-style:{style};}}")
        base = (
            "text{font-kerning:normal;}"
            "@media (prefers-reduced-motion:reduce){*{animation:none!important;}"
            ".motion{display:none!important;}}"
        )
        style = "".join(faces) + base + "".join(self.css)
        desc = f'<desc id="d">{esc(self.desc)}</desc>' if self.desc else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" '
            f'aria-labelledby="t d" fill="none">'
            f'<title id="t">{esc(self.title)}</title>{desc}'
            f"<style>{style}</style><defs>{''.join(self.defs)}</defs>{''.join(self.parts)}</svg>\n"
        )


# -- shared scenery ----------------------------------------------------------

def panel(svg: SVG, x=0.5, y=0.5, w=None, h=None, r=22, fill=None, grid=True, glow=None) -> None:
    """The framed, gridded surface every image sits on (portfolio 'atmosphere')."""
    t = svg.t
    w = w if w is not None else svg.w - 1
    h = h if h is not None else svg.h - 1
    clip = svg.uid("clip")
    svg.defn(f'<clipPath id="{clip}"><rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{r}"/></clipPath>')
    svg.add(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{r}" fill="{fill or t["bg"]}"/>')
    svg.add(f'<g clip-path="url(#{clip})">')
    if grid:
        pat, fade, mask = svg.uid("grid"), svg.uid("fade"), svg.uid("mask")
        svg.defn(
            f'<pattern id="{pat}" width="44" height="44" patternUnits="userSpaceOnUse">'
            f'<path d="M44 0H0V44" stroke="{t["grid"]}" stroke-width="1"/></pattern>'
            f'<linearGradient id="{fade}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0.15"/></linearGradient>'
            f'<mask id="{mask}"><rect width="{svg.w}" height="{svg.h}" fill="url(#{fade})"/></mask>'
        )
        svg.add(f'<rect width="{svg.w}" height="{svg.h}" fill="url(#{pat})" mask="url(#{mask})"/>')
    if glow:
        gx, gy, gr = glow
        g = svg.uid("glow")
        svg.defn(
            f'<radialGradient id="{g}"><stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glow_opacity"]}"/>'
            f'<stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>'
        )
        svg.add(f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="url(#{g})"/>')
    svg.add("</g>")
    svg.add(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{r}" stroke="{t["line_strong"]}"/>')


def label(svg: SVG, x, y, s, fill=None, size=12, anchor="start", cls="", attrs="") -> str:
    """Mono, uppercase, tracked: the portfolio's label style."""
    return svg.text(x, y, s, "mono", size, fill or svg.t["ink3"], anchor, 0.06, cls, attrs, upper=True)


def pill(svg: SVG, x, y, s, size=11, pad=9, h=24, fill=None, stroke=None, color=None, font="mono",
         upper=False) -> float:
    """A tag pill; returns its width so callers can flow pills along a line."""
    t = svg.t
    s2 = s.upper() if upper else s
    w = measure(s2, font, size, 0.02 if upper else 0) + pad * 2
    svg.add(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{h}" rx="{h / 2}" '
            f'fill="{fill or "none"}" stroke="{stroke or t["line_strong"]}"/>')
    svg.add(svg.text(x + w / 2, y + h / 2 + size * 0.36, s2, font, size, color or t["ink2"], "middle",
                     0.02 if upper else 0))
    return w


def wrap_runs(runs, size: float, width: float) -> list[list[tuple]]:
    """Wrap mixed-font runs [(text, font, fill)] into lines of runs, word by word."""
    words = []  # (word, font, fill, space_before)
    pending = False
    for text, font, fill in runs:
        for i, w in enumerate(text.split(" ")):
            if w == "":
                pending = True
                continue
            # A word follows a space unless it continues the previous run ("workflow" + ".").
            words.append([w, font, fill, i > 0 or pending])
            pending = False
    lines, cur, cur_w = [], [], 0.0
    for w, font, fill, lead in words:
        sp = measure(" ", font, size) if (cur and lead) else 0
        ww = measure(w, font, size)
        if cur and cur_w + sp + ww > width:
            lines.append(cur)
            cur, cur_w, sp = [], 0.0, 0
        cur.append(((" " if sp else "") + w, font, fill))
        cur_w += sp + ww
    if cur:
        lines.append(cur)
    # merge adjacent same-font runs
    out = []
    for line in lines:
        merged = []
        for text, font, fill in line:
            if merged and merged[-1][1] == font and merged[-1][2] == fill:
                merged[-1] = (merged[-1][0] + text, font, fill)
            else:
                merged.append((text, font, fill))
        out.append(merged)
    return out
