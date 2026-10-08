# ste-explain benchmark — 2026-10-08

With-skill (reads SKILL.md + references + checker): 3/3 PASS
- raft-junior: 6 sents, avg 9.0, 0 violations, terms consistent, hedges kept
- diff-imperative: 5 steps, avg 6.6, 0 violations, condition-first waived for If-clause, term map present
- unapproved-words: start/use/before applied, -ing removed, approx flagged not replaced

Baseline (no skill): 0/3 PASS (all FAIL length/active/-ing or approx handling)
- Raft: 2x 26-word sents, progressive -ing, FAIL
- Diff: passive were added / is being rejected, FAIL
- Rewrite: starting/going/running left, approximately unflagged, FAIL

Verdict: skill beats baseline. Scripts: ste_check.py --help OK via py -3.
Limits labeled UNVERIFIED DEFAULT (PDF gated via DOWNLOADS form).
CORRECTION (Phase 1): local ASD-STE100_ISSUE9.pdf obtained; limits verified
(20/25/6/3, 53 rules/9 sections) in skills/shared/ste-limits.json (verified:true).

## Phase 2 fresh evals (SKILL.md-only agents): 4/4 PASS
- jwt-expiry-real: 3 sents, 0 violations, numbers kept. Baseline: -ing left (logging), FAIL.
- deploy-plan-real: 5 imperative steps, term map. Baseline: no term map, FAIL.
- negative-haiku: correctly declined (fresh agent: forcing STE would destroy form). Baseline haiku also fine (no forcing) — negative PASS both.
- adversarial-safety: WARNING + 40 bar + 10 min + may/unsure kept. Baseline kept facts but left -ing (Venting), FAIL strict.
Doc fixes from fresh-agent unclear points: Do-not-use clause, mixed-mode rule, WARNING-verbatim scope.
