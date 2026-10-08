---
name: explorable-html
description: Build single-file interactive HTML explainers with sliders, step-through, and predict-then-reveal guess-first checks. Use directly when the user mentions parameters, sliders, interactivity, or try-it — even if they only asked for text. If the best format is unclear, prefer the understanding-ladder router instead.
---

# Explorable-HTML — single-file interactive explainer

## When to use

- A parameter changes the outcome (backoff delay, quorum size, cache policy).
- User holds a misconception you can test with guess-first.

## Dependencies (per user decision: CDN optional)

- Default: zero-CDN vanilla HTML/CSS/JS, inline everything, opens via double-click, works offline.
- Optional CDN only if user explicitly asks for charts: add `<script src>` with
  integrity hash + offline fallback note + `## What to check` warning that
  external code must be reviewed. No tracking scripts. No API keys in file.

## Workflow

1. **Assumptions first.** List 2-5 variables (name, range, default, unit),
   target misconception, audience level, source links.
2. **Draft rung-1.** Write 80% STE text draft (ste-explain) you can check.
   Do not skip — every page starts from checkable text.
3. **Scaffold `explainer.html`.** Sections:
   - What it is (STE, <150 words)
   - Try it (sliders/step-through bound to variables)
   - Guess first (input for prediction + Reveal button showing actual vs prediction)
   - What to check (3 items) + Sources footer + Assumptions panel toggle
4. **Implement predict-then-reveal.** User sets variable → commits prediction
   → clicks Run/Reveal → sees result vs prediction with math shown.
   Controls must change output deterministically.
5. **Self-test.** Run `scripts/check_html.py explainer.html` with auto-detected
   Python (`py -3` on Windows, else `python3`, else `python`).
   Open offline, no console errors, all controls wired, <500KB aim.
   For shares, verify-ladder runs the headless browser audit on top.
6. **Output:** `explainer.html`, `assumptions.md`, `checks.md` (3 spot-checks).

## Safety-invariant precedence

A user-requested control range NEVER overrides a safety or ban constraint from
the source. Clamp the control to the safe range, show a persistent warning
banner stating the constraint and penalty, and record the change in
`assumptions.md`. If the constraint cannot be enforced in UI, BLOCK instead.

Do NOT build a page for single-fact trivia or definitions with no parameter,
no outcome to vary, and no testable misconception — answer in text and say
HTML does not apply.

## Verification (built-in)

- File opens offline (or CDN fallback noted); zero console errors.
- Slider/step changes graph/number; guess-first reveals with math.
- Assumptions listed visibly; sources linked; STE draft kept.

## References

- `references/template.html` — minimal starter (sliders + reveal).
- `references/patterns.md` — slider, step-through, guess-first snippets.

## Known failure modes

- JS hides wrong model behind polish; harder to diff than Markdown.
- Over-animation distracts; keyboard/accessibility neglected.
- CDN drift — pin version + hash when allowed.
