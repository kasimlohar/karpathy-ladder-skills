# Understanding-Ladder Skills

Turn LLM output into forms humans can check quickly: constrained English,
validated diagrams, interactive pages, storyboarded videos — with a verifier
and a router that picks the lowest sufficient rung.

Inspired by [Andrej Karpathy's October 2026 post on understanding LLM outputs](https://x.com/karpathy/status/2105819303471976479).
Independent project — not affiliated with or endorsed by ASD, Karpathy, or
Anthropic. "ASD-STE100" is a trademark of ASD (Aerospace, Security and Defence
Industries Association of Europe); no spec text or dictionary is reproduced
here. Request the free official PDF at https://www.asd-ste100.org/.

## Install

```bash
npx skills add kasimlohar/karpathy-ladder-skills
```

Or clone: `git clone https://github.com/kasimlohar/karpathy-ladder-skills.git`.
`npx skills add` installs only skill folders — copy `skills/shared/` next to
them for verified limits (`ste_check.py` falls back to built-in defaults
without it; `ste-explain` bundles a copy). Fallback for Claude Code:

```bash
cp -r skills/ste-explain skills/diagram-first ~/.claude/skills/
cp -r skills/explorable-html skills/storyboard-video ~/.claude/skills/
cp -r skills/verify-ladder skills/understanding-ladder skills/shared ~/.claude/skills/
```

claude.ai: download the `.skill` files from Releases, then Settings →
Capabilities → Skills to upload.

## Skills

| Skill | Status | Needs |
|---|---|---|
| ste-explain | tested (7/7 vs 1/7 baseline) | Python only |
| diagram-first | tested (7/7 vs 1/7) | Python + Node/npx for real parse, else pre-check |
| explorable-html | tested (6/6 vs 1/6) | Python; browser audit via verify-ladder |
| storyboard-video | tested (preview render) | Python + PIL + ffmpeg + local TTS; 90s 854x480 preview with narration verified |
| verify-ladder | tested (10/10 vs 2/6) | Python + Node + puppeteer-core + Chrome for HTML audit |
| understanding-ladder | tested (7/7 vs 1/7) | None (routes only) |

## Known limits

- Preview render proven once: 90s 854x480 mp4 (PIL frames + ffmpeg, Windows
  SAPI narration, check_render 0 errors). Full-quality renders (Manim `-pqh`,
  Remotion, Showtime) are still untested.
- Mermaid/HTML checks are pre-checks unless the run reports `parse` / `browser:ran`.
- ASD dictionary not bundled (advisory subset only); numeric limits verified
  from Issue 9 — see `skills/shared/UPDATE.md`.
- Details, pass rates, and fragile assertions: `docs/FINAL-REPORT.md`.
