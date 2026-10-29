#!/usr/bin/env python3
"""agentic-os-review.py — the Design Agency OS integrity review (one command, one verdict).

Recomputes every gate from disk and prints a table of MUST/SHOULD rows with
PASS / FAIL / WARN / SKIP, then a verdict. Exit 0 only when every MUST row passes.
Passing proves repository integrity, not live runtime or plug-in quality.

    python3 00_Agentic-OS/agentic-os-review.py                 # full review
    python3 00_Agentic-OS/agentic-os-review.py --fast          # skip unit tests and evals (pre-commit)
    python3 00_Agentic-OS/agentic-os-review.py --json
    python3 00_Agentic-OS/agentic-os-review.py --contracts-only  # only the six L0–L5 contracts
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "06_Engine"
sys.path.insert(0, str(ENGINE))

from agency.config import ConfigError, load_config  # noqa: E402
from agency.catalog import binding_coverage, build_catalog, companion_hint  # noqa: E402
from agency.plugins import load_profiles, plugin_states, requirement_issues, resolve_python, run_checks  # noqa: E402

PY = sys.executable
DECISIONS = "03_Agents-and-Skills/Skills/traffic-light-decisions/scripts/check_decision.py"
LAYERS = ["L0", "L1", "L2", "L3", "L4", "L5"]
ADAPTER_MAX_LINES = 60
TEST_SUITES = [
    "06_Engine/tests",
    "06_Engine/retrieval/tests",
    "03_Agents-and-Skills/Skills/traffic-light-decisions/tests",
]


@dataclass
class Row:
    name: str
    kind: str  # MUST | SHOULD
    verdict: str  # PASS | FAIL | WARN | SKIP
    evidence: str
    detail: str = ""
    seconds: float = 0.0


def run(*args: str, timeout: int = 900) -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        process = subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    return process.returncode, (process.stdout + process.stderr).strip()


def tail(text: str, lines: int = 15) -> str:
    return "\n".join(text.splitlines()[-lines:])


def command_row(name: str, kind: str, evidence: str, *args: str, timeout: int = 900) -> Row:
    started = time.monotonic()
    code, output = run(*args, timeout=timeout)
    verdict = "PASS" if code == 0 else ("FAIL" if kind == "MUST" else "WARN")
    return Row(name, kind, verdict, evidence, "" if code == 0 else tail(output), time.monotonic() - started)


def entry_points_row() -> Row:
    problems = []
    for required in ("AGENTS.md", "AUTHORITIES.md", "agency.yaml", "00_Agentic-OS/README.md", "SETUP.md", "README.md"):
        if not (ROOT / required).is_file():
            problems.append(f"missing {required}")
    for adapter in ("CLAUDE.md", ".github/copilot-instructions.md"):
        path = ROOT / adapter
        if not path.is_file():
            problems.append(f"missing {adapter}")
            continue
        text = path.read_text(encoding="utf-8")
        if "AGENTS.md" not in text:
            problems.append(f"{adapter} must route to AGENTS.md")
        lines = len(text.splitlines())
        if lines > ADAPTER_MAX_LINES:
            problems.append(f"{adapter} has {lines} lines; keep runtime adapters ≤ {ADAPTER_MAX_LINES} and policy in AGENTS.md")
    try:
        load_config(ROOT)
    except ConfigError as error:
        problems.append(f"agency.yaml: {error}")
    return Row("Agent entry points route to AGENTS.md", "MUST", "FAIL" if problems else "PASS",
               "AGENTS.md canonical; CLAUDE.md and copilot-instructions thin adapters", "\n".join(problems))


def plugins_row() -> tuple[Row, Row]:
    try:
        profiles = load_profiles(ROOT)
        states = plugin_states(ROOT)
        catalog = build_catalog(ROOT)
    except Exception as error:  # noqa: BLE001 - report any profile failure as a failed gate
        return (Row("Plug-in profiles valid; mounted plug-ins recognised", "MUST", "FAIL",
                    "06_Engine/plugins/*.plugin.yaml", str(error)),
                Row("Registered plug-ins checked out", "SHOULD", "SKIP", "profiles invalid"))
    problems = [f"{name}: {issue}" for name, state in states.items()
                if state.present or state.registered for issue in state.issues if "not checked out" not in issue]
    problems += list(catalog.errors)
    pending = [name for name, state in states.items() if state.registered and not state.present]
    plugged = [name for name, state in states.items() if state.enabled]
    profile_row = Row("Plug-in profiles valid; mounted plug-ins recognised", "MUST", "FAIL" if problems else "PASS",
                      f"{len(profiles)} profiles; plugged in: {', '.join(plugged) or 'none'}", "\n".join(problems))
    mount_row = Row("Registered plug-ins checked out", "SHOULD", "WARN" if pending else "PASS",
                    "submodules initialised" if not pending else f"not checked out: {', '.join(pending)}",
                    "run: python3 06_Engine/scripts/agency.py plugin add <name>" if pending else "")
    return profile_row, mount_row


def plugin_health_row() -> Row:
    """Run every mounted plug-in's declared read-only checks (a new pin must still pass them)."""
    started = time.monotonic()
    try:
        states = plugin_states(ROOT)
    except Exception as error:  # noqa: BLE001
        return Row("Mounted plug-ins pass their declared checks", "MUST", "FAIL", "profiles invalid", str(error))
    mounted = [state for state in states.values() if state.recognized]
    if not mounted:
        return Row("Mounted plug-ins pass their declared checks", "MUST", "PASS", "no plug-in mounted")
    failures, blocked, failing = [], [], []
    for state in mounted:
        python = resolve_python(state)
        missing = requirement_issues(state, python)
        if missing:
            blocked.append(f"{state.profile.name}: " + "; ".join(missing))
            continue
        for result in run_checks(ROOT, state, kind="checks", python=python):
            if not result.ok:
                failures.append(f"{state.profile.name}/{result.name}: {result.skipped or result.detail}")
                if state.profile.name not in failing:
                    failing.append(state.profile.name)
    names = ", ".join(state.profile.name for state in mounted)
    if failures:
        try:
            coverage = binding_coverage(build_catalog(ROOT))
        except Exception:  # noqa: BLE001 — the hint is advisory; the failure itself is already recorded
            coverage = {}
        hints = [f"{name} binds skills this host lacks ({len(coverage[name]['gaps'])}); add its companions: "
                 f"{companion_hint(coverage[name]) or 'see 00_README/PLUGINS.md#engine-skill-bindings'}"
                 for name in failing if coverage.get(name, {}).get("gaps")]
        return Row("Mounted plug-ins pass their declared checks", "MUST", "FAIL",
                   f"failing: {', '.join(failing)} (of {names})", "\n".join(hints + failures),
                   time.monotonic() - started)
    if blocked:
        return Row("Mounted plug-ins pass their declared checks", "MUST", "WARN", f"{names} (not all runnable here)",
                   "\n".join(blocked) + "\nset AGENCY_PYTHON or install the plug-in requirements", time.monotonic() - started)
    return Row("Mounted plug-ins pass their declared checks", "MUST", "PASS", names, "", time.monotonic() - started)


