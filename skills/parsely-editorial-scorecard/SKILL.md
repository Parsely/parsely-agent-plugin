---
name: parsely-editorial-scorecard
description: Build a Parse.ly editorial scorecard — how authors, sections or tags performed over a period, ranked by reach and by engagement, with risers, fallers and output. Use when the user asks for an author leaderboard, a section or tag report, "which topics work", editorial performance, or a desk-by-desk review.
---

# Editorial scorecard

Rank authors, sections or tags fairly: by reach, by engagement, and by output. Follow the `parsely-reports` skill
for windows, sources and guardrails.

**Dates:** ask for the start and end dates before any query (see `parsely-reports`). Suggest the last 28 full days ending yesterday, against the 28 days before.

## Data to pull

1. `list_site` → `api_key`.
2. `query_top_aspect` with `aspect` set to `authors`, `sections` or `tags`, with `compare_start`/`compare_end`.
   Call it once per metric you rank by: `views`, `visitors`, `engaged_minutes`, `posts`.
3. For the top five rows: `query_top_content` filtered to that author, section or tag, for their best posts.
4. To match a name the user typed, use `list_author`, `list_section` or `list_tag` first. Never guess the exact
   value.

## What to write

1. **Reach** — the top 10 by views, with the change against the period before.
2. **Engagement** — the top 10 by engaged minutes per visitor, among rows with enough views to matter (say what
   floor you used).
3. **Output** — `posts` means posts that received traffic in the window, not posts published. Say so if you show
   it.
4. **Risers and fallers** — the biggest absolute changes.
5. **Best post each** — for the top five, their most-read post in the window.

Don't present this as a ranking of people's worth: different beats get different traffic. Say so if the user asks
for a single "best author".
