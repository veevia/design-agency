#!/usr/bin/env python3
"""
06_Engine/harness/lint-skill.py

Run the declarative `lints[*]` rules declared in a SKILL.md against the workspace.

Usage:
    python 06_Engine/harness/lint-skill.py <skill-slug-or-path> [--target <glob>] [--severity error|warning|info]
    python 06_Engine/harness/lint-skill.py --all [--severity error|warning|info]

Exit codes:
    0  no error-severity findings
    1  one or more error-severity findings
    2  invalid arguments or skill not found
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from skill_paths import find_skill_dir, iter_skill_dirs

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def _split_frontmatter(text: str) -> str | None:
    """Return the raw YAML front-matter block, or None if absent.

    Matches only the FIRST closing `---` fence. The naive text.split("---", 2)
    breaks whenever the SKILL.md BODY contains a `---` (horizontal rules, markdown
    table separators), wrongly flagging a skill with valid YAML as unparseable
    (it bit demo-master). Mirror 06_Engine/harness/spec-compliance.py.
    """
    if not text.startswith("---"):
        return None
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        return None
    return text[3 : m.start() + 3]


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / "03_Agents-and-Skills" / "Skills"
SEVERITY_ORDER = {"error": 3, "warning": 2, "info": 1}


@dataclass(frozen=True)
class Finding:
    severity: str
    skill: str
    rule_id: str
    path: Path
    line: int
    message: str

    def format(self) -> str:
        rel = self.path.relative_to(REPO_ROOT)
        return f"{self.severity} | {self.skill} | {self.rule_id} | {rel}:{self.line} | {self.message}"


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


def load_skill(slug_or_path: str) -> tuple[str, dict | None]:
    p = Path(slug_or_path)
    if not p.is_absolute():
        found = find_skill_dir(SKILLS_ROOT, slug_or_path)
        candidate = (found / "SKILL.md") if found else SKILLS_ROOT / slug_or_path / "SKILL.md"
        if candidate.exists():
            p = candidate
        elif (REPO_ROOT / slug_or_path).exists():
            p = REPO_ROOT / slug_or_path
    if p.is_dir():
        skill_file = p / "SKILL.md"
        if skill_file.exists():
            p = skill_file
        else:
            print(f"ERROR: directory has no SKILL.md: {slug_or_path}", file=sys.stderr)
            sys.exit(2)
    if not p.exists():
        print(f"ERROR: skill not found: {slug_or_path}", file=sys.stderr)
        sys.exit(2)
    text = p.read_text(encoding="utf-8")
    fm = _split_frontmatter(text)
    if fm is None:
        return p.parent.name, {}
    try:
        data = yaml.safe_load(fm) or {}
    except yaml.YAMLError as e:
        print(f"# {p.parent.name}: front-matter YAML parse error — FAIL ({e.__class__.__name__})", file=sys.stderr)
        return p.parent.name, None
    if not isinstance(data, dict):
        print(f"# {p.parent.name}: front-matter is not a mapping — FAIL", file=sys.stderr)
        return p.parent.name, None
    return p.parent.name, data


def expand_glob(pattern: str, *, include_proposed: bool = False) -> list[Path]:
    out: list[Path] = []
    for sub in expand_braces(pattern):
        for p in REPO_ROOT.glob(sub):
            s = str(p)
            if not p.is_file():
                continue
            if "/Archive/" in s or "/.git/" in s:
                continue
            if "/06_Engine/evals/" in s:
                continue
            if not include_proposed and ("/_proposed/" in s or "/_proposed-skills/" in s):
                continue
            out.append(p)
    return out


def _frontmatter_keys_present(text: str, keys: list[str]) -> bool:
    """True if the file's YAML front-matter declares ALL of `keys` with truthy values.

    Used by `skip_if_frontmatter`: a rule can declare that a page which sets, e.g.,
    `evidence-default` + `sources` in front-matter has already supplied provenance at
    the page level (per the evidence-tagging skill's documented front-matter shortcut),
    so inline per-claim citations are not separately required. Keeps the linter honest
    to the skill's own spec instead of flagging a correctly-attributed page.
    """
    fm = _split_frontmatter(text)
    if fm is None:
        return False
    try:
        data = yaml.safe_load(fm) or {}
    except yaml.YAMLError:
        return False
    if not isinstance(data, dict):
        return False
    return all(bool(data.get(k)) for k in keys)


def apply_rule(skill: str, rule: dict, target_glob: str | None) -> Iterable[Finding]:
    rule_id = rule.get("id", "?")
    severity = rule.get("severity", "warning")
    where = target_glob or rule.get("where")
    pattern = rule.get("pattern")
    must_also = rule.get("must_also_match")
    forbid = rule.get("forbid")
    exclude = rule.get("exclude")
    skip_if_frontmatter = rule.get("skip_if_frontmatter")
    message = rule.get("message", "rule fired")

    if not where or not pattern:
        return

    try:
        rx = re.compile(pattern, re.MULTILINE)
    except re.error as e:
        yield Finding("error", skill, rule_id, REPO_ROOT, 0, f"invalid regex: {e}")
        return

    must_also_rx = re.compile(must_also, re.MULTILINE) if must_also else None
    forbid_rx = re.compile(forbid, re.MULTILINE) if forbid else None
    # `exclude`: an optional regex tested against the MATCHED TEXT itself. When it
    # matches, the hit is suppressed. This lets a line-oriented rule (e.g. the
    # untagged-claim-bullet check) skip lines that match the broad pattern but are
    # not actually claims — citations, wiki-link cross-refs, questions, sub-bullets,
    # metadata key/values. Keeps rules declarative instead of forcing ever-more-
    # baroque negative-lookahead into the main pattern.
    exclude_rx = re.compile(exclude) if exclude else None
    # `skip_if_frontmatter`: a list of front-matter keys; when a page declares ALL of
    # them (truthy), the whole rule is satisfied at the page level and we don't flag
    # its bodies. Honors the evidence-tagging skill's documented `evidence-default` +
    # `sources` shortcut — a correctly-attributed page isn't an error.
    fm_keys = skip_if_frontmatter if isinstance(skip_if_frontmatter, list) else (
        [skip_if_frontmatter] if skip_if_frontmatter else None)

    for path in expand_glob(where, include_proposed=target_glob is not None):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if fm_keys and _frontmatter_keys_present(text, fm_keys):
            continue
        for m in rx.finditer(text):
            if exclude_rx is not None and exclude_rx.search(m.group(0)):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            if must_also_rx is not None:
                if not must_also_rx.search(text):
                    yield Finding(severity, skill, rule_id, path, line_no, message)
                    break
            elif forbid_rx is not None:
                if forbid_rx.search(text):
                    yield Finding(severity, skill, rule_id, path, line_no, message)
                    break
            else:
                yield Finding(severity, skill, rule_id, path, line_no, message)
                break


def lint_skill(slug_or_path: str, target_glob: str | None, min_severity: str) -> int:
    slug, data = load_skill(slug_or_path)
    if data is None:
        print(f"# {slug}: unlintable — malformed front-matter (FAIL, exit 1)", file=sys.stderr)
        return 1
    lints = data.get("lints") or []
    if not lints:
        print(f"# {slug}: no lints declared \u2014 skipping", file=sys.stderr)
        return 0
    threshold = SEVERITY_ORDER.get(min_severity, 1)
    findings: list[Finding] = []
    for rule in lints:
        findings.extend(apply_rule(slug, rule, target_glob))
    findings = [f for f in findings if SEVERITY_ORDER.get(f.severity, 0) >= threshold]
    for f in findings:
        print(f.format())
    error_count = sum(1 for f in findings if f.severity == "error")
    print(
        f"# {slug}: {len(findings)} finding(s) (errors={error_count})",
        file=sys.stderr,
    )
    return 1 if error_count else 0


def contract_fields(data: dict) -> dict:
    """Merge portable nested metadata with legacy top-level contract fields."""
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return {**metadata, **data}


def contract_score(slug: str, data: dict) -> tuple[int, dict]:
    """Decomposition rubric (0-2 each, max 12) — the 'born executable' bar.

    Mirrors 06_Engine/harness/smoke-test-skills.py so the pre-commit gate and the
    BML smoke test agree. A skill scoring <10 is not yet agent-executable.
    """
    contract = contract_fields(data)
    subagent = contract.get("subagent") if isinstance(contract.get("subagent"), dict) else {}
    G = 2 if contract.get("title") and contract.get("status") else (1 if contract.get("title") or contract.get("description") else 0)
    WT = 2 if contract.get("when_to_load") else 0
    inp = contract.get("inputs") or []
    IN = 0
    if subagent.get("reads"):
        IN = 2
    elif inp:
        IN = 2 if any(isinstance(i, dict) and i.get("where") for i in inp) else 1
    out = contract.get("outputs") or []
    OUT = 0
    if subagent.get("emits"):
        OUT = 2
    elif out:
        OUT = 2 if any(isinstance(o, dict) and o.get("schema") for o in out) else 1
    DW = 2 if contract.get("done_when") else 0
    skill_dir = find_skill_dir(SKILLS_ROOT, slug)
    has_evals = bool(
        skill_dir
        and (skill_dir / "eval_queries.json").is_file()
        and (skill_dir / "evals" / "evals.json").is_file()
    )
    TR = 2 if (contract.get("lints") or []) or has_evals else 0
    return G + WT + IN + OUT + DW + TR, {"goal": G, "when": WT, "input": IN, "output": OUT, "done": DW, "trace": TR}


CONTRACT_MIN = 10  # a skill below this is not yet agent-executable


def contract_gate(slug_or_path: str) -> int:
    """Check one skill against the decomposition bar. Returns 1 if it fails.

    A skill may opt out with `contract-exempt: <reason>` in front-matter — for
    tool-recipe / knowledge-library skills that intentionally carry no file I/O
    or lints (the executable contract lives in a graduated agent or a prompt).
    Exempt skills are reported but never fail the gate.
    """
    slug, data = load_skill(slug_or_path)
    if data is None:
        print(f"FAIL  {slug:<28} malformed front-matter")
        return 1
    score, bd = contract_score(slug, data)
    exempt = contract_fields(data).get("contract-exempt")
    if exempt:
        print(f"exem  {slug:<28} {score}/12  (exempt: {str(exempt)[:48]})")
        return 0
    status = "ok" if score >= CONTRACT_MIN else "FAIL"
    missing = [k for k, v in bd.items() if v < 2]
    print(f"{status:<5} {slug:<28} {score}/12" + (f"  thin: {','.join(missing)}" if score < CONTRACT_MIN else ""))
    return 0 if score >= CONTRACT_MIN else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", help="skill slug or path to SKILL.md")
    parser.add_argument("--target", help="override `where:` with this glob")
    parser.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        default="info",
        help="minimum severity to report",
    )
    parser.add_argument(
        "--all", action="store_true", help="lint every skill that declares contracts"
    )
    parser.add_argument(
        "--contract",
        action="store_true",
        help=f"score the decomposition contract instead of running lints; fail any skill <{CONTRACT_MIN}/12",
    )
    args = parser.parse_args()

    # --- contract gate mode (the 'born executable' guardrail) ---
    if args.contract:
        if args.all or not args.skill:
            rc = 0
            print(f"# contract gate — every skill must score >= {CONTRACT_MIN}/12")
            for skill_dir in iter_skill_dirs(SKILLS_ROOT):
                if not skill_dir.is_dir():
                    continue
                if not (skill_dir / "SKILL.md").exists():
                    continue
                rc |= contract_gate(str(skill_dir / "SKILL.md"))
            print("# contract gate: " + ("PASS" if rc == 0 else "FAIL — thin skills above"))
            return rc
        return contract_gate(args.skill)

    if args.all:
        rc = 0
        for skill_dir in iter_skill_dirs(SKILLS_ROOT):
            if not skill_dir.is_dir():
                continue
            sk = skill_dir / "SKILL.md"
            if not sk.exists():
                continue
            rc |= lint_skill(skill_dir.name, args.target, args.severity)
        return rc

    if not args.skill:
        parser.print_help()
        return 2

    return lint_skill(args.skill, args.target, args.severity)


if __name__ == "__main__":
    sys.exit(main())
