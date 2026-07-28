#!/usr/bin/env python3
"""Verify Limei's semantic color use and generate a comfort report."""

from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/comfort-report.json"

canonical = json.loads(
    (ROOT / "palette/canonical/limei-25.json").read_text(encoding="utf-8")
)
c = {entry["id"]: entry["hex"].lower() for entry in canonical["ordered_colors"]}
roles = json.loads(
    (ROOT / "palette/mappings/ui-roles.json").read_text(encoding="utf-8")
)

expected_roles = {
    ("surfaces", "background"): c["background.base"],
    ("surfaces", "surface"): c["background.raised"],
    ("surfaces", "surface_selected"): c["background.selection"],
    ("surfaces", "surface_active"): c["background.active"],
    ("surfaces", "border"): c["foreground.subtle"],
    ("text", "primary"): c["foreground.base"],
    ("text", "secondary"): c["foreground.dim"],
    ("text", "muted"): c["foreground.muted"],
    ("text", "emphasis"): c["foreground.bright"],
    ("interaction", "focus"): c["warm.taupe"],
    ("interaction", "primary"): c["earth.sage"],
    ("interaction", "navigation"): c["earth.navigation"],
    ("interaction", "highlight"): c["earth.wheat"],
    ("semantic", "success"): c["earth.green"],
    ("semantic", "warning"): c["warm.amber"],
    ("semantic", "error"): c["warm.red"],
    ("semantic", "urgent"): c["warm.urgent"],
    ("semantic", "information"): c["cool.slate"],
    ("semantic", "visited"): c["cool.lavender"],
    ("semantic", "transform"): c["warm.orange"],
    ("semantic", "warm_interaction"): c["warm.clay"],
    ("semantic", "logic"): c["earth.olive"],
}

failures = []
checks = []
for (group, name), expected in expected_roles.items():
    actual = roles[group][name].lower()
    passed = actual == expected
    checks.append({
        "kind": "role",
        "name": f"{group}.{name}",
        "expected": expected,
        "actual": actual,
        "passed": passed,
    })
    if not passed:
        failures.append(f"{group}.{name}")

# Persistent large-surface colors must remain neutral.
neutral = {
    c["background.deep"], c["background.inactive"], c["background.base"],
    c["background.alternate"], c["background.raised"],
    c["background.selection"], c["background.active"],
}
for name in ("background", "background_deep", "surface", "surface_alternate",
             "surface_selected", "surface_active"):
    value = roles["surfaces"][name].lower()
    passed = value in neutral
    checks.append({
        "kind": "persistent-surface",
        "name": name,
        "actual": value,
        "passed": passed,
    })
    if not passed:
        failures.append(f"non-neutral persistent surface: {name}")

# A few high-impact port checks ensure the role mapping is actually used.
port_expectations = {
    "ports/desktop/niri/limei.kdl": [
        c["warm.taupe"], c["warm.red"], c["cool.slate"],
    ],
    "ports/desktop/mako/limei.conf": [
        c["warm.taupe"], c["cool.slate"], c["warm.red"], c["earth.green"],
    ],
    "ports/desktop/waybar/limei.css": [
        c["earth.navigation"], c["warm.amber"], c["warm.red"],
        c["cool.slate"], c["cool.lavender"],
    ],
    "ports/apps/helix/limei.toml": [
        c["warm.taupe"], c["earth.sage"], c["warm.clay"],
        c["cool.slate"], c["earth.olive"],
    ],
    "ports/apps/lazygit/limei.yml": [
        c["warm.taupe"], c["warm.amber"], c["warm.red"],
    ],
    "ports/shell/fzf/limei.sh": [
        c["warm.taupe"], c["earth.navigation"], c["earth.green"],
        c["warm.amber"], c["cool.slate"],
    ],
}

for relative, required in port_expectations.items():
    text = (ROOT / relative).read_text(encoding="utf-8").lower()
    missing = [value for value in required if value not in text]
    passed = not missing
    checks.append({
        "kind": "port-role-coverage",
        "name": relative,
        "missing": missing,
        "passed": passed,
    })
    if missing:
        failures.append(f"{relative} missing expected roles: {', '.join(missing)}")

report = {
    "meta": {
        "name": "Limei comfort and semantic-role report",
        "creator": "harunnoir",
        "version": (ROOT / "VERSION").read_text().strip(),
        "generated_by": "scripts/check-comfort.py",
        "note": (
            "This is a structural comfort check. Real long-session review "
            "on each application remains necessary."
        ),
    },
    "principles": [
        "Neutral colors dominate persistent surfaces.",
        "Selection is neutral rather than a large accent fill.",
        "Taupe represents focus and functional attention.",
        "Accents communicate meaning and are distributed by role.",
        "Muted text is not used for required body text.",
    ],
    "summary": {
        "checks": len(checks),
        "failures": failures,
    },
    "checks": checks,
}
expected = json.dumps(report, indent=2) + "\n"

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()

if args.check:
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if current != expected:
        print("comfort-report.json is out of date")
        sys.exit(1)
else:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")

if failures:
    print("Comfort validation failed:")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print(f"OK: {len(checks)} semantic comfort checks passed.")
