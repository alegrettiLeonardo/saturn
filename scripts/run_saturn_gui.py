#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saturn_gui.model import SaturnProject


def main() -> int:
    ap = argparse.ArgumentParser(description="SATURN desktop interface for shaftOpt")
    ap.add_argument("--project-root", default=str(ROOT))
    ap.add_argument("--check", action="store_true", help="load project/model and exit without opening Tk")
    args = ap.parse_args()
    project = SaturnProject(args.project_root)
    if args.check:
        s = project.summary
        print("SATURN GUI CHECK")
        print(f"PROJECT={s.project_id}")
        print(f"SECTIONS={s.section_count}")
        print(f"DISKS={s.disk_count}")
        print(f"BEARINGS={s.bearing_count}")
        print(f"DESIGN_VARIABLES={len(project.design_variables)}")
        problems = project.validate_paths()
        print("STATUS=" + ("OK" if not problems else "FAIL"))
        for p in problems:
            print("PROBLEM=" + p)
        return 0 if not problems else 2

    try:
        from saturn_gui.app import SaturnApp
    except Exception as exc:
        print(f"SATURN GUI import failed: {exc}", file=sys.stderr)
        return 2
    app = SaturnApp(args.project_root)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
