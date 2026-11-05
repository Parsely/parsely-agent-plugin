---
name: parsely-marketing-questions
description: Answer marketing's three standing questions from Parse.ly data — where good content is under-promoted, how exposed the site is to a Google change, and whether AI assistants send more readers and to what. Use when the user asks about under-promoted content, search or Google dependency, AI referrals (ChatGPT, Perplexity, Gemini), or for a marketing review.
---

# Marketing's three questions

Three questions, each answered in one sentence with the table behind it. Follow the `parsely-reports` skill for
windows, sources and guardrails.

**Dates:** ask for the start and end dates before any query (see `parsely-reports`). Suggest the last 28 full days ending yesterday, against the 28 days before.

## 1. Where are we under-promoting good content?

- `query_top_content` by `engaged_minutes` (top 50) and by `views` (top 100), same window.
- Under-promoted: high engaged minutes per visitor but outside the top views. Show title, URL as text, section,
  views, engaged minutes and minutes per visitor.
- Answer: "These N posts hold readers longer than the site average but get few views: link or promote them."

## 2. How exposed are we to a Google change?

- `query_referrers` by category: the search share of views, this window and last.
- `query_top_aspect` with `aspect=sections` and `referrers_category=search`, and `query_top_content` with
  `referrers_category=search`: which sections and posts depend most on search.
- If `query_search_console` returns data for this site, add top keywords and Discover vs Search clicks. If it
  returns nothing, say Search Console isn't connected and skip it.
- Answer with a sized example: "If search traffic fell 20%, about X views a month would go, mostly in sections A
  and B." Show the arithmetic.

## 3. Are AI assistants sending more people, and to what?

- `query_referrers` with `category=ai` for both windows: views by assistant domain.
- `query_top_content` and `query_top_aspect` (`aspect=sections`) with `referrers_category=ai`.
- Answer: the change in AI-referred views, which assistants, and what kind of content they send readers to.

## Output

One sentence per question, then its table. When the user wants to share it, build a Parse.ly report artifact
(`parsely-report-artifacts`).
