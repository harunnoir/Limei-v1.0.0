#!/usr/bin/env python3
"""Verify ANSI16 mapping consistency across terminal ports."""

from pathlib import Path
import json
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
ansi = json.loads((ROOT / "palette/mappings/ansi16.json").read_text())
expected = list(ansi["normal"].values()) + list(ansi["bright"].values())
errors = []

# Alacritty.
data = tomllib.loads((ROOT / "ports/terminals/alacritty/limei.toml").read_text())
actual = list(data["colors"]["normal"].values()) + list(data["colors"]["bright"].values())
if actual != expected:
    errors.append("Alacritty ANSI mapping differs")

# Foot.
text = (ROOT / "ports/terminals/foot/limei.ini").read_text()
actual = []
for prefix in ("regular", "bright"):
    for index in range(8):
        match = re.search(rf"^{prefix}{index}=([0-9a-fA-F]{{6}})$", text, re.M)
        actual.append("#" + match.group(1).lower() if match else "missing")
if actual != expected:
    errors.append("Foot ANSI mapping differs")

# Ghostty.
text = (ROOT / "ports/terminals/ghostty/limei").read_text()
actual = []
for index in range(16):
    match = re.search(rf"^palette\s*=\s*{index}=(#[0-9a-fA-F]{{6}})$", text, re.M)
    actual.append(match.group(1).lower() if match else "missing")
if actual != expected:
    errors.append("Ghostty ANSI mapping differs")

# Kitty.
text = (ROOT / "ports/terminals/kitty/limei.conf").read_text()
actual = []
for index in range(16):
    match = re.search(rf"^color{index}\s+(#[0-9a-fA-F]{{6}})$", text, re.M)
    actual.append(match.group(1).lower() if match else "missing")
if actual != expected:
    errors.append("Kitty ANSI mapping differs")

# WezTerm: first 16 hexes after ansi/brights declarations.
text = (ROOT / "ports/terminals/wezterm/limei.lua").read_text()
ansi_block = re.search(r"ansi\s*=\s*\{(.*?)\}", text, re.S)
bright_block = re.search(r"brights\s*=\s*\{(.*?)\}", text, re.S)
actual = re.findall(r"#[0-9a-fA-F]{6}", ansi_block.group(1)) + re.findall(r"#[0-9a-fA-F]{6}", bright_block.group(1))
actual = [value.lower() for value in actual]
if actual != expected:
    errors.append("WezTerm ANSI mapping differs")

# Windows Terminal.
data = json.loads((ROOT / "ports/terminals/windows-terminal/limei.json").read_text())
keys = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white", "brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite"]
actual = [data[key].lower() for key in keys]
if actual != expected:
    errors.append("Windows Terminal ANSI mapping differs")

# Xresources.
text = (ROOT / "ports/terminals/xresources/Limei.Xresources").read_text()
actual = []
for index in range(16):
    match = re.search(rf"^\*\.color{index}:\s*(#[0-9a-fA-F]{{6}})$", text, re.M)
    actual.append(match.group(1).lower() if match else "missing")
if actual != expected:
    errors.append("Xresources ANSI mapping differs")

# Konsole decimal RGB.
text = (ROOT / "ports/terminals/konsole/Limei.colorscheme").read_text()
actual = []
for index in range(8):
    for suffix in ("", "Intense"):
        block = re.search(rf"\[Color{index}{suffix}\]\s*\nColor=(\d+),(\d+),(\d+)", text)
        if not block:
            actual.append("missing")
        else:
            actual.append("#" + "".join(f"{int(block.group(i)):02x}" for i in range(1, 4)))
# Konsole is ordered normal0,bright0,normal1,bright1; reorder.
normal = actual[0::2]
bright = actual[1::2]
if normal + bright != expected:
    errors.append("Konsole ANSI mapping differs")

if expected[0] == "#101010":
    errors.append("ANSI black must not equal the terminal background")

if errors:
    print("ANSI validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("OK: all terminal ports use the official Limei ANSI16 mapping.")
