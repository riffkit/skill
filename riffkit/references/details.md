## Details by step

What a step of **The flow** needs beyond what it says there, for an agent that makes the calls itself (the CLI or HTTP). The routes are in "API reference".

### Mode (step 0)

| Mode | `mode` | What stays | What changes | Pick it when |
|---|---|---|---|---|
| **Adapt** | `adapt` (also what the API runs when `mode` is omitted) | The emotion formula: hook, rhythm, beats | The story, scenes, script, language | The user wants *their own* video that works like the winner |
| **Swap** | `swap` | The source's camera, cuts, framing, action, timing, sound and frame shape | What the user names: the person (your character, if you pick one), a product, and whatever `content_anchor` names: the setting, an outfit, a line's wording | The user wants *this* video with their character in it ("the same video, but me", "keep every shot") |

Swap rules (backend-enforced):
- **A swap must change at least one thing**: a character (`character_ids`), a product that has images (`product_id`; a product without images changes nothing), or a non-empty `content_anchor`. None of the three → 400 whose `detail` is a plain localized sentence (en: "A swap needs at least one change: …"; the body carries no error code, so relay `detail` rather than matching on it). Checked for every swap source, before anything is analyzed or billed.
- **The character is optional.** With no character the source's own person stays (their real face is in the output); there is no Auto person in swap. One task per character, like adapt; no character = one task. A picked character needs an approved avatar (`has_any_active_avatar=true`), same as adapt. If the user wants a *different* person, recommend picking a character: a person changed only by words in `content_anchor` has no reference image, so the face can differ between shots (and on Seedance 2.0 the voice stays the original's).
- **Whose voice changes.** On engines that change voices (Seedance 2.5, MiniMax H3), a replaced person gets a new voice only on the lines they speak on camera; narration (heard, not seen) keeps the source's voice. To change the narration too, say so in `content_anchor`, e.g. "the narration also in the new person's voice" (vague wording may not be picked up). To keep every original voice, say "keep the original audio".
- **Check the avatar before a paid swap with a character.** The swap takes the person's face, hair and build from the character's avatar image (`reference_image` in `GET /api/characters`; fetch `${BASE_URL}${reference_image}` with the session cookie, like a video's `file_url`). What works: one person, facing the camera, face large in the frame, plain background. The layout the Characters page recommends works too: one image with that person's chest-up close-up on the left and the same person head to toe on the right, same outfit (two large views, so the build and outfit are shown as well). What usually fails to replace the face in a close-up talking-head source is a sheet of many small poses, decorations or other people: the output keeps the original face and at most picks up the hair. When the avatar looks like that, suggest a new avatar in one of the layouts that work (uploaded on the Characters page, reviewed before it can be used) or another character, instead of retrying the swap.
- **A character only counts if the source shows a person to replace.** For a template source the analysis is already known, so a swap whose only change is a character, of a source with no person in it, → 400 whose `detail` is a localized sentence (en: "This video shows no person to replace: …"): offer a product with images or a written change instead. A new upload / TikTok link isn't analyzed yet at submit, so the same rule is applied after its analysis (see Swap specifics). Either way nothing is billed.
- **Never compressed**: the output is as long as the source, so the source must be within the render-duration cap (default 45s, see General constraints). A swap source's length is its **video stream's** length, measured the way the render engine measures it (a trailing audio tail doesn't count); for a template this can differ slightly from the analyzed length in `GET /api/formulas/{id}` → `extraction_summary.duration_seconds`. A longer source → 400 whose `detail` is a plain localized sentence stating both numbers (en: "This video is ~Ns, over the Ms limit. Please pick a video under Ms."; no error code in the body, so don't match on fixed text), including a template over the cap. For a template source, `GET /api/riffs/swap-quote` tells you the length, the price and whether it's over the cap before you submit (a source longer than one render window can bill slightly more than the quote; see Swap specifics).
- **Ignored in swap** (accepted, not used — no need to strip them): `language` (the source's own language is kept), `product_visibility` (a product is on camera or absent), `bgm_mode`, `video_ratios` (the source's frame shape is kept, one video per character). `user_hint` still feeds a new source's analysis.
- `content_anchor` means **"what to change"**: empty = only the picked character / product change. A product still needs to be attached (`product_id`) and, to show a specific image, named in the text.
- **Engine: Seedance 2.5 is the recommended swap engine** (it gives the best swap result). Read it from `GET /api/settings` → `swap_recommended_video_backend` (`seedance25`, or `null` when this deployment doesn't offer that engine: then recommend nothing). For a paid account it is also the swap default (an omitted `video_backend` lands on Seedance 2.5 720p); a free-tier swap lands on Seedance 2.0 Fast 480p, the free default in every mode and the cheapest free swap (50/s, vs 60/s on Seedance 2.0 480p), and a free-tier account still gets 403 on Seedance 2.5. When the quote's `fits` is false, offer a pair from its `alternatives`. Adapt mode has no recommended engine.
- In the app the two modes are labelled **Adapt** and **Swap** (zh 「改编」/「翻拍」); use those names when you point the user at the screen.
- A finished swap video can be reframed into extra **vertical** ratios with `POST /api/pipeline/backfill` (billed at the same swap / reframe rates below). A swap submits one video per character in the source's own frame shape, so `video_ratios` doesn't fan it out at submit.

### Source (step 1)

| Source | Param | When |
|---|---|---|
| **Analyzed template** | `formula_id` | The user wants an existing template, or has riffed this source before — **skips analysis, fastest** (analysis is free either way; skipping it saves the wait, not credits) |
| **TikTok link** | `tiktok_url` | The user dropped a viral link; the server auto-downloads the video + extracts BGM |
| **A file you can send** | `video` | The file is on this machine (≤100MB, and within the render-duration cap — see General constraints; a longer source is rejected, not trimmed) |
| **A file only the user has** | `upload_id` | The video is on the user's phone or computer: `POST /api/riffs/uploads` makes a link where they add it, and `GET /api/riffs/uploads/{upload_id}` tells you when it is `ready` |

- Template candidates: `GET /api/formulas?status=analyzed&template_type=pipeline`. `visibility=public` are platform-curated templates (usable across scopes, prefer recommending them). A template with `analysis_prompt_is_latest=false` can't be riffed or swapped: the quote and the submit refuse it with a 400 (nothing is created or billed). If it's your own template (`visibility=scope`), call `POST /api/formulas/{id}/refresh-analysis`, wait for that analyze task to complete (while it runs the template isn't `analyzed`, so a riff is rejected with 400), then riff. A `visibility=public` platform template can't be refreshed from your account (404): recommend a current one instead, or riff the original from its TikTok link or an upload (analysis is free).
- **The same TikTok link already analyzed with current analysis, in your scope or as a public template, is reused** (free, faster). The reused link acts like `formula_id`: `user_hint` is ignored and the response is `mode: "generate"`. If the only earlier analysis is stale, the link is analyzed fresh automatically; the agent needs no special handling.
- The sources are **mutually exclusive**; exactly one must be provided (else 400).
- A video the user already made with Riffkit can't be named as a source by its id. To swap it, the user downloads it and uploads the file as the source, like any other upload.

### Character, product, placement, language (steps 2 and 3)

Each can be left alone on its default; the agent may suggest where helpful but **never blocks**. (In swap mode language / visibility / ratios don't apply, and at least one change must be named: see Mode.)

**Character (default Auto)**
- By default `character_ids` is empty = **Auto mode**: no digital human bound, SD2 generates the on-camera person. This is the product default, not an edge case.
- **The agent may proactively pick/suggest a fitting character** — when the user expresses account/persona intent ("post it to my health account", "use my creator persona"), read `GET /api/characters` and match by `persona` feel + `gender` / `age_range`, then suggest one. **Only suggest characters with `has_any_active_avatar=true`** (a `false` character can't generate video yet: its current avatar is still in the automatic review, usually under a minute, was rejected, or it has no avatar. The user can wait, switch to an approved avatar from the character's history, retry the review, or upload a different image on the Characters page).
- If the user expresses no account intent, **proceed silently on Auto** — don't interrupt just to make them choose.
- Multiple characters: only pass several when the user explicitly says "make one for each of these characters" (one task per character).

**Product (default none)**
- By default `product_id` is empty = `no_product` mode: pure content, the caption never mentions a product name or product CTA, the whole video just runs the template's emotion formula. Good for growth / relatability / educational content.
- To place a product:
  - **Existing product** → `GET /api/products`, take the `product_id`.
  - **New product** → stage the fields (name / description required) in memory; **defer the real `POST /api/products` write until just before submit** (don't leave a half-baked product in the DB before the plan is settled).
- Product images: upload clean product photos / app screenshots (no watermark, no browser chrome, subject centered); at least one clean image noticeably lifts a placement. If the original has noise, the agent may crop/clean it before uploading (see `POST /api/products/{id}/images`). **Every image must have a `name`** — to put a specific image on camera, write that image's `name` directly in `content_anchor` text (see the content_anchor framework); an unnamed image can't be referenced.

**Visibility `product_visibility` (only meaningful with a product; default on_camera)**

| Value | Meaning | Best for |
|---|---|---|
| `on_camera` (default) | Product appears as a physical object on screen (character holds / scans / shows it) | Food / cosmetics / small physical goods / packaging as the core hook |
| `off_camera` | Product never enters frame; conveyed only via subtitles / voiceover / caption text | Apps / websites / SaaS / services / non-portable goods |

When `product_id` is empty this field is ignored and the backend derives `no_product`. **The caller may not pass `no_product` directly** (only the two literals on_camera / off_camera are accepted). The script and visual staging differ greatly across modes, so when a product is bound always state the value and the reason at the confirmation step.

**Language (default en)**
- Candidates from `GET /api/languages` (currently `en` / `es` / `pt` / `id` / `de` / `fr` / `it` / `ja` / `zh-CN`, in picker order). Trust the endpoint, don't hardcode.

**content_anchor (optional creative direction) + user_hint (optional hook hint)**
- `content_anchor` is the agent's highest-value contribution: it may proactively draft one for the user to review (see `## content_anchor drafting framework`). If the user doesn't want one, leave it empty — the video still generates.
- `user_hint` feeds only a **new source's** analysis ("this popped off on the twist at 0:03"); it's ignored when a `formula_id` is chosen, so don't send it then.

### Price and plan (steps 5 and 6)

Restate the plan with its price from `GET /api/riffs/quote`, asked with the same mode, source, engine, tier, character count, (adapt) ratio count and delivery you are about to submit. Mention the balance only when the quote's `fits` is false, and then offer an engine from `alternatives` that fits (or a template from `fitting_templates`):

```
Ready to riff:
├── Mode: [Adapt / Swap]
├── Source: [template name / TikTok link / the user's video]
├── Character: [name / Auto (AI-generated person); swap: a name / keep the original person]
├── Product: [name + visibility / none]
├── Language: [en / es / pt / id / de / fr / it / ja / zh-CN; swap: the source's own]
├── Price: [quote `credits` ÷ 100, already the whole batch (one video per character; one with no character or when keeping the original person); "about" when `exact` is false, when you asked for more than one ratio (each extra ratio is re-priced from the finished video), or for a swap source longer than one render window. Made in sections: the first section's price, and about the whole (`sections_estimate.whole_credits` ÷ 100). No number when `source_seconds` is null (`credits` is then a minimum, not a price): say the length couldn't be read and the charge follows the real length; if `probe` is `busy`, ask the quote again shortly. Same for a local file whose length you can't measure]
└── content_anchor: [drafted creative direction / none; swap: what changes besides the person]
```

When the user says "submit / generate / riff" → call `POST /api/riffs`.
- If a **new product** was chosen, first `POST /api/products` (+ upload images serially) to get the `product_id`, then include it in the riff.
- Insufficient balance returns **HTTP 402** (structured `insufficient_credits`) → handle per "Billing & balance".
- A submit can also get **HTTP 429** with `detail.code == "server_busy"` (and a `Retry-After: 30` header) when the servers are at capacity. Nothing was created or billed: wait about 30 seconds, then submit once more. Other 429s are rate or daily limits (see Common errors).

### Progress (step 8)

- The whole riff shares one `batch_id` (the analyze task and the chained generation task both carry it) → poll `GET /api/tasks/batch/{batch_id}`.
- Every **30 seconds**; cap a single poll loop at **15 minutes** (pipeline tops out around 8 min, 2× tolerance), then pause and tell the user.
- **Swap on a Seedance engine** first sends each source clip through the video vendor's content review before any rendering starts; the first swap of a source can wait several minutes there. Verdicts are remembered per clip content, so later swaps of the same, unchanged source reuse them (a clip already refused fails the task at once, without a new review); if the source file itself changed, its clips are reviewed again. If the review refuses a clip (or the video engine refuses its format), the task fails **before any video second is billed** and the `error` names the window's seconds and a code in parentheses. That `error` is a fixed Chinese sentence whatever the request language: restate it in the user's language (keep the code verbatim) and offer what the message offers: a different source.
- Summarize, don't echo every poll: "running 2m30s, currently writing the script," roughly once a minute (put `current_step` in plain words; never quote the raw code).
- Failure handling: on `failed`/`dead`, read `error` to locate the cause, **don't auto-retry**, tell the user and let them decide; if a task stays `queued` for over 2 minutes, the servers are busy: say the video will start as soon as a slot frees up, and keep polling.
- **Insufficient credits mid-riff** (a new-source riff clears the submit gate, then the real duration proves too costly — since v1.1.3 a low-balance riff usually gets an instant `402` at submit instead: TikTok URLs via a metadata duration probe, uploads via the on-disk file's real duration; this can still happen when the duration couldn't be read at submit, when the real duration differs from the probe, or when the balance dropped between submit and analysis, because the balance is checked again before analysis and again before generation): the analyze task carries `result.auto_generate_error == "insufficient_credits"` and `result.insufficient_credits` = the same structured 402 payload (`required_credits` / `available_credits` / `topup_url`). This means **no video was generated** — even when `status == "completed"` (the analysis finished but generation was skipped). Treat it like a 402: relay `topup_url` verbatim and tell the user to top up. Once they have: if the analyze task is `failed` (the check ran before analysis), **retry that task** (`POST /api/tasks/{id}/retry`, within 24h); if it is `completed`, a retry is refused, so **submit again** with `POST /api/riffs`, `formula_id` = the task's `result.formula_id` and **the same options as before** (`mode`, `character_ids`, `product_id`, `product_visibility`, `content_anchor`, `language`, `video_backend`, `resolution`, `video_ratios`). Nothing carries over from the first submit; the saved analysis is reused (no second analysis, no wait for one) and only the video is billed, as usual. **Never report success on a riff whose analyze task carries this field.**

### Delivery and files (step 9)

`GET /api/assets?asset_role=final_reel&sort=created_desc&limit=10` (add `formula_id` / `character` to filter this run):

1. **The video file** — `${BASE_URL}${file_url}`. This is the ONLY file path — there is **no** `/api/assets/{id}/download` sub-resource (it 404s; do not invent REST-style suffixes). The GET needs the same `Cookie: vee_session=<token>` as every API call, and must follow redirects (`curl -L`): in production it 302s to object storage. A cookie-less GET returns 401. For a link the user can open in their own browser, where your session cookie doesn't travel, call `GET /api/assets/{asset_id}/link`: its `url` opens the video without the cookie for 6 hours; say how long it works and that you can get a fresh one.
2. **Suggested copy** — `caption` (hook → body → closing call-to-action folded into one paragraph) + `asset_hashtags`
3. **Strategy recap** — which emotion formula this used, through which beat the product was felt, what the content_anchor did. To see what the engine actually "extracted / rewrote," call `GET /api/tasks/{task_id}/content`.
4. **Next iteration** — next time tweak content_anchor / character / product combo; a richer template library (more `used_count` / `tags`) gives sharper picks.

#### Using a finished video in Remotion or another code-made video

When the user wants the clip inside their own Remotion composition (or any video rendered from code), download it to a local file first. Remotion reads a local file or a public URL, and the asset URL only answers with the session cookie, so don't hand it the URL directly:

```bash
curl -L -b "vee_session=<token>" "${BASE_URL}<sd_video_url or file_url>" -o clip.mp4
```

The first request needs the cookie; the redirect then lands on signed storage. Put `clip.mp4` in the project's `public/` folder and load it with `staticFile("clip.mp4")`.

- **Clean master, no burned-in captions**: use `sd_video_url` when it's set. It is the render before post-processing: no burned-in captions, but the final mixed audio is already in it. It's only set when post-processing ran; when it's null, `file_url` is already that render. Use `file_url` when the user wants the captions kept, and then don't add a second set of captions on top. A swap is the exception: the source video's on-screen text is drawn into the swap's picture, so neither file is free of it.
- **Frame shape**: choose it at submit to match the composition. Riffs take `video_ratios` (vertical `9:16` / `3:4` / `1:1` / `4:5`, any mix, or one of `16:9` / `4:3` / `21:9` alone); creation takes one `video_ratio`; a swap keeps the source's frame. A vertical video you already have can get more vertical ratios with `POST /api/pipeline/backfill`.
- **Fixed length**: a creation video can be pinned with `duration_mode=fixed` + `duration_seconds` (4-45). A swap is exactly as long as its source; an adapt riff's length isn't fixed until it renders, so for a composition that needs an exact length use a creation video with `duration_mode=fixed`.
- **Sound**: the video has ONE mixed audio track, voice and music together. In Remotion you can keep it, lower it or mute it as a whole (`volume` / `muted` on `<OffthreadVideo>`), but you can't take the music out and keep the voice. If the user adds their own music, tell them it will play over the music already in the clip.
- Save the file into the user's own project; don't upload it to a third-party host unless the user asks.

---

## General constraints

| Dimension | Limit | Source |
|------|------|------|
| Source video (upload or TikTok link) | Upload ≤ **100 MB**; both ≤ the **render-duration cap** (`max_render_duration`, default **45 s**, runtime-adjustable, ceiling 90s) — the SAME single number that caps the riff output, not a separate limit; over the duration → 400 at submit for an upload (the file is also cleaned up); a TikTok link gets the same 400 when its length can be read up front, otherwise the link is accepted and the analyze task fails with the same "~Ns, over the Ms limit" message once the video has downloaded (nothing is generated or billed) | `POST /api/riffs` `video`/`tiktok_url`, `POST /api/formulas/analyze` |
| Generated video length | Riffs (adapt / swap): ≤ **max_render_duration** (the same single cap as the source upload above). Creation videos: **4-45 s**, a separate fixed ceiling that does not follow `max_render_duration` (smart mode is also capped at what the balance affords; see `POST /api/creation/batch`) | engine render budget; creation: `POST /api/creation/batch` |
| Swap source length | ≤ **max_render_duration** for every swap source (template, upload, link): a swap is never compressed, so the output equals the source length | `POST /api/riffs` `mode=swap` |
| Image upload | ≤ **50 MB** each, ≤ **8 images** per product, `.jpg/.jpeg/.png/.webp` | product images |
| `content_anchor` / `user_hint` | ≤ **5000 chars** (over → `422`) | riffs / pipeline/batch / creation/batch |
| riffs rate | **10 / 60 s** | `POST /api/riffs` |
| Task concurrency | Shared worker pool, sized per server (not a per-account quota); overflow → `queued`; under heavy load a new submit gets `429` with `detail.code == "server_busy"` (`Retry-After: 30`) | server TaskRunner |
| Generation time | pipeline **3-8 min** (empirical) | — |
| Poll interval | every **30 s** | The flow, step 8 |
| Daily credit cap | `daily_limit` from `GET /api/usage/credits` (`0` = unlimited; internal credits ÷100 for display) | adjustable by owner/admin |

> BGM is picked by the backend (optionally steered with `bgm_mode` on an analyzed template) — the riff flow has no audio upload step.

---
