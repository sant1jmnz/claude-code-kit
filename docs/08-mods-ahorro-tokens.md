# 08 — Mods de ahorro de tokens (solo Claude Code)

Los **mods** son plugins que enganchan la propia interfaz de Claude Code (paneles laterales, hooks sobre tu prompt, resultados de herramientas). Este pack, de **Ben AI**, recorta tokens de forma automática. Está publicado en GitHub; no se copia en este repo (no declara licencia): se instala desde su origen.

Fuente: <https://github.com/michaelzwiener/claude-mods> · directorio: <https://claudemods.si>

## Requisitos
- Claude Code **2.1.287+** en terminal (o 2.1.286+ en la app de escritorio) y las *function hooks* disponibles. Si `/mods` no aparece al terminar, tu versión no las tiene: actualiza, o salta esta fase.
- Windows: PowerShell 5.1 (ya viene). Opcionales: Poppler (para que `input-router` lea PDFs) y la CLI de Firecrawl (para `research-router`).

## Instalar

```
/plugin marketplace add michaelzwiener/claude-mods
/plugin install input-router@token-saving-mods
/plugin install effort-optimizer@token-saving-mods
/plugin install model-router@token-saving-mods
/plugin install handoff@token-saving-mods
/plugin install research-router@token-saving-mods
/plugin install efficient-browser-use@token-saving-mods
/plugin install mods@token-saving-mods
/plugin install savings-proof@token-saving-mods
/reload-plugins
```

Comprueba con `/mods` (panel con todos los mods; ahí se prende o apaga cada uno) y `/savings` (cuántos tokens ahorró cada uno).

## Qué hace cada uno

| Mod | Qué hace |
|---|---|
| `input-router` | Los archivos grandes y resultados de conectores los lee primero Haiku; Claude recibe notas cortas y la ruta al original. `/input-router full` deja pasar el siguiente completo |
| `effort-optimizer` | Lee cada prompt y propone el nivel de esfuerzo que necesita (o lo cambia solo en modo auto) |
| `model-router` | Antes de lanzar un subagente, Haiku decide si una tarea puede ir a un modelo más barato (solo con alta confianza). No toca el modelo del chat principal |
| `handoff` | A ~250k tokens ofrece "Refresh": resume el chat y sigue en uno nuevo |
| `research-router` | Mantiene la investigación web fuera del chat principal: un trabajador barato lee las páginas y devuelve un resumen con fuentes |
| `efficient-browser-use` | Achica cada captura de pantalla que toma Claude al manejar un navegador (o hace que Haiku la describa en texto) |
| `mods` | Panel para ver y activar/desactivar todos los mods |
| `savings-proof` | `/savings`: prueba de cuánto ahorró cada mod hoy y en este chat |
| `cache-clock` *(opcional)* | Cuenta regresiva hasta que se enfría la caché del chat |

También hay en el mismo repo `helper-desk` (barra de progreso de tareas y una tarjeta por subagente) y `chat-inventory` (qué usó este chat).

## Precauciones
- `input-router` y `research-router` resumen con Haiku: ahorran mucho, pero pueden perder detalle. Si necesitas el original completo, usa los comandos `full`.
- Son mods de terceros: revisa el código antes de instalar, como con cualquier plugin.
- `guia-skills` (de este repo, en `plugins/guia-skills`) también es un mod: `/plugin marketplace add sant1jmnz/claude-code-kit` y `/plugin install guia-skills@claude-code-kit`.
