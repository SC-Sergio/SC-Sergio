# GitHub Profile v3.0 — Mahiro Tech Edition

Continuity notes for whoever maintains this profile next (human, Claude Code or Codex).
Read this before editing any README.

## 1. What this repository is

`SC-Sergio/SC-Sergio` is the GitHub profile repository. GitHub shows `README.md` on
https://github.com/SC-Sergio. `README.en.md` and `README.pt-BR.md` are full translations
reached through the language selector under the hero.

## 2. Design direction

**Premium Anime Tech — futuristic developer portfolio.** Three concepts were compared:

| Concept | Kept | Dropped |
| --- | --- | --- |
| A. Futuristic Developer Dashboard | terminal section chips (`01 ~/whoami`), `whoami.yml` block, project status overview | dense stat grids, extra third-party stat cards |
| B. Premium Anime Tech Portfolio | six Mahiro illustrations integrated into the layout, brand gradient | decorative overload, image-only sections |
| C. Minimal Professional Tech | real text, few badges, no `---` dividers, collapsible detail | removing personality |

The result: the professional content leads, and Mahiro appears as the brand mascot
alongside it, with a different composition in each section.

### Design tokens

| Token | Value | Use |
| --- | --- | --- |
| Ink | `#0D1117` | chip background |
| Panel | `#161B22` | badge label colour, dark diagram nodes |
| Signature pink | `#C75C8A` (light theme: `#B0466F`) | primary CTA, tagline prompt, accents |
| Violet | `#A78BFA` / `#7C3AED` | gradient, LinkedIn CTA, connectors |
| Cyan | `#67E8F9` / `#0E7490` | gradient, email CTA, chip index |
| Soft white | `#F0F6FC` | text on dark assets |
| Neutral grey | `#8B949E` / `#59636E` | secondary text in SVGs |

Text colour in the Markdown is never forced, so GitHub's own light/dark contrast is used.
Colours appear only in our SVGs and badges.

### Badge rules

- `for-the-badge` + `labelColor=161B22` only for the main calls to action (hero and contact):
  Portfolio = pink, LinkedIn = violet `7C3AED`, email = cyan `0E7490`.
- `flat-square` for everything secondary (project status/links, credentials, Steam).
- Live, first-party status where possible: the portfolio CI badge comes from GitHub Actions,
  and the Carey Assistant release badge reads the public releases repository.

## 3. Page structure (identical in the three languages)

| # | Chip | Section | Illustration / composition |
| --- | --- | --- | --- |
| — | — | Hero: banner (protected), name, role, location, animated tagline, 3 CTAs, language selector | `hero-mahiro-tech-dark-a.webp` |
| 01 | `~/whoami` | About me + current focus | `mahiro-about-me.webp` floated right (31%) beside the intro + `whoami.yml` |
| 02 | `~/stack` | Tech ecosystem: 7 categories, core in chips, full inventory collapsible | `mahiro-tech-stack.webp` floated left (29%) |
| 03 | `~/projects` | Single-column project panel: overview row + 4 cards (description, problem solved, stack, verifiable status, links) + more projects collapsible | `mahiro-projects.webp` inside the panel header (27%) |
| 04 | `~/learning` | Year/credential timeline, details collapsible | `mahiro-education.webp` floated left (23%) |
| 05 | `~/activity` | Self-hosted contribution card + snake, one caption | — |
| 06 | `~/workflow` | Workflow diagram (SVG), stage details collapsible | `mahiro-debugging.webp` floated right (29%) |
| 07 | `~/offline` | Games, anime, technology + Steam (secondary) | — |
| 08 | `~/contact` | Centred closing that mirrors the hero, 3 CTAs | `mahiro-contact.webp` centred (24%) |

### Why the layout works on mobile

The profile README is only **846 px** wide on desktop, **398 px** at 768 px viewports
(the sidebar stays beside it), **308 px** at 390 px and **278 px** at 360 px
(measured with Playwright on github.com).

- Illustrations use `align="left|right"` with **percentage** widths, so they shrink with the
  column instead of squeezing the text.
- `<br clear="all" />` ends every floated block before the next heading.
- Projects use one column (one table, one row per card) instead of a two-column grid.
- Code lines in `whoami.yml` are ≤ 28 characters, so the block fits at 278 px without scrolling.
- The workflow diagram is 2 × 3 (not 6 in a row), so labels stay legible on phones.

## 4. Protected assets — never modify

SHA-256 manifest: `scripts/protected-assets.sha256` (checked in CI).

| File | SHA-256 |
| --- | --- |
| `images/hero-mahiro-tech-dark-a.webp` | `86629AF69F93E96586DE90D1432B415B0DEE4C6509DB0EBC84D8EBE6C686153C` |
| `images/mahiro-v2/mahiro-about-me.webp` | `BDADA2D47C27FE11BA3A00FAC18059F980B59537EE449185791EBC26CB361820` |
| `images/mahiro-v2/mahiro-tech-stack.webp` | `1F799C3C72B965339FFEC2B280C5ADEDA1D6A768D5DF358C6E54B9832DC7E3A9` |
| `images/mahiro-v2/mahiro-projects.webp` | `2D0D9693142CDF11AE0E44DDF69C8E5D8C7CAB9A96C0CEDC460D2FB3D5A26A76` |
| `images/mahiro-v2/mahiro-education.webp` | `F4009F214DC0D9D558C4C4CCE4D1F84388CC119EA56C3C91B57658779AABBCC7` |
| `images/mahiro-v2/mahiro-debugging.webp` | `1EECF74B9BDD4A2C7198433A569B9EBE7D1BA08B912BC736FDA9EC4791CC66F5` |
| `images/mahiro-v2/mahiro-contact.webp` | `00E212F90714C9F1029B28AC0A64114BCB16B890FC5D0A3B1AEF98990787A8CB` |

