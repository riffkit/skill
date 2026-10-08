## Natural-language intent ↔ action map

| Intent | Example | Action |
|---------|-------------|-----------|
| One-shot riff | "riff this link", "make me one from this video" | `POST /api/riffs` (settle Adapt or Swap first, the flow's step 0; then source + optional config; confirm before submit) |
| Original / no source | "make an original ad, no reference", "just write me a video about X", "创作一条" | `POST /api/creation/batch` (creative direction REQUIRED — draft it with the user; price it with `GET /api/creation/quote`; confirm before submit) |
| Riff a new viral | "why did this TikTok pop off — riff it for me" | `POST /api/riffs` (pass `tiktok_url`/`video` → analyze→generate) |
| A video on the user's phone | "I have it on my phone", "can I send you my video" | `POST /api/riffs/uploads` → the user adds it on that page → `GET /api/riffs/uploads/{upload_id}` → `POST /api/riffs` with `upload_id` |
| Run an existing template | "make one with template 3" | `POST /api/riffs` (pass `formula_id`) |
| Same shots, my character | "put my character in this exact video", "keep the video, swap the person", "翻拍" | `POST /api/riffs` with `mode=swap` + a character + one source; `content_anchor` = what else changes |
| Browse templates | "what templates are there", "which is hot lately" | `GET /api/formulas?status=analyzed&template_type=pipeline` (by `used_count` / `tags`) |
| Drill into a template | "tell me about this one", "why recommend it" | `GET /api/formulas/{id}`, read `extraction_summary` |
| Re-analyze a template / fix its hint | "this is stale", "the hook is actually at 0:05" | `PATCH /api/formulas/{id}` (`user_hint`, optional) → `POST /api/formulas/{id}/refresh-analysis` (your own templates; a stale public template → pick another) |
| Add a product / image | "I have a new product", "add an image to the product" | Restate + confirm → `POST /api/products` / `POST /api/products/{id}/images` (serial) |
| Pick language | "make it in Spanish", "switch language" | `GET /api/languages` for candidates → set `language` |
| On / off camera / none | "should the product show", "I don't want a product, just growth" | Explain `product_visibility` (incl. no `product_id` = no_product) + recommend a value |
| Check progress | "how's it going", "done yet" | `GET /api/tasks/batch/{batch_id}` or `GET /api/tasks/{id}` |
| Get results | "give me the download link" | `GET /api/assets?asset_role=final_reel&...`, then `GET /api/assets/{id}/link` for a link the user can open |
| Fix subtitles | "the captions are mistimed", "move the subtitles up", "change the caption text/color" | Subtitle editing loop: `GET/PUT /api/assets/{id}/subtitles` → `POST .../preview` (iterate) → `POST .../burn` once (free; see `### Subtitle editing`) |
| Check balance / spend | "how much is left", "how much today" | `GET /api/usage/credits` → `available` / `daily_spent` (the caller's own spend since 00:00 UTC; ÷ 100 for display) |
| Finish a video made in sections | "make the rest", "next part", "redo that section" | `GET /api/assets` → its `staged.prices` → confirm → `POST /api/assets/{asset_id}/continue` |
| Stop a task | "stop it", "cancel" | `POST /api/tasks/{id}/cancel` (note no refund of what's charged) |
| Retry | "try again", "re-run" | `POST /api/tasks/{id}/retry` (state the most it can cost, confirm first) |
| Set a character's voice | "use my voice for this character", "lock her voice" | `POST /api/characters/{id}/voice-sample` (mp3/wav, 4-15s clean speech) — then automatic on every adapt riff / creation |

**Routing principle:** when intent is ambiguous, ask — don't guess and proceed.

---
