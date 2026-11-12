# 07 — Porting the setup to other agents (free plans included)

The idea: what's valuable is **text** (instructions, skills, habits, file-based memory). That travels between agents. What's specific to Claude Code (plugins, hooks, slash commands) doesn't.

## What ports and what doesn't

| Piece | Claude Code | Codex | Antigravity | Gemini CLI / Cursor / Windsurf / Cline |
|---|---|---|---|---|
| Global instructions | `~/.claude/CLAUDE.md` | `AGENTS.md` (project) / `~/.codex/AGENTS.md` | `GEMINI.md` / `AGENTS.md` | their rules file (`GEMINI.md`, `.cursor/rules`, ...) |
| Skills (`SKILL.md`) | `~/.claude/skills/` | yes (the `skills` CLI resolves the path) | `<project>/.agents/skills/` or `~/.gemini/config/skills/` | yes if the agent reads `SKILL.md`; use `npx skills add -a <agent>` |
| MCP servers | `claude mcp add` | `~/.codex/config.toml` | "Manage MCP servers" panel | their MCP config |
| File-based memory (`tracking/`) | ✅ | ✅ | ✅ | ✅ |
| RTK (terminal savings) | ✅ | check `rtk init --help` | `rtk init --agent antigravity` | `--gemini`, `--agent cursor`, `windsurf`, `cline`, ... |
| Plugins / marketplaces | ✅ | ❌ | ❌ | ❌ |
| Hooks, mods, `/handoff` as a command | ✅ | ❌ (invoke the skill by name) | ❌ | ❌ |
| Per-task model choice / subagents | ✅ | limited | limited | varies |

Plugins are replaced by installing their loose skills from `docs/02-skills.md` (for example `superpowers` skills live in its repo `obra/superpowers`; check the current repo with `npx skills find superpowers`).

## Steps

1. **Instructions:** copy `templates/global-instructions.md` into the file your agent reads (`AGENTS.md`, `GEMINI.md`, a rules file). Remove Claude Code-only bits (mentions of plugins/hooks/`/handoff` as a command).
2. **Skills:** `npx skills add <repo> -g -a codex -y -s ...` (or `-a antigravity`, ...) with the base set in `docs/02-skills.md`. **On a free plan, install few** (6–10): context is limited.
3. **MCPs:** context7 and playwright per `docs/04-mcp.md`.
4. **Memory:** create `tracking/` from the templates. In your instructions file keep the rule "at the start read ABOUT_ME.md and the area index".
5. **Habits** from `docs/01-workflow.md` and `docs/05-save-tokens.md` apply as-is (short sessions, read less, short answers, verify).

## Tips for free plans

- Quota runs out fast: small, well-defined tasks, plan before executing, never "explore the whole repo".
- If the agent has several models, use the small one to read/search and the big one only to decide/write.
- Pass work between agents with files (`handoff`, `tracking/`): when one agent's quota runs out, resume with another without losing context.
- Keep the global instructions short (under ~100 lines): they load in every conversation.
