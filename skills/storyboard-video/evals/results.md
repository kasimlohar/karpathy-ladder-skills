# storyboard-video benchmark — 2026-10-08 (storyboard-only per decision)

With-skill: PASS binary-search-90s
- 8 shots, 90s total, STE narration 132wpm, captions 1:1, local Kokoro default, grep clean, 3-claim checklist, check_storyboard errors=0
- No render, no keys, no 34GB claims
Baseline: FAIL — VHS prose idea, no table, no lengths, no captions plan (key hygiene clean but structure missing).

Note: low-quality preview renders (`manim -pql`) not tested — storyboard-only per user decision.

## Phase 2 fresh evals (SKILL.md-only, storyboard-only): 4/4 PASS
- dns-60s-real (6 shots/60s) + rebase-90s-real (7 shots/90s): tables, STE narration, local voice, no keys. Baselines: prose ideas, no tables, FAIL.
- negative-time: correctly declined. Baseline also direct — negative PASS both.
- adversarial-hedge: hedge kept in narration + captions + claims marked unconfirmed. Baseline kept hedge in prose but no storyboard/claims, FAIL.
Doc fix: caption-timing + checklist-template conventions added.

## Render gap closed — render-preview-90s: PASS
- Toolchain (nothing installed): PIL text+shape frames 854x480@15fps +
  ffmpeg 9.0 h264/aac + Windows SAPI local TTS. 1350 frames, 8 narration
  tracks, 90.0s mp4 with 1 audio stream.
- check_render.py: 0 errors — duration 90.0/90.0s, 854x480, audio present,
  frame brightness 27.0/29.7/34.3 (not black). Artifacts: ffprobe.json +
  frame-1/2/3.png + srt/narration/log under evals/artifacts/; mp4 deleted.
- Failures fixed during the run (recorded): (1) check_render moved frames
  with Path.replace across disk drives -> OSError; fixed with shutil.move.
  (2) PIL getdata deprecation warning -> switched brightness to histogram
  mean. No visual-quality claim made — frames show shot/caption text only.
