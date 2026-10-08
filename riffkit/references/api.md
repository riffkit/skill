## API reference

### Commands and routes

Each step of **The flow** names a `riffkit` command; each command is one route. Without the CLI, call the route (full parameters below); with it, `riffkit help <command>` shows the same.

| Command | Route | What it does |
|---|---|---|
| `riffkit get_options` | `GET /api/settings` | What this account can use: engines and resolutions (locked or not), default pairs, limits, `credit_cover`, `staged_delivery` |
| `riffkit list_templates` | `GET /api/formulas` | Analyzed templates (a source) |
| `riffkit get_template` | `GET /api/formulas/{formula_id}` | One template's `extraction_summary` |
| `riffkit create_upload_link` | `POST /api/riffs/uploads` | A link where the user adds a video from their phone or computer |
| `riffkit get_upload` | `GET /api/riffs/uploads/{upload_id}` | Has that video arrived (`ready` → its `upload_id` is a source) |
| `riffkit list_characters` | `GET /api/characters` | Digital characters |
| `riffkit list_products` | `GET /api/products` | Products |
| `riffkit create_product` | `POST /api/products` | Create a product |
| `riffkit add_product_image` | `POST /api/products/{product_id}/images` | Add a product image |
| `riffkit list_languages` | `GET /api/languages` | Video language codes |
| `riffkit quote_remake` | `GET /api/riffs/quote` | The price of an adapt or swap riff, from any source |
| `riffkit quote_swap` | `GET /api/riffs/swap-quote` | The price of one swap video from a template |
| `riffkit quote_create` | `GET /api/creation/quote` | The price of a creation video |
| `riffkit remake_video` | `POST /api/riffs` | **Submit an adapt or swap riff** (spends credits) |
| `riffkit remake_video_batch` | `POST /api/pipeline/batch` | Analyzed-template batch, the advanced form of `riffkit remake_video` (spends credits) |
| `riffkit create_video` | `POST /api/creation/batch` | **Submit a creation video** (spends credits) |
| `riffkit get_batch` | `GET /api/tasks/batch/{batch_id}` | A batch's tasks and progress |
| `riffkit get_task` | `GET /api/tasks/{task_id}` | One task |
| `riffkit list_tasks` | `GET /api/tasks` | List tasks |
| `riffkit count_tasks` | `GET /api/tasks/stats` | Task counts |
| `riffkit get_task_content` | `GET /api/tasks/{task_id}/content` | What the engine extracted and rewrote (optional) |
| `riffkit cancel_task` | `POST /api/tasks/{task_id}/cancel` | Stop a task (what rendered stays charged) |
| `riffkit retry_task` | `POST /api/tasks/{task_id}/retry` | Retry a failed task (can spend credits) |
| `riffkit list_videos` | `GET /api/assets` | Finished videos, with caption and hashtags |
| `riffkit get_video_link` | `GET /api/assets/{asset_id}/link` | A link that opens a finished video without signing in (6 hours) |
| `riffkit continue_video` | `POST /api/assets/{asset_id}/continue` | The next section, the rest or a redo of a video made in sections (spends credits) |
| `riffkit quote_ratios` | `GET /api/pipeline/backfill/occupied` | The ratios a video already has, and the price of one more |
| `riffkit add_ratios` | `POST /api/pipeline/backfill` | Add vertical ratios to finished videos (spends credits) |
| `riffkit get_subtitles` | `GET /api/assets/{asset_id}/subtitles` | A video's burned-in subtitle lines |
| `riffkit save_subtitles` | `PUT /api/assets/{asset_id}/subtitles` | Save subtitle edits |
| `riffkit preview_subtitles` | `POST /api/assets/{asset_id}/subtitles/preview` | A free preview of the edited subtitles |
| `riffkit burn_subtitles` | `POST /api/assets/{asset_id}/subtitles/burn` | Render the edits into a new version of the video |
| `riffkit reset_subtitles` | `DELETE /api/assets/{asset_id}/subtitles/edits` | Undo the edits |
| `riffkit reconcile_subtitles` | `POST /api/assets/{asset_id}/subtitles/reconcile` | Rebuild a video's subtitle lines |
| `riffkit analyze_template` | `POST /api/formulas/analyze` | Subscribers only: analyze a new source into a template, without making a video |
| `riffkit refresh_template` | `POST /api/formulas/{formula_id}/refresh-analysis` | Re-analyze one of your own templates |
| `riffkit update_template` | `PATCH /api/formulas/{formula_id}` | Rename one of your own templates or change its hint |
| `riffkit set_voice_sample` | `POST /api/characters/{character_id}/voice-sample` | Set a character's voice sample |
| `riffkit clear_voice_sample` | `DELETE /api/characters/{character_id}/voice-sample` | Remove a character's voice sample |
| `riffkit upload_reference` | `POST /api/assets/upload` | Upload a reference file (not used by the main flow) |
| `riffkit get_credits` | `GET /api/usage/credits` | The balance, today's spend and the daily limit |
| `riffkit get_daily_budget` | `GET /api/usage/daily-budget` | Today's spend against the daily limit |
| `riffkit get_usage_summary` | `GET /api/usage/summary` | Spend summary |
| `riffkit get_usage_history` | `GET /api/usage/history` | Spend history |
| `riffkit get_plan` | `GET /api/billing/subscription` | The current plan's name and the per-second rates (read-only) |
| `riffkit list_members` | `GET /api/scopes/{scope_id}/members` | Team members (team scopes) |
| `riffkit get_account` | `GET /api/auth/me` | Who is signed in |
| `riffkit sign_out` | `POST /api/auth/logout` | End this session |
| `riffkit device_authorize` | `POST /api/skill/device/authorize` | Start the one-click sign-in (Auth) |
| `riffkit device_token` | `POST /api/skill/device/token` | Poll that sign-in for the session (Auth) |
| `riffkit list_plans` | `GET /api/billing/plans` | The plan catalog |
| `riffkit cancel_plan` | `POST /api/billing/cancel` | End the plan at the period's end |
| `riffkit resume_plan` | `POST /api/billing/resume` | Keep a plan that was set to end |

The CLI's own commands: `riffkit login` and `riffkit logout` (the sign-in below, and sign-out), `riffkit wait <batch_id>` (follow a batch), `riffkit download <asset_id>` (save a video's file), `riffkit help`.

### Service config

```
BASE_URL = https://riffkit.ai
Content-Type: application/json; charset=utf-8  (except multipart endpoints)
Auth: cookie-based session (vee_session)
```

Every path below already includes the full prefix — just append it to `${BASE_URL}` (e.g. `GET /api/auth/me` → `https://riffkit.ai/api/auth/me`).

⚠️ **Request bodies must be UTF-8.** Python `requests.post(url, json=...)`, Node `fetch`/`axios`, Go `json.Marshal` are UTF-8 by default — pure-ASCII needs nothing. **Only** on Chinese Windows `cmd` run `chcp 65001` first (PowerShell also needs `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`), or non-ASCII characters get sent as GBK and rejected with `BAD_REQUEST`. Never assemble a byte string with `data=` in any language.

### Auth

The API uses a cookie-based session (`vee_session`). **Never ask for a password in chat.** The agent obtains a session through a **one-click device-authorization flow** — the user just opens a link and clicks Approve, and the session flows back automatically. **No token is ever pasted into chat.** (Same UX as `gh auth login`.)

**With the Riffkit CLI (see Start here), skip the curl steps below:** `riffkit login` runs this same device flow and saves the session to the same file, `~/.riffkit/session`, so a sign-in with either one serves both. Without the CLI, run the start and the polling below in one shell script, keeping `device_code` in a variable: never print it or write it into a command you show.

1. Check: if you saved a session earlier (see step 3), `GET /api/auth/me` with it → 200 logged in / 401 not.
2. If not logged in (401), run the device flow:
   - **a. Start** — `POST /api/skill/device/authorize` (no body, no auth needed) → `{device_code, user_code, verification_uri, verification_uri_complete, expires_in, interval}`.
   - **b. Show the user the link + code** (do NOT ask for anything back):
     ```
     Open this and click Approve — I'll connect automatically:
     <verification_uri_complete>
     (confirm the page shows this code before approving: <user_code>)
     ```
   - **c. Poll** — `POST /api/skill/device/token` with `{"device_code": "<device_code>"}` every `interval` seconds (default 5s):
     - `{"status":"authorization_pending"}` → keep polling
     - `{"status":"approved","token":"<t>"}` → **done**; use `Cookie: vee_session=<t>` on every later request
     - `{"status":"expired"|"denied"|"invalid"|"consumed"}` (sent with **HTTP 400**: read the JSON body anyway) → stop and start over with a fresh `authorize`
     - HTTP **429** (you polled faster than `interval`) → the body has no `status`; this is not a dead flow: wait `interval` seconds and poll again
     - stop after `expires_in` (10 min) and tell the user the link expired
3. **Keep the token for the whole session.** Each shell command runs in a new process, so a token held in a shell variable is gone after that one command, and the next call would need a new sign-in. Right after `approved`, save it to a private file and read it back in every later command:
   ```bash
   mkdir -p ~/.riffkit && (umask 077 && printf '%s' "$TOKEN" > ~/.riffkit/session)
   curl -sS -b "vee_session=$(cat ~/.riffkit/session)" "https://riffkit.ai/api/auth/me"
   ```
   Reuse it until a request returns 401, then delete the file and run the device flow again. Never print it. In zsh, don't name a polling variable `status`: it is read-only there and breaks the loop.
4. Add `Cookie: vee_session=<value>` to every subsequent request.
5. To sign out (the user asks to disconnect this agent, or to switch accounts): `POST /api/auth/logout` with the cookie ends that session (→ `{"ok": true}`); then delete `~/.riffkit/session`.

> The device flow is the only sign-in path — the token never gets pasted into chat. (Settings → **AI agent mode** shows the same one-click steps.)

#### `GET /api/auth/me`

**200 → `UserOut`** / **401 → unauthenticated.**

| Field | Type | Notes |
|------|------|------|
| `id` | string | User ID |
| `email` | string | Email (= identity; no separate name) |
| `role` | string | Scope role: `owner` / `admin` / `member` |
| `is_active` | boolean | Active |
| `is_staff` | boolean | Product-level staff (default false) |
| `scope_id` | string? | Owning scope |
| `daily_credits_limit` | float | The account's own daily cap. A team member can have a per-member cap that applies instead, so always read the cap in force from `daily_limit` on `GET /api/usage/credits` (raw internal credits, ÷100 for display; `0` = unlimited) |
| `created_at` / `last_login_at` | datetime | Created / last login |

#### `POST /api/skill/device/authorize` — start one-click sign-in

No auth, and no body required. `client` (optional, `^[a-z0-9][a-z0-9-]{0,63}$`) — labels which skill started the sign-in; echoed as `skill` in `verification_uri_complete`; invalid values are ignored. **Response:**

| Field | Type | Notes |
|------|------|------|
| `device_code` | string | **Secret** — the agent polls with it; never show it to the user, never write it anywhere |
| `user_code` | string | Short code shown to the user (they confirm it matches the approval page) |
| `verification_uri` | string | Approval page (bare) |
| `verification_uri_complete` | string | Approval page with the code pre-filled — **give the user this link** |
| `expires_in` | int | Seconds until the flow expires (600) |
| `interval` | int | Seconds to wait between polls (5) |

#### `POST /api/skill/device/token` — poll for the session

