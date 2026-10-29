#!/usr/bin/env python3
"""agency — operate a Design Agency OS repository: status, plug-ins, discovery, hubs, checks.

    python3 06_Engine/scripts/agency.py status
    python3 06_Engine/scripts/agency.py plugin list
    python3 06_Engine/scripts/agency.py plugin add fde-design-toolkit [--edition full] [--source URL_OR_PATH]
    python3 06_Engine/scripts/agency.py plugin add prototype-design --with-companions
    python3 06_Engine/scripts/agency.py plugin status|check|smoke|report|remove <name>
    python3 06_Engine/scripts/agency.py sync [--check]
    python3 06_Engine/scripts/agency.py hub new <slug>
    python3 06_Engine/scripts/agency.py check [--fast]
    python3 06_Engine/scripts/agency.py publish-check [--ref main] [--remote origin]

Exit codes: 0 success, 1 a check failed / drift found / plug-in not plugged in, 2 usage or configuration error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE_DIR))

from agency import catalog as catalog_mod  # noqa: E402
from agency import discovery, plugins, report  # noqa: E402
from agency.config import (  # noqa: E402
    HUBS_DIR,
    TEMPLATE_HUB,
    ConfigError,
    load_config,
    set_mode,
)

ROOT = Path(os.environ.get("AGENCY_ROOT", ENGINE_DIR.parent)).resolve()
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _rel(path: Path) -> str:
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)


def _table(rows: list[list[str]], header: list[str]) -> str:
    widths = [max(len(str(cell)) for cell in column) for column in zip(header, *rows)] if rows else [len(h) for h in header]
    line = "  ".join(f"{{:<{width}}}" for width in widths)
    out = [line.format(*header), line.format(*["-" * width for width in widths])]
    out += [line.format(*[str(cell) for cell in row]) for row in rows]
    return "\n".join(out)


def _pinned(state: plugins.PluginState) -> str:
    if not state.present or not (state.path / ".git").exists():
        return "-"
    result = subprocess.run(["git", "-C", str(state.path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() or "-"


def _sync(check: bool) -> int:
    """Discovery links and the capability catalog, together: write both, or (check) verify both."""
    result = discovery.plan(ROOT)
    print(discovery.summary(result))
    for error in result.errors:
        print(f"  ERROR: {error}")
    for issue in result.issues:
        print(f"  note: {issue}")
    for path in result.deferred:
        print(f"  deferred (plug-in not checked out): {_rel(path)}")
    if check:
        for link in result.create:
            print(f"  missing: {_rel(link.path)} -> {link.target}")
        for link in result.update:
            print(f"  outdated: {_rel(link.path)} -> {link.target}")
        for path in result.remove:
            print(f"  stale: {_rel(path)}")
        for conflict in result.conflicts:
            print(f"  CONFLICT: {conflict}")
        if result.drift:
            print("DRIFT: run python3 06_Engine/scripts/agency.py sync")
        if result.errors:
            print("ERRORS: fix the plug-in profile or mount listed above")
        catalog_rc = _catalog(check=True)
        if result.failed or catalog_rc:
            return 1
        print("discovery: in sync")
        return 0
    catalog_rc = _catalog(check=False)  # independent of link conflicts, so rebuild it first
    discovery.apply(ROOT, result)
    print("discovery: updated" + (" (with errors above)" if result.errors else ""))
    return 1 if result.errors or catalog_rc else 0


def _catalog(check: bool) -> int:
    """The catalog (03_Agents-and-Skills/INDEX.md) is derived from the same sources as discovery."""
    script = Path(__file__).resolve().parents[1] / "harness" / "build-skill-index.py"
    if not script.is_file():
        return 0
    command = [sys.executable, "-B", str(script), "--root", str(ROOT)] + (["--check"] if check else [])
    process = subprocess.run(command, capture_output=True, text=True)
    message = (process.stdout + process.stderr).strip()
    if message:
        print(message.replace("run python3 06_Engine/harness/build-skill-index.py",
                              "run python3 06_Engine/scripts/agency.py sync"))
    return process.returncode


# --------------------------------------------------------------------------- commands


def cmd_status(args) -> int:
    config = load_config(ROOT)
    cat = catalog_mod.build_catalog(ROOT, config)
    hubs = sorted(p.name for p in (ROOT / HUBS_DIR).iterdir() if p.is_dir()) if (ROOT / HUBS_DIR).is_dir() else []
    counts: dict[tuple[str, str], int] = {}
    for item in cat.items:
        key = ("native" if item.origin == "native" else "plug-in", item.surface)
        counts[key] = counts.get(key, 0) + 1
    gated = sum(len(names) for names in cat.gated.values())
    plan = discovery.plan(ROOT, config, cat)
    print(f"Design Agency OS · {config.name} · mode: {config.mode} · discovery targets: {', '.join(config.targets)}")
    print(f"Hubs: {', '.join(hubs) or 'none'}")
    print("Native: " + ", ".join(f"{surface} {counts.get(('native', surface), 0)}" for surface in ("skills", "agents", "prompts"))
          + f" · host adapters waiting for a plug-in: {gated}")
    print("Plug-ins:")
    rows = [[name, state.status, state.edition or "-", state.profile.kind, str(state.mount)] for name, state in cat.states.items()]
    print(_table(rows, ["name", "status", "edition", "kind", "mount"]))
    print(discovery.summary(plan) + (" · DRIFT" if plan.drift else " · in sync"))
    for error in cat.errors:
        print(f"ERROR: {error}")
    for issue in cat.issues:
        print(f"note: {issue}")
    return 1 if cat.errors else 0


def cmd_sync(args) -> int:
    return _sync(args.check)


def cmd_check(args) -> int:
    review = ROOT / "00_Agentic-OS" / "agentic-os-review.py"
    return subprocess.run([sys.executable, str(review), *args.review_args], cwd=ROOT).returncode


def _git_out(*args: str) -> tuple[int, str]:
    process = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return process.returncode, process.stdout.strip() if process.returncode == 0 else process.stderr.strip()


def _publish_step(label: str, command: list[str], limit: int = 25) -> int:
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                             env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    lines = (process.stdout + process.stderr).strip().splitlines()
    print(f"{'PASS' if process.returncode == 0 else 'FAIL'}  {label}")
    shown = lines[-1:] if process.returncode == 0 else lines[:limit] + ([lines[-1]] if len(lines) > limit else [])
    for line in shown:
        print(f"        {line}")
    if process.returncode and len(lines) > limit + 1:
        print(f"        … {len(lines) - limit - 1} more (run the step's command for the full list)")
    return 0 if process.returncode == 0 else 1


def _privacy_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_privacy", Path(__file__).resolve().parents[1] / "harness" / "check-privacy.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def cmd_publish_check(args) -> int:
    """Everything that would leave with a public push: the tree, the full history of REF, and the remote."""
    harness = Path(__file__).resolve().parents[1] / "harness"
    config = load_config(ROOT)
    code, target = _git_out("rev-parse", "--verify", f"{args.ref}^{{commit}}")
    if code:
        raise ConfigError(f"unknown ref {args.ref!r}: {target}")
    print(f"publish check · {config.name} · {args.ref} = {target[:12]} · mode: {config.mode}")
    failed = 0
    _, head = _git_out("rev-parse", "--verify", "HEAD^{commit}")
    _, dirty = _git_out("status", "--porcelain", "--untracked-files=no")
    if head != target or dirty:
        print(f"FAIL  the working tree is not a clean checkout of {args.ref}: the tree and template checks would test "
              f"something else (switch to {args.ref} and commit or stash changes)")
        failed = 1
    if config.mode != "template" and not args.allow_workspace:
        print("FAIL  mode is workspace: a published template must be blank (agency.yaml mode: template)")
        failed = 1
    allow = [flag for domain in args.allow_email_domain for flag in ("--allow-email-domain", domain)]
    failed |= _publish_step("tree: no personal data, client terms or file metadata",
                            [sys.executable, str(harness / "check-privacy.py"), "--root", str(ROOT), *allow])
    failed |= _publish_step(f"history of {args.ref}: blobs, file names, messages and commit identities",
                            [sys.executable, str(harness / "check-privacy.py"), "--root", str(ROOT), "--history", target, *allow])
    failed |= _publish_step("hygiene and template-mode rules", [sys.executable, str(harness / "check-template.py"), "--root", str(ROOT)])
    _, branches = _git_out("for-each-ref", "--format=%(refname:short) %(objectname)", "refs/heads", "refs/tags")
    others = [name for name, sha in (line.split() for line in branches.splitlines() if line)
              if _git_out("merge-base", "--is-ancestor", sha, target)[0] != 0]
    if others:
        print(f"note  local refs with history outside {args.ref} (never push them): {', '.join(others)}")
    if args.remote:
        code, listing = _git_out("ls-remote", args.remote)
        if code:
            print(f"FAIL  cannot list {args.remote}: {listing}")
            failed = 1
        else:
            privacy = _privacy_module()
            denylist = privacy.load_denylist(ROOT)
            stale, named = [], []
            for line in listing.splitlines():
                sha, refname = line.split("\t", 1)
                if refname == "HEAD" or refname.endswith("^{}"):
                    continue
                named += [f"{refname} (denylisted term {term!r})"
                          for term in privacy.denylist_hits(refname.split("/", 2)[-1], denylist)]
                if sha == target or _git_out("merge-base", "--is-ancestor", sha, target)[0] == 0:
                    continue
                hint = ("pull request refs cannot be deleted by the owner: publish from a fresh repository"
                        if refname.startswith("refs/pull/") else f"delete it or replace it with {args.ref} before publishing")
                stale.append(f"{refname} ({sha[:8]}) holds other history: {hint}")
            print(f"{'FAIL' if stale else 'PASS'}  remote {args.remote}: every ref is {args.ref} or part of its history")
            for ref in stale:
                print(f"        {ref}")
            print(f"{'FAIL' if named else 'PASS'}  remote {args.remote}: ref names carry no denylisted terms")
            for ref in named:
                print(f"        {ref}")
            failed |= 1 if stale or named else 0
        print("note  hosts can keep unreachable commits and forks after a rewrite; for a repository that once held "
              "confidential data, publish from a fresh repository or ask the host to purge cached objects")
    print("publish check: " + ("READY" if not failed else "NOT READY"))
    return 1 if failed else 0


def cmd_plugin_list(args) -> int:
    states = plugins.plugin_states(ROOT)
    rows = [[name, s.status, s.edition or "-", s.profile.kind, ", ".join(s.profile.editions), s.profile.title]
            for name, s in states.items()]
    print(_table(rows, ["name", "status", "edition", "kind", "editions", "title"]))
    print("\nAdd one with: python3 06_Engine/scripts/agency.py plugin add <name> [--edition <edition>]")
    return 0


def _state(name: str) -> plugins.PluginState:
    states = plugins.plugin_states(ROOT)
    if name not in states:
        raise plugins.PluginError(f"unknown plug-in {name!r}; known: {', '.join(sorted(states))}")
    return states[name]


def cmd_plugin_status(args) -> int:
    state = _state(args.name)
    profile = state.profile
    entry = plugins.read_gitmodules(ROOT).get(str(state.mount), {})
    print(f"{profile.title} ({profile.name}) — {state.status}")
    print(f"  kind: {profile.kind} · mount: {state.mount} · edition: {state.edition or '-'} · pinned: {_pinned(state)}")
    print(f"  source: {entry.get('url') or profile.editions[profile.default_edition].source}")
    if state.recognized:
        found, errors, issues = plugins.contributions(state)
        by_surface: dict[str, list[str]] = {}
        for item in found:
            by_surface.setdefault(item.surface, []).append(item.name)
        if not state.enabled:
            print("  hidden from discovery by agency.yaml (enabled: false)")
        for surface, names in sorted(by_surface.items()):
            print(f"  {surface} ({len(names)}): {', '.join(sorted(names))}")
        if not by_surface:
            print("  contributes nothing to discovery")
        for error in errors:
            print(f"  ERROR: {error}")
        coverage = catalog_mod.binding_coverage(catalog_mod.build_catalog(ROOT)).get(profile.name)
        if coverage:
            _print_bindings(coverage)
        if profile.host_adapters:
            print("  unlocks host adapters: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in profile.host_adapters.items()))
        python = plugins.resolve_python(state, args.python)
        problems = plugins.requirement_issues(state, python)
        print(f"  python: {python}")
        for problem in problems:
            print(f"  requirement: {problem}")
        for issue in issues + list(state.issues):
            print(f"  note: {issue}")
        if profile.project:
            print("  projects: " + ", ".join(f"{k}={v}" for k, v in profile.project.items()))
        return 1 if errors or state.issues else 0
    for issue in state.issues:
        print(f"  note: {issue}")
    companions = (profile.skill_bindings or {}).get("companions") or ()
    if companions:
        print("  companions (supply skills its graph binds): "
              + ", ".join(c["plugin"] + (f" (edition {c['edition']})" if c["edition"] else "") for c in companions))
    print(f"  plug it in: python3 06_Engine/scripts/agency.py plugin add {profile.name}"
          + (f" [--edition {'|'.join(profile.editions)}]" if len(profile.editions) > 1 else ""))
    return 1


def _print_bindings(coverage: dict) -> None:
    print(f"  skill bindings: {len(coverage['resolved'])}/{len(coverage['bound'])} resolve in this host")
    if coverage["gaps"]:
        print(f"    missing: {', '.join(coverage['gaps'])}")
    if coverage["tenant"]:
        print(f"    tenant integrations (your fork supplies them): {', '.join(coverage['tenant'])}")
    hint = catalog_mod.companion_hint(coverage)
    if hint:
        print(f"    companion plug-ins not plugged in: {hint}")


def _print_results(results: list[plugins.CheckResult]) -> int:
    failed = 0
    for result in results:
        if result.skipped:
            label = "SKIP " if result.ok else "BLOCKED"
            failed += 0 if result.ok else 1
            print(f"  {label} {result.name}: {result.skipped}")
            continue
        mark = "PASS" if result.ok else "FAIL"
        failed += 0 if result.ok else 1
        print(f"  {mark}  {result.name} ({result.seconds:.1f}s)")
        if result.detail and (not result.ok or result.name == "scratch"):
            print("        " + result.detail.replace("\n", "\n        "))
    return failed


def _run(state: plugins.PluginState, kind: str, args) -> int:
    python = plugins.resolve_python(state, args.python)
    problems = plugins.requirement_issues(state, python)
    print(f"{state.profile.name} {kind} (python: {python})")
    if problems:
        for problem in problems:
            print(f"  BLOCKED  {problem}")
        return 1
    results = plugins.run_checks(
        ROOT, state, kind=kind, python=python, only=args.only,
        allow_mount_writes=getattr(args, "allow_mount_writes", False), keep_temp=getattr(args, "keep_temp", False),
    )
    if not results:
        print(f"  (no {kind} declared)")
        return 0
    return 1 if _print_results(results) else 0


def cmd_plugin_check(args) -> int:
    return _run(_state(args.name), "checks", args)


def cmd_plugin_smoke(args) -> int:
    return _run(_state(args.name), "smoke", args)


def _add_companions(name: str) -> tuple[int, list[str]]:
    """Add the companion plug-ins an engine's profile names; report each failure and keep going."""
    profile = plugins.load_profiles(ROOT).get(name)
    if profile is None:
        raise plugins.PluginError(f"unknown plug-in {name!r}")
    companions = (profile.skill_bindings or {}).get("companions") or ()
    if not companions:
        print(f"  {name} declares no companions")
        return 0, []
    rc, mounts = 0, []
    for companion in companions:
        state = _state(companion["plugin"])
        wanted = companion["edition"]
        if state.override.enabled is False:
            print(f"  companion {companion['plugin']}: hidden by agency.yaml (enabled: false), so its skills stay "
                  "unavailable; remove that override to use it")
            rc = 1
            continue
        if state.enabled and wanted in (None, state.edition):
            print(f"  companion {companion['plugin']}: already plugged in ({state.edition})")
            continue
        try:
            added, notes = plugins.add_plugin(ROOT, companion["plugin"], edition=wanted)
        except plugins.PluginError as error:
            print(f"  companion {companion['plugin']}: NOT ADDED — {error}")
            rc = 1
            continue
        for note in notes:
            print(f"  {note}")
        print(f"  companion {added.profile.name}: plugged in (edition {added.edition})")
        mounts.append(str(added.mount))
    return rc, mounts


