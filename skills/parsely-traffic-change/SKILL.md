---
name: parsely-traffic-change
description: Break down a rise or drop in Parse.ly traffic — find the day it changed, which sources, sections and posts account for it, and whether it looks like a tracking or data issue. Use when the user asks "why did traffic drop", "what caused the spike", "why are we down this week", or to investigate a sudden change.
---

# Traffic change breakdown

Parse.ly shows what changed, not why it changed. This skill finds which sources, sections and posts account for a
change, so the user can work out the cause. Follow the `parsely-reports` skill for windows, sources and guardrails.

**Dates:** ask which dates the change happened in, and which period to compare it with, before any query (see
`parsely-reports`). Suggest the last 7 full days against the 7 before.

## Steps

1. **Size it.** `query_traffic_trend`, `interval=1d`, for the period the user means plus the same length before.
   Find the day the change started and how big it is in views and %.
2. **Check for a data issue.** If views fall to near zero on one day, or every source and section drops by the
   same % at once, it may be a tracking or data problem rather than a real change. Say that, and suggest checking
   the tracker on the site or contacting Parse.ly support.
3. **Which source?** `query_referrers` for the change window with `compare_start`/`compare_end`. Rank categories
   and domains by absolute change.
4. **Which section?** `query_top_aspect` with `aspect=sections`, filtered to the moving source with
   `referrers_category` or `referrer_domain`, against the period before.
5. **Which posts?** `query_top_content` with the same filter, for both windows. Look for a few posts that account
   for most of the change, such as a post whose traffic ended or a referrer that stopped sending readers.
6. **One post?** `query_post_detail` to see when its traffic rose or fell and from where.

Stop as soon as one step accounts for most of the change, and say how much: "Facebook referrals account for 70%
of the drop; the rest is spread across sources."

## What to write

1. **What changed** — size, start date, metric.
2. **Where it shows up** — the sources, sections or posts that account for it, with numbers from both windows.
3. **Data issue or not** — the evidence either way.
4. **Questions to check** — what the user could look into for the cause, framed as questions ("Did the Facebook
   posting schedule change that week?"). Never state a cause as fact: Parse.ly has no data on causes.
5. **Not accounted for** — the part of the change you could not place.
