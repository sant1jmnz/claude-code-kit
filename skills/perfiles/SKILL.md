---
name: perfiles
description: Activa o desactiva grupos de skills según el tipo de trabajo (frontend, marketing, video, código…) para no pasarse del presupuesto de contexto. Usar cuando la persona diga qué tipo de trabajo hará ("hoy toca frontend", "vamos con video"), pida ver/cambiar/crear perfiles, o pregunte por qué una skill no aparece o por qué el listado de skills está recortado. Solo Claude Code.
---

# Perfiles de skills

Claude Code carga la descripción de todas las skills al arrancar, con un presupuesto chico (~1% del contexto). Con muchas skills, las descripciones se recortan y el agente deja de elegirlas solo. Un perfil deja activas solo las skills del trabajo del momento.

## Catálogo

Archivo `~/.claude/skill-profiles.json` (si no existe, créalo con la estructura de abajo y pregunta a la persona qué grupos quiere según las skills que tenga en `~/.claude/skills/`).

```json
{
  "activo": "todo",
  "grupos": {
    "nucleo": ["handoff", "perfiles", "find-skills", "last30days", "humanizer"],
    "frontend": ["design-taste-frontend", "high-end-visual-design", "emil-design-eng", "apple-design"],
    "marketing": ["copywriting", "content-strategy", "social", "cold-email", "ads", "seo-audit"],
    "video": ["hyperframes", "hyperframes-cli", "media-use"]
  },
  "perfiles": {
    "codigo": { "desc": "Solo lo esencial", "grupos": ["nucleo"] },
    "frontend": { "desc": "Diseño de interfaz", "grupos": ["nucleo", "frontend"] },
    "publicidad": { "desc": "Marketing y contenido", "grupos": ["nucleo", "marketing"] },
    "video": { "desc": "Producción de video", "grupos": ["nucleo", "video"] },
    "todo": { "desc": "Todo activo", "grupos": ["nucleo", "frontend", "marketing", "video"] }
  }
}
```

## Aplicar un perfil

1. Lee `skill-profiles.json` y resuelve el conjunto activo (unión de los grupos del perfil).
2. En `~/.claude/settings.json`, escribe `skillOverrides` con `"off"` para **cada skill de `~/.claude/skills/` que no esté en el conjunto activo**, y sin entrada para las activas. No toques otras claves. Haz backup antes.
3. Actualiza `activo` en `skill-profiles.json`.
4. Avisa: **el cambio se ve al reiniciar la sesión.**

Haz siempre el merge del JSON completo con un script o archivo temporal; nunca interpoles nombres de skills dentro de un comando de shell.

## Reglas

- Solo skills de `~/.claude/skills/`. No toques las de plugins ni las integradas.
- Nunca borres archivos: un perfil solo escribe `skillOverrides`. Volver a `todo` las reactiva.
- Si el trabajo no encaja en un perfil, propón el más cercano y ofrece crear uno nuevo.
- Si piden activar una skill suelta que está apagada, quita su entrada de `skillOverrides` sin cambiar el resto.
- Limitación: el perfil es uno a la vez para toda la máquina.
