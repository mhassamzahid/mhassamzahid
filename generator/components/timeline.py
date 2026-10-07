"""Career timeline: lanes for degree, final year project and industry.

Year-precision lanes get soft ends; month-precision lanes get hard ends. The
"now" line is the build date, so the current role grows every day the
workflow runs.
"""

from datetime import date

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel

W, H = 1000, 286
X0, X1 = 250, 968
LANE_Y = 74
LANE_H = 52


def _months(ym: str) -> float:
    y, m = map(int, ym.split("-"))
    return y * 12 + (m - 1)


def build(t: dict) -> SVG:
    today = date.today()
    now = today.year * 12 + today.month - 1 + today.day / 31
    start = _months("2022-01")
    end = (today.year + 1) * 12 + 3
    sx = lambda m: X0 + (m - start) / (end - start) * (X1 - X0)  # noqa: E731

    s = SVG(W, H, t, "Career timeline",
            "; ".join(f'{x["lane"]}: {x["title"]}, {x["where"]}, from {x["start"][:4]}'
                      + (" to present" if x["end"] is None else f' to {x["end"][:4]}') for x in P.TIMELINE))
    s.style("@keyframes bar{from{transform:scaleX(0)}to{transform:none}}"
            ".bar{transform-box:fill-box;transform-origin:left;animation:bar 1.3s cubic-bezier(.6,0,.2,1) both}")
    panel(s)

    # years
    axis_y = LANE_Y + len(P.TIMELINE) * LANE_H + 14
    for yr in range(2022, today.year + 2):
        x = sx(yr * 12)
        if x > X1:
            break
        s.add(f'<path d="M{fmt(x)} {LANE_Y - 26}V{axis_y}" stroke="{t["line"]}"/>')
        s.add(label(s, x + 6, axis_y + 18, str(yr), size=10.5))

    for i, lane in enumerate(P.TIMELINE):
        y = LANE_Y + i * LANE_H
        s.add(label(s, 28, y + 2, lane["lane"], size=10))
        s.add(s.text(28, y + 22, lane["title"], "semi", 15, t["ink"], tracking=-0.01))
        a = sx(_months(lane["start"]))
        b = sx(now if lane["end"] is None else min(_months(lane["end"]) + 1, now))
        cur = lane.get("current")
        fill = t["signal"] if cur else t["ink4"]
        bh, by = 20, y - 2
        if lane["precision"] == "year":
            gid = s.uid("soft")
            s.defn(f'<linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{fill}" stop-opacity="0"/>'
                   f'<stop offset=".08" stop-color="{fill}"/><stop offset=".92" stop-color="{fill}"/>'
                   f'<stop offset="1" stop-color="{fill}" stop-opacity="0"/></linearGradient>')
            fill = f"url(#{gid})"
        s.add(f'<rect x="{fmt(a)}" y="{by}" width="{fmt(b - a)}" height="{bh}" rx="{bh / 2 if not cur else 4}" '
              f'fill="{fill}" class="bar" style="animation-delay:{.2 + i * .2:.1f}s"/>')
        inside = lane["where"]
        ink = t["on_signal"] if cur else t["ink"]
        if measure(inside, "mono", 10.5) + 24 < b - a:
            s.add(s.text(a + 12, by + 14, inside, "mono", 10.5, ink))
        else:
            s.add(s.text(b + 10, by + 14, inside, "mono", 10.5, t["ink3"]))

    # now line
    nx = sx(now)
    s.add(f'<path d="M{fmt(nx)} {LANE_Y - 30}V{axis_y}" stroke="{t["accent"]}" stroke-dasharray="3 4"/>')
    s.add(f'<circle cx="{fmt(nx)}" cy="{LANE_Y - 30}" r="4" fill="{t["accent"]}"/>'
          f'<circle cx="{fmt(nx)}" cy="{LANE_Y - 30}" r="4" stroke="{t["accent"]}" class="motion">'
          f'<animate attributeName="r" values="4;12" dur="2s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/></circle>')
    s.add(label(s, nx - 10, LANE_Y - 26, f"now · {today.strftime('%b %Y')}", t["accent"], size=10, anchor="end"))
    return s
