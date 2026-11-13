#!/usr/bin/env python3
"""Read-only update check for an AI-agent setup. Changes NOTHING.

Reports, in plain text:
  - agent CLI version (Claude Code) vs latest on npm
  - skills installed with the `skills` CLI whose source repo has newer commits
  - Claude Code plugins whose marketplace repo has newer commits
  - MCP servers pinned to an npm version that has a newer release
  - RTK version vs latest GitHub release

Stdlib only. Uses `gh` for GitHub if available (higher rate limit), else the public API.
Usage: python check-updates.py
"""
import json, os, shutil, subprocess, sys, urllib.request
from datetime import datetime, timezone

HOME = os.path.expanduser("~")


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=(os.name == "nt"))
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def http_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "update-check"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception:
        return None


def gh_json(path):
    if shutil.which("gh"):
        out = run(["gh", "api", path])
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
    return http_json("https://api.github.com/" + path)


def ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def load(path):
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


_commit_cache = {}


def latest_commit_date(repo):
    if repo not in _commit_cache:
        d = gh_json(f"repos/{repo}/commits?per_page=1")
        try:
            _commit_cache[repo] = ts(d[0]["commit"]["committer"]["date"])
        except Exception:
            _commit_cache[repo] = None
    return _commit_cache[repo]


def npm_latest(pkg):
    d = http_json("https://registry.npmjs.org/" + pkg.replace("/", "%2F") + "/latest")
    return d.get("version") if d else None


def newer(a, b):
    """True if version a is older than b (numeric compare, best effort)."""
    def parts(v):
        return [int(x) for x in v.lstrip("v").split("-")[0].split(".") if x.isdigit()]
    try:
        return parts(a) < parts(b)
    except Exception:
        return a != b


lines, updates = [], 0


def say(s=""):
    lines.append(s)


# 1. Agent CLI
say("== Agent CLI ==")
if shutil.which("claude"):
    cur = (run(["claude", "--version"]) or "").split(" ")[0]
    lat = npm_latest("@anthropic-ai/claude-code")
    if cur and lat and newer(cur, lat):
        say(f"UPDATE  Claude Code {cur} -> {lat}  (note: the desktop app updates itself)")
        updates += 1
    else:
        say(f"ok      Claude Code {cur or '?'} (latest {lat or '?'})")
else:
    say("skip    `claude` not found on PATH")

# 2. Skills (skills CLI lock file)
say("\n== Skills (skills CLI) ==")
lock = load("~/.agents/.skill-lock.json")
if lock and lock.get("skills"):
    by_src = {}
    for name, s in lock["skills"].items():
        if s.get("sourceType") == "github" and s.get("source"):
            by_src.setdefault(s["source"], []).append((name, ts(s.get("updatedAt") or s.get("installedAt") or "")))
    for src, items in sorted(by_src.items()):
        last_local = max((t for _, t in items if t), default=None)
        last_remote = latest_commit_date(src)
        ns = sorted(n for n, _ in items)
        names = ", ".join(ns[:5]) + (f" (+{len(ns) - 5} more)" if len(ns) > 5 else "")
        # ponytail: repo-level signal; newer commits may not touch your skills. Upgrade: compare tree hashes.
        if last_local and last_remote and last_remote > last_local:
            say(f"UPDATE? {src}: newer commits since {last_local.date()} (latest {last_remote.date()}) -> {names}")
            updates += 1
        elif not last_remote:
            say(f"skip    {src}: could not reach GitHub")
        else:
            say(f"ok      {src}")
else:
    say("skip    no ~/.agents/.skill-lock.json (no skills installed with the skills CLI)")

# 3. Claude Code plugins
say("\n== Claude Code plugins ==")
inst = load("~/.claude/plugins/installed_plugins.json")
mkts = load("~/.claude/plugins/known_marketplaces.json") or {}
local_only = []
if inst and inst.get("plugins"):
    for pid, entries in sorted(inst["plugins"].items()):
        mk = pid.split("@")[-1]
        src = (mkts.get(mk) or {}).get("source", {})
        if src.get("source") != "github":
            local_only.append(pid)
            continue
        local = max((ts(e.get("lastUpdated", "")) for e in entries if e.get("lastUpdated")), default=None)
        remote = latest_commit_date(src["repo"])
        if local and remote and remote > local:
            say(f"UPDATE? {pid}: marketplace {src['repo']} has newer commits (latest {remote.date()}, yours {local.date()})")
            updates += 1
        else:
            say(f"ok      {pid}")
    if local_only:
        say(f"skip    {len(local_only)} local/directory plugin(s) can't be checked: " + ", ".join(local_only))
else:
    say("skip    no plugins installed")

# 4. MCP servers pinned to npm versions
say("\n== MCP servers (npm) ==")
cfg = load("~/.claude.json") or {}
seen = False
for name, srv in (cfg.get("mcpServers") or {}).items():
    for a in srv.get("args", []) or []:
        if "@" in a.lstrip("@") and not a.startswith("-"):
            pkg, _, ver = a.rpartition("@")
            if pkg and ver[:1].isdigit():
                seen = True
                lat = npm_latest(pkg)
                if lat and newer(ver, lat):
                    say(f"UPDATE  {name}: {pkg} {ver} -> {lat}  (pinned in args)")
                    updates += 1
                else:
                    say(f"ok      {name}: {pkg} {ver}")
if not seen:
    say("skip    no version-pinned npm MCP servers found")

# 5. RTK
say("\n== RTK ==")
if shutil.which("rtk"):
    cur = (run(["rtk", "--version"]) or "").split(" ")[-1]
    rel = gh_json("repos/rtk-ai/rtk/releases/latest") or {}
    lat = (rel.get("tag_name") or "").lstrip("v")
    if cur and lat and newer(cur, lat):
        say(f"UPDATE  rtk {cur} -> {lat}")
        updates += 1
    else:
        say(f"ok      rtk {cur or '?'} (latest {lat or '?'})")
else:
    say("skip    rtk not installed")

say(f"\nSummary: {updates} possible update(s). Nothing was changed.")
print("\n".join(lines))
sys.exit(0)
