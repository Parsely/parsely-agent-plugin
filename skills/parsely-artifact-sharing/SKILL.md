---
name: parsely-artifact-sharing
description: Explain and manage who can open a Parse.ly report artifact and for how long — visibility (only me, my team, anyone with the link), expiry and extending it, new share links, versions, deleting and restoring, limits, and what to do without access. Use when the user asks who can see a saved report artifact, how to share it with their team or outside it, when it expires, how to extend, revoke, delete or restore it, why a link stopped working, or why they can't save one.
---

# Sharing report artifacts

Facts about who can open a report artifact and for how long. Use them to answer the user's questions plainly, and
to set `visibility` and `expires_in_days` when saving with `save_report_artifact` (see `parsely-report-artifacts`).

Report artifacts sit under **Reports → Artifacts** in the Parse.ly dashboard, next to recent and scheduled
reports. They are not scheduled reports: they never run again by themselves or arrive by email.

## Who can open it

Three choices, shown in the dashboard as "Only me", "My team" and "Anyone with the link":

| `visibility` | Who can open it | Sign-in needed |
|---|---|---|
| `private` — Only me | the person who saved it, and the site's admins | yes |
| `publisher` — My team (the default) | people on the user's Parse.ly team who can open the site and may view report artifacts | yes |
| `link` — Anyone with the link | anyone who has the share link, inside or outside the company | no |

- Use `link` only when the user asked to share outside their team. Say clearly that anyone holding the link can
  open it, without signing in.
- Pick from what the user said ("just me", "my team", "the client"). If they didn't say, ask once, offering "my team
  for 7 days" as the default.
- Changing who can open it doesn't change the page: send `artifact_id` with the new `visibility` and no `html`.

## How long it lasts

- A report artifact expires 1 to 90 days after it is saved. **The default is 7 days.**
- **Every save restarts the count**, including a save that only changes the page. A save without
  `expires_in_days` goes back to 7 days, so send the length again when the user had chosen a longer one.
- When it expires, nothing is deleted, but the link stops working for everyone, the owner included. People
  opening it see "This report isn't available".
- No reminder email is sent before it expires. Tell the user the end date when you save, so they can plan.
- To extend it, or bring an expired one back, save it again with `artifact_id` and a new `expires_in_days`. In
  the dashboard this is "Share and extend".

## Share links

- `link` report artifacts have a share link that works without signing in. Give it to the user exactly as the
  response returns it.
- To stop an old share link from working, save with `artifact_id` and `new_share_link: true`. The old link stops at
  once; anyone who still needs it must get the new one.
- Team members can always open it from the Artifacts tab while it hasn't expired, whatever the share link.

## Versions

- Saving a change adds a version behind the same link. The last 10 versions are kept.
- Readers see the latest version. The owner and admins can open older ones and restore one in the viewer.

## Delete and restore

- To delete one, save with `artifact_id` and `archived: true`. The link stops working for everyone right away.
- Nothing is lost: a site admin can restore it from the Artifacts tab (filter "Archived"). Only admins can restore.
- Confirm before you delete or create a new share link, since both break links people may already have.

## Limits

- A site can have up to 100 active report artifacts, unless Parse.ly set a different limit. When it's full, the
  save fails; suggest deleting old ones or letting them expire, which frees a slot.
- Each page must be under 200 KB, and its source trail under 2 MB. See `parsely-report-artifacts` for how to shrink
  one.

## When the user can't open or save one

Read the error and tell the user what it means:

- **"not enabled for this site"** — report artifacts are turned off for the site. Tell them to ask their Parse.ly
  contact to turn them on.
- **"aren't enabled for you"**, or **"don't have access"** — they need the "View Report Artifacts" permission. Tell
  them to ask their site admin, under Users and permissions.
- **"can view … but not save or change them"** — they need "View and Manage Report Artifacts" from their site
  admin.
- **"This report isn't available"** on a link — it expired, was deleted, got a new share link, or they aren't
  allowed to open it. The owner or an admin can check it on the Artifacts tab.

Never retry a save that failed for permissions, and don't offer a way around it.
