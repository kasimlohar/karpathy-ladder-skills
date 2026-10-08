# Understanding-Ladder Skills

Six Agent Skills that turn Karpathy's "understanding ladder" (STE writing,
diagrams, interactive HTML, explainer video) into reusable agent behavior.
English only. Each skill beats its no-skill baseline on its evals —
see `<skill>/evals/results.md`.

| Skill | Does | Needs to run fully |
|---|---|---|
| ste-explain | 80% ASD-STE100 rewrite + `ste_check.py` | Python only (`py -3` / `python3` / `python` auto-detected) |
| diagram-first | Validated Mermaid + edge list | Python + Node/npx for real parse (`@mermaid-js/mermaid-cli` via npx cache); regex pre-check fallback |
| explorable-html | Single-file interactive explainer | Python for static check; browser audit via verify-ladder |
| storyboard-video | Storyboard + narration + captions + plan | Python only — **video rendering UNTESTED** (no Manim/Showtime here) |
| verify-ladder | Full audit: STE + edges + HTML + video script | Python + Node + puppeteer-core + Chrome for headless HTML audit |
| understanding-ladder | Thin router (lowest sufficient rung) | No tools (delegates) |

## Install

Per skill (Claude Code global skills shown; adapt `~/.claude/skills` to your agent):

```bash
git clone <this-repo>
cp -r skills/ste-explain ~/.claude/skills/
cp -r skills/diagram-first ~/.claude/skills/
# ... or install a packed file:
# unzip skills/ste-explain.skill -d ~/.claude/skills/ste-explain
```

Or via a skill manager: `npx skills add <repo>` / unpack the `.skill` zips
(each `.skill` file is a zip of its skill folder).

## Shared config

`shared/ste-limits.json` holds the ASD numeric limits with provenance.
See `shared/UPDATE.md` for how to re-verify against a newer Issue 9+ PDF.

## What is UNTESTED

- Video rendering (Manim `-pql`/`-pqh`, Remotion, Showtime): no renderer is
  installed here; storyboard-video outputs storyboard + script + plan only.
- Headless HTML audit outside this machine: needs `puppeteer-core` + a Chrome
  binary (`CHROME_PATH`, `PUPPETEER_MOD` envs override the defaults baked in
  `verify-ladder/scripts/audit_html.js`); without them it reports
  `browser:unavailable` and caps verdicts at WITH-NITS.
- Real-parse Mermaid without Node/npx: falls back to regex pre-check
  (`validator:pre-check only`), which caps verify-ladder at WITH-NITS.

## Constraints the skills obey

- No ASD rule text or dictionary reproduced (small advisory subset only +
  link to https://www.asd-ste100.org/STE_downloads.html).
- No 34 GB-type figures, no endorsement claims.
- No API keys in prompts or files; local TTS default; zero-CDN HTML default
  (CDN only with integrity hash + documented fallback).

## Credits (MIT patterns borrowed, no code copied)

- `ChangWenC/understanding-ladder` (MIT): lowest-sufficient-rung routing,
  Nothing cut, Draft first, What-to-check.
- `danyuchn/asd-ste100-skill` (MIT): STE rewriting with a linter.
- `FavioVazquez/showtime` (MIT): local video studio, storyboard-table shape.
- Ideas only (not copied): `0xpili/simplified-technical-english`
  (custom license — checker-mode and advisory-subset shape) and ASD-STE100
  itself (ASD property, Issue 9 PDF used solely to confirm numeric limits).
