# Limei comfort guidelines

Limei is not successful merely because a configuration contains the correct
hex values. Color must be assigned by **area, persistence, frequency,
contrast, and meaning**.

## 1. Area

Large surfaces stay neutral:

- main background: `#101010`
- raised surface: `#171717`
- selection: `#292724`
- active surface: `#302d29`

Accent-filled backgrounds are reserved for small controls, urgent states,
short-lived indicators, and compact mode labels.

## 2. Persistence

Elements visible all day should be quiet. Persistent window borders, bars,
inactive tabs, sidebars, and panels use neutral colors or one restrained
focus accent.

Temporary states may be stronger:

- search match: wheat
- warning: amber
- error: red
- information: slate
- success: green

## 3. Frequency

A common state must be quieter than a rare state. Normal battery, CPU, and
memory modules remain dim; warning and critical states receive color.
Ordinary tabs use neutral surfaces; only focus and activity need accents.

## 4. Semantic roles

| Meaning | Limei role |
|---|---|
| Focus / keyboard attention | Taupe |
| Primary action / small active indicator | Sage |
| Navigation | Navigation |
| Success / addition / progress | Green |
| Soft highlight / type | Wheat |
| Warning | Amber |
| Error / destructive action | Red |
| Urgent conflict | Urgent |
| Information / links | Slate |
| Visited / secondary cool state | Lavender |
| Warm interaction / mode | Clay |
| Transform / replacement | Orange |
| Logic / secondary earth state | Olive |

## 5. Balance

Balance does not mean showing every accent at the same time. It means not
using one accent for unrelated roles. A launcher may need taupe, navigation,
and red; an editor may use most accents; a notification may need only taupe,
slate, green, amber, and red.

## 6. Text

- Main body text uses `#ada9a3`.
- Secondary readable text uses `#837f78`.
- `#64605a` is reserved for intentionally low-emphasis content.
- `#c0bbb3` is used sparingly for emphasis.
- Required text should not be placed in the border color `#393632`.

## 7. Selection and focus

Selection and focus are separate:

- selection is a neutral surface (`#292724` or `#302d29`);
- keyboard focus is taupe (`#9a897c`);
- primary action can be sage (`#7f8c77`).

This prevents every selected row, tab, pane, and button from becoming a
large green block.

## 8. Validation

Automated checks can validate roles, contrast, reproducibility, and approved
colors. They cannot prove long-session comfort. Each port still needs manual
review in its real application at normal brightness for several hours.
