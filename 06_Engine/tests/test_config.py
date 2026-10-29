from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import REPO, make_host, write

from agency.config import ConfigError, load_config, repo_path, set_mode


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_host(Path(self.tmp.name), init_git=False)

    def tearDown(self):
        self.tmp.cleanup()

    def test_shipped_config_is_valid_template(self):
        config = load_config(REPO)
        self.assertIn(config.mode, ("template", "workspace"))
        self.assertTrue(config.targets)

    def test_defaults_when_missing(self):
        (self.root / "agency.yaml").unlink()
        config = load_config(self.root)
        self.assertFalse(config.exists)
        self.assertEqual(config.mode, "template")
        self.assertEqual(config.targets, ("copilot", "claude"))

    def test_rejects_unknown_keys_and_values(self):
        for body in ("schema: agency/v1\nmode: production\n", "schema: agency/v2\n", "colour: blue\n",
                     "discovery: {targets: [cursor]}\n", "plugins: {x: {mount: ../escape}}\n",
                     "plugins: {x: {enabled: maybe}}\n"):
            with self.subTest(body=body):
                write(self.root / "agency.yaml", body)
                with self.assertRaises(ConfigError):
                    load_config(self.root)

    def test_set_mode_rewrites_only_mode_line(self):
        before = (self.root / "agency.yaml").read_text()
        self.assertTrue(set_mode(self.root, "workspace"))
        after = (self.root / "agency.yaml").read_text()
        self.assertEqual(load_config(self.root).mode, "workspace")
        self.assertEqual(before.replace("mode: template", "mode: workspace"), after)
        self.assertFalse(set_mode(self.root, "workspace"))

    def test_repo_path_rejects_escapes(self):
        for value in ("/abs/path", "../up", "a/../../b", "", "C:\\x", "C:/outside", "d:relative"):
            with self.subTest(value=value), self.assertRaises(ConfigError):
                repo_path(value, field_name="mount")
        self.assertEqual(str(repo_path("02_Workflows/x/", field_name="mount")), "02_Workflows/x")


if __name__ == "__main__":
    unittest.main()
