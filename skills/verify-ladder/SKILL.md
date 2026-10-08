---
name: verify-ladder
description: Audit any STE text, diagram, HTML explainer, or video script for hidden errors before sharing. Use directly when the user asks to check, audit, review, or verify an artifact — even polished outputs — whenever correctness matters more than speed.
---

# Verify-Ladder (full: STE + edges + HTML + video script)

Never approve fluent-but-wrong prose. Limits load from
`../shared/ste-limits.json` (verified against ASD-STE100 Issue 9 PDF;
see provenance field). Run scripts with auto-detected Python
(`py -3` on Windows, else `python3`, else `python`); HTML audit needs Node.

## When to use

- After ste-explain, diagram-first, explorable-html, or storyboard-video,
  before sharing or merging.
- When a reviewer says looks good but no one checked claims.

## Workflow

1. **STE parse.** Run `ste_audit.py <file> --mode <mode> --terms a,b --json`
   (wrapper over `../../ste-explain/scripts/ste_check.py`). Record long
   sentences, -ing, passive-procedural, long paras, term drift.
2. **Term drift.** Compare term map vs text. Flag worker/agent/executor style
   drift. Fail if canonical name missing or synonym unlisted.
3. **Edge audit.** Run `../../diagram-first/scripts/validate_mermaid_full.py
   diagram.mmd --json`. ALWAYS report `validator: parse` or
   `validator: pre-check only`. Pre-check-only caps verdict at
   APPROVE-WITH-NITS — never APPROVE. Check every arrow has one edge
   sentence and vice versa. Flag unlabeled arrows, unknown participants,
   swallowed branches.
4. **HTML audit (if artifact is HTML).** Run
   `node scripts/audit_html.js explainer.html --json`. Requires:
   `browser: ran`, zero console errors, zero unexpected external requests
   (CDN allowed only with integrity hash + documented fallback),
   every control changes output (`controlTest: changed`).
   `browser: unavailable` caps verdict at APPROVE-WITH-NITS.
5. **Video-script audit (if artifact is video).** Run
   `audit_video_script.py --narration narration.txt --captions captions.srt
   --claims claims.md --source source.txt --json`. Requires: narration equals
   captions, >=3 checkable claims, every claim number present in source
   (else contradiction flag), no keys in files. If a rendered mp4 exists,
   additionally run `../../storyboard-video/scripts/check_render.py preview.mp4
   storyboard.md --expect-audio|--expect-silent` and require 0 errors.
6. **Spot-checks.** List 3 surprising claims. Verify each to original source.
   If source missing, mark BLOCK.
7. **Verdict.** ALWAYS end with one line:
   `Verdict: APPROVE | APPROVE-WITH-NITS | BLOCK` plus fix list.

Conventions: default `--mode descriptive` (procedural if mostly instructions);
`--terms` from the artifact's term map, omit if none. Run STE checks on
extracted text, never raw HTML markup (markup inflates sentence length).
Parse the artifact body only — exclude Term map, Waivers, and What-to-check
sections from sentence/paragraph counts (waive them if the script flags them).
If fewer than 3 natural claims exist, check all and note the count.
`source missing -> BLOCK` covers factual claims only; non-artifacts
(poems, greetings) get no verdict, just an out-of-scope note.

## Output template

## Checks
- STE: ...
- Terms: ...
- Edges (validator=...): ...
- HTML (browser=...): ... / n/a
- Video script: ... / n/a (plus render check if mp4 exists)
- Spot-checks: 1... 2... 3...

## Fixes required
- ...

Verdict: ...

## Verification (self)

- Verifier must find every planted error in evals. Must not pass on polish alone.

## Known failure modes

- Checker fatigue: green checks mistaken for truth; domain truth still needs human.
- Heuristic claim-number matching misses paraphrased contradictions — human must
  still read the script.
