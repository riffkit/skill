## Task state machine

| State | Meaning | Keep polling? |
|------|------|----------|
| `queued` | Submitted, waiting for a TaskRunner slot | ✅ |
| `running` | Executing | ✅ |
| `completed` | Output persisted; `result` carries asset_id | ❌ (fetch assets) |
| `failed` | Normal failure (LLM error / API rate limit / …); `error` has the cause | ❌ (no auto-retry) |
| `dead` | Stopped by an interruption it couldn't recover from on its own: a template analysis or a subtitle burn/reconcile cut off by a server restart, or a riff / creation / swap interrupted over and over. A riff, creation or swap caught by a single restart is NOT dead: it picks up where it stopped, with no extra credits, so keep polling while it shows `queued`/`running` | ❌ (offer a retry, available within 24 h of submission) |
| `cancelled` | User cancelled | ❌ |

```
queued → running → completed
                 ↘ failed / dead / cancelled
```

---

## Common errors

| HTTP / error | Scenario | Handling |
|-------------|------|------|
| `401` unauthenticated | vee_session expired/missing | Re-run the device flow (`POST /api/skill/device/authorize` → user approves → poll `.../token`); see **Auth** |
| `402` insufficient_credits | not enough to submit | Show the shortfall in display credits (internal ÷ 100) + relay `topup_url` verbatim, **no retry** |
| `400` — not exactly one source | missing or multiple sources | Ensure exactly one of `video`/`tiktok_url`/`formula_id`/`upload_id` |
| `400` — "This template needs an update before it can be used. …" (header `X-Refusal: template_outdated`) | `formula_id` names a template whose analysis is out of date (`analysis_prompt_is_latest=false`), on `POST /api/riffs`, `POST /api/pipeline/batch` or a quote; nothing created or billed | Your own template: `POST /api/formulas/{id}/refresh-analysis`, wait for it, then submit. A public one: pick a current template, or riff the original from its TikTok link |
| `400` — `detail.error == "character_avatar_not_ready"` | a picked character's current avatar is still in review or was rejected (`reviewing` / `rejected` list the names), on any riff, swap or creation submit; nothing created or billed | Relay `message`. In review: wait about a minute and submit again. Rejected: another character, or the user switches to an approved avatar or uploads a new one on the Characters page |
| `400` — "A swap needs at least one change: …" | `mode=swap` with no character, no product with images and an empty `content_anchor` | Ask what should change: a character to put in, a product to place, or a written change |
| `400` — "This video shows no person to replace: …" | `mode=swap` naming only a character, from a template that shows no person | Offer a product with images or a written change, or another source |
| `400` — video can't be used for a swap | `mode=swap` from a template that has no source video | Offer another template, or a new upload/link |
| `400` — "Swapping one of your own finished videos is not available. Download the video and upload it as the source." | the request named one of the user's finished videos as the source (`source_asset_id`, a retired parameter: any value, in either mode, on `POST /api/riffs` or a quote); nothing created or billed | Send it without `source_asset_id`. Tell the user to download the video and upload it as the source (`video`), or offer a template or a TikTok link |
| `400` — source video too long | the uploaded file, or a TikTok link whose length could be read at submit, runs longer than `max_render_duration` (the message states both numbers); in swap mode, also any template over the cap | Ask the user for a shorter video, or to trim it and upload the trimmed file |
| `400` — "Only TikTok links are supported." | `tiktok_url` isn't on tiktok.com / www.tiktok.com / vm.tiktok.com / vt.tiktok.com, or it carries a port, a login part or a backslash | Ask the user for the TikTok share link of the video (Share → Copy link) |
| `400` — TikTok link is not a specific video | `tiktok_url` points at a profile, photo post, Shop product page or live instead of one video: on tiktok.com the path has no `/video/` and isn't a `/t/` share link; for a `vm.`/`vt.` short link, this is where it redirects | Ask the user for the link of **one video**: one containing `/video/`, a `tiktok.com/t/…` share link, or a `vm.`/`vt.` short link |
| `400` — required missing | name/description etc. not sent | Fill per the field tables; don't paper over with empty strings |
| `400` — invalid language | a code not in the candidates | First `GET /api/languages` for candidates |
| `400` — "`<field>` is not UTF-8 — it arrived as legacy-encoded bytes (GBK/Big5/Shift-JIS)…" | a multipart text field (`content_anchor` / `user_hint` on `POST /api/riffs`; the image's `name` / `description` / `usage_context` on `POST /api/products/{id}/images`; `name` on `POST /api/characters`; `name` / `user_hint` on `POST /api/formulas/analyze`; `name` / `notes` on `POST /api/assets/upload`) was typed into a non-UTF-8 console (Windows CJK default), which re-encoded it before curl sent it | Do **not** resend the same command: it fails the same way, and `chcp` alone doesn't fix it. Write the text to a UTF-8 file and pass it by reference: `-F "content_anchor=<'/tmp/anchor.txt'"` (see `POST /api/riffs`). Already doing that? Rewrite the file with an explicit UTF-8 encoding. Never switch a multipart endpoint to `json=`: its fields would be ignored |
| `400` — "There was an error parsing the body" | a JSON body (e.g. `POST /api/products`) was not UTF-8 | Send JSON with your library's UTF-8 encoder (`requests.post(url, json=…)`, `fetch`/`axios`, `json.Marshal`); on Chinese Windows `cmd` run `chcp 65001` first; never build the body by hand with `data=` |
| `422` — request validation | a JSON body without a required field (e.g. `creation/batch` without `content_anchor`, or with it empty or only spaces); a wrong type or an unsupported value (e.g. `product_visibility` / `duration_mode` outside the listed values, `duration_seconds` outside 4-45, `duration_mode=fixed` without `duration_seconds`); `content_anchor` / `user_hint` over 5000 chars | `detail` is a list of `{loc, msg, type}`: fix the field named in `loc` using the field tables, and don't resend the same body. A misspelled **optional** field gets no error at all (it's ignored), so check field names against the tables |
| `413` file too large | over 100MB video / 50MB image | State the limit, recompress, re-upload |
| `409` `upload_used` (with `formula_id` / `batch_id`) | `upload_id` on `POST /api/riffs` or a quote, for an upload already submitted once; nothing created or billed | Don't make a new link: follow that `batch_id`, or for another video from the same source send that `formula_id` once the template reads `analyzed` |
| `409` — the video hasn't arrived / is being used by another submit (`upload_id`) | the upload link's page has no video in yet, or another submit of the same upload is running | Not arrived: ask the user to finish on the page, then `GET /api/riffs/uploads/{upload_id}`. In use: wait for that submit; don't send it twice |
| `410` — the upload is gone (`upload_id`) | the link or its video ran out, or the account ended its links ("Sign out other devices", an assistant disconnected) | Make a new link (`POST /api/riffs/uploads`) |
| `429` on `POST /api/riffs/uploads` | 10 unused uploads have a video in or arriving, or more than 6 links in 10 minutes | Use one of the uploads already in (`GET /api/riffs/uploads/{upload_id}`), or wait; don't loop |
| `409` `price_changed` on `POST /api/assets/{asset_id}/continue` | the price or the video's progress changed since you quoted it; nothing started | Quote the new `credits` (÷100) and ask again |
| `409` `confirm_needed` on `POST /api/assets/{asset_id}/continue` | the body had no `credits` or `delivered_through`; nothing started | Quote its `credits` (÷100), get the go-ahead, send both |
| `409` `film_busy` / `film_complete` on `POST /api/assets/{asset_id}/continue` | part of the video is being made now / nothing is left to make | Busy: follow its batch and offer the next step when it's done. Complete: nothing to continue |
| `409` `film_pending` on a subtitle `PUT` / `DELETE` / `burn` / `reconcile` | the video is made in sections and sections are still left | Captions wait for the whole video: continue it first, or leave them |
| `410` `continue_expired` on `POST /api/assets/{asset_id}/continue` | past the video's `staged.finish_by` | Only a new video can be made |
| `400` `not_sectioned` / `action_unavailable` / `invalid_action` on `POST /api/assets/{asset_id}/continue` | not a video made in sections, that action has no price now (e.g. `redo` before anything was delivered), or `action` isn't `next` / `rest` / `redo` | Read the video's `staged` block and offer only an action in `staged.prices` |
| `403` `first_section_only` (`error` `subscription_required`) on `POST /api/assets/{asset_id}/continue` | an account held to the first section asked for `next` / `rest` | It can only `redo` the first section; handle as `403` subscription_required (Billing & balance) |
| `403` `one_at_a_time` (`error` `subscription_required`) on a submit, a retry, a continue or a ratio backfill | a free-tier account already has a video in the making | Nothing started. Say a video is in progress; once `GET /api/tasks` shows it done, submit again (handle the plan side as `403` subscription_required, Billing & balance) |
| `409` `film_delivered` on `POST /api/tasks/{task_id}/retry` | the first render of a video made in sections failed after it had delivered a section: a retry would replace the video | Continue the video instead (`POST /api/assets/{asset_id}/continue`) |
| `410` on `POST /api/tasks/{task_id}/retry` (`detail` always Chinese) | over 24 h since the task was first submitted, or a riff / swap submitted before a Riffkit update that changed how riffs are built; nothing restarted or billed | Say in the user's language that this task is too old to retry; offer a fresh submit of the same kind with the same options (see `POST /api/tasks/{task_id}/retry`) |
| `409` on `POST /api/tasks/{task_id}/retry` (`detail` always Chinese) | the task's previous run hasn't finished shutting down | Wait about a minute, then retry once; still `409` → tell the user and check back later |
| `400` on `POST /api/tasks/{task_id}/retry` (`detail` always Chinese) | the task isn't `failed`/`dead` (cancelled, completed, or already restarted by an earlier retry); nothing restarted or billed | Read the task's status and poll it; don't submit again |
| `429` — `detail` starts with 请求过于频繁 (always Chinese) | more than 10 submits in 60 s (counted separately for `POST /api/riffs`, `/api/creation/batch` and `/api/pipeline/batch`) | Wait about a minute, then submit once; don't loop |
| `429` — `detail.code == "server_busy"` (header `Retry-After: 30`) | the servers are at capacity (any riff, creation, pipeline batch or backfill submit); nothing was created or billed | Tell the user the servers are busy, wait about 30 s, then submit once more; if it happens again, suggest trying later |
| `429` — daily limit reached (`detail` names the limit and today's spend, already in credits) | today's spend has reached the daily cap (`daily_limit` in `GET /api/usage/credits`) | Relay the message. The cap resets at 00:00 UTC; in a team, the team owner can raise a member's cap; for a personal account, or a team owner's own cap, the user contacts Riffkit. Don't resubmit until the cap is raised or the day rolls over |
| `429` — `detail.error == "free_cost_limit"` | this account's model spend that produces no video in the last `window_days` (analysis, subtitle alignment, automatic image descriptions and the like) is over its current allowance; it is checked when you start an analysis (a riff from a new upload or TikTok link, `POST /api/formulas/analyze`, `refresh-analysis`) | Not a short wait: offer to riff an already-analyzed template (`formula_id`). The allowance grows as the account generates paid videos. Its numbers are internal credits (÷ 100 for display) |
| `500` / timeout | server error | Say try again later; if it recurs, report to the developers |
| Task `failed` + error mentions "Seedance" | proxy / API failure | Surface the specific error, let the user decide |
| Task `failed` + error says the video is ~Ns, over the Ms limit | a TikTok link whose length couldn't be read at submit turned out too long after download (riff or swap; nothing billed) | Same as the 400: ask for a shorter video, or a trimmed upload |
| Swap task `failed` + `error` starts with 这条原片里没有可替换的人物 | only a character was named, but the source shows no person (nothing billed; checked before any review or render) | Offer a product with images or a written change, or another source |
| Swap task `failed` + `error` starts with 这次翻拍没有指定任何改动 | nothing to change was left by the time the task ran, e.g. the product lost its images (nothing billed) | Offer a product with images, a character, or a written change |
| Swap task `failed` + `error` names a window's seconds (原视频 A–B 秒) and a code in parentheses | the video vendor refused that source clip, in content review (没有通过平台的内容审核) or for its format (格式不符合视频引擎的要求, code `InvalidParameter.*`); nothing billed | Restate the message in the user's language (the `error` text is always Chinese; keep the code verbatim); offer another source. Retrying the same source fails the same way |
| Task `queued` over 2 min | the servers are busy | Say "the servers are busy, your video will start as soon as a slot frees up" |

---
