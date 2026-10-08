---
name: ste-explain
description: Rewrite explanations, diffs, and plans in 80% ASD-STE100 controlled English for fast human verification. Use directly when the user asks to simplify, clarify, or explain in text (e.g. 'explain this diff simply'), even if they did not ask for STE. If the best format is unclear, prefer the understanding-ladder router instead.
---

# STE-Explain — 80% STE rewriter + checker

Inspired by ASD-STE100 Simplified Technical English (not affiliated with ASD).
No STE rule text or dictionary is reproduced. Get the official standard free via
https://www.asd-ste100.org/STE_downloads.html

## When to use

- User asks to explain, simplify, clarify, review a diff/plan, or make output easier to verify.
- Output is long, passive, or uses inconsistent terms (worker/agent/executor drift).

Default is 80% STE: short, active, consistent, precise. Strict STE only if user asks.

Do NOT use for: poetry, fiction, chit-chat, or single-fact trivia — answer
directly and say STE does not apply. The pushy description targets
hard-to-check prose, not all text.

Mixed text: run the checker in the mode of the majority of sentences and note
the mix in Waivers. `WARNING:` labels stay attached to their sentence even when
a condition clause moves first; verbatim scope = label + constraint + numbers.

## Limits (verified against ASD-STE100 Issue 9 PDF)

Loaded from `../shared/ste-limits.json` (verified: true). Confirmed values:
`procedural_max_words: 20`, `descriptive_max_words: 25`,
`max_sentences_per_para: 6`, `max_noun_cluster_words: 3`,
Part 1 has 9 sections with 53 rules. Provenance is recorded in the JSON.
Override via `--config` only with a cited reason. Dictionary size is NOT
verified — never cite a count and never reproduce the dictionary.

Verified rules (from ASD FAQ webfetch): one meaning per word in general,
avoid -ing except technical nouns, condition-first, procedural imperative,
descriptive active (passive only if agent unknown), one topic per sentence.

## Workflow

1. **Lock terms.** Extract key entities. Pick one name per thing. Record synonyms
   to replace in `## Term map`. Never introduce a new synonym.
2. **Split.** One idea per sentence. Procedural = one instruction per sentence.
3. **Voice.** Procedural → imperative starting with verb. Descriptive → active.
   If reader must know condition first, put `If ... ,` clause first.
4. **Clean words.** Remove -ing forms unless part of a technical noun
   (e.g. keep `opening` only as noun). Replace unapproved fillers with advisory
   picks from `references/substitutions-advisory.md`. If unsure, keep the
   technical term and flag in Waivers. Preserve numbers, modals
   (can/may/might), negations, safety warnings verbatim.
5. **Check.** Run `scripts/ste_check.py --mode <procedural|descriptive> <file>`
   with auto-detected Python (`py -3` on Windows, else `python3`, else `python`).
   Fix violations or add explicit waiver with reason.
6. **Output.** ALWAYS use this template:

## STE text
<rewritten text>

## Term map
- canonical: [synonyms replaced]

## Waivers
- sentence N: reason (or None)

## ste-report.json
Run checker with `--json` and paste summary: sentence count, avg length, violations.

## Verification (built-in)

- Checker passes or waivers justified.
- Second pass: actor explicit? Uncertainty preserved? No dropped condition?
- Spot-check 3 surprising claims against source. If publishing, needs human STE review.

## References

- `references/rules-80pct.md` — 80% rule summary (own paraphrase).
- `references/substitutions-advisory.md` — small advisory subset, not a dictionary.
- Official spec: https://www.asd-ste100.org/ — request free PDF, do not redistribute.

## Known failure modes

- Over-simplification drops precision; longer output in strict mode.
- Checker cannot know approved meaning; human must review important text.
- Do not copy secondary cheat-sheets; they contain dictionary errors.
