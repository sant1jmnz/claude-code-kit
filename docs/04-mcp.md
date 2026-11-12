# 04 — MCP servers

An MCP server gives the agent tools (read docs, drive a browser, scrape). Every active MCP loads its tools into the context: **install few**.

## Base set (no key)

| MCP | What for |
|---|---|
| `context7` | **Current** documentation for any library or framework, instead of trusting the model's memory |
| `playwright` | Automated browser: test your site, screenshots, forms, responsive checks |
| `chrome-devtools` | Console, network, performance and Lighthouse audits of a page |

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

### Antigravity, Gemini CLI, Cursor, Windsurf, Cline

Add them through the agent's MCP panel or its MCP config file using the same `command` / `args` (`npx -y <package>`).

## Optional: Firecrawl (web search and scraping)

Useful for searching the web and reading full pages (great for research). It has a free tier; for more usage get an API key at firecrawl.dev. **You enter the key in your own terminal; don't paste it to the agent:**

```bash
claude mcp add --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp --header "Authorization: Bearer YOUR_KEY"
```

## Review an MCP before installing it

Before accepting a new one: who publishes the package? What command does it run? Does it ask for access to files, accounts or the network? Read it as text, don't run it "just to see". The `mcp-dependency-review` skill does this static review. Pin versions (`package@1.2.3`) when you can, so a malicious update can't slip in by itself.

## Connectors (Gmail, Drive, etc.)

Keep them **off by default** and turn them on only when a task needs them: each one adds many tools to the context.
