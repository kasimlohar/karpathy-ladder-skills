#!/usr/bin/env python3
"""ste_check.py — deterministic 80% STE checker (stdlib only).
Checks are advisory, not a substitute for the official ASD-STE100 spec.
Limits load from skills/shared/ste-limits.json (verified against Issue 9 PDF);
override via --config. Run with auto-detected Python: py -3 on Windows,
else python3, else python.
Usage:
  ste_check.py --mode procedural|descriptive draft.txt [--json] [--config other.json]
"""
import argparse, json, re, sys
from pathlib import Path

SHARED_CONFIG = Path(__file__).resolve().parents[2] / "shared" / "ste-limits.json"
# Packed installs (.skill zips) may bundle the config inside the skill folder.
PACKED_CONFIG = Path(__file__).resolve().parents[1] / "shared" / "ste-limits.json"

def load_defaults():
    for cand in (SHARED_CONFIG, PACKED_CONFIG):
        try:
            cfg = json.loads(cand.read_text(encoding="utf-8"))
            return {k: cfg[k] for k in ("procedural_max_words", "descriptive_max_words", "max_sentences_per_para") if k in cfg} | {"provenance": cfg.get("provenance", ""), "verified": cfg.get("verified", False)}
        except Exception:
            continue
    return {
            "procedural_max_words": 20,
            "descriptive_max_words": 25,
            "max_sentences_per_para": 6,
            "provenance": "FALLBACK — shared/ste-limits.json unreadable",
            "verified": False,
        }

DEFAULTS = load_defaults()

ING_RE = re.compile(r"\b([A-Za-z]+ing)\b")
PASSIVE_RE = re.compile(r"\b(is|are|was|were|be|been|being)\s+\w+(ed|en)\b", re.I)
COND_WORDS = ("if ", "when ", "after ", "before ")
APPROVED_ING_NOUNS = {"opening", "remaining", "something", "during", "morning", "evening"}

def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]

def check_file(path, mode, cfg):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    limit = cfg["procedural_max_words"] if mode == "procedural" else cfg["descriptive_max_words"]
    paras = [p for p in text.split("\n\n") if p.strip()]
    violations = []
    sents = split_sentences(text)
    for i, s in enumerate(sents, 1):
        words = re.findall(r"[A-Za-z0-9'-]+", s)
        if len(words) > limit:
            violations.append({"type": "long_sentence", "sentence": i, "words": len(words), "limit": limit, "text": s[:120]})
        for m in ING_RE.finditer(s):
            w = m.group(1).lower()
            if w not in APPROVED_ING_NOUNS:
                violations.append({"type": "ing_form", "sentence": i, "word": w})
                break
        if mode == "procedural" and PASSIVE_RE.search(s):
            violations.append({"type": "passive_procedural", "sentence": i, "text": s[:120]})
        low = s.lower()
        if any(k in low for k in ("ensure that", "make sure that")) and not low.startswith(("if ", "when ")):
            # advisory: condition-first may apply
            pass
    for pi, p in enumerate(paras, 1):
        n = len(split_sentences(p))
        if n > cfg["max_sentences_per_para"]:
            violations.append({"type": "long_paragraph", "para": pi, "sentences": n})
    # semicolons / contractions advisory
    if ";" in text:
        violations.append({"type": "semicolon", "note": "avoid semicolons, split sentences"})
    return {"sentences": len(sents), "avg_words": round(sum(len(re.findall(r"[A-Za-z0-9'-]+", s)) for s in sents)/max(len(sents),1), 1),
            "violations": violations, "config_provenance": cfg.get("provenance", "")}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--mode", choices=["procedural", "descriptive"], default="descriptive")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--config")
    a = ap.parse_args()
    cfg = dict(DEFAULTS)
    if a.config:
        try:
            cfg.update(json.loads(Path(a.config).read_text()))
        except Exception as e:
            print(f"config error: {e}", file=sys.stderr)
            sys.exit(2)
    rep = check_file(a.file, a.mode, cfg)
    if a.json:
        print(json.dumps(rep, indent=2))
    else:
        print(f"sentences={rep['sentences']} avg={rep['avg_words']} violations={len(rep['violations'])}")
        for v in rep["violations"]:
            print(f"- {v}")
        print(f"limits: {cfg['procedural_max_words']}/{cfg['descriptive_max_words']} ({cfg['provenance'][:40]}...)")
    sys.exit(1 if rep["violations"] else 0)

if __name__ == "__main__":
    main()
