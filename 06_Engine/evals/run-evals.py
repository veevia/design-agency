#!/usr/bin/env python3
"""
06_Engine/evals/run-evals.py

Run golden-task evals. Each eval applies its skill's lint rules to fixture
files under `input/` and compares findings to `expected.yaml`.

Usage:
    python 06_Engine/evals/run-evals.py                # all evals
    python 06_Engine/evals/run-evals.py <skill-id>     # single eval

Exit codes:
    0  all signals passed
    1  one or more signals failed
    2  invalid arguments
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, date, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[2]
EVALS_DIR = Path(__file__).resolve().parent
SKILLS_DIR = REPO_ROOT / "03_Agents-and-Skills" / "Skills"
STALE_AFTER_DAYS = 90


def _split_frontmatter(text: str) -> str | None:
    """Return the raw YAML front-matter block, or None if absent.

    Matches only the FIRST closing `---` fence on its own line. The naive
    text.split("---", 2) breaks whenever the SKILL.md BODY contains a `---`
    (horizontal rules, markdown table separators), wrongly truncating valid
    YAML. Mirror of 06_Engine/harness/lint-skill.py:_split_frontmatter.
    """
    if not text.startswith("---"):
        return None
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        return None
    return text[3 : m.start() + 3]


def expand_braces(pattern: str) -> list[str]:
    """Expand one-level brace alternation: a/{x,y}/b -> [a/x/b, a/y/b]."""
    m = re.search(r"\{([^{}]+)\}", pattern)
    if not m:
        return [pattern]
    head, tail = pattern[: m.start()], pattern[m.end() :]
    alts = [a.strip() for a in m.group(1).split(",")]
    out: list[str] = []
    for a in alts:
        out.extend(expand_braces(head + a + tail))
    return out


def load_skill_lints(skill_id: str) -> list[dict]:
    sk = next(iter(SKILLS_DIR.glob(f"*/{skill_id}/SKILL.md")), SKILLS_DIR / skill_id / "SKILL.md")
    text = sk.read_text(encoding="utf-8")
    fm = _split_frontmatter(text) or ""
    data = yaml.safe_load(fm) or {}
    return data.get("lints") or []


def _frontmatter_keys_present(text: str, keys: list[str]) -> bool:
    """True if the file's YAML front-matter declares ALL of `keys` with truthy values.

    Mirror of the same helper in 06_Engine/harness/lint-skill.py so the eval harness
    evaluates rules with the SAME semantics the linter uses (incl. skip_if_frontmatter).
    """
    if not text.startswith("---"):
        return False
    fm = _split_frontmatter(text)
    if fm is None:
        return False
    try:
        data = yaml.safe_load(fm) or {}
    except yaml.YAMLError:
        return False
    return isinstance(data, dict) and all(bool(data.get(k)) for k in keys)


def count_matches(rule: dict, fixture_root: Path) -> int:
    """Count every match of `rule` across fixture files (no per-file break).

    Honors the same optional fields the linter applies — must_also_match, forbid,
    exclude, skip_if_frontmatter — so an eval can't pass while the linter's real
    behavior has silently changed (e.g. an over-broad `exclude` that kills detection).
    """
    where = rule.get("where", "")
    pattern = rule.get("pattern", "")
    must_also = rule.get("must_also_match")
    forbid = rule.get("forbid")
    exclude = rule.get("exclude")
    skip_if_frontmatter = rule.get("skip_if_frontmatter")
    if not where or not pattern:
        return 0
    files: list[Path] = []
    for sub in expand_braces(where):
        files.extend(fixture_root.glob(sub))
    try:
        rx = re.compile(pattern, re.MULTILINE)
    except re.error:
        return 0
    must_also_rx = re.compile(must_also, re.MULTILINE) if must_also else None
    forbid_rx = re.compile(forbid, re.MULTILINE) if forbid else None
    exclude_rx = re.compile(exclude) if exclude else None
    fm_keys = skip_if_frontmatter if isinstance(skip_if_frontmatter, list) else (
        [skip_if_frontmatter] if skip_if_frontmatter else None)
    count = 0
    for f in files:
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if fm_keys and _frontmatter_keys_present(text, fm_keys):
            continue
        for m in rx.finditer(text):
            if exclude_rx is not None and exclude_rx.search(m.group(0)):
                continue
            if must_also_rx is not None:
                if not must_also_rx.search(text):
                    count += 1
            elif forbid_rx is not None:
                if forbid_rx.search(text):
                    count += 1
            else:
                count += 1
    return count


def run_eval(skill_id: str) -> tuple[bool | None, list[str]]:
    eval_dir = EVALS_DIR / skill_id
    expected_path = eval_dir / "expected.yaml"
    fixture_root = eval_dir / "input"
    if not expected_path.exists() or not fixture_root.exists():
        # Incomplete stub (e.g. README-only): skip rather than fail the whole gate,
        # so one unfinished eval cannot block every commit. Completing it re-enables it.
        return None, [f"eval {skill_id}: incomplete stub (no expected.yaml/input) — skipped"]
    expected = yaml.safe_load(expected_path.read_text(encoding="utf-8")) or {}

    # Staleness warning
    updated = expected.get("updated")
    today = date.today()
    if updated is None:
        print(f"  WARN: eval {skill_id} has no `updated:` field; add `updated: YYYY-MM-DD` to expected.yaml")
    elif isinstance(updated, (date, datetime)):
        d = updated if isinstance(updated, date) else updated.date()
        age_days = (today - d).days
        if age_days > STALE_AFTER_DAYS:
            print(f"  WARN: eval {skill_id} is {age_days}d old (stale > {STALE_AFTER_DAYS}d); review gold signals.")
    else:
        try:
            d = datetime.strptime(str(updated), "%Y-%m-%d").date()
            age_days = (today - d).days
            if age_days > STALE_AFTER_DAYS:
                print(f"  WARN: eval {skill_id} is {age_days}d old (stale > {STALE_AFTER_DAYS}d); review gold signals.")
        except ValueError:
            print(f"  WARN: eval {skill_id} `updated:` is not YYYY-MM-DD: {updated!r}")

    lints = {r["id"]: r for r in load_skill_lints(skill_id) if "id" in r}
    findings: list[str] = []
    all_pass = True

    for signal in expected.get("signals", []):
        sid = signal.get("id", "?")
        rule_id = signal.get("rule")
        rule = lints.get(rule_id)
        if rule is None:
            findings.append(f"  FAIL {sid}: rule `{rule_id}` not declared in {skill_id}")
            all_pass = False
            continue
        count = count_matches(rule, fixture_root)
        min_c = signal.get("min_count")
        max_c = signal.get("max_count")
        forbid = signal.get("forbid", False)
        ok = True
        if forbid:
            ok = count == 0
        else:
            if min_c is not None and count < min_c:
                ok = False
            if max_c is not None and count > max_c:
                ok = False
        if ok:
            findings.append(f"  PASS {sid}: rule={rule_id} count={count}")
        else:
            findings.append(
                f"  FAIL {sid}: rule={rule_id} count={count} "
                f"expected min={min_c} max={max_c} forbid={forbid}"
            )
            all_pass = False
    return all_pass, findings


def main() -> int:
    args = sys.argv[1:]
    if not args:
        targets = sorted(
            d.name for d in EVALS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")
        )
    else:
        targets = args

    overall_pass = True
    for skill_id in targets:
        eval_dir = EVALS_DIR / skill_id
        if not eval_dir.exists():
            print(f"=== {skill_id}: NOT FOUND ===")
            overall_pass = False
            continue
        print(f"=== {skill_id} ===")
        ok, findings = run_eval(skill_id)
        for line in findings:
            print(line)
        if ok is None:
            print("  Result: SKIP (incomplete stub)")
            continue
        print(f"  Result: {'PASS' if ok else 'FAIL'}")
        overall_pass = overall_pass and ok
    print(f"\nOverall: {'PASS' if overall_pass else 'FAIL'}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