def _mounted() -> int:
    """After any mount: leave template mode and regenerate discovery links and the catalog."""
    config = load_config(ROOT)
    if config.exists and config.mode == "template":
        set_mode(ROOT, "workspace")
        print("  agency.yaml: mode template → workspace (this repository now carries a plug-in)")
    return _sync(check=False)


def cmd_plugin_add(args) -> int:
    rc, mounts = _add_companions(args.name) if args.with_companions else (0, [])
    try:
        state, notes = plugins.add_plugin(ROOT, args.name, edition=args.edition, source=args.source, branch=args.branch)
    except plugins.PluginError:
        if mounts:  # keep the companions that were mounted consistent before reporting the failure
            _mounted()
        raise
    for note in notes:
        print(f"  {note}")
    rc |= _mounted()
    print(f"{state.profile.title} plugged in: edition {state.edition} at {state.mount}")
    coverage = catalog_mod.binding_coverage(catalog_mod.build_catalog(ROOT)).get(state.profile.name)
    if coverage:
        _print_bindings(coverage)
        if coverage["gaps"]:
            print("    nodes that bind a missing skill cannot load it (some engines also fail validation);"
                  f" add the companions, then re-run: agency.py plugin check {state.profile.name}")
    if not args.no_check:
        rc |= _run(plugins.plugin_state(ROOT, state.profile), "checks", args)
    print("\nNext: review, then commit the plug-in pin and generated links, for example:")
    print(f"  git add .gitmodules {' '.join([*mounts, str(state.mount)])} agency.yaml .github .claude 03_Agents-and-Skills/INDEX.md"
          f" && git commit -m \"feat(plugins): add {state.profile.name}\"")
    return rc


