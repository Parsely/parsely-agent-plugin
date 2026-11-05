---
name: parsely-weekly-pulse
description: Build a weekly Parse.ly pulse for a newsroom or content team — last week's top stories, where their readers came from, standout authors and sections, and how the week compared with the one before. Use when the user asks for a weekly recap, top stories of the week, a newsroom pulse, or a Monday summary.
---

# Weekly pulse

A short recap a content team can read in two minutes on Monday. Follow the `parsely-reports` skill for windows,
sources and guardrails.

**Dates:** ask for the start and end dates before any query (see `parsely-reports`). Suggest the last full week (7 days ending yesterday, or Monday to Sunday if the user says "last week"), against the week before.

## Data to pull

1. `list_site` → `api_key`.
2. Week totals and daily shape: `query_traffic_trend`, `interval=1d`, with `compare_start`/`compare_end`.
3. Top 10 posts by `views`, and top 10 by `engaged_minutes`: `query_top_content`.
4. Top sections and top authors: `query_top_aspect` with `aspect=sections`, then `aspect=authors`, with
   `compare_start`/`compare_end`.
5. Top referrers for the week: `query_referrers`.
6. For the top three posts only: `query_post_detail` to see where their readers came from.

## What to write

1. **The week in one line** — views and visitors, change against the week before.
2. **Top stories** — the top 5 with views, engaged minutes and their main traffic source. Note any post published
   before this week that is still in the top 10.
3. **Stayed longest** — posts in the engaged-minutes top 10 that aren't in the views top 10.
4. **Sections and authors** — the biggest risers and fallers against last week, with both numbers.
5. **Traffic sources** — any referrer that moved a lot (a social spike, an aggregator pick-up).
6. **Best day** — the peak day, and the post that accounts for most of it if there is one.

## Output

Chat by default, as short bullets. When the user wants to share it or keep it weekly, build a Parse.ly report
artifact (`parsely-report-artifacts`). To update last week's page, edit the saved artifact rather than making a new
one, so the link stays the same.
