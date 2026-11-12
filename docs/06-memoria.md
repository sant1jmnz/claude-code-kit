# 06 — Memoria en archivos

El agente no recuerda nada entre sesiones por sí solo. La solución simple y portable: **una carpeta de Markdown** que el agente lee al empezar y actualiza en lotes. Funciona igual en Claude Code, Codex y Antigravity.

## Estructura

```
seguimiento/
├── SOBRE_MI.md               ← quién eres y cómo te gusta trabajar (se lee SIEMPRE)
├── SEGUIMIENTO.md            ← índice general: áreas y dónde está cada cosa
├── <area>/                   ← p. ej. trabajo/, estudio/, personal/
│   ├── SEGUIMIENTO.md        ← ÍNDICE corto del área: una línea por proyecto + estado
│   ├── REGLAS.md             ← reglas que valen solo en esta área
│   └── proyectos/
│       └── <proyecto>.md     ← el detalle (decisiones, pendientes, datos)
└── handoffs/                 ← resúmenes para continuar en una sesión nueva
```

Plantillas listas en [`../templates/memoria/`](../templates/memoria).

## Reglas de uso (van también en la plantilla de `CLAUDE.md`)

1. **Al empezar una tarea:** identificar el área, leer `SOBRE_MI.md`, el índice del área, sus `REGLAS.md` y **solo** el archivo del proyecto de la tarea. No leer todo.
2. **Índice corto, detalle aparte.** El índice solo apunta; así leer el contexto cuesta pocos tokens.
3. **Las reglas de un área no aplican a otra.** Ante la duda de área, preguntar.
4. **Guardado por lotes.** No editar el seguimiento a cada decisión (gasta tokens y frena el trabajo). Acumular decisiones, datos y reglas nuevas y escribirlas en **una** edición cuando: (a) hay ~5 cosas nuevas, (b) se cierra un tema importante, (c) la persona dice "guardá esto", o (d) la sesión está por terminar. Confirmar en una línea solo cuando se guarda.
5. **Reglas nuevas** van a `REGLAS.md` con fecha, en el mismo lote.
6. **Buscar lo viejo** con `grep`, o con un subagente Haiku que lea y devuelva un resumen corto. No cargar historiales enteros.
7. **Aprender a la persona.** Si el agente detecta una preferencia o límite nuevo y relevante, actualiza `SOBRE_MI.md` (la persona puede corregir o borrar lo que quiera).

## Memoria nativa de Claude Code

Claude Code además tiene memoria automática (`~/.claude/projects/<proyecto>/memory/`) para preferencias y hechos sueltos. Úsala para lo corto y de largo plazo; la carpeta `seguimiento/` es para el detalle de proyectos y áreas.

## Continuar en una sesión nueva: `/handoff`

La skill `handoff` (en [`../skills/handoff`](../skills/handoff)) escribe un resumen en `seguimiento/handoffs/` con: qué se hizo, qué quedó, qué skills usar y qué archivos leer. En la sesión nueva solo pegas: `Leé <ruta> y seguí`.

## Automatizar un resumen semanal (opcional)

Un script o tarea programada puede, una vez por semana, resumir las sesiones recientes a `seguimiento/`. Tiene que tolerar que la PC esté apagada (que corra al encender si se salteó). Opcional; no hace falta para empezar.
