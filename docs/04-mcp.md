# 04 — MCPs

Un MCP le da herramientas al agente (leer docs, controlar un navegador, scrapear). Cada MCP activo carga sus herramientas en el contexto: **instala pocos**.

## Set base (sin clave)

| MCP | Para qué |
|---|---|
| `context7` | Documentación **actual** de cualquier librería o framework, en vez de confiar en la memoria del modelo |
| `playwright` | Navegador automatizado: probar tu web, capturas, formularios, responsive |
| `chrome-devtools` | Consola, red, rendimiento y auditorías Lighthouse de una página |

### Claude Code

```bash
claude mcp add context7 -s user -- npx -y @upstash/context7-mcp
claude mcp add playwright -s user -- npx -y @playwright/mcp@latest
claude mcp add chrome-devtools -s user -- npx -y chrome-devtools-mcp@latest
claude mcp list
```

### Codex (`~/.codex/config.toml`)

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]
```

### Antigravity

Panel de MCP del agente → "Manage MCP servers" → agregar con el mismo `command` / `args`.

## Opcional: Firecrawl (búsqueda web y scraping)

Sirve para buscar en la web y leer páginas completas (útil para investigar). Tiene capa gratis; para más uso pide una API key en firecrawl.dev. **La clave la pones tú, en tu terminal; no se la pegues al agente:**

```bash
claude mcp add --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp --header "Authorization: Bearer TU_CLAVE"
```

## Revisar un MCP antes de instalarlo

Antes de aceptar uno nuevo: ¿de quién es el paquete? ¿qué comando ejecuta? ¿pide acceso a archivos, cuentas o red? Léelo como texto, no lo ejecutes "para ver". La skill `mcp-dependency-review` hace esta revisión estática. Fija versiones (`paquete@1.2.3`) cuando puedas, así una actualización maliciosa no te entra sola.

## Conectores (Gmail, Drive, etc.)

Mantenlos **apagados por defecto** y préndelos solo cuando una tarea los necesite: cada uno agrega muchas herramientas al contexto.
