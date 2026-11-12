# skill-guide

A Claude Code "mod" (panel + hook on your prompt) that fixes the problem of having many skills and not knowing which one to use.

- **`/guide`** opens a panel: task → skill → example of how to ask. Skills you don't have installed are greyed out.
- **As you type**, if your request matches a task ("plan this week's posts", "armá un carrusel sobre…"), it asks whether to use the matching skill. Works in English and Spanish. It only suggests skills you have installed, and you can choose "Don't suggest again this session".

## Install

```
/plugin marketplace add sant1jmnz/claude-code-kit
/plugin install skill-guide@claude-code-kit
/reload-plugins
```

Needs a Claude Code version with mods (function hooks, see `docs/08-token-saving-mods.md`).

## Customize

Edit `hooks/register.tsx`:
- `GUIDE`: the panel rows.
- `RULES`: keyword → skill. One regex per rule; the first match wins.
