# Riffkit — riff winning TikTok videos into your own

[![Live skill](https://img.shields.io/badge/skill-riffkit.ai%2FSKILL.md-6d4ae0)](https://riffkit.ai/SKILL.md)
[![ClawdHub](https://img.shields.io/badge/ClawdHub-riffkit-ff6a3d)](https://clawhub.ai/riffkit/skills/riffkit)
[![License: MIT](https://img.shields.io/badge/license-MIT-3b82f6)](LICENSE)

**Don't copy. Riff.** Riffkit takes a winning short video, studies its *formula* — the hook, the pacing, the emotional beats — and generates a brand-new video around your product, your character, and your story. It never re-uploads the source clip; what comes out is your own original.

This is the **official Riffkit agent skill**. Add it to your AI assistant (Claude Code, Codex, Cursor, OpenClaw, …) and just say *"riff this TikTok into mine"* — your agent drives the whole pipeline. Or use it in the browser at **[riffkit.ai](https://riffkit.ai)**.

## Quick start (from your agent)

Point your AI coding assistant at the live skill and let it set itself up:

```
Read https://riffkit.ai/SKILL.md and follow the instructions to set up Riffkit.
```

Then just ask, in plain language:

```
riff https://www.tiktok.com/@user/video/123 into a video for my product, in Spanish
```

Your agent handles the rest: source → formula → new footage → your product & character → captions, cover, hashtags.

> The `SKILL.md` in this repo is a **readable mirror** — your agent always reads the live, canonical [`https://riffkit.ai/SKILL.md`](https://riffkit.ai/SKILL.md).

## See it in action

Every clip below was **riffed from one winning short video** — the source is never re-uploaded, so each result is an original.

**Recreate a proven survival hook**

https://github.com/user-attachments/assets/b7e6ea34-9f9a-4d3c-a191-cabd84ca6f00

**Weave your product into the format**

https://github.com/user-attachments/assets/d476c952-8ae6-404e-9a62-349f476fa89c

**Localize to native Spanish — phrasing + fonts, not a subtitle overlay**

https://github.com/user-attachments/assets/a3016013-fa4a-48cf-8c74-8fe1cb3e2a48

**Any look — real, cartoon, or game / CG**

https://github.com/user-attachments/assets/b7196db2-311b-48f5-b9c8-8f08a96a2831

<details>
<summary>More riffs</summary>

https://github.com/user-attachments/assets/c4b3d4d9-2a50-4f05-9c03-02ca413ca9ce

https://github.com/user-attachments/assets/397d8ace-82fb-41b0-8b04-539d68eeb1e3

https://github.com/user-attachments/assets/e2fb65c3-5123-409f-bdce-3f64b4a66f48

</details>

## Works with

| Where | How |
| --- | --- |
| **Claude Code · Codex · Cursor · OpenClaw** — any agent that can read a URL and make HTTP calls | `Read https://riffkit.ai/SKILL.md and follow the instructions` |
| **Browser** — no agent needed | Upload a clip or paste a TikTok link at [riffkit.ai](https://riffkit.ai) |

No MCP server to run, no local models — the skill is a thin layer over Riffkit's hosted backend.

## What you get

- **Riffs the formula, not the footage** — studies a proven video's hook, pacing, and beats, then generates new footage. The source clip is never re-uploaded, so the result is your own original.
- **Your product, woven in** — a physical item or an app screen, placed into the story the format calls for (not bolted onto a generic stock avatar).
- **A consistent character** — your own avatar and persona across every video, or **Auto** (no avatar needed).
- **English or Spanish** — native phrasing and the right fonts, not a translated subtitle laid on top.
- **Post-ready** — voiceover, on-screen captions timed to the audio, a cover frame, and a caption with hashtags.
- **Any look** — real footage, cartoon, or game-style; the music ducks under the voiceover so it reads as real, not AI.
- **Full commercial rights** — everything you make is yours to post, run as ads, and monetize.

## Examples

Short, real walkthroughs — the prompt you give your agent and what comes back:

- [Riff a proven format for your product](examples/tiktok-shop-product.md)
- [Localize a winning video into Spanish](examples/localize-spanish.md)
- [Any look — real, cartoon, or game / CG](examples/any-look-styles.md)
- [Run a faceless account on Auto](examples/faceless-and-auto.md)

## FAQ

**Do I need an account?** Yes — Riffkit is hosted; generating videos needs a Riffkit account, billed by the second of finished video.

**Which agents work?** Any assistant that can read a URL and make HTTP calls — Claude Code, Codex, Cursor, OpenClaw, and more. There's no MCP server to run.

**What languages?** English and Spanish — native phrasing and fonts, not a translated subtitle laid on top.

**Is my source video re-uploaded?** No. Riffkit studies the *formula* and generates new footage; the source clip is never re-hosted, so the output is your own original.

**Do I own what I make?** You get full commercial rights — post it, run it as ads, monetize it.

**Do I need a GPU or local setup?** No. Rendering runs on Riffkit's servers.

## Requirements

Riffkit is a **hosted** service: the skill is a thin layer that calls the Riffkit backend, and rendering happens on Riffkit's servers — no local GPU, models, or setup. **Generating videos requires a Riffkit account** (billed by the second of finished video). Create one at [riffkit.ai](https://riffkit.ai).

## Who it's for

TikTok Shop & e-commerce sellers, ad buyers, indie founders, and faceless-account operators — anyone who has to keep posting short-form video.

## Links

- App & sign-up — https://riffkit.ai
- Pricing — https://riffkit.ai/pricing
- Blog — https://riffkit.ai/blog
- Live skill (source of truth) — https://riffkit.ai/SKILL.md
- ClawdHub listing — https://clawhub.ai/riffkit/skills/riffkit

---

Don't copy. Riff.

## License

[MIT](LICENSE) — covers this repo's files (the skill's integration spec + docs). The Riffkit service itself is a hosted product.
