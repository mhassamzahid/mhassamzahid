"""The CV skills as a periodic table: one period per CV group, numbered in CV order.

AI & Automation is tinted signal: it's the core specialism.
"""

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel

W = 1000
LEFT = 176
GAP = 7
COLS = max(len(items) for _, items in P.SKILL_GROUPS)
CELL = (W - LEFT - 28 - GAP * (COLS - 1)) / COLS
TOP = 64


def build(t: dict) -> SVG:
    rows = len(P.SKILL_GROUPS)
    H = int(TOP + rows * (CELL + GAP) + 40)
    total = sum(len(i) for _, i in P.SKILL_GROUPS)
    s = SVG(W, H, t, "Stack: the CV skills as a periodic table",
            " ".join(f"{g}: {', '.join(n for _, n in items)}." for g, items in P.SKILL_GROUPS))
    s.style("@keyframes el{from{opacity:0;transform:translateY(10px) scale(.92)}to{opacity:1;transform:none}}"
            ".el{transform-box:fill-box;transform-origin:center;animation:el .55s cubic-bezier(.2,.8,.2,1) both}")
    panel(s, glow=(LEFT + 200, TOP + 40, 320))
    s.add(label(s, 28, 38, f"{total} elements · {rows} periods", size=11))
    s.add(label(s, W - 28, 38, "numbered in CV order · core specialism tinted", size=11, anchor="end"))

    n = 0
    for r, (group, items) in enumerate(P.SKILL_GROUPS):
        y = TOP + r * (CELL + GAP)
        core = r == 0
        s.add(s.text(28, y + 24, f"P{r + 1}", "mono", 11, t["accent"] if core else t["ink4"]))
        words = group.split(" & ")
        for j, wd in enumerate(words):
            s.add(s.text(28, y + 46 + j * 18, wd + (" &" if j < len(words) - 1 else ""), "semi", 15,
                         t["ink"] if core else t["ink2"], tracking=-0.01))
        for c, (sym, name) in enumerate(items):
            n += 1
            x = LEFT + c * (CELL + GAP)
            fill = t["signal"] if core else t["bg_raised"]
            ink = t["on_signal"] if core else t["ink"]
            sub = t["on_signal"] if core else t["ink3"]
            g = [f'<g class="el" style="animation-delay:{.15 + (r + c) * .05:.2f}s">',
                 f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(CELL)}" height="{fmt(CELL)}" rx="8" fill="{fill}" '
                 f'stroke="{t["line_strong"] if not core else "none"}"/>',
                 s.text(x + 7, y + 15, str(n), "mono", 9.5, sub),
                 s.text(x + CELL / 2, y + CELL / 2 + 8, sym, "semi", 26, ink, "middle", -0.02)]
            nsize = 9
            while measure(name, "mono", nsize) > CELL - 8 and nsize > 7:
                nsize -= 0.5
            g.append(s.text(x + CELL / 2, y + CELL - 9, name, "mono", nsize, sub, "middle"))
            g.append("</g>")
            s.add("".join(g))
    return s
