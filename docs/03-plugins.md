# 03 — Plugins (solo Claude Code)

Los plugins empaquetan skills, comandos, hooks y agentes. Se instalan desde un *marketplace* (un repo de GitHub). En Claude Code:

```
/plugin marketplace add <owner/repo>
/plugin install <plugin>@<marketplace>
```

Reinicia después de instalar. `/plugin` muestra el estado.

## Set base

| Plugin | Marketplace (repo) | Qué aporta |
|---|---|---|
| `superpowers` | `claude-plugins-official` (ya viene) | **El más importante.** Flujo completo: brainstorming → plan → ejecución → revisión → verificación, TDD, debugging sistemático, worktrees |
| `claude-security` | `claude-plugins-official` | Escaneo de seguridad del código y parches verificados |
| `frontend-design` | `claude-code-plugins` (`anthropics/claude-code`) | Diseño de interfaz con criterio propio, no genérico |
| `ui-ux-pro-max` | `ui-ux-pro-max-skill` (`nextlevelbuilder/ui-ux-pro-max-skill`) | Base de estilos, paletas, tipografías y guías UX para web y móvil |
| `ponytail` | `ponytail` (`DietrichGebert/ponytail`) | Modo "dev perezoso": el código más corto que resuelve el problema, sin sobre-ingeniería |

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

## Opcionales

| Plugin | Marketplace | Para qué |
|---|---|---|
| `ux-design`, `marketing-cro`, `sales-influence` | `wondelai-skills` (`wondelai/skills`) | Libros de diseño UX, conversión y ventas convertidos en skills (heurísticas, microinteracciones, persuasión) |
| `egm` | `egm` (`google/elephant-goldfish-model`) | Redactar un plan por escrito y revisarlo con revisores en paralelo **antes** de programar proyectos grandes |
| `claude-video-vision` | `claude-video-vision` (`jordanrendric/claude-video-vision`) | Que Claude "vea" videos (frames + audio). Necesita FFmpeg |

## Cuidado con la cuota

Cada plugin suma skills y agentes al listado inicial. En un plan gratis o de prueba, empieza con `superpowers` + `ponytail` + `frontend-design` y suma el resto cuando lo necesites. Los de revisión en paralelo (`egm`, revisiones "ultra") lanzan muchos subagentes: gastan mucho.
