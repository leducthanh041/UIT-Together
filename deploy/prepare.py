"""Compatibility entry point: the canonical artifact is now dist/."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/build.py"), run_name="__main__")
