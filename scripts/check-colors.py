#!/usr/bin/env python3
"""Check that ports use canonical colors or explicitly approved derivatives."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "palette/canonical/limei-25.json").read_text())
canonical = {entry["hex"].lower() for entry in source["ordered_colors"]}

ansi_derived = json.loads((ROOT / "palette/derived/ansi-bright.json").read_text())
approved_derived = {value.lower() for value in ansi_derived["colors"].values()}
allowed = canonical | approved_derived

hex_pattern = re.compile(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?")
rgb_pattern = re.compile(r"(?<![\d,])(\d{1,3}),(\d{1,3}),(\d{1,3})(?![\d,])")

ignored = {
    ROOT / "LICENSES/CC-BY-SA-4.0.txt",
    ROOT / "LICENSES/GPL-3.0-or-later.txt",
    ROOT / "palette/mappings/xterm256.json",
    ROOT / "scripts/generate.py",
}
ignored_prefixes = {
    ROOT / "palette/canonical",
    ROOT / "docs/contrast-report.json",
    ROOT / "docs/comfort-report.json",
}

unexpected = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path in ignored or path.suffix in {".svg", ".png", ".zip"}:
        continue
    if any(prefix == path or prefix in path.parents for prefix in ignored_prefixes):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue

    for match in hex_pattern.findall(text):
        rgb_hex = match[:7].lower()
        if rgb_hex not in allowed:
            unexpected.append((path.relative_to(ROOT), match))

    if path.suffix in {".colorscheme", ".gpl"} or path.name == "manifest.json":
        for match in rgb_pattern.finditer(text):
            values = tuple(int(match.group(i)) for i in range(1, 4))
            if not all(0 <= value <= 255 for value in values):
                continue
            value = "#" + "".join(f"{part:02x}" for part in values)
            if value not in allowed:
                unexpected.append((path.relative_to(ROOT), value))

if unexpected:
    print("Unapproved RGB colors found:")
    for path, color in unexpected:
        print(f"  {path}: {color}")
    sys.exit(1)

print(
    f"OK: ports use {len(canonical)} canonical colors and "
    f"{len(approved_derived)} approved ANSI derivatives."
)
