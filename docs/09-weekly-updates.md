# 09 — Weekly updates and the anti-slop rule

Two always-on habits. Both are cheap and both are in the instructions you install.

## Rule #1: AI slop is forbidden

Slop is output that looks mass-produced: generic, padded, templated, unverifiable. The agent must (1) not produce it and (2) **tell you whenever something might be or look like slop** instead of shipping it silently.

- The rule sits at the top of [`templates/global-instructions.md`](../templates/global-instructions.md), so it loads in every conversation.
- The [`anti-slop`](../skills/anti-slop/SKILL.md) skill holds the detailed checklist (text, UI, code, media, data) and the exact reporting format: *"Possible AI-slop: what, where, why it reads generic, fix or proposal."*
- Companions: `humanizer` (rewrite AI-sounding prose), `design-taste-frontend` (anti-generic UI).

## Weekly update check

Skills, plugins and MCP servers are written by other people and change often. A weekly job tells your agent to look for updates and report; **it never installs anything without your OK** (updating third-party instructions/code is a supply-chain decision).

What it checks (read-only, via [`skills/weekly-update/check-updates.py`](../skills/weekly-update/check-updates.py)):

| Item | How |
|---|---|
| Agent CLI (Claude Code) | local version vs latest on npm |
| Skills installed with the `skills` CLI | source repo has commits newer than your install date |
| Claude Code plugins | marketplace repo has newer commits |
| MCP servers pinned to an npm version | newer release on npm |
| RTK | local version vs latest GitHub release |

It then triages (what, current → latest, risk), writes a short report to `tracking/updates/YYYY-MM-DD.md`, and asks once what to apply. Uses `gh` if you have it (higher GitHub rate limit), else the public API.

### Schedule it (pick your agent)

The task prompt is always the same:

> Use the weekly-update skill: run the update check, write the report, and ask me what to apply. Change nothing without my OK.

- **Claude Code desktop app:** create a scheduled task (weekly, e.g. Sundays 10:00). It runs while the app is open and, if the app was closed, on next launch.
- **Claude Code CLI**
  - macOS/Linux cron: `0 10 * * 0 claude -p "<prompt>"`
  - Windows Task Scheduler: `schtasks /create /sc weekly /d SUN /st 10:00 /tn "agent-weekly-update" /tr "claude -p \"<prompt>\""` and enable *Run task as soon as possible after a scheduled start is missed*, so it survives a powered-off PC.
- **Codex:** same pattern with `codex exec "<prompt>"`. **Gemini CLI:** `gemini -p "<prompt>"`.
- **Agents with no headless mode (e.g. Antigravity):** set a weekly calendar reminder that says "tell my agent: use the weekly-update skill".

Headless runs can't answer questions: they write the report and stop; you approve the updates the next time you open the agent.
