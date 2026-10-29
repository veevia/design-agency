from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml
from helpers import REPO, make_host, write

from agency.config import ConfigError
from agency.plugins import (
    contributions,
    detect_edition,
    load_profiles,
    parse_profile,
    plugin_state,
    plugin_states,
    read_gitmodules,
)

BASE = {
    "schema": "agency-plugin/v1", "name": "sample", "title": "Sample", "summary": "A sample.", "kind": "skills",
    "mount": "03_Agents-and-Skills/Skills/sample",
    "editions": {"main": {"source": "https://example.invalid/s.git", "marker": "m.json",
                          "provides": {"skills": ["*/SKILL.md"]}}},
}


def profile(data: dict, name: str = "sample"):
    return parse_profile(data, Path(f"{name}.plugin.yaml"))


class ProfileParsingTests(unittest.TestCase):
    def test_shipped_profiles_are_valid(self):
        profiles = load_profiles(REPO)
        self.assertEqual(set(profiles), {"fde-design-toolkit", "prototype-design", "video-production", "ui-ux-pro-max",
                                         "anthropic-skills", "impeccable", "video-shotcraft"})
        self.assertEqual(profiles["fde-design-toolkit"].default_edition, "public")
        self.assertEqual(list(profiles["fde-design-toolkit"].editions), ["full", "public"])
        self.assertEqual(str(profiles["prototype-design"].mount), "02_Workflows/prototype-design")
        self.assertEqual(str(profiles["video-production"].mount), "02_Workflows/video-production")
        self.assertIn("prototype-design", profiles["prototype-design"].host_adapters["prompts"])
        for engine in ("prototype-design", "video-production"):
            companions = {c["plugin"]: c["edition"] for c in profiles[engine].skill_bindings["companions"]}
            self.assertEqual(companions["fde-design-toolkit"], "full", "engine bindings need the full FDE edition")
            self.assertIn("anthropic-skills", companions)
        self.assertEqual(profiles["video-production"].skill_bindings["tenant_skills"],
                         ("azure-foundry-image", "workiq-grounding"))
        wired = [rule.glob for rule in profiles["anthropic-skills"].editions["upstream"].provides["skills"]]
        self.assertFalse([glob for glob in wired if any(doc in glob for doc in ("docx", "pdf", "pptx", "xlsx"))],
                         "proprietary document skills must stay unwired")

    def test_companions_must_name_other_profiles(self):
        def engine(companions):
            data = json.loads(json.dumps(BASE))
            data.update(name="engine", kind="engine", mount="02_Workflows/engine",
                        skill_bindings={"file": "graph.yaml", "collection": "nodes", "field": "skills",
                                        "companions": companions})
            return data

        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "06_Engine/plugins"
            folder.mkdir(parents=True)
            (folder / "sample.plugin.yaml").write_text(yaml.safe_dump(BASE))
            (folder / "engine.plugin.yaml").write_text(yaml.safe_dump(engine([{"plugin": "sample", "edition": "main"}])))
            parsed = load_profiles(Path(tmp))["engine"].skill_bindings["companions"]
            self.assertEqual(parsed, ({"plugin": "sample", "edition": "main"},))
            (folder / "engine.plugin.yaml").write_text(yaml.safe_dump(engine(["sample"])))
            self.assertEqual(load_profiles(Path(tmp))["engine"].skill_bindings["companions"],
                             ({"plugin": "sample", "edition": None},))
            for bad in (["nobody"], [{"plugin": "sample", "edition": "gold"}], ["engine"],
                        ["sample", {"plugin": "sample", "edition": "main"}]):
                (folder / "engine.plugin.yaml").write_text(yaml.safe_dump(engine(bad)))
                with self.subTest(bad), self.assertRaises(ConfigError):
                    load_profiles(Path(tmp))
        for bad in ([{"plugin": "sample", "colour": "x"}], [3], "sample"):
            with self.subTest(bad), self.assertRaises(ConfigError):
                profile(engine(bad), name="engine")
        data = engine([])
        data["skill_bindings"]["tenant_skills"] = ["Not A Skill"]
        with self.assertRaises(ConfigError):
            profile(data, name="engine")

    def test_minimal_profile(self):
        parsed = profile(json.loads(json.dumps(BASE)))
        self.assertEqual(parsed.default_edition, "main")
        self.assertEqual(parsed.editions["main"].provides["skills"][0].glob, "*/SKILL.md")

    def test_invalid_profiles(self):
        def variant(**changes):
            data = json.loads(json.dumps(BASE))
            for dotted, value in changes.items():
                target = data
                keys = dotted.split("__")
                for key in keys[:-1]:
                    target = target[key]
                target[keys[-1]] = value
            return data

        cases = {
            "schema": variant(schema="agency-plugin/v2"),
            "kind": variant(kind="tool"),
            "unknown key": variant(colour="blue"),
            "mount escape": variant(mount="../outside"),
            "skill glob": variant(editions__main__provides={"skills": ["*/README.md"]}),
            "glob escape": variant(editions__main__provides={"skills": ["../*/SKILL.md"]}),
            "side effects": variant(editions__main__checks=[{"name": "x", "run": ["a"], "side_effects": "network"}]),
            "duplicate checks": variant(editions__main__checks=[{"name": "x", "run": ["a"]}, {"name": "x", "run": ["b"]}]),
            "default edition": variant(default_edition="missing"),
            "provides_from": variant(editions__main__provides_from="npm"),
            "env name": variant(editions__main__checks=[{"name": "x", "run": ["a"], "env": {"lower": "v"}}]),
            "shallow type": variant(editions__main__shallow="yes"),
        }
        for label, data in cases.items():
            with self.subTest(label), self.assertRaises(ConfigError):
                profile(data)
        with self.assertRaises(ConfigError):
            profile(json.loads(json.dumps(BASE)), name="other-name")


class StateAndContributionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_host(Path(self.tmp.name), init_git=False)
        self.profile = load_profiles(self.root)["fixture"]
        self.mount = self.root / "03_Agents-and-Skills/Skills/fixture-kit"

    def tearDown(self):
        self.tmp.cleanup()

    def test_available_registered_and_enabled_states(self):
        self.assertEqual(plugin_state(self.root, self.profile).status, "available")
        write(self.root / ".gitmodules", '[submodule "kit"]\n\tpath = 03_Agents-and-Skills/Skills/fixture-kit\n\turl = https://example.invalid/k.git\n')
        self.assertIn("03_Agents-and-Skills/Skills/fixture-kit", read_gitmodules(self.root))
        self.mount.mkdir(parents=True)
        state = plugin_state(self.root, self.profile)
        self.assertEqual(state.status, "not-checked-out")
        write(self.mount / "README.md", "content without marker\n")
        self.assertEqual(plugin_state(self.root, self.profile).status, "unrecognized")
        write(self.mount / "fixture.json", "{}\n")
        state = plugin_state(self.root, self.profile)
        self.assertEqual((state.status, state.edition), ("enabled", "main"))

    def test_contributions_prefix_targets_and_invalid_names(self):
        write(self.mount / "fixture.json", "{}\n")
        write(self.mount / "skills/good-skill/SKILL.md", "---\nname: good-skill\n---\n")
        write(self.mount / "skills/Bad_Skill/SKILL.md", "---\nname: Bad_Skill\n---\n")
        write(self.mount / "agents/rev.agent.md", "---\nname: Rev\n---\n")
        write(self.mount / "commands/go.md", "# go\n")
        found, errors, issues = contributions(plugin_state(self.root, self.profile))
        names = {(c.surface, c.name, c.targets) for c in found}
        self.assertIn(("skills", "good-skill", ("copilot", "claude")), names)
        self.assertIn(("agents", "rev", ("copilot",)), names)
        self.assertIn(("prompts", "fx-go", ("claude",)), names)
        self.assertFalse(any(c.name == "Bad_Skill" for c in found))
        self.assertTrue(any("Bad_Skill" in issue for issue in issues), "invalid names are warnings")
        self.assertEqual(errors, [], "every rule matched something")

    def test_rule_matching_nothing_is_an_error(self):
        write(self.mount / "fixture.json", "{}\n")
        write(self.mount / "skills/only-skill/SKILL.md", "---\nname: only-skill\n---\n")
        found, errors, _ = contributions(plugin_state(self.root, self.profile))
        self.assertTrue(any("agents/*.agent.md" in error and "matched nothing" in error for error in errors))
        self.assertTrue(any("commands/*.md" in error for error in errors))

    def test_effective_mounts_may_not_overlap(self):
        write(self.root / "06_Engine/plugins/nested.plugin.yaml", yaml.safe_dump({
            "schema": "agency-plugin/v1", "name": "nested", "title": "Nested", "summary": "Overlaps.", "kind": "skills",
            "mount": "03_Agents-and-Skills/Skills/fixture-kit/inner",
            "editions": {"main": {"source": "https://example.invalid/n.git", "marker": "n.json"}},
        }))
        with self.assertRaises(ConfigError):
            plugin_states(self.root)

    def test_unregistered_content_is_flagged(self):
        write(self.mount / "fixture.json", "{}\n")
        state = plugin_state(self.root, self.profile)
        self.assertTrue(state.recognized)
        self.assertTrue(any("not a registered submodule" in issue for issue in state.issues))

    def test_edition_detection_prefers_requested_marker(self):
        data = json.loads(json.dumps(BASE))
        data["editions"] = {
            "full": {"source": "https://example.invalid/f.git", "marker": "full.json"},
            "public": {"source": "https://example.invalid/p.git", "marker": "public.json"},
        }
        parsed = profile(data)
        folder = Path(self.tmp.name) / "editions"
        write(folder / "public.json", "{}")
        self.assertEqual(detect_edition(parsed, folder), "public")
        write(folder / "full.json", "{}")
        self.assertEqual(detect_edition(parsed, folder), "full")
        self.assertEqual(detect_edition(parsed, folder, "public"), "public")

    def test_claude_plugin_manifest_adapter(self):
        data = yaml.safe_load((self.root / "06_Engine/plugins/fixture.plugin.yaml").read_text())
        data["editions"]["main"]["provides"] = {}
        data["editions"]["main"]["provides_from"] = "claude-plugin"
        data["editions"]["main"]["command_prefix"] = "kit-"
        write(self.root / "06_Engine/plugins/fixture.plugin.yaml", yaml.safe_dump(data))
        write(self.mount / "fixture.json", "{}\n")
        write(self.mount / ".claude-plugin/plugin.json", json.dumps({
            "name": "kit", "skills": ["./stage-one", "./.claude/skills/solo"],
            "agents": ["./agents/critic.md"], "commands": "./commands",
        }))
        write(self.mount / "stage-one/first-skill/SKILL.md", "---\nname: first-skill\n---\n")
        write(self.mount / ".claude/skills/solo/SKILL.md", "---\nname: solo\n---\n")
        write(self.mount / "agents/critic.md", "---\nname: critic\n---\n")
        write(self.mount / "commands/ship.md", "# ship\n")
        found, _, _ = contributions(plugin_state(self.root, load_profiles(self.root)["fixture"]))
        names = {(c.surface, c.name) for c in found}
        self.assertTrue({("skills", "first-skill"), ("skills", "solo"), ("claude_agents", "critic"),
                         ("prompts", "kit-ship")} <= names)

    def test_claude_plugin_that_is_one_skill_at_its_root(self):
        data = yaml.safe_load((self.root / "06_Engine/plugins/fixture.plugin.yaml").read_text())
        data["editions"]["main"]["provides"] = {}
        data["editions"]["main"]["provides_from"] = "claude-plugin"
        write(self.root / "06_Engine/plugins/fixture.plugin.yaml", yaml.safe_dump(data))
        write(self.mount / "fixture.json", "{}\n")
        write(self.mount / ".claude-plugin/plugin.json", json.dumps({"name": "kit", "skills": "./"}))
        write(self.mount / "SKILL.md", "---\nname: fixture-kit\n---\n")
        write(self.mount / "agents/openai.yaml", "interface: {}\n")  # another runtime's metadata, not Claude agents
        found, errors, _ = contributions(plugin_state(self.root, load_profiles(self.root)["fixture"]))
        self.assertEqual(errors, [])
        self.assertEqual([(c.surface, c.name, c.source) for c in found], [("skills", "fixture-kit", self.mount)])


if __name__ == "__main__":
    unittest.main()