def privacy_row() -> Row:
    """Personal data, client terms and file metadata: blocking for the blank template, advisory in a workspace."""
    try:
        mode = load_config(ROOT).mode
    except ConfigError:
        mode = "template"
    kind = "MUST" if mode == "template" else "SHOULD"
    return command_row("No personal data, client terms or file metadata", kind,
                       "emails, IDs, meeting/doc links, credentials, binary metadata, local denylists",
                       PY, "06_Engine/harness/check-privacy.py")


def bindings_row() -> Row:
    """Engines name the skills their nodes load; report how many this host can resolve."""
    try:
        coverage = binding_coverage(build_catalog(ROOT))
    except Exception as error:  # noqa: BLE001
        return Row("Engine skill bindings resolve in this host", "SHOULD", "WARN", "could not read bindings", str(error))
    if not coverage:
        return Row("Engine skill bindings resolve in this host", "SHOULD", "PASS", "no engine with skill bindings mounted")
    evidence = ", ".join(f"{name} {len(c['resolved'])}/{len(c['bound'])}"
                         + (f" (+{len(c['tenant'])} tenant)" if c["tenant"] else "") for name, c in coverage.items())
    lines = []
    for name, entry in coverage.items():
        if entry["gaps"]:
            hint = companion_hint(entry)
            lines.append(f"{name} missing: {', '.join(entry['gaps'])}"
                         + (f"\n  add companions: {hint}" if hint else ""))
        if entry["tenant"]:
            lines.append(f"{name} tenant integrations (a fork supplies them; the template ships none): "
                         + ", ".join(entry["tenant"]))
    gaps = any(entry["gaps"] for entry in coverage.values())
    if gaps:
        lines.append("see 00_README/PLUGINS.md#engine-skill-bindings")
    return Row("Engine skill bindings resolve in this host", "SHOULD", "WARN" if gaps else "PASS", evidence, "\n".join(lines))


def tests_row() -> Row:
    started = time.monotonic()
    failures = []
    for suite in TEST_SUITES:
        if not (ROOT / suite).is_dir():
            failures.append(f"missing suite {suite}")
            continue
        code, output = run(PY, "-B", "-m", "unittest", "discover", "-s", suite, "-t", suite, timeout=1800)
        if code != 0:
            failures.append(f"{suite}:\n{tail(output, 20)}")
    return Row("Unit tests (engine, retrieval, decision validator)", "MUST", "FAIL" if failures else "PASS",
               ", ".join(TEST_SUITES), "\n".join(failures), time.monotonic() - started)


