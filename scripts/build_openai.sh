#!/usr/bin/env bash
# Build the ZIP uploaded to the existing Parse.ly plugin in OpenAI's portal: manifest, MCP declaration, skills and icons.
# Usage: scripts/build_openai.sh
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"

python3 - "$root" <<'EOF'
import json
import sys
import zipfile
from pathlib import Path

root = Path(sys.argv[1])
version = json.loads((root / ".codex-plugin/plugin.json").read_text())["version"]
files = [root / "README.md", root / "LICENSE"]
files += sorted(p for folder in (".codex-plugin", "skills", "assets") for p in (root / folder).rglob("*") if p.is_file())

out = root / "dist" / f"parsely-openai-{version}.zip"
out.parent.mkdir(exist_ok=True)
servers = json.loads((root / ".mcp.json").read_text())["mcpServers"]
# OpenAI's `.mcp.json` format has no `type`, which Claude's copy in this repo needs.
openai_mcp = {"mcpServers": {name: {"url": server["url"]} for name, server in servers.items()}}
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(root).as_posix())
    archive.writestr(".mcp.json", json.dumps(openai_mcp, indent=2) + "\n")
print(out)
EOF
