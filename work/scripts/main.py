"""Project command-line entry point."""

from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))

from work.scripts.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
