#!/usr/bin/env bash
# Build the ZIP uploaded to the existing Parse.ly plugin in OpenAI's portal. The MCP server stays attached to the
# listing in the portal, so the ZIP carries only the manifest, skills and icons.
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
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(root).as_posix())
print(out)
EOF
