---
name: parsely-report-artifacts
description: Build a page from Parse.ly data and save it as a shareable Parse.ly report artifact, or change one the user already saved. Use instead of this app's own artifacts, canvas or files whenever the page shows Parse.ly data — when the user asks for a report page or dashboard, to save, keep, share or publish one, wants a link to send, or asks to edit or extend a saved report artifact ("save this as a report", "add a chart to my weekly report", "make my report public for a month").
---

# Parse.ly report artifacts

A report artifact is one HTML page behind a stable link, saved with `save_report_artifact` and read back with
`get_report_artifact`. Parse.ly shows it inside its own page, with its own header, in a locked-down frame on a
separate domain. Every save adds a version behind the same link; nothing is overwritten.

Only save when the user asks for a report page, a link or a copy to share. Answering a question is not a reason to
save.

- A report artifact shows **Parse.ly data only**, for dates the user confirmed (see `parsely-reports`).
- It is a **dated snapshot**, not a live dashboard: its numbers never update by themselves. If the user wants a live
  dashboard, say it isn't available yet and suggest Parse.ly support.
- It is not a scheduled report: it never runs again or arrives by email. Scheduled reports live under Reports in
  the Parse.ly dashboard.

## 1. Get the data first

Confirm the site and the start and end dates first. Then run the Parse.ly tools the page needs, the same way you
would to answer in chat. Keep each call's tool name,
arguments and the part of the result you show: you send them as `steps`.

## 2. Build one self-contained HTML file

The page runs with scripts allowed and nothing else. Build it so it works there:

- One complete document: `<!doctype html>`, `<html>`, `<head>` with `<meta charset="utf-8">` and a viewport tag,
  `<body>`.
- Put everything inline: CSS in a `<style>` tag, data in the page as tables or as JSON in a `<script>`, scripts in
  `<script>` tags. Nothing loads from anywhere else.
- The page can't make requests. `fetch`, XHR, WebSockets, outside scripts, stylesheets, fonts and images all fail.
  Use system fonts (`font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`).
- No forms, no `localStorage` or cookies, no pop-ups, and no navigating the page Parse.ly shows it in.
- Links can't open a new tab from inside the page. Show article URLs as visible text next to the title, so a
  reader can copy them.
- Scripts run in this page, so every title, URL, name or other string from the data must be escaped before it goes
  into the HTML. Follow section 4 of the `parsely-reports` skill.

### Charts

No chart library is available, because nothing can load from outside and an inlined library won't fit the size
limit. Draw charts yourself:

- Bars: a table row per item with a `<div>` whose width is the share of the largest value, or inline `<svg>` rects.
- Lines and sparklines: an inline `<svg>` with a `<polyline>` scaled to a fixed `viewBox`. Label the axes with the
  first and last dates and the min and max values.
- Always show the numbers in a table too. A chart without numbers can't be checked.

### Make it read well

- At the top: a clear title, the site (`api_key`), the date range in words and in dates, and "Data from
  Parse.ly, built on <date>".
- Lead with the two or three findings that matter, then the detail.
- Format numbers with thousands separators, percentages to one decimal, and say which metric each number is
  (views, visitors, engaged minutes).
- Keep it readable on a phone (`max-width` around 960px, tables that scroll sideways) and when printed.
- Plain colors with enough contrast. Don't rely on color alone to tell series apart.
- Never invent numbers. Every number on the page comes from a Parse.ly tool result in `steps`.
- The page can't call any API when it opens. All data goes in at build time, so write the dates it covers and the
  day you built it.

### Size

The HTML must be under 200 KB, and `steps` under 2 MB. When a page doesn't fit:

1. Show the top rows (the top 25 instead of 200) and say so on the page.
2. Drop columns and raw data the page doesn't display.
3. Aggregate: weekly instead of daily points.
4. If it still doesn't fit, split it into two report artifacts and tell the user.

In `steps`, keep only the part of each tool's result the page uses, and leave out rows it doesn't show.

## 3. Ask about sharing when the user didn't say

Before the first save, if the user didn't say who should open it or for how long, ask once, offering the defaults:

> I'll save it for your team for 7 days. Want it only for you, or anyone with the link, or a different length
> (1 to 90 days)?

If they say "just save it", use the defaults: `visibility: publisher`, 7 days. The `parsely-artifact-sharing` skill
has the details: who each choice lets in, how expiry works, share links, deleting and restoring.

## 4. Save it

Call `save_report_artifact` with `title` (short, recognizable in a list), `html`, `steps`, and `visibility` and
`expires_in_days` when they aren't the defaults. Give the user the `url` from the response, and say who can open it
and the date it expires. No reminder is sent before it expires.

`steps` items: `{"tool": "query_top_content", "arguments": {...}, "result": {...}, "called_at": "2026-10-24T18:00:00Z"}`,
with `called_at` as an ISO 8601 date and time.

## 5. Change a saved report artifact

When the user asks to change a report artifact they saved ("add a chart to my weekly report"):

1. Find it: `get_report_artifact` lists their report artifacts. Match the title, and ask if more than one fits.
2. Read it in full: `get_report_artifact` with `artifact_id`. Note `version`.
3. Edit that HTML. Keep what the user didn't ask to change. Get any new data with the Parse.ly tools first.
4. Save with the same `artifact_id`, `base_version` set to the `version` you read, the new `html`, and the `steps`
   for the whole page, old and new.
5. If the save is refused because it changed since you read it, read the latest version again, apply your
   change to it, and save with its `version`. Don't overwrite someone else's change.

Never create a new artifact when the user asked to change one: it would get a new link, and the old link they
already shared would keep the old page.

To change only who can open it, the expiry or the title, send `artifact_id` with just those settings and no
`html`. Every save, a change or an extension, restarts the expiry count, and a save without `expires_in_days` goes
back to 7 days. For deleting, restoring and new share links, see `parsely-artifact-sharing`.

## When something fails

- Not enabled, no access, or view-only: tell the user who to ask, as listed in `parsely-artifact-sharing`. Don't
  retry, and don't build the page with this app's own features instead.
- Limit reached: the site has too many active report artifacts. Suggest deleting old ones or letting them expire.
- Too large: follow the Size steps above and save again.
