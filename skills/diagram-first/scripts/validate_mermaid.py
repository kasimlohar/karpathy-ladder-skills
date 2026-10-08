#!/usr/bin/env python3
"""validate_mermaid.py — lightweight Mermaid syntax pre-check (stdlib only).
Full validation via mermaid.parse / mmdc when available.
Usage: python3 validate_mermaid.py diagram.mmd [--json]
Exit 0 if no blocking errors, 1 otherwise.
"""
import argparse, json, re, sys
from pathlib import Path

BAD_ARROW = re.compile(r"--<|--\|[^|\n]*\|\s*\w")  # --< or --|label| missing second dash handled below
ARROW_RE = re.compile(r"-->|->>|-->>|==>|-.->|-->\\|")
LABEL_PIPE = re.compile(r"--\|")

def check(text):
    errors = []
    lines = text.splitlines()
    fst = "\n".join(lines[:5])
    if "flowchart" not in text and "sequenceDiagram" not in text and "graph " not in text:
        errors.append({"type": "no_diagram_type", "note": "missing flowchart/graph/sequenceDiagram header"})
    if "--<" in text:
        errors.append({"type": "bad_arrow", "note": "found --<, use --> "})
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if not s or s.startswith("%%"):
            continue
        # --|label| pipe form without --> is malformed (needs -->|label|)
        if re.search(r"--\|[^|\n]+\|", s) and "-->" not in s:
            errors.append({"type": "arrow_label", "line": i, "text": s[:100]})
    # participant consistency for sequence diagrams
    if "sequenceDiagram" in text:
        parts = set(re.findall(r"participant\s+(\w+)", text))
        msgs = re.findall(r"(\w+)\s*-?->+[>\-]*\s*(\w+)\s*:", text)
        for a, b in msgs:
            if a not in parts and a.lower() not in ("actor", "participant"):
                errors.append({"type": "unknown_participant", "name": a})
    # edge count includes broken attempts so count-match does not understate
    edges = len(re.findall(r"-->|->>|-->>|--<", text))
    # flowchart unlabeled arrows: flag bare --> without |label|
    if "flowchart" in text or re.search(r"(?m)^\s*graph\s", text):
        for i, ln in enumerate(lines, 1):
            s = ln.strip()
            if not s or s.startswith("%%"):
                continue
            if "-->" in s and "-->|" not in s:
                errors.append({"type": "unlabeled_edge", "line": i, "text": s[:100]})
    return {"edges": edges, "errors": errors}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    rep = check(text)
    if a.json:
        print(json.dumps(rep, indent=2))
    else:
        print(f"edges~{rep['edges']} errors={len(rep['errors'])}")
        for e in rep["errors"]:
            print(f"- {e}")
    sys.exit(1 if rep["errors"] else 0)

if __name__ == "__main__":
    main()
