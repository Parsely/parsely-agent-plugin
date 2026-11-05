---
name: parsely-insight-brief
description: Build a Parse.ly insight brief — a four-week health check with the few findings worth acting on, what moved and where it shows up, and where to see each one in Parse.ly. Use when the user asks "how are we doing", for a health check, a monthly brief, a state-of-the-site summary, talking points for a meeting, or "what should I pay attention to".
---

# Insight brief

A four-week health check that names the few things worth attention, shows where each change comes from, and tells the reader
where to look in Parse.ly. Follow the `parsely-reports` skill for windows, sources and guardrails.

**Dates:** ask for the start and end dates before any query (see `parsely-reports`). Suggest the last 28 full days ending yesterday, against the 28 days before.

## Data to pull

1. `list_site` → `api_key`.
2. Headline numbers for both windows: `query_traffic_trend` with `interval=1d` and `compare_start`/`compare_end`
   (views, visitors, engaged minutes). Use `get_site_overview` only for its standard periods.
3. What moved traffic: `query_referrers` for both windows (domains and categories) with `compare_start`/`compare_end`.
4. Where it landed: `query_top_aspect` with `aspect=sections`, both windows.
5. Top posts: `query_top_content` by `views` and again by `engaged_minutes`.
6. AI assistants: `query_top_content` with `referrers_category=ai`, and the `ai` row from step 3.

## What to write

1. **Headline** — one sentence: up, down or flat, by how much, on which metric, for which dates.
2. **What moved it** — the two or three referrer categories or domains that account for most of the change, with both
   windows' numbers.
3. **Under-promoted content** — posts in the top 20 by engaged minutes that sit outside the top 50 by views:
   readers who find them stay, but few find them. Next step: promote or link them.
4. **Platform dependency** — the share of views from the largest single referrer domain and the largest category.
   Flag any one source above about a third of views as a risk.
5. **AI referrals** — views from AI assistants this window and last, and the posts or sections they land on.
6. **Check before quoting** — any number that jumped several times over, or moved against the others.
7. **Talking points** — three short lines the reader can say in a meeting, each with its number and dates.

Each finding ends with "Where to see it in Parse.ly: …" (for example "Referrers, filter AI").

## Output

A short chat answer by default. When the user wants a page or to share it, build it as a Parse.ly report artifact
(`parsely-report-artifacts`): findings first, a daily trend line for both windows, then the tables.
