---
name: handoff
description: Resume la conversación actual en un archivo para que otra sesión (o agente) continúe el trabajo con poco contexto. Usar cuando la charla se alargó, se cerró un tema, o la persona dice "handoff", "pasemos a una sesión nueva" o "guardá el estado para seguir después".
argument-hint: "Para qué se usará la sesión siguiente"
disable-model-invocation: true
---

Escribe un documento de traspaso para que un agente nuevo continúe sin releer la conversación.

1. **Dónde guardarlo:** `seguimiento/handoffs/AAAA-MM-DD_<tema>.md` dentro de la carpeta de seguimiento del usuario (si no existe, pregunta la ruta una vez y créala). Si no hay carpeta de seguimiento, usa `./handoffs/` en el proyecto actual.
2. **Contenido (corto, sin relleno):**
   - Objetivo y estado actual en 3–5 líneas.
   - Decisiones tomadas y por qué.
   - Qué falta hacer, en orden.
   - Archivos y rutas clave (referenciarlos, no copiar su contenido).
   - Skills que el agente siguiente debería usar y el área/proyecto a leer del seguimiento.
   - Riesgos o cosas que no se pudieron verificar.
3. **No dupliques** lo que ya vive en otros archivos (seguimiento, planes, commits, diffs): enlázalo por ruta.
4. **Redacta datos sensibles:** nada de claves, contraseñas ni datos personales.
5. Si el usuario pasó argumentos, adapta el documento a lo que hará la sesión siguiente.
6. Al terminar, dile la línea exacta para pegar en la sesión nueva: `Leé <ruta> y seguí`.
