---
name: diagram-first
description: Turn structure, flows, or architecture into validated Mermaid plus edge list and STE caption. Use directly when the user asks for a diagram, flowchart, sequence, or map — even if they only asked for text. If the best format is unclear, prefer the understanding-ladder router instead.
---

# Diagram-First — validated diagram + edge audit

## When to use

- User asks how something works, flows, connects, or what a diff changes.
- Text explanation would list more than 5 entities or 6 relationships.

Default renderer is Mermaid (text-source, diffable). Graphviz/SVG fallback.
Excalidraw JSON only if user explicitly asks.

Validator lives at `scripts/validate_mermaid_full.py` (sibling of this SKILL.md;
fallback `scripts/validate_mermaid.py`). Requires Node + npx on PATH for the
real parse (`@mermaid-js/mermaid-cli` via npx — may download on first run,
needs network once).
Save one diagram per file (`diagram.mmd`); extra diagrams get numbered names.
For `sequenceDiagram` alt/else branches, label each branch message after `:`.

## Workflow

1. **Lock names.** Reuse ste-explain term map if present. One name per thing.
   Cap at 15 nodes; split if larger.
2. **Edge sentences first.** Write numbered list: `1. Client sends token to Auth.`
   Every arrow must have one sentence and vice versa.
3. **Emit Mermaid.** Prefer `flowchart TD` for architecture, `sequenceDiagram`
   for interactions. Short labels, no spaces in IDs, quote labels with special chars.
4. **Validate (primary: real parse).** Run `validate_mermaid_full.py diagram.mmd --json`
   (auto-detected Python: `py -3` on Windows, else `python3`, else `python`).
   It tries `mmdc` render first and falls back to regex pre-check.
   ALWAYS report `validator: parse` or `validator: pre-check only` with the result.
   A pre-check pass is never a parse pass. Fix arrow syntax
   (`-->` not `--<`, `-->|label|` needs both dashes), semicolons, reserved words.
   `validate_mermaid.py` alone is fallback only.
5. **Render + caption.** Save `diagram.mmd`, `diagram.svg` (or .png), `edges.md`,
   plus 2-3 sentence STE caption and `## What to check` (3 items).
6. **Output template:**

## Diagram source (diagram.mmd)
```mermaid
...
```

## Edges
1. ...

## Caption
...

## What to check
- ...

## Verification (built-in)

- Full validator ran; report `validator: parse` or `validator: pre-check only`.
- Parse must succeed for APPROVE; pre-check-only caps verdict at APPROVE-WITH-NITS.
- Edge count equals arrow count; names match term map.
- All arrows labeled; error path explicit for flows.
- If render fails, ship source + edges only and mark render BLOCKED.

## References

- `references/mermaid-patterns.md` — minimal patterns + failure modes.
- Mermaid docs via context7 `/mermaid-js/mermaid` (`mermaid.parse` API).

## Known failure modes

- Hallucinated edges; label drift (worker/agent/executor).
- Mermaid v10 vs v11 syntax drift; UML lifeline misuse.
- Layout unreadable at scale — split, do not shrink font.
