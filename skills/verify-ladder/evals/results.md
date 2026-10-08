# verify-ladder thin v1 benchmark — 2026-10-08

With-skill: correctly BLOCKs both planted-error artifacts
- auth-drift: caught family_drift worker/agent/executor, bad_arrow --<, (unlabeled B-->C now caught after fix)
- planted-passive: caught long_sentence 35>20, ing_form, missing_term server
- Verdicts: BLOCK/BLOCK. Self-grade: APPROVE-WITH-NITS (3 nits fixed: ste_audit --json flag added, word-boundary term match, unlabeled_edge check)

Baseline: looks-good/pass, missed drift, bad arrow, passive. 0/2 catches.

Thin scope noted: HTML JS logic + video timing deferred to full version.

## Phase 1 (full v2) — new planted-error tests, all BLOCK

## Phase 2 fresh evals (SKILL.md-only): 4/4
- clean-approve-real: APPROVE with validator=parse reported. Baseline gave WITH-NITS without scripts — lenient non-BLOCK, partial credit.
- template-html-real: APPROVE, browser=ran, controlTest=changed. Baseline refused to open file (BLOCK on looks-fine) — FAIL (over-block).
- negative-poem: correctly scoped out (no verdict). Baseline APPROVEd poem without scope note — FAIL.
- adversarial-number-swap (50 vs 15 min): BLOCK. Baseline also BLOCKed (numbers in prompt) — PASS both.
Doc fix: mode/terms defaults, no-raw-markup rule, <3-claims handling, non-artifact scope note.

## Phase 3 end-to-end: BLOCK planted 13.0.0 (source 12.0.0), term map carried (7/7 canonical across ste/diagram/edges/outline), validator=parse.
Doc fix: parse body only — exclude Term map/Waivers/What-to-check from counts.
- html-console-error: audit_html.js browser=ran, consoleErrors=[pageerror: Error: planted] -> exit 1 -> BLOCK. PASS.
- html-dead-control: controlTest=unchanged (slider with no listener, zero console errors) -> exit 1 -> BLOCK. PASS.
- video-claim-contradiction: audit_video_script flags "number 30 not in source", catches narration/captions mismatch -> exit 1 -> BLOCK. PASS.
- Skill bugs fixed in Phase 1: validate_mermaid unlabeled check used "--|" instead of "-->|" (false positive on labeled edges, missed malformed form) — fixed; mmdc npx resolution failed on Windows (.cmd shim needs cmd /c) — fixed, now validator=parse; ste_audit substring term match — fixed to word-boundary; number-word normalization added to audit_video_script (digits caught; word-paraphrase limits documented).
