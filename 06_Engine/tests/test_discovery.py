from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from helpers import make_host, skill, write

from agency import discovery
from agency.catalog import CatalogError, binding_coverage, build_catalog, companion_hint


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_host(Path(self.tmp.name), init_git=False)

    def tearDown(self):
        self.tmp.cleanup()

    def sync(self):
        result = discovery.plan(self.root)
        discovery.apply(self.root, result)
        return discovery.plan(self.root)

    def test_native_links_and_gating(self):
        after = self.sync()
        self.assertFalse(after.drift)
        expected = {
            ".github/skills/demo-skill": "../../03_Agents-and-Skills/Skills/demo-skill",
            ".claude/skills/demo-skill": "../../03_Agents-and-Skills/Skills/demo-skill",
            ".github/agents/demo-agent.agent.md": "../../03_Agents-and-Skills/Agents/demo-agent.agent.md",
            ".claude/agents/demo-agent.md": "../../03_Agents-and-Skills/Agents/demo-agent.agent.md",
            ".github/prompts/demo-prompt.prompt.md": "../../02_Workflows/prompts/demo-prompt.prompt.md",
            ".claude/commands/demo-prompt.md": "../../02_Workflows/prompts/demo-prompt.prompt.md",
        }
        for link, target in expected.items():
            path = self.root / link
            self.assertTrue(path.is_symlink(), link)
            self.assertEqual(os.readlink(path), target)
            self.assertTrue(path.exists(), f"{link} resolves")
        self.assertFalse((self.root / ".github/prompts/gated-adapter.prompt.md").exists(), "adapter hidden until plug-in")

    def test_plugin_mount_unlocks_adapter_and_contributions(self):
        mount = self.root / "03_Agents-and-Skills/Skills/fixture-kit"
        write(mount / "fixture.json", "{}\n")
        write(mount / "skills/alpha-skill/SKILL.md", "---\nname: alpha-skill\n---\n")
        self.sync()
        self.assertTrue((self.root / ".github/prompts/gated-adapter.prompt.md").is_symlink())
        self.assertTrue((self.root / ".github/skills/alpha-skill").exists())
        self.assertFalse((self.root / ".github/skills/fixture-kit").exists(), "a mount is not a native skill")

    def test_stale_links_are_removed_and_conflicts_reported(self):
        self.sync()
        (self.root / "03_Agents-and-Skills/Skills/demo-skill/SKILL.md").unlink()
        stale = discovery.plan(self.root)
        self.assertIn(self.root / ".github/skills/demo-skill", stale.remove)
        discovery.apply(self.root, stale)
        self.assertFalse((self.root / ".github/skills/demo-skill").is_symlink())
        agent_link = self.root / ".github/agents/demo-agent.agent.md"
        agent_link.unlink()
        write(agent_link, "hand-written file\n")
        result = discovery.plan(self.root)
        self.assertTrue(any("unmanaged file" in conflict for conflict in result.conflicts))
        with self.assertRaises(RuntimeError):
            discovery.apply(self.root, result)
        self.assertEqual(agent_link.read_text(), "hand-written file\n", "unmanaged file untouched")

    def test_target_selection_and_deferred_links(self):
        self.sync()
        write(self.root / "agency.yaml", "schema: agency/v1\nmode: template\ndiscovery: {targets: [copilot]}\n")
        result = discovery.plan(self.root)
        self.assertIn(self.root / ".claude/skills/demo-skill", result.remove)
        discovery.apply(self.root, result)
        self.assertFalse((self.root / ".claude").exists(), "empty discovery folders are pruned")
        # A link into a registered plug-in that is not checked out is deferred, not deleted.
        write(self.root / ".gitmodules", '[submodule "kit"]\n\tpath = 03_Agents-and-Skills/Skills/fixture-kit\n\turl = https://example.invalid/k.git\n')
        (self.root / "03_Agents-and-Skills/Skills/fixture-kit").mkdir()
        dangling = self.root / ".github/skills/alpha-skill"
        os.symlink("../../03_Agents-and-Skills/Skills/fixture-kit/skills/alpha-skill", dangling)
        result = discovery.plan(self.root)
        self.assertIn(dangling, result.deferred)
        self.assertNotIn(dangling, result.remove)

    def test_name_collision_is_an_error(self):
        mount = self.root / "03_Agents-and-Skills/Skills/fixture-kit"
        write(mount / "fixture.json", "{}\n")
        write(mount / "skills/demo-skill/SKILL.md", "---\nname: demo-skill\n---\n")
        with self.assertRaises(CatalogError):
            build_catalog(self.root)

    def test_adapter_declarations_are_validated(self):
        profile = self.root / "06_Engine/plugins/fixture.plugin.yaml"
        profile.write_text(profile.read_text().replace("prompts: [gated-adapter]", "prompts: [gated-adaptor]"))
        catalog = build_catalog(self.root)
        self.assertTrue(any("gated-adaptor does not exist" in error for error in catalog.errors))
        self.assertTrue(discovery.plan(self.root).failed)

    def test_engine_skill_binding_coverage(self):
        profile = self.root / "06_Engine/plugins/fixture.plugin.yaml"
        profile.write_text(profile.read_text().replace(
            "editions:\n", "skill_bindings:\n  file: graph/workflow.yaml\n  collection: nodes\n  field: skills\neditions:\n", 1))
        mount = self.root / "03_Agents-and-Skills/Skills/fixture-kit"
        write(mount / "fixture.json", "{}\n")
        write(mount / "skills/alpha-skill/SKILL.md", "---\nname: alpha-skill\n---\n")
        write(mount / "graph/workflow.yaml",
              "nodes:\n  - id: n1\n    skills: [demo-skill, alpha-skill]\n  - id: n2\n    skills: [missing-skill]\n")
        coverage = binding_coverage(build_catalog(self.root))["fixture"]
        self.assertEqual(coverage["bound"], ["alpha-skill", "demo-skill", "missing-skill"])
        self.assertEqual(coverage["resolved"], ["alpha-skill", "demo-skill"], "native and plug-in skills both count")
        self.assertEqual(coverage["missing"], ["missing-skill"])
        self.assertEqual(coverage["gaps"], ["missing-skill"])
        self.assertEqual(coverage["tenant"], [])

    def test_binding_gaps_tenant_skills_and_companions(self):
        write(self.root / "06_Engine/plugins/helper.plugin.yaml", """
            schema: agency-plugin/v1
            name: helper
            title: Helper skills
            summary: Supplies a skill the fixture engine binds.
            kind: skills
            mount: 03_Agents-and-Skills/Skills/helper-kit
            editions:
              main:
                source: https://example.invalid/helper.git
                marker: helper.json
                provides:
                  skills: [skills/*/SKILL.md]
            """)
        profile = self.root / "06_Engine/plugins/fixture.plugin.yaml"
        profile.write_text(profile.read_text().replace("editions:\n", (
            "skill_bindings:\n  file: graph/workflow.yaml\n  collection: nodes\n  field: skills\n"
            "  companions: [helper]\n  tenant_skills: [tenant-connector]\neditions:\n"), 1))
        mount = self.root / "03_Agents-and-Skills/Skills/fixture-kit"
        write(mount / "fixture.json", "{}\n")
        write(mount / "graph/workflow.yaml",
              "nodes:\n  - id: n1\n    skills: [demo-skill, helper-skill, tenant-connector]\n")
        coverage = binding_coverage(build_catalog(self.root))["fixture"]
        self.assertEqual((coverage["gaps"], coverage["tenant"]), (["helper-skill"], ["tenant-connector"]))
        self.assertEqual(coverage["companions"], [{"plugin": "helper", "edition": None, "plugged_in": False}])
        self.assertEqual(companion_hint(coverage), "agency.py plugin add helper")
        helper = self.root / "03_Agents-and-Skills/Skills/helper-kit"
        write(helper / "helper.json", "{}\n")
        write(helper / "skills/helper-skill/SKILL.md", "---\nname: helper-skill\n---\n")
        coverage = binding_coverage(build_catalog(self.root))["fixture"]
        self.assertEqual((coverage["gaps"], coverage["tenant"]), ([], ["tenant-connector"]))
        self.assertTrue(coverage["companions"][0]["plugged_in"])
        self.assertEqual(companion_hint(coverage), "")
        skill(self.root, "tenant-connector")
        coverage = binding_coverage(build_catalog(self.root))["fixture"]
        self.assertEqual((coverage["missing"], len(coverage["resolved"])), ([], 3), "a fork may supply tenant skills")

    def test_native_skill_cannot_take_over_an_unmounted_plugin_link(self):
        write(self.root / ".gitmodules", '[submodule "kit"]\n\tpath = 03_Agents-and-Skills/Skills/fixture-kit\n'
                                         "\turl = https://example.invalid/fixture.git\n")
        link = self.root / ".github/skills/alpha-skill"
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink("../../03_Agents-and-Skills/Skills/fixture-kit/skills/alpha-skill", link)
        self.assertIn(link, discovery.plan(self.root).deferred, "a pinned plug-in's link waits for its checkout")
        skill(self.root, "alpha-skill")
        result = discovery.plan(self.root)
        self.assertTrue(any("belongs to a plug-in that is not checked out" in c for c in result.conflicts), result.conflicts)
        self.assertTrue(result.failed)
        self.assertEqual(os.readlink(link), "../../03_Agents-and-Skills/Skills/fixture-kit/skills/alpha-skill")

    def test_hidden_folders_and_mounts_are_not_native_skills(self):
        skill(self.root, "_draft-skill")
        names = {item.name for item in build_catalog(self.root).items if item.surface == "skills"}
        self.assertEqual(names, {"demo-skill"})


if __name__ == "__main__":
    unittest.main()
