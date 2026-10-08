# storyboard-video benchmark — 2026-10-08 (storyboard-only per decision)

With-skill: PASS binary-search-90s
- 8 shots, 90s total, STE narration 132wpm, captions 1:1, local Kokoro default, grep clean, 3-claim checklist, check_storyboard errors=0
- No render, no keys, no 34GB claims
Baseline: FAIL — VHS prose idea, no table, no lengths, no captions plan (key hygiene clean but structure missing).

Note: low-quality preview renders (`manim -pql`) not tested — storyboard-only per user decision.

## Phase 2 fresh evals (SKILL.md-only, storyboard-only): 4/4 PASS
- dns-60s-real (6 shots/60s) + rebase-90s-real (7 shots/90s): tables, STE narration, local voice, no keys. Baselines: prose ideas, no tables, FAIL.
- negative-time: correctly declined. Baseline also direct — negative PASS both.
- adversarial-hedge: hedge kept in narration + captions + claims marked unconfirmed. Baseline kept hedge in prose but no storyboard/claims, FAIL.
Doc fix: caption-timing + checklist-template conventions added.
