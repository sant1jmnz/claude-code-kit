# 05 — Save tokens

On a free or trial plan, quota is the main limit. These habits add up. Ordered by impact.

## 1. Short, focused sessions
- One task = one session. When a topic closes, `/handoff` and a new session. A huge conversation is re-read in full on every message.
- `/clear` between unrelated topics. `/compact` if you must stay in the same one.
- What matters goes to files (see `06-memory.md`), not the conversation.

## 2. Pick the right model and effort
- **Haiku-class (small)**: searching, bulk reading, summarizing, classifying. Cheap and fast.
- **Sonnet-class (mid)**: day to day (code, text, design).
- **Opus-class (large)**: only hard problems, architecture, stubborn debugging.
- Reasoning effort: *medium* by default; raise it only on complex tasks. Simple questions don't need high effort.

## 3. Subagents with judgment
A subagent reads a lot and returns a short summary: your conversation doesn't fill up. Use one for long searches and bulk reading, **with a small model (Haiku)**. Subagents on big models (parallel reviews, "ultra", broad exploration) burn a lot: use them only when you explicitly ask.

## 4. Read less
- `grep` / search before opening a file; open only the range you need.
- Don't reread a file you just edited "to verify": the tool already reports failures.
- When material is long and necessary, have a Haiku subagent read it and return what's relevant.

## 5. Filtered command output: RTK
RTK ("Rust Token Killer") is a proxy that trims terminal command output (git, ls, tests, builds) before it reaches the model. It saves a large share of terminal-reading tokens.

1. Install it from the *releases* of the `rtk-ai/rtk` repo on GitHub (or `cargo install` if you have Rust). **Watch for the name clash:** another program is also called `rtk` (Rust Type Kit). Check with `rtk gain`: it must show token statistics; if it errors, it's the wrong one.
2. Enable the global hook: `rtk init -g` (other agents: `rtk init -g --agent antigravity`, `--gemini`, `--opencode`, ...; see `rtk init --help`).
3. From then on `git status` is rewritten to `rtk git status` automatically. See what you saved with `rtk gain`.

## 6. Short answers
- Telegram style with the `caveman` skill (or the "Response style" section of the global-instructions template). Fewer output tokens and faster to read.
- `ponytail`: shorter code = fewer tokens and fewer bugs.
- Don't ask "explain everything": ask for the result and ask for detail if needed.

## 7. Fewer tools loaded
- Few MCPs, few plugins, few active skills (`skill-profiles` skill).
- Connectors (Gmail, Drive, ...) off until needed.

## 8. Parallel and background work
- Independent calls in the same turn (the agent can do several reads at once).
- Long processes (renders, downloads, scripts) in the background, in one pass, **without polling** (don't keep asking whether it finished: the system notifies you).
- Visual review: one contact sheet at the end instead of dozens of screenshots.

## 9. Measure
`rtk gain` for terminal output. In Claude Code, `/cost` or the usage panel to see where quota goes; fix the habit that weighs the most.

## 10. Automatic savers
The community mods in [`08-token-saving-mods.md`](08-token-saving-mods.md) do several of these for you (small models read big files, screenshots shrink, effort is suggested per prompt).
