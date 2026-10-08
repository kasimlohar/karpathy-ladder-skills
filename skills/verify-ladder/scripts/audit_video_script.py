#!/usr/bin/env python3
"""audit_video_script.py — narration/captions/claims audit (stdlib only).
Checks:
 1. narration.txt wording equals captions.srt cue text (order-insensitive join).
 2. claims.md lists >=3 checkable claims (lines starting with - or numbered).
 3. Every number in claims appears in the source file (else flag as contradiction risk).
 4. No API keys in any file.
Usage: audit_video_script.py --narration narration.txt --captions captions.srt --claims claims.md --source source.txt [--json]
Exit 1 on any failure (verifier must BLOCK).
"""
import argparse, json, re, sys
from pathlib import Path

KEY_RE = re.compile(r"(?i)(elevenlabs.*sk-|api[_-]?key\s*[:=]\s*\S+|Bearer\s+\S{10,})")

def srt_text(p):
    t = Path(p).read_text(encoding="utf-8", errors="replace")
    cues = []
    for block in re.split(r"\n\s*\n", t):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        # drop index + timestamp lines
        lines = [l for l in lines if not re.match(r"^\d+$", l) and "-->" not in l]
        cues.extend(lines)
    return " ".join(cues)

def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()

NUMWORDS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30}

def numbers(s):
    nums = set(re.findall(r"\d+(?:\.\d+)?", s))
    nums.update(str(NUMWORDS[w]) for w in re.findall(r"[A-Za-z]+", s.lower())
                if w in NUMWORDS)
    return nums

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", required=True)
    ap.add_argument("--captions", required=True)
    ap.add_argument("--claims", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    errs = []
    narr = Path(a.narration).read_text(encoding="utf-8", errors="replace")
    cap = srt_text(a.captions)
    if norm(narr) != norm(cap):
        errs.append("narration/captions mismatch (texts differ after normalization)")
    claims_t = Path(a.claims).read_text(encoding="utf-8", errors="replace")
    claims = [l.strip() for l in claims_t.splitlines()
              if re.match(r"^\s*(-|\d+[.)])\s+\S", l)]
    if len(claims) < 3:
        errs.append(f"only {len(claims)} checkable claims, need >=3")
    src = Path(a.source).read_text(encoding="utf-8", errors="replace")
    src_nums = numbers(src)
    for c in claims:
        for n in numbers(c):
            if n not in src_nums:
                errs.append(f"possible contradiction (number {n} not in source): {c[:100]}")
    for f, t in (("narration", narr), ("claims", claims_t), ("captions", cap)):
        if KEY_RE.search(t):
            errs.append(f"possible API key in {f}")
    rep = {"claims_found": len(claims), "errors": errs}
    if a.json:
        print(json.dumps(rep, indent=2))
    else:
        print(f"claims={len(claims)} errors={len(errs)}")
        for e in errs:
            print(f"- {e}")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()
