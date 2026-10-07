"""Section headers: a mono index label, then a heading with one serif-italic phrase.

Transparent background so they sit directly on GitHub's page in either theme.
"""

from ..svgkit import SVG, label, measure

W, H = 1000, 112

SECTIONS = {
    "impact": ("01", "Impact", ("Every number is ", "on the record", "")),
    "work": ("02", "Selected work", ("Systems I've ", "shipped", "")),
    "stack": ("03", "Stack", ("The ", "periodic table", " I build with")),
    "path": ("04", "Path", ("Where I've ", "been", ", where I am")),
    "principles": ("05", "How I work", ("Three rules, ", "no exceptions", "")),
    "telemetry": ("06", "Telemetry", ("Live from ", "GitHub", ", rebuilt daily")),
}


def build_one(key):
    num, lab, (a, b, c) = SECTIONS[key]

    def build(t: dict) -> SVG:
        s = SVG(W, H, t, f"{lab}: {a}{b}{c}")
        s.style("@keyframes sl{from{opacity:0;transform:translateX(-16px)}to{opacity:1;transform:none}}"
                ".sl{animation:sl .8s cubic-bezier(.2,.8,.2,1) both}"
                "@keyframes grow{from{transform:scaleX(0)}to{transform:none}}"
                ".grow{transform-box:fill-box;transform-origin:left;animation:grow 1.4s .3s cubic-bezier(.6,0,.2,1) both}")
        s.add(f'<g class="sl">{label(s, 2, 30, f"({num})  {lab}", t["accent"])}</g>')
        size = 44
        runs = [(a, "semi", t["ink"]), (b, "serif", t["ink"]), (c, "semi", t["ink"])]
        runs = [r for r in runs if r[0]]
        s.add(f'<g class="sl" style="animation-delay:.08s">{s.runs(0, 84, runs, size, tracking=-0.03)}</g>')
        end = sum(measure(r[0], r[1], size, -0.03) for r in runs) + 24
        s.add(f'<path d="M{end:.0f} 72H{W}" stroke="{t["line_strong"]}" class="grow"/>')
        s.add(f'<circle cx="{W - 4}" cy="72" r="4" fill="{t["signal"]}"/>')
        return s

    return build
