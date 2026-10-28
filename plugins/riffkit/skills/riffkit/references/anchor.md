## Core idea: the three responsibility layers (why content_anchor is the agent's value)

| Layer | Role | Locked by | Freedom |
|---|---|---|---|
| **Formula + skeleton** | **Floor guarantee** — a validated emotion mechanism + camera language | At template analysis | None (changing it forfeits the riff's value) |
| **Character + product** | **Base constants** — the digital human + product facts | Chosen in settings (or default) | Different picks = different constants, but constant within one task |
| **content_anchor** | **Ceiling driver** — which selling-point angle, which surface to fill | Agent + user draft it (optional) | **The one degree of strategic freedom** |

The formula skeleton decides which psychological path the viewer walks; `content_anchor` decides what specific content fills that path. The other layers are pre-existing constants, so **the agent's differentiated value is fusing "source formula × product/account × character" into one concrete creative instruction**: which of the product's N selling points to angle on, which surface to fill into the template's emotion mechanism. It is an **optional collaboration, not a blocking hard-stop.**

---

## content_anchor drafting framework (core subsection)

> The formula and skeleton decide which psychological path the viewer walks; `content_anchor` decides what specific content fills that path.
> When non-empty it is the **highest-priority input** for surface direction.
> Failure test: if swapping the surface for any other topic still holds, the anchor never anchored the output → invalid.
>
> **Pointing at a picture or a person**: an image is used because its id was sent (`product_image_ids`, `reference_ids`), never because its name appears in the text. To tie words to one, write an @-mention: `@` plus a short name in the anchor, listed in `mentions` with what it points at (a reference image, a product image in use, a character). The words around it say who wears it, where and when.

**Drafting template:**

```
[a specific emotion-mechanism beat of the template] × [a specific feature of the product/account] → [the viewer mind-shift you want]
```

| ✅ Focus on | ❌ Don't (lives elsewhere or zero-info) |
|---|---|
| The specific product × template join ("the scan feature × the reveal beat at segment 2") | Product generalities ("show the product's strengths") |
| The angle you want this time (which of N selling points) | Template generalities ("use the funny formula") |
| One specific face of the audience's pain point | Account positioning ("health niche" — already in persona) |
| The viewer mind-shift ("from 'I assumed it was safe' to 'a quick scan reveals hidden additives'") | Generic creative words ("authentic / real / heartfelt") |

**Where the anchor's weight goes per mode:**

| Mode | content_anchor weight |
|---|---|
| `on_camera` | Product **visual** feature × the template's on-screen action ("the package-scan gesture × the reveal beat's curiosity→surprise") |
| `off_camera` | Product **function/benefit** × the template's voiceover/subtitle ("the pain the app solves × the hook's resonance → download urge") |
| `no_product` | The account's specific angle × the template's emotion formula → the resonance you want (**the anchor matters most here** — with no product, it's the only thematic anchor) |

### How to write it (craft)

The engine already mirrors the source. Your anchor is a **delta**, not a brief.

1. **Say only what should differ from the source.** Everything you don't mention is inherited. If the only thing that changes is who is on camera, the correct anchor is empty — writing more pulls the render away from a formula that already works.

2. **Locate every change.** A change stated as a concept loses to the source; the same change stated with a place — which beat, which moment, what happens right before and after — is the one that lands.

3. **Length tracks how far you're departing, not how much you care.** A big departure needs detail; a small one needs a line.

4. **Keep separate axes separate.** How it's shot (lighting, grain, camera feel) and what's in it (wardrobe, props, setting) are different axes. Collapse them into one sentence and one will drag the other — asking for an unpolished look often flattens the subject too.

5. **Quote what must stay word-for-word.** Text in double quotes — a slogan, a line to be spoken exactly, a caption that must read a certain way — is kept byte-for-byte and never translated, even when the video's `language` differs (`she says "Make it yours."` keeps that English line inside a Japanese video). Everything unquoted is direction: the engine realizes it in the target language and fits numbers and details to the script it writes.

**Building your own guard list.** Something in a render you never asked for is the engine's default showing: add an explicit "not X" next time, and keep a short list of these to paste into every anchor. It is the cheapest fix there is.

**Point at a picture or a person with an @-mention**: write `@` plus a short name in `content_anchor` ("she wears @Red dress in the car") and send `mentions` = `[{"token": "@Red dress", "target": "reference", "id": "<reference id>"}]`. `target` is `reference` (one of `reference_ids`), `product_image` (one of the product images in use) or `persona` (one of `character_ids`). The token must appear in the text exactly as written, once per mention. A name written without a mention is only text: it selects nothing.

---