The hero markup (`<p align="center"><img src="./images/hero-mahiro-tech-dark-a.webp" width="100%" …/></p>`)
must also stay as it is; the validator checks it.

## 5. Image organisation

```
images/                      original assets (kept as a historical backup)
  hero-mahiro-tech-dark-a.webp   ← banner (protected)
  hero-mahiro-tech-dark-b.webp, bg.webp, mahiro*.png   legacy, unused, keep
  mahiro-v2/*.webp            ← six illustrations (protected)
profile-assets/
  contributions.{dark,light}.svg  ← written daily by profile-cards.yml — do not edit
  v3/                         ← generated by scripts/build_profile_assets.py — do not hand-edit
    chip-0N-<name>.svg          section chips (language neutral, theme neutral)
    tagline-<lang>-<theme>.svg  animated hero tagline (SMIL; replaces readme-typing-svg)
    workflow-<lang>-<theme>.svg workflow diagram
docs/v3-evidence/*.webp       before/after screenshots from the v3 QA
```

All v3 SVGs are static XML with no scripts, event handlers, external fonts or remote
references. They use system font stacks and `textLength`, so they render the same in
any browser.

## 6. Routine maintenance

### Update a project or certification

1. Edit the same block in **all three** READMEs (same position, same badges).
2. Never invent metrics, users, dates or credentials. Private repositories (e.g. FastLaundry)
   get no link and keep the `Código privado / Source private` badge.
3. Run `python scripts/validate_profile.py`. It fails if years, exam codes or versions
   differ between languages.

### Change the tagline, workflow labels or a chip

1. Edit `TAGLINES`, `WORKFLOW`, `WORKFLOW_HINT` or `CHIPS` in `scripts/build_profile_assets.py`.
2. Run `python scripts/build_profile_assets.py`.
3. Update each README's `alt` text to match.
4. Run `python scripts/validate_profile.py` (it also runs the generator in `--check` mode).

### Keep languages in sync

The three files have the same line-by-line structure. Change one, then mirror it in the
other two. CI (`profile-validate.yml`) compares section count, image list (language
suffix normalised), `<picture>`/`<details>`/table counts, external links, badge count and
key facts.

## 7. Automations (unchanged by v3)

| Workflow | Schedule | Output |
| --- | --- | --- |
| `profile-cards.yml` | daily 03:30 UTC | commits `profile-assets/contributions.{dark,light}.svg` to `main` (`[skip ci]`) |
| `profile-snake.yml` | daily 03:15 UTC | publishes the snake SVGs to the `output` branch |
| `profile-validate.yml` (new) | PRs + pushes to `main` touching the profile | read-only validation, stdlib Python, no dependencies |

Third-party image services still in use: `img.shields.io` (badges) and `skillicons.dev`
(one icon strip). `readme-typing-svg.demolab.com` was removed and replaced by the
self-hosted tagline.

## 8. GitHub rendering constraints (verified)

Checked through `POST /markdown` (GFM, repository context) and on github.com:

- Kept: `align` and percentage `width` on `<img>`, `<br clear="all">`, `<picture>` +
  `<source media>` (wrapped in GitHub's `themed-picture`), `<details>/<summary>`,
  Markdown inside `<td>`, `<sub>`, `<code>`.
- GitHub forces `table { width: max-content; max-width: 100% }`, so `width` on tables is
  ignored. Images are auto-wrapped in links to themselves.
- No JavaScript, iframes, inline CSS, external CSS or web fonts are used anywhere.

## 9. QA performed for v3

Playwright (Chromium 1.65) against github.com: the live profile as the baseline, and the
feature branch's blob pages, with the article constrained to the measured profile widths
(846 / 398 / 308 / 278 px). Run in dark and light colour schemes for the three languages
(24 renders): 0 broken images, 0 horizontal overflow, 0 internally scrolling tables or code
blocks. After the merge, the live profile was re-checked at 1920×1080, 1366×768, 768×1024,
390×844 and 360×800 in both themes.

Known limitations:

- The animated tagline is about 9 px tall on 278 px phones (decorative; the role line
  above it is real text and the `alt` text carries the content).
- The workflow hint lines (small grey text) are small on phones; the full description is
  in the collapsible list below the diagram.
- Logged-in users who override GitHub's theme see the `<picture>` variant for their chosen
  theme (handled by GitHub). The section chips are dark in both themes by design.

## 10. History

- v2: PR #2, merge `a183cf125bf2b93dec334fc100b992f721338206`. Introduced the six Mahiro illustrations.
- v3: branch `feature/github-profile-v3-premium-redesign`. See the v3 pull request for the
  final merge commit.
