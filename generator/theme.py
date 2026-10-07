"""Design tokens, mirrored from the portfolio's design contract ("Signal", v2).

One signal colour (electric lime) marks the live parts: the agent core, pulses,
the current role. Everything else is near-black / paper neutrals.
"""

THEMES = {
    "dark": {
        "name": "dark",
        "bg": "#08080a",
        "bg_raised": "#111114",
        "bg_sunk": "#0d0d10",
        "ink": "#f3f3ee",
        "ink2": "#b6b6bb",
        "ink3": "#8a8a93",
        "ink4": "#4a4a52",
        "line": "rgba(255,255,255,0.08)",
        "line_strong": "rgba(255,255,255,0.17)",
        "grid": "rgba(255,255,255,0.045)",
        "signal": "#c6f432",
        "on_signal": "#0c0c0d",
        "accent": "#c6f432",
        "pulse": "#c6f432",
        "glow": "#c6f432",
        "glow_opacity": 0.13,
        # single-hue ramp for heatmaps and bars: empty -> full signal
        "ramp": ["#16161a", "#2f3d12", "#56731c", "#8bb526", "#c6f432"],
    },
    "light": {
        "name": "light",
        "bg": "#f4f4ef",
        "bg_raised": "#fbfbf8",
        "bg_sunk": "#eaeae3",
        "ink": "#0c0c0d",
        "ink2": "#38383d",
        "ink3": "#64646b",
        "ink4": "#a6a6a0",
        "line": "rgba(12,12,13,0.10)",
        "line_strong": "rgba(12,12,13,0.20)",
        "grid": "rgba(12,12,13,0.05)",
        "signal": "#c6f432",
        "on_signal": "#0c0c0d",
        "accent": "#3d6b00",
        "pulse": "#5a8f00",
        "glow": "#9ccc0a",
        "glow_opacity": 0.18,
        "ramp": ["#e3e3db", "#d4ec8f", "#b5dc3c", "#7fa61a", "#3d6b00"],
    },
}
