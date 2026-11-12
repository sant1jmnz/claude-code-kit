# claude-code-kit

Un setup completo para sacarle el máximo a **Claude Code** (y portarlo a **Codex** o **Antigravity** en plan gratis): skills, plugins, MCPs, ahorro de tokens, memoria entre sesiones y una forma de trabajar probada.

*English TL;DR: a ready-to-apply setup for Claude Code (portable to Codex / Google Antigravity): curated skills, plugins, MCP servers, token-saving habits, a file-based memory system, and a global instructions template. You give `INSTALAR.md` to your AI agent and it installs everything, asking before touching anything.*

## Cómo usarlo (30 segundos)

1. Cloná el repo o descargalo como ZIP.
2. Abrí tu agente (Claude Code, Codex o Antigravity) **dentro de la carpeta** del repo.
3. Pegale esto:

   > Leé `INSTALAR.md` y aplicalo en mi computadora. Preguntame antes de modificar cualquier archivo global.

4. Reiniciá el agente al final (las skills y plugins se cargan al arrancar).

Nada se instala a escondidas: el agente hace backup de tu configuración, te muestra qué va a cambiar y espera tu OK.

## Qué trae

| Carpeta / archivo | Para qué |
|---|---|
| [`INSTALAR.md`](INSTALAR.md) | Instrucciones paso a paso **para el agente de IA** |
| [`docs/01-como-trabajo.md`](docs/01-como-trabajo.md) | La forma de trabajar: el flujo y los hábitos que hacen la diferencia |
| [`docs/02-skills.md`](docs/02-skills.md) | Skills recomendadas, de dónde salen y cómo instalarlas |
| [`docs/03-plugins.md`](docs/03-plugins.md) | Plugins de Claude Code (superpowers, diseño, seguridad, etc.) |
| [`docs/04-mcp.md`](docs/04-mcp.md) | MCPs útiles: docs al día, navegador, scraping |
| [`docs/05-ahorrar-tokens.md`](docs/05-ahorrar-tokens.md) | Cómo gastar menos cuota (clave en planes gratis o de prueba) |
| [`docs/06-memoria.md`](docs/06-memoria.md) | Sistema de memoria en archivos para no perder el hilo entre sesiones |
| [`docs/07-codex-antigravity.md`](docs/07-codex-antigravity.md) | Qué se porta a Codex / Antigravity y cómo |
| [`templates/`](templates) | `CLAUDE.md` global, fragmento de `settings.json` y plantillas de memoria |
| [`skills/`](skills) | Dos skills propias: `handoff` y `perfiles` |

## Qué NO trae

No copia skills ni plugins de terceros: los instala desde su repositorio original (cada uno con su licencia y autor). Tampoco incluye claves ni datos personales. Las herramientas pagas o con API key (por ejemplo Firecrawl) son opcionales y la clave la pones vos.

## Aviso

Es una configuración de uso personal compartida tal cual. Revisá lo que instala (cada skill es texto que le dice a tu IA qué hacer) antes de aceptar. Licencia MIT para lo escrito acá.
