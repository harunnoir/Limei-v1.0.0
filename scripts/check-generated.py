#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
result = subprocess.run([sys.executable, str(root / "scripts/generate.py"), "--check"])
raise SystemExit(result.returncode)
