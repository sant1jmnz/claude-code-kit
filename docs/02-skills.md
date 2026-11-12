# 02 — Skills

Una skill es una carpeta con un `SKILL.md`: instrucciones que el agente carga solo cuando la tarea coincide. Es un formato abierto que usan Claude Code, Codex y Antigravity. Se instalan con la CLI `skills`:

```bash
npx skills add <owner/repo> -l                    # ver qué trae, sin instalar
npx skills add <owner/repo> -g -a claude-code -y -s <skill> [<skill> ...]
```

`-g` = global (todos tus proyectos). `-a` = agente: `claude-code`, `codex`, `antigravity` (si el id falla, `npx skills add --help`). Para ver qué tienes: `npx skills ls -g`.

> **Regla de oro: instala menos, no más.** El agente lee la descripción de *todas* las skills al arrancar y ese listado tiene un presupuesto chico. Con 100+ se recortan descripciones y el agente deja de elegirlas solo. Instala el set base y suma paquetes según lo que hagas (ver la skill `perfiles` de este kit).

## Set base (instalar siempre)

| Repo | Skills | Para qué |
|---|---|---|
| `JuliusBrussee/caveman` | `caveman`, `caveman-commit`, `investigate-first`, `verify-and-stop`, `surgical-patch`, `safe-refactor`, `lean-build` | Respuestas ultra cortas (ahorra tokens), commits limpios y disciplina: investigar antes de tocar, cambios mínimos, verificar antes de parar |
| `mvanhorn/last30days-skill` | `last30days` | Investiga qué dice la gente sobre un tema en los últimos 30 días (Reddit, X, YouTube, HN…) |
| `blader/humanizer` | `humanizer` | Reescribe textos que suenan a IA |
| `agentbay-ai/agentbay-skills` | `find-skills` | Encuentra e instala más skills cuando las necesites |
| `anthropics/skills` | `skill-creator`, `docx`, `pdf`, `pptx`, `xlsx`, `canvas-design`, `algorithmic-art` | Skills oficiales de Anthropic: documentos y creación de skills propias |
| `Leonxlnx/taste-skill` | `design-taste-frontend`, `high-end-visual-design`, `redesign-existing-projects`, `imagegen-frontend-web`, `full-output-enforcement` | Anti "diseño genérico de IA" en webs; `full-output-enforcement` evita respuestas recortadas |
| `emilkowalski/skill` | `emil-design-eng`, `apple-design`, `improve-animations`, `animation-vocabulary` | Detalle fino de interfaz y movimiento |

Ejemplo (set base completo en Claude Code):

```bash
npx skills add JuliusBrussee/caveman -g -a claude-code -y -s caveman caveman-commit investigate-first verify-and-stop surgical-patch safe-refactor lean-build
npx skills add mvanhorn/last30days-skill -g -a claude-code -y -s last30days
npx skills add blader/humanizer -g -a claude-code -y -s humanizer
npx skills add agentbay-ai/agentbay-skills -g -a claude-code -y -s find-skills
npx skills add anthropics/skills -g -a claude-code -y -s skill-creator docx pdf pptx xlsx canvas-design
npx skills add Leonxlnx/taste-skill -g -a claude-code -y -s design-taste-frontend high-end-visual-design redesign-existing-projects imagegen-frontend-web full-output-enforcement
npx skills add emilkowalski/skill -g -a claude-code -y -s emil-design-eng apple-design improve-animations animation-vocabulary
```

(Antes de cada uno, `-l` te confirma los nombres exactos: los repos cambian.)

## Paquetes opcionales

**Marketing y ventas** — `coreyhaines31/marketingskills` (~45 skills). Elige solo las que uses: `copywriting`, `copy-editing`, `content-strategy`, `social`, `cold-email`, `emails`, `ads`, `ad-creative`, `seo-audit`, `pricing`, `offers`, `product-marketing`, `launch`, `marketing-psychology`, `customer-research`, `competitor-profiling`. El resto es muy específico (aso, paywalls, churn…).

**Video con código (HyperFrames)** — `heygen-com/hyperframes`: `hyperframes`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-registry`, `media-use`, `general-video`, `motion-graphics`, `faceless-explainer`, `slideshow`. Video generado desde HTML; necesita Node y FFmpeg.

**Otras que uso y no vienen de un repo que pueda garantizar** (búscalas por nombre con `npx skills find <nombre>` y revisa la fuente antes de instalar): `youtube-scriptwriting`, `manim-video`, `excalidraw-diagram`, `frontend-slides`, `graphify` (grafo de conocimiento de un repo), `security-bounty-hunter`, `mcp-dependency-review`, `osint-investigation`, `business-case`, `contract-review`, `incident-postmortem`, `sop-builder`, `launch-runbook`, y un set de skills para Instagram (`ig-caption-writer`, `ig-carousel-planner`, `ig-hook-extractor`…).

## Skills propias de este kit

Copia las carpetas de [`../skills/`](../skills) a la carpeta global de skills de tu agente:

| Skill | Qué hace |
|---|---|
| `handoff` | Resume la conversación en un archivo para continuar en una sesión nueva (ahorra tokens) |
| `perfiles` | Activa/desactiva grupos de skills según el trabajo del día, para no pasarte del presupuesto de contexto |

Rutas globales de skills: Claude Code `~/.claude/skills/` · Antigravity `~/.gemini/config/skills/` · Codex: deja que `npx skills add -a codex` resuelva la ruta.

## Seguridad al instalar skills

Una skill es texto que le da órdenes a tu IA. Antes de instalar una de un autor desconocido, léela (`-l` y abre el `SKILL.md`). Desconfía de las que piden ejecutar scripts remotos, leer credenciales o mandar datos afuera.
