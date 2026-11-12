# 06 — File-based memory

The agent remembers nothing between sessions on its own. The simple, portable fix: **a folder of Markdown files** the agent reads at the start and updates in batches. It works the same on Claude Code, Codex, Antigravity and any other agent.

## Structure

```
tracking/
├── ABOUT_ME.md               ← who you are and how you like to work (always read)
├── TRACKING.md               ← general index: areas and where everything is
├── <area>/                   ← e.g. work/, study/, personal/
│   ├── TRACKING.md           ← SHORT index of the area: one line per project + status
│   ├── RULES.md              ← rules that apply only in this area
│   └── projects/
│       └── <project>.md      ← the detail (decisions, to-dos, data)
└── handoffs/                 ← summaries to continue in a new session
```

Ready-made templates in [`../templates/memory/`](../templates/memory).

## Usage rules (also in the global-instructions template)

1. **At the start of a task:** identify the area, read `ABOUT_ME.md`, the area index, its `RULES.md` and **only** the project file for the task. Don't read everything.
2. **Short index, detail elsewhere.** The index only points; reading context costs few tokens.
3. **An area's rules don't apply to another.** If the area is unclear, ask.
4. **Batched saving.** Don't edit the tracking files on every decision (it burns tokens and slows the work). Accumulate decisions, data and new rules and write them in **one** edit when: (a) ~5 new things piled up, (b) an important topic closes, (c) the person says "save this", or (d) the session is about to end. Confirm in one line only when saving.
5. **New rules** go to `RULES.md` with a date, in the same batch.
6. **Look up old stuff** with `grep`, or with a Haiku subagent that reads and returns a short summary. Don't load whole histories.
7. **Learn the person.** If the agent notices a new, relevant preference or limit, it updates `ABOUT_ME.md` (the person can correct or delete anything).

## Claude Code's native memory

Claude Code also has automatic memory (`~/.claude/projects/<project>/memory/`) for short preferences and loose facts. Use it for short, long-term stuff; the `tracking/` folder is for the detail of projects and areas.

## Continue in a new session: `/handoff`

The `handoff` skill (in [`../skills/handoff`](../skills/handoff)) writes a summary into `tracking/handoffs/` with: what was done, what's left, which skills to use and which files to read. In the new session you only paste: `Read <path> and continue`.

## Automate a weekly summary (optional)

A script or scheduled task can, once a week, summarize recent sessions into `tracking/`. It must tolerate the computer being off (run at next boot if it was skipped). Optional; not needed to start.
