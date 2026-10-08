---
name: storyboard-video
description: Draft storyboard.md, 80% STE narration, captions, and local render plan for bespoke 3Blue1Brown-style explainer videos. Use directly when the user asks for a video or storyboard — storyboard first, render only after verification, local voice by default. NOTE: video rendering is untested here (no Manim/Showtime); outputs are storyboard + script + plan only. If the best format is unclear, prefer the understanding-ladder router instead.
---

# Storyboard-Video — storyboard first, local render plan (RENDERING UNTESTED)

Video rendering is UNTESTED in this environment: neither Manim nor Showtime
is installed, and no preview render has been run. This skill outputs
storyboard + narration + captions + render plan only. Do not claim a video
was rendered. To enable rendering, install Manim or Showtime, run one
`manim -pql` preview, save `render.log`, and remove this notice.

No API keys in prompts or files. Default to local TTS. Never claim endorsement
or size figures without render logs. 34GB-type figures are excluded.

## When to use

- Process unfolds over time and animation plus narration adds value.
- User explicitly asks for 3b1b-style or explainer video.

## Workflow

1. **Storyboard.** Write `storyboard.md` table `Shot|Length|Visual|Narration`
   (any column order). ≤12 shots for 60-180s. Narration in 80% STE, ~130 wpm.
2. **Script + captions.** Save `narration.txt` (exact TTS text) + `captions.srt`.
   Read script without watching; list 3 surprising claims; verify to source.
3. **Visuals as code.** Manim Scene for math, Remotion composition for React,
   or Showtime `--from-storyboard` (0.4.0+ reads table directly). Never diffusion-only.
4. **Render plan (test mode: storyboard-only).** Per user decision, tests validate
   storyboard + narration + captions only — no video render required.
   For real runs: preview low first (`manim -pql` 480p15 or Remotion preview),
   then final (`manim -pqh` 1080p60 or `renderMedia h264`). Log resolution/fps/codec/size.
5. **Voice.** Local Kokoro (or system TTS) by default. ElevenLabs only if key
   already in env/credential store — read from env, never paste in prompt.
   Note logging default per vendor docs.
6. **Output:** `storyboard.md`, `narration.txt`, `captions.srt`, `main.py` or Remotion `src/` or showtime dir, `render.log` (when rendered), `verify.md` via verify-ladder.

## Conventions (defaults unless source dictates otherwise)

- Captions: split `narration.txt` verbatim into cues of ~1 line per 4 seconds;
  never paraphrase in captions.
- Read-script checklist template: three boxes — claims listed, each traced to
  source, hedges marked confirmed/unconfirmed.
- Do NOT storyboard static lookups (time, trivia) — answer directly.

## Verification (built-in)

- Storyboard shots ≤12, lengths sum to target ±15s.
- `scripts/check_storyboard.py` passes (columns, narration length, captions match).
- TTS text equals captions; no key in files (`grep -ri elevenlabs|api.key` clean).
- Read-script-before-watch checklist signed.

## References

- `references/storyboard-template.md` — table starter.
- Tools: Manim (`manim -pql` preview, `-pqh` 1080p60 slower), Remotion (`bundle`+`selectComposition`+`renderMedia h264`), Showtime local studio (MIT, no keys/uploads).

## Known failure modes

- Render blowup on high quality; ManimGL vs ManimCE API mismatch.
- TTS mispronunciation; uncompressed intermediates mistaken for delivery size.
- Narrated error harder to catch — script check is mandatory.
