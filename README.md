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

| Skill | Status (run / not run) | Needs |
|---|---|---|
| ste-explain | 7/7 run | Python only |
| diagram-first | 7/7 run | Python + Node/npx for real parse, else pre-check |
| explorable-html | 6/6 run, 1 not run (eviction-step) | Python; browser audit via verify-ladder |
| storyboard-video | 6/8 run (sort-compare, local-only not run). PIL/ffmpeg preview render tested; narration audio path, Manim, Remotion and Showtime untested. | Python + PIL + ffmpeg + local TTS |
| verify-ladder | 10/10 run | Python + Node + puppeteer-core + Chrome for HTML audit |
| understanding-ladder | 7/7 run | None (routes only) |

Never run anywhere: mmdc-unavailable and browser-unavailable fallback paths
in eval conditions, non-Windows machines, non-Chrome browsers, Showtime
integration, Chinese output.

## Known limits

- Preview render proven once on Windows: 90s 854x480 mp4 (PIL frames +
  ffmpeg, SAPI narration, check_render 0 errors). The narration audio path
  outside that setup, and full-quality renders (Manim, Remotion, Showtime),
  are still untested.
- Mermaid/HTML checks are pre-checks unless the run reports `parse` / `browser:ran`.
- ASD dictionary not bundled (advisory subset only); numeric limits verified
  from Issue 9 — see `skills/shared/UPDATE.md`.
- Details, pass rates, and fragile assertions: `docs/FINAL-REPORT.md`.
- The evals check rule-following against a no-skill baseline, not whether
  readers understand better. The planted-error tests in verify-ladder (every
  one BLOCKed) are the strongest evidence.
- The ASD-STE100 numbers cannot be checked from this repo alone. Check them
  against your own Issue 9 copy (see `skills/shared/UPDATE.md`).
- `scripts/pack.ps1` deletes files only inside its own temp stage folders and
  the repo `dist/` folder (path-guarded); it never touches skills or docs.
