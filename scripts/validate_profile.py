#!/usr/bin/env python3
"""Lightweight checks for the GitHub profile README (standard library only).

    python scripts/validate_profile.py

1. Protected images (banner + six Mahiro illustrations) match
   scripts/protected-assets.sha256 byte for byte.
2. Every local path referenced by the READMEs (src, srcset, href) exists.
3. The three language versions share the same structure: section count,
   images (language suffix normalised), <picture>/<details>/<table> counts,
   external links and the professional data that must not drift (dates,
   exam code, versions).
4. Each README links to the other two (language selector).
5. Every <img> has an alt attribute.
6. Generated SVGs are safe (no scripts, handlers, foreignObject or remote
   references) and up to date with scripts/build_profile_assets.py.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READMES = {"es": "README.md", "en": "README.en.md", "pt": "README.pt-BR.md"}
ERRORS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def check_protected() -> None:
    manifest = ROOT / "scripts" / "protected-assets.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        path = ROOT / rel.strip()
        if not path.exists():
            err(f"protected asset missing: {rel}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest.lower():
            err(f"protected asset modified: {rel} ({actual})")


ATTR = re.compile(r'\b(src|srcset|href)="([^"]+)"')
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")


def local_refs(text: str) -> list[str]:
    refs = [v for _, v in ATTR.findall(text)] + MD_LINK.findall(text)
    out = []
    for r in refs:
        if re.match(r"^(https?:|mailto:|#)", r):
            continue
        out.append(r.split("#")[0].split("?")[0])
    return out


def external_links(text: str) -> list[str]:
    hrefs = re.findall(r'href="(https?://[^"]+|mailto:[^"]+)"', text) + re.findall(r"\]\((https?://[^)\s]+)\)", text)
    return sorted(set(hrefs))


def images(text: str, lang: str) -> list[str]:
    srcs = re.findall(r'(?:src|srcset)="(\./[^"]+)"', text)
    return [s.replace(f"-{lang}-", "-{lang}-") for s in srcs]


FACTS = re.compile(r"\b(?:19|20)\d\d\b|1Z0-[\d-]+|Python 3\.12|Django 5\.2|\b12\b")


def structure(text: str, lang: str) -> dict:
    return {
        "sections": len(re.findall(r"^## ", text, re.M)),
        "images": images(text, lang),
        "picture": text.count("<picture>"),
        "details": text.count("<details>"),
        "tables": text.count("<table>") + len(re.findall(r"^\| --- \|", text, re.M)) + len(re.findall(r"^\| :---: \|", text, re.M)),
        "external_links": external_links(text),
        "facts": sorted(FACTS.findall(text)),
        "badges": len(re.findall(r"img\.shields\.io|badge\.svg", text)),
    }


def check_readmes() -> None:
    texts = {lang: (ROOT / name).read_text(encoding="utf-8") for lang, name in READMES.items()}
    for lang, text in texts.items():
        name = READMES[lang]
        for ref in local_refs(text):
            if not (ROOT / ref.lstrip("./")).exists() and not (ROOT / ref).exists():
                err(f"{name}: broken local reference {ref}")
        for tag in re.findall(r"<img\b[^>]*>", text):
            if " alt=" not in tag:
                err(f"{name}: <img> without alt: {tag[:80]}")
        for other_lang, other in READMES.items():
            if other_lang != lang and f'href="./{other}"' not in text:
                err(f"{name}: language selector does not link to {other}")
        if 'src="./images/hero-mahiro-tech-dark-a.webp" width="100%"' not in text.split("\n", 3)[1]:
            err(f"{name}: hero banner markup changed")
    base = structure(texts["es"], "es")
    for lang in ("en", "pt"):
        other = structure(texts[lang], lang)
        for key, value in base.items():
            if other[key] != value:
                err(f"{READMES[lang]} differs from README.md in '{key}':\n    es={value}\n    {lang}={other[key]}")


FORBIDDEN_SVG = [
    (re.compile(r"<script", re.I), "<script>"),
    (re.compile(r"\son[a-z]+\s*=", re.I), "event handler"),
    (re.compile(r"<foreignObject", re.I), "foreignObject"),
    (re.compile(r"(?:href|src)\s*=\s*\"(?!#)", re.I), "external reference"),
    (re.compile(r"@import|url\((?!#)", re.I), "remote CSS"),
]


def check_svgs() -> None:
    for svg in sorted((ROOT / "profile-assets" / "v3").glob("*.svg")):
        text = svg.read_text(encoding="utf-8")
        for pattern, label in FORBIDDEN_SVG:
            if pattern.search(text):
                err(f"{svg.relative_to(ROOT).as_posix()}: contains {label}")
    res = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_profile_assets.py"), "--check"],
                         capture_output=True, text=True)
    if res.returncode != 0:
        err(res.stdout.strip() or res.stderr.strip())


def main() -> int:
    check_protected()
    check_readmes()
    check_svgs()
    if ERRORS:
        print("Profile validation FAILED:")
        for e in ERRORS:
            print(" -", e)
        return 1
    print("Profile validation passed: protected assets intact, local references resolve, "
          "3 languages in sync, SVGs safe and up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
