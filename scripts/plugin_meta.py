#!/usr/bin/env python3
"""Refresh the Claude Code plugin listing from the served skill.

Usage: python3 scripts/plugin_meta.py SKILL.md SKILL.json

The sync workflow passes the freshly fetched root SKILL.md and SKILL.json
(both pulled from https://riffkit.ai). This script writes the skill's own
description (the frontmatter `description`, up to " Triggers:") and the
SKILL.json version into:

  plugins/riffkit/.claude-plugin/plugin.json   description + version
  .claude-plugin/marketplace.json              plugins[riffkit].description

so the plugin listing never drifts from the skill. The marketplace's own
top-level description is a fixed sentence that carries no facts.

Stdlib only. Exits non-zero, writing nothing, when the description or the
version cannot be read, so a bad fetch never blanks the listing. Output is
json.dump(indent=2) + newline, so a rerun on the same input changes nothing.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / "plugins" / "riffkit" / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN_NAME = "riffkit"
MARKETPLACE_DESCRIPTION = "The official Riffkit plugin for Claude Code."

# A double-quoted YAML scalar, which may span several lines, up to the
# closing quote that is not escaped.
DESCRIPTION_RE = re.compile(r'^description:\s*"((?:[^"\\]|\\.)*)"', re.M | re.S)


def fail(message):
    sys.exit(f"plugin_meta: {message}")


def frontmatter(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        fail("SKILL.md does not start with a --- frontmatter block")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    fail("SKILL.md frontmatter has no closing ---")


def skill_description(skill_md):
    match = DESCRIPTION_RE.search(frontmatter(skill_md))
    if not match:
        fail("no double-quoted description in the SKILL.md frontmatter")
    text = re.sub(r"\s+", " ", match.group(1))
    text = re.sub(r'\\(["\\/])', r"\1", text)
    text = text.split(" Triggers:", 1)[0].strip()
    if not text:
        fail("the SKILL.md description is empty")
    return text


def skill_version(skill_json):
    try:
        version = json.loads(skill_json).get("version")
    except (ValueError, AttributeError) as exc:
        fail(f"SKILL.json is not a JSON object: {exc}")
    if not isinstance(version, str) or not version.strip():
        fail("SKILL.json has no version")
    return version.strip()


def with_version(plugin, version):
    if "version" in plugin:
        plugin["version"] = version
        return plugin
    anchor = "displayName" if "displayName" in plugin else "name"
    out = {}
    for key, value in plugin.items():
        out[key] = value
        if key == anchor:
            out["version"] = version
    if "version" not in out:
        out["version"] = version
    return out


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")


def dump(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main(argv):
    if len(argv) != 3:
        sys.exit("usage: python3 scripts/plugin_meta.py SKILL.md SKILL.json")
    try:
        skill_md, skill_json = (Path(p).read_text(encoding="utf-8") for p in argv[1:])
    except OSError as exc:
        fail(f"cannot read the served skill: {exc}")
    description = skill_description(skill_md)
    version = skill_version(skill_json)

    plugin = load(PLUGIN_JSON)
    plugin["description"] = description
    plugin = with_version(plugin, version)

    marketplace = load(MARKETPLACE_JSON)
    entries = [p for p in marketplace.get("plugins", []) if p.get("name") == PLUGIN_NAME]
    if not entries:
        fail(f"marketplace.json lists no plugin named {PLUGIN_NAME!r}")
    marketplace["description"] = MARKETPLACE_DESCRIPTION
    entries[0]["description"] = description

    for path, data in ((PLUGIN_JSON, plugin), (MARKETPLACE_JSON, marketplace)):
        text = dump(data)
        if path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
        else:
            print(f"unchanged {path.relative_to(ROOT)}")
    print(f"version {version}: {description}")


if __name__ == "__main__":
    main(sys.argv)
