#!/usr/bin/env python3
"""Launch Streamlit UI from repo root (sets PYTHONPATH)."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("PYTHONPATH", str(ROOT / "src"))
app = ROOT / "streamlit_app" / "app.py"
sys.exit(subprocess.call([sys.executable, "-m", "streamlit", "run", str(app), "--server.headless", "true"]))
