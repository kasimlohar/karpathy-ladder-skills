# Understanding-Ladder Skills

Turn LLM output into forms humans can check quickly: constrained English,
validated diagrams, interactive pages, storyboarded videos — with a verifier
and a router that picks the lowest sufficient rung.

Inspired by [Andrej Karpathy's October 2026 post on understanding LLM outputs](https://x.com/karpathy/status/2105819303471976479).
Independent project — not affiliated with or endorsed by ASD, Karpathy, or
Anthropic. "ASD-STE100" is a trademark of ASD (Aerospace, Security and Defence
Industries Association of Europe); no spec text or dictionary is reproduced
here. Request the free official PDF at https://www.asd-ste100.org/.

## Install (5 lines)

```bash
git clone <this-repo> && cd <repo>
cp -r skills/ste-explain skills/diagram-first ~/.claude/skills/
cp -r skills/explorable-html skills/storyboard-video ~/.claude/skills/
cp -r skills/verify-ladder skills/understanding-ladder skills/shared ~/.claude/skills/
python3 ~/.claude/skills/ste-explain/scripts/ste_check.py --help
```

Keep `shared/` next to the skills (`ste_check.py` falls back to built-in
defaults without it). Or unpack release `.skill` zips (each bundles
`shared/ste-limits.json`; see `scripts/pack.ps1`).

## Skills

| Skill | Status | Needs |
|---|---|---|
| ste-explain | tested (7/7 vs 1/7 baseline) | Python only |
| diagram-first | tested (7/7 vs 1/7) | Python + Node/npx for real parse, else pre-check |
| explorable-html | tested (6/6 vs 1/6) | Python; browser audit via verify-ladder |
| storyboard-video | partly tested (5/5 storyboard; render untested) | Python only; no Manim/Showtime here |
| verify-ladder | tested (10/10 vs 2/6) | Python + Node + puppeteer-core + Chrome for HTML audit |
| understanding-ladder | tested (7/7 vs 1/7) | None (routes only) |

## Known limits

- No real video rendering has been run anywhere in this repo.
- Mermaid/HTML checks are pre-checks unless the run reports `parse` / `browser:ran`.
- ASD dictionary not bundled (advisory subset only); numeric limits verified
  from Issue 9 — see `skills/shared/UPDATE.md`.
- Details, pass rates, and fragile assertions: `docs/FINAL-REPORT.md`.
