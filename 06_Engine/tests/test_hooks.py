"""The staged-credential scan: catches secrets in large diffs, never blocks removing one."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import ENGINE, git, write

SCAN = ENGINE / "scripts" / "scan-staged-credentials.sh"
TOKEN = "gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"  # built at runtime: this file holds no secret


@unittest.skipUnless(shutil.which("bash") and shutil.which("git"), "bash and git are required")
class CredentialScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        write(self.repo / "README.md", "# repo\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def scan(self) -> int:
        return subprocess.run(["bash", str(SCAN)], cwd=self.repo, capture_output=True, text=True).returncode

    def test_clean_change_passes(self):
        write(self.repo / "notes.md", "plain text\n")
        git(self.repo, "add", "-A")
        self.assertEqual(self.scan(), 0)

    def test_secret_at_the_end_of_a_large_diff_is_caught(self):
        lines = "\n".join(f"line {number} of filler text" for number in range(200_000))
        write(self.repo / "big.txt", f"{TOKEN}\n{lines}\n{TOKEN}\n")
        git(self.repo, "add", "-A")
        self.assertEqual(self.scan(), 1)

    def test_removing_a_secret_is_not_blocked(self):
        write(self.repo / "leak.txt", f"token={TOKEN}\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "--no-verify", "-m", "simulate an earlier leak")
        (self.repo / "leak.txt").unlink()
        git(self.repo, "add", "-A")
        self.assertEqual(self.scan(), 0)


if __name__ == "__main__":
    unittest.main()
