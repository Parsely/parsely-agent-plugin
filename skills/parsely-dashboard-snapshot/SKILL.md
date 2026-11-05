---
name: parsely-dashboard-snapshot
description: Build a single-view Parse.ly dashboard page — a dated snapshot with headline tiles, the traffic trend against the period before, top posts, sources, sections and campaigns on one page. Use when the user asks for a dashboard, a one-page overview, an executive snapshot, or "everything on one page".
---

# Dashboard snapshot

One page with everything a reader checks first. It is a dated snapshot, not a live dashboard: say the dates at
the top. If the user wants it to update by itself, say live dashboards aren't available yet and suggest they
contact Parse.ly support; they can ask again later for a new version with new dates. Follow the `parsely-reports` skill for windows, sources and guardrails, and build the page with
`parsely-report-artifacts`.

**Dates:** ask for the start and end dates before any query (see `parsely-reports`). Suggest the last 28 full days ending yesterday, against the 28 days before.

## Data to pull

1. `list_site` → `api_key`.
2. `query_traffic_trend`, `interval=1d`, with `compare_start`/`compare_end`.
3. `query_top_content` by `views`, top 10.
4. `query_referrers`, categories and top 10 domains.
5. `query_top_aspect` with `aspect=sections`, top 10.
6. `query_campaigns`, top 10 by views, plus campaign views as a share of all views.

## Page layout

1. **Title, site, dates, "Data from Parse.ly, built on <date>".**
2. **Tiles** — views, visitors, engaged minutes, minutes per visitor, each with its change against the period
   before.
3. **Trend** — daily views, this period and last, aligned by day.
4. **One-line findings** — the two or three things that changed most.
5. **Tables** — top posts, sources, sections, campaigns. Each table shows its numbers, not only bars.
6. **Footer** — the source trail: which tool produced each block, and the dates.
