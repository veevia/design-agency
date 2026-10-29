"""End-to-end plug-in lifecycle through the CLI, with a real local git submodule."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import git, load_harness, make_host, make_plugin_repo, run_cli, write

from agency.config import load_config
from agency.plugins import read_gitmodules


@unittest.skipUnless(shutil.which("git"), "git is required")
class PluginLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.source = make_plugin_repo(base)
        self.root = make_host(base, plugin_source=self.source)
        self.mount = self.root / "03_Agents-and-Skills/Skills/fixture-kit"

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args: str, expect: int = 0):
        result = run_cli(self.root, *args)
        self.assertEqual(result.returncode, expect, f"{args}:\n{result.stdout}\n{result.stderr}")
        return result.stdout

    def test_add_check_smoke_report_remove(self):
        self.assertIn("available", self.cli("plugin", "list"))
        self.cli("plugin", "status", "fixture", expect=1)

        out = self.cli("plugin", "add", "fixture")
        self.assertIn("mode template → workspace", out)
        self.assertIn("PASS  ok", out)
        self.assertEqual(load_config(self.root).mode, "workspace")
        self.assertIn("03_Agents-and-Skills/Skills/fixture-kit", read_gitmodules(self.root))
        for link in (".github/skills/alpha-skill", ".claude/skills/beta-skill",
                     ".github/agents/fixture-reviewer.agent.md", ".claude/commands/fx-run.md",
                     ".github/prompts/gated-adapter.prompt.md"):
            self.assertTrue((self.root / link).exists(), link)
        self.assertFalse((self.root / ".claude/agents/fixture-reviewer.md").exists(), "Copilot agent stays Copilot-only")
        catalog = (self.root / "03_Agents-and-Skills/INDEX.md").read_text()
        self.assertIn("| `alpha-skill` |", catalog, "plug-in add refreshes the catalog engines check bindings against")

        self.cli("sync", "--check")
        self.cli("plugin", "status", "fixture")
        self.cli("plugin", "check", "fixture")

        smoke = self.cli("plugin", "smoke", "fixture", expect=1)
        self.assertIn("UNDECLARED SIDE EFFECT", smoke)
        self.assertIn("BLOCKED needs-tool", smoke, "a required step that cannot run is not a pass")
        self.assertIn("ignored-cache", smoke, "writes to ignored files inside the mount are detected")
        self.assertIn("stray.txt", smoke, "writes into the host repository are detected")
        (self.root / "stray.txt").unlink()

        report = json.loads(self.cli("plugin", "report", "fixture", "--json"))
        self.assertEqual(report["summary"]["skills"], 2)
        self.assertEqual(report["summary"]["agents"], 1)

        hygiene = load_harness("check-template.py").check(self.root)
        self.assertTrue(any("local source" in problem for problem in hygiene), "local submodule source is flagged")

        refused = run_cli(self.root, "plugin", "remove", "fixture")
        self.assertEqual(refused.returncode, 2)
        self.assertIn("uncommitted change", refused.stderr, "local work in the mount is protected")
        git(self.mount, "clean", "-fdq")
        self.cli("plugin", "remove", "fixture")
        self.assertNotIn("03_Agents-and-Skills/Skills/fixture-kit", read_gitmodules(self.root))
        for link in (".github/skills/alpha-skill", ".github/prompts/gated-adapter.prompt.md", ".claude/commands/fx-run.md"):
            self.assertFalse((self.root / link).is_symlink(), link)
        self.cli("sync", "--check")

    def test_readd_from_another_source_never_reuses_the_old_clone(self):
        other = Path(self.tmp.name) / "other-plugin"
        shutil.copytree(self.source, other, ignore=shutil.ignore_patterns(".git"))
        (other / "skills" / "gamma-skill").mkdir()
        (other / "skills" / "gamma-skill" / "SKILL.md").write_text("---\nname: gamma-skill\n---\n")
        git(other, "init", "-q")
        git(other, "add", "-A")
        git(other, "commit", "-q", "-m", "other source")
        self.cli("plugin", "add", "fixture", "--no-check")
        self.cli("plugin", "remove", "fixture")
        out = self.cli("plugin", "add", "fixture", "--no-check", "--source", str(other))
        self.assertTrue((self.mount / "skills" / "gamma-skill").is_dir(), out)
        self.assertTrue((self.root / ".github/skills/gamma-skill").exists())
        # A cache left by a manual removal must not silently stand in for a different source.
        git(self.root, "submodule", "deinit", "-f", "--", "03_Agents-and-Skills/Skills/fixture-kit")
        git(self.root, "rm", "-q", "-f", "--", "03_Agents-and-Skills/Skills/fixture-kit")
        result = run_cli(self.root, "plugin", "add", "fixture", "--no-check")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cached clone of a different source", result.stderr)

    def test_hidden_plugin_is_still_checkable(self):
        self.cli("plugin", "add", "fixture", "--no-check")
        config = self.root / "agency.yaml"
        config.write_text(config.read_text().replace("plugins: {}", "plugins:\n  fixture:\n    enabled: false"))
        self.cli("sync")
        self.assertFalse((self.root / ".github/skills/alpha-skill").exists(), "hidden from discovery")
        self.assertIn("PASS  ok", self.cli("plugin", "check", "fixture"))

    def test_copies_and_source_switches_are_refused(self):
        (self.mount / "skills").mkdir(parents=True)
        (self.mount / "fixture.json").write_text("{}\n")
        copied = run_cli(self.root, "plugin", "add", "fixture", "--no-check")
        self.assertEqual(copied.returncode, 2)
        self.assertIn("not a registered submodule", copied.stderr)
        shutil.rmtree(self.mount)
        self.cli("plugin", "add", "fixture", "--no-check")
        switched = run_cli(self.root, "plugin", "add", "fixture", "--no-check", "--source", "https://example.invalid/other.git")
        self.assertEqual(switched.returncode, 2)
        self.assertIn("is registered from", switched.stderr)

    def test_shallow_edition_records_shallow_submodule(self):
        profile = self.root / "06_Engine/plugins/fixture.plugin.yaml"
        text = profile.read_text()
        self.assertIn("    marker: fixture.json\n", text)
        profile.write_text(text.replace("    marker: fixture.json\n", "    marker: fixture.json\n    shallow: true\n", 1))
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "shallow profile")
        out = self.cli("plugin", "add", "fixture", "--no-check", "--source", self.source.as_uri())
        self.assertIn("shallow mount", out)
        self.assertEqual(git(self.mount, "rev-parse", "--is-shallow-repository").strip(), "true")
        self.assertEqual(git(self.root, "config", "-f", ".gitmodules",
                             "submodule.03_Agents-and-Skills/Skills/fixture-kit.shallow").strip(), "true")
        self.assertIn(".gitmodules", git(self.root, "diff", "--cached", "--name-only"), "the shallow flag is staged")
        self.assertTrue((self.root / ".github/skills/alpha-skill").exists())

    def bind_helper_companion(self, helper_source: str) -> None:
        write(self.root / "06_Engine/plugins/helper.plugin.yaml", f"""
            schema: agency-plugin/v1
            name: helper
            title: Helper skills
            summary: Supplies a skill the fixture engine binds.
            kind: skills
            mount: 03_Agents-and-Skills/Skills/helper-kit
            editions:
              main:
                source: {helper_source}
                marker: helper.json
                provides:
                  skills: [skills/*/SKILL.md]
            """)
        profile = self.root / "06_Engine/plugins/fixture.plugin.yaml"
        profile.write_text(profile.read_text().replace("editions:\n", (
            "skill_bindings:\n  file: graph/workflow.yaml\n  collection: nodes\n  field: skills\n"
            "  companions: [helper]\neditions:\n"), 1))

    def make_helper_repo(self) -> Path:
        helper = Path(self.tmp.name) / "helper-plugin"
        write(helper / "helper.json", "{}\n")
        write(helper / "skills/helper-skill/SKILL.md",
              "---\nname: helper-skill\ndescription: Helper. Use when testing companions.\n---\n# helper\n")
        git(helper, "init", "-q")
        git(helper, "add", "-A")
        git(helper, "commit", "-q", "-m", "helper")
        return helper

    def test_with_companions_adds_the_skill_suppliers_first(self):
        self.bind_helper_companion(str(self.make_helper_repo()))
        out = self.cli("plugin", "add", "fixture", "--with-companions", "--no-check")
        self.assertIn("companion helper: plugged in", out)
        self.assertIn("skill bindings: 2/2 resolve in this host", out)
        self.assertTrue({"03_Agents-and-Skills/Skills/helper-kit", "03_Agents-and-Skills/Skills/fixture-kit"}
                        <= set(read_gitmodules(self.root)))
        self.assertIn("03_Agents-and-Skills/Skills/helper-kit 03_Agents-and-Skills/Skills/fixture-kit", out,
                      "the commit hint names every mount it added")
        self.assertIn("| `helper-skill` |", (self.root / "03_Agents-and-Skills/INDEX.md").read_text())
        again = self.cli("plugin", "add", "fixture", "--with-companions", "--no-check")
        self.assertIn("companion helper: already plugged in", again)

    def test_unreachable_companion_is_reported_and_the_engine_still_added(self):
        self.bind_helper_companion(str(Path(self.tmp.name) / "no-such-helper"))
        result = run_cli(self.root, "plugin", "add", "fixture", "--with-companions", "--no-check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("companion helper: NOT ADDED", result.stdout)
        self.assertIn("03_Agents-and-Skills/Skills/fixture-kit", read_gitmodules(self.root))
        self.assertIn("missing: helper-skill", result.stdout)
        self.assertIn("companion plug-ins not plugged in: agency.py plugin add helper", result.stdout)

    def test_failed_engine_add_still_wires_the_companions_it_mounted(self):
        self.bind_helper_companion(str(self.make_helper_repo()))
        result = run_cli(self.root, "plugin", "add", "fixture", "--with-companions", "--no-check",
                         "--source", str(Path(self.tmp.name) / "no-such-engine"))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("companion helper: plugged in", result.stdout)
        self.assertEqual(load_config(self.root).mode, "workspace", "a mounted companion leaves template mode")
        self.assertTrue((self.root / ".github/skills/helper-skill").exists(), "the companion is wired")
        self.cli("sync", "--check")

    def test_hidden_companion_is_reported_not_added(self):
        self.bind_helper_companion(str(self.make_helper_repo()))
        config = self.root / "agency.yaml"
        config.write_text(config.read_text().replace("plugins: {}", "plugins:\n  helper:\n    enabled: false"))
        result = run_cli(self.root, "plugin", "add", "fixture", "--with-companions", "--no-check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("companion helper: hidden by agency.yaml", result.stdout)
        self.assertNotIn("03_Agents-and-Skills/Skills/helper-kit", read_gitmodules(self.root))

    def test_remove_inspects_the_cached_clone_when_the_mount_is_not_checked_out(self):
        self.cli("plugin", "add", "fixture", "--no-check")
        git(self.mount, "commit", "--allow-empty", "-q", "-m", "local only")
        git(self.root, "submodule", "deinit", "-f", "--", "03_Agents-and-Skills/Skills/fixture-kit")
        cache = self.root / ".git/modules/03_Agents-and-Skills/Skills/fixture-kit"
        refused = run_cli(self.root, "plugin", "remove", "fixture")
        self.assertEqual(refused.returncode, 2, refused.stdout + refused.stderr)
        self.assertIn("cached clone with commits that no remote branch contains", refused.stderr)
        self.assertTrue(cache.is_dir())
        self.assertIn("kept git's cached clone", self.cli("plugin", "remove", "fixture", "--force"))
        self.assertTrue(cache.is_dir(), "the local-only commit survives in the cache")

    def test_branch_flag_is_checked_against_a_branchless_registration(self):
        self.cli("plugin", "add", "fixture", "--no-check")
        result = run_cli(self.root, "plugin", "add", "fixture", "--no-check", "--branch", "dev")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("tracks no branch", result.stderr)

    def test_sync_check_covers_the_catalog(self):
        self.cli("sync")
        index = self.root / "03_Agents-and-Skills/INDEX.md"
        index.write_text(index.read_text() + "hand edit\n")
        self.assertIn("catalog: STALE — run python3 06_Engine/scripts/agency.py sync", self.cli("sync", "--check", expect=1))
        self.cli("sync")
        self.cli("sync", "--check")

    def test_hub_new_switches_mode(self):
        out = self.cli("hub", "new", "example-project")
        self.assertTrue((self.root / "01_Project-Hubs/example-project/README.md").is_file())
        self.assertIn("workspace", out)
        self.cli("hub", "new", "Bad_Slug", expect=2)
        self.cli("hub", "new", "example-project", expect=2)

    def test_unknown_plugin_is_a_usage_error(self):
        self.cli("plugin", "add", "does-not-exist", expect=2)


if __name__ == "__main__":
    unittest.main()
