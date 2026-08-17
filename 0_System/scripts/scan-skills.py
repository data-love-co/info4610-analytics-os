#!/usr/bin/env python3
"""
scan-skills.py — Scan .agents/skills/ for SKILL.md files and update skills.json.

Run from the repo root:
    python3 0_System/scripts/scan-skills.py

skills.json is a SLIM STATE REGISTRY, not a description cache:
- It records, per skill, only {name, path, enabled}.
- The source of truth for what a skill is and when it fires is each SKILL.md
  frontmatter on disk — read that directly (find-skills does). Descriptions are
  deliberately NOT copied here, so they can never go stale against the SKILL.md.
- `enabled` is the one field that cannot be re-derived from the directory, so it
  is preserved across rescans. New skills default to enabled: true; a skill that
  exists on disk but is missing from the registry should be treated as enabled.

Behaviour:
- Walks .agents/skills/ recursively, finds every SKILL.md, reads its `name:`.
- Drops skills whose SKILL.md was deleted; adds new ones (enabled: true).
- Writes .agents/skills/skills.json, sorted by path.
"""

import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILLS_DIR = os.path.join(REPO_ROOT, ".agents", "skills")
MANIFEST = os.path.join(SKILLS_DIR, "skills.json")


def frontmatter_name(path):
    """Return the `name:` scalar from a SKILL.md YAML frontmatter block, or None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return None

    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return None
    name_m = re.search(r"^name:\s*(.+)$", m.group(1), re.MULTILINE)
    return name_m.group(1).strip().strip('"').strip("'") if name_m else None


def main():
    # Load existing manifest to preserve enabled/disabled choices (keyed by path).
    existing_enabled = {}
    if os.path.exists(MANIFEST):
        try:
            with open(MANIFEST, "r", encoding="utf-8") as f:
                data = json.load(f)
            for skill in data.get("skills", []):
                existing_enabled[skill["path"]] = skill.get("enabled", True)
        except (json.JSONDecodeError, KeyError):
            print("Warning: could not parse existing skills.json -- rebuilding from scratch.")

    skills = []

    for dirpath, dirnames, filenames in os.walk(SKILLS_DIR):
        # Skip hidden and _underscore dirs
        dirnames[:] = sorted(
            d for d in dirnames if not d.startswith(".") and not d.startswith("_")
        )

        if "SKILL.md" not in filenames:
            continue

        skill_abs = os.path.join(dirpath, "SKILL.md")
        rel_path = os.path.relpath(skill_abs, SKILLS_DIR).replace(os.sep, "/")

        name = frontmatter_name(skill_abs)
        if not name:
            print(f"  Skipping {rel_path} -- no `name:` in frontmatter")
            continue

        # Preserve existing enabled state; default new skills to True.
        enabled = existing_enabled.get(rel_path, True)

        skills.append({"name": name, "path": rel_path, "enabled": enabled})

    skills.sort(key=lambda s: s["path"])

    manifest = {
        "version": "2",
        "_note": (
            "Slim state registry — enabled flags only. Source of truth for what each "
            "skill is and when it fires = the SKILL.md frontmatter under .agents/skills/. "
            "Regenerate with 0_System/scripts/scan-skills.py. Do not hand-edit."
        ),
        "skills": skills,
    }

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Report
    total = len(skills)
    enabled_count = sum(1 for s in skills if s["enabled"])

    print(f"\nWrote {total} skills to .agents/skills/skills.json")
    print(f"  {enabled_count} enabled  |  {total - enabled_count} disabled\n")

    for s in skills:
        status = "ok" if s["enabled"] else " x"
        print(f"  {status}  {s["name"]}  --  {s["path"]}")


if __name__ == "__main__":
    main()
