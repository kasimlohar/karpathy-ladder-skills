---
name: storyboard-video
description: "Draft storyboard.md, 80% STE narration, captions, and render a 480p preview mp4 for bespoke explainer videos. Use directly when the user asks for a video or storyboard — storyboard first, preview render with check_render.py, local voice by default. NOTE: tested preview path is PIL frames + ffmpeg + local TTS only; Manim/Remotion/Showtime renders are still untested. If the best format is unclear, prefer the understanding-ladder router instead."
---

# Storyboard-Video — storyboard first, tested 480p preview

Tested preview path (90s sample, check_render 0 errors): `render_preview.py`
builds 854x480@15fps PIL text+shape frames, muxes with ffmpeg, narrates with
local system TTS. Manim/Remotion/Showtime renders are still UNTESTED — do not
claim them. Preview proves the storyboard-to-mp4 pipeline, not visual quality.

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
4. **Preview render (tested).** Run `render_preview.py storyboard.md --out
   preview.mp4` (auto-detected Python; needs PIL + ffmpeg; local SAPI/system
   TTS when present, else silent-with-captions and reported). Then run
   `check_render.py preview.mp4 storyboard.md --expect-audio|--expect-silent`.
   Full-quality Manim/Remotion/Showtime renders remain untested — use the
   tested preview path unless the user explicitly provides a renderer.
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
- `scripts/check_render.py` passes on the preview mp4 (duration ±15%,
  854x480, audio iff narration requested, no black frames).
- TTS text equals captions; no key in files (`grep -ri elevenlabs|api.key` clean).
- Read-script-before-watch checklist signed.

## References

- `references/storyboard-template.md` — table starter.
- Tools: Manim (`manim -pql` preview, `-pqh` 1080p60 slower), Remotion (`bundle`+`selectComposition`+`renderMedia h264`), Showtime local studio (MIT, no keys/uploads).

## Known failure modes

- Render blowup on high quality; ManimGL vs ManimCE API mismatch.
- TTS mispronunciation; uncompressed intermediates mistaken for delivery size.
- Narrated error harder to catch — script check is mandatory.
