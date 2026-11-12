# 07 — Portar el setup a Codex o Antigravity (plan gratis)

La idea: lo que vale es **texto** (instrucciones, skills, hábitos, memoria en archivos). Eso viaja entre agentes. Lo que es propio de Claude Code (plugins, hooks, slash commands) no.

## Qué se porta y qué no

| Pieza | Claude Code | Codex | Antigravity |
|---|---|---|---|
| Instrucciones globales | `~/.claude/CLAUDE.md` | `AGENTS.md` (proyecto) / `~/.codex/AGENTS.md` | `GEMINI.md` / `AGENTS.md` |
| Skills (`SKILL.md`) | `~/.claude/skills/` | sí (la CLI `skills` resuelve la ruta) | `<proyecto>/.agents/skills/` o `~/.gemini/config/skills/` |
| MCPs | `claude mcp add` | `~/.codex/config.toml` | panel "Manage MCP servers" |
| Memoria en archivos (`seguimiento/`) | ✅ | ✅ | ✅ |
| RTK (ahorro de terminal) | ✅ | verificar con `rtk init --help` | `rtk init --agent antigravity` |
| Plugins / marketplaces | ✅ | ❌ | ❌ |
| Hooks, modos propios, `/handoff` como comando | ✅ | ❌ (la skill se invoca por nombre) | ❌ |
| Elegir modelo por tarea / subagentes | ✅ | limitado | limitado |

Los plugins se reemplazan instalando sus skills sueltas desde `docs/02-skills.md` (por ejemplo, las de `superpowers` están en su repo `obra/superpowers` como skills individuales; verifica el repo actual con `npx skills find superpowers`).

## Pasos

1. **Instrucciones:** copia `templates/CLAUDE.global.md` al archivo que tu agente lea (`AGENTS.md` o `GEMINI.md`). Quita lo exclusivo de Claude Code (menciones a plugins/hooks/`/handoff` como comando).
2. **Skills:** `npx skills add <repo> -g -a codex -y -s ...` (o `-a antigravity`) con el set base de `docs/02-skills.md`. **En plan gratis, instala pocas** (6–10): el contexto es limitado.
3. **MCPs:** context7 y playwright según `docs/04-mcp.md`.
4. **Memoria:** crea `seguimiento/` con las plantillas. En tu archivo de instrucciones deja la regla "al empezar leer SOBRE_MI.md y el índice del área".
5. **Hábitos** de `docs/01-como-trabajo.md` y `docs/05-ahorrar-tokens.md`: valen tal cual (sesiones cortas, leer menos, respuestas cortas, verificar).

## Consejos para planes gratis

- La cuota se acaba rápido: tareas chicas y bien definidas, plan antes de ejecutar, nada de explorar "todo el repo".
- Si el agente tiene varios modelos, usa el chico para leer/buscar y el grande solo para decidir/escribir.
- Pasa el trabajo de un agente a otro con archivos (`handoff`, `seguimiento/`): cuando se acaba la cuota de uno, retomas con otro sin perder contexto.
- Mantén las instrucciones globales cortas (menos de ~100 líneas): se cargan en cada conversación.
