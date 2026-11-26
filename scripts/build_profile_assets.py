#!/usr/bin/env python3
"""Generate the static SVG assets used by the GitHub profile README (v3).

Every file in profile-assets/v3/ is produced by this script, so translations
and colours live in one place instead of being edited by hand in 20 SVGs.

    python scripts/build_profile_assets.py          # (re)write the assets
    python scripts/build_profile_assets.py --check  # fail if they are stale

Standard library only. The SVGs are static (CSS/SMIL animation at most):
no scripts, no event handlers, no external fonts, links or images, which is
what GitHub (camo + <img>) can render safely.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "profile-assets" / "v3"

# --- Design tokens ---------------------------------------------------------
PINK, VIOLET, CYAN = "#C75C8A", "#A78BFA", "#67E8F9"
INK, PANEL, SOFT_WHITE = "#0D1117", "#161B22", "#F0F6FC"

THEMES = {
    "dark": {
        "text": SOFT_WHITE, "muted": "#8B949E", "panel": PANEL, "panel_edge": "#30363D",
        "pink": PINK, "violet": VIOLET, "cyan": CYAN,
    },
    # Darker accents on light backgrounds so text keeps >= 4.5:1 contrast.
    "light": {
        "text": "#1F2328", "muted": "#59636E", "panel": "#F6F8FA", "panel_edge": "#D1D9E0",
        "pink": "#B0466F", "violet": "#7C3AED", "cyan": "#0E7490",
    },
}

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

# --- Copy (keep in sync with the three READMEs) ----------------------------
TAGLINES = {
    "es": ["Backend con Python · Django · PostgreSQL",
           "IA aplicada con LLMs · RAG · Ollama",
           "Escritorio con Tauri · Rust · React"],
    "en": ["Backend with Python · Django · PostgreSQL",
           "Applied AI with LLMs · RAG · Ollama",
           "Desktop apps with Tauri · Rust · React"],
    "pt": ["Backend com Python · Django · PostgreSQL",
           "IA aplicada com LLMs · RAG · Ollama",
           "Desktop com Tauri · Rust · React"],
}

WORKFLOW = {
    "es": ["ENTENDER", "DISEÑAR", "CONSTRUIR", "VALIDAR", "DESPLEGAR", "MEJORAR"],
    "en": ["UNDERSTAND", "DESIGN", "BUILD", "VALIDATE", "DEPLOY", "IMPROVE"],
    "pt": ["ENTENDER", "PROJETAR", "CONSTRUIR", "VALIDAR", "PUBLICAR", "MELHORAR"],
}
WORKFLOW_HINT = {
    "es": ["problema y flujo real", "simple y verificable", "incremental", "pruebas y datos",
           "dev ≠ producción", "documentar y evolucionar"],
    "en": ["real problem & workflow", "simple & verifiable", "incremental", "tests & data",
           "dev ≠ production", "document & evolve"],
    "pt": ["problema e fluxo real", "simples e verificável", "incremental", "testes e dados",
           "dev ≠ produção", "documentar e evoluir"],
}
WORKFLOW_TITLE = {
    "es": "Flujo de desarrollo de Sergio Carey",
    "en": "Sergio Carey's development workflow",
    "pt": "Fluxo de desenvolvimento de Sergio Carey",
}

# Section chips are language-neutral (terminal paths), shared by all READMEs.
CHIPS = ["whoami", "stack", "projects", "learning", "activity", "workflow", "offline", "contact"]


def gradient(id_: str, c1: str, c2: str, c3: str) -> str:
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset=".5" stop-color="{c2}"/>'
            f'<stop offset="1" stop-color="{c3}"/></linearGradient>')


def svg(w: int, h: int, body: str, title: str, extra_attrs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"{extra_attrs}>'
            f'<title>{escape(title)}</title>{body}</svg>\n')


# --- 1. Section chip: "● 01  ~/whoami" ------------------------------------
def chip(index: int, name: str) -> str:
    label = f"~/{name}"
    char_w = 7.8  # 13px monospace
    text_w = round(len(label) * char_w)
    w = 16 + 8 + 22 + 10 + text_w + 14
    h = 28
    body = (
        f"<defs>{gradient('g', PINK, VIOLET, CYAN)}</defs>"
        f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="8" fill="{INK}" stroke="url(#g)" stroke-width="1.5"/>'
        f'<circle cx="16" cy="14" r="4" fill="{PINK}"/>'
        f'<circle cx="16" cy="14" r="7" fill="{PINK}" opacity=".18"/>'
        f'<text x="28" y="18.5" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}">{index:02d}</text>'
        f'<text x="56" y="18.5" font-family="{MONO}" font-size="13" fill="{SOFT_WHITE}" '
        f'textLength="{text_w}" lengthAdjust="spacingAndGlyphs">{escape(label)}</text>'
    )
    return svg(w, h, body, f"Section {index:02d}: {label}")


# --- 2. Typing tagline (SMIL, loops forever) --------------------------------
def typing(lang: str, theme: str) -> str:
    t = THEMES[theme]
    lines = TAGLINES[lang]
    W, H, fs = 640, 40, 17
    char_w = fs * 0.6
    slot, type_s, erase_s = 4.0, 1.6, 0.5
    total = slot * len(lines)
    parts = [f"<defs>{gradient('g', t['pink'], t['violet'], t['cyan'])}"]
    texts = []
    for i, line in enumerate(lines):
        full = "> " + line
        tw = round(len(full) * char_w)
        x0 = round((W - tw) / 2)
        n = len(full)
        # discrete key frames: typing steps, hold, erase, hidden
        start = i * slot
        times, widths = [0.0], [0]
        if start > 0:
            times.append(start / total); widths.append(0)
        for k in range(1, n + 1):
            times.append((start + type_s * k / n) / total); widths.append(round(tw * k / n) + 2)
        hold_end = start + slot - erase_s
        times.append(hold_end / total); widths.append(tw + 2)
        times.append((start + slot - 0.05) / total); widths.append(0)
        if times[-1] < 1:
            times.append(1.0); widths.append(0)
        end = (start + slot - 0.05) / total
        if start == 0:
            cur_kt, cur_vals = f"0;{end:.4f}", "1;0"
        else:
            cur_kt, cur_vals = f"0;{start / total:.4f};{end:.4f}", "0;1;0"
        kt = ";".join(f"{x:.4f}" for x in times)
        vals = ";".join(str(v) for v in widths)
        cur_x = ";".join(str(x0 + v) for v in widths)
        parts.append(
            f'<clipPath id="c{i}"><rect x="{x0}" y="0" width="0" height="{H}">'
            f'<animate attributeName="width" dur="{total}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>'
            f"</rect></clipPath>"
        )
        texts.append(
            f'<g clip-path="url(#c{i})"><text x="{x0}" y="26" font-family="{MONO}" font-size="{fs}" '
            f'textLength="{tw}" lengthAdjust="spacingAndGlyphs" fill="{t["text"]}">'
            f'<tspan fill="{t["pink"]}" font-weight="700">&gt;</tspan> {escape(line)}</text></g>'
            f'<rect y="10" width="9" height="20" rx="1.5" fill="url(#g)" opacity="0">'
            f'<animate attributeName="x" dur="{total}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{cur_x}"/>'
            f'<animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{cur_kt}" values="{cur_vals}"/>'
            f"</rect>"
        )
    parts.append("</defs>")
    body = "".join(parts) + "".join(texts)
    return svg(W, H, body, " · ".join(lines))


# --- 3. Workflow diagram (2 columns x 3 rows, mobile friendly) -------------
def workflow(lang: str, theme: str) -> str:
    t = THEMES[theme]
    steps, hints = WORKFLOW[lang], WORKFLOW_HINT[lang]
    W, H = 440, 336
    nw, nh, gx, top, gy = 190, 84, 28, 8, 30
    x_cols = [(W - 2 * nw - gx) / 2, (W - 2 * nw - gx) / 2 + nw + gx]
    defs = (f"<defs>{gradient('g', t['pink'], t['violet'], t['cyan'])}"
            f'<marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{t["violet"]}"/></marker></defs>')
    accents = [t["pink"], t["pink"], t["violet"], t["violet"], t["cyan"], t["cyan"]]
    nodes, links = [], []
    pos = []
    for i in range(6):
        r, c = divmod(i, 2)
        x, y = x_cols[c], top + r * (nh + gy)
        pos.append((x, y))
        nodes.append(
            f'<g><rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="14" fill="{t["panel"]}" stroke="url(#g)" stroke-width="1.6"/>'
            f'<rect x="{x + 14}" y="{y + 14}" width="30" height="20" rx="6" fill="{accents[i]}" opacity=".16"/>'
            f'<text x="{x + 29}" y="{y + 28.5}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{accents[i]}">{i + 1:02d}</text>'
            f'<text x="{x + 16}" y="{y + 58}" font-family="{SANS}" font-size="19" font-weight="800" letter-spacing=".4" fill="{t["text"]}">{escape(steps[i])}</text>'
            f'<text x="{x + 16}" y="{y + 75}" font-family="{SANS}" font-size="12.5" fill="{t["muted"]}">{escape(hints[i])}</text>'
            + (f'<text x="{x + nw - 16}" y="{y + 29}" text-anchor="end" font-family="{SANS}" font-size="16" fill="{t["cyan"]}">↻</text>' if i == 5 else "")
            + "</g>"
        )
    for i in range(5):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if i % 2 == 0:  # left -> right in the same row
            links.append(f'<path d="M{x1 + nw + 3} {y1 + nh / 2} H{x2 - 4}" stroke="{t["violet"]}" stroke-width="2" fill="none" marker-end="url(#a)"/>')
        else:  # right column -> next row, left column
            mid = y1 + nh + gy / 2
            links.append(f'<path d="M{x1 + nw / 2} {y1 + nh + 2} V{mid} H{x2 + nw / 2} V{y2 - 4}" stroke="{t["violet"]}" '
                         f'stroke-width="2" stroke-dasharray="4 4" fill="none" stroke-linejoin="round" marker-end="url(#a)"/>')
    body = defs + "".join(links) + "".join(nodes)
    title = WORKFLOW_TITLE[lang] + ": " + " → ".join(steps)
    return svg(W, H, body, title)


def build() -> dict[Path, str]:
    files: dict[Path, str] = {}
    for i, name in enumerate(CHIPS, 1):
        files[OUT / f"chip-{i:02d}-{name}.svg"] = chip(i, name)
    for lang in TAGLINES:
        for theme in THEMES:
            files[OUT / f"tagline-{lang}-{theme}.svg"] = typing(lang, theme)
            files[OUT / f"workflow-{lang}-{theme}.svg"] = workflow(lang, theme)
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if generated files differ from disk")
    args = ap.parse_args()
    files = build()
    stale = []
    for path, content in files.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if args.check:
        if stale:
            print("Stale generated assets (run scripts/build_profile_assets.py):", *stale, sep="\n  ")
            return 1
        print(f"OK: {len(files)} generated assets are up to date")
    else:
        print(f"Wrote {len(files)} files to {OUT.relative_to(ROOT).as_posix()}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
