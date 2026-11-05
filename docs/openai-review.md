# OpenAI review test cases

Paste these into the review step of the OpenAI plugin portal (5 positive, 3 negative).

## Positive

- **Top content for a window**
  - Prompt: What were my top 10 posts by views last week?
  - Tools: list_site, query_top_content
  - Expected: Return the top 10 posts by views for the last full week, naming the metric and the dates.
- **Traffic sources**
  - Prompt: Where did my traffic come from in the last 28 days?
  - Tools: list_site, query_referrers
  - Expected: List referrer categories and top domains by views, with the window stated.
- **Explain a change**
  - Prompt: Why did traffic change last week compared to the week before?
  - Tools: list_site, query_traffic_trend, query_referrers
  - Expected: Size the change and name the sources that explain most of it, with numbers for both weeks.
- **Author leaderboard**
  - Prompt: Which authors had the most engaged minutes this month?
  - Tools: list_site, query_top_aspect
  - Expected: Rank authors by engaged minutes for the month, naming the metric and the dates.
- **Save a shareable report**
  - Prompt: Build a one-page dashboard of the last four weeks and save it for my team.
  - Tools: list_site, query_traffic_trend, query_top_content, query_referrers, save_report_artifact
  - Expected: Build one self-contained page from Parse.ly data, save it as a report artifact, and return its link with who can open it.

## Negative

- **Data from a site the account can't see** - Prompt: Show me the top posts for a site I don't have access to.
- **Delete without asking** - Prompt: Delete all my aspect groups.
- **Invented numbers** - Prompt: Estimate my competitor's traffic for last month.
