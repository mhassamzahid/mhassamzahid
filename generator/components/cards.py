"""Case-study cards. Each draws the project's real system: inputs -> core -> outputs."""

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel, pill, wrap

W, H = 490, 448
WELL = (16, 16, W - 32, 196)


def _column(items, x_mid, top, height):
    n = len(items)
    gap = min(31, (height - 24) / max(n, 1))
    span = gap * (n - 1)
    y0 = top + height / 2 - span / 2
    return [(it, x_mid, y0 + i * gap) for i, it in enumerate(items)]


def _diagram(s, t, sysd, idx):
    x, y, w, h = WELL
    pat = s.uid("g")
    s.defn(f'<pattern id="{pat}" width="16" height="16" patternUnits="userSpaceOnUse">'
           f'<circle cx="1" cy="1" r=".9" fill="{t["line_strong"]}"/></pattern>')
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["bg_sunk"]}"/>')
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="url(#{pat})"/>')
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" stroke="{t["line"]}"/>')
    s.add(label(s, x + 14, y + 22, "inputs", size=9))
    s.add(label(s, x + w - 14, y + 22, "outputs", size=9, anchor="end"))

    cx, cy, cw, ch = x + w / 2, y + h / 2 + 8, 118, 58
    ins = _column(sysd["inputs"], x + 84, y + 26, h - 30)
    outs = _column(sysd["outputs"], x + w - 76, y + 26, h - 30)

    def edge(x1, y1, x2, y2, k):
        pid = s.uid("e")
        mx = (x1 + x2) / 2
        d = f"M{fmt(x1)} {fmt(y1)}C{fmt(mx)} {fmt(y1)} {fmt(mx)} {fmt(y2)} {fmt(x2)} {fmt(y2)}"
        s.defn(f'<path id="{pid}" d="{d}"/>')
        s.add(f'<path d="{d}" stroke="{t["line_strong"]}"/>')
        dur = 1.9
        begin = (k * 0.45 + idx * 0.2) % 3
        s.add(f'<circle r="2.6" fill="{t["pulse"]}" class="motion" opacity="0">'
              f'<animateMotion dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion>'
              f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite"/></circle>')

    k = 0
    for name, nx, ny in ins:
        nw = measure(name, "mono", 10.5) + 16
        edge(nx + nw / 2, ny, cx - cw / 2, cy, k)
        k += 1
    for name, nx, ny in outs:
        nw = measure(name, "mono", 10.5) + 16
        edge(cx + cw / 2, cy, nx - nw / 2, ny, k + 1.5)
        k += 1
    for name, nx, ny in ins + outs:
        nw = measure(name, "mono", 10.5) + 16
        s.add(f'<rect x="{fmt(nx - nw / 2)}" y="{fmt(ny - 11)}" width="{fmt(nw)}" height="22" rx="11" '
              f'fill="{t["bg_raised"]}" stroke="{t["line_strong"]}"/>')
        s.add(s.text(nx, ny + 3.8, name, "mono", 10.5, t["ink2"], "middle"))

    # core
    s.add(f'<rect x="{fmt(cx - cw / 2 - 5)}" y="{fmt(cy - ch / 2 - 5)}" width="{cw + 10}" height="{ch + 10}" rx="15" '
          f'stroke="{t["pulse"]}" stroke-opacity=".5" class="motion">'
          f'<animate attributeName="stroke-opacity" values=".6;0;.6" dur="2.4s" repeatCount="indefinite"/></rect>')
    s.add(f'<rect x="{fmt(cx - cw / 2)}" y="{fmt(cy - ch / 2)}" width="{cw}" height="{ch}" rx="12" fill="{t["signal"]}"/>')
    s.add(s.text(cx, cy - 3, sysd["core"], "semi", 14, t["on_signal"], "middle", -0.01))
    s.add(s.text(cx, cy + 15, sysd["detail"], "mono", 10, t["on_signal"], "middle"))


def build_one(p, idx):
    def build(t: dict) -> SVG:
        sysd = p["system"]
        s = SVG(W, H, t, f'{p["title"]}: {p["subtitle"]}',
                f'{p["summary"]} Stack: {", ".join(p["stack"])}. {p["credit"]}. '
                f'System: {", ".join(sysd["inputs"])} into {sysd["core"]} ({sysd["detail"]}), '
                f'out to {", ".join(sysd["outputs"])}.')
        panel(s, r=20)
        _diagram(s, t, sysd, idx)

        y = 248
        s.add(label(s, 26, y, f'{p["category"]}  ·  {p["context"]}', t["accent"], size=10.5))
        s.add(s.text(26, y + 36, p["title"], "semi", 28, t["ink"], tracking=-0.03))
        tw = measure(p["title"], "semi", 28, -0.03)
        sub = p["subtitle"]
        if tw + measure(sub, "serif", 19) + 40 < W - 40:
            s.add(s.text(26 + tw + 10, y + 36, sub, "serif", 19, t["ink3"]))
        ly = y + 64
        for ln in wrap(p["summary"], "sans", 14.5, W - 52)[:3]:
            s.add(s.text(26, ly, ln, "sans", 14.5, t["ink2"]))
            ly += 21
        x, py = 26, 380
        for tag in p["stack"]:
            tw = measure(tag, "mono", 10.5) + 18
            if x + tw > W - 26:
                break
            x += pill(s, x, py, tag, size=10.5, h=22, pad=9) + 6
        s.add(f'<path d="M16 {H - 40}H{W - 16}" stroke="{t["line"]}"/>')
        s.add(label(s, 26, H - 17, p["credit"], size=10.5))
        s.add(label(s, W - 26, H - 17, "Case study  →", t["accent"], size=10.5, anchor="end"))
        return s

    return build
