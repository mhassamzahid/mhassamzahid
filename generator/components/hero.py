"""Hero: status bar, thesis, and the integrations orbiting an agent core.

The picture is the CV's one-line story drawn literally: scattered business tools
(the real integrations) send signal into a single agent.
"""

import math

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel, pill, wrap, wrap_runs

W, H = 1000, 628
CX, CY = 785, 222


def _orbit_nodes(names, rx, ry, phase):
    out = []
    for i, n in enumerate(names):
        a = phase + 2 * math.pi * i / len(names)
        out.append((n, CX + rx * math.cos(a), CY + ry * math.sin(a)))
    return out


def build(t: dict) -> SVG:
    s = SVG(W, H, t, f"{P.NAME_FIRST} {P.NAME_LAST}, {P.ROLE}",
            f"{P.AVAILABILITY}. {P.LOCATION}. {''.join(P.THESIS)} {P.TAGLINE} "
            f"Diagram: {', '.join(P.ORBIT_OUTER + P.ORBIT_INNER)} feeding one agent core.")
    s.style(
        "@keyframes rise{from{transform:translateY(110px);opacity:0}to{transform:none;opacity:1}}"
        ".ch{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}"
        "@keyframes fadein{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
        ".fi{animation:fadein .8s ease-out both}"
        "@keyframes beat{0%{opacity:.9}70%,100%{opacity:0}}"
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:.35}}"
        ".live{animation:blink 2s ease-in-out infinite}"
        "@keyframes pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}"
        ".node{transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.2,.8,.2,1) both}"
    )
    panel(s, glow=(CX, CY, 330))

    # -- status bar ---------------------------------------------------------
    s.add(f'<circle cx="46" cy="44" r="4" fill="{t["signal"]}" class="live"/>')
    s.add(f'<circle cx="46" cy="44" r="4" fill="none" stroke="{t["signal"]}" class="motion">'
          f'<animate attributeName="r" values="4;12" dur="2s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>')
    s.add(label(s, 60, 48, P.AVAILABILITY, t["ink"]))
    mid = f'{P.CURRENT["role"]} @ {P.CURRENT["company"]}'
    s.add(label(s, W / 2 + 40, 48, mid, anchor="middle"))
    s.add(label(s, W - 40, 48, f"{P.LOCATION} · {P.UTC_OFFSET}", anchor="end"))
    s.add(f'<path d="M24 70H{W - 24}" stroke="{t["line"]}"/>')

    # -- thesis ------------------------------------------------------------
    s.add(f'<g class="fi" style="animation-delay:.15s">{label(s, 40, 118, "(00)  " + P.ROLE, t["accent"])}</g>')
    a, b, c = P.THESIS
    lines = wrap_runs([(a, "semi", t["ink"]), (b, "serif", t["ink"]), (c, "semi", t["ink"])], 42, 520)
    y = 170
    for i, ln in enumerate(lines):
        s.add(f'<g class="fi" style="animation-delay:{.25 + i * .08:.2f}s">'
              f'{s.runs(40, y, ln, 42, tracking=-0.035)}</g>')
        y += 48
    y += 6
    for i, ln in enumerate(wrap(P.TAGLINE, "sans", 16, 500)):
        s.add(f'<g class="fi" style="animation-delay:{.5 + i * .05:.2f}s">'
              f'{s.text(40, y, ln, "sans", 16, t["ink2"])}</g>')
        y += 25
    x, y = 40, y + 10
    s.add(f'<g class="fi" style="animation-delay:.75s">')
    for tag in P.HERO_TAGS:
        x += pill(s, x, y, tag, size=11, upper=True, color=t["ink2"]) + 8
    s.add("</g>")

    # -- orbit graph ---------------------------------------------------------
    rings = [(96, 78, "inner"), (190, 140, "outer")]
    for rx, ry, _ in rings:
        s.add(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" stroke="{t["line_strong"]}" '
              f'stroke-dasharray="2 6"><animate attributeName="stroke-dashoffset" from="0" to="-64" '
              f'dur="6s" repeatCount="indefinite"/></ellipse>')
    nodes = _orbit_nodes(P.ORBIT_INNER, 96, 78, -math.pi / 4) + \
        _orbit_nodes(P.ORBIT_OUTER, 190, 140, -math.pi / 2 + math.pi / 8)

    # spokes + pulses into the core
    for i, (n, x, y) in enumerate(nodes):
        pid = s.uid("sp")
        s.defn(f'<path id="{pid}" d="M{fmt(x)} {fmt(y)}L{CX} {CY}"/>')
        s.add(f'<path d="M{fmt(x)} {fmt(y)}L{CX} {CY}" stroke="{t["line"]}"/>')
        dur = 2.2 + (i % 3) * 0.35
        s.add(f'<circle r="2.6" fill="{t["pulse"]}" class="motion" opacity="0">'
              f'<animateMotion dur="{dur:.2f}s" begin="{1.2 + i * 0.37:.2f}s" repeatCount="indefinite" '
              f'keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".5 0 .9 .6">'
              f'<mpath xlink:href="#{pid}"/></animateMotion>'
              f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="{dur:.2f}s" '
              f'begin="{1.2 + i * 0.37:.2f}s" repeatCount="indefinite"/></circle>')

    # core
    s.add(f'<circle cx="{CX}" cy="{CY}" r="38" fill="{t["signal"]}" opacity=".18" class="motion">'
          f'<animate attributeName="r" values="38;64" dur="2.4s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".35;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    s.add(f'<circle cx="{CX}" cy="{CY}" r="38" fill="{t["signal"]}"/>')
    s.add(s.text(CX, CY - 2, "AGENT", "mono", 12, t["on_signal"], "middle", 0.08))
    s.add(s.text(CX, CY + 13, "one workflow", "serif", 13, t["on_signal"], "middle"))

    # tool nodes
    for i, (n, x, y) in enumerate(nodes):
        w = measure(n, "mono", 11) + 18
        s.add(f'<g class="node" style="animation-delay:{.4 + i * .06:.2f}s">'
              f'<rect x="{fmt(x - w / 2)}" y="{fmt(y - 12)}" width="{fmt(w)}" height="24" rx="12" '
              f'fill="{t["bg_raised"]}" stroke="{t["line_strong"]}"/>'
              f'{s.text(x, y + 4, n, "mono", 11, t["ink2"], "middle")}</g>')

    # -- billboard name ----------------------------------------------------------
    base = 588
    size = 150
    gap = 0.22 * size
    w_first = measure(P.NAME_FIRST, "semi", size, -0.065)
    w_last = measure(P.NAME_LAST, "serif", size * 1.08)
    total = w_first + gap + w_last
    if total > W - 80:
        size *= (W - 80) / total
        gap = 0.22 * size
    clip = s.uid("nm")
    s.defn(f'<clipPath id="{clip}"><rect x="0" y="{base - size}" width="{W}" height="{size + 40}"/></clipPath>')
    s.add(f'<g clip-path="url(#{clip})">')
    x = 34
    delay = 0.1
    for ch in P.NAME_FIRST:
        s.add(f'<g class="ch" style="animation-delay:{delay:.2f}s">'
              f'{s.text(x, base, ch, "semi", size, t["ink"])}</g>')
        x += measure(ch, "semi", size, -0.065)
        delay += 0.045
    x += gap
    for ch in P.NAME_LAST:
        s.add(f'<g class="ch" style="animation-delay:{delay:.2f}s">'
              f'{s.text(x, base, ch, "serif", size * 1.08, t["ink"])}</g>')
        x += measure(ch, "serif", size * 1.08)
        delay += 0.045
    s.add("</g>")
    # signal full stop
    s.add(f'<circle cx="{fmt(x + 14)}" cy="{base - 12}" r="11" fill="{t["signal"]}" class="ch" '
          f'style="animation-delay:{delay + .1:.2f}s"/>')
    return s
