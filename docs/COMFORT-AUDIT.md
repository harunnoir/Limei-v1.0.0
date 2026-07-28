# Limei v1.0.1 comfort audit

This pass reviewed every included port, not only terminal palettes.

## Changes by area

### Window managers

Niri and Hyprland now use taupe for focus, red for urgency, slate for insert
information, and clay for locked-group state.

### Bars and notifications

Waybar no longer colors every monitoring module continuously. Normal CPU,
memory, battery, and temperature states are quiet; semantic colors appear
for charging, connectivity, warnings, and critical states.

Mako uses taupe for normal attention, slate for low urgency, green for
progress, and red for high urgency. SwayNC uses clay for do-not-disturb mode
and green for progress.

### Launchers

Rofi and Wofi use neutral selected rows. Taupe marks input focus,
navigation marks the selected icon, and red remains urgent-only.

### GTK and Qt

Persistent surfaces and selected tabs are neutral. Taupe marks keyboard
focus, sage marks primary controls, green marks progress, slate/lavender
mark links, and amber/red mark warnings and destructive states.

### Editors and developer tools

Helix uses taupe for the primary cursor and sage for secondary cursors.
Syntax colors retain distinct semantic roles without making punctuation or
comments visually loud.

Lazygit and fzf now use taupe for focus, navigation for pointers, green for
selected markers or additions, amber for searching, slate for information,
and red for errors.

### Readers

Sioyek and Zathura keep the document background and text neutral. Wheat,
taupe, amber, slate, lavender, and navigation are reserved for highlights,
search, links, synchronization, and completion groups.

### System monitors

btop keeps its graphs semantic: green-to-amber-to-red for load and
temperature, slate for networking, lavender for memory, clay for CPU, and
taupe for focus.

### Browsers

Chromium/Helium remains mostly neutral. Taupe is limited to functional
toolbar icons and slate to links.

### Terminals

Normal ANSI slots use canonical colors. Bright hue slots use six approved,
muted derived colors so bright blue remains related to blue, bright magenta
remains related to magenta, and no bright slot collides with another.
Terminal tabs and splits use neutral surfaces or small role-based accents.

## What automation cannot certify

The repository now checks semantic roles and common high-impact choices, but
final approval still requires real use in GTK applications, Qt applications,
launchers, notifications, readers, editors, and terminals.
