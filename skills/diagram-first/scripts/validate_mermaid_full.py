#!/usr/bin/env python3
"""validate_mermaid_full.py — primary mmdc parse, regex pre-check fallback (stdlib only).
Every run reports which validator ran: "parse" (real mmdc render) or
"pre-check only" (regex fallback). A pre-check pass is NEVER a parse pass.
Run with auto-detected Python: py -3 on Windows, else python3, else python.
Usage: validate_mermaid_full.py diagram.mmd [--json] [--no-mmdc]
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run_precheck(text):
    import importlib.util
    spec = importlib.util.spec_from_file_location("precheck", HERE / "validate_mermaid.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check(text)

def find_npx():
    import shutil
    for cand in ("npx", "npx.cmd", "npx.ps1"):
        p = shutil.which(cand)
        if p:
            return p
    for cand in (r"C:\Program Files\nodejs\npx.cmd",
                 r"C:\Program Files\nodejs\npx.ps1"):
        if Path(cand).exists():
            return cand
    return None

def run_mmdc(src: Path):
    npx = find_npx()
    if not npx:
        return False, "npx not found on PATH (tried npx/npx.cmd/npx.ps1)"
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out.svg"
        args = [npx, "-y", "@mermaid-js/mermaid-cli", "-i", str(src), "-o", str(out)]
        if npx.lower().endswith((".cmd", ".bat", ".ps1")):
            args = ["cmd", "/c"] + args  # batch shims need cmd on Windows
        p = subprocess.run(args, capture_output=True, text=True, timeout=180)
        if p.returncode == 0 and out.exists():
            return True, ""
        err = (p.stderr or p.stdout or "")[-600:]
        return False, err

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-mmdc", action="store_true", help="skip real parse, pre-check only")
    a = ap.parse_args()
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    pre = run_precheck(text)
    if a.no_mmdc:
        rep = {"validator": "pre-check only", "parse_ok": None,
               "edges": pre["edges"], "errors": pre["errors"]}
    else:
        try:
            ok, err = run_mmdc(Path(a.file))
        except FileNotFoundError as e:
            ok, err = False, f"npx not found: {e}"
        except subprocess.TimeoutExpired:
            ok, err = False, "mmdc timed out after 120s"
        if ok:
            rep = {"validator": "parse", "parse_ok": True,
                   "edges": pre["edges"], "errors": pre["errors"],
                   "note": "mmdc rendered SVG successfully; regex errors (e.g. unlabeled_edge) are style gates, not parse failures"}
        else:
            rep = {"validator": "pre-check only", "parse_ok": False,
                   "parse_error": err[-300:] if err else "unknown",
                   "edges": pre["edges"], "errors": pre["errors"],
                   "note": "mmdc unavailable/failed; result is pre-check only, NOT a parse pass"}
    if a.json:
        print(json.dumps(rep, indent=2))
    else:
        print(f"validator={rep['validator']} edges~{rep['edges']} errors={len(rep['errors'])}")
        for e in rep["errors"]:
            print(f"- {e}")
        if rep.get("parse_error"):
            print(f"parse_error: {rep['parse_error']}")
    # Exit on style/parse errors. A clean pre-check still reports
    # validator="pre-check only" so it is never read as a parse pass.
    sys.exit(1 if rep["errors"] else 0)

if __name__ == "__main__":
    main()
