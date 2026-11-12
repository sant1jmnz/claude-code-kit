# 08 — Token-saving mods (Claude Code only)

**Mods** are plugins that hook into Claude Code's own interface (side panes, hooks on your prompt, tool results). This pack, by **Ben AI**, cuts tokens automatically. It's published on GitHub; it is not copied into this repo (it declares no license): install it from its source.

Source: <https://github.com/michaelzwiener/claude-mods> · directory: <https://claudemods.si>

## Requirements
- Claude Code **2.1.287+** in the terminal (or 2.1.286+ in the desktop app) with *function hooks* available. If `/mods` doesn't show up at the end, your version doesn't have them: update, or skip this phase.
- Windows: PowerShell 5.1 (built in). Optional: Poppler (so `input-router` can read PDFs) and the Firecrawl CLI (for `research-router`).

## Install

```
/plugin marketplace add michaelzwiener/claude-mods
/plugin install input-router@token-saving-mods
/plugin install effort-optimizer@token-saving-mods
/plugin install model-router@token-saving-mods
/plugin install handoff@token-saving-mods
/plugin install research-router@token-saving-mods
/plugin install efficient-browser-use@token-saving-mods
/plugin install mods@token-saving-mods
/plugin install savings-proof@token-saving-mods
/reload-plugins
```

Check with `/mods` (pane listing all mods; turn each on or off there) and `/savings` (how many tokens each one saved).

## What each one does

| Mod | What it does |
|---|---|
| `input-router` | Big files and connector results are read first by Haiku; Claude gets short notes and the path to the original. `/input-router full` lets the next one through whole |
| `effort-optimizer` | Reads each prompt and suggests the effort level it needs (or switches it by itself in auto mode) |
| `model-router` | Before launching a subagent, Haiku decides whether the task can go to a cheaper model (only with high confidence). Doesn't touch the main chat's model |
| `handoff` | At ~250k tokens offers "Refresh": summarizes the chat and continues in a new one |
| `research-router` | Keeps web research out of the main chat: a cheap worker reads pages and returns a summary with sources |
| `efficient-browser-use` | Shrinks every screenshot Claude takes while driving a browser (or has Haiku describe it in text) |
| `mods` | Pane to see and turn all mods on/off |
| `savings-proof` | `/savings`: proof of how much each mod saved today and in this chat |
| `cache-clock` *(optional)* | Countdown until the chat's prompt cache goes cold |

The same repo also has `helper-desk` (task progress bar and a card per subagent) and `chat-inventory` (what this chat used).

## Precautions
- `input-router` and `research-router` summarize with Haiku: they save a lot but can lose detail. If you need the full original, use the `full` commands.
- They're third-party mods: read the code before installing, as with any plugin.
- `skill-guide` (from this repo, in `plugins/skill-guide`) is also a mod: `/plugin marketplace add sant1jmnz/claude-code-kit` then `/plugin install skill-guide@claude-code-kit`.
