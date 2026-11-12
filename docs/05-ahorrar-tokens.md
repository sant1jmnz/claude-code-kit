# 05 — Ahorrar tokens

En un plan gratis o de prueba, la cuota es lo que más limita. Estos hábitos suman mucho. Ordenados por impacto.

## 1. Sesiones cortas y enfocadas
- Una tarea = una sesión. Cuando un tema se cierra, `/handoff` y sesión nueva. Una conversación enorme se relee entera en cada mensaje.
- `/clear` entre temas que no se relacionan. `/compact` si debes seguir en la misma.
- Lo que importa va a archivos (ver `06-memoria.md`), no a la conversación.

## 2. Elegir bien el modelo y el esfuerzo
- **Haiku**: buscar, leer mucho material, resumir, clasificar. Barato y rápido.
- **Sonnet**: día a día (código, textos, diseño).
- **Opus**: solo problemas difíciles, arquitectura, depuración rebelde.
- Esfuerzo de razonamiento: *medio* por defecto; subirlo solo en tareas complejas. Preguntas simples no necesitan esfuerzo alto.

## 3. Subagentes con criterio
Un subagente lee mucho y devuelve un resumen corto: tu conversación no se llena. Úsalo para búsquedas largas y lectura masiva, **con modelo Haiku**. Los subagentes de modelos grandes (revisiones en paralelo, "ultra", exploraciones amplias) gastan mucho: úsalos solo si lo pides expresamente.

## 4. Leer menos
- `grep` / búsqueda antes de abrir un archivo; abrir solo el rango que hace falta.
- No releer un archivo recién editado para "verificar": la herramienta ya avisa si falló.
- Cuando el material es largo y necesario, que lo lea un subagente Haiku y devuelva lo relevante.

## 5. Salida de comandos filtrada: RTK
RTK ("Rust Token Killer") es un proxy que recorta la salida de comandos de terminal (git, ls, tests, builds) antes de que llegue al modelo. Ahorra gran parte de los tokens de lectura de terminal.

1. Instálalo desde las *releases* del repo `rtk-ai/rtk` en GitHub (o con `cargo install` si tienes Rust). **Ojo con el choque de nombre:** hay otro programa llamado `rtk` (Rust Type Kit). Comprueba con `rtk gain`: debe mostrar estadísticas de tokens; si da error, es el equivocado.
2. Activa el hook global: `rtk init -g` (otros agentes: `rtk init -g --agent antigravity`, etc.; mira `rtk init --help`).
3. A partir de ahí `git status` se reescribe solo a `rtk git status`. Mira lo ahorrado con `rtk gain`.

## 6. Respuestas cortas
- Estilo telegrama con la skill `caveman` (o la sección "Estilo de respuesta" de la plantilla de `CLAUDE.md`). Menos tokens de salida y se lee más rápido.
- `ponytail`: código más corto = menos tokens y menos errores.
- No pedir "explícamelo todo": pedir el resultado y preguntar el detalle si hace falta.

## 7. Menos herramientas cargadas
- Pocos MCPs, pocos plugins, pocas skills activas (skill `perfiles`).
- Conectores (Gmail, Drive…) apagados hasta que hagan falta.

## 8. Trabajo en paralelo y en segundo plano
- Llamadas independientes en el mismo turno (el agente puede hacer varias lecturas a la vez).
- Procesos largos (renders, descargas, scripts) en segundo plano, de una pasada, **sin "polling"** (no preguntar cada rato si terminó: el sistema avisa).
- Revisión visual: una sola hoja de contacto al final en vez de decenas de capturas.

## 9. Medir
`rtk gain` para la salida de terminal. En Claude Code, `/cost` o el panel de uso para ver dónde se va la cuota; ajusta el hábito que más pesa.
