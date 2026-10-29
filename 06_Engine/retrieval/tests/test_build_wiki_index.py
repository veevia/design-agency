from __future__ import annotations

import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def load_module(name: str, filename: str):
    specification = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parents[1] / filename,
    )
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


INDEXER = load_module("build_wiki_index", "build-wiki-index.py")
DIGEST = load_module("build_wiki_digest", "build-wiki-digest.py")


class WikiIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.hubs = self.root / "01_Project-Hubs"
        self.hubs.mkdir()
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        self.addCleanup(patch.stopall)
        patch.object(INDEXER, "REPO_ROOT", self.root).start()
        patch.object(INDEXER, "HUBS_ROOT", self.hubs).start()

    def write(self, relative: str, text: str = "# Example\n", tracked: bool = True) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if tracked:
            subprocess.run(["git", "-C", str(self.root), "add", "--", relative], check=True)
        return path

    def test_discovery_includes_root_wiki_but_not_untracked_hubs(self) -> None:
        self.write("00_Agentic-OS/_wiki/concepts/architecture.md")
        self.write("01_Project-Hubs/demo/_wiki/concepts/topic.md")
        self.write("01_Project-Hubs/sibling/_wiki/concepts/draft.md", tracked=False)
        self.write("02_Workflows/tests/fixtures/_wiki/concepts/example.md")
        self.assertEqual(INDEXER.discover_programs(), [self.root / "00_Agentic-OS", self.hubs / "demo"])

    def test_empty_git_index_does_not_fall_back_to_untracked_wikis(self) -> None:
        self.write("00_Agentic-OS/_wiki/concepts/draft.md", tracked=False)
        self.write("01_Project-Hubs/sibling/_wiki/concepts/draft.md", tracked=False)
        self.assertEqual(INDEXER.discover_programs(), [])

    def test_only_authored_tracked_existing_pages_are_indexed(self) -> None:
        prefix = "01_Project-Hubs/demo/_wiki/"
        self.write(prefix + "concepts/topic.md", "# Topic\n\n**TL;DR:** Durable context.\n")
        for name in ("index.md", "log.md", "README.md", "_digest.md", "_gaps.md",
                     "_templates/source.md", "concepts/templates/example.md",
                     "tests/fake.md", "fixtures/fake.md"):
            self.write(prefix + name)
        self.write(prefix + "concepts/untracked.md", tracked=False)
        self.write(prefix + "concepts/deleted.md").unlink()
        entries, warnings = INDEXER.index_wiki(self.root / prefix)
        self.assertEqual([entry["path"] for entry in entries], ["concepts/topic.md"])
        self.assertEqual(warnings, [])

    def test_irregular_folder_names_have_valid_types(self) -> None:
        self.assertEqual(INDEXER.infer_type(Path("entities/person.md"), {}), "entity")
        self.assertEqual(INDEXER.infer_type(Path("syntheses/topic.md"), {}), "synthesis")
        self.assertEqual(INDEXER.infer_type(Path("sources/note.md"), {}), "source")

    def test_decision_lifecycle_and_identity_survive_indexing(self) -> None:
        prefix = "01_Project-Hubs/demo/_wiki/"
        self.write(prefix + "decisions/history.md", """---
type: decision
id: demo-0001
record_type: adr
status: superseded
light: yellow
canonical: false
layer: L1
updated: 2026-09-05
---
# Historical decision

**TL;DR:** Preserved rationale, not the current contract.
""")
        entries, warnings = INDEXER.index_wiki(self.root / prefix)
        self.assertEqual(warnings, [])
        self.assertEqual(entries[0]["id"], "demo-0001")
        self.assertEqual(entries[0]["status"], "superseded")
        self.assertFalse(entries[0]["canonical"])
        self.assertEqual(entries[0]["layer"], "L1")
        INDEXER.write_index_md(self.root / prefix / "index.md", "demo", entries)
        self.assertIn("demo-0001 · adr · superseded · yellow", (self.root / prefix / "index.md").read_text())

    def test_empty_index_is_not_a_phantom_digest_page(self) -> None:
        hub = self.hubs / "demo"
        wiki = hub / "_wiki"
        wiki.mkdir(parents=True)
        INDEXER.write_jsonl(wiki / "index.jsonl", [])
        self.assertEqual((wiki / "index.jsonl").read_text(), "")
        full, memory = DIGEST.build(hub)
        self.assertIn("0 pages", full)
        self.assertIn("No knowledge pages indexed yet", full)
        self.assertIn("0 pages", memory)

    def test_digest_rebuild_does_not_change_knowledge_index(self) -> None:
        prefix = "01_Project-Hubs/demo/_wiki/"
        self.write(prefix + "concepts/topic.md", "# Topic\n\n**TL;DR:** Durable context.\n")
        self.write(prefix + "_digest.md")
        wiki = self.root / prefix
        before, _ = INDEXER.index_wiki(wiki)
        INDEXER.write_jsonl(wiki / "index.jsonl", before)
        full, memory = DIGEST.build(wiki.parent)
        (wiki / "_digest.md").write_text(full, encoding="utf-8")
        after, _ = INDEXER.index_wiki(wiki)
        self.assertEqual(before, after)
        self.assertIn("[Topic](concepts/topic.md)", full)
        self.assertNotIn("](concepts/topic.md)", memory)

    def test_phase_is_sourced_from_hub_overview(self) -> None:
        self.write("01_Project-Hubs/demo/README.md", "# Demo\n\n> **Current phase:** Build; validation pending\n")
        wiki = self.hubs / "demo" / "_wiki"
        wiki.mkdir()
        INDEXER.write_index_md(wiki / "index.md", "demo", [])
        self.assertIn("**Phase:** Build; validation pending", (wiki / "index.md").read_text())

    def test_malformed_yaml_fails_with_path_and_line(self) -> None:
        path = self.write("01_Project-Hubs/demo/_wiki/decisions/broken.md", """---
type: decision
id: demo-0001
decided_by: Lead Coordinator: delegated
updated: 2026-09-04
---
# Broken
""")
        with self.assertRaisesRegex(INDEXER.WikiIndexError, r"decisions/broken\.md:4: invalid YAML"):
            INDEXER.index_wiki(path.parent.parent)

    def test_unterminated_or_nonmapping_frontmatter_is_not_silently_empty(self) -> None:
        for text in ("---\nstatus: accepted\n# Missing close\n", "---\n- not a mapping\n---\n"):
            with self.subTest(text=text), self.assertRaises(INDEXER.WikiIndexError):
                INDEXER.parse_front_matter(text, Path("bad.md"))
        metadata, body = INDEXER.parse_front_matter("---\ntitle: Valid\n---")
        self.assertEqual((metadata, body), ({"title": "Valid"}, ""))
        self.assertEqual(INDEXER.parse_front_matter("# No metadata\n"), ({}, "# No metadata\n"))

    def test_duplicate_decision_ids_report_both_paths(self) -> None:
        prefix = "01_Project-Hubs/demo/_wiki/"
        for name in ("original.md", "original 2.md"):
            self.write(prefix + "decisions/" + name, "---\ntype: decision\nid: demo-0040\n---\n# Record\n")
        with self.assertRaises(INDEXER.WikiIndexError) as error:
            INDEXER.index_wiki(self.root / prefix)
        self.assertIn("duplicate decision id 'demo-0040'", str(error.exception))
        self.assertIn("decisions/original.md", str(error.exception))
        self.assertIn("decisions/original 2.md", str(error.exception))

    def test_all_selected_wikis_are_validated_before_any_projection_is_written(self) -> None:
        self.write("01_Project-Hubs/first/_wiki/concepts/topic.md")
        self.write("01_Project-Hubs/second/_wiki/decisions/broken.md",
                   "---\ndecided_by: Lead Coordinator: delegated\n---\n")
        sentinel = self.write("01_Project-Hubs/first/_wiki/index.jsonl", "unchanged\n")
        with patch("sys.argv", ["build-wiki-index.py", "first", "second"]), \
                patch("sys.stderr", new_callable=io.StringIO) as errors, \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(INDEXER.main(), 1)
        self.assertIn("second/_wiki/decisions/broken.md", errors.getvalue())
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(sentinel.read_text(), "unchanged\n")

    def test_duplicate_ids_across_selected_wikis_fail_before_writing(self) -> None:
        for hub in ("first", "second"):
            self.write(f"01_Project-Hubs/{hub}/_wiki/decisions/call.md",
                       "---\ntype: decision\nid: shared-0001\n---\n# Call\n")
        with patch("sys.argv", ["build-wiki-index.py", "first", "second"]), \
                patch("sys.stderr", new_callable=io.StringIO) as errors:
            self.assertEqual(INDEXER.main(), 1)
        self.assertIn("shared-0001", errors.getvalue())
        self.assertFalse((self.hubs / "first/_wiki/index.jsonl").exists())
        self.assertFalse((self.hubs / "second/_wiki/index.md").exists())

    def test_check_validates_without_writing_and_preserves_authored_metadata(self) -> None:
        self.write("01_Project-Hubs/demo/_wiki/decisions/call.md", """---
type: decision
id: demo-0011
status: superseded
light: yellow
decided_by: "Lead Coordinator: delegated"
updated: 2026-09-04
---
# A call

## The call
Adopt the `ritual`, not the harness,
and retain the original boundary.

## Reason
Not part of the snippet.
""")
        wiki = self.hubs / "demo/_wiki"
        with patch("sys.argv", ["build-wiki-index.py", "--check", "demo"]), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(INDEXER.main(), 0)
        self.assertIn("validated (no writes)", output.getvalue())
        self.assertFalse((wiki / "index.jsonl").exists())
        self.assertFalse((wiki / "index.md").exists())
        entries, _ = INDEXER.index_wiki(wiki)
        self.assertEqual(entries[0]["updated"], "2026-09-04")
        self.assertEqual(entries[0]["status"], "superseded")
        self.assertEqual(entries[0]["light"], "yellow")
        self.assertEqual(entries[0]["id"], "demo-0011")
        self.assertEqual(entries[0]["tldr"], "Adopt the ritual, not the harness, and retain the original boundary.")

    def test_decision_snippets_are_authored_bounded_and_tldr_takes_precedence(self) -> None:
        self.assertEqual(INDEXER.extract_tldr("## Action\n\n**Yellow, proposed:** Preserve scope.\n",
                                            decision=True), "Yellow, proposed: Preserve scope.")
        self.assertEqual(INDEXER.extract_tldr("**Action:** Keep [the plan](plan.md).\n",
                                            decision=True), "Keep the plan.")
        self.assertEqual(INDEXER.extract_tldr("## Action\n\nKeep scope.\n"), "")
        self.assertEqual(INDEXER.extract_tldr("```md\n## Action\nFake.\n```\n", decision=True), "")
        self.assertEqual(INDEXER.extract_tldr("```\n**TL;DR:** Example only.\n```\n## Action\nReal call.\n",
                                            decision=True), "Real call.")
        self.assertEqual(INDEXER.extract_tldr("**TL;DR:** Explicit summary.\n\n## Action\nOther text.\n",
                                            decision=True), "Explicit summary.")
        snippet = INDEXER.extract_tldr("## The call\n" + "Retain scope. " * 40, decision=True)
        self.assertLessEqual(len(snippet), 200)
        self.assertTrue(snippet.startswith("Retain scope."))

    def test_writers_refuse_duplicate_decision_id_rows(self) -> None:
        entries = [{"type": "decision", "id": "demo-0001", "path": name}
                   for name in ("one.md", "two.md")]
        destination = self.root / "index.jsonl"
        with self.assertRaises(INDEXER.WikiIndexError):
            INDEXER.write_jsonl(destination, entries)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
