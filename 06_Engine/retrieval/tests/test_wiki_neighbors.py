from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "wiki_neighbors", Path(__file__).resolve().parents[1] / "wiki-neighbors.py",
)
assert SPEC and SPEC.loader
NEIGHBORS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NEIGHBORS)


class WikiNeighborTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        self.hub = self.root / "01_Project-Hubs/demo"
        self.patch = patch.object(NEIGHBORS, "REPO", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def page(self, relative: str, body: str = "# Note\n", hub: str = "demo") -> dict:
        path = self.root / "01_Project-Hubs" / hub / "_wiki" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "--",
                        str(path.relative_to(self.root))], check=True)
        return {"path": relative, "title": Path(relative).stem, "tldr": "", "tags": []}

    def index(self, rows: list[dict], hub: str = "demo") -> dict:
        wiki = self.root / "01_Project-Hubs" / hub / "_wiki"
        wiki.mkdir(parents=True, exist_ok=True)
        (wiki / "index.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
        return {row["path"]: row for row in rows}

    def overlay(self, edges: list[dict]) -> None:
        path = self.root / "06_Engine/retrieval/legacy/semantic-graph.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"generated_at": "2026-07-03T13:15:49+00:00", "edges": edges}))

    def test_markdown_and_frontmatter_links_are_edges_but_examples_are_not(self) -> None:
        rows = [
            self.page("concepts/seed.md",
                      '---\nsources: ["[[sources/evidence]]"]\n---\n# Seed\n'
                      '[Authored](../concepts/Topic%20%28one%29.md#Heading)\n'
                      '`[[concepts/fake]]`\n```markdown\n[Fake](fake.md)\n```\n'),
            self.page("sources/evidence.md"),
            self.page("concepts/Topic (one).md"),
            self.page("concepts/fake.md"),
        ]
        graph = NEIGHBORS.build_graph(self.hub, self.index(rows))
        self.assertEqual(graph["concepts/seed.md"], {"sources/evidence.md", "concepts/Topic (one).md"})
        self.assertEqual(graph["concepts/fake.md"], set())
        self.assertEqual(graph.provenance[tuple(sorted(("concepts/seed.md", "sources/evidence.md")))],
                         {"authored:wikilink"})

    def test_explicit_cross_hub_links_expand_without_merging_same_named_nodes(self) -> None:
        target = "01_Project-Hubs/other/_wiki/concepts/shared.md"
        local = [
            self.page("concepts/seed.md", f"[[{target}|Other hub]]\n[[concepts/shared]]\n"),
            self.page("concepts/shared.md"),
        ]
        self.index([self.page("concepts/shared.md", hub="other")], hub="other")
        idx = self.index(local)
        graph = NEIGHBORS.build_graph(self.hub, idx)
        self.assertEqual(graph["concepts/seed.md"], {target, "concepts/shared.md"})
        self.assertEqual(NEIGHBORS.build_graph(self.hub, idx, cross_hub=False)["concepts/seed.md"],
                         {"concepts/shared.md"})

    def test_relative_markdown_cross_hub_links_are_supported(self) -> None:
        target = "01_Project-Hubs/other/_wiki/concepts/target.md"
        local = [self.page("concepts/seed.md", "[Other](../../../other/_wiki/concepts/target.md)\n")]
        self.index([self.page("concepts/target.md", hub="other")], hub="other")
        graph = NEIGHBORS.build_graph(self.hub, self.index(local))
        self.assertEqual(graph["concepts/seed.md"], {target})

    def test_unqualified_cross_hub_stems_and_wrong_qualified_paths_do_not_create_edges(self) -> None:
        local = [
            self.page("sources/seed.md", "[[remote]]\n[[missing/shared]]\n[[shared]]\n"),
            self.page("concepts/shared.md"), self.page("entities/shared.md"),
        ]
        self.index([self.page("concepts/remote.md", hub="other")], hub="other")
        graph = NEIGHBORS.build_graph(self.hub, self.index(local))
        self.assertEqual(graph["sources/seed.md"], set())
        self.assertIsNone(NEIGHBORS.norm("shared", graph.rows))
        self.assertIsNone(NEIGHBORS.norm("missing/shared", graph.rows))

    def test_unindexed_local_target_does_not_redirect_to_another_hub(self) -> None:
        local = [self.page("sources/seed.md", "[[concepts/shared]]\n")]
        self.index([self.page("concepts/shared.md", hub="other")], hub="other")
        draft = self.hub / "_wiki/concepts/shared.md"
        draft.parent.mkdir(parents=True)
        draft.write_text("# A local draft, not a published node\n")
        graph = NEIGHBORS.build_graph(self.hub, self.index(local))
        self.assertEqual(graph["sources/seed.md"], set())

    def test_historical_edges_are_opt_in_and_keep_provenance(self) -> None:
        rows = [self.page("concepts/seed.md"), self.page("concepts/history.md")]
        idx = self.index(rows)
        self.overlay([{"source": "seed", "target": "history"}])
        current = NEIGHBORS.build_graph(self.hub, idx)
        self.assertEqual(current["concepts/seed.md"], set())
        self.assertIsNone(current.historical_snapshot)
        historical = NEIGHBORS.build_graph(self.hub, idx, historical_overlay=True)
        self.assertEqual(historical["concepts/seed.md"], {"concepts/history.md"})
        self.assertEqual(historical.provenance[("concepts/history.md", "concepts/seed.md")],
                         {"historical:2026-07-03T13:15:49+00:00"})
        (self.root / "06_Engine/retrieval/legacy/semantic-graph.json").write_text("not valid JSON")
        self.assertEqual(NEIGHBORS.build_graph(self.hub, idx)["concepts/seed.md"], set())

    def test_history_cannot_resolve_ambiguous_stems(self) -> None:
        rows = [self.page("concepts/seed.md"), self.page("concepts/shared.md"),
                self.page("entities/shared.md")]
        self.overlay([{"source": "seed", "target": "shared"}])
        graph = NEIGHBORS.build_graph(self.hub, self.index(rows), historical_overlay=True)
        self.assertEqual(graph["concepts/seed.md"], set())

    def test_cli_labels_history_and_propagates_provenance_through_authored_hops(self) -> None:
        rows = [self.page("concepts/seed.md"),
                self.page("concepts/history.md", "[[concepts/next]]\n"),
                self.page("concepts/next.md")]
        self.index(rows)
        self.overlay([{"source": "seed", "target": "history"}])
        argv = ["wiki-neighbors.py", "demo", "--page", "concepts/seed.md", "--hops", "2"]
        with patch("sys.argv", argv), patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(NEIGHBORS.main(), 0)
        self.assertNotIn("concepts/history.md", output.getvalue())
        with patch("sys.argv", argv + ["--historical-overlay"]), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(NEIGHBORS.main(), 0)
        self.assertIn("2026-07-03", output.getvalue())
        self.assertIn("[1h · historical overlay] concepts/history.md", output.getvalue())
        self.assertIn("[2h · historical overlay] concepts/next.md", output.getvalue())

    def test_authored_edge_wins_when_also_present_in_history(self) -> None:
        rows = [self.page("concepts/seed.md", "[[concepts/real]]\n"),
                self.page("concepts/real.md")]
        self.index(rows)
        self.overlay([{"source": "seed", "target": "real"}])
        with patch("sys.argv", ["wiki-neighbors.py", "demo", "--page", "seed", "--historical-overlay"]), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(NEIGHBORS.main(), 0)
        self.assertIn("[1h · authored link] concepts/real.md", output.getvalue())

    def test_legacy_query_top_hops_and_missing_page_behavior(self) -> None:
        self.index([self.page("concepts/seed.md", "[[concepts/next]]\n"), self.page("concepts/next.md")])
        with patch("sys.argv", ["wiki-neighbors.py", "demo", "seed", "--top", "1", "--hops", "1"]), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(NEIGHBORS.main(), 0)
        self.assertIn("[1h · authored link] concepts/next.md", output.getvalue())
        with patch("sys.argv", ["wiki-neighbors.py", "demo", "--page", "unknown"]), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(NEIGHBORS.main(), 0)
        self.assertIn("No seed page found", output.getvalue())
        self.assertNotIn("## Seeds", output.getvalue())

    def test_missing_local_seed_is_not_replaced_by_a_foreign_stem(self) -> None:
        self.index([self.page("concepts/local.md")])
        self.index([self.page("concepts/remote.md", hub="other")], hub="other")
        with patch("sys.argv", ["wiki-neighbors.py", "demo", "--page", "remote"]), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(NEIGHBORS.main(), 0)
        self.assertIn("No seed page found", output.getvalue())
        self.assertNotIn("## Seeds", output.getvalue())


if __name__ == "__main__":
    unittest.main()
