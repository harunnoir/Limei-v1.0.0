# Color-system architecture

## Canonical

`palette/canonical/limei-25.json` contains the immutable Limei identity.
The exact ordered token/hex payload is protected by a lock file, a stored
SHA-256 fingerprint, a hard-coded validator fingerprint, and CI.

## Mappings

Mappings adapt canonical colors to fixed external systems:

- ANSI 16 for terminal compatibility;
- terminal special colors;
- nearest fixed xterm-256 indices.

Mappings may select or reuse canonical colors, but they do not create canonical
colors.

## Derived

Derived outputs may add alpha, ramps, gradients, or accessibility alternatives.
They must identify their source and generation method and must never be described
as part of the canonical 25.

## Ports

Generated terminal ports are reproduced by `scripts/generate.py`. Other ports
are hand-maintained but validated so every RGB value comes from the canonical
palette, except documented alpha variants and fixed xterm mapping values.
