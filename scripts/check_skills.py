"""Check every skill before release.

- Frontmatter has `name` (matching its folder) and a `description` of at most 1024 characters.
- Every backticked snake_case word is a Parse.ly tool, a tool parameter, an enum value, or listed in
  scripts/known_terms.txt. This catches skills that name a tool or parameter the MCP no longer has.
- No file contains a term from scripts/denylist.txt (internal hosts, customer names).

Usage: python3 scripts/check_skills.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAKE = re.compile(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SCANNED_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}


def read_list(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip() and not line.startswith("#")]


def frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def known_words() -> set[str]:
    tools = json.loads((ROOT / "tools.json").read_text())["tools"]
    words = set(tools)
    for spec in tools.values():
        words.update(spec["params"])
        words.update(spec["enums"])
    words.update(read_list(ROOT / "scripts" / "known_terms.txt"))
    return words


def check_skill(path: Path, words: set[str]) -> list[str]:
    text = path.read_text()
    errors = []
    fields = frontmatter(text)
    if fields.get("name") != path.parent.name:
        errors.append(f"{path}: frontmatter name must be {path.parent.name!r}")
    if not fields.get("description"):
        errors.append(f"{path}: frontmatter description is missing")
    elif len(fields["description"]) > 1024:
        errors.append(f"{path}: description is longer than 1024 characters")
    for word in sorted(set(SNAKE.findall(text)) - words):
        errors.append(f"{path}: `{word}` is not a Parse.ly tool, parameter or known term")
    return errors


def check_denylist() -> list[str]:
    terms = read_list(ROOT / "scripts" / "denylist.txt")
    local_terms = ROOT / "scripts" / "denylist.local.txt"
    if local_terms.exists():
        terms += read_list(local_terms)
    patterns = [re.compile(term, re.IGNORECASE) for term in terms]
    errors = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or "dist" in path.parts or path.suffix not in SCANNED_SUFFIXES:
            continue
        if path.name in {"denylist.txt", "denylist.local.txt", "tools.json"}:
            continue
        text = path.read_text()
        for pattern in patterns:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: contains denylisted term {pattern.pattern!r}")
    return errors


def main() -> None:
    words = known_words()
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    errors = [error for skill in skills for error in check_skill(skill, words)] + check_denylist()
    for error in errors:
        print(error)
    print(f"{len(skills)} skills checked, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
