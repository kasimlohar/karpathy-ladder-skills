#!/usr/bin/env python3
"""check_render.py — verify a preview mp4 against its storyboard (stdlib + PIL).
Checks (ffprobe): duration within 15% of storyboard total, resolution is
480p (height 480), an audio stream exists iff narration was requested
(--expect-audio / --expect-silent), and no all-black frames (3 samples via PIL).
Usage: check_render.py preview.mp4 storyboard.md [--expect-audio|--expect-silent] [--json]
Exit 1 on any failure. Claims only what was verified, never visual quality.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path
def ffprobe_json(mp4):
    ffprobe = shutil.which("ffprobe") or "ffprobe"
    p = subprocess.run([ffprobe, "-v", "error", "-show_format", "-show_streams",
                        "-of", "json", str(mp4)], capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise SystemExit(f"ffprobe failed: {(p.stderr or p.stdout)[:300]}")
    return json.loads(p.stdout)

def storyboard_total(path):
    import re
    total, n = 0.0, 0
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.match(r"(\d+(?:\.\d+)?)\s*s", cells[1], re.I) \
                and cells[0].lower() not in ("shot",):
            total += float(re.match(r"(\d+(?:\.\d+)?)", cells[1]).group(1)); n += 1
    return total, n

def frame_brightness(mp4, at_sec, tmp):
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    out = tmp / f"s{at_sec:.0f}.png"
    subprocess.run([ffmpeg, "-y", "-v", "error", "-ss", str(at_sec), "-i", str(mp4),
                    "-frames:v", "1", str(out)], check=True, capture_output=True, timeout=60)
    from PIL import Image
    img = Image.open(out).convert("L")
    hist = img.histogram()
    total = sum(hist)
    mean = sum(i * n for i, n in enumerate(hist)) / total
    return mean, str(out)

def main():
    import tempfile
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4"); ap.add_argument("storyboard")
    ap.add_argument("--expect-audio", action="store_true")
    ap.add_argument("--expect-silent", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    errs, info = [], {}
    meta = ffprobe_json(a.mp4)
    streams = meta.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    au = [s for s in streams if s.get("codec_type") == "audio"]
    dur = float(meta.get("format", {}).get("duration", 0) or 0)
    want, nshots = storyboard_total(a.storyboard)
    info.update({"duration": round(dur, 2), "storyboard_seconds": want,
                 "shots": nshots, "width": v.get("width"), "height": v.get("height"),
                 "audio_streams": len(au), "video_codec": v.get("codec_name")})
    if want <= 0:
        errs.append("storyboard total is 0 (unparseable lengths?)")
    elif abs(dur - want) / want > 0.15:
        errs.append(f"duration {dur:.1f}s differs >15% from storyboard {want:.1f}s")
    if v.get("height") != 480:
        errs.append(f"expected 480p (height 480), got {v.get('width')}x{v.get('height')}")
    if a.expect_audio and not au:
        errs.append("narration requested but no audio stream")
    if a.expect_silent and au:
        errs.append("expected silent but audio stream present")
    with tempfile.TemporaryDirectory(prefix="checkrender") as td:
        brights, saved = [], []
        for frac in (0.25, 0.5, 0.75):
            b, f = frame_brightness(a.mp4, max(dur * frac, 0.5), Path(td))
            brights.append(round(b, 1)); saved.append(f)
            if b < 2.0:
                errs.append(f"frame at {frac*100:.0f}% looks all-black (mean {b:.1f})")
        info["frame_brightness"] = brights
        keep = Path(a.mp4).parent
        for i, f in enumerate(saved):
            dst = keep / f"frame-{i+1}.png"
            shutil.move(f, dst)
        info["frames"] = [f"frame-{i+1}.png" for i in range(3)]
    rep = {"errors": errs, **info}
    if a.json:
        print(json.dumps(rep, indent=2))
    else:
        print(f"errors={len(errs)} duration={dur:.1f}s/{want:.0f}s "
              f"{v.get('width')}x{v.get('height')} audio={len(au)} bright={brights}")
        for e in errs:
            print(f"- {e}")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()
