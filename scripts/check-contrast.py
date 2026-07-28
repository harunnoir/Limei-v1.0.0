#!/usr/bin/env python3
"""Generate and verify a role-aware Limei contrast report."""

from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/contrast-report.json"
source = json.loads((ROOT / "palette/canonical/limei-25.json").read_text())
c = {entry["id"]: entry["hex"] for entry in source["ordered_colors"]}


def channel(value):
    value /= 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(value):
    value = value.lstrip("#")
    r, g, b = [channel(int(value[i:i+2], 16)) for i in (0, 2, 4)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)

pairs = [
    ("body-text", c["foreground.base"], c["background.base"], "required-aa", 4.5),
    ("bright-text", c["foreground.bright"], c["background.base"], "required-aa", 4.5),
    ("dim-text", c["foreground.dim"], c["background.base"], "required-aa", 4.5),
    ("muted-text", c["foreground.muted"], c["background.base"], "intentional-low-emphasis", 3.0),
    ("border", c["foreground.subtle"], c["background.base"], "decorative", 1.2),
    ("ansi-black", c["foreground.subtle"], c["background.base"], "intentional-low-emphasis", 1.2),
]
for token in ["warm.red", "warm.urgent", "warm.orange", "warm.amber", "warm.clay", "warm.taupe", "earth.green", "earth.sage", "earth.wheat", "earth.navigation", "earth.olive", "cool.slate", "cool.lavender"]:
    pairs.append((f"{token}-text", c[token], c["background.base"], "accent-text", 4.5))
    pairs.append((f"on-{token}", c["background.base"], c[token], "text-on-accent", 4.5))

entries = []
failures = []
for name, foreground, background, category, threshold in pairs:
    value = round(ratio(foreground, background), 3)
    passed = value >= threshold
    entries.append({
        "name": name, "foreground": foreground, "background": background,
        "category": category, "threshold": threshold, "contrast_ratio": value,
        "passed": passed,
    })
    if not passed and category in {"required-aa", "accent-text", "text-on-accent"}:
        failures.append(name)

report = {
    "meta": {
        "name": "Limei role-aware contrast report", "creator": "harunnoir",
        "generated_by": "scripts/check-contrast.py", "derived_from": "palette/canonical/limei-25.json",
        "standard": "WCAG relative luminance and contrast ratio",
        "note": "Only roles intended for readable text fail validation. Decorative and intentionally low-emphasis roles use role-specific thresholds.",
    },
    "summary": {"checks": len(entries), "required_failures": failures},
    "checks": entries,
}
expected = json.dumps(report, indent=2) + "\n"

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
if args.check:
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if current != expected:
        print("contrast-report.json is out of date")
        sys.exit(1)
else:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")

if failures:
    print("Required contrast checks failed: " + ", ".join(failures))
    sys.exit(1)
print(f"OK: {len(entries)} role-aware contrast checks passed their required thresholds.")
