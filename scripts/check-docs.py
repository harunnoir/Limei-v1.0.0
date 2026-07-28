#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), 1):
        if line.endswith(" ") or line.endswith("\t"):
            errors.append(f"trailing whitespace: {path.relative_to(ROOT)}:{number}")
        if "\t" in line:
            errors.append(f"tab in Markdown: {path.relative_to(ROOT)}:{number}")
    if "Dava" + "mos" in text:
        errors.append(f"old attribution in {path.relative_to(ROOT)}")

palette = (ROOT / "palette/README.md").read_text(encoding="utf-8")
if "    Limei contains" in palette or "    ## ANSI" in palette:
    errors.append("palette/README.md still contains accidental code-block indentation")

if errors:
    print("Documentation validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
print("OK: Markdown formatting checks passed.")
