#!/usr/bin/env python3
"""Generate deterministic Limei mappings, templates, and terminal ports."""

from __future__ import annotations

from pathlib import Path
import argparse
import colorsys
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "palette/canonical/limei-25.json"
VERSION_FILE = ROOT / "VERSION"


def load_source():
    doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    colors = {entry["id"]: entry["hex"].lower() for entry in doc["ordered_colors"]}
    return doc, colors


def jt(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


def rgb_text(value):
    return ",".join(str(part) for part in rgb(value))


def header(prefix):
    lines = [
        "Limei by harunnoir",
        "SPDX-License-Identifier: GPL-3.0-or-later",
        "Colors: CC-BY-SA-4.0",
        "DO NOT EDIT DIRECTLY. Generated from palette/canonical/limei-25.json.",
    ]
    if prefix == "/*":
        return "/*\n" + "\n".join(f" * {line}" for line in lines) + "\n */\n"
    return "\n".join(f"{prefix} {line}" for line in lines) + "\n"


def xterm_palette():
    base16 = [
        "#000000", "#800000", "#008000", "#808000", "#000080", "#800080", "#008080", "#c0c0c0",
        "#808080", "#ff0000", "#00ff00", "#ffff00", "#0000ff", "#ff00ff", "#00ffff", "#ffffff",
    ]
    result = list(base16)
    levels = [0, 95, 135, 175, 215, 255]
    for r in levels:
        for g in levels:
            for b in levels:
                result.append(f"#{r:02x}{g:02x}{b:02x}")
    for step in range(24):
        v = 8 + step * 10
        result.append(f"#{v:02x}{v:02x}{v:02x}")
    return result


def srgb_to_lab(value):
    r, g, b = [part / 255 for part in rgb(value)]
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047
    y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750)
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883
    def f(t):
        d = 6 / 29
        return t ** (1 / 3) if t > d ** 3 else t / (3 * d * d) + 4 / 29
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta76(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def nearest_xterm(value):
    # Indices 16..255 are fixed. Slots 0..15 are theme-controlled and are
    # intentionally excluded from nearest-index compatibility mapping.
    palette = xterm_palette()
    target = srgb_to_lab(value)
    candidates = [(delta76(target, srgb_to_lab(palette[i])), i, palette[i]) for i in range(16, 256)]
    return min(candidates)


def build_outputs():
    doc, c = load_source()
    project_version = VERSION_FILE.read_text(encoding="utf-8").strip()
    bg = c["background.base"]
    deep = c["background.deep"]
    alt = c["background.alternate"]
    surface = c["background.raised"]
    selection = c["background.selection"]
    active = c["background.active"]
    border = c["foreground.subtle"]
    muted = c["foreground.muted"]
    dim = c["foreground.dim"]
    fg = c["foreground.base"]
    bright_fg = c["foreground.bright"]
    red = c["warm.red"]
    urgent = c["warm.urgent"]
    orange = c["warm.orange"]
    amber = c["warm.amber"]
    clay = c["warm.clay"]
    taupe = c["warm.taupe"]
    green = c["earth.green"]
    sage = c["earth.sage"]
    wheat = c["earth.wheat"]
    navigation = c["earth.navigation"]
    olive = c["earth.olive"]
    slate = c["cool.slate"]
    lavender = c["cool.lavender"]

    normal = {
        "black": border, "red": red, "green": green, "yellow": amber,
        "blue": slate, "magenta": lavender, "cyan": sage, "white": fg,
    }
    # ANSI bright colors are approved derived Limei values. They preserve the
    # normal slot's hue while raising lightness only slightly, keeping the
    # terminal comfortable and every bright slot visually distinct.
    derived_brights = {
        "red": "#a88386",
        "green": "#859479",
        "yellow": "#b29673",
        "blue": "#879093",
        "magenta": "#9c9099",
        "cyan": "#8e9b87",
    }
    brights = {
        "black": muted,
        "red": derived_brights["red"],
        "green": derived_brights["green"],
        "yellow": derived_brights["yellow"],
        "blue": derived_brights["blue"],
        "magenta": derived_brights["magenta"],
        "cyan": derived_brights["cyan"],
        "white": bright_fg,
    }
    special = {
        "background": bg, "foreground": fg, "cursor": taupe,
        "cursor_text": bg, "selection_background": selection,
        "selection_foreground": bright_fg,
    }

    generated_meta = {
        "name": "Limei", "creator": "harunnoir", "version": project_version,
        "canonical": False, "generated": True,
        "derived_from": "palette/canonical/limei-25.json",
        "generator": "scripts/generate.py",
    }

    compatibility = {
        "meta": {**generated_meta, "kind": "compatibility-export", "license": "CC-BY-SA-4.0"},
        "colors": doc["groups"], "semantic": doc["semantic"],
        "terminal": {"normal": normal, "bright": brights, **special},
    }

    yaml_lines = [
        "# Limei by harunnoir", "# SPDX-License-Identifier: CC-BY-SA-4.0",
        "# DO NOT EDIT DIRECTLY. Generated from palette/canonical/limei-25.json.",
        "name: Limei", "creator: harunnoir", f"version: {project_version}", "canonical: false",
        "generated: true", "derived_from: palette/canonical/limei-25.json", "", "colors:",
    ]
    for group, values in doc["groups"].items():
        yaml_lines.append(f"  {group}:")
        for name, value in values.items():
            yaml_lines.append(f'    {name}: "{value}"')
    yaml_lines += ["", "semantic:"]
    for name, value in doc["semantic"].items():
        yaml_lines.append(f'  {name}: "{value}"')
    yaml_lines += ["", "terminal:", "  normal:"]
    for name, value in normal.items():
        yaml_lines.append(f'    {name}: "{value}"')
    yaml_lines.append("  bright:")
    for name, value in brights.items():
        yaml_lines.append(f'    {name}: "{value}"')
    for name, value in special.items():
        yaml_lines.append(f'  {name}: "{value}"')
    yaml_text = "\n".join(yaml_lines) + "\n"

    ansi_doc = {
        "meta": {
            **generated_meta, "kind": "official-ansi16-mapping", "stable": True,
            "license": "CC-BY-SA-4.0",
            "notes": [
                "ANSI black is foreground.subtle rather than the terminal background, so black text remains visible.",
                "Normal slots use canonical Limei colors.",
                "Bright red, green, yellow, blue, magenta, and cyan are approved derived Limei colors that preserve hue and remain muted.",
            ],
        },
        "normal": normal, "bright": brights,
    }
    ansi_bright_doc = {
        "meta": {
            **generated_meta,
            "kind": "approved-derived-ansi-bright-colors",
            "canonical": False,
            "license": "CC-BY-SA-4.0",
            "method": "OKLab lightness lift of approximately 0.05 with a small chroma reduction",
            "purpose": "Keep ANSI bright slots distinct and hue-related without making them harsh.",
        },
        "colors": derived_brights,
    }

    ui_roles = {
        "meta": {
            **generated_meta,
            "kind": "official-ui-role-mapping",
            "canonical": False,
            "license": "CC-BY-SA-4.0",
            "note": "Roles point to immutable canonical colors; this mapping controls how Limei is used, not only which colors exist.",
        },
        "surfaces": {
            "background": bg,
            "background_deep": deep,
            "surface": surface,
            "surface_alternate": alt,
            "surface_selected": selection,
            "surface_active": active,
            "border": border,
        },
        "text": {
            "primary": fg,
            "secondary": dim,
            "muted": muted,
            "emphasis": bright_fg,
            "on_accent": bg,
        },
        "interaction": {
            "focus": taupe,
            "primary": sage,
            "navigation": navigation,
            "cursor": taupe,
            "selection": selection,
            "highlight": wheat,
        },
        "semantic": {
            "success": green,
            "warning": amber,
            "error": red,
            "urgent": urgent,
            "information": slate,
            "visited": lavender,
            "transform": orange,
            "warm_interaction": clay,
            "logic": olive,
        },
        "comfort_rules": [
            "Persistent large surfaces use neutral colors.",
            "Selections use neutral surface colors rather than saturated accent fills.",
            "Taupe is the default focus and functional accent.",
            "Sage is reserved for primary actions, success-adjacent states, and small active indicators.",
            "Accent colors communicate state and hierarchy; they are not decoration.",
        ],
    }

    ansi_toml = [
        "# Limei by harunnoir", "# SPDX-License-Identifier: CC-BY-SA-4.0",
        "# DO NOT EDIT DIRECTLY. Generated from palette/canonical/limei-25.json.",
        "", "[normal]",
    ]
    ansi_toml += [f'{name} = "{value}"' for name, value in normal.items()]
    ansi_toml += ["", "[bright]"]
    ansi_toml += [f'{name} = "{value}"' for name, value in brights.items()]
    ansi_toml.append("")

    xterm_entries = []
    for entry in doc["ordered_colors"]:
        distance, index, nearest = nearest_xterm(entry["hex"])
        xterm_entries.append({
            "token": entry["id"], "source_hex": entry["hex"],
            "nearest_fixed_xterm_index": index, "nearest_fixed_xterm_hex": nearest,
            "delta_e_76": round(distance, 3),
        })
    xterm_doc = {
        "meta": {
            **generated_meta, "kind": "fixed-xterm256-nearest-index-map",
            "license": "CC-BY-SA-4.0",
            "index_range": "16-255",
            "method": "nearest CIE Lab color using Delta E 1976",
            "note": "Indices 0-15 are excluded because terminal themes redefine those ANSI slots.",
        },
        "mappings": xterm_entries,
    }

    alpha_levels = [10, 20, 30, 40, 50, 60, 70]
    alpha_doc = {
        "meta": {
            **generated_meta, "kind": "derived-alpha-overlays", "license": "CC-BY-SA-4.0",
            "canonical": False,
            "note": "RGB components remain canonical; only alpha bytes are appended.",
        },
        "overlays": {},
    }
    for token in ["background.deep", "background.selection", "earth.sage", "warm.red", "cool.slate"]:
        base = c[token]
        alpha_doc["overlays"][token] = {
            f"{level}%": base + f"{round(level * 255 / 100):02x}" for level in alpha_levels
        }

    css_names = {entry["id"].replace('.', '-'): entry["hex"] for entry in doc["ordered_colors"]}
    css = header("/*") + ":root {\n" + "\n".join(
        f"  --limei-{name}: {value};" for name, value in css_names.items()
    ) + "\n}\n"
    scss = header("/*") + "\n".join(
        f"$limei-{name}: {value};" for name, value in css_names.items()
    ) + "\n"
    lua = header("--") + "return {\n" + "\n".join(
        f'  ["{entry["id"]}"] = "{entry["hex"]}",' for entry in doc["ordered_colors"]
    ) + "\n}\n"
    py = header("#") + "PALETTE = " + repr({entry["id"]: entry["hex"] for entry in doc["ordered_colors"]}) + "\n"
    gpl = [
        "GIMP Palette", "Name: Limei", "Columns: 5",
        "# Limei by harunnoir", "# SPDX-License-Identifier: CC-BY-SA-4.0", "#",
    ]
    for entry in doc["ordered_colors"]:
        r, g, b = rgb(entry["hex"])
        gpl.append(f"{r:3d} {g:3d} {b:3d}  {entry['name']}")
    gpl_text = "\n".join(gpl) + "\n"

    # Palette SVG.
    width, height, columns = 190, 92, 5
    rows = math.ceil(len(doc["ordered_colors"]) / columns)
    svg = [
        '<!-- Limei by harunnoir -->',
        '<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * columns}" height="{height * rows}" viewBox="0 0 {width * columns} {height * rows}">',
        f'<rect width="100%" height="100%" fill="{bg}"/>',
        '<style>text{font-family:monospace}.name{font-size:15px;font-weight:700}.hex{font-size:13px}</style>',
    ]
    dark_names = {"Deep", "Inactive", "Base", "Alternate", "Raised", "Selection", "Active", "Subtle"}
    for i, entry in enumerate(doc["ordered_colors"]):
        x, y = (i % columns) * width, (i // columns) * height
        text = bright_fg if entry["name"] in dark_names else bg
        svg.extend([
            f'<rect x="{x+8}" y="{y+8}" width="{width-16}" height="{height-16}" rx="8" fill="{entry["hex"]}" stroke="{border}"/>',
            f'<text class="name" x="{x+20}" y="{y+37}" fill="{text}">{entry["name"]}</text>',
            f'<text class="hex" x="{x+20}" y="{y+60}" fill="{text}">{entry["hex"]}</text>',
        ])
    svg.append('</svg>')
    svg_text = "\n".join(svg) + "\n"

    # Terminal ports.
    alacritty = header("#") + f"""\n[colors.primary]\nbackground = "{bg}"\nforeground = "{fg}"\ndim_foreground = "{dim}"\nbright_foreground = "{bright_fg}"\n\n[colors.cursor]\ntext = "{bg}"\ncursor = "{taupe}"\n\n[colors.vi_mode_cursor]\ntext = "{bg}"\ncursor = "{navigation}"\n\n[colors.selection]\ntext = "{bright_fg}"\nbackground = "{selection}"\n\n[colors.search.matches]\nforeground = "{bg}"\nbackground = "{wheat}"\n\n[colors.search.focused_match]\nforeground = "{bg}"\nbackground = "{taupe}"\n\n[colors.hints.start]\nforeground = "{bg}"\nbackground = "{amber}"\n\n[colors.hints.end]\nforeground = "{bg}"\nbackground = "{slate}"\n\n[colors.footer_bar]\nforeground = "{fg}"\nbackground = "{surface}"\n\n[colors.normal]\n""" + "\n".join(f'{k} = "{v}"' for k, v in normal.items()) + """\n\n[colors.bright]\n""" + "\n".join(f'{k} = "{v}"' for k, v in brights.items()) + f"""\n\n[colors]\ndraw_bold_text_with_bright_colors = false\ntransparent_background_colors = false\n"""

    foot = header("#") + f"""\n[colors]\nforeground={fg[1:]}\nbackground={bg[1:]}\nselection-foreground={bright_fg[1:]}\nselection-background={selection[1:]}\ncursor={bg[1:]} {taupe[1:]}\nurls={slate[1:]}\n\n""" + "\n".join(f'regular{i}={v[1:]}' for i, v in enumerate(normal.values())) + "\n\n" + "\n".join(f'bright{i}={v[1:]}' for i, v in enumerate(brights.values())) + f"""\n\n[csd]\ncolor={bg[1:]}\nborder-color={border[1:]}\nbutton-color={fg[1:]}\nbutton-minimize-color={wheat[1:]}\nbutton-maximize-color={green[1:]}\nbutton-close-color={red[1:]}\n"""

    ghostty = header("#") + f"""\nbackground = {bg}\nforeground = {fg}\ncursor-color = {taupe}\ncursor-text = {bg}\nselection-background = {selection}\nselection-foreground = {bright_fg}\n\n""" + "\n".join(f'palette = {i}={v}' for i, v in enumerate(list(normal.values()) + list(brights.values()))) + "\n"

    kitty = header("#") + f"""\nforeground              {fg}\nbackground              {bg}\nselection_foreground    {bright_fg}\nselection_background    {selection}\ncursor                  {taupe}\ncursor_text_color       {bg}\nurl_color               {slate}\nactive_border_color     {taupe}\ninactive_border_color   {border}\nbell_border_color       {red}\nactive_tab_foreground   {bright_fg}\nactive_tab_background   {active}\ninactive_tab_foreground {dim}\ninactive_tab_background {surface}\ntab_bar_background      {bg}\n\n""" + "\n".join(f'color{i:<2} {v}' for i, v in enumerate(list(normal.values()) + list(brights.values()))) + "\n"

    wezterm = header("--") + f"""\nreturn {{\n  foreground = "{fg}",\n  background = "{bg}",\n  cursor_bg = "{taupe}",\n  cursor_fg = "{bg}",\n  cursor_border = "{taupe}",\n  selection_fg = "{bright_fg}",\n  selection_bg = "{selection}",\n  scrollbar_thumb = "{border}",\n  split = "{slate}",\n  ansi = {{\n""" + "\n".join(f'    "{v}",' for v in normal.values()) + """\n  },\n  brights = {\n""" + "\n".join(f'    "{v}",' for v in brights.values()) + f"""\n  }},\n  tab_bar = {{\n    background = "{bg}",\n    active_tab = {{ bg_color = "{active}", fg_color = "{bright_fg}", intensity = "Bold" }},\n    inactive_tab = {{ bg_color = "{surface}", fg_color = "{dim}" }},\n    inactive_tab_hover = {{ bg_color = "{selection}", fg_color = "{fg}" }},\n    new_tab = {{ bg_color = "{bg}", fg_color = "{muted}" }},\n    new_tab_hover = {{ bg_color = "{selection}", fg_color = "{navigation}" }},\n  }},\n}}\n"""

    xresources = header("!") + f"""\n*.foreground: {fg}\n*.background: {bg}\n*.cursorColor: {taupe}\n\n""" + "\n".join(f'*.color{i}: {v}' for i, v in enumerate(list(normal.values()) + list(brights.values()))) + "\n"

    konsole = header("#") + f"""\n[Background]\nColor={rgb_text(bg)}\n\n[BackgroundFaint]\nColor={rgb_text(deep)}\n\n[BackgroundIntense]\nColor={rgb_text(surface)}\n\n""" + "\n".join(
        f'[Color{i}]\nColor={rgb_text(list(normal.values())[i])}\n[Color{i}Intense]\nColor={rgb_text(list(brights.values())[i])}' for i in range(8)
    ) + f"""\n\n[Foreground]\nColor={rgb_text(fg)}\n\n[ForegroundFaint]\nColor={rgb_text(dim)}\n\n[ForegroundIntense]\nColor={rgb_text(bright_fg)}\n\n[General]\nAnchor=0.5,0.5\nBlur=false\nColorRandomization=false\nDescription=Limei by harunnoir\nFillStyle=Tile\nOpacity=1\nWallpaper=\n"""

    windows = {
        "name": "Limei", "background": bg, "foreground": fg,
        "cursorColor": taupe, "selectionBackground": selection,
        "black": normal["black"], "red": normal["red"], "green": normal["green"],
        "yellow": normal["yellow"], "blue": normal["blue"], "purple": normal["magenta"],
        "cyan": normal["cyan"], "white": normal["white"],
        "brightBlack": brights["black"], "brightRed": brights["red"],
        "brightGreen": brights["green"], "brightYellow": brights["yellow"],
        "brightBlue": brights["blue"], "brightPurple": brights["magenta"],
        "brightCyan": brights["cyan"], "brightWhite": brights["white"],
    }

    bash = header("#") + "\n".join(
        f"export LIMEI_{entry['id'].replace('.', '_').upper()}='{entry['hex']}'" for entry in doc["ordered_colors"]
    ) + "\n"

    starship = header("#") + "\n[palettes.limei]\n" + "\n".join(
        f'{entry["id"].replace(".", "_")} = "{entry["hex"]}"' for entry in doc["ordered_colors"]
    ) + "\n"

    zellij = header("//") + f"""\nthemes {{\n  limei {{\n    fg "{fg}"\n    bg "{bg}"\n    black "{normal['black']}"\n    red "{normal['red']}"\n    green "{normal['green']}"\n    yellow "{normal['yellow']}"\n    blue "{normal['blue']}"\n    magenta "{normal['magenta']}"\n    cyan "{normal['cyan']}"\n    white "{normal['white']}"\n    orange "{clay}"\n  }}\n}}\n"""

    return {
        "palette/limei.json": jt(compatibility),
        "palette/limei.yml": yaml_text,
        "palette/mappings/ansi16.json": jt(ansi_doc),
        "palette/mappings/ansi16.toml": "\n".join(ansi_toml),
        "palette/derived/ansi-bright.json": jt(ansi_bright_doc),
        "palette/mappings/ui-roles.json": jt(ui_roles),
        "palette/mappings/terminal-special.json": jt({"meta": {**generated_meta, "kind": "terminal-special-colors", "license": "CC-BY-SA-4.0"}, "colors": special}),
        "palette/mappings/xterm256.json": jt(xterm_doc),
        "palette/derived/overlays.json": jt(alpha_doc),
        "templates/css/limei.css": css,
        "templates/scss/_limei.scss": scss,
        "templates/lua/limei.lua": lua,
        "templates/python/limei.py": py,
        "templates/gimp/Limei.gpl": gpl_text,
        "assets/palette.svg": svg_text,
        "ports/terminals/alacritty/limei.toml": alacritty,
        "ports/terminals/foot/limei.ini": foot,
        "ports/terminals/ghostty/limei": ghostty,
        "ports/terminals/kitty/limei.conf": kitty,
        "ports/terminals/wezterm/limei.lua": wezterm,
        "ports/terminals/xresources/Limei.Xresources": xresources,
        "ports/terminals/konsole/Limei.colorscheme": konsole,
        "ports/terminals/windows-terminal/limei.json": jt(windows),
        "ports/shell/bash/limei.sh": bash,
        "ports/shell/starship/limei.toml": starship,
        "ports/shell/zellij/limei.kdl": zellij,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when generated files differ")
    args = parser.parse_args()
    outputs = build_outputs()
    mismatches = []
    for relative, expected in outputs.items():
        path = ROOT / relative
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != expected:
            mismatches.append(relative)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")
    if args.check and mismatches:
        print("Generated files are out of date:")
        for relative in mismatches:
            print(f"  {relative}")
        return 1
    if args.check:
        print(f"OK: {len(outputs)} generated files are current.")
    else:
        print(f"Generated {len(outputs)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