**Body:** `{"device_code": "<device_code>"}`. **Response `{status, ...}`** (HTTP 200 for `authorization_pending` and `approved`, HTTP 400 for the dead-flow statuses: read the body on a 400, and don't let an error-raising client such as `curl -f` or `raise_for_status()` stop before you see `status`):

| `status` | Meaning | Action |
|------|------|------|
| `authorization_pending` | User hasn't approved yet | Wait `interval` seconds, poll again |
| `approved` | Approved — response also has `token` | Use `Cookie: vee_session=<token>`; stop polling |
| `expired` / `denied` / `invalid` / `consumed` | Flow is dead | Stop; start over with a fresh `authorize` |

> Polling faster than `interval` (more than 2 polls per 5 s for one `device_code`, or more than 120 a minute from one IP) → **429** with `{"detail": …}` and no `status`. Treat it as "keep waiting": sleep `interval` and poll again. Never start a new `authorize` because of a 429.

> The minted `token` is a normal session (identical to a browser login). Treat it like a credential: never echo it, never store it in a task/caption/product field.

---

### Video generation

#### `POST /api/riffs` — one-shot riff (preferred entry)

**Content-Type:** `multipart/form-data`

> **Non-ASCII text: write it to a UTF-8 file, don't inline it in the shell.**
> For `content_anchor` and `user_hint`, pass the value by file reference:
>
> ```
> printf '%s' "$BRIEF" > /tmp/anchor.txt      # or your language's write-file call
> curl … -F "content_anchor=<'/tmp/anchor.txt'"
> ```
>
> (`-F "name=<file"` reads the field VALUE from the file. That is not `@file`,
> which would attach it as an upload.)
>
> Why: when a brief is typed straight into a `curl -F "content_anchor=主题：…"`
> command, the bytes that reach the wire are whatever the shell's codepage
> produced. On a non-UTF-8 console — the Windows default in CJK locales — those
> are GBK/Big5/Shift-JIS bytes, and the field is stored as mojibake
> (`主题：一条…` → `Ö÷Ìâ£ºÒ»Ìõ…`). This happened on prod: six riffs rendered
> from garbage briefs and were billed normally. The server now rejects it with
> **400** instead, but the 400 is a backstop — you cannot see the corruption
> from inside the agent, because the text you wrote was correct and it was
> mangled a layer below you. Writing the file avoids the shell layer entirely.
>
> **If you do get that 400:** do NOT resend the same command; it will fail
> identically. Switch to the file form above. Already using it? Then the file
> itself isn't UTF-8 — rewrite it with an explicit UTF-8 encoding.

**Source (exactly one):**

| Param | Type | Notes |
|------|------|------|
| `video` | File | Upload source video (≤100MB, and ≤ the render-duration cap — default 45s; see General constraints) |
| `tiktok_url` | string | TikTok link (server downloads + extracts BGM). Must point at **one specific video** — `…/@user/video/<id>` (query params fine) or a `vm.`/`vt.`/`tiktok.com/t/` share short link. A profile-page link (`tiktok.com/@handle`, no `/video/`) is rejected with an instant 400, and so is a video longer than the render-duration cap when the link's metadata gives its length before anything downloads (otherwise the analyze task fails with the same message after the download; nothing is billed) |
| `formula_id` | string | Analyzed template ID (yours or a public one; status must be `analyzed` and its analysis current, `analysis_prompt_is_latest=true`, else 400) |
| `upload_id` | string | A video the user added through an upload link (`POST /api/riffs/uploads`), once `GET /api/riffs/uploads/{upload_id}` reads `ready`: for a file you cannot send yourself (it is on the user's phone). It is analyzed like an uploaded `video` (`analyze_then_generate`). One upload makes one submit: after it, 409 `upload_used` with that submit's `formula_id` / `batch_id` (send that `formula_id` for another video from it, once that template reads `analyzed` in `GET /api/formulas/{formula_id}`: its analysis is the first submit's analyze task); 409 while the video has not arrived or another submit of it is running; 410 once it is gone; 404 not this account's |

**Mode:**

| Param | Type | Default | Notes |
|------|------|------|------|
| `mode` | string | `adapt` | `adapt` (keep the formula, new story; everything below behaves as documented) or `swap` (keep the source's shots, swap in your character; see The flow, step 0). Other values → 400. `adapt` is only the API's default when the param is omitted: the mode is the user's choice (The flow, step 0), so always send the one they chose |

**Optional creative config** (in swap mode `character_ids` is optional but at least one of character / product with images / `content_anchor` is required, and `language` / `product_visibility` / `bgm_mode` / `video_ratios` are accepted but ignored):

| Param | Type | Default | Notes |
|------|------|------|------|
| `character_ids` | string | `""` | JSON array string (`'["caden","chloe"]'`) or comma-separated (`caden,chloe`). **Empty = Auto mode** (no digital human, SD2 generates the person); non-empty = one task per character. **Note it's a string, not an array** (multipart limitation) |
| `product_id` | string | `""` | Empty = no product placement (`no_product` mode) |
| `product_visibility` | string | `on_camera` | `on_camera` / `off_camera`; only effective when `product_id` is non-empty (ignored when empty) |
| `language` | string | `en` | Must be a code from `GET /api/languages` (currently `en` / `es` / `pt` / `id` / `de` / `fr` / `it` / `ja` / `zh-CN`); an invalid value returns 400 |
| `video_backend` | string | tier-dependent | `seedance` (Seedance 2.0) / `seedance25` (Seedance 2.5, premium) / `seedance_fast` (Seedance 2.0 Fast) / `minimax` (MiniMax H3). Picks the render engine. Default for a **free-tier account** (no purchase or subscription on the wallet yet): **`seedance_fast` `480p` in both modes** (also the cheapest free swap; where Fast isn't offered, `seedance` `480p`); **`seedance` `720p` in adapt mode and `seedance25` `720p` in swap mode for a paid one** (the recommended swap engine; `seedance` `720p` where 2.5 isn't offered) — so **omit this param unless the user has a plan**. A free-tier wallet may render on `seedance_fast` `480p` or `seedance` `480p` (480p only); a free-tier caller that names `seedance` / `seedance_fast` without `resolution` gets `480p`. Any other (engine, resolution) pair from a free-tier caller gets **403 `subscription_required`**, the same payload as the analyze paywall (see `POST /api/formulas/analyze`): relay `message`, hand over `subscribe_url` verbatim, do not retry. Resubmit without `video_backend` / `resolution` (the free default for that mode) if the user just wants the video. The pair each form defaults to for THIS account is `GET /api/settings` → `default_video_pairs` (`adapt` / `creation` / `swap` → `{backend, resolution}`). **Resolution is engine-scoped** — see `resolution` below. An engine the deployment has no key for → 400 `video_backend_unavailable`; unknown value → 400. `GET /api/settings` → `video_backends` lists engines in display order (MiniMax H3 → Seedance 2.0 Fast → Seedance 2.0 → Seedance 2.5), which is **not** a default order: never take the first entry as the default |
| `resolution` | string | engine base | Engine-scoped: `720p` / `480p` / `1080p` for `seedance`, `720p` / `480p` for `seedance25` and `seedance_fast` (no 1080p on either), `768P` / `2K` for `minimax`. `480p` is draft quality at a lower rate. **Omit it** and you get that engine's base tier (a free-tier account gets that engine's free tier: `480p` on `seedance` / `seedance_fast`); a value the picked engine doesn't sell is a 400. Billing is per second at the (engine, tier) display rate: seedance 480p 50 credits/s · 720p 100/s · 1080p 250/s · seedance25 480p 75/s · 720p 150/s · seedance_fast 480p 40/s · 720p 80/s · H3 768P 40/s · H3 2K 80/s. Live rates: `GET /api/billing/subscription` → `video_credits_per_second_map`; the engines a deployment offers and each one's tiers: `GET /api/settings` → `video_backends` — each entry carries `name`, `resolutions`, `locked: true` when THIS account may use none of its tiers, and `locked_resolutions` (tiers this account may not use; free tier: everything except Seedance 2.0 Fast 480p and Seedance 2.0 480p). Offer only unlocked pairs instead of discovering the 403 |
| `content_anchor` | string | `""` | Creative direction (≤5000 chars); to place a product image on camera, write that image's `name` in the text (on_camera; plain name match) |
| `user_hint` | string | `""` | Hook hint (≤5000); **new source only** — ignored when `formula_id` is given |
| `bgm_mode` | string | `""` | Empty = automatic (the template's original BGM if it has one that isn't `disabled`, else AI-generated music). `source` / `source_ref` / `sd2`, only used with an analyzed template (see Behavior notes); any other value → 400 |
| `video_ratios` | string | `'["9:16"]'` | JSON-array string of delivery aspect ratios. **Vertical group `9:16` / `3:4` / `1:1` / `4:5` can be multi-selected** (one master render fans out into a reframed video per ratio, each metered as its own video at that engine's **reframe** rate: Seedance 2.0 480p 60/s · 720p 120/s · 1080p 300/s · Seedance 2.5 480p 90/s · 720p 180/s · Seedance 2.0 Fast 480p 50/s · 720p 100/s · MiniMax H3 768P 80/s · 2K 160/s; see Billing); a **horizontal ratio `16:9` / `4:3` / `21:9` must be requested alone** (list length 1). Duplicates are dropped and the list is put in a fixed order (9:16 → 3:4 → 1:1 → 4:5): the first ratio in that order is the master render, and each other ratio is reframed from it once it finishes, joining the same `batch_id`. The response doesn't list the ratios back: read each task's `ratio` from `GET /api/tasks/batch/{batch_id}`. Invalid ratio / horizontal-mixed → 400 |
| `delivery` | string | `whole` | `whole` = the whole video in one go; `sections` = one section at a time: the first now, the rest later on the same script with `POST /api/assets/{asset_id}/continue`. Send `sections` only when the user asks for it. A free-tier account always gets `sections`, sent or not (`GET /api/settings` → `staged_delivery.forced`), and is held to the first section: it can make that section again (`redo`), never the rest; a video shorter than 8 seconds is one section, so it is always made whole. Any other value → 400 |

**Response (`RiffOut`):**

| Field | Type | Notes |
|------|------|------|
| `mode` | string | `"generate"` (an analyzed template → the generation batch is submitted now; this includes a TikTok link that already has a current analyzed template in your scope or a public one, which is reused: `formula_id` is that template and `analyze_task_id` is null) / `"analyze_then_generate"` (an upload, or a TikTok link with no current analyzed template → analysis is submitted first; on completion the worker chains the generation) |
| `batch_id` | string | **The riff's handle** — the analyze task and chained generation task share it; poll `GET /api/tasks/batch/{batch_id}` to track the whole run |
| `formula_id` | string | Template ID (a new source creates a placeholder-named template, auto-renamed by a hook once analysis lands) |
| `analyze_task_id` | string? | Analyze task ID (only in `analyze_then_generate`) |
| `task_ids` | string[] | Generation task IDs: the master tasks, one per character (immediate in `generate`; in the chained mode they appear after analysis, fetched from the batch). Extra-ratio reframe tasks join the batch after each master completes |

**Behavior notes:**
- **Rate limit 10 / 60s**; the daily credit cap, a busy server and the new-source analysis cap also return 429 (see Common errors).
- The backend runs a pre-submit balance hold check; on shortfall it returns **HTTP 402** (see "Billing & balance").
- A new source's analysis isn't charged, but is guarded by a **free-cost guard** — spamming new-upload analyses gets blocked (a genuine first riff never is).
- BGM is picked automatically when you leave out `bgm_mode`: the template's original BGM if it has one that isn't `disabled`, otherwise AI-generated music. Leave it out unless the user asks for something specific. With an analyzed template (a `formula_id`, or a TikTok link that was already analyzed, which reuses its template) you can set `bgm_mode` to `source` (keep the original BGM), `source_ref` (the original BGM guides the video's own soundtrack) or `sd2` (AI-generated music). Check the template's `bgm_status` in `GET /api/formulas` first: `source` needs `active` or `policy_violation`, `source_ref` needs `active`, `sd2` always works. Errors: any other value → 400 on every adapt riff; `source` or `source_ref` on a template whose BGM is `disabled` → 400; `source_ref` on a `policy_violation` template → 400 (offer `source`, which still keeps the original BGM). On a template with no BGM (`none`), `source` and `source_ref` are accepted and the video gets AI-generated music. A new upload or a new TikTok link always gets the automatic pick, and swap ignores `bgm_mode`.

**Swap specifics (`mode=swap`):**
- Same response shape. A template source returns `mode: "generate"`. So does a TikTok link that already has a current analyzed template (yours or a public one): it is swapped as that template, so the change / person / length refusals come back at once as 400s, not as `auto_generate_error`. A new upload, or a TikTok link not yet analyzed, returns `analyze_then_generate`, and the chained generation runs as a swap of the new template. The chain re-checks the change rule after analysis: if nothing is left to change (e.g. the product lost its images meanwhile), no video is generated and the analyze task's `result.auto_generate_error` is `"swap_nothing_to_change"`, or `"swap_no_person_to_replace"` when only a character was named and the analyzed source shows no person — tell the user and resubmit with a product with images or a written change (or a character, for the first code). `"swap_product_missing"` means the chosen product was deleted before the swap could start — resubmit with another product (or none). Any other non-empty `auto_generate_error` except `insufficient_credits` (e.g. `source_video_too_long`) also means no video was generated.
- Task `type` is `swap` and the finished asset's `type` is `swap` (`asset_role=final_reel`, listed in `GET /api/assets` like any riff). Poll the batch exactly like a riff.
- Length = the source's length (never compressed); frame shape and language = the source's. One video per character (no character = one video with the original person).
- Billing is per second like every render, with two differences to know when quoting: each render window bills **whole seconds rounded up** (minimum 4s) of the source's video-stream length, so a 14.3s source bills 15s; a source up to one window long (15s on Seedance 2.0, Seedance 2.0 Fast and MiniMax H3; 30s on Seedance 2.5) is a single window, and a longer one is split at its shot cuts into several windows, each rounded up on its own, so it can bill up to 1s more per extra window than its length rounded up (a 20.5s source split at 11.3s bills 12 + 10 = 22s, not 21s; how many windows a source gets depends on its cuts, so it isn't known before rendering); and every swap render carries the source's own clip as a reference, which costs more to render, so **a swap has its own per-second rate** (display credits per delivered second): Seedance 2.0 480p **60/s** · 720p **120/s** · 1080p **300/s**; Seedance 2.5 480p **90/s** · 720p **180/s**; Seedance 2.0 Fast 480p **50/s** · 720p **100/s**; MiniMax H3 768P **80/s** · 2K **160/s**. Reframed extra ratios (of any riff, creation or swap video) use the same rates. Quote these absolute numbers, never "×N the normal rate". `GET /api/settings` → `video_backends[*].input_video_multiplier` is each engine's swap rate ÷ its normal rate (e.g. 1.2 on Seedance 2.0, 2.0 on H3): use it to compare engines, and `swap-quote` for the price.
- **Quote before you submit** (template source): `GET /api/riffs/swap-quote` returns the seconds and credits one video holds on the chosen engine, from the same rules the 402 gate and the hold use: never compute a swap price yourself. For a source within one window that is exactly what the video bills; for a longer source, quote it as "about" that price, since each extra window can add up to 1s. Multiply `credits` by the number of characters (one video each). If `source_seconds` is null, `credits` is a 15-second placeholder, not a price: say the length couldn't be measured and the charge follows the seconds actually rendered. A new upload, or a TikTok link not yet analyzed, has no swap-quote; `GET /api/riffs/quote` gives an approximate price for it (the link's length read from its metadata, the upload's from your measurement), and the exact check runs at submit and again before analysis, with the usual 402.
- Swap errors: nothing to change (no character, no product with images, empty `content_anchor`) → 400 ("A swap needs at least one change…"); only a character, but the template shows no person → 400 ("This video shows no person to replace…"). Both are 400s with a localized `detail` sentence and no machine code: relay `detail`, and don't match on the English text, which follows the request language. The lowercase codes `swap_nothing_to_change` / `swap_no_person_to_replace` appear only in the analyze task's `result.auto_generate_error` (new upload / TikTok link). Source over the render cap → 400 (the same localized too-long sentence as uploads, en: "This video is ~Ns, over the Ms limit. …"); a template that has no source video → 400 ("can't be used for a swap"). A source clip refused by the Seedance content review fails the task (see Details by step → Progress), unbilled.

#### `GET /api/riffs/swap-quote` — price a swap before submitting

The price of one swap video from a template, computed by the same rules as the submit's 402 gate and the task's hold. It is exact for a source that fits one render window (15s on Seedance 2.0, Seedance 2.0 Fast and MiniMax H3; 30s on Seedance 2.5); a longer source can bill up to 1s more per extra window (see Swap specifics). Call it once the user has picked the source, engine and resolution (and again if they change any of them), and quote from it.

**Query:** `formula_id` (an analyzed template, yours or public; required), plus `video_backend` and `resolution` (same values and validation as `POST /api/riffs`; always pass the engine you will submit with; an omitted `video_backend` / `resolution` defaults exactly as a swap submit's does, per account tier) and `delivery` (as on `POST /api/riffs`: with `sections`, `credits` is the first section's and `sections_estimate.whole_credits` the whole video's). The free-tier engine lock is not applied here (the submit still enforces it; check `locked` / `locked_resolutions` in `GET /api/settings`). Rate limit 60 / 60s.

**Response (`SwapQuoteOut`):**

| Field | Type | Notes |
|------|------|------|
| `source_seconds` | number? | The source's video-stream length (null if it couldn't be measured and a template has no analyzed length) |
| `billed_seconds` | integer? | Whole seconds one video holds (rounded up, minimum 4s): what it bills when the source fits one window. Null when `source_seconds` is null |
| `credits` | integer | **Internal** credits one video holds (the 402 gate): what it bills when the source fits one window. ÷100 for display credits; × the number of characters for the batch. Already includes the engine's `input_video_multiplier`. When `source_seconds` is null this is a 15-second placeholder hold, not the video's price: don't quote it; say the length couldn't be measured and the charge follows the seconds actually rendered |
| `max_seconds` | integer | The render-duration cap |
| `over_cap` | boolean | `true` = the source is longer than the cap: a swap of it will be refused with 400, so offer another source instead of submitting |

**Errors:** no `formula_id` → 400; template not analyzed, a template whose analysis is out of date, or a source that can't be swapped → 400 (same messages as `POST /api/riffs`); unknown template → 404; bad engine / tier → 400.

#### `GET /api/riffs/quote` — price any riff before submitting

Use it to answer "what will this cost?" for any riff, adapt or swap, from any source, including a TikTok link that hasn't been analyzed yet. It prices with the same functions as the submit's 402 gate, and says whether the balance covers it and what would. For a template the price is exact (for a swap, see `swap-quote` above for the per-window caveat); for a new link or an upload it is approximate (`exact: false`): the server measures the downloaded file again before analysis, and still stops with a 402 before anything is billed if the video costs more.

**Query:** `mode` (`adapt` / `swap`; `adapt` when omitted, so always send the mode you will submit), exactly one source: `formula_id` (analyzed template) / `tiktok_url` (the server reads the video's length from TikTok's metadata: no download) / `upload_seconds` (the length of a file you are about to upload; for a swap, its video track) / `upload_id` (a video added through an upload link, once it reads `ready`: priced exactly, from the length the server measured). Plus `video_backend`, `resolution` (same values and defaults as `POST /api/riffs`; the free-tier lock is not applied to them here: a locked pair is priced and reported as `locked`), `n_characters` (0 = one video with no character / the original person; else one video per character) `n_ratios` (adapt, 1-4, delivery ratios) and `delivery` (as on `POST /api/riffs`; a free-tier account is priced on `sections` whatever it sends). Same 400s as the submit (not a TikTok video link, source over the render cap, a template whose analysis is out of date, a source that can't be swapped, bad engine / tier). Rate limit 60 / 60s, and 20 / 60s for `tiktok_url`.

**Response (`RiffQuoteOut`)** — every credits field is **internal** (÷100 for display credits):

| Field | Type | Notes |
|------|------|------|
| `source_seconds` | number? | Source length; null for a link whose length couldn't be read |
| `billed_seconds` | integer? | Seconds one video bills (null when the length is unknown) |
| `credits` / `credits_per_video` | integer | The whole batch (what the 402 gate requires) / one character's video |
| `exact` | boolean | `false` for a new link or upload: say "about" |
| `delivery` / `sections_estimate` | string / object? | The delivery the submit would use (`whole` / `sections`). With `sections`, `credits` is the first section's price (exact for a Swap from a template, whose sections are measured before submit; otherwise an estimate, `exact: false`) and `sections_estimate` is `{first_credits, whole_credits}`: quote both, the first section now and about the whole video's price in all (an account held to the first section: only the first, since the rest can't be made from it) |
| `max_seconds` / `over_cap` | integer / boolean | Render cap; `over_cap` only for a swap template (the submit refuses it) |
| `available` / `fits` | integer / boolean | The balance the gate compares with, and whether it covers `credits`. Quote only the price when `fits`; mention the balance only when it doesn't |
| `locked` | boolean | `true` = the submit would answer 403 `subscription_required` for this account on the engine and tier priced here (the price is still that pair's): offer a pair from `alternatives` instead of submitting it |
| `daily_limit_reached` | boolean | A team member's daily limit is used up (a separate refusal from the balance) |
| `reused_formula_id` | string? | The link was already analyzed: submitting it reuses this template, and the price is exact |
| `probe` | string? | For a link: `ok` / `unreadable` (length unknown: the price is the minimum; say the charge follows the real length and a short balance stops before analysis, unbilled) / `busy` (try again shortly) |
| `alternatives` | array | `{video_backend, resolution, credits, fits}` for every other engine and tier this account may use, cheapest first: when `fits` is false, offer one that fits |
| `fitting_templates` | array | Only when `fits` is false: up to 3 public templates `{formula_id, name, thumbnail_url, seconds, credits, video_backend, resolution}` that fit. They are priced on the same engine and tier when any fit there; otherwise on the cheapest engine and tier this account may use, so submit with that template's own `video_backend` / `resolution` to get the price it shows |

#### `POST /api/riffs/uploads` — a link where the user adds a video from their own device

No params. For a source video you cannot send yourself as `video` (it is on the user's phone, or you have no file access): this makes a link to a Riffkit page where the user adds one video from a phone or computer. The page asks for no sign-in, so anyone who holds the link can add one video to this account for up to 90 minutes: the page offers an upload for `seconds_valid` (an hour), and an upload already on its way is still taken for 30 minutes more. Give the user `url` exactly as returned, ask them to say when the video is added, and keep `upload_id`. **Response (`UploadLinkOut`):** `upload_id`, `url`, `expires_at` (naive UTC: when the page stops offering a new upload), `seconds_valid`. The page turns away a video over 100 MB or longer than the render-duration cap. An account keeps at most 10 unused uploads: the oldest links still waiting for a video make room, and with 10 videos in or arriving this answers 429. Rate limit 6 / 10 min. Nothing is charged.

#### `GET /api/riffs/uploads/{upload_id}` — has the video arrived?

`upload_id` (path) is the id `POST /api/riffs/uploads` returned. Ask when the user says the video is added, not in a loop. **Response (`UploadOut`):** `status` = `waiting` (nothing yet; an upload in progress reads `waiting` too; `refused_as` says why the page turned the last file away: `too_long` (over the render-duration cap), `too_large`, `bad_type` or `not_a_video`, and the same link takes another file) / `ready` (`seconds` is its length: send `upload_id` as the source of `GET /api/riffs/quote` and `POST /api/riffs` before `expires_at`) / `used` (already submitted, as `batch_id` from `formula_id`: for another video from it, send that `formula_id` once that template reads `analyzed` in `GET /api/formulas/{formula_id}`, after the first submit's analysis finishes; if that analysis failed, make a new link) / `expired` (the link or the video is gone: make a new link). Another account's upload → 404. Rate limit 60 / 60s. Nothing is changed or charged.

#### `POST /api/pipeline/batch` — riff video (advanced / analyzed-template batch)

`riffs` already covers nearly everything (including multi-character batches). This endpoint remains for fine-grained "analyzed template + explicit params" control; the agent rarely needs it.

| Field | Type | Req | Default | Notes |
|------|------|------|------|------|
| `formula_id` | string | ✓ | | Template ID (status must be `analyzed`, with current analysis: `analysis_prompt_is_latest=true`; else 400) |
| `character_ids` | string[] | | `[]` | Character ID **array** (an array here, unlike riffs' string). Empty array = Auto mode |
| `product_id` | string \| null | | `null` | `null`/omitted = `no_product` |
| `product_visibility` | string | | `on_camera` | Only `on_camera`/`off_camera`; `no_product` is derived from `product_id=null`, never passed directly |
| `content_anchor` | string | | `""` | ≤5000 chars |
| `language` | string | ✓ | | Must be a code from `GET /api/languages` |
| `video_backend` | string | | tier-dependent | `seedance` (Seedance 2.0) / `seedance25` (Seedance 2.5, premium) / `seedance_fast` (Seedance 2.0 Fast) / `minimax` (MiniMax H3). Picks the render engine. Default is **`seedance_fast` `480p` for a free-tier account** (no purchase or subscription on the wallet yet; where Fast isn't offered, `seedance` `480p`) and **`seedance` `720p` for a paid one**, so **omit this param unless the user has a plan**. A free-tier wallet may render on `seedance_fast` `480p` or `seedance` `480p` (480p only); a free-tier caller that names `seedance` / `seedance_fast` without `resolution` gets `480p`. Any other (engine, resolution) pair from a free-tier caller gets **403 `subscription_required`**, the same payload as the analyze paywall (see `POST /api/formulas/analyze`): relay `message`, hand over `subscribe_url` verbatim, do not retry. Resubmit without `video_backend` / `resolution` (the free default) if the user just wants the video. **Resolution is engine-scoped** — see `resolution` below. An engine the deployment has no key for → 400 `video_backend_unavailable`; unknown value → 400 |
| `resolution` | string | | engine base | Engine-scoped: `720p` / `480p` / `1080p` for `seedance`, `720p` / `480p` for `seedance25` and `seedance_fast` (no 1080p on either), `768P` / `2K` for `minimax`. `480p` is draft quality at a lower rate. **Omit it** and you get that engine's base tier (a free-tier account gets that engine's free tier: `480p` on `seedance` / `seedance_fast`); a value the picked engine doesn't sell is a 400. Billing is per second at the (engine, tier) rate, same table as riffs. Live rates: `GET /api/billing/subscription` → `video_credits_per_second_map`; the engines a deployment offers and each one's tiers: `GET /api/settings` → `video_backends` — each entry carries `name`, `resolutions`, `locked: true` when THIS account may use none of its tiers, and `locked_resolutions` (tiers this account may not use; free tier: everything except Seedance 2.0 Fast 480p and Seedance 2.0 480p). Offer only unlocked pairs instead of discovering the 403 |
| `video_ratios` | string[] | | `["9:16"]` | Delivery aspect ratios (array here, unlike riffs' string). Vertical group `9:16`/`3:4`/`1:1`/`4:5` multi-selectable (fans out one video per ratio × character; each extra ratio is metered at that engine's reframe rate, same table as riffs); a horizontal ratio `16:9`/`4:3`/`21:9` must be alone. Invalid / horizontal-mixed → 400 |
| `delivery` | string | | `whole` | As on `POST /api/riffs`: `sections` only when the user asks; a free-tier account always gets `sections` |

**Response (`PipelineBatchResponse`):** `batch_id` / `task_ids[]` / `total` (`task_ids` are the MASTER tasks; extra-ratio reframe children join the same `batch_id` after each master completes).

#### `POST /api/pipeline/backfill` — add ratios to already-delivered videos

Add extra **vertical** aspect ratios to renders you already have (riff, creation or swap videos), without re-generating from scratch (each new ratio reframes the existing render: same shots, same sound, same subtitles, new frame). **Body (JSON):** `{source_asset_ids: string[], video_ratios: string[]}` (vertical ratios only — a horizontal ratio → 400). Any member of a render family works as the source: a reframed variant's `asset_id` resolves to the family's original master render automatically, and one request makes each (family, ratio) at most once (a repeated `asset_id` is read once and its duplicates are dropped with no `skipped` entry; when two different members of one family ask for the same ratio, it is submitted for the first one listed and skipped as `already_occupied` for the other. Nothing is billed twice). **Response:** `{submitted: [{task_id, asset_id, ratio}], skipped: [{asset_id, ratio, reason}], batch_id}`. Skip reasons: `already_occupied` (ratio already delivered or in-flight for that family), `source_not_reframeable` (no reusable render on hand, or the family's original master video was deleted from the library: deleting it ends that family's reframes), `landscape_source` (a `16:9`/`4:3`/`21:9` render can't be reframed — targets are portrait-only and cross-orientation reframe is unsupported; don't submit landscape sources). Each reframe bills at its engine's reframe rate (see `POST /api/riffs` → `video_ratios`) for the seconds of the existing render it re-renders (on MiniMax H3 that can be up to 1s more per rendered piece than the video's length, because H3's pieces run slightly past their whole second; `credits_per_ratio` already includes it). 402 when the balance can't cover the submitted reframes; quote the price from `occupied` below first.

#### `GET /api/pipeline/backfill/occupied?asset_id=<id>` — ratios already produced

Returns `{occupied: string[], credits_per_ratio: number, reframeable: boolean}`. `occupied` = the delivery ratios already delivered or in-flight for the asset's render family (grey these out in a ratio picker; they'd be skipped by the backfill). `credits_per_ratio` = the exact internal credits one extra ratio will cost (÷100 for display credits), measured from the existing render: the same number the 402 gate and the hold use, so quote it and never compute a reframe price yourself. `reframeable=false` (with `credits_per_ratio` 0) = this video can't be reframed at all (e.g. its original was deleted, or it's a landscape video): don't offer extra ratios.

#### `POST /api/creation/batch` — creation video (original, no source video)

The second generation mode: no source video, no template — the **creative direction IS the script's source**, so here it is REQUIRED (on riffs it optionally steers a template). The engine authors an original ad video from it (per-second billing, same rates as riffs). Price it first with `GET /api/creation/quote` (below), asked with the length, engine, resolution and number of characters you are about to submit, and restate the plan with that price before the confirmation, as for a riff.

**Content-Type:** `application/json`

| Param | Type | Required | Notes |
|------|------|------|------|
| `content_anchor` | string | **yes** | Creative direction, 1-5000 chars — the story/scene, captions, lines, pacing. The more specific, the more controllable. Text that is only spaces is refused like an empty one (422) |
| `character_ids` | string[] | no | Empty = Auto (AI generates the on-screen person). One video per character; a character needs an approved avatar (`has_any_active_avatar=true`), else 400 `character_avatar_not_ready` |
| `product_id` | string? | no | null or `""` = no product placement. `on_camera` placement requires the product to have images (400 otherwise) |
| `product_visibility` | string | no | `on_camera` (default) / `off_camera` |
| `duration_mode` | string | no | `smart` (default: AI picks the length by content, capped at 45s AND at what the balance affords) / `fixed` |
| `duration_seconds` | int | with fixed | 4-45; required when `duration_mode=fixed` |
| `language` | string | no | Default `en`; same whitelist as riffs |
| `video_backend` | string | no | `seedance` (Seedance 2.0) / `seedance25` (Seedance 2.5) / `seedance_fast` (Seedance 2.0 Fast) / `minimax` (MiniMax H3); 400 if not configured on the deployment. Default is **`seedance_fast` `480p` for a free-tier account** (no purchase or subscription on the wallet yet; where Fast isn't offered, `seedance` `480p`) and **`seedance` `720p` for a paid one**, so **omit this param unless the user has a plan**. A free-tier wallet may render on `seedance_fast` `480p` or `seedance` `480p` (480p only); a free-tier caller that names `seedance` / `seedance_fast` without `resolution` gets `480p`. A free-tier caller that passes any other engine or tier gets **403 `subscription_required`**, the same payload as the analyze paywall (see `POST /api/formulas/analyze`): relay `message`, hand over `subscribe_url` verbatim, do not retry; resubmit without `video_backend` / `resolution` (the free default) if the user just wants the video. |
| `resolution` | string | no | Engine-scoped: `720p`/`480p`/`1080p` (seedance), `720p`/`480p` (seedance25, seedance_fast) or `768P`/`2K` (minimax). Omit for the engine base tier (a free-tier account gets that engine's free tier: `480p` on `seedance` / `seedance_fast`); a value the picked engine doesn't sell is a 400. Same rate rules as riffs |
| `video_ratio` | string | no | Single ratio, default `9:16` (creation has no reframe fan-out at submit; add ratios later with `POST /api/pipeline/backfill`) |
| `delivery` | string | no | `whole` (default) / `sections`, as on `POST /api/riffs`: `sections` only when the user asks; a free-tier account always gets `sections` |

**Response:** `{batch_id, task_ids: string[], total}` — one task per character (or one Auto task). Task `type` is `creation`; poll the batch exactly like a riff. 402 detail shape is identical to riffs. Task output shows in Library like any riff (`AssetOut.content_anchor` carries the direction).

#### `GET /api/creation/quote` — price a creation video before submitting

The price of a creation batch before you submit it, computed by the same function as the submit's 402 gate, with the balance read the same way. Call it once the length, engine, resolution and characters are settled (and again if one of them changes), and quote from it. The creative direction, the product, the language and the ratio don't change the price, so it takes none of them.

**Query:** `duration_mode` (`fixed` / `smart`; `smart` when omitted, exactly as the submit runs it, so always send the one you will submit), `duration_seconds` (4-45: required with `fixed`, where leaving it out is a 400; ignored with `smart`), `video_backend`, `resolution` (same values and defaults as `POST /api/creation/batch`; the free-tier lock is not applied to them here: a locked pair is priced and reported as `locked`), `n_characters` (how many characters you will send: one video per character; omitted or below 1 = one video), `delivery` (as on `POST /api/creation/batch`; a free-tier account is priced on `sections` whatever it sends). Bad engine / resolution → 400. Rate limit 60 / 60s.

**Response (`CreationQuoteOut`)** — every credits field is **internal** (÷100 for display credits):

| Field | Type | Notes |
|------|------|------|
| `video_backend` / `resolution` | string | The engine and resolution the submit would render on (yours, or this account's defaults) |
| `seconds` | integer? | Length of one video. `fixed`: the seconds you asked for. `smart`: the longest the balance allows, at most 45 (the cap the submit hands the engine; the video may come out shorter). Null in `smart` when the balance is below the shortest video (4s) |
| `credits` | integer | The whole batch: what the 402 gate compares with the balance and the tasks hold. `fixed`: what the videos bill. `smart`: the most the batch can bill |
| `min_credits` | integer | The batch at the shortest video (4s each): what a `smart` submit needs at least |
| `exact` | boolean | `true` for `fixed`. `false` for `smart`: the charge is for the seconds delivered, so say "up to" |
| `delivery` / `sections_estimate` | string / object? | As in `GET /api/riffs/quote`: with `sections`, `credits` is the first section's (and `exact` is `false`), `sections_estimate.whole_credits` the whole video's |
| `available` / `fits` | integer / boolean | The balance the gate compares with, and whether the submit would pass its 402 gate (`smart` fits as soon as the balance covers `min_credits`: the video is sized to the balance). Quote only the price when `fits`; mention the balance only when it doesn't, and then offer a shorter `fixed` length or another engine and resolution |
| `locked` | boolean | `true` = the submit would answer 403 `subscription_required` for this account on this engine and resolution: offer a pair that isn't locked (`GET /api/settings` → `video_backends`) |
| `daily_limit_reached` | boolean | A team member's daily limit is used up (a separate refusal from the balance) |

#### `POST /api/assets/{asset_id}/continue` — make the rest of a video made in sections

A video submitted with `delivery=sections` (always, on a free-tier account) is made a section at a time: its first render delivers the first section, and the video's `staged` block in `GET /api/assets` says what is left: `pending` (true while sections are left), `delivered_through` (the last delivered section, 0-based), `finish_by` (naive UTC: the last moment it can be continued) and `prices` (`{next, rest, redo}`, internal credits, ÷100 for display credits). This call makes more of it, on the same script. **Body (JSON):** `action` (`next` = the next section, `rest` = everything that is left, `redo` = the last delivered section again), `credits` (the price of that action you quoted from `staged.prices`: when it is not the price now, nothing starts and the answer is 409 `price_changed` with the price now, so ask again) and `delivered_through` (the `staged.delivered_through` you read: when the video has moved on since, 409 `price_changed`). Both are required: a body without either starts nothing and answers 409 `confirm_needed` with the price and `delivered_through` now (402 first when the balance doesn't cover it). Quote the price and get the user's go-ahead first; every call spends again. Each delivery becomes a new version of the same video (same `asset_id`): fetch its link again (`GET /api/assets/{asset_id}/link`) once the task is done. **Response (202):** `{task_id, batch_id}`: follow `batch_id` with `GET /api/tasks/batch/{batch_id}`. A refusal starts nothing: 400 not a video made in sections, or an action it has no price for now; 409 `film_complete` (nothing is left) or `film_busy` (part of it is being made now); 410 past `finish_by` (only a new video can be made); 402 the balance does not cover the price (see "Billing & balance"); 403 `subscription_required` with `code` `first_section_only`: this account is held to the first section (it can only `redo` the first section), handled as in "Billing & balance"; so on such an account (`staged_delivery.forced` is `sections`) never quote or offer `next` / `rest`. Rate limit 10 / 60s, and the daily credit cap applies.

---

### Templates (formula library)

#### `GET /api/formulas`

**Query:** `status` (exact match: collected/analyzing/analyzed/archived; omitted = everything except archived), `template_type` (use `pipeline`), `tags` (comma-separated), `search`, `sort` (created_desc/created_asc/used_desc), `limit` (default 50), `offset`.

**Response (`FormulaListOut`):** `items: FormulaOut[]` / `total` / `limit` / `offset` (header `X-Total-Count` = filtered total).

**FormulaOut (customer-visible fields):**

| Field | Type | Notes |
|------|------|------|
| `id` / `name` | string | Template ID / name |
| `template_type` | string? | Default `"pipeline"` (this skill only consumes this; filter out others) |
| `status` | string | `collected` / `analyzing` / `analyzed` / `archived` — `analyzing` = analysis still running (including a riff's placeholder template); only `analyzed` can be riffed (others return 400) |
| `emotion_arc` | string? | Emotion arc (generic funnel-stage sequence, e.g. "hook → build-up → cta") |
| `slot_count` | int? | Number of formula segments |
| `used_count` | int? | Times riffed (high = peer-validated) |
| `tags` | string[] | Tags |
| `source_url` / `source_platform` | string? | Original link / platform |
| `thumbnail_url` | string? | Thumbnail |
| `analysis_prompt_is_latest` | bool | `false` = analysis out of date: the quotes and the submit refuse a riff or swap on it (400, nothing billed). Your own template: `refresh-analysis` first. A public one: pick another |
| `user_hint` | string? | Hook hint the analysis ran with (change your own via `PATCH /api/formulas/{id}`, then refresh) |
| `bgm_status` | string | `none` / `active` / `disabled` / `policy_violation` — which `bgm_mode` values the template can serve (see `POST /api/riffs` → Behavior notes) |
| `visibility` | string | `scope` (this scope only) / `public` (platform-curated, prefer recommending) |
| `created_at` | datetime? | Created |

> `hook_type` / `cta_type` (two legacy formula-derivative fields) are **not exposed to customers**; the per-slot formula itself IS exposed via `extraction_summary.formula_slots` (see below). The raw `analysis_card` stays customer-hidden.

#### `GET /api/formulas/{formula_id}` — extraction summary

**Response (`FormulaDetailOut`):** all FormulaOut fields + `analysis_card` (**always `null` for customers** — the full formula DSL is engine IP) + `extraction_summary` (a safe projection).

**`extraction_summary` (the agent reads this to understand the template, NOT analysis_card):**

| Field | Type | Notes |
|------|------|------|
| `duration_seconds` | float? | Source video length |
| `language` | string? | Source language |
| `speaking_mode` | string? | Speech form |
| `narrative` | string | Plain-language record of "what happens" in the source (internal markers stripped) |
| `transcript` | `[{at, text, mode}]` | Line-by-line dialogue (`at` = start second, `mode` = on_camera_dialogue/voiceover/no_dialogue) |
| `on_screen` | `[{kind, label, at}]` | On-screen entity timeline (`kind` = person/subtitle/product_image/... `label` = human label) |
| `formula_slots` | `[{at, end, formula}]` | The real Stage A attention formula, one entry per funnel slot. `formula` is a free dict — typical keys: `funnel_stage` (attention/interest/payoff/cta), `function`, `mechanism`, `viewer_state_before`/`viewer_state_after`, `meaning_contract{attention_contract, payoff_meaning, proof_surface}`, `constraint`, `sensory_channel`, `retention_anchor`, `linguistic_craft`. Empty on templates analyzed before slots existed. |

**Reading the emotion formula**: `formula_slots` IS the formula — per-slot mechanism, viewer-state transition, and meaning contract straight from the analysis. Skim it first; use `narrative` + `transcript` for the concrete surface that carries it, and `emotion_arc` for the stage sequence at a glance.

#### `POST /api/formulas/analyze` — analyze a new source into a template (subscribers only)

Turn a **new** source into the caller's own template **without generating a video** — for building a template library ahead of time. **Subscriber-only**: callers without an active subscription get `403`; they should riff instead (`POST /api/riffs`, which is paid per generated video). Subscribers are additionally volume-capped by the same margin-tied free-cost guard that protects all no-generation analysis, so heavy standalone analyzing without ever generating eventually returns `429`.

**Request (multipart/form-data):** exactly one source — `tiktok_url` (a TikTok **video** link, ≤ render cap) **or** `video` (upload, ≤100MB, ≤ render cap); an upload over the cap gets a 400 and nothing is created; a TikTok link over the cap gets the same 400 when its length can be read up front, otherwise the task is queued and fails with the same message once the video has downloaded — plus optional `user_hint` (where the hook/payoff is) and `name`. **Response:** `{task_id, status: "queued"}`; poll `GET /api/tasks/{task_id}`. On completion the new template appears in `GET /api/formulas` (the caller's own, `status` transitions `analyzing`→`analyzed`). Unlike `POST /api/riffs`, this **never chains generation** — it only analyzes.

**When to use:** the user explicitly wants to *bank a template for later* from a new source without spending on a video. For the normal "make me a video" ask, use `POST /api/riffs` — it analyzes and generates in one shot.

**`403` for free users (guide them to pay):** a caller without an active subscription gets `403` with a structured detail — `{"error": "subscription_required", "message": <localized sentence>, "subscribe_url": "<server-issued billing URL>"}` (same shape family as the `402` `insufficient_credits` payload). **The same payload is the free-tier engine lock**: submitting any engine/resolution other than Seedance 2.0 Fast 480p or Seedance 2.0 480p on a wallet that has never paid returns this exact detail (handle it identically: the working alternative is resubmitting without `video_backend` / `resolution`, which lands on the free default for that mode). On this 403: relay `message`, hand over `subscribe_url` **verbatim** (server-issued — never hardcode a billing URL), and note the alternative that works without a subscription — `POST /api/riffs` (analyze **and** generate in one shot, paid per generated video). Do not retry the analyze call.

#### `POST /api/formulas/{formula_id}/refresh-analysis`

Re-run the analysis of one of **your own** templates (`visibility=scope`, `status` `analyzed` or `collected`) under the current version: when it's stale (`analysis_prompt_is_latest=false`) or when the analysis missed the hook. Free. **Response:** `{task_id, status: "queued"}`; poll `GET /api/tasks/{task_id}`. The run uses the template's stored `user_hint`; to change it, `PATCH` first (below), then refresh. A platform template (`visibility=public`) can't be refreshed or edited from your account (`404`): pick a current one instead, or riff the original from its TikTok link or an upload. Any other status → `400`; heavy re-analysis without generating is capped (`429`, as with `POST /api/formulas/analyze`).

#### `PATCH /api/formulas/{formula_id}` — rename a template or change its hint

**Body (JSON):** any of `name`, `user_hint` (≤5000 chars; `null` or `""` clears it). Your own templates only (a platform template → `404`); a name already used by another of your templates → `409`; an over-long hint → `400`. Returns the updated `FormulaOut`. Changing the hint doesn't re-analyze by itself: follow with `refresh-analysis`.

---

### Creation caps (characters / products / avatars)

How many characters, products, and avatars an account may own depends on whether the wallet has ever paid. **The numbers are runtime-tunable — never hardcode them; read them from `GET /api/settings` → `creation_limits` and pre-check before staging a new character/product/avatar.**

| Tier | Characters | Products | Avatars per character |
|---|---|---|---|
| **Free** (wallet never purchased / subscribed / comped) | 1 | 1 | 1: the one uploaded at creation. A new upload is allowed only if that one failed review (failed avatars don't use the slot; one still in review does) or was deleted |
| **Paid** | 50 | 50 | 10 |
| Staff | unlimited | unlimited | unlimited |

`creation_limits` = `{tier: "free" \| "paid" \| "staff", characters, products, avatars_per_character}`, each count an integer or `null` (= unlimited). The caps are **per scope** (a team's members share the owner's allowance), and they are re-derived server-side on every create, so the pre-check only saves a round-trip — the errors below still have to be handled.

The capped writes are `POST /api/characters`, `POST /api/products`, and `POST /api/characters/{character_id}/avatars`. Deleting an unused character / product / avatar version frees a slot immediately (a character's only avatar may be deleted even while active — the character then has no avatar until a new upload is approved). Creates are also throttled per workspace (`429` past roughly 20 characters / 30 products / 20 avatar uploads per hour) — a person never reaches that; do not loop.

- **Free tier over a cap → `403`** with the **same** `{"error": "subscription_required", "message", "subscribe_url"}` detail as the analyze and engine paywalls — handle it identically (see the `403` paragraph under `POST /api/formulas/analyze`): relay `message`, hand over `subscribe_url` **verbatim**, do not retry.
- **Paid tier over a cap → `400`** `{"error": "limit_reached", "kind": "character" \| "product" \| "avatar", "limit": <N>, "message": <localized sentence>}`. This is a stop, not an upsell: relay `message` and tell the user to delete an unused one (or reuse an existing character/product) — **do not** pitch a plan and do not retry.

---

### Characters

#### `GET /api/characters`

**Response:** `CharacterOut[]`.

| Field | Type | Notes |
|------|------|------|
| `id` / `slug` | string | Immutable identifier (same value; `slug` is the canonical name) |
| `name` | string | Display name |
| `gender` | string? | `female` / `male` / null |
| `age_range` | string? | `young` / `middle_aged` / `senior` / null |
| `persona` | string? | **Free-text account identity** — the single source for positioning / audience / tone |
| `reference_image` | string? | Avatar image path (fetch `${BASE_URL}${reference_image}` with the session cookie, like a video's `file_url`) |
| `has_any_active_avatar` | bool | (default false) **The hard test for "can generate video"**: true only when the character's current avatar (`active_avatar_id`) has passed review. Uploading a new avatar, or retrying review on a different one, switches the character to it immediately, so this is false while that avatar is in review (usually under a minute), and stays false if that review fails, even if older avatars were approved. To go back to an approved avatar, pick it on the Characters page |
| `has_any_processing_avatar` / `has_any_failed_avatar` | bool | Has an avatar in review / failed |
| `seedance_asset` | object? | The in-use / most-recent avatar's review record (`status`: processing/active/failed) |
| `active_avatar_id` | string? | The in-use avatar row id |
| `stats` | object? | Asset stats (`total_assets` / `by_type`) |

> Choose a character by `persona` feel + `gender` / `age_range` + `has_any_active_avatar`. Creating/editing characters is left to the Characters page (the create form needs a name, an avatar image, a gender and an age range; persona is optional but worth filling in, since it's the account identity Riffkit matches on); Riffkit doesn't proactively guide creation. If the user does create one on that page, remember it's capped — free tier 1 character with 1 avatar, paid 50 with 10 avatars each (see "Creation caps" above). There is no `description` field (account identity lives entirely in `persona`).

`CharacterOut` also carries `voice_sample` (string?, web path; null = none) — a 4-15s clean-speech clip the engine locks as the character's voice on dialogue segments (adapt riffs and creations, automatic once set; swap riffs don't use it).

#### `POST /api/characters/{character_id}/voice-sample` — upload voice sample

**Content-Type:** `multipart/form-data`, field `audio` (**mp3/wav only** — Seedance accepts exactly these; ≤5MB, duration 4-15s — 5-10s is best; no background music/noise). **Response:** updated `CharacterOut`. Replacing = upload again (pointer swaps).

#### `DELETE /api/characters/{character_id}/voice-sample`

Clears the sample (generation falls back to the default voice). **Response:** updated `CharacterOut`.

---

### Products

#### `GET /api/products` → `ProductOut[]`

| Field | Type | Notes |
|------|------|------|
| `id` / `name` | string | Product ID / name |
| `description` | string? | Product description (**the single source of product fact**; Stage B infers category/tags from it as needed) |
| `target_audience` | string? | Target audience |
| `images` | `ProductImageOut[]` | Product images |

**ProductImageOut:**

| Field | Type | Notes |
|------|------|------|
| `id` | string | Image ID |
| `url` | string | Image URL |
| `name` | string | **Image name** — write this name in `content_anchor` text to place the image on screen (on_camera). An unnamed image can't be referenced |
| `description` | string | Image description |
| `usage_context` | string | User-written "when to use this image" |
| `content_policy` | string | `locked` (default, AI cannot edit it) / `mutable` (editable) |
| `caption_status` | string | Background vision-captioning state: `pending` (generating) / `""` (not captioning: finished, skipped, or failed). Don't treat pending as an error; check `description` to see whether a caption was actually written |

#### `POST /api/products`

**Body (`ProductUpdateRequest`):** `name` (✓), `description` (✓), `target_audience`. **Response:** `ProductOut`.

> **Capped** — free tier 1 product, paid 50 (see "Creation caps" above). Pre-check `GET /api/settings` → `creation_limits.products` against `GET /api/products` before staging a new product; over the cap you get the free-tier `403 subscription_required` or the paid-tier `400 limit_reached`.

#### `POST /api/products/{product_id}/images`

Add an image. URL or file (**either/or**). Max 8 images per product (either source; a 9th → 400). File uploads: `.jpg/.jpeg/.png/.webp` (other formats → 400), ≤50MB each (over → 413), and an image whose short edge is too small or whose aspect ratio is too narrow or too wide for the video engine → 400 (the message states the limit and the image's size). URL images must be a public **https** link (http, or a host that doesn't resolve to a public address → 400); they aren't checked for format, size or dimensions here.

**Form:**

| Field | Type | Req | Notes |
|------|------|------|------|
| `file` | File | either/or | Upload image |
| `image_url` | string | either/or | Public **https** image URL (http is rejected) |
| `name` | string | ✓ | **Image name** (required on new upload; non-empty names are unique per product, trimmed, case-insensitive) |
| `image_id` | string | | Custom id (else derived from filename/URL; reserved words `protagonist` / `supporting_a`~`z` not allowed) |
| `description` | string | | Image description (for a file upload left blank → captioned automatically in the background, `caption_status=pending` meanwhile; URL images are never auto-captioned, nor are uploads once the workspace's free-cost guard is exceeded, and captioning can come back empty, so write the description yourself when it matters) |
| `usage_context` | string | | When to use this image |
| `content_policy` | string | | `locked` (default) / `mutable` |

**Response:** `ProductOut` (the full updated product).

> Multi-image upload must be **serial** (one awaited after another, not parallel) — the backend does read-modify-write per product, and parallel uploads race and drop images.

---

### Languages

#### `GET /api/languages` → `Language[]`

| Field | Type | Notes |
|------|------|------|
| `code` | string | BCP-47 code (`en` / `es` / `ja` …) to put in the `language` field |
| `name` | string | English display name (English / Spanish / Japanese …) |

> Currently **9 languages**: `en` / `es` / `pt` / `id` / `de` / `fr` / `it` / `ja` / `zh-CN` (English, Spanish, Portuguese, Indonesian, German, French, Italian, Japanese, Mandarin). Each riff is **generated natively in-language** — native phrasing and captions aligned to the spoken audio, not a translated caption layered on a finished video. The set adjusts with the product, so **trust this endpoint's response, don't hardcode**. `riffs` and `pipeline/batch` share the same candidate set.

---

### Task monitoring

#### `GET /api/tasks/{task_id}` → `TaskOut`

| Field | Type | Notes |
|------|------|------|
| `id` | string | Task ID |
| `type` | string | `pipeline` (adapt riff) / `swap` (swap riff) / `creation` (original video) / `analyze` (template analysis) / `subtitle_burn` / `subtitle_reconcile` (free subtitle post-production). An extra-ratio render (a ratio fan-out or `POST /api/pipeline/backfill`) carries its source video's type (`pipeline` / `creation` / `swap`) |
| `status` | string | `queued` → `running` → `completed` / `failed` / `dead` / `cancelled` |
| `progress` | int | 0-100 |
| `current_step` | string? | Internal progress code, not display text: usually a step key, plain (`step.stage_b`) or with parameters after `:` (`step.segment_generating:2\|3` = segment 2 of 3), possibly with a label prefix. A few lifecycle values are not keys (e.g. `subtitle_reconcile`, or short non-English status words when a task starts, finishes or is recovered). Never show it verbatim; describe progress in plain words ("writing the script", "generating video, segment 2 of 3", "adding captions") |
| `error` | string? | Failure reason (sanitized + truncated) |
| `character_id` / `formula_id` / `formula_name` / `product_id` | string? | Linked entities + template-name snapshot |
| `batch_id` | string? | Batch ID |
| `product_visibility` | string? | `on_camera` / `off_camera` / `no_product` (config replay) |
| `language` | string? | Language code |
| `ratio` | string? | Delivery aspect ratio of this task's video (e.g. `9:16`). Null on a swap task (its video's ratio is `extra_metadata.ratio` on the finished asset) and on tasks that render no video |
| `content_anchor` | string? | Creative direction (riff AND creation — same field) |
| `user_hint` | string? | Hook hint (analyze tasks only) |
| `duration_mode` / `duration_seconds` | string? / int? | Creation tasks only: `smart`/`fixed` + the fixed seconds |
| `segment_count` | int? | Not filled for current tasks (always null; older tasks may still carry a value). Don't rely on it |
| `submitted_by_user_id` | string? | Submitter user_id (in a team scope, resolve to a member via `/api/scopes/{id}/members`; a solo scope = the owner) |
| `result` | any? | On success, contains asset_id etc. |
| `output_video_url` / `output_cover_url` | string? | The video / cover THIS task produced (append `${BASE_URL}`, fetch like `file_url`). For a render it is the first cut; for a `subtitle_burn` it is that burn's version. When it differs from the asset's current `file_url`, this task made an earlier version. Null when the task produced no video (`analyze`, `subtitle_reconcile`, or not finished) |
| `created_at` / `started_at` / `finished_at` | datetime | Timestamps (naive UTC; parse as UTC on the frontend) |

#### `GET /api/tasks/batch/{batch_id}` → `BatchStatusOut`

`batch_id` / `total` / `completed` / `failed` / `running` / `queued` / `tasks: TaskOut[]`. **Preferred for tracking a whole riff.**

#### `GET /api/tasks` — list tasks

**Query:** `status` (single or comma-separated allowlist like `failed,dead`), `type` (any of the task types above; one value or a comma-separated list, e.g. `pipeline,swap` for every riff render; an unknown value just returns no rows), `date_from` / `date_to` (`YYYY-MM-DD` or full ISO 8601; Task.created_at is naive UTC), `submitted_by_user_id` (filter by submitter, only meaningful in a team scope), `limit` (default 100, 1-500), `offset`. Header `X-Total-Count`.

**Response:** `TaskOut[]`. Usage: "how many are running now" → `?status=running`; "last 10 failures" → `?status=failed&limit=10`; "today's tasks" → `?date_from=2026-06-20&date_to=2026-06-20`.

#### `GET /api/tasks/stats`

Counts grouped by `type` / `status` (for tab badges). **Query:** `date_from` / `date_to` / `submitted_by_user_id` (not `status`/`type` — those are the grouping dimensions). **Response:** `total` / `by_type` (e.g. `{"pipeline":12}`) / `by_status` (e.g. `{"completed":9,"failed":2}`).

#### `POST /api/tasks/{task_id}/cancel`

Cancel a `queued`/`running` task. Other states → 400. A running task already in its final steps (stitching, music, subtitles, cover, saving) → 409: every second is already rendered and billed, so it can't be stopped and will finish and deliver. Otherwise it marks the task `cancelled` (not failed); it **does not interrupt** a running subprocess (it exits after the current step), and **external calls already made are charged and not refunded**. Usage: on "stop it" → call it and say clearly: "what's already charged isn't refunded; running sub-steps finish the current stage before stopping." On 409 → tell the user it's already in the final stage and the video is about to arrive, then keep polling. Don't proactively suggest cancelling unless a task is clearly hung.

#### `POST /api/tasks/{task_id}/retry`

Retry a `failed`/`dead` task (retryable within 24h and only if the schema version matches). **It re-runs the same task (same `task_id`) and picks up from its saved progress: video parts that finished before the failure are usually reused and not billed again; only what it renders again is billed, and nothing is billed for what fails. Reuse isn't guaranteed (e.g. when saved parts can't be restored), so the cost can reach the full video's price.** `dead` means the task was interrupted and couldn't resume on its own (see Task state machine); retry is the only way to recover it, and retrying a subtitle burn / reconcile is free. Usage: on "run it again" → **first state the most the retry can cost**, from the server, never your own arithmetic: the quote for the same arguments as the task (its own `mode`, source, `video_backend`, `resolution` and `delivery` from `GET /api/tasks/{task_id}`) — `GET /api/riffs/quote` for a riff or swap, `GET /api/creation/quote` for a creation, `credits_per_ratio` from `GET /api/pipeline/backfill/occupied` for a reframed extra ratio — and say it can cost less if part of the video was already made; `GET /api/usage/credits` gives the balance to compare against → let the user decide; if the failure was user-fixable (bad product image / stale template analysis), fix the cause first. Note: retrying an **analyze** task whose template was deleted after the failure rebuilds that template (same id) and completes normally — the deleted card reappears in `GET /api/formulas`.

A refused retry restarts and bills nothing, and its `detail` is always Chinese, so explain it in the user's language:
- `410`: more than 24 h have passed since the task was first submitted (`created_at`, UTC; a retry doesn't restart this clock, so check it before quoting a retry), or it is a riff or swap submitted before a Riffkit update that changed how riffs are built (unrelated to which video engine was picked). Say it's too old to retry and offer a fresh submit of the same kind with the same options: a riff or swap → `POST /api/riffs` with the same `mode` (a template source, `formula_id`, reuses its saved analysis); a creation → `POST /api/creation/batch`; an extra ratio (`reframe_master_task_id` set) → `POST /api/pipeline/backfill`; a template analysis → the same source sent the same way again; a subtitle burn / reconcile → the same `POST /api/assets/{asset_id}/subtitles/…` call.
- `409`: the task's previous run is still shutting down. Wait about a minute and retry once; if it's still `409`, tell the user and check back later (ignore the `detail`'s advice to cancel: a failed task can't be cancelled).
- `400`: the task isn't `failed`/`dead` (a `cancelled` task can't be retried, and one an earlier retry already restarted reads `queued`). Poll `GET /api/tasks/{task_id}` instead of submitting again.
- `404`: no such task in this account.

#### `GET /api/tasks/{task_id}/content` — extraction/rewrite preview (optional)

Review what the engine "extracted / rewrote" for a task, for the delivery strategy recap. **Response (`TaskContentOut`):** `extraction` (an analyze task's extraction, same shape as `extraction_summary`), `rewrite` (a generation task's rewrite: `story` / `dialogue` / `caption` / `hashtags`), `template_name`, `content_anchor`, `user_hint`.

---

### Assets

#### `GET /api/assets`

**Query:** `asset_id` (string[]), `type` (`pipeline` = riff video / `creation` = creation video / `swap` = swap video / `upload` = reference material), `source_type` (string[], repeatable: filter by those same type values, e.g. `source_type=pipeline&source_type=creation`), `asset_role` (final video = `final_reel`), `character` (string[]), `product_id` (string[]), `formula_id` (string[]), `created_window` (today/7d/30d/90d), `sort` (created_desc/created_asc/character_az/product_az), `page` (≥1), `limit` (1-200, default 50).

**Response:** `AssetOut[]`.

| Field | Type | Notes |
|------|------|------|
| `id` / `type` / `asset_role` / `name` | | `asset_role=final_reel` is the finished riff |
| `character_id` / `formula_id` / `formula_name` / `product_id` | string? | Linked entities |
| `file_url` | string? | Download path (append `${BASE_URL}`) |
| `thumb_url` | string? | Thumbnail |
| `sd_video_url` | string? | Raw pre-post-processing SD video (only when the final had post-processing) |
| `caption` | string? | Suggested copy (hook → body → closing CTA in one paragraph) |
| `asset_hashtags` | string[] | Suggested hashtags |
| `batch_id` / `task_id` | string? | Source batch / task |
| `metadata` / `extra_metadata` | dict | Metadata |
| `created_at` | datetime | Created |

#### `GET /api/assets/{asset_id}/link` — a link to a finished video that needs no session

`asset_id` (path) is the id of a finished video (`asset_role=final_reel`): a completed task's `result.asset_id`, or an `id` from `GET /api/assets`. Returns `{url, expires_at, seconds_valid}`: `url` is an absolute link that plays the video in a browser with no cookie (it opens in place rather than as a download), `seconds_valid` is how long it works, counted from the call (21600 = 6 hours), and `expires_at` is that moment as a timestamp (naive UTC, like every timestamp here). Use it to hand the video to the user where your session cookie doesn't travel: a link in chat, their browser, another tool. Give `url` exactly as returned, say how long it works, and that anyone who holds the link can open the video until then. It points at the video's current file: after a subtitle burn, or once it has stopped working, call again for a fresh one. Nothing is stored or changed and nothing becomes public (a public share page is something the user starts in the web app). 404 = no finished video with that id in this account. Rate limit 60 / 60s.

#### `POST /api/assets/upload` (sidecar; not used by the main flow)

Riff videos are derived from template + product + character — **no manual material upload is needed.** This endpoint only ingests user-provided reference videos/images. **Form:** `file` (✓, video ≤100MB / image ≤50MB), `asset_role` (✓, `reference`), `product_id` / `character_id` / `name` / `notes` (optional).

> To download a finished video: GET `${BASE_URL}${asset.file_url}` **with the `vee_session` cookie and `-L`** (production 302s to object storage; no cookie → 401). There is no `/download` endpoint — `file_url` is the only path for your own download; for a link the user opens without the cookie, see `GET /api/assets/{asset_id}/link` above.

---

### Subtitle editing (post-production, free)

Fix a finished video's subtitles without regenerating it: retime a line, move captions out of a face, change text/color/size, delete a line, then re-burn. **Zero-charge** — burn/reconcile are pure post-production (no video generation), so no credits are ever spent here; don't warn the user about cost. All endpoints take the **asset id** of the finished video (`asset_role=final_reel`). A video made in sections whose `staged.pending` is true can be read but not changed: `PUT`, `DELETE .../edits`, `burn` and `reconcile` answer 409 `film_pending` (its captions belong to the whole video) until all of it is made.

**What you can edit, on every video:** the caption layer Riffkit burns on top of the picture, and nothing else; `GET` returns that layer. Text that is part of the picture itself can't be edited, moved or removed here. On a swap (`type: "swap"`) that is the common case: the source video's on-screen text (its captions, labels, stickers) is drawn into the picture, so a swap's list holds only what its "What to change" (`content_anchor`) added (new captions, or a full-screen card it replaced), and is often empty. You can still add new lines on top of any video. Never re-type text that is already in the picture; it would show twice. To change a swap's original on-screen text, make a new swap and say so under "What to change".

**The editing loop (recommended):**

1. `GET /api/assets/{asset_id}/subtitles` → current state. A 404 mentioning *reconcile* means no caption layer is recorded for this video yet: it predates subtitle persistence, or nothing was burned on it (a video rendered without subtitles, or a swap whose only text is its source's, drawn into the picture). Run step 0: `POST .../subtitles/reconcile` (a short task; poll it like any task), then GET again. Reconcile even if you only want to ADD lines: an older video already shows its subtitles, and burn re-burns from the video without subtitles using only the lines in your list, so PUTting just the new lines would erase the existing ones. Skip reconcile only for a video you know was generated without subtitles.

   **Which lines to check first.** Spoken lines in the machine baseline carry `params.align_status`, how their timing was found: `aligned` / `member_submatch` = measured against the speech; `imputed` = the planned time shifted by how far the measured lines drifted; `member_scaled` = one of several captions for one spoken line, placed by scaling its planned time onto that line's measured window; `unaligned_planned` = the speech couldn't be matched, so the line sits at its planned time; `dropped_conflict` = it overlapped a measured line and was left out of the video, but any later burn includes it at its listed time, so retime or delete it before burning. Preview the `imputed` / `member_scaled` / `unaligned_planned` / `dropped_conflict` lines first, then the ones the user points at. Lines without `align_status` (titles, labels) keep their written time. `align_status` is copied as-is into your edited list, so once you change a line it no longer describes it.

2. Modify the `entities` array and `PUT` it back (**full replacement** — send the COMPLETE list; omitting a line deletes it, appending a new object adds one). Start from the GET response and change only the fields you mean to change: send every entity back, including `kind: "graphic"` layers (see below), and keep every `params` key you don't edit exactly as it came, even ones not listed here (the server writes some for its own use; dropping them changes how the line or layer is drawn).
3. `POST .../subtitles/preview` with a timestamp inside the edited line's `time_range` → returns `preview_url` (a single frame with the edits burned in). **Look at the frame** (download/view it) and iterate steps 2-3 until it's right.
4. `POST .../subtitles/burn` once at the end → a `subtitle_burn` task re-burns the whole video (it appears as an extra row on the source video's batch; poll it). When it completes, GET the asset again: each burn is saved as a new version with its own file and cover, and the asset's `file_url` / `thumb_url` now name it. A `file_url` you kept from before the burn still serves the earlier version, so don't reuse it. The burn task's own `output_video_url` (`GET /api/tasks/{task_id}`) is the same new file.
5. Wrong turn? `DELETE .../subtitles/edits` resets to the machine baseline (the original alignment) — free and instant.

**Entity shape** (each item in `entities` is one subtitle line, or a graphic layer):

| Field | Editable | Notes |
|------|------|------|
| `id` | keep | Stable line id; invent a new unique id for an added line |
| `kind` | no | `"subtitle"` for a caption line; `"graphic"` for a graphic layer burned in the same pass (a card, logo, sticker or picture copied from the template or the product). Add lines as `"subtitle"` |
| `time_range` | ✓ | `[start_sec, end_sec]` — retime a line here |
| `params.text` | ✓ | The on-screen text. Emoji in it are burned in color on videos made from 2026-09-30 on; on older videos they are left out of the burn, so don't add emoji to an older video's lines |
| `params.position_x_ratio` / `params.position_y_ratio` | ✓ | Normalized 0-1 position (0.5/0.8 ≈ bottom-center); same value works across resolutions |
| `params.color` | ✓ | `#RRGGBB` or a basic CSS colour name (`gold`, `red`, …); stored as hex; a value that isn't a hex code or a known name is removed on `PUT` |
| `params.highlight_words` | ✓ | Words / phrases to accent inside this line — each must occur verbatim (same case) in `params.text`. Keep them in sync when you rewrite the text: when you `PUT`, an entry that doesn't occur in `params.text` (or that is the whole line) is removed. Check the returned `entities` |
| `params.highlight_color` | ✓ | Accent colour for `highlight_words` — `#RRGGBB` or a name; one accent per line (omit → gold) |
| `params.approximate_size` | ✓ | One of `very_small` / `small` / `medium` / `large` / `very_large` |
| `params.align_status` | no | How the baseline timed a spoken line (see step 1); stale once you edit the line |
| `semantic` / `attributes` | keep | Pass through unchanged |

**Graphic layers** (`kind: "graphic"`). They carry no `params.text`, and they are part of the list the burn draws, so a PUT that leaves one out deletes it from the video. You can retime one (`time_range`) or delete it on request; leave its other `params` as they are. Its image keys (`params.source_crop_url`, `params.edited_asset_url`, `params.image_url`) can't be changed: a PUT that points a layer at any other file is rejected (400).

#### `GET /api/assets/{asset_id}/subtitles`

Returns `{source, entities, video_url, language, has_baseline, has_edits}`. `source` = `"edited"` whenever saved edits exist, else `"baseline"`, and `has_edits` says the same. Every PUT saves the edits and they stay after a burn, so `"edited"` does NOT mean "not burned yet"; only `DELETE .../subtitles/edits` clears them (after that, GET shows the baseline, or 404s if the video never had one). 404 = no caption layer recorded yet (an older video, a render without subtitles, or a swap with nothing burned): see reconcile below. After reconcile, a video with nothing burned returns 200 with an **empty** `entities` list. You can still ADD lines: PUT new entities, preview, then burn. PUT works without a baseline, but skip reconcile only for a video generated without subtitles: burn starts from the video without subtitles, so any line missing from your list disappears from the video.

#### `PUT /api/assets/{asset_id}/subtitles`

**Body:** `{entities: [...]}` — the complete replacement list, checked against the burn contract. A 400 means an entity has the wrong shape (a `kind` other than `"subtitle"` / `"graphic"`, a missing `id` / `semantic` / `time_range`, a wrong type) or a graphic layer's image key changed, and says what to fix. Style values the burn can't use are removed instead of rejected: an unrecognized `color` / `highlight_color`, a `highlight_words` that isn't a list of strings, or entries not found in `params.text`; compare the returned `entities` with what you sent. `params.font` isn't supported (there is no per-line font) and is removed on save. Other values (e.g. `approximate_size`) aren't checked here, so stick to the listed options. Saving does NOT change the video — only `burn` does.

#### `DELETE /api/assets/{asset_id}/subtitles/edits`

Reset to the machine baseline. Idempotent; returns `{reset, source}`.

#### `POST /api/assets/{asset_id}/subtitles/preview`

**Body:** `{t: <seconds>}`. Renders ONE frame with the current effective subtitles; returns `{preview_url, t}` (GET `${BASE_URL}${preview_url}`). Synchronous (~1-2s). Rate limit 20/min → 429 means slow the loop down.

#### `POST /api/assets/{asset_id}/subtitles/burn`

No body. Submits a `subtitle_burn` task (free) → `{task_id, batch_id, status}`. 409 = a burn for this asset is already running (poll it instead of resubmitting). Rate limit 6/min. Prefer many previews + ONE burn over burning per tweak.

#### `POST /api/assets/{asset_id}/subtitles/reconcile`

No body. Records the caption layer for a video that has none stored, from its script: an older video, or one with nothing burned (a render without subtitles, or a swap without added captions; for these it records an empty list). Returns `{status: "queued", task_id}`, or `{status: "exists"}` when data is already there. 404 = this video has no script on record and can't be edited. Rate limit 3/10min.

---

### Billing & balance

> **Billing rules (use this framing when explaining to users)**: charged only by **successfully generated video seconds**, at the rate of the tier that rendered them; on MiniMax H3, a render that carries more than 5 reference images (character, product and other pictures) also bills each image past 5: **16** display credits at 768P, **20** at 2K (`extra_image_credits` per engine in `GET /settings` → `video_backends`; quotes cover seconds only, the image count is known only once it renders). **Customer-facing numbers are DISPLAY CREDITS = internal credits ÷ 100** (the unit the app's wallet shows; never re-price a credit in dollars). Display rates: Seedance 2.0 480p **50/s** (internal 5,000) / 720p **100 credits/s** (10,000) / 1080p **250/s** (25,000); Seedance 2.5 480p **75/s** / 720p **150/s** (premium sibling engine, keyed `seedance25:480p` / `seedance25:720p` in the rate map); Seedance 2.0 Fast 480p **40/s** / 720p **80/s** (`seedance_fast:*`); MiniMax H3 768P **40/s** (internal 4,000, launch pricing) / 2K **80/s** (8,000). No 1080p on 2.5 or Fast. The engine is the user's choice at submit (`video_backend`), so **a cheaper engine is a real lever** when someone is short on balance — offer it before offering an upgrade. **analysis is free** (re-riffing the same source reuses the cached analysis); **you pay only for video seconds actually generated** — a run that produces no video output costs nothing, but any seconds already rendered (including on cancel or a later-stage failure) are charged and not refunded. One standard 15s video bills **from ≈600 display credits** at standard quality (MiniMax H3 768P, 40/s → 600; Seedance 2.0 720p 100/s → 1,500 = 150,000 internal). 480p is draft quality and cheaper than 720p on Seedance (Seedance 2.0 Fast 480p 40/s → 600, Seedance 2.0 480p 50/s → 750). **The signup trial covers at least one free 15-second video on the free default** (its size is a runtime setting: read the user's balance, never assume a number). A free-tier wallet may render on Seedance 2.0 Fast 480p or Seedance 2.0 480p (480p only; MiniMax H3 needs a plan). The default is Seedance 2.0 Fast 480p in every mode; it is also the cheapest free swap (50/s, vs 60/s on Seedance 2.0 480p). Where Fast isn't offered, the default is Seedance 2.0 480p. Every other engine or tier needs a plan (see `video_backend`). When the user asks what a video costs: BEFORE they pick an engine, give the "from" floor + the rate list; AFTER they pick, give their engine and resolution's exact per-second rate (no "from"). Give a total only from the server, never from your own arithmetic: `GET /api/riffs/quote` for an adapt or swap riff (exact for a template in one ratio, "about" for a new link, an upload or more than one ratio), `GET /api/creation/quote` for a creation video (exact for a fixed length; "up to" for a smart one, whose length follows the content), `credits_per_ratio` for extra ratios of a video you already have. Subscription credits are valid for the period and don't roll over. **Plan prices are in USD and exclude tax** — where the customer's region is taxable, Stripe adds it at checkout (business customers can enter a VAT/tax ID there for reverse charge), so when you quote a plan price, say "plus any applicable tax". Get exact rates from `GET /api/billing/subscription` — `video_credits_per_second` is the 720p base and `video_credits_per_second_map` has every tier; never hardcode either. **Swap mode and reframed extra ratios** carry the source video as a reference in every render, so they have their own per-second rates: Seedance 2.0 480p **60/s** / 720p **120/s** / 1080p **300/s**; Seedance 2.5 480p **90/s** / 720p **180/s**; Seedance 2.0 Fast 480p **50/s** / 720p **100/s**; MiniMax H3 768P **80/s** / 2K **160/s**. Adapt and creation videos always bill the plain rates above. A swap also rounds up to whole seconds per render window (minimum 4s). For a swap's price use `GET /api/riffs/quote` with `mode=swap` (`swap-quote` gives the same number for one video): exact for a source that fits one render window, up to 1s more per extra window for a longer one (see `POST /api/riffs` → Swap specifics).

**402 handling (hard constraint):** when submit (`riffs` / `pipeline/batch`) lacks balance, it returns **HTTP 402** with a structured `detail`:

| Field | Notes |
|------|------|
| `error` | always `"insufficient_credits"` |
| `required_credits` / `available_credits` | INTERNAL credits — **divide by 100** for the display credits the app shows (below); never shown to the user raw |
| `topup_url` | **the upgrade link the backend issues — relay it verbatim, don't build a URL yourself** |

On 402: **no retry, no silent failure** — present the shortfall in **display credits ONLY** (the unit the app shows users — never raw internal credits, never USD): `display_credits = internal ÷ 100`, e.g. "this riff needs ~1,500 credits but you have ~800 left." A cheaper engine is a real lever here (MiniMax H3 renders at 40/s vs 100/s at 720p) — offer it before offering an upgrade. (For a free-tier wallet only its free pairs count: Seedance 2.0 Fast 480p and Seedance 2.0 480p — Fast 480p is the cheaper of the two. Past those a plan is the way forward; the first payment unlocks every engine.) Relay `topup_url` verbatim, and optionally call `GET /api/billing/plans` to introduce plans. Only some changes help right now: a first plan (or a new one after an old plan ended) adds its first month's credits as soon as the payment clears; moving up a tier on the same billing interval (including Studio's bigger credit amounts) adds the difference between the two tiers' monthly allotments for what's left of the current month as soon as the upgrade payment goes through (if the bank asks the user to confirm it, nothing changes and nothing is charged or added until they do; on a yearly plan the higher allotment then arrives with each later monthly refresh); switching between monthly and yearly, or moving down a tier, takes effect at the end of the current period and adds nothing today (see Yearly mechanics). Apart from the check before a retry and a quote that doesn't fit (`fits: false`, see Step 3), this is the **only time you bring up the balance unasked.**

#### `GET /api/usage/credits` — check balance

| Field | Type | Notes |
|------|------|------|
| `available` | float | **Available credits, RAW INTERNAL** (= `total_remaining - held`) — the only field for "can I submit". **Every number in this response is raw internal credits: ÷ 100 before saying it to the user** |
| `held` | float | Total held by in-flight tasks |
| `total_remaining` | float | Total unspent credits (including held) |
| `daily_spent` / `daily_limit` | float | Settled spend today (since 00:00 UTC) / daily cap (`0` = unlimited). The daily-limit check at submit also counts today's holds of tasks still running |
| `ledgers` | array | Per-batch detail (`type` / `total_credits` / `remaining_credits` / `held_credits` / `expires_at`; raw internal like every number here); the earliest-refreshing ledger is always spent first, transparently to the agent (to users say "refresh" / "this month", never "expire") |

> In a team scope this returns the owner's balance (shared by members); `daily_spent`/`daily_limit` are computed for the calling member's own daily allowance.

#### `GET /api/billing/plans` — plan catalog

No params. Returns `[{id, tier, family, interval, name, price_usd, monthly_price_usd, credits, videos, purchasable, savings_percent, first_month_offer_applies}]` (`purchasable=false` = payments not configured). Three plans (Lite, Creator, Studio), and Studio comes in three monthly credit amounts (`family: "starter"`, all named "Studio"). Each is sold **monthly or yearly**; the yearly entry carries the same monthly credit allotment at a lower per-month price:

| name | monthly id | monthly | yearly id | yearly, per month | billed yearly | saves | credits a month (wallet) |
|---|---|---|---|---|---|---|---|
| Lite | `lite` | $15/mo | `lite_year` | $12/mo | $144/yr | $36 | 3,000 |
| Creator | `solo` | $39/mo | `solo_year` | $29/mo | $348/yr | $120 | 8,000 |
| Studio | `starter` | $99/mo | `starter_year` | $79/mo | $948/yr | $240 | 22,000 |
| Studio (70,000) | `studio_2` | $279/mo | `studio_2_year` | $223/mo | $2,676/yr | $672 | 70,000 |
| Studio (220,000) | `studio_3` | $799/mo | `studio_3_year` | $639/mo | $7,668/yr | $1,920 | 220,000 |

The ids keep their original spelling (Creator is `solo`, Studio is `starter`; the bigger Studio amounts are `studio_2` / `studio_3`): match on `id` / `tier`, say `name` to the user, and name a Studio amount with its credits ("Studio with 70,000 credits a month") since all three are called Studio. `savings_percent` is how much cheaper per credit it is than the 22,000 Studio on the same interval (11 / 19). Those ids are what the web checkout and the change-plan flow take; a deployment with no price configured for an entry still returns it, with `purchasable: false`. Never offer a plan whose `purchasable` is false. **Introducing a plan is a pre-payment money moment: lead with dollars** (`monthly_price_usd`/mo, e.g. "$79/mo, billed $948 yearly"), then what it buys as credits + a videos range ("22,000 credits · 14-36 videos a month"). The low number is the plan's `videos` (15-second videos at the default engine's 720p rate). The high number isn't in the response: it is floor(`credits` ÷ 15 ÷ the cheapest rate among the (engine, resolution) pairs this deployment offers, **excluding 480p**, which is draft quality and never counted); take the pairs from `GET /api/settings` → `video_backends` and price each from `video_credits_per_second_map` (`engine:resolution` key first, then the bare resolution). Engine names only in rate lists, never the sentence subject; `credits` is RAW INTERNAL (÷ 100 for the wallet number), and never re-price credits in dollars.

**Yearly mechanics an agent must relay correctly:** a yearly plan bills once but **credits arrive monthly, not all at once**. It is the same allotment as that tier's monthly plan, refreshed at each monthly mark of the year and not rolled over. So yearly buys a lower price, not a bigger pile. **Yearly is non-refundable.** Switching: moving **up a tier while staying on the same billing interval takes effect as soon as the prorated payment goes through** (usually at once; if the bank asks the user to confirm the payment, after they do). **Everything else takes effect at the end of the current period**: switching between monthly and yearly in either direction, moving down a tier, or canceling. Until then the current plan keeps running.

#### `GET /api/billing/subscription` — current plan

No params. Returns `{plan_id?, plan_name?, plan_credits?, can_upgrade, upgrade_plan_id?, status?, scheduled_plan_id?, cancel_at_period_end, current_period_start?, current_period_end?, stripe_enabled, credits_display_scale, video_credits_per_second, video_credits_per_second_map, first_month_offer_percent?}`. `first_month_offer_percent` is set only for a payer who has never subscribed, while a first-month offer runs: that percent comes off the first invoice of a **monthly** Lite, Creator or 22,000-credit Studio plan (`first_month_offer_applies` in the catalog; yearly and the bigger Studio amounts excluded), regular price from month two; null otherwise. Mention it when the user is deciding whether to subscribe. `plan_credits` is the plan's monthly credit allotment (null when unsubscribed). `can_upgrade: false` means the account is already on the largest plan offered (Studio with 220,000 credits a month): when credits run short, point the user to team@riffkit.ai for more volume (or a cheaper engine) instead of suggesting an upgrade. Otherwise `upgrade_plan_id` names the next step up on the same billing interval (Studio 22,000 → 70,000 → 220,000). `plan_name` is "Studio" for all three Studio amounts: use `plan_credits` to say which. `video_credits_per_second` is the Seedance 2.0 720p base rate; `video_credits_per_second_map` holds every tier's rate, keyed by plain resolution for Seedance 2.0 (`720p`/`480p`/`1080p`) and MiniMax H3 (`768P`/`2K`) plus engine-scoped keys for the sibling engines (`seedance25:720p`, `seedance25:480p`, `seedance_fast:720p`, `seedance_fast:480p`): look up `<engine>:<resolution>` first, then the plain resolution. All of these are raw internal credits: divide by `credits_display_scale` (100) for the number the wallet shows. `plan_id=null` = unsubscribed; `plan_id` / `scheduled_plan_id` may be a yearly id (`lite_year`, `solo_year`, `starter_year`, …); and on a yearly plan `current_period_end` is the end of the paid YEAR (the monthly credit refresh happens inside it). **Buying/upgrading/downgrading is a web action** (Settings → Billing); the agent only guides, never orders.

**Pending change fields.** `scheduled_plan_id` non-null = a change already takes effect at `current_period_end` (a tier-down, or a monthly↔yearly switch; both are period-end changes); until then the current plan keeps running and its credits keep refreshing. `cancel_at_period_end: true` = the plan ends at `current_period_end` and is not renewed. Both are states to *report*, not to act on: say what changes and when, using `current_period_end`.

#### `POST /api/billing/cancel` · `POST /api/billing/resume` — end or keep the plan

No body. **Payer-only** (in a team scope, only the owner who pays; anyone else gets 403). `cancel` sets the plan to end at `current_period_end`: nothing is charged again, and the plan and its credits keep running until then. A pending **monthly↔yearly switch is dropped** by the cancel, so `scheduled_plan_id` comes back null; a pending **same-interval tier-down stays scheduled** and `scheduled_plan_id` keeps its value, but it never bills, because the subscription ends at `current_period_end`. Either way the plan simply ends on the plan the user is on today. Yearly is non-refundable: canceling a yearly plan stops the renewal, it does not refund the year or stop the remaining monthly credit refreshes. `resume` undoes a cancel before the period ends, putting the plan back on renewal. Both return the same shape as `GET /api/billing/subscription` (the subscription re-read after the change), so read `cancel_at_period_end` / `current_period_end` / `scheduled_plan_id` back from the response rather than assuming (a non-null `scheduled_plan_id` next to `cancel_at_period_end: true` is the tier-down case above, not a failed cancel).

Usage: these are the only billing actions an agent may take, and only on an explicit, unambiguous instruction ("cancel my plan"). **Confirm first, quote the date it ends from `current_period_end`, and never cancel as a side effect of some other request.** Upgrades, downgrades and checkout stay web-only.

> Also available: `GET /api/usage/daily-budget` (`allowed`/`spent_credits`/`limit_credits`/`remaining_credits`, the simple pre-submit gate; `spent_credits` includes today's holds of videos still rendering, as the submit's daily-limit check does), `GET /api/usage/summary` (usage aggregated by period: `total_credits`; ignore `total_cost_usd`, which is internal cost; `groups` is empty for customers. Its periods are rolling windows, `today` = last 24 h, `week` = last 7 days, `month` = last 30 days, and they cover the whole scope, so in a team scope it's the team total, not the caller's own spend; for a calendar-aligned span pass `since=YYYY-MM-DD` (UTC midnight) and an optional `until` instead of `period`), `GET /api/usage/history` (per-day rows for your own usage; team owners/admins can pass `user_id`. It has **no credit figures**: `cost_usd`/`cost_cny` are internal cost and `call_count`/tokens are ops detail, so never relay those; its only customer-facing number is `video_seconds`, the seconds rendered that day). Use credits `daily_spent` for "how much have I spent today," summary for longer spans, credits `available` for "can I generate again." **Always report usage/spend to customers in display credits** — the unit the app's wallet shows — `display_credits = internal_credits ÷ 100`; never surface raw internal credits / USD. Real video DURATION stays in seconds (it is time, not balance). This matches the app's credits wallet + brand voice.

---

### Team (optional)

#### `GET /api/scopes/{scope_id}/members`

List scope members (you must be a member, else 403). Returns `[{id, scope_id, user_id, role, daily_credits_limit, joined_at, user_email}]`. Use it to resolve `TaskOut.submitted_by_user_id` to a `user_email` in a team scope. Not needed in a solo scope.

---
