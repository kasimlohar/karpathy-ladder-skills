# diagram-first benchmark — 2026-10-08

With-skill: 3/3 PASS, validator exit 0
- oauth-sequence: 6 edges, participants consistent, token edges numbered
- microservice-arch: 5 nodes/4 labeled arrows, edge list matches
- trace-flowchart: diamonds condition-first, one action/node, error path explicit

Baseline: FAIL — vague labels, no validation, error path missing, prose only for 2/3.

Validator: validate_mermaid.py --help OK. Fixed post-eval: edge count includes --< attempts, flowchart bare --> flagged as unlabeled_edge.

## Phase 1 — real parse as primary (mmdc 12.0.0 via npx)

## Phase 2 fresh evals (SKILL.md-only): 4/4 PASS, all validator=parse
- retry-code-real (9 edges) + login-seq-real (8 msgs, failure branch): parse_ok true. Baselines: prose only, FAIL.
- negative-capital: correctly declined diagram (Paris in text). Baseline same — negative PASS both.
- adversarial-drift-source: locked Deployer, drift flagged. Baseline noted mixing informally but kept 3 names, FAIL.
Doc fix: validator path + naming + alt/else label conventions added.
- validate_mermaid_full.py: good diagram -> validator=parse, parse_ok=true, 0 errors. Bad diagram (A--<B, B-->C) -> validator=parse, bad_arrow + unlabeled_edge flagged, exit 1.
- Every run reports validator field; pre-check-only caps verify-ladder verdict at WITH-NITS.
- Fixed: "--|" vs "-->|" label check (false positive); npx.cmd resolution via cmd /c.
