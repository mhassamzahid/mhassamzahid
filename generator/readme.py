"""Write README.md from profile.py so the text and the images never drift apart."""

from pathlib import Path

from . import profile as P
from .components import section

ROOT = Path(__file__).resolve().parent.parent


def pic(name: str, alt: str, width: str | None = "100%") -> str:
    size = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<img alt="{alt}" src="assets/{name}-light.svg"{size}></picture>')


def link(href: str, inner: str) -> str:
    return f'<a href="{href}">{inner}</a>'


def header(key: str) -> str:
    num, lab, (a, b, c) = section.SECTIONS[key]
    return f'<p>{pic(f"section-{key}", f"{num} · {lab}: {a}{b}{c}")}</p>'


def build() -> str:
    out = []
    w = out.append
    w("<!--\n  This README is generated. Edit generator/profile.py, then run: python -m generator.build\n"
      "  Images are hand-built SVGs (generator/components) with embedded font subsets,\n"
      "  rebuilt daily by .github/workflows/profile.yml.\n-->\n")
    w(f'<p>{link(P.SITE, pic("hero", f"{P.NAME_FIRST} {P.NAME_LAST} — {P.ROLE}. " + "".join(P.THESIS)))}</p>\n')
    w('<p align="center">'
      + link(f"mailto:{P.EMAIL}", pic("btn-email", "Email me", None)) + "&nbsp;"
      + link(P.CV_URL, pic("btn-cv", "Download CV", None)) + "&nbsp;"
      + link(P.SITE, pic("btn-site", "Portfolio", None)) + "</p>\n")
    w(f'<p>{pic("trace", "Agent trace: an LLM agent screens this profile with tool calls; every result is quoted from the CV.")}</p>\n')

    w("<div align=\"center\">\n")
    w("| At a glance | |\n|:--|:--|")
    w(f"| **Looking for** | {P.ROLE} roles building LLM-powered products |")
    w(f"| **Now** | {P.CURRENT['role']} @ {P.CURRENT['company']} · Sep 2025 – present |")
    w(f"| **Core** | RAG · LLM agents · MCP · ElevenLabs voice agents · n8n · FastAPI · Next.js · AWS |")
    w(f"| **Education** | {P.EDUCATION['degree']}, {P.EDUCATION['school']} · {P.EDUCATION['period']} |")
    w(f"| **Based** | {P.LOCATION} · {P.UTC_OFFSET} |")
    w(f"| **Reach me** | [{P.EMAIL}](mailto:{P.EMAIL}) · [CV (PDF)]({P.CV_URL}) · [{P.SITE_LABEL}]({P.SITE}) |")
    w("\n</div>\n")

    w(header("impact"))
    w(f'<p>{pic("metrics", "; ".join(m["value"] + " " + m["label"] for m in P.METRICS))}</p>\n')

    w(header("work"))
    for i in range(0, len(P.PROJECTS), 2):
        row = []
        for p in P.PROJECTS[i:i + 2]:
            alt = f'{p["title"]} — {p["subtitle"]}. {p["summary"]} ({p["credit"]})'
            row.append(link(f'{P.SITE}/work/{p["slug"]}', pic(f'cards/{p["slug"]}', alt, "49%")))
        w('<p align="center">\n' + "\n".join(row) + "\n</p>\n")
    w("<details>\n<summary><b>More work</b> — backends, scrapers, automations</summary>\n<br>\n")
    w("| Project | What it does | Stack | |\n|:--|:--|:--|:--|")
    for name, what, stack, href, kind in P.ARCHIVE:
        w(f"| **{name}** | {what} | <sub>{stack}</sub> | [{kind} ↗]({href}) |")
    w(f"\n<sub>Full case studies, with architecture diagrams, at [{P.SITE_LABEL}/work]({P.SITE}/work). "
      "Team projects list only the parts I built.</sub>\n\n</details>\n")

    w(header("stack"))
    w(f'<p>{pic("stack", "Skills as a periodic table: " + "; ".join(g + ": " + ", ".join(n for _, n in items) for g, items in P.SKILL_GROUPS))}</p>\n')

    w(header("path"))
    w(f'<p>{pic("timeline", "Career timeline: BS Software Engineering 2022 – Feb 2026 (graduated); final year project 2025; Python Developer at Axioware Solutions since Sep 2025.")}</p>\n')
    for e in P.EXPERIENCE:
        w(f"**{e['role']} · {e['company']}** &nbsp;<sub>{e['location']} · {e['period']}</sub>\n")
        for h in e["highlights"]:
            w(f"- {h}")
        w("")
    w(f"**{P.EDUCATION['degree']} · {P.EDUCATION['school']}** &nbsp;<sub>{P.EDUCATION['period']}</sub>\n")
    w(f"- Final year project — {P.EDUCATION['fyp']}. [Live ↗](https://usamania-university.vercel.app)\n")

    w(header("principles"))
    w(f'<p>{pic("principles", " ".join(f"{a} {b}: {c}" for a, b, c in P.HOW_I_WORK))}</p>\n')

    w(header("telemetry"))
    w(f'<p>{pic("telemetry", "Live GitHub telemetry: contribution grid, streaks and languages, rebuilt daily.")}</p>\n')

    w(f'<p>{link(f"mailto:{P.EMAIL}", pic("footer", f"Let us build something that ships. {P.EMAIL}"))}</p>\n')
    return "\n".join(out) + "\n"


def write() -> None:
    (ROOT / "README.md").write_text(build(), encoding="utf-8")
    print("  README.md")
