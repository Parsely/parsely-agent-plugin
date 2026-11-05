# Publishing the plugin

Claude is the default format. The repo root is a working Claude plugin, so Claude reads it directly from GitHub with no
build step. Every other platform gets an export built from the same files. Today that means one ZIP for OpenAI.

## What ships where

| Change | Where it lives | How it reaches users |
|---|---|---|
| Skills, plugin metadata, icons | This repo | A new plugin version, submitted to each platform |
| MCP tools, tool descriptions, server instructions | The Parse.ly dashboard code | Deploying the dashboard. No plugin release needed, but see [MCP changes](#mcp-changes) |
| MCP server URL | `.mcp.json`, `server.json` and each platform's listing | All of those by hand. OpenAI needs a support request |

| Platform | What it reads | How to update |
|---|---|---|
| Claude | This public repo for the plugin, the server URL for the connector | Merge to the tracked branch. The connector follows the server |
| OpenAI (ChatGPT, Codex) | A ZIP from `scripts/build_openai.sh` | Upload the ZIP in the portal |
| MCP registry | `server.json` | Publish only when `server.json` changes |
| Any other MCP client | The server URL | Nothing to do. These clients get the tools without the skills |

## Prepare a release

Every platform starts here.

```bash
python3 scripts/sync_tools.py ../dash origin/main   # refresh tools.json from the dash tool snapshots
python3 scripts/check_skills.py                     # also reads your local denylist, which CI can't see
python3 scripts/bump_version.py <version>           # one version across every manifest
claude plugin validate .                            # Claude's manifest check
bash scripts/build_openai.sh                        # writes dist/parsely-openai-<version>.zip
```

Commit, tag `v<version>` and push. CI runs the same checks and keeps the ZIP as a build artifact.

## Claude

Claude takes two submissions, both in the [developer portal](https://claude.ai/directory/manage): the MCP server as a
connector, then this repo as a plugin bundle. A connector listing can't carry skills, so the skills need the bundle.

Submitting takes a paid plan. On Team and Enterprise, an Owner submits, or on Enterprise someone with the **Directory**
permission. The first organization to submit a repo folder holds that listing, so submit from the Automattic one.

**First submission**

1. Make sure the connector is listed. If it isn't, choose **Submit new**, then **MCP connector**, and enter the server URL.
2. Choose **Submit new**, then **Plugin bundle**, and fill in **Source**:
   - **Repository:** `Parsely/parsely-agent-plugin`.
   - **Plugin path:** leave empty, because the plugin is at the repo root.
   - **Branch or tag:** leave empty to follow `main`.
3. Select **Validate** and fix what it reports. A result covers one commit, so validate again after any push.
4. Check **Listing details**, which come from `.claude-plugin/plugin.json` and the README. To change them, change those
   files.
5. Answer **Data handling** and **Compliance**.
6. In **Review and submit**, choose **Auto-publish passing versions** and how new versions arrive. **GitHub push webhook**
   is the default and needs admin access to the repo. Then select **Submit for review**. Review time isn't fixed.
7. Pair the bundle with the connector. Both must come from the same organization, and `.mcp.json` should keep the
   connector's URL, so people who have both see one set of tools. Claude's docs don't show where this control is, so look
   for it on the listings in the portal.

**Updates**

1. Raise `version`.
2. Merge to `main`. The directory finds the commit on a schedule, on the webhook, or when you select
   **Check for new commits**.
3. Each version gets a validation and security scan. Users keep the last published version until a new one goes live.
4. Check the **Auto-publish** row on the plugin's Overview tab to see what happens next:
   - By default, you select **Publish** on each passing version, and a reviewer publishes it.
   - With auto-publish on, a reviewer publishes only the first version. Later passing versions go live by themselves,
     unless the plugin is waiting for a reviewer.

A clean `claude plugin validate` doesn't guarantee a clean portal validation. The portal also checks the README, the
license and the rest of the folder, as the [checklist](https://claude.com/docs/plugins/pre-submission-checklist) explains.

Docs: [publish to the directory](https://claude.com/docs/directory/publish), [submit a plugin](https://claude.com/docs/plugins/submit).

## OpenAI

OpenAI never reads this repo. It reads the ZIP, which holds `.codex-plugin/plugin.json`, `.mcp.json`, `skills/`, `assets/`,
the README and the license. The build writes its own `.mcp.json` without `type`, the format OpenAI documents. The ZIP must
declare the MCP server: the portal rejects a package that omits it, because removing the MCP isn't supported.

1. Open [Plugins](https://platform.openai.com/plugins) and select the Parse.ly plugin. Submitting takes an organization
   owner or **Apps Management Write**.
2. Select **Upload plugin to make changes** and choose the ZIP. It must be complete, with a new version number.
3. Fix anything under **Metadata & Skills**. Required skill scans must pass before you can submit. Under **MCPs**, check
   the connection and scanned tools, and select **Reconnect** if it needs attention.
4. Use the cases in `docs/openai-review.md` if the portal asks for test cases. Reviewer credentials go in the secure
   **Review details** form, never in the ZIP.
5. Select **Submit for review**. Feedback arrives by email. Only one review can be active, so to replace a package under
   review, wait for the decision or cancel the review first.
6. After approval, open the approved version and select **Publish plugin**. It replaces the previous version.

Keep these as they are:

- **`name` in `.codex-plugin/plugin.json`.** It is the id OpenAI gave the existing app.
- **No root `plugin.json` or `mcp.json`.** A root `plugin.json` with OpenAI settings replaces the `.codex-plugin` manifest.
- **No hooks or app references in the ZIP.** OpenAI rejects them.

Docs: [package a plugin](https://developers.openai.com/plugins/build/plugins), [submission](https://developers.openai.com/plugins/deploy/submission).

## MCP registry

Publish `server.json` with the registry's `mcp-publisher` tool, only when it changes. Its version is separate from the
plugin version. The key that proves we own the `com.parsely.dash` name isn't in this repo, so ask a maintainer.

## MCP changes

Tool changes deploy with the dashboard, without a new ZIP or plugin version. Run `sync_tools.py` and `check_skills.py`
afterwards, because a renamed or removed tool breaks any skill that names it.

**OpenAI** scans the server daily. To scan sooner, select **MCPs**, the server, then **Rescan** under **Issues**.

- OpenAI checks each tool change separately, and changes that pass go live by themselves.
- A new tool stays unavailable until it is approved.
- A flagged change to an existing tool is held, and users keep the approved version until then.
- A removed tool goes away after the scan.
- Keep the server compatible with the approved tool schemas until the new ones are live, or held tools will break.
- Changed server instructions show as "need further review" with a diff. That means they wait for review. It isn't an
  objection. OpenAI's docs don't describe this step, so check the portal.

**Claude** picks up tool changes from the deployed server, with no portal step for the server itself.

- Tool names on the connector's listing are separate. Update them with a listing edit, which a reviewer approves.
- Changing the connector's display name also needs re-review.
- Claude's docs don't say whether tool changes get re-scanned or how fast clients see them, and they set no process for
  breaking changes. For anything beyond this, email `mcp-review@anthropic.com`.

Docs: [after publishing](https://claude.com/docs/connectors/building/after-publishing), [managing your listing](https://claude.com/docs/connectors/building/managing-your-listing).

## Add another platform

Keep the repo root as the Claude plugin and add a build script next to `scripts/build_openai.sh`. It should package the
same `skills/` folder, plus any manifest that platform needs. Skills stay free of platform names, as `AGENTS.md` requires.
