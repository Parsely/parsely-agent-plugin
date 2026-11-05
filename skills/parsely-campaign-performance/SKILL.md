---
name: parsely-campaign-performance
description: Report on marketing campaign performance in Parse.ly — UTM sources, mediums and campaigns ranked by views, visitors, engaged time and conversions, one campaign's timeline, and what content campaign readers went to. Use when the user asks about campaigns, UTM traffic, newsletter or paid traffic performance, or campaign ROI.
---

# Campaign performance

Campaigns in Parse.ly are UTM values. Follow the `parsely-reports` skill for windows, sources and guardrails.

**Dates:** ask for the start and end dates before any query (see `parsely-reports`). Suggest the last 28 full days ending yesterday.

## All campaigns

1. `list_site` → `api_key`.
2. `query_campaigns` without `campaign_key` for an overview of every UTM dimension, then with `campaign_key` set to
   the dimension the user cares about (`source`, `medium`, `id`…). Page through with `page` while `has_more` is
   true.
3. Rank by what the user cares about: `views`, `visitors`, `engaged_minutes`, or a conversion metric if the site
   tracks conversions. If you use conversions, name the attribution model and say `last_touch` is the default.

## One campaign

1. Find it: `search_campaign` with the name the user gave. Ask if several match.
2. Its timeline: `get_campaign` with the `utm_value` from the search result and `campaign_key` set to its UTM
   dimension. Send both: the same value can exist under more than one dimension.
3. Where its readers went: `query_top_content` filtered to that campaign (for example `campaign_source`,
   `campaign_medium`, `campaign_id`).

## What to write

1. **Top campaigns** — by the chosen metric, with views, visitors, engaged minutes per visitor and conversions
   where available.
2. **Quality, not just volume** — campaigns whose readers stay much longer or shorter than the site average.
3. **Share of traffic** — campaign views as a share of all site views for the window, with both numbers.
4. **Gaps** — UTM values that look like typos or duplicates of each other ("newsletter" vs "Newsletter"). Report
   them as found; don't merge them silently.
