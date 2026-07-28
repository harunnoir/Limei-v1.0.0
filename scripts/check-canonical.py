#!/usr/bin/env python3
"""Verify the immutable Limei 25 ordered token/hex payload."""

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = "ab4856baa6f2f3bba89372d39a8aee6d05f015ec5fc07a3c92b656dcae1f2763"
EXPECTED_COUNT = 25

source = json.loads((ROOT / "palette/canonical/limei-25.json").read_text())
lock = json.loads((ROOT / "palette/canonical/limei-25.lock.json").read_text())
ordered = [{"id": entry["id"], "hex": entry["hex"].lower()} for entry in source["ordered_colors"]]
payload = json.dumps(ordered, ensure_ascii=False, separators=(",", ":")).encode()
digest = hashlib.sha256(payload).hexdigest()

errors = []
if len(ordered) != EXPECTED_COUNT:
    errors.append(f"expected {EXPECTED_COUNT} colors, found {len(ordered)}")
if source["meta"].get("canonical") is not True or source["meta"].get("immutable") is not True:
    errors.append("canonical and immutable metadata must both be true")
if source["meta"].get("creator") != "harunnoir":
    errors.append("creator must be harunnoir")
if ordered != lock.get("ordered_colors"):
    errors.append("canonical ordered colors differ from the lock file")
if digest != EXPECTED_SHA256:
    errors.append(f"canonical SHA-256 changed: {digest}")
if lock.get("meta", {}).get("sha256") != EXPECTED_SHA256:
    errors.append("lock metadata SHA-256 is incorrect")
sha_file = (ROOT / "palette/canonical/limei-25.sha256").read_text().split()[0]
if sha_file != EXPECTED_SHA256:
    errors.append("limei-25.sha256 is incorrect")

if errors:
    print("Canonical Limei validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(f"OK: immutable Limei 25 fingerprint {digest}")
