# Limei color layers

Limei has **25 immutable canonical colors**. Compatibility mappings and derived
colors are kept separate so Limei can support different software without
changing its identity.

## Canonical Limei 25

The only source of truth is:

```text
palette/canonical/limei-25.json
```

| Name | Token | Hex | Suggested role |
|---|---|---:|---|
| Deep | `background.deep` | `#080808` | Deepest background |
| Inactive | `background.inactive` | `#0c0c0c` | Inactive or recessed background |
| Base | `background.base` | `#101010` | Main background |
| Alternate | `background.alternate` | `#141414` | Alternate background |
| Raised | `background.raised` | `#171717` | Raised surface |
| Selection | `background.selection` | `#292724` | Selection background |
| Active | `background.active` | `#302d29` | Active surface |
| Subtle | `foreground.subtle` | `#393632` | Borders and hidden UI |
| Muted | `foreground.muted` | `#64605a` | Muted text |
| Dim | `foreground.dim` | `#837f78` | Secondary text |
| Foreground | `foreground.base` | `#ada9a3` | Main text |
| Bright | `foreground.bright` | `#c0bbb3` | High-emphasis text |
| Red | `warm.red` | `#9a7477` | Errors and destructive states |
| Urgent | `warm.urgent` | `#9b7469` | Urgent and conflict states |
| Orange | `warm.orange` | `#9c795e` | Transforms and replacements |
| Amber | `warm.amber` | `#a38762` | Warnings |
| Clay | `warm.clay` | `#9a7869` | Warm interaction accent |
| Taupe | `warm.taupe` | `#9a897c` | Focus and functional accent |
| Green | `earth.green` | `#768569` | Success and additions |
| Sage | `earth.sage` | `#7f8c77` | Primary earth accent |
| Wheat | `earth.wheat` | `#97916f` | Types and soft highlights |
| Navigation | `earth.navigation` | `#918862` | Navigation state |
| Olive | `earth.olive` | `#898661` | Logic and secondary earth accent |
| Slate | `cool.slate` | `#788184` | Information and links |
| Lavender | `cool.lavender` | `#8d818a` | Constants and visited states |

The ordered names and values are locked by:

```text
palette/canonical/limei-25.lock.json
palette/canonical/limei-25.sha256
```

## Official ANSI 16 mapping

ANSI terminals require eight normal and eight bright slots. This mapping is
stable and generated from the canonical palette:

| Slot | Normal | Bright |
|---|---:|---:|
| Black | `#393632` | `#64605a` |
| Red | `#9a7477` | `#9b7469` |
| Green | `#768569` | `#7f8c77` |
| Yellow | `#a38762` | `#97916f` |
| Blue | `#788184` | `#837f78` |
| Magenta | `#8d818a` | `#9a7869` |
| Cyan | `#7f8c77` | `#9a897c` |
| White | `#ada9a3` | `#c0bbb3` |

ANSI black uses `#393632`, not the `#101010` terminal background, so black text
remains visible. Normal cyan and bright green intentionally share sage because
Limei has a compact, muted hue range and semantic consistency is more important
than forcing artificial colors.

## xterm-256 mapping

`palette/mappings/xterm256.json` maps every canonical Limei color to the nearest
fixed xterm index in the range 16–255. It does not claim that a terminal theme
can redefine the fixed xterm cube.

## Derived colors

`palette/derived/` contains generated colors such as alpha overlays. Derived
colors are never canonical and never replace any of the original 25 colors.

## Compatibility exports

`palette/limei.json` and `palette/limei.yml` are generated compatibility files.
Do not edit them directly.
