# Working on this repo

This repo is public. It packages the Parse.ly MCP server (`https://dash.parsely.com/mcp`) with skills for Claude
and OpenAI. Read `README.md` first.

## Rules

- **Skills are markdown only.** Nothing in `skills/` runs code on the user's machine: no scripts, no `bin/`, no
  local files. Everything a skill needs comes from Parse.ly MCP tools.
- **Claude is the default format.** The repo root stays a working Claude plugin with no build step. Other platforms
  get exports built from it, such as `scripts/build_openai.sh`. See `docs/publishing.md`.
- **Skills are shared.** One `skills/` folder serves every platform. Write for "the assistant", never for Claude or
  ChatGPT by name. Platform-only details go in that platform's manifest.
- **Skills don't redefine Parse.ly.** Metric meanings, routing and tool details come from the MCP server's
  instructions and tool descriptions, which live in the dash repo. A skill adds the workflow on top: which tools in
  what order, what to write, how to check it. If a fact is wrong, fix it in dash.
- **Name real tools and parameters only.** `scripts/check_skills.py` fails on any backticked snake_case word that
  isn't in `tools.json` or `scripts/known_terms.txt`. Refresh `tools.json` with `scripts/sync_tools.py` when dash
  changes its tools.
- **Nothing internal.** No customer names or sites, internal hosts, internal links, staff names or real numbers.
  Use `example.com`. `scripts/denylist.txt` is the CI check. Customer names and internal hosts go in
  `scripts/denylist.local.txt`, which git ignores, because listing them in a public file would publish them. CI
  can't see that file, so run `scripts/check_skills.py` locally before you push.
- **Reports here run on the MCP tools alone.** A report that needs the Parse.ly Data Pipeline or local data belongs
  in [Agentic Analytics](https://github.com/Automattic/agentic-analytics). See `README.md`.
- **One version.** Change versions with `scripts/bump_version.py`, never by hand.
- **Every report skill points at `parsely-reports`** and builds pages with `parsely-report-artifacts`.
- English only, plain words, short sentences.