def cmd_plugin_remove(args) -> int:
    for note in plugins.remove_plugin(ROOT, args.name, force=args.force):
        print(f"  {note}")
    return _sync(check=False)


def cmd_plugin_report(args) -> int:
    state = _state(args.name)
    if not state.enabled:
        print(f"{args.name} is not plugged in ({state.status}); run: python3 06_Engine/scripts/agency.py plugin add {args.name}")
        return 1
    found, errors, issues = plugins.contributions(state)
    issues = errors + issues
    skills = sorted((item.source, item.origin) for item in found if item.surface == "skills")
    records = report.portfolio(skills)
    summary = report.summarize(records)
    summary["agents"] = sum(item.surface in ("agents", "claude_agents") for item in found)
    summary["prompts"] = sum(item.surface == "prompts" for item in found)
    coverage = catalog_mod.binding_coverage(catalog_mod.build_catalog(ROOT)).get(args.name)
    if coverage:
        summary["skill_bindings_resolved"] = f"{len(coverage['resolved'])}/{len(coverage['bound'])}"
    if args.json:
        print(json.dumps({
            "plugin": args.name, "edition": state.edition, "pinned": _pinned(state), "summary": summary,
            "skills": [{"name": r.name, "path": _rel(r.path), "spec_issues": r.spec_issues, "trigger": r.has_trigger,
                        "mode": r.mode, "score": r.score, "contract_ready": r.contract_ready} for r in records],
            "notes": issues,
            "skill_bindings": coverage,
        }, indent=2))
        return 0
    print(f"{state.profile.title} · edition {state.edition} · pinned {_pinned(state)}")
    for key, value in summary.items():
        print(f"  {key.replace('_', ' ')}: {value}")
    weak = [r for r in records if r.spec_issues or not r.contract_ready]
    if weak:
        print("\nSkills to improve (spec issues or contract score < 10 and not exempt):")
        rows = [[r.name, r.mode, f"{r.score}/12" if r.score is not None else "-", "; ".join(r.spec_issues) or "-"] for r in weak]
        print(_table(rows, ["skill", "mode", "score", "spec issues"]))
    for issue in issues:
        print(f"note: {issue}")
    return 0


