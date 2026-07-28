#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in ROOT.rglob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

for path in ROOT.rglob("*.toml"):
    try:
        tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid TOML {path.relative_to(ROOT)}: {exc}")

try:
    import yaml
except ImportError:
    yaml = None
if yaml:
    for path in list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.yaml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid YAML {path.relative_to(ROOT)}: {exc}")
else:
    print("NOTE: PyYAML not installed; YAML syntax check skipped.")

for path in ROOT.rglob("*.sh"):
    result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    if result.returncode:
        errors.append(f"invalid shell {path.relative_to(ROOT)}: {result.stderr.strip()}")

if errors:
    print("Format validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print("OK: JSON, TOML, available YAML, and shell files parse correctly.")
