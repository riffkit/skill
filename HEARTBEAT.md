# Riffkit Heartbeat

> **Version:** 1.0.2 (kept in sync with SKILL.md's frontmatter)

This file is the **version-check procedure**; it does **no throttling** — throttling is owned by SKILL.md's heartbeat entry section (once every 24 hours). All this does is compare the local SKILL.md `version` against the remote `/SKILL.json` `version` and re-download on mismatch.

**Base URL:** `https://riffkit.ai` (written below as `${BASE_URL}`)

## Environment variables used here

| Variable | Meaning | Suggested default |
|------|------|-----------|
| `BASE_URL` | Riffkit API root | `https://riffkit.ai` |
| `SKILLS_ROOT` | The AI agent's skills root (the one exported in install step 1) | project `.claude/skills` / global `~/.claude/skills` / Codex `.codex/skills`, etc. |
| `SKILL_DIR` | The riffkit skill's local directory (where `SKILL.md` / `HEARTBEAT.md` live) | `${SKILLS_ROOT}/Riffkit` |
| `AGENT_MEMORY_DIR` | The agent's own memory dir (holds `Riffkit-heartbeat-state.json`, separate from the skill dir) | Claude Code: `~/.claude/memory` / Codex: `~/.codex/workspace/memory` |

---

## Two trigger paths

| Path | Trigger | Throttling needed? |
|------|---------|-----------------|
| **Auto heartbeat** | The 24h throttle is due (decided by SKILL.md's entry section) | Already done by SKILL.md's entry section; throttling has passed by the time you're here |
| **Manual trigger** | The user says something like "check Riffkit for updates" | No throttle check — **run unconditionally** |

Either way, **run the version compare below directly** when you get here.

---

## Version compare

```bash
# Remote version (via the /SKILL.json endpoint; timestamp the URL to dodge caches)
REMOTE_VERSION=$(curl -s "${BASE_URL}/SKILL.json?t=$(date +%s)" \
  | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>process.stdout.write(JSON.parse(s).version))')

# Local version (extracted from SKILL.md's frontmatter)
LOCAL_VERSION=$(grep -m1 '^version:' "${SKILL_DIR}/SKILL.md" \
  | sed -E 's/^version:[[:space:]]*["'\'']?([^"'\''[:space:]]+).*/\1/')
```

> **No `node`?** Use `python3`:
> ```bash
> REMOTE_VERSION=$(curl -s "${BASE_URL}/SKILL.json?t=$(date +%s)" | python3 -c 'import json,sys;print(json.load(sys.stdin)["version"])')
> ```

**Comparison rule:** a plain **string equality** check (Riffkit version numbers are always minted by the server; the local copy is never newer than remote).

- `REMOTE_VERSION === LOCAL_VERSION` → already up to date; tell the user the current version and finish
- `REMOTE_VERSION !== LOCAL_VERSION` (including either side being empty) → re-download SKILL.md per below
- `REMOTE_VERSION` empty (`/SKILL.json` errored, network failure) → skip this update, tell the user the failure honestly, don't retry; on the **manual** path, suggest trying again later

## Re-download SKILL.md

```bash
curl -s "${BASE_URL}/SKILL.md?t=$(date +%s)" > "${SKILL_DIR}/SKILL.md"
```

After downloading, tell the user the new `frontmatter.version` (SKILL.md keeps no changelog, so just report the version):

```
riffkit skill upgraded from <old> to <new> — now using the latest definition.
```

---

## Wrap-up: write the state file

**Auto-heartbeat path:** SKILL.md's entry section already updated `lastHeartbeatCheck` before branching here, so **this file writes nothing.**

**Manual path:** when the user triggers manually, set `lastHeartbeatCheck` to the current Unix second to prevent the heartbeat from firing again moments later:

```bash
STATE="${AGENT_MEMORY_DIR}/Riffkit-heartbeat-state.json"
mkdir -p "$(dirname "$STATE")"
NOW=$(date +%s)
# Read current state, update lastHeartbeatCheck, write the whole thing back
[ -f "$STATE" ] || printf '{}' > "$STATE"
node -e '
  const fs = require("fs");
  const path = process.argv[1];
  const now = parseInt(process.argv[2], 10);
  const state = (() => { try { return JSON.parse(fs.readFileSync(path, "utf8")); } catch { return {}; } })();
  state.lastHeartbeatCheck = now;
  fs.writeFileSync(path, JSON.stringify(state, null, 2));
' "$STATE" "$NOW"
```

(Environments without `node` can use `jq` or `python3` instead.)

---

## Error handling

| Error | Handling |
|------|----------|
| `/SKILL.json` non-200 / timeout | Tell the user remote is temporarily unreachable; on the **auto** path skip and still update `lastHeartbeatCheck` (so the next heartbeat doesn't immediately hammer remote); on the **manual** path report the cause honestly, no auto-retry |
| Local `SKILL.md` missing | Reinstall per SKILL.md's "Installation" section (the `curl -o` line), then update `lastHeartbeatCheck` as appropriate |
| JSON parse failure (remote/local) | Skip this round, do NOT update `lastHeartbeatCheck` (leave it for the next heartbeat) |
| SKILL.md download failure (disk full, permissions) | Tell the user the cause, keep the old SKILL.md, **do not** update `lastHeartbeatCheck` |

On error, don't retry in a loop — **log and move on.**

---

## Response format

> **Language:** the examples below are in English, but the actual response should **follow the user's current input language** (translate to Chinese for a Chinese conversation, consistent with SKILL.md's "Language" section). Identifiers like the version number and `HEARTBEAT_OK` are not translated.

**Up to date:**
```
HEARTBEAT_OK - Riffkit is already up to date (1.0.2)
```

**Upgraded:**
```
riffkit skill upgraded from <old> to <new> — now using the latest definition.
```

**Needs user attention:**
```
riffkit skill version check failed: <reason>. Please confirm ${SKILL_DIR}/SKILL.md exists and is readable, or reinstall.
```
