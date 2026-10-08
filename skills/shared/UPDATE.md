# Updating `ste-limits.json`

The file holds: `procedural_max_words`, `descriptive_max_words`,
`max_sentences_per_para`, `max_noun_cluster_words`, `rules_total`,
`rules_sections`, plus `verified` + `provenance`.

## Current state

`verified` is `true`: values were confirmed 2026-10-08 by extracting text
from the local Issue 9 PDF (434 pages). Each number comes from the section
whose topic it governs, described here in our own words (no spec text quoted):
- Procedural sentences cap (20): the procedural-writing section's rule on how
  long a procedural sentence may be.
- Descriptive sentences cap (25): the descriptive-writing section's rule on how
  long a descriptive sentence may be.
- Paragraph cap (six sentences): the descriptive-writing section's rule on how
  many sentences a paragraph may hold.
- Noun-cluster cap (three words): the nouns section's rule on how long a
  multi-word noun may be.
- 9 sections / 53 rules: the guide-to-the-rules overview near the front matter
  stating how the writing rules are organized.
Dictionary size was NOT confirmed — never cite it.

## Re-verify against a newer issue

1. Request the free PDF at https://www.asd-ste100.org/STE_downloads.html
   (distribution is PDF-only; do not redistribute it).
2. Extract text and locate, in your own words: the sentence-length provisions
   (procedural vs descriptive), the paragraph-length provision, the
   noun-cluster provision, and the overview stating the rule/section counts.
3. Update the values, set `verified` true only with section citations in
   `provenance`, and keep the dictionary-size caveat unless you count the
   dictionary yourself. Never paste rule text or word lists into skills.
