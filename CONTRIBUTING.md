# Contributing

Contributions are welcome when they preserve Limei's visual direction.

Before submitting a port:

- use `palette/canonical/limei-25.json` as the source of truth;
- never modify or regenerate the canonical 25 colors;
- use the official ANSI mapping for terminal ports;
- avoid arbitrary RGB colors;
- keep accent usage balanced and role-based;
- validate the configuration with the target application when possible;
- preserve attribution to harunnoir;
- include the appropriate SPDX identifier and installation notes.

Run the complete local validation suite:

```bash
./scripts/validate.sh
```

Suggested commit messages:

```text
feat(foot): add Limei terminal port
fix(ansi): keep black visible on the base background
docs(color): explain canonical and derived layers
```
