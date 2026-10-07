"""Live telemetry from data/github.json: contribution grid, streaks, languages.

The grid is redrawn in the profile's single-hue ramp, and a signal scan sweeps
across it. With no snapshot yet, it renders an honest "awaiting first sync".
"""

import json
import os
from datetime import date, timedelta
from pathlib import Path

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel

DATA = Path(os.environ.get("PROFILE_DATA") or Path(__file__).resolve().parent.parent.parent / "data" / "github.json")
W, H = 1000, 316
GX, GY, STEP, CELL = 28, 84, 14, 11


def load():
    try:
        return json.loads(DATA.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    cur = 0
    seq = list(reversed(days))
    if seq and seq[0]["count"] == 0:  # today not over yet
        seq = seq[1:]
    for d in seq:
        if not d["count"]:
            break
        cur += 1
    return cur, longest


def build(t: dict) -> SVG:
    d = load()
    days = (d or {}).get("days") or []
    if days:
        cur, longest = streaks(days)
        stats = [(f'{d["total"]:,}', "contributions / yr"), (f"{longest}", "days, best streak"),
                 (f"{cur}", "days, current streak"), (f'{d["repos"]}', "public repos")]
        desc = "; ".join(f"{a} {b}" for a, b in stats)
    else:
        stats = [("—", "contributions / yr"), ("—", "days, best streak"),
                 ("—", "days, current streak"), ("—", "public repos")]
        desc = "Awaiting the first sync by the GitHub Actions workflow."
    s = SVG(W, H, t, "GitHub telemetry", desc)
    panel(s)

    # grid
    if days:
        first = date.fromisoformat(days[0]["date"])
        offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
        cells = [(i + offset, x) for i, x in enumerate(days)]
    else:
        end = date.today()
        start = end - timedelta(days=7 * 52 + (end.weekday() + 1) % 7)
        first, offset = start, 0
        cells = [(i, {"date": (start + timedelta(i)).isoformat(), "level": 0, "count": 0})
                 for i in range((end - start).days + 1)]
    weeks = cells[-1][0] // 7 + 1
    last_month = None
    out = []
    for pos, day in cells:
        wk, wd = divmod(pos, 7)
        x, y = GX + wk * STEP, GY + wd * STEP
        dt = date.fromisoformat(day["date"])
        if wd == 0 or pos == cells[0][0]:
            if dt.month != last_month and wk < weeks - 2:
                if last_month is not None or wd == 0:
                    out.append(label(s, x, GY - 12, dt.strftime("%b"), size=9.5))
                last_month = dt.month
        lvl = day["level"]
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{t["ramp"][lvl]}"/>')
    s.add("".join(out))
    grid_w = weeks * STEP

    # scan
    clip, grad = s.uid("c"), s.uid("g")
    s.defn(f'<clipPath id="{clip}"><rect x="{GX}" y="{GY}" width="{grid_w}" height="{7 * STEP}"/></clipPath>'
           f'<linearGradient id="{grad}" x1="0" x2="1"><stop offset="0" stop-color="{t["pulse"]}" stop-opacity="0"/>'
           f'<stop offset=".85" stop-color="{t["pulse"]}" stop-opacity=".28"/>'
           f'<stop offset="1" stop-color="{t["pulse"]}" stop-opacity=".9"/></linearGradient>')
    s.add(f'<g clip-path="url(#{clip})" class="motion"><rect x="{GX - 90}" y="{GY - 2}" width="90" height="{7 * STEP + 4}" '
          f'fill="url(#{grad})"><animateTransform attributeName="transform" type="translate" from="0 0" '
          f'to="{grid_w + 90} 0" dur="6s" repeatCount="indefinite"/></rect></g>')

    if not days:
        msg = "awaiting first sync  ·  .github/workflows/profile.yml"
        mw = measure(msg.upper(), "mono", 11, 0.06) + 32
        cx = GX + grid_w / 2
        s.add(f'<rect x="{fmt(cx - mw / 2)}" y="{GY + 7 * STEP / 2 - 16}" width="{fmt(mw)}" height="32" rx="16" '
              f'fill="{t["bg_raised"]}" stroke="{t["line_strong"]}"/>')
        s.add(label(s, cx, GY + 7 * STEP / 2 + 4, msg, anchor="middle", size=11))

    # legend
    ly = GY + 7 * STEP + 22
    s.add(label(s, GX, ly, f'synced {d["synced"].replace("T", " ")} UTC' if d else "rebuilt daily", size=10))
    lx = GX + grid_w - 5 * 14 - 34
    s.add(label(s, lx - 8, ly, "less", size=10, anchor="end"))
    for i, c in enumerate(t["ramp"]):
        s.add(f'<rect x="{lx + i * 14}" y="{ly - 10}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>')
    s.add(label(s, lx + 5 * 14 + 4, ly, "more", size=10))

    s.add(label(s, GX, 40, "contribution signal", size=11))
    s.add(label(s, W - 28, 40, f"@{P.HANDLE}", t["accent"],
                size=11, anchor="end"))

    # stats column
    sx = GX + grid_w + 34
    s.add(f'<path d="M{sx - 18} {GY - 12}V{ly}" stroke="{t["line"]}"/>')
    for i, (v, lab) in enumerate(stats):
        y = GY + 14 + i * 34
        s.add(s.text(sx, y, v, "semi", 20, t["ink"] if i else t["accent"], tracking=-0.03))
        vw = measure(v, "semi", 20, -0.03)
        s.add(s.text(sx + vw + 8, y, lab, "sans", 11.5, t["ink3"]))

    # languages
    by = ly + 30
    langs = (d or {}).get("languages") or []
    total = sum(x["bytes"] for x in langs) or 1
    top = langs[:5]
    rest = total - sum(x["bytes"] for x in top)
    segs = [(x["name"], x["bytes"]) for x in top] + ([("Other", rest)] if rest > 0 and langs else [])
    bw = W - 2 * GX
    s.add(label(s, GX, by, "languages · public repos, by bytes", size=10))
    if segs:
        x = GX
        ramp = list(reversed(t["ramp"][1:])) + [t["ink4"], t["ink4"]]
        for i, (name, b) in enumerate(segs):
            w = bw * b / total
            s.add(f'<rect x="{fmt(x)}" y="{by + 12}" width="{fmt(max(w - 3, 1))}" height="10" rx="3" fill="{ramp[i]}"/>')
            x += w
        x = GX
        for i, (name, b) in enumerate(segs):
            txt = f"{name} {100 * b / total:.1f}%"
            s.add(f'<circle cx="{fmt(x + 4)}" cy="{by + 40}" r="4" fill="{ramp[i]}"/>')
            s.add(s.text(x + 14, by + 44, txt, "mono", 11, t["ink2"]))
            x += measure(txt, "mono", 11) + 34
    else:
        s.add(f'<rect x="{GX}" y="{by + 12}" width="{bw}" height="10" rx="3" fill="{t["ramp"][0]}"/>')
    return s
