"""Agent trace: an LLM agent screening a candidate, typed out as a tool-call log.

Every value a tool "returns" is a fact from the CV or the portfolio.
"""

from .. import profile as P
from ..svgkit import SVG, fmt, label, measure, panel

W = 1000
LH = 30
TOP = 92


def lines():
    m = {x["glyph"]: x["value"] for x in P.METRICS}
    featured = " · ".join(p["title"].replace("AI Sales Call Analysis", "Sales Call AI") for p in P.PROJECTS)
    return [
        ("user", "Find me an engineer who can ship an AI agent to production."),
        ("think", "Needs retrieval, tool use, voice and the backend to run it. Checking sources."),
        ("tool", f'github.profile(handle="{P.HANDLE}")'),
        ("result", f'{{ role: "{P.ROLE}", based: "{P.LOCATION}", status: "open to roles" }}'),
        ("tool", f'cv.experience(company="{P.CURRENT["company"]}")'),
        ("result", f'{m["nodes"]} n8n workflows · {m["shrink"]} less manual ops · {m["dots"]} pipeline accuracy'),
        ("tool", "portfolio.case_studies(featured=True)"),
        ("result", featured),
        ("tool", 'stack.query(domain="ai")'),
        ("result", "RAG · pgvector · MCP · ElevenLabs · FastAPI · Next.js · AWS"),
        ("agent", f"Strong match. Next step: {P.EMAIL}"),
    ]


KIND = {  # tag, typing speed (chars/s), pause after (s)
    "user": ("USER", 38, 0.45),
    "think": ("THINK", 70, 0.35),
    "tool": ("TOOL", 60, 0.25),
    "result": ("RESULT", 260, 0.35),
    "agent": ("AGENT", 34, 0.0),
}


def build(t: dict) -> SVG:
    L = lines()
    H = TOP + LH * len(L) + 70
    s = SVG(W, H, t, "Agent trace: screening Hassam Zahid",
            " ".join(f"{k}: {v}." for k, v in L))
    s.style("@keyframes cur{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:cur 1s steps(1) infinite}")
    panel(s, fill=t["bg_sunk"], grid=False, r=18)

    # window chrome
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        s.add(f'<circle cx="{30 + i * 20}" cy="30" r="6" fill="{c}" opacity=".85"/>')
    s.add(s.text(W / 2, 35, "agent-trace — screening.log", "mono", 13, t["ink3"], "middle"))
    s.add(label(s, W - 30, 35, "tools: github · cv · portfolio", anchor="end", size=11))
    s.add(f'<path d="M0 58H{W}" stroke="{t["line"]}"/>')

    colors = {"user": t["ink"], "think": t["ink3"], "tool": t["accent"], "result": t["ink2"],
              "agent": t["on_signal"]}
    clock = 0.6
    y = TOP
    for kind, text in L:
        tag, cps, pause = KIND[kind]
        dur = max(len(text) / cps, 0.18)
        tw = measure(text, "mono", 14) + 16
        cid = s.uid("ln")
        x0 = 196
        s.defn(f'<clipPath id="{cid}"><rect x="{x0 - 8}" y="{y - 20}" height="{LH}" width="0">'
               f'<animate attributeName="width" from="0" to="{fmt(tw + 8)}" begin="{clock:.2f}s" '
               f'dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
        # timestamp + tag appear when the line starts
        vis = (f'<set attributeName="opacity" to="1" begin="{clock:.2f}s" fill="freeze"/>')
        s.add(f'<g opacity="0">{vis}'
              f'{s.text(30, y, f"{clock:05.2f}s", "mono", 12, t["ink4"])}'
              f'{s.text(100, y, tag, "mono", 11, t["accent"] if kind in ("tool", "agent") else t["ink3"], tracking=0.08)}'
              f'</g>')
        if kind == "agent":
            s.add(f'<g clip-path="url(#{cid})"><rect x="{x0 - 8}" y="{y - 18}" width="{fmt(tw)}" height="26" '
                  f'rx="6" fill="{t["signal"]}"/>'
                  f'{s.text(x0, y, text, "mono", 14, colors[kind])}</g>')
        else:
            prefix = {"tool": "→ ", "result": "← ", "user": "› ", "think": "… "}[kind]
            body = s.runs(x0, y, [(prefix, "mono", t["ink4"]), (text, "mono", colors[kind])], 14)
            s.add(f'<g clip-path="url(#{cid})">{body}</g>')
        clock += dur + pause
        last_y, last_w = y, tw
        y += LH + (8 if kind == "result" else 0)

    # blinking cursor after the final answer
    s.add(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{clock:.2f}s" fill="freeze"/>'
          f'<rect class="cur" x="{fmt(196 + last_w)}" y="{last_y - 15}" width="9" height="19" fill="{t["ink"]}"/></g>')

    # footer
    fy = H - 26
    s.add(f'<path d="M0 {fy - 22}H{W}" stroke="{t["line"]}"/>')
    n_tools = sum(1 for k, _ in L if k == "tool")
    s.add(label(s, 30, fy, f"{len(L)} steps · {n_tools} tool calls", size=11))
    s.add(label(s, W - 30, fy, "every value returned is quoted from the CV", anchor="end", size=11))
    return s
