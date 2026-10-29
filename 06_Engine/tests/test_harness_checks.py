from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from helpers import git, load_harness, make_host, skill, write

from agency.config import set_mode

HYGIENE = load_harness("check-template.py")
LINKS = load_harness("check-links.py")
INDEX = load_harness("build-skill-index.py")


class HygieneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_host(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_template(self):
        self.assertEqual(HYGIENE.check(self.root), [])

    def test_template_mode_rules(self):
        write(self.root / "01_Project-Hubs/example-project/README.md", "# Example project\n")
        write(self.root / "notes_TENANT.md", "customer label\n")
        problems = HYGIENE.check(self.root)
        self.assertTrue(any("template mode allows only" in p for p in problems))
        self.assertTrue(any("customer-labelled" in p for p in problems))
        set_mode(self.root, "workspace")
        problems = HYGIENE.check(self.root)
        self.assertFalse(any("template mode" in p for p in problems))

    def test_noise_and_personal_paths(self):
        home = "/Us" + "ers/someone/project"  # built at runtime so this file stays clean
        write(self.root / "docs/notes.md", f"see {home}/file.md\n")
        write(self.root / ".DS_Store", "x")
        write(self.root / "pkg/__pycache__/m.cpython-311.pyc", "x")
        problems = HYGIENE.check(self.root)
        self.assertTrue(any("absolute personal path in docs/notes.md:1" in p for p in problems))
        self.assertTrue(any(".DS_Store" in p for p in problems))
        self.assertTrue(any("__pycache__" in p for p in problems))


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_host(Path(self.tmp.name), init_git=False)
        write(self.root / "00_README/guide.md", "# Guide\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_links_pass_through_discovery(self):
        skill(self.root, "linked-skill", body="See [guide](../../../00_README/guide.md) and [sibling](../demo-skill/SKILL.md).\n")
        broken, checked = LINKS.check(self.root)
        self.assertEqual(broken, [])
        self.assertGreater(checked, 0)

    def test_missing_target_and_depth_parity(self):
        skill(self.root, "linked-skill", body="[gone](missing.md) and [agent](../../Agents/demo-agent.agent.md)\n")
        broken, _ = LINKS.check(self.root)
        reasons = {(item["target"], item["reason"].split(" ")[0]) for item in broken}
        self.assertIn(("missing.md", "missing"), reasons)
        self.assertTrue(any(item["target"] == "../../Agents/demo-agent.agent.md" and "depth parity" in item["reason"]
                            for item in broken))

    def test_links_into_unmounted_plugins_are_skipped(self):
        write(self.root / "00_README/plugins.md",
              "[engine](../03_Agents-and-Skills/Skills/fixture-kit/README.md)\n[[guide]]\n")
        broken, _ = LINKS.check(self.root)
        self.assertEqual(broken, [])


class CatalogIndexTests(unittest.TestCase):
    def test_render_is_deterministic_and_lists_gated_adapters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_host(Path(tmp), init_git=False)
            first, second = INDEX.render(root), INDEX.render(root)
            self.assertEqual(first, second)
            self.assertIn("[demo-skill](Skills/demo-skill/SKILL.md)", first)
            self.assertIn("| **gated-adapter** | prompts | **fixture** |", first)
            self.assertNotIn("[/gated-adapter]", first)
            self.assertIn("None: no plug-in is pinned in this repository.", first)

    def test_plugin_skills_are_listed_and_survive_a_clone_without_submodules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_host(Path(tmp), init_git=False)
            mount = root / "03_Agents-and-Skills/Skills/fixture-kit"
            write(root / ".gitmodules", '[submodule "kit"]\n\tpath = 03_Agents-and-Skills/Skills/fixture-kit\n'
                                        "\turl = https://example.invalid/fixture.git\n")
            write(mount / "fixture.json", "{}\n")
            write(mount / "skills/alpha-skill/SKILL.md", "---\nname: alpha-skill\ndescription: Alpha. Use when testing.\n---\n")
            text = INDEX.render(root)
            self.assertIn("| `alpha-skill` | Alpha. Use when testing. |", text, "engines match bound names in backticks")
            self.assertIn("(1 in this repository)", text)
            (root / INDEX.INDEX).write_text(text)
            shutil.rmtree(mount)  # a fresh clone: the pin is registered, the mount is empty
            self.assertEqual(INDEX.render(root), text, "the committed section is kept until the mount is checked out")

    def test_only_skill_names_are_written_between_delimiters(self):
        """Engines (PDG) find bound skills as `name`, /name/ or [name] anywhere in the catalog."""
        def findable(name: str, text: str) -> bool:
            return re.search(r"(`|/|\[)" + re.escape(name) + r"(`|/|\])", text) is not None

        with tempfile.TemporaryDirectory() as tmp:
            root = make_host(Path(tmp), init_git=False)
            path = skill(root, "talky-skill")
            path.write_text(path.read_text().replace(
                "description: Demonstrates talky-skill.",
                "description: Hands off to `ghost-skill`, [ghost-skill] and Skills/ghost-skill/SKILL.md."))
            text = INDEX.render(root)
            self.assertIn("ghost-skill", text, "the description is still listed")
            for name in ("ghost-skill", "fixture", "gated-adapter", "demo-agent", "demo-prompt"):
                self.assertFalse(findable(name, text), f"{name} must not pass for an available skill")
            self.assertTrue(findable("talky-skill", text) and findable("demo-skill", text), "skills stay findable")

    def test_kept_section_requires_the_same_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_host(Path(tmp))
            write(root / ".gitmodules", '[submodule "kit"]\n\tpath = 03_Agents-and-Skills/Skills/fixture-kit\n'
                                        "\turl = https://example.invalid/fixture.git\n")
            mount = "03_Agents-and-Skills/Skills/fixture-kit"
            git(root, "update-index", "--add", "--cacheinfo", f"160000,{'1' * 40},{mount}")
            kept = ("<!-- plugin:fixture pin:" + "1" * 40 + " -->\nEdition **main** · 1 skills\n\n| Skill | Use it to |\n"
                    "|---|---|\n| `alpha-skill` | Alpha. |\n<!-- /plugin:fixture -->")
            (root / INDEX.INDEX).write_text(kept + "\n")
            self.assertIn("| `alpha-skill` | Alpha. |", INDEX.render(root), "same pin: the committed list is kept")
            git(root, "update-index", "--cacheinfo", f"160000,{'2' * 40},{mount}")
            text = INDEX.render(root)
            self.assertNotIn("alpha-skill", text, "a re-pinned plug-in's old skill list is not trusted")
            self.assertIn(f"<!-- plugin:fixture pin:{'2' * 40} -->", text)
            self.assertIn("but not checked out here", text)


if __name__ == "__main__":
    unittest.main()
