"""Render every profile image in both themes into assets/.

    python -m generator.build            # everything
    python -m generator.build hero cards # just some components
"""

import sys
import time
from pathlib import Path

from .theme import THEMES

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def targets():
    from . import profile
    from .components import cards, extras, hero, metrics, section, stack, telemetry, timeline, trace
    yield "hero", hero.build
    yield "trace", trace.build
    yield "metrics", metrics.build
    for key in section.SECTIONS:
        yield f"section-{key}", section.build_one(key)
    for i, p in enumerate(profile.PROJECTS):
        yield f"cards/{p['slug']}", cards.build_one(p, i)
    yield "stack", stack.build
    yield "timeline", timeline.build
    yield "principles", extras.principles
    yield "telemetry", telemetry.build
    yield "footer", extras.footer
    yield "btn-email", extras.button("Email me", "primary")
    yield "btn-cv", extras.button("Download CV", "outline")
    yield "btn-site", extras.button("Portfolio", "outline")


def main(only=None):
    ASSETS.mkdir(exist_ok=True)
    for name, fn in targets():
        if only and not any(name.startswith(o) for o in only):
            continue
        for theme in THEMES.values():
            t0 = time.time()
            out = ASSETS / f"{name}-{theme['name']}.svg"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(fn(theme).render(), encoding="utf-8")
            print(f"  {out.relative_to(ROOT)}  {out.stat().st_size / 1024:6.1f} KB  {time.time() - t0:.2f}s")
    if not only:
        from . import readme
        readme.write()


if __name__ == "__main__":
    main(sys.argv[1:] or None)
