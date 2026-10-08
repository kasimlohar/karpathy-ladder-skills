# Ladder Skills

Six agent skills that reshape LLM output into forms you can check fast.
Built for anyone who reviews agent work: engineers, researchers, students.

## Before / After (from our own evals)

Before: "Access tokens expire after 15 minutes, so users need to refresh
them often. Refresh tokens last 7 days and let you get new access tokens
without logging in again. We allow 30 seconds of clock skew to handle small
time differences between servers."

After (`ste-explain`): "The system expires each access token after 15 min.
You can refresh the access token during a 7 day window. The system tolerates
30 s of clock skew."

Same facts. One name per thing. No clutter.

## Install

```bash
npx skills add kasimlohar/karpathy-ladder-skills
```

| Agent | How |
|---|---|
| Claude Code | `npx skills add` above, or copy `skills/*` to `~/.claude/skills/` |
| claude.ai | Download the `.skill` files from Releases, then Settings → Capabilities → Skills |
| Other agents | Copy the skill folders into the agent's skills dir |

Try this to check it works: "Explain JWT expiry in 80% STE: access tokens
expire after 15 min, refresh window is 7 days, clock skew of 30s is
tolerated." Then run the checker on the answer (see Reproduce below).

## The six skills

| Skill | What it does | Say this | Status |
|---|---|---|---|
| ste-explain | Rewrites text in plain controlled English | "explain this diff simply" | tested |
| diagram-first | Turns structure into a validated diagram | "draw the auth flow" | tested |
| explorable-html | Builds a small interactive page | "let me change the parameters" | tested |
| storyboard-video | Storyboards a short explainer video | "storyboard a 60s video" | preview only |
| verify-ladder | Audits any of the above for hidden errors | "check this before I share it" | tested |
| understanding-ladder | Picks the simplest format that fits | "help me understand X" | tested |

"Tested" means the skill beat a no-skill baseline on its evals (see
`skills/<name>/evals/results.md`). "Preview only" means only the 480p
preview path ran. Storyboard-video never rendered Manim, Remotion, or
Showtime output.

## How they fit together

`understanding-ladder` is a thin router. It picks the lowest rung that
fully answers — text, diagram, page, or storyboard — and then calls that
skill. Use it when you name no format. Name one, and call it directly.

## Honest limits

- Tested on Windows with Chrome nearby. Narration audio outside Windows
  SAPI, Manim, Remotion, Showtime renders, and non-Windows runs are
  untested.
- The evals check rule-following against a no-skill baseline. They do not
  prove readers understand better. The planted-error audits (all BLOCKed)
  are the strongest evidence.
- Reproduce any check yourself:

```bash
py -3 skills/ste-explain/scripts/ste_check.py --mode descriptive draft.txt --json
py -3 skills/diagram-first/scripts/validate_mermaid_full.py diagram.mmd --json
node skills/verify-ladder/scripts/audit_html.js page.html --json
py -3 skills/storyboard-video/scripts/check_render.py preview.mp4 storyboard.md --expect-audio --json
```

- The ASD numbers in `skills/shared/ste-limits.json` were confirmed against
  the maintainer's copy of Issue 9. The spec and word list are not bundled.
  Request the free PDF at https://www.asd-ste100.org/ to check them.

## Credits

Ideas and patterns from ChangWenC/understanding-ladder, danyuchn/
asd-ste100-skill, and FavioVazquez/showtime (all MIT). 0xpili's skill shaped
the checker idea only — no code or word list was copied. Independent
project, not affiliated with or endorsed by ASD, Karpathy, or Anthropic.
"ASD-STE100" is ASD's trademark. Ladder idea from
[Karpathy's post](https://x.com/karpathy/status/2105819303471976479).
MIT license, see LICENSE.
