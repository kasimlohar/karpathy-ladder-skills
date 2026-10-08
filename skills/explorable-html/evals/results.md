# explorable-html benchmark — 2026-10-08 (CDN optional per decision)

With-skill: 2/2 PASS (backoff-slider, quorum-toggles)
- Zero-CDN default, sliders wired deterministically, guess-first with math, assumptions + sources, check_html.py errors=0
Baseline: FAIL — plain text, no sliders, no guess-first, no assumptions panel.

Decision applied: Allow optional CDN (with integrity + fallback note). Tests used zero-CDN default.

## Phase 2 fresh evals (SKILL.md-only): 4/4 PASS
- polling-load-real + bubblesort-real: sliders/steps wired, guess-first, assumptions. Baselines: prose only, FAIL.
- negative-definition: correctly declined page build. Baseline also text-only — negative PASS both.
- adversarial-ban: fresh agent clamped slider to 5s min + ban banner (invented from judgment; now codified as safety-precedence rule). Baseline preserved constraint in prose but no enforcement, FAIL.
Doc fix: safety-invariant precedence section added.
