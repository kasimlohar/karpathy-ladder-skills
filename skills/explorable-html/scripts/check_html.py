#!/usr/bin/env python3
"""check_html.py — static checks for explainer.html (stdlib only)."""
import argparse, re, sys
from pathlib import Path
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); a = ap.parse_args()
    t = Path(a.file).read_text(encoding="utf-8", errors="replace")
    errs = []
    if "<script src=" in t and "integrity=" not in t:
        errs.append("cdn without integrity hash")
    if "Guess" not in t and "guess" not in t:
        errs.append("missing guess-first control")
    if "Assumption" not in t and "assumption" not in t:
        errs.append("missing assumptions panel")
    if "http" in t and "Sources" not in t and "sources" not in t:
        errs.append("external link without Sources footer?")
    print(f"errors={len(errs)} size={len(t)}")
    for e in errs: print(f"- {e}")
    sys.exit(1 if errs else 0)
if __name__ == "__main__": main()
