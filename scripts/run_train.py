#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from solvscreen.train_baseline import run_cli  # noqa: E402

if __name__ == "__main__":
    run_cli()
