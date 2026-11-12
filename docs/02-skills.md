# 02 — Skills

A skill is a folder with a `SKILL.md`: instructions the agent loads only when the task matches. It's an open format used by Claude Code, Codex, Antigravity and many other agents. Install them with the `skills` CLI:

```bash
npx skills add <owner/repo> -l                    # see what a repo offers, without installing
npx skills add <owner/repo> -g -a claude-code -y -s <skill> [<skill> ...]
```

`-g` = global (all your projects). `-a` = target agent: `claude-code`, `codex`, `antigravity`, ... (if an id fails, run `npx skills add --help`). To see what you have: `npx skills ls -g`.

> **Golden rule: install less, not more.** The agent reads the description of *every* skill at startup and that listing has a small budget. With 100+ skills, descriptions get truncated and the agent stops picking them by itself. Install the base set and add packs depending on what you do (see this kit's `skill-profiles` skill).

## Base set (always install)

| Repo | Skills | What for |
|---|---|---|
| `JuliusBrussee/caveman` | `caveman`, `caveman-commit`, `investigate-first`, `verify-and-stop`, `surgical-patch`, `safe-refactor`, `lean-build` | Ultra-short answers (saves tokens), clean commits and discipline: investigate before touching, minimal changes, verify before stopping |
| `mvanhorn/last30days-skill` | `last30days` | Researches what people say about a topic in the last 30 days (Reddit, X, YouTube, HN, ...) |
| `blader/humanizer` | `humanizer` | Rewrites text that sounds AI-made |
| `agentbay-ai/agentbay-skills` | `find-skills` | Finds and installs more skills when you need them |
| `anthropics/skills` | `skill-creator`, `docx`, `pdf`, `pptx`, `xlsx`, `canvas-design`, `algorithmic-art` | Official Anthropic skills: documents and creating your own skills |
| `Leonxlnx/taste-skill` | `design-taste-frontend`, `high-end-visual-design`, `redesign-existing-projects`, `imagegen-frontend-web`, `full-output-enforcement` | Anti "generic AI design" for websites; `full-output-enforcement` prevents truncated answers |
| `emilkowalski/skill` | `emil-design-eng`, `apple-design`, `improve-animations`, `animation-vocabulary` | Fine UI and motion detail |

Full base set on Claude Code:

```bash
npx skills add JuliusBrussee/caveman -g -a claude-code -y -s caveman caveman-commit investigate-first verify-and-stop surgical-patch safe-refactor lean-build
npx skills add mvanhorn/last30days-skill -g -a claude-code -y -s last30days
npx skills add blader/humanizer -g -a claude-code -y -s humanizer
npx skills add agentbay-ai/agentbay-skills -g -a claude-code -y -s find-skills
npx skills add anthropics/skills -g -a claude-code -y -s skill-creator docx pdf pptx xlsx canvas-design
npx skills add Leonxlnx/taste-skill -g -a claude-code -y -s design-taste-frontend high-end-visual-design redesign-existing-projects imagegen-frontend-web full-output-enforcement
npx skills add emilkowalski/skill -g -a claude-code -y -s emil-design-eng apple-design improve-animations animation-vocabulary
```

(Run `-l` before each one to confirm the exact names: repos change.)

## Optional packs

**Marketing and sales** — `coreyhaines31/marketingskills` (~45 skills). Pick only what you use: `copywriting`, `copy-editing`, `content-strategy`, `social`, `cold-email`, `emails`, `ads`, `ad-creative`, `seo-audit`, `pricing`, `offers`, `product-marketing`, `launch`, `marketing-psychology`, `customer-research`, `competitor-profiling`. The rest is very specific (aso, paywalls, churn, ...).

**Video as code (HyperFrames)** — `heygen-com/hyperframes`: `hyperframes`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-registry`, `media-use`, `general-video`, `motion-graphics`, `faceless-explainer`, `slideshow`. Video generated from HTML; needs Node and FFmpeg.

**Instagram** — `sergebulaev/instagram-skills` (9 skills: `ig-content-planner`, `ig-caption-writer`, `ig-carousel-planner`, `ig-hook-extractor`, `ig-hashtag-strategist`, `ig-humanizer`, `ig-profile-optimizer`, `ig-repurposer`, `ig-audience-insights`). They write captions, carousels, hooks and the content calendar; publishing is optional (via Publora, with its key) and **never without your OK**.

```bash
npx skills add sergebulaev/instagram-skills -g -a claude-code -y -s '*'
```

**Understand a project with a knowledge graph** — `graphify` (a PyPI package, not a skills repo):

```bash
pip install graphifyy        # or: uv tool install graphifyy
graphify --help              # the program installs its own skill; use /graphify inside the agent
```

**Security, OSINT and technical animation** — from the `affaan-m/ECC` repo ("Everything Claude Code": a huge collection of skills by one author). Install only these 4 with `-s` and ignore the rest:

```bash
npx skills add affaan-m/ECC -g -a claude-code -y -s security-bounty-hunter mcp-dependency-review osint-investigation manim-video
```

`security-bounty-hunter` finds reachable vulnerabilities (in your code or with permission), `mcp-dependency-review` reviews an MCP before you approve it, `osint-investigation` is a methodology for investigating from sparse clues, and `manim-video` makes technical animations.

**Documents, business and diagrams** — all verified with `-l` in their repos:

```bash
npx skills add IPedrax/OmniSkill -g -a claude-code -y -s sop-builder incident-postmortem business-case contract-review
npx skills add rampstackco/claude-skills -g -a claude-code -y -s launch-runbook
npx skills add zarazhangrui/frontend-slides -g -a claude-code -y -s frontend-slides
npx skills add coleam00/excalidraw-diagram-skill -g -a claude-code -y -s excalidraw-diagram
```

`OmniSkill` is a collection of ~53 office skills; install only those 4.

## Skills bundled in this kit

Copy the folders in [`../skills/`](../skills) to your agent's global skills folder:

| Skill | What it does |
|---|---|
| `handoff` | Summarizes the conversation into a file so you can continue in a new session (saves tokens) |
| `skill-profiles` | Turns groups of skills on/off depending on the day's work, so you don't exceed the context budget (Claude Code) |
| `youtube-scriptwriting` | Retention-focused YouTube scripts (hook, structure, outro). Included as-is; I couldn't trace its original author, if it's yours or you know whose it is, open an issue |

Global skills paths: Claude Code `~/.claude/skills/` · Antigravity `~/.gemini/config/skills/` · Codex and others: let `npx skills add -a <agent>` resolve the path.

## Security when installing skills

A skill is text that gives orders to your AI. Before installing one from an unknown author, read it (`-l`, then open the `SKILL.md`). Be wary of ones that ask you to run remote scripts, read credentials or send data out.
