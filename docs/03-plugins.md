# 03 — Plugins (Claude Code only)

Plugins bundle skills, commands, hooks and agents. They install from a *marketplace* (a GitHub repo). In Claude Code:

```
/plugin marketplace add <owner/repo>
/plugin install <plugin>@<marketplace>
```

Restart afterwards. `/plugin` shows the status.

## Base set

| Plugin | Marketplace (repo) | What it adds |
|---|---|---|
| `superpowers` | `claude-plugins-official` (built in) | **The most important one.** Full flow: brainstorming → plan → execution → review → verification, TDD, systematic debugging, worktrees |
| `claude-security` | `claude-plugins-official` | Code security scanning and verified patches |
| `frontend-design` | `claude-code-plugins` (`anthropics/claude-code`) | UI design with its own judgment, not generic |
| `ui-ux-pro-max` | `ui-ux-pro-max-skill` (`nextlevelbuilder/ui-ux-pro-max-skill`) | Database of styles, palettes, typefaces and UX guidelines for web and mobile |
| `ponytail` | `ponytail` (`DietrichGebert/ponytail`) | "Lazy senior dev" mode: the shortest code that solves the problem, no over-engineering |

```
/plugin marketplace add anthropics/claude-code
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin marketplace add DietrichGebert/ponytail
/plugin install superpowers@claude-plugins-official
/plugin install claude-security@claude-plugins-official
/plugin install frontend-design@claude-code-plugins
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/plugin install ponytail@ponytail
```

## Optional

| Plugin | Marketplace | What for |
|---|---|---|
| `ux-design`, `marketing-cro`, `sales-influence` | `wondelai-skills` (`wondelai/skills`) | Books on UX design, conversion and sales turned into skills (heuristics, microinteractions, persuasion) |
| `egm` | `egm` (`google/elephant-goldfish-model`) | Write a plan on paper and have parallel reviewers critique it **before** coding big projects |
| `claude-video-vision` | `claude-video-vision` (`jordanrendric/claude-video-vision`) | Lets Claude "watch" videos (frames + audio). Needs FFmpeg |

## Mods

- **`skill-guide`** (from this repo): `/guide` opens a "task → skill → how to ask" panel and, as you type, suggests the right skill (EN/ES) only if you have it installed.
  ```
  /plugin marketplace add sant1jmnz/claude-code-kit
  /plugin install skill-guide@claude-code-kit
  ```
- **Token-saving mods** (Ben AI): see [`08-token-saving-mods.md`](08-token-saving-mods.md).

## Watch your quota

Each plugin adds skills and agents to the startup listing. On a free or trial plan, start with `superpowers` + `ponytail` + `frontend-design` and add the rest when you need them. Parallel-review plugins (`egm`, "ultra" reviews) launch many subagents: they burn a lot.
