#!/usr/bin/env python3
"""check_storyboard.py — validate storyboard.md + narration/captions (stdlib only)."""
import argparse, re, sys
from pathlib import Path
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("--narration"); ap.add_argument("--captions")
    a = ap.parse_args()
    t = Path(a.storyboard).read_text(encoding="utf-8", errors="replace")
    errs = []
    lines = [l for l in t.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3: errs.append("no table rows (header+separator+shots)")
    hdr = lines[0].lower() if lines else ""
    for c in ("shot", "length", "visual", "narration"):
        if c not in hdr: errs.append(f"missing column {c}")
    shots = lines[2:] if len(lines) > 2 else []
    if len(shots) > 12: errs.append(f"too many shots {len(shots)} > 12")
    if a.narration:
        n = Path(a.narration).read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?i)elevenlabs.*sk-|api[_-]?key\s*[:=]", n): errs.append("possible key in narration")
    if a.captions and not Path(a.captions).exists(): errs.append("captions missing")
    print(f"shots={len(shots)} errors={len(errs)}")
    for e in errs: print(f"- {e}")
    sys.exit(1 if errs else 0)
if __name__ == "__main__": main()
