#!/usr/bin/env python3
"""Render need-named skill variants from the canonical SKILL.md.

One source of truth: the canonical `SKILL.md` at the repo root (mirrored daily
from https://riffkit.ai/SKILL.md by .github/workflows/sync-skill.yml). Each
entry in `variants.json` becomes `<name>/SKILL.md` — the canonical body verbatim,
under a frontmatter whose name/description come from the variant and whose
version/updated_at/source_url/homepage are inherited from the canonical file.

Never edit a generated `<name>/SKILL.md`: edit `variants.json` (naming/description)
or the canonical SKILL.md (body, which lives in the Riffkit app).

Stdlib only — this runs on a bare `actions/checkout` + ubuntu python3.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CANONICAL = REPO / "SKILL.md"
HEARTBEAT = REPO / "HEARTBEAT.md"
VARIANTS = REPO / "variants.json"

SOURCE_URL = "https://riffkit.ai/SKILL.md"
GENERATED_BANNER = (
    f"<!-- GENERATED from {SOURCE_URL} by scripts/render_variants.py "
    "— edit variants.json or the canonical SKILL.md, never this file -->"
)

# Frontmatter keys carried over from the canonical skill, in emitted order.
INHERITED_KEYS = ("version", "updated_at", "source_url", "homepage")

# A variant is a distinct client, so its body identifies itself — attribution
# only. Two independent, idempotent rewrites; each is a no-op when its anchor
# isn't in the canonical body (the canonical file is never edited for this).
#
# 1. Any literal client tag, should the canonical ever carry one.
CLIENT_MARKER = '"client": "riffkit"'
# 2. The one-click sign-in "a. Start" step: teach it to post the client name.
DEVICE_ANCHOR = "POST /api/skill/device/authorize"
DEVICE_FROM = "(no body, no auth needed)"

# Directories that are ours to delete when a variant leaves variants.json.
GENERATED_MARKER = "generated_from:"


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """Return (frontmatter lines, body) for a `---`-delimited YAML header."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{CANONICAL}: expected YAML frontmatter opening '---'")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "".join(lines[i + 1 :])
    raise SystemExit(f"{CANONICAL}: unterminated YAML frontmatter")


def parse_simple_keys(fm_lines: list[str]) -> dict[str, str]:
    """Pick out top-level `key: value` scalars. No pyyaml, by design.

    Only column-0 keys count, so indented continuation lines (the canonical
    description is a multi-line plain scalar) never masquerade as keys.
    """
    out: dict[str, str] = {}
    for line in fm_lines:
        if not line.strip() or line[:1].isspace() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or not key or key != key.strip():
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key.strip()] = value
    return out


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def tag_client(body: str, name: str) -> str:
    """Make the variant's body identify itself as the calling client."""
    body = body.replace(CLIENT_MARKER, f'"client": "{name}"')

    device_to = f'(JSON body {{"client": "{name}"}}, no auth needed)'
    lines = body.splitlines(keepends=True)
    hits = 0
    for i, line in enumerate(lines):
        if DEVICE_ANCHOR in line and DEVICE_FROM in line:
            lines[i] = line.replace(DEVICE_FROM, device_to)
            hits += 1
    if not hits:
        print(
            f"WARN {name}: device-authorize anchor not found "
            f"({DEVICE_ANCHOR!r} + {DEVICE_FROM!r}) — body left as-is"
        )
    return "".join(lines)


def render(variant: dict, canonical_meta: dict[str, str], body: str) -> str:
    name = variant["name"]
    fm = [f"name: {name}", f"description: {yaml_quote(variant['description'])}"]
    for key in INHERITED_KEYS:
        if key in canonical_meta:
            fm.append(f"{key}: {yaml_quote(canonical_meta[key])}")
    fm.append(f"generated_from: {yaml_quote(SOURCE_URL)}")

    variant_body = tag_client(body, name)
    return "---\n" + "\n".join(fm) + "\n---\n\n" + GENERATED_BANNER + "\n" + variant_body


def prune_stale(keep: set[str]) -> list[str]:
    """Drop variant dirs we generated that are no longer in variants.json."""
    removed = []
    for child in sorted(REPO.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in keep:
            continue
        skill = child / "SKILL.md"
        if not skill.is_file():
            continue
        head = skill.read_text(encoding="utf-8")[:2048]
        if GENERATED_MARKER in head:
            shutil.rmtree(child)
            removed.append(child.name)
    return removed


def main() -> int:
    if not CANONICAL.is_file():
        raise SystemExit(f"missing {CANONICAL}")
    variants = json.loads(VARIANTS.read_text(encoding="utf-8"))

    fm_lines, body = split_frontmatter(CANONICAL.read_text(encoding="utf-8"))
    meta = parse_simple_keys(fm_lines)
    body = body.lstrip("\n")

    names = set()
    for variant in variants:
        name = variant["name"]
        if name in names:
            raise SystemExit(f"variants.json: duplicate name {name!r}")
        if "/" in name or name.startswith("."):
            raise SystemExit(f"variants.json: unusable name {name!r}")
        names.add(name)

        out_dir = REPO / name
        out_dir.mkdir(exist_ok=True)
        (out_dir / "SKILL.md").write_text(render(variant, meta, body), encoding="utf-8")
        if HEARTBEAT.is_file():
            shutil.copyfile(HEARTBEAT, out_dir / "HEARTBEAT.md")
        print(f"rendered {name}/SKILL.md")

    for name in prune_stale(names):
        print(f"removed stale variant {name}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
