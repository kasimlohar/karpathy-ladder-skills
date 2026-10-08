# Final Report — Understanding-Ladder Skills (v0.1.0)

Date: 2026-10-08. Six skills in `skills/`: ste-explain, diagram-first,
explorable-html, storyboard-video, verify-ladder, understanding-ladder.
Research brief: `docs/research-brief.md`. Method: skill-creator loop —
draft, evals, with-skill vs baseline subagents, grade, fix, repeat —
then fresh-context validation, triggering/integration, packaging.

## With-skill vs baseline pass rates

| Skill | With-skill | Baseline | Notes |
|---|---|---|---|
| ste-explain | 7/7 (3 orig + 4 fresh) | 1/7 (negative only) | Baselines fail length/active/-ing; adv. close but -ing |
| diagram-first | 7/7 (3 orig + 4 fresh) | 1/7 (negative only) | Baselines prose-only, drift unflagged |
| explorable-html | 6/6 run (2 orig + 4 fresh) | 1/6 (negative only) | eviction-step orig eval NOT run |
| storyboard-video | 5/5 run (1 orig + 4 fresh) | 1/5 (negative only) | sort-compare, local-only orig evals NOT run |
| verify-ladder | 10/10 (3 thin + 3 planted + 4 fresh) | 2/6 (phase-1 planted not baselined) | All planted errors BLOCK |
| understanding-ladder | 7/7 (3 orig + 4 fresh) | 1/7 (greeting only) | Human-graded routing |
| Triggering (descriptions-only) | 6/7 → G fixed | n/a | "explain simply with a diagram" double-claimed; router now owns multi-format |
| End-to-end (real fix + planted 13.0.0) | PASS | n/a | Term map 7/7 carried; verify BLOCKED version lie |

Negative prompts: all skills correctly decline (and baselines, which simply
answer directly, also pass negatives — expected). Adversarials: all preserved
or flagged (safety verbatim, drift lock, slider clamp, hedge, number-swap).

## Which validator ran for each check

- STE: `ste_check.py` reading `shared/ste-limits.json` (`verified:true`;
  numbers confirmed from the Issue 9 PDF, see `shared/UPDATE.md`).
- Diagrams: `validate_mermaid_full.py` → `validator:parse` via mmdc 12.0.0
  (npx cache, no install) on every eval; regex `validate_mermaid.py` kept as
  fallback (`validator:pre-check only`, caps verify at WITH-NITS).
- HTML: `audit_html.js` → `browser:ran` (puppeteer-core + cached Chrome) on
  template + planted fixtures: zero console errors on clean, caught thrown
  error and dead slider; `check_html.py` static checks as backup.
- Video scripts: `audit_video_script.py` (narration=captions, ≥3 claims,
  claim numbers cross-checked to source, key grep); `check_storyboard.py`
  (columns, ≤12 shots).
- Python launcher auto-detected everywhere (`py -3` / `python3` / `python`).

## Still untested

- Video rendering (no Manim/Showtime here; storyboard-video says so plainly).
- Original evals: eviction-step, sort-compare, local-only (never run).
- `browser:unavailable` and mmdc-unavailable fallback paths in eval conditions.
- Non-Windows / non-Chrome machines; Showtime integration; Chinese output.
- Triggering fix for case G verified by inspection only — needs a fresh-agent retest.

## The one next fix

Run the three never-run original evals (eviction-step, sort-compare,
local-only) plus a fresh-agent retest of triggering case G, and record in
`evals/results.md`. After that, the highest-value work is an HTML-inclusive
end-to-end (the current e2e had no HTML artifact, so the browser audit never
gated a chain).

## Assertions tuned to author output (fragile, listed per instructions)

Exact edge counts (9/8/4/5), `100*2^3=800` backoff math, shot counts and
durations, template zero-error (Chrome-dependent), digit-form claim numbers,
JWT/TLS/rung choices on ambiguous prompts. Re-runs with different valid
outputs may need assertion updates — none were changed; failures would be
recorded, not edited away.
