---
name: understanding-ladder
description: Pick the lowest rung that fully answers — STE text, diagram, interactive HTML, or video storyboard — and route there. Use ONLY when the user wants to understand something and names no format, or names two or more formats at once. If they ask for exactly one of text/simply, a diagram, interactivity, a video, or a check, call that skill directly instead. English only.
---

# Understanding-Ladder — thin router only (English only)

This skill routes. It does not implement rungs. Delegate to:
ste-explain, diagram-first, explorable-html, storyboard-video, then verify-ladder.

Ideas owe to ChangWenC/understanding-ladder (MIT) and danyuchn/asd-ste100-skill (MIT):
lowest sufficient rung, Nothing cut, Draft first, What to check. No code copied.

## Routing rules (lowest rung that fully answers)

- Definition, fact, procedure, diff summary → ste-explain (rung 1).
- Process, causality, states, components, architecture → diagram-first (rung 2).
- Parameter changes outcome or misconception testable → explorable-html (rung 3).
- Derivation unfolding over time where motion+narr narration beats static → storyboard-video (rung 4).
- Any share/merge/publish → verify-ladder after generation.
- If torn between two rungs, pick lower. Never climb higher than question needs.
- If the user names two or more formats (e.g. "explain simply with a diagram"),
  produce both, text first, then the higher rung from the same term map.
- Greetings, chit-chat, and single-fact trivia with no understanding gap get no
  rung: respond directly, no `What to check`.
- Rung 2 vs 4: static diagram suffices unless the question is about change over
  time that still frames cannot show; default to 2.

English only per decision. Chinese handling deferred.

## Workflow

1. Classify content into one row above. State choice in one line.
2. Call the rung skill (read its SKILL.md and follow it).
3. Keep rung-1 STE draft for rungs 2-4 (Draft first).
4. Append `## What to check` (3 items) and `Nothing cut` confirmation
   (numbers, conditions, hedges preserved).
5. Route to verify-ladder before sharing.

## Output template

Rung: N — reason in one line
<delegated skill output>
## What to check
- ...
Nothing cut: yes/no (list any dropped fact as BLOCK)

## Verification

- Rung choice justified; lower rung would miss X.
- verify-ladder verdict attached for shares.

## Known limits

- Easier to understand ≠ verified. Polish lowers guard.
- Router never renders video itself; delegates to storyboard-video (storyboard-only in tests).
