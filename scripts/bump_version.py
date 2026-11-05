"""Set one version in every manifest, so the platforms never disagree.

Usage: python3 scripts/bump_version.py 0.2.0
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = [".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    version = sys.argv[1]
    for name in MANIFESTS:
        path = ROOT / name
        data = json.loads(path.read_text())
        data["version"] = version
        write(path, data)
    marketplace_path = ROOT / ".claude-plugin/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    for plugin in marketplace["plugins"]:
        plugin["version"] = version
    write(marketplace_path, marketplace)
    print(f"version set to {version}")


if __name__ == "__main__":
    main()
