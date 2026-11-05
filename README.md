# Parse.ly plugin

Parse.ly content analytics inside your AI assistant. The plugin connects the Parse.ly MCP server
(`https://dash.parsely.com/mcp`) and adds skills that teach the assistant how to build Parse.ly reports you can
trust: every number traced to a Parse.ly query, windows that compare fairly, and pages you can share with your team
as Parse.ly report links.

You sign in with your Parse.ly account the first time the assistant uses a Parse.ly tool. You see only the sites
your account can see.

## Why this repo exists

Like any other MCP server, the Parse.ly MCP server offers a set of deterministic tools built specifically for agents.
While these tools include descriptions, they don't include much information about the work we do at Parse.ly:
specifically, how we use these numbers to build a deep understanding of site performance.

These skills bridge the gap between "capable agent" and "expert data analyst". They load automatically through the
Claude and OpenAI directories, among others.

## How this differs from Agentic Analytics

[Agentic Analytics](https://github.com/Automattic/agentic-analytics) is a separate Parse.ly plugin for coding agents.
It answers questions that need raw, visitor-level data, such as how readers move between loyalty tiers. This repo
serves every Parse.ly customer using only the MCP server.

| | This plugin | Agentic Analytics |
|---|---|---|
| **Who can use it** | Any Parse.ly customer | Customers with a Parse.ly Data Pipeline subscription |
| **Where the data comes from** | Parse.ly MCP tools, under the user's own account | Raw event data downloaded from the customer's Data Pipeline bucket |
| **Setup** | Sign in with Parse.ly | About 30 minutes in a terminal, with AWS credentials |
| **What runs on the user's computer** | Nothing: the skills are markdown | Scripts and a local copy of the data |
| **Where it runs** | Claude, ChatGPT, Codex and other MCP clients | Coding agents such as Claude Code, Codex and Cursor |
| **How it ships** | Claude and OpenAI directories and other registries | Installed from its own repo |

The two projects share no code. A report belongs here only if it can run on the MCP tools alone. Reports that need
Data Pipeline data, such as the staircase and journey reports, stay in Agentic Analytics.

## What you can ask for

| Skill | Ask for |
|---|---|
| `parsely-insight-brief` | A four-week health check: what moved, where it comes from, and what to do about it |
| `parsely-weekly-pulse` | Last week's top stories, sources, sections and authors |
| `parsely-period-comparison` | Week over week, month over month, year over year |
| `parsely-traffic-change` | Which sources, sections and posts account for a rise or drop |
| `parsely-marketing-questions` | Under-promoted content, Google dependency, AI referrals |
| `parsely-campaign-performance` | UTM campaigns, newsletters, paid traffic |
| `parsely-editorial-scorecard` | Authors, sections and tags ranked by reach and engagement |
| `parsely-headline-tests` | Headline A/B test results and what wins |
| `parsely-dashboard-snapshot` | Everything on one page |

Three skills run under all of them:

- `parsely-reports`: ask for the dates first, Parse.ly data only, cite every number, guardrails.
- `parsely-report-artifacts`: build a page and save it as a Parse.ly report artifact, a shareable link.
- `parsely-artifact-sharing`: who can open a report artifact, expiry, share links, deleting, and what to do
  without access.

Report artifacts are dated snapshots of Parse.ly data, found under Reports → Artifacts in the Parse.ly dashboard.
They are not live dashboards and not scheduled reports.

## Install

- **Claude**: from the Claude directory, or in Claude Code with
  `/plugin install parsely --marketplace Parsely/parsely-agent-plugin`.
- **ChatGPT and Codex**: from the OpenAI plugin directory.
- **Any other MCP client**: add `https://dash.parsely.com/mcp` as a remote MCP server. You get the tools without
  the skills.

## How this repo works

The MCP server, its tools and their descriptions live in the Parse.ly dashboard code, not here. This repo holds
only what each platform needs on top of the server URL.

Claude is the default format: the repo root is a working Claude plugin, and Claude reads it directly from GitHub.
Every other platform gets an export built from the same `skills/` folder. Today that means a ZIP for OpenAI.

```
.claude-plugin/plugin.json      Claude plugin manifest (the repo root is the Claude plugin)
.claude-plugin/marketplace.json lets Claude Code install straight from this repo
.mcp.json                       the Parse.ly MCP server for Claude
.codex-plugin/plugin.json       OpenAI (ChatGPT, Codex) manifest; `name` is the id OpenAI gave the existing app
skills/<name>/SKILL.md          the skills, shared by every platform
docs/publishing.md              how to release to Claude, OpenAI and the MCP registry
docs/openai-review.md           test cases for OpenAI's review step
assets/                         icons
server.json                     entry for the official MCP registry
tools.json                      the MCP tool names and parameters the skills may use
scripts/                        maintainer scripts; nothing here runs for plugin users
```

### Maintainer commands

```bash
python3 scripts/sync_tools.py ../dash origin/main   # refresh tools.json from the dash tool snapshots
python3 scripts/check_skills.py                     # frontmatter, tool and parameter names, denylist
python3 scripts/bump_version.py 0.2.0               # one version across every manifest
bash scripts/build_openai.sh                        # dist/parsely-openai-<version>.zip for OpenAI's portal
claude plugin validate .                            # Claude's own manifest check
```

### Releasing

See [docs/publishing.md](docs/publishing.md).

## Privacy

The plugin sends nothing anywhere by itself. The assistant talks to the Parse.ly MCP server under your Parse.ly
account; see the [Parse.ly privacy policy](https://www.parse.ly/privacy-policy).

## License

MIT
