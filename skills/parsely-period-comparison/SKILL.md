---
name: parsely-period-comparison
description: Compare two periods of Parse.ly data — week over week, month over month, year over year, or any two date ranges — for the whole site or one section, author, tag or campaign. Use when the user asks "vs last month", "year over year", "compared to", "how does this period compare", or for a period-over-period report.
---

# Period comparison

The same numbers for two periods side by side, and where the difference comes from. Follow the `parsely-reports`
skill for windows, sources and guardrails.

## Pick the two periods

Ask for both periods' start and end dates before any query (see `parsely-reports`). Offer these as choices:

- Week over week: 7 full days ending yesterday against the 7 before.
- Month over month: the last full calendar month against the one before, or 28 days against 28 when the user means
  "recently". Calendar months differ in length and weekday mix; say so when you compare them.
- Year over year: the same dates one year earlier, shifted to match weekdays when the period is under a month.
- If the user named a section, author, tag or campaign, use the same filter for both periods.

## Data to pull

1. `list_site` → `api_key`.
2. Totals and shape: `query_traffic_trend` for the current period with `compare_start`/`compare_end` for the
   other one. Pick `interval` by length: `1d` up to two months, `1w` up to a year, `1M` beyond.
3. Where the change came from:
   - `query_referrers` with `compare_start`/`compare_end` (categories and domains).
   - `query_top_aspect` with `compare_start`/`compare_end`, for sections and then authors.
4. `query_top_content` for each period: posts that entered or left the top 20.

## What to write

1. **Headline** — views, visitors and engaged minutes for both periods, with absolute and % change.
2. **Biggest contributors** — the referrer categories and sections that account for most of the change, ranked by
   absolute change, not %. A tiny section doubling matters less than a big one losing 10%.
3. **New and gone** — posts that entered or left the top 20.
4. **Caveats** — different period lengths, a holiday in one period, a data gap, a changed filter.

## Output

A comparison table with both periods and the change, then the findings. Draw both trend lines on one chart when
you build a page (`parsely-report-artifacts`).
