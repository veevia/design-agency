"""Canonical skill-path discovery for harness scripts.

Native skills use one flat layout, ``03_Agents-and-Skills/Skills/<slug>/SKILL.md``,
so a skill directory sits at the same depth as its discovery links
(``.github/skills/<slug>/`` and ``.claude/skills/<slug>/``) and relative links
resolve identically through either path. Plug-in mounts under ``Skills/`` are
not native skills; the plug-in registry in ``06_Engine/agency`` owns them.
"""

from __future__ import annotations

import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from agency.catalog import (  # noqa: E402  (path bootstrap above)
    SKILL_NAME,
    canonical_skill_map,
    find_skill_dir,
    iter_skill_dirs,
    native_skill_dirs,
)

__all__ = [
    "SKILL_NAME",
    "canonical_skill_map",
    "find_skill_dir",
    "is_canonical_skill_md",
    "iter_skill_dirs",
    "native_skill_dirs",
    "skill_group",
]


def is_canonical_skill_md(path: Path, skills_root: Path) -> bool:
    """True for a native ``Skills/<slug>/SKILL.md`` entry point."""
    return path.name == "SKILL.md" and path.parent in set(native_skill_dirs(skills_root))


def skill_group(skill_dir: Path, skills_root: Path) -> str:
    """Native skills have no group; plug-in skills report their mount folder."""
    relative = skill_dir.resolve().relative_to(skills_root.resolve())
    return "native" if len(relative.parts) == 1 else relative.parts[0]
