#!/usr/bin/env python3
"""ste_audit.py — thin wrapper: runs ste_check + reports term drift (stdlib only)."""
import argparse, json, re, subprocess, sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--mode", default="descriptive")
    ap.add_argument("--terms", help="comma-separated canonical terms, e.g. leader,follower,candidate")
    ap.add_argument("--json", action="store_true", help="accepted for compatibility, output is always JSON")
    a = ap.parse_args()
    base = Path(__file__).resolve().parents[2] / "ste-explain" / "scripts" / "ste_check.py"
    out = subprocess.run([sys.executable, str(base), "--mode", a.mode, a.file, "--json"],
                         capture_output=True, text=True)
    try:
        rep = json.loads(out.stdout or "{}")
    except Exception:
        print(out.stdout); print(out.stderr, file=sys.stderr); sys.exit(2)
    text = Path(a.file).read_text(encoding="utf-8", errors="replace").lower()
    drift = []
    if a.terms:
        for t in [x.strip().lower() for x in a.terms.split(",") if x.strip()]:
            if not re.search(r"\b" + re.escape(t) + r"\b", text):
                drift.append({"missing_term": t})
        # naive drift hint: known confusing families
        for fam in (["worker", "agent", "executor"], ["begin", "commence", "initiate"]):
            found = [w for w in fam if re.search(r"\b"+w+r"\b", text)]
            if len(found) > 1:
                drift.append({"family_drift": found})
    print(json.dumps({"ste": rep, "drift": drift}, indent=2))
    sys.exit(1 if (rep.get("violations") or drift) else 0)

if __name__ == "__main__":
    main()