def review(fast: bool) -> list[Row]:
    rows = [
        command_row("Six canonical L0–L5 contracts", "MUST", "exactly one accepted canonical ADR per layer",
                    PY, DECISIONS, "00_Agentic-OS/decisions", "--canonical", "--expected-count", "6",
                    "--expected-layers", *LAYERS, "--quiet"),
        command_row("Decision records valid", "MUST", "typed records, lifecycle, Traffic Light, supersession",
                    PY, DECISIONS, "--repo-root", ".", "--quiet"),
        entry_points_row(),
        command_row("Native skill spec (portable triggers)", "MUST", "name == folder, description with 'Use when'",
                    PY, "06_Engine/harness/spec-compliance.py"),
        command_row("Native skill contracts", "MUST", "executable ≥10/12 or explicitly exempt",
                    PY, "06_Engine/harness/lint-skill.py", "--contract"),
        command_row("Skill lints clean", "MUST", "declared lints report no errors",
                    PY, "06_Engine/harness/lint-skill.py", "--all", "--severity", "error"),
        command_row("SOP contracts", "MUST", "02_Workflows/SOPs front-matter contract",
                    PY, "06_Engine/harness/lint-sop.py"),
        command_row("Capability map integrity", "MUST", "00_README/domain-coverage-map.md records resolve",
                    PY, "06_Engine/harness/check-capability-map.py", "--integrity-only"),
        command_row("Capability map reviewed within 90 days", "SHOULD", "re-verify before claiming current coverage",
                    PY, "06_Engine/harness/check-capability-map.py"),
        command_row("Capability catalog current", "MUST", "03_Agents-and-Skills/INDEX.md matches sources",
                    PY, "06_Engine/harness/build-skill-index.py", "--check"),
        command_row("Discovery links in sync", "MUST", ".github/* and .claude/* match the catalog",
                    PY, "06_Engine/scripts/agency.py", "sync", "--check"),
        *plugins_row(),
        bindings_row(),
        command_row("Links resolve (incl. depth parity)", "MUST", "relative links, wiki-links, through discovery links",
                    PY, "06_Engine/harness/check-links.py"),
        command_row("Repository hygiene", "MUST", "mode rules, no noise files, no personal paths, URL submodules",
                    PY, "06_Engine/harness/check-template.py"),
        privacy_row(),
        command_row("Wiki indexes current", "SHOULD", "hub _wiki/index.* match pages",
                    PY, "06_Engine/retrieval/build-wiki-index.py", "--check"),
    ]
    if fast:
        rows.append(Row("Mounted plug-ins pass their declared checks", "MUST", "SKIP", "--fast"))
        rows.append(Row("Golden evals", "MUST", "SKIP", "--fast"))
        rows.append(Row("Unit tests (engine, retrieval, decision validator)", "MUST", "SKIP", "--fast"))
    else:
        rows.append(plugin_health_row())
        rows.append(command_row("Golden evals", "MUST", "lint rules still catch their target violations",
                                PY, "06_Engine/evals/run-evals.py"))
        rows.append(tests_row())
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fast", action="store_true", help="skip unit tests and evals")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--contracts-only", action="store_true", help="validate only the six L0–L5 contracts (JSON)")
    args = parser.parse_args()
    if args.contracts_only:
        code, output = run(PY, DECISIONS, "00_Agentic-OS/decisions", "--canonical", "--expected-count", "6",
                           "--expected-layers", *LAYERS, "--json")
        print(output)
        return code
    rows = review(args.fast)
    failed = [row for row in rows if row.kind == "MUST" and row.verdict == "FAIL"]
    verdict = "PASS" if not failed else "ITERATE"
    if args.json:
        print(json.dumps({"verdict": verdict, "rows": [row.__dict__ for row in rows]}, indent=2, default=str))
        return 0 if not failed else 1
    width = max(len(row.name) for row in rows)
    print(f"{'ROW'.ljust(width)}  KIND    VERDICT  EVIDENCE")
    print("-" * (width + 60))
    for row in rows:
        print(f"{row.name.ljust(width)}  {row.kind:<6}  {row.verdict:<7}  {row.evidence}")
    print("-" * (width + 60))
    counts = {key: sum(row.verdict == key for row in rows) for key in ("PASS", "FAIL", "WARN", "SKIP")}
    print(f"VERDICT: {verdict}   ({counts['PASS']} pass, {counts['FAIL']} fail, {counts['WARN']} warn, {counts['SKIP']} skip)")
    for row in rows:
        if row.detail and row.verdict in ("FAIL", "WARN"):
            print(f"\n## {row.verdict}: {row.name}\n{row.detail}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
