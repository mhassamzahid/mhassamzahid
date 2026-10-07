"""Principles, footer and CTA buttons."""

import math

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel, wrap, wrap_runs


def principles(t: dict) -> SVG:
    W, H = 1000, 236
    s = SVG(W, H, t, "How I work",
            " ".join(f"{a} {b}. {c}" for a, b, c in P.HOW_I_WORK))
    s.style("@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
            ".up{animation:up .7s cubic-bezier(.2,.8,.2,1) both}")
    panel(s)
    col = W / 3
    for i, (a, b, body) in enumerate(P.HOW_I_WORK):
        x = i * col + 28
        if i:
            s.add(f'<path d="M{fmt(i * col)} 24V{H - 24}" stroke="{t["line"]}"/>')
        g = [f'<g class="up" style="animation-delay:{.15 + i * .15:.2f}s">',
             label(s, x, 44, f"rule {i + 1:02d}", t["accent"], size=10.5)]
        y = 80
        for ln in wrap_runs([(a + " ", "semi", t["ink"]), (b, "serif", t["ink"])], 23, col - 56):
            g.append(s.runs(x, y, ln, 23, tracking=-0.02))
            y += 27
        y += 8
        for ln in wrap(body, "sans", 14, col - 56):
            g.append(s.text(x, y, ln, "sans", 14, t["ink2"]))
            y += 21
        g.append("</g>")
        s.add("".join(g))
    return s


def footer(t: dict) -> SVG:
    W, H = 1000, 320
    s = SVG(W, H, t, "Contact", f"Let's build something that ships. Email {P.EMAIL}. Portfolio {P.SITE_LABEL}.")
    panel(s, glow=(W * .78, H * .5, 300))
    # oscilloscope traces, right half
    mask, fade = s.uid("m"), s.uid("f")
    s.defn(f'<linearGradient id="{fade}" x1="0" x2="1"><stop offset=".35" stop-color="#fff" stop-opacity="0"/>'
           f'<stop offset=".75" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity=".6"/></linearGradient>'
           f'<mask id="{mask}"><rect width="{W}" height="{H}" fill="url(#{fade})"/></mask>')
    s.add(f'<g mask="url(#{mask})">')
    for k, (amp, wl, op, dur) in enumerate([(46, 220, .9, 5), (28, 140, .45, 3.6), (64, 330, .25, 7.5)]):
        pts = []
        for i in range(0, W + 2 * wl + 10, 6):
            env = 1 if k else 0.85 + 0.15 * math.sin(i / 90)
            pts.append(f"{i - wl * 2} {H / 2 + amp * env * math.sin(2 * math.pi * i / wl + k):.1f}")
        col = t["pulse"] if k == 0 else t["ink3"]
        s.add(f'<path d="M{"L".join(pts)}" stroke="{col}" stroke-opacity="{op}" stroke-width="{1.6 if k == 0 else 1}">'
              f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{wl} 0" dur="{dur}s" '
              f'repeatCount="indefinite"/></path>')
    s.add("</g>")

    s.add(label(s, 40, 62, "(07)  Contact", t["accent"]))
    y = 116
    for ln in wrap_runs([("Let's build something ", "semi", t["ink"]), ("that ships", "serif", t["ink"]),
                         (".", "semi", t["ink"])], 50, 520):
        s.add(s.runs(40, y, ln, 50, tracking=-0.035))
        y += 56
    y += 14
    s.add(s.text(40, y, P.EMAIL, "mono", 20, t["accent"]))
    s.add(f'<path d="M40 {y + 9}H{40 + measure(P.EMAIL, "mono", 20):.0f}" stroke="{t["accent"]}" stroke-opacity=".5"/>')
    s.add(label(s, 40, H - 34, f"{P.LOCATION} · {P.UTC_OFFSET}  ·  {P.SITE_LABEL}", size=11))
    return s


def button(text, kind):
    def build(t: dict) -> SVG:
        size = 15
        w = int(measure(text, "semi", size) + 30 + 34)
        s = SVG(w, 56, t, text)
        if kind == "primary":
            s.add(f'<rect x="1" y="4" width="{w - 2}" height="48" rx="24" fill="{t["signal"]}"/>')
            ink = t["on_signal"]
        else:
            s.add(f'<rect x="1.5" y="4.5" width="{w - 3}" height="47" rx="23.5" stroke="{t["line_strong"]}" '
                  f'fill="{t["bg_raised"]}"/>')
            ink = t["ink"]
        s.add(s.text(26, 33.5, text, "semi", size, ink, tracking=-0.01))
        ax = w - 30
        s.add(f'<path d="M{ax - 6} 28H{ax + 6}M{ax + 1} 23l5 5-5 5" stroke="{ink}" stroke-width="1.8" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')
        return s
    return build
