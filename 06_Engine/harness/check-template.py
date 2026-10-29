#!/usr/bin/env python3
"""check-template.py — repository hygiene, stricter in `mode: template`.

Always:
  * no dependency, cache or OS-noise files in the repository (node_modules, .venv, __pycache__,
    .pytest_cache, *.pyc, .DS_Store) — tracked or untracked-and-not-ignored;
  * no absolute personal paths (a user's home directory) in text files;
  * `.gitmodules` sources are URLs, never local filesystem paths.
Template mode (the blank harness) additionally requires:
  * 01_Project-Hubs holds only README.md and _template-project/;
  * no plug-in is mounted or registered, and no *_TENANT.md customer file exists.

    python3 06_Engine/harness/check-template.py [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_DIR))

from agency.config import HUBS_DIR, TEMPLATE_HUB, load_config  # noqa: E402
from agency.plugins import plugin_states, read_gitmodules  # noqa: E402

NOISE = re.compile(r"(^|/)(node_modules|\.venv[^/]*|__pycache__|\.pytest_cache)(/|$)|(^|/)\.DS_Store$|\.pyc$")
# A home directory followed by a user name, e.g. /Users/<name>/ or C:\Users\<name>\ .
PERSONAL_PATH = re.compile(r"(?<![\w.])(?:/Users/|/home/)[A-Za-z0-9._-]+/|\b[A-Za-z]:\\\\?Users\\\\?[A-Za-z0-9._-]+")
LOCAL_SOURCE = re.compile(r"^(?:/|\./|\.\./|~|file://|[A-Za-z]:[\\/])")
ALLOWED_HUB_ENTRIES = {"README.md", TEMPLATE_HUB}
SELF = Path(__file__).resolve()


def repository_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [name for name in result.stdout.split("\0") if name]


def check(root: Path) -> list[str]:
    root = Path(root)
    config = load_config(root)
    states = plugin_states(root, config)
    mounts = [str(state.mount) for state in states.values()]
    problems: list[str] = []
    files = repository_files(root)
    for name in files:
        if NOISE.search(name):
            problems.append(f"noise file in repository: {name} (ignore or delete it)")
    for name in files:
        path = root / name
        if any(name == mount or name.startswith(mount + "/") for mount in mounts):
            continue
        if path.resolve() == SELF or path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        data = path.read_bytes()
        if b"\0" in data[:4096]:
            continue
        for number, line in enumerate(data.decode("utf-8", errors="ignore").splitlines(), 1):
            if PERSONAL_PATH.search(line):
                problems.append(f"absolute personal path in {name}:{number}; use a repository-relative path")
                break
    for path, entry in read_gitmodules(root).items():
        if LOCAL_SOURCE.match(entry.get("url", "")):
            problems.append(f".gitmodules: {path} uses a local source ({entry['url']}); set an https URL")
    if config.mode == "template":
        hubs = root / HUBS_DIR
        if hubs.is_dir():
            extra = sorted(p.name for p in hubs.iterdir() if p.name not in ALLOWED_HUB_ENTRIES and p.name != ".DS_Store")
            if extra:
                problems.append(
                    f"template mode allows only {TEMPLATE_HUB} in {HUBS_DIR}; found {', '.join(extra)} "
                    "(set `mode: workspace` in agency.yaml if this repository now holds project work)"
                )
        for name, state in states.items():
            if state.present or state.registered:
                problems.append(f"template mode: plug-in {name} is mounted at {state.mount}; the blank template mounts none")
        tenant = [name for name in files if name.endswith("_TENANT.md")]
        if tenant:
            problems.append(f"template mode: customer-labelled files present: {', '.join(tenant)}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ENGINE_DIR.parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    problems = check(args.root)
    mode = load_config(args.root).mode
    if args.json:
        print(json.dumps({"mode": mode, "problems": problems}, indent=2))
    else:
        for problem in problems:
            print(f"FAIL {problem}")
        print(f"hygiene ({mode} mode): {'clean' if not problems else f'{len(problems)} problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
