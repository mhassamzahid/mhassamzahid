"""CV metrics, each figure drawn literally.

15 nodes and a "+"; a bar shrunk to the 30% of manual work left; 199 of 200
dots; one tick per month in production since Sep 2025 (counted at build time).
"""

from datetime import date

from .. import profile as P
from ..svgkit import SVG, fmt, label, panel, wrap

W, H = 1000, 262
TILE = W / 4


def months_in_production(today: date | None = None) -> int:
    today = today or date.today()
    y, m = map(int, P.CURRENT["since"].split("-"))
    return (today.year - y) * 12 + today.month - m + 1


def _nodes(s, t, x, y):
    pts = []
    for i in range(15):
        r, c = divmod(i, 5)
        c = c if r % 2 == 0 else 4 - c  # snake through the grid like a workflow
        pts.append((x + 6 + c * 30, y + 8 + r * 28))
    d = "M" + "L".join(f"{fmt(a)} {fmt(b)}" for a, b in pts)
    s.add(f'<path d="{d}" stroke="{t["line_strong"]}" stroke-width="1.5"/>')
    s.add(f'<path d="{d}" stroke="{t["accent"]}" stroke-width="1.5" pathLength="1" stroke-dasharray="1" '
          f'stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin=".3s" '
          f'dur="2.2s" fill="freeze"/></path>')
    for i, (a, b) in enumerate(pts):
        s.add(f'<circle cx="{fmt(a)}" cy="{fmt(b)}" r="5.5" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="1.5"/>'
              f'<circle cx="{fmt(a)}" cy="{fmt(b)}" r="3.2" fill="{t["accent"]}" class="pop" '
              f'style="animation-delay:{.3 + i * .14:.2f}s"/>')
    px, py = x + 170, y + 36
    s.add(f'<path d="M{px - 9} {py}H{px + 9}M{px} {py - 9}V{py + 9}" stroke="{t["accent"]}" stroke-width="2.5" '
          f'stroke-linecap="round" class="pop" style="animation-delay:2.5s"/>')


def _shrink(s, t, x, y):
    w, h = 186, 16
    by = y + 22
    s.add(f'<rect x="{x}" y="{by}" width="{w}" height="{h}" rx="4" fill="{t["ramp"][1]}"/>')
    s.add(f'<rect x="{x}" y="{by}" width="{w * .3:.1f}" height="{h}" rx="4" fill="{t["accent"]}">'
          f'<animate attributeName="width" from="{w}" to="{w * .3:.1f}" begin=".4s" dur="1.8s" fill="freeze" '
          f'calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/></rect>')
    for i in range(11):
        tx = x + w * i / 10
        s.add(f'<path d="M{fmt(tx)} {by + h + 6}v{6 if i % 5 == 0 else 3}" stroke="{t["ink4"]}"/>')
    s.add(label(s, x, by + h + 30, "manual ops: 100%", size=10))
    s.add(label(s, x + w, by + h + 30, "→ 30%", t["accent"], size=10, anchor="end"))


def _dots(s, t, x, y):
    for c in range(20):
        g = [f'<g class="pop" style="animation-delay:{.3 + c * .06:.2f}s">']
        for r in range(10):
            cx, cy = x + 3 + c * 9.4, y + 3 + r * 8.2
            if c == 19 and r == 9:
                g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="2.6" stroke="{t["ink3"]}" stroke-width="1"/>')
            else:
                g.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="2.8" fill="{t["accent"]}"/>')
        g.append("</g>")
        s.add("".join(g))


def _months(s, t, x, y):
    n = months_in_production()
    w = 186
    step = w / max(n - 1, 1)
    for i in range(n):
        tx = x + i * step
        last = i == n - 1
        hgt = 46 if last else (34 if i % 12 == 0 else 24)
        s.add(f'<rect x="{fmt(tx - 1.5)}" y="{fmt(y + 52 - hgt)}" width="3" height="{hgt}" rx="1.5" '
              f'fill="{t["accent"] if last else t["ink3"]}" class="pop" style="animation-delay:{.3 + i * .09:.2f}s"/>')
    lx = x + (n - 1) * step
    s.add(f'<circle cx="{fmt(lx)}" cy="{y + 2}" r="4" fill="{t["accent"]}"/>'
          f'<circle cx="{fmt(lx)}" cy="{y + 2}" r="4" stroke="{t["accent"]}" class="motion">'
          f'<animate attributeName="r" values="4;11" dur="2s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/></circle>')
    s.add(label(s, x, y + 76, "Sep 2025", size=10))
    s.add(label(s, lx, y + 76, f"now · {n} mo", t["accent"], size=10, anchor="end"))


GLYPHS = {"nodes": _nodes, "shrink": _shrink, "dots": _dots, "months": _months}


def build(t: dict) -> SVG:
    s = SVG(W, H, t, "Impact, quoted from the CV",
            "; ".join(f'{m["value"]} {m["label"]}' for m in P.METRICS))
    s.style("@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:none}}"
            ".pop{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,.8,.2,1) both}"
            "@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
            ".up{animation:up .7s cubic-bezier(.2,.8,.2,1) both}")
    panel(s)
    for i, m in enumerate(P.METRICS):
        x0 = i * TILE
        if i:
            s.add(f'<path d="M{fmt(x0)} 24V{H - 24}" stroke="{t["line"]}"/>')
        GLYPHS[m["glyph"]](s, t, x0 + 26, 34)
        s.add(f'<g class="up" style="animation-delay:{.2 + i * .12:.2f}s">'
              f'{s.text(x0 + 26, 180, m["value"], "semi", 52, t["ink"], tracking=-0.045)}</g>')
        for j, ln in enumerate(wrap(m["label"], "sans", 14, TILE - 50)):
            s.add(s.text(x0 + 26, 208 + j * 20, ln, "sans", 14, t["ink3"]))
    return s
