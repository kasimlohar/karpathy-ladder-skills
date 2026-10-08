# Third-party credits

Upstream licenses re-verified 2026-10-08 via `gh repo view <repo>
--json licenseInfo`, plus direct reads of the upstream LICENSE files below.

## Patterns borrowed (MIT — no code copied, ideas only)

- `ChangWenC/understanding-ladder` (MIT): lowest-sufficient-rung routing,
  "Nothing cut / Draft first / What to check" structure.
- `danyuchn/asd-ste100-skill` (MIT): STE rewriting with a deterministic linter.
- `FavioVazquez/showtime` (MIT): local video studio model, storyboard-table
  shape (`Shot|Length|Visual|Narration`).

## Ideas only (nothing copied — no code, rule text, or word list reused)

- `0xpili/simplified-technical-english`: checker-mode and advisory-subset
  shape only. Its upstream LICENSE file (read verbatim 2026-10-08) says the
  skill text and scripts are MIT while carving out the ASD word list:

  ```text
  MIT License

  Copyright (c) 2026 0xpili
  [... standard MIT permission and warranty text ...]

  NOTE: This license applies to the text of this skill and to its scripts.
  The word list in references/word-list.md shows words from the ASD-STE100
  dictionary, which is the property of ASD. Refer to NOTICE.md.
  ```

  Only the shape of the idea was borrowed; no code or word list was copied,
  so the carve-out does not touch this repo.
- `ASD-STE100 Simplified Technical English` (ASD property): the Issue 9 PDF
  was used solely to confirm numeric limits (see `skills/shared/UPDATE.md`).
  No rule text, examples, or dictionary entries are reproduced. "ASD-STE100"
  is ASD's trademark; this project is not affiliated with ASD.
- Andrej Karpathy's ladder post (linked, not quoted): the four-format idea.
