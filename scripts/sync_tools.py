"""Write tools.json from the Parse.ly MCP tool snapshots in a dash checkout.

Usage: python3 scripts/sync_tools.py /path/to/dash [git-ref]
"""

import json
import subprocess
import sys
from pathlib import Path

SNAPSHOT_DIR = "tests/jess/__toolsnaps__"
OUTPUT = Path(__file__).resolve().parent.parent / "tools.json"


def git(dash: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(dash), *args], check=True, capture_output=True, text=True).stdout


def collect_names(schema: object, params: set[str], enums: set[str]) -> None:
    if isinstance(schema, dict):
        for name, sub in (schema.get("properties") or {}).items():
            params.add(name)
            collect_names(sub, params, enums)
        for value in schema.get("enum") or []:
            if isinstance(value, str):
                enums.add(value)
        for key in ("items", "anyOf", "oneOf", "allOf"):
            collect_names(schema.get(key), params, enums)
    elif isinstance(schema, list):
        for item in schema:
            collect_names(item, params, enums)


def main() -> None:
    dash = Path(sys.argv[1])
    ref = sys.argv[2] if len(sys.argv) > 2 else "origin/main"
    sha = git(dash, "rev-parse", ref).strip()
    paths = [p for p in git(dash, "ls-tree", "--name-only", f"{ref}:{SNAPSHOT_DIR}").split() if p.endswith(".mcp.json")]
    tools = {}
    for path in sorted(paths):
        snapshot = json.loads(git(dash, "show", f"{ref}:{SNAPSHOT_DIR}/{path}"))
        params: set[str] = set()
        enums: set[str] = set()
        collect_names(snapshot.get("inputSchema"), params, enums)
        params -= {"path_params", "query_params", "body"}
        tools[snapshot["name"]] = {"params": sorted(params), "enums": sorted(enums)}
    OUTPUT.write_text(json.dumps({"source": {"ref": ref, "sha": sha}, "tools": tools}, indent=2) + "\n")
    print(f"{len(tools)} tools from {ref} ({sha[:10]}) -> {OUTPUT.name}")


if __name__ == "__main__":
    main()