def cmd_hub_new(args) -> int:
    if not SLUG.fullmatch(args.slug):
        raise ConfigError("hub slug must be lowercase kebab-case, for example example-project")
    source = ROOT / HUBS_DIR / TEMPLATE_HUB
    target = ROOT / HUBS_DIR / args.slug
    if not source.is_dir():
        raise ConfigError(f"{_rel(source)} is missing")
    if target.exists():
        raise ConfigError(f"{_rel(target)} already exists")
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    print(f"created {_rel(target)} from {_rel(source)}")
    config = load_config(ROOT)
    if config.exists and config.mode == "template":
        set_mode(ROOT, "workspace")
        print("agency.yaml: mode template → workspace (this repository now holds project work)")
    print("Next: set the owner, goal and phase in the hub README, then start W1 (02_Workflows/workflows/W1-understand.md).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agency", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="mode, hubs, capabilities, plug-ins and discovery state").set_defaults(fn=cmd_status)
    p = sub.add_parser("sync", help="generate discovery links (.github/*, .claude/*)")
    p.add_argument("--check", action="store_true", help="report drift without writing")
    p.set_defaults(fn=cmd_sync)
    p = sub.add_parser("check", help="run the full OS review (00_Agentic-OS/agentic-os-review.py)")
    p.add_argument("review_args", nargs=argparse.REMAINDER, help="passed to the review, e.g. --fast or --json")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("publish-check", help="release gate: tree, full history, commit identities and remote refs")
    p.add_argument("--ref", default="HEAD", help="the commit you will publish (default HEAD)")
    p.add_argument("--remote", help="also require every branch and tag on this remote to be REF or its history")
    p.add_argument("--allow-email-domain", action="append", default=[], help="additional allowed email domain")
    p.add_argument("--allow-workspace", action="store_true", help="publish a repository in workspace mode")
    p.set_defaults(fn=cmd_publish_check)
    hub = sub.add_parser("hub", help="project hubs").add_subparsers(dest="hub_command", required=True)
    p = hub.add_parser("new", help="create 01_Project-Hubs/<slug> from the template hub")
    p.add_argument("slug")
    p.set_defaults(fn=cmd_hub_new)
    plug = sub.add_parser("plugin", help="plug-in lifecycle").add_subparsers(dest="plugin_command", required=True)
    plug.add_parser("list", help="known plug-ins and their state").set_defaults(fn=cmd_plugin_list)
    for name, fn, text in (
        ("status", cmd_plugin_status, "state, pin, contributions and requirements (exit 1 when not plugged in)"),
        ("check", cmd_plugin_check, "run the plug-in's read-only health checks"),
        ("smoke", cmd_plugin_smoke, "run the plug-in's smoke steps in a temporary folder"),
        ("report", cmd_plugin_report, "skill portfolio baseline: spec, triggers, contract coverage"),
        ("remove", cmd_plugin_remove, "unmount a submodule plug-in and remove its discovery links"),
    ):
        p = plug.add_parser(name, help=text)
        p.add_argument("name")
        if name in ("status", "check", "smoke"):
            p.add_argument("--python", help="interpreter for the plug-in (default: AGENCY_PYTHON, <mount>/.venv, this python)")
        if name in ("check", "smoke"):
            p.add_argument("--only", help="run one named check")
        if name == "smoke":
            p.add_argument("--allow-mount-writes", action="store_true", help="permit steps declared to write into the mount")
            p.add_argument("--keep-temp", action="store_true", help="keep the scratch folder for inspection")
        if name == "report":
            p.add_argument("--json", action="store_true")
        if name == "remove":
            p.add_argument("--force", action="store_true",
                           help="remove even with local changes or unpushed commits (the cached clone is kept)")
        p.set_defaults(fn=fn)
    p = plug.add_parser("add", help="mount a plug-in (git submodule), wire discovery and run its checks")
    p.add_argument("name")
    p.add_argument("--edition", help="edition to mount (see `plugin list`)")
    p.add_argument("--source", help="git URL or local path overriding the profile source")
    p.add_argument("--branch", help="branch to track")
    p.add_argument("--python", help="interpreter for the plug-in checks")
    p.add_argument("--only", help=argparse.SUPPRESS)
    p.add_argument("--no-check", action="store_true", help="skip the plug-in's health checks")
    p.add_argument("--with-companions", action="store_true",
                   help="first add the plug-ins that supply skills this engine binds (its profile's companions)")
    p.set_defaults(fn=cmd_plugin_add)
    args = parser.parse_args(argv)
    try:
        return args.fn(args)
    except (ConfigError, plugins.PluginError, catalog_mod.CatalogError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
