# Canonical Limei 25

The 25 names and RGB values in `limei-25.json` are immutable for Limei 1.x.
They are the sole source of truth for every mapping, port, preview, and derived
color.

A change to any canonical name or hex value is a new palette identity and must
not be made through an ordinary port or generator update.

Run:

```bash
python3 scripts/check-canonical.py
```

to verify the ordered lock payload and hard-coded SHA-256 fingerprint.
