## Installation

The riffkit skill is a **general AI-agent skill** — usable by any agent with "local skill loading + heartbeat scheduling" (Claude Code / Codex / others). Use placeholder paths, substituting your agent's directory convention.

**The Riffkit CLI** (install and sign-in: **Start here**, at the top of SKILL.md) takes each route's parameters and prints the JSON the route answers, in English and without the response headers; sign-out is `riffkit logout`. An option value that starts with `@` is read from that file: send text from the user or anyone else that starts with `@` (a handle, a caption) as `@@…`. Without `--yes`, a command that spends credits asks y/N at a terminal and otherwise refuses with exit code 3, sending nothing. `riffkit wait <batch_id>` follows a batch for up to 9 minutes: exit code 10 means it is still running (run it again), 11 that it finished but a task made no video (read that task's `error` and `result`). When `riffkit` adds a line that a newer version is out, update it with `npm i -g @riffkit/cli@latest` (its commands themselves stay current without an update).

### Step 1: install the skill files

```bash
# ${SKILLS_ROOT} = your AI agent's skills root, commonly:
#   Claude Code project .claude/skills / global ~/.claude/skills
#   Codex project .codex/skills / global ~/.codex/skills
export SKILLS_ROOT=<one of the paths above>
mkdir -p "${SKILLS_ROOT}/Riffkit/references" && cd "${SKILLS_ROOT}/Riffkit"

curl -sL "https://riffkit.ai/SKILL.md"     -o SKILL.md
curl -sL "https://riffkit.ai/HEARTBEAT.md" -o HEARTBEAT.md
for n in details anchor api intents errors install; do
  curl -sL "https://riffkit.ai/skill/$n.md" -o "references/$n.md"
done
```

Filenames are case-sensitive: `SKILL.md` (the skill's core), `HEARTBEAT.md` (version-check heartbeat) and `references/` (the files SKILL.md's index names, this one among them).

> **One-off quick use (no local install):** send the agent `Run curl -fsSL https://riffkit.ai/SKILL.md in your terminal and follow the instructions to join Riffkit`; it runs the device flow (hands you a one-click approval link) to sign in — no token to copy. For long-term use, install locally + set up the heartbeat.

### Step 2: install self-check

Check each item in order; on any failure, return to the previous step and reinstall:

1. **Files present** — `ls "${SKILLS_ROOT}/Riffkit/"` includes `SKILL.md`, `HEARTBEAT.md` and `references/`, exact case, and `references/` holds the six files of the index.
2. **Version matches** — SKILL.md's frontmatter `version` equals `curl -s https://riffkit.ai/SKILL.json | jq -r .version`.
3. **Network reachable** — `curl -sS -o /dev/null -w "%{http_code}" https://riffkit.ai/api/auth/me` returns `401` (no cookie is normal).
4. **Auth reachable** — the one-click sign-in is live: `curl -s -X POST https://riffkit.ai/api/skill/device/authorize` returns JSON with a `user_code`.

> After self-check passes, continue to [Heartbeat setup](#heartbeat-setup) — the agent's path for auto-syncing skill updates.

---

## Heartbeat setup

The riffkit skill keeps evolving — folding it into your agent's periodic heartbeat is the robust way to auto-sync updates, or the local SKILL.md drifts out of date.

**Frequency: once every 24 hours.**

### Add to the heartbeat checklist

````markdown
## Riffkit (every 24h)

> ⚠️ **Never compute Unix seconds, convert to UTC, or do the subtraction yourself.** The bash below does all the time math; just read the first stdout line's tag to branch.

1. Run the check:

   ```bash
   STATE="${AGENT_MEMORY_DIR}/Riffkit-heartbeat-state.json"
   mkdir -p "$(dirname "$STATE")"
   [ -f "$STATE" ] || printf '{"lastHeartbeatCheck":null}' > "$STATE"
   NOW=$(date +%s)
   LAST=$(grep -o '"lastHeartbeatCheck"[^,}]*' "$STATE" | grep -oE '[0-9]+' || echo 0)
   DIFF=$(( NOW - LAST ))
   INTERVAL=$(( 24 * 60 * 60 ))
   if [ "$DIFF" -ge "$INTERVAL" ]; then
     echo "HBCHECK=DUE now=$NOW last=$LAST diff=${DIFF}s interval=${INTERVAL}s"
   else
     echo "HBCHECK=SKIP now=$NOW last=$LAST diff=${DIFF}s wait=$(( INTERVAL - DIFF ))s"
   fi
   ```

2. **Branch strictly on the first stdout line's tag:**
   - `HBCHECK=SKIP …` → **end the heartbeat, reply `HEARTBEAT_OK`**, do nothing else
   - `HBCHECK=DUE …`  → continue to step 3

3. Update the state file's `lastHeartbeatCheck` to the number after `now=` from the previous stdout (copy it; don't re-run `date`), and write the whole state back to `${AGENT_MEMORY_DIR}/Riffkit-heartbeat-state.json`.

4. Read the local `HEARTBEAT.md` and run the version check per its instructions.
````

> **Env conventions:**
> - `${SKILLS_ROOT}` = your AI agent's skills root (the one exported in install step 1)
> - `${SKILL_DIR}` = `${SKILLS_ROOT}/Riffkit` (where `SKILL.md` / `HEARTBEAT.md` live)
> - `${AGENT_MEMORY_DIR}` = your agent's runtime memory dir (holds `Riffkit-heartbeat-state.json`). Usually `~/.claude/memory` for Claude Code, `~/.codex/workspace/memory` for Codex.
>
> **The heartbeat only checks the version — no write requests.** It never submits tasks or tops up credits for you.

### Manual version check

| Intent | Example | Action |
|---------|------|--------------|
| Check now | "check Riffkit for updates", "update the skill" | **Skip throttling**, read `HEARTBEAT.md` and run the version compare |
| Force re-download | "force-update Riffkit", "reinstall the skill" | `curl`-overwrite the local SKILL.md and `references/` directly (the commands in install step 1), no version compare |

After a manual trigger, also set `lastHeartbeatCheck` to the current Unix second (so the heartbeat doesn't fire again minutes later), using the same "never compute time by hand" script to read `NOW` and write it.
