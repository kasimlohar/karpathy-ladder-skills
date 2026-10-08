#!/usr/bin/env python3
"""render_preview.py — storyboard table -> 480p preview mp4 (stdlib + PIL + ffmpeg).
Preview-quality pipeline only (proves storyboard -> mp4, not 3Blue1Brown looks).
Each shot becomes N seconds of 854x480 frames: background hue varies per shot,
shot number + visual + narration caption are drawn as text. Narration uses
local Windows SAPI TTS when available, else silent with captions (reported).
Usage:
  render_preview.py storyboard.md --out preview.mp4 [--fps 15] [--no-audio] [--workdir DIR]
Outputs: preview.mp4 + preview.srt + narration.txt + render.log next to --out.
Run with auto-detected Python (py -3 on Windows, else python3, else python).
"""
import argparse, math, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

W, H, DEFAULT_FPS = 854, 480, 15

def parse_storyboard(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0].lower() in ("shot", "-", "---"):
            continue
        if re.fullmatch(r"[\s\-:]+", cells[0]):
            continue
        m = re.match(r"(\d+(?:\.\d+)?)\s*s", cells[1], re.I)
        if not m:
            continue
        rows.append({"shot": cells[0], "length": float(m.group(1)),
                     "visual": cells[2], "narration": cells[3]})
    if not rows:
        raise SystemExit("no storyboard rows parsed (need | Shot | Length | Visual | Narration |)")
    return rows

def draw_frame(shot_idx, n_shots, visual, caption, size=(W, H)):
    from PIL import Image, ImageDraw
    hue = int(255 * shot_idx / max(n_shots, 1))
    img = Image.new("RGB", size, (18 + hue // 6, 24, 40 + hue // 3))
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, size[0] - 20, 120], outline=(255, 255, 255), width=3)
    d.text((34, 34), f"Shot {shot_idx + 1}/{n_shots}", fill=(255, 220, 120))
    d.text((34, 62), visual[:90], fill=(255, 255, 255))
    words, lines, cur = caption.split(), [], ""
    for w in words:
        if len(cur) + 1 + len(w) > 72:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    y = size[1] - 30 - 22 * len(lines)
    d.rectangle([0, y - 12, size[0], size[1]], fill=(0, 0, 0))
    for ln in lines[:6]:
        d.text((34, y), ln, fill=(255, 255, 255)); y += 22
    return img

def synth_sapi(text, wav_path):
    """Local Windows SAPI TTS -> wav. Returns True, else False (silent)."""
    if os.name != "nt":
        return False
    ps = (f"Add-Type -AssemblyName System.Speech; "
          f"$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.Rate = -1; "
          f"$s.SetOutputToWaveFile('{wav_path}'); "
          f"$s.Speak(@'\n{text}\n'@); $s.Dispose()")
    try:
        p = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, timeout=120)
        return p.returncode == 0 and Path(wav_path).exists()
    except Exception:
        return False

def wav_seconds(path, ffprobe="ffprobe"):
    p = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, timeout=30)
    try:
        return float(p.stdout.strip())
    except Exception:
        return 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out", default="preview.mp4")
    ap.add_argument("--fps", type=int, default=DEFAULT_FPS)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--workdir", default=None)
    a = ap.parse_args()
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    ffprobe = shutil.which("ffprobe") or "ffprobe"
    rows = parse_storyboard(a.storyboard)
    total = sum(r["length"] for r in rows)
    work = Path(a.workdir) if a.workdir else Path(tempfile.mkdtemp(prefix="renderprev"))
    work.mkdir(parents=True, exist_ok=True)
    frames = work / "frames"
    frames.mkdir(exist_ok=True)
    log = []
    # 1. frames
    fi = 0
    for i, r in enumerate(rows):
        n = max(int(round(r["length"] * a.fps)), 1)
        for _ in range(n):
            draw_frame(i, len(rows), r["visual"], r["narration"]).save(frames / f"f{fi:06d}.png")
            fi += 1
    log.append(f"frames={fi} fps={a.fps} total_shots={len(rows)} storyboard_seconds={total}")
    # 2. narration wavs, one per shot, fitted to shot length
    audio_tracks, silent = [], False
    if not a.no_audio:
        ok_any = False
        for i, r in enumerate(rows):
            w = work / f"n{i:02d}.wav"
            if synth_sapi(r["narration"], str(w)):
                ok_any = True
                dur = wav_seconds(w, ffprobe) or 0.01
                filt = ""
                if dur > r["length"]:
                    stretch = max(r["length"] / dur, 0.5)
                    filt = f"atempo={stretch:.3f},atrim=0:{r['length']}"
                else:
                    filt = f"apad=whole_dur={r['length']}"
                fit = work / f"a{i:02d}.wav"
                subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(w),
                                "-af", filt, "-ar", "22050", str(fit)], check=True,
                               capture_output=True, timeout=120)
                audio_tracks.append(str(fit))
            else:
                break
        silent = not ok_any
        if silent:
            log.append("TTS unavailable -> silent preview with captions")
        else:
            log.append(f"TTS=local SAPI, narration tracks={len(audio_tracks)}")
    else:
        silent = True
        log.append("--no-audio -> silent preview with captions")
    # 3. mux
    out = Path(a.out)
    cmd = [ffmpeg, "-y", "-v", "error", "-framerate", str(a.fps),
           "-i", str(frames / "f%06d.png")]
    if not silent:
        lst = work / "aud.txt"
        lst.write_text("".join(f"file '{t}'\n" for t in audio_tracks), encoding="utf-8")
        cmd += ["-f", "concat", "-safe", "0", "-i", str(lst),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest", str(out)]
    else:
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)]
    subprocess.run(cmd, check=True, capture_output=True, timeout=600)
    # 4. sidecars: srt + narration + log
    srt, t = [], 0.0
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms//3600000:02d}:{(ms//60000)%60:02d}:{(ms//1000)%60:02d},{ms%1000:03d}"
    for i, r in enumerate(rows):
        srt += [str(i + 1), f"{ts(t)} --> {ts(t + r['length'])}", r["narration"], ""]
        t += r["length"]
    out.with_suffix(".srt").write_text("\n".join(srt), encoding="utf-8")
    out.with_name(out.stem + "-narration.txt").write_text(
        "\n".join(r["narration"] for r in rows), encoding="utf-8")
    log.append(f"silent={silent} out={out} seconds={total}")
    out.with_name(out.stem + "-render.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))

if __name__ == "__main__":
    main()
