#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in ROOT.rglob("*"):
    if not path.is_file() or path.parts[-2] == "LICENSES":
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if "Dava" + "mos" in text:
        errors.append(f"old creator name remains in {path.relative_to(ROOT)}")

for base in [ROOT / "ports", ROOT / "templates"]:
    for path in base.rglob("*"):
        if not path.is_file() or path.name == "README.md":
            continue
        rel = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix == ".json":
            companion = path.parent / "README.md"
            own_credit = "harunnoir" in text
            companion_credit = companion.exists() and "harunnoir" in companion.read_text(encoding="utf-8")
            if not (own_credit or companion_credit):
                errors.append(f"comment-free port lacks companion attribution: {rel}")
            continue
        if "harunnoir" not in text:
            errors.append(f"missing harunnoir attribution: {rel}")
        if "SPDX-License-Identifier:" not in text:
            errors.append(f"missing SPDX identifier: {rel}")

if errors:
    print("Attribution validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("OK: attribution is consistently assigned to harunnoir.")
