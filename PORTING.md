# Porting Limei

Use `palette/canonical/limei-25.json` as the **only source of truth**.
The 25 canonical names and hex values are immutable.

## Surface hierarchy

| Role | Color |
|---|---:|
| Deep background | `#080808` |
| Main background | `#101010` |
| Alternate background | `#141414` |
| Raised surface | `#171717` |
| Selection | `#292724` |
| Active surface | `#302d29` |
| Border | `#393632` |

## Text hierarchy

| Role | Color |
|---|---:|
| Muted | `#64605a` |
| Dim | `#837f78` |
| Main | `#ada9a3` |
| Bright | `#c0bbb3` |

## Accent balance

- Green and sage: success, additions, or one primary state.
- Clay and taupe: warm interaction, functions, and focus.
- Wheat and amber: soft highlights and warnings.
- Slate and lavender: information and secondary navigation.
- Olive and navigation: logic and earthy secondary structure.
- Red and urgent: destructive, error, conflict, or urgent states only.

Do not assign sage to every active component. Neutral surfaces should remain
dominant, and accents should clarify hierarchy rather than decorate everything.

## ANSI and indexed terminals

Use the official mapping in `palette/mappings/ansi16.json`. Do not invent a
per-port ANSI mapping. For indexed terminal applications, use
`palette/mappings/xterm256.json` to find the nearest fixed xterm index.

## Derived values

Ramps, gradients, overlays, and high-contrast alternatives are derived Limei.
They must never overwrite, rename, or be presented as members of the canonical
25-color palette.

For transparency, append an alpha byte to a canonical RGB color:

```text
#7f8c7780
```

## File header

Configuration ports should include:

```text
Limei by harunnoir
SPDX-License-Identifier: GPL-3.0-or-later
Colors: CC-BY-SA-4.0
```

JSON or other comment-free formats need a companion README containing the same
attribution and license information.
