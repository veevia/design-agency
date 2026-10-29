"""Shared builders for engine tests: disposable host repositories and fixture plug-ins."""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
REPO = ENGINE.parent
CLI = ENGINE / "scripts" / "agency.py"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Agency Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Agency Test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    return path


def git(cwd: Path, *args: str) -> str:
    env = dict(os.environ, **GIT_ENV)
    result = subprocess.run(["git", "-c", "protocol.file.allow=always", "-c", "init.defaultBranch=main", *args],
                            cwd=cwd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout


def skill(root: Path, slug: str, *, extra: str = "", body: str = "Body.\n") -> Path:
    return write(root / "03_Agents-and-Skills" / "Skills" / slug / "SKILL.md", f"""
        ---
        name: {slug}
        title: Do the {slug} thing
        description: Demonstrates {slug}. Use when a test needs a native skill.
        status: stable
        contract-exempt: "test fixture"
        done_when:
          - the test passes
        {extra}
        ---
        # {slug}

        **TL;DR:** Fixture.

        {body}
        """)


def make_host(tmp: Path, *, mode: str = "template", targets: str = "[copilot, claude]",
              plugin_source: Path | None = None, init_git: bool = True) -> Path:
    root = tmp / "host"
    root.mkdir()
    write(root / "agency.yaml", f"""
        schema: agency/v1
        name: test-host
        mode: {mode}
        discovery:
          targets: {targets}
        plugins: {{}}
        """)
    skill(root, "demo-skill")
    write(root / "03_Agents-and-Skills" / "Agents" / "demo-agent.agent.md", """
        ---
        name: Demo Agent
        description: "Fixture agent. Use when a test needs an agent."
        ---
        # Demo agent
        """)
    write(root / "02_Workflows" / "prompts" / "demo-prompt.prompt.md", """
        ---
        description: "Fixture prompt"
        agent: agent
        ---
        # /demo-prompt
        """)
    write(root / "02_Workflows" / "prompts" / "gated-adapter.prompt.md", """
        ---
        description: "Drives the fixture plug-in"
        agent: agent
        ---
        # /gated-adapter
        """)
    write(root / "01_Project-Hubs" / "README.md", "# Hubs\n")
    write(root / "01_Project-Hubs" / "_template-project" / "README.md", "# Template hub\n")
    source = str(plugin_source) if plugin_source else "https://example.invalid/fixture.git"
    write(root / "06_Engine" / "plugins" / "fixture.plugin.yaml", f"""
        schema: agency-plugin/v1
        name: fixture
        title: Fixture plug-in
        summary: Test double with skills, an agent, a command, a check and a misbehaving smoke step.
        kind: mixed
        mount: 03_Agents-and-Skills/Skills/fixture-kit
        default_edition: main
        host_adapters:
          prompts: [gated-adapter]
        editions:
          main:
            source: {source}
            marker: fixture.json
            provides:
              skills: [skills/*/SKILL.md]
              agents: [agents/*.agent.md]
              prompts:
                - glob: commands/*.md
                  prefix: fx-
                  targets: [claude]
            checks:
              - name: ok
                run: ["{{python}}", check.py]
            smoke:
              - name: scribble
                run: ["{{python}}", scribble.py]
              - name: needs-tool
                run: ["{{python}}", check.py]
                requires: [agency-test-missing-tool]
              - name: ignored-write
                run: ["{{python}}", ignored.py]
              - name: host-write
                run: ["{{python}}", host.py, "{{root}}"]
        """)
    if init_git:
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "init")
    return root


def make_plugin_repo(tmp: Path) -> Path:
    source = tmp / "fixture-plugin"
    write(source / "fixture.json", '{"name": "fixture"}\n')
    for slug in ("alpha-skill", "beta-skill"):
        write(source / "skills" / slug / "SKILL.md", f"""
            ---
            name: {slug}
            description: Fixture plug-in skill {slug}. Use when testing plug-in discovery.
            ---
            # {slug}
            """)
    write(source / "agents" / "fixture-reviewer.agent.md", """
        ---
        name: Fixture Reviewer
        description: "Reviews fixtures. Use when testing plug-in agents."
        ---
        # Fixture reviewer
        """)
    write(source / "commands" / "run.md", "---\ndescription: Run the fixture\n---\n# run\n")
    write(source / "check.py", "print('fixture ok')\n")
    write(source / "scribble.py", "open('scribble.txt', 'w').write('undeclared write')\n")
    write(source / ".gitignore", "ignored-cache/\n")
    write(source / "ignored.py", "import os\nos.makedirs('ignored-cache', exist_ok=True)\nopen('ignored-cache/x', 'w').write('x')\n")
    write(source / "host.py", "import sys, pathlib\npathlib.Path(sys.argv[1], 'stray.txt').write_text('host write')\n")
    write(source / "graph" / "workflow.yaml", "nodes:\n  - id: n1\n    skills: [alpha-skill, helper-skill]\n")
    git(source, "init", "-q")
    git(source, "add", "-A")
    git(source, "commit", "-q", "-m", "fixture plug-in")
    return source


def run_cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, AGENCY_ROOT=str(root), PYTHONDONTWRITEBYTECODE="1", **GIT_ENV)
    env.pop("AGENCY_PYTHON", None)
    return subprocess.run([sys.executable, str(CLI), *args], cwd=root, capture_output=True, text=True, env=env)


def load_harness(filename: str):
    """Import a hyphenated harness script (e.g. check-template.py) as a module."""
    import importlib.util

    path = ENGINE / "harness" / filename
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_").removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
