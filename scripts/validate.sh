#!/usr/bin/env bash
set -Eeuo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

python3 scripts/check-canonical.py
python3 scripts/check-generated.py
python3 scripts/check-colors.py
python3 scripts/check-attribution.py
python3 scripts/check-ansi.py
python3 scripts/check-formats.py
python3 scripts/check-docs.py
python3 scripts/check-contrast.py --check
python3 scripts/check-comfort.py --check
