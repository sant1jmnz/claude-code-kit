# guia-skills

Un "mod" de Claude Code (panel + hook sobre tu prompt) que resuelve el problema de tener muchas skills y no saber cuál usar.

- **`/guia`** abre un panel: tarea → skill → ejemplo de cómo pedirla. Las skills que no tienes instaladas salen en gris.
- **Mientras escribes**, si tu pedido coincide con una tarea ("armá el calendario de la semana", "make a carousel about…"), pregunta si usar la skill correspondiente. Funciona en español e inglés. Solo sugiere skills que tienes instaladas, y puedes elegir "No sugerir más en esta sesión".

## Instalar

```
/plugin marketplace add sant1jmnz/claude-code-kit
/plugin install guia-skills@claude-code-kit
/reload-plugins
```

Requiere una versión de Claude Code con mods (hooks de función, ver `docs/08-mods-ahorro-tokens.md`).

## Personalizar

Edita `hooks/register.tsx`:
- `GUIA`: las filas del panel.
- `REGLAS`: palabra clave → skill. Una regex por regla; la primera que coincide gana.
