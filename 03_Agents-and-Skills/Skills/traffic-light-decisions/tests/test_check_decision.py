#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCRIPT = SKILL / "scripts/check_decision.py"
FIXTURES = HERE / "fixtures"
REPO = SKILL.parents[2]  # flat layout: Skills/<slug>/
AOS_DECISIONS = REPO / "00_Agentic-OS/decisions"
LAYER_CONTRACTS = {
    "L0": ("aos-0001", "l0-authority-and-safety.md"),
    "L1": ("aos-0002", "l1-knowledge-and-context.md"),
    "L2": ("aos-0003", "l2-capabilities-and-interfaces.md"),
    "L3": ("aos-0004", "l3-task-control.md"),
    "L4": ("aos-0005", "l4-delivery-and-outcomes.md"),
    "L5": ("aos-0006", "l5-verification-and-learning.md"),
}


def run(*args: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def frontmatter(path: Path) -> dict[str, str]:
    """Read the flat fields used by the decision contract fixtures."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    header = text.split("---", 2)[1]
    fields: dict[str, str] = {}
    for line in header.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


class DecisionValidatorTests(unittest.TestCase):
    def test_solo_ops_note_passes_without_invented_disagreement(self) -> None:
        result = run(FIXTURES / "valid-solo-ops-note.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_product_decision_passes_with_independent_lifecycle_and_light(self) -> None:
        result = run(FIXTURES / "valid-product-decision.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_release_attestation_passes_without_adr_ceremony(self) -> None:
        result = run(FIXTURES / "valid-release.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_adr_without_alternatives_fails(self) -> None:
        result = run(FIXTURES / "invalid-adr-missing-alternatives.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("at least two documented alternatives", result.stdout)

    def test_yellow_without_trigger_and_expiry_fails(self) -> None:
        result = run(FIXTURES / "invalid-yellow-missing-conditions.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Yellow requires `trigger:`", result.stdout)
        self.assertIn("Yellow requires `expiry:`", result.stdout)

    def test_active_expired_yellow_can_be_reported_without_hiding_other_checks(self) -> None:
        target = FIXTURES / "valid-active-expired-yellow.md"
        authoring = run(target)
        migration = run(target, "--allow-expired")
        self.assertEqual(authoring.returncode, 1)
        self.assertEqual(migration.returncode, 0, migration.stdout + migration.stderr)
        self.assertIn("warning: active Yellow expired", migration.stdout)

    def test_retired_expired_yellow_passes_without_a_successor(self) -> None:
        result = run(FIXTURES / "valid-retired-without-successor.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("active Yellow expired", result.stdout)

    def test_superseded_expired_yellow_reaches_an_accepted_successor(self) -> None:
        result = run(
            FIXTURES / "valid-superseded-expired-yellow.md",
            FIXTURES / "valid-supersession-successor.md",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("active Yellow expired", result.stdout)

    def test_superseded_record_without_successor_fails(self) -> None:
        result = run(FIXTURES / "invalid-superseded-missing-successor.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("`status: superseded` requires `superseded_by:`", result.stdout)

    def test_superseded_record_with_ambiguous_successors_fails(self) -> None:
        result = run(FIXTURES / "invalid-ambiguous-successors.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("`status: superseded` requires exactly one successor", result.stdout)

    def test_accepted_predecessor_cannot_be_ambiguously_replaced(self) -> None:
        result = run(
            FIXTURES / "invalid-accepted-predecessor.md",
            FIXTURES / "invalid-successor-of-accepted.md",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires `test-0010` to use `status: superseded`", result.stdout)

    def test_canonical_true_requires_an_accepted_adr(self) -> None:
        result = run(FIXTURES / "invalid-canonical-non-adr.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("`canonical: true` requires an accepted ADR", result.stdout)

    def test_supersession_cycle_fails(self) -> None:
        result = run(
            FIXTURES / "invalid-cycle-a.md",
            FIXTURES / "invalid-cycle-b.md",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("supersession cycle detected", result.stdout)

    def test_supersession_dead_end_fails(self) -> None:
        result = run(FIXTURES / "invalid-dead-end.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not resolve", result.stdout)

    def test_duplicate_canonical_id_fails(self) -> None:
        result = run(FIXTURES / "duplicate-id-a.md", FIXTURES / "duplicate-id-b.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate canonical id", result.stdout)

    def test_repository_discovery_audits_every_namespace(self) -> None:
        result = run("--repo-root", REPO, "--minimum-count", "6", "--quiet")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        found = re.search(r"(\d+) record\(s\) discovered", result.stdout)
        self.assertIsNotNone(found, result.stdout)
        self.assertGreaterEqual(int(found.group(1)), 6)
        self.assertIn("0 error(s)", result.stdout)

    def test_agentic_os_has_exactly_one_canonical_adr_per_layer(self) -> None:
        canonical = {
            fields.get("id", "")
            for path in AOS_DECISIONS.rglob("*.md")
            if (fields := frontmatter(path)).get("canonical", "").lower() == "true"
        }
        self.assertEqual(canonical, {identifier for identifier, _ in LAYER_CONTRACTS.values()})
        top_level_records = {path.name for path in AOS_DECISIONS.glob("*.md") if path.name != "index.md"}
        self.assertEqual(top_level_records, {filename for _, filename in LAYER_CONTRACTS.values()})
        for layer, (identifier, filename) in LAYER_CONTRACTS.items():
            path = AOS_DECISIONS / filename
            fields = frontmatter(path)
            self.assertEqual(fields.get("id"), identifier)
            self.assertEqual(fields.get("layer"), layer)
            self.assertEqual(fields.get("record_type"), "adr")
            self.assertEqual(fields.get("status"), "accepted")
            self.assertIn(f"# {identifier} — {layer} ", path.read_text(encoding="utf-8"))

    def test_canonical_manifest_has_six_contracts_without_history_bodies(self) -> None:
        result = run("--repo-root", REPO, "--canonical", "--json", "--expected-count", "6",
                     "--expected-layers", *LAYER_CONTRACTS)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["count"], 6)
        self.assertEqual(payload["errors"], 0)
        self.assertEqual({record["id"] for record in payload["records"]},
                         {identifier for identifier, _ in LAYER_CONTRACTS.values()})
        self.assertEqual({record["layer"] for record in payload["records"]}, set(LAYER_CONTRACTS))
        self.assertLess(len(result.stdout), 6000)
        for record in payload["records"]:
            self.assertNotIn("/records/", record["path"])
            self.assertNotIn("body", record)
            self.assertLessEqual(record["body_words"], 600)
            self.assertTrue((REPO / record["path"]).is_file())
        self.assertEqual({record["light"] for record in payload["records"]}, {"green"})

    def test_reviewer_contract_route_matches_scoped_manifest(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO / "00_Agentic-OS/agentic-os-review.py"), "--contracts-only"],
            cwd=REPO, text=True, capture_output=True, check=False,
        )
        direct = run(AOS_DECISIONS, "--canonical", "--expected-count", "6",
                     "--expected-layers", *LAYER_CONTRACTS, "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), json.loads(direct.stdout))

    def test_canonical_filter_does_not_hide_invalid_canonical_records(self) -> None:
        result = run(FIXTURES / "invalid-canonical-non-adr.md", "--canonical", "--json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["count"], 1)
        self.assertGreater(payload["errors"], 0)

    def test_invalid_canonical_marker_fails_instead_of_disappearing(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid-marker.md"
            source = (FIXTURES / "invalid-canonical-non-adr.md").read_text(encoding="utf-8")
            path.write_text(source.replace("canonical: true", "canonical: maybe"), encoding="utf-8")
            result = run(path, "--canonical", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["count"], 1)
        self.assertIn("must be true or false", result.stdout)

    def test_missing_target_fails_without_traceback(self) -> None:
        result = run(FIXTURES / "does-not-exist.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing target", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_empty_canonical_selection_fails(self) -> None:
        result = run(FIXTURES / "valid-solo-ops-note.md", "--canonical", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["count"], 0)

    def test_canonical_selection_cannot_claim_a_history_manifest_audit(self) -> None:
        result = run(AOS_DECISIONS, "--canonical", "--manifest", FIXTURES / "unused-manifest.csv")
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires the full corpus", result.stderr)

    def test_unreadable_record_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "unreadable.md"
            path.write_bytes(b"\xff\xfe")
            result = run(path, "--json")
        self.assertEqual(result.returncode, 1)
        self.assertGreater(json.loads(result.stdout)["errors"], 0)

    def test_canonical_body_budget_prevents_context_growth(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "overlong.md"
            source = (AOS_DECISIONS / LAYER_CONTRACTS["L0"][1]).read_text(encoding="utf-8")
            source = source.replace("id: aos-0001", "id: test-0099").replace("supersedes: [aos-0010]\n", "")
            path.write_text(source + "\n" + "detail " * 601, encoding="utf-8")
            result = run(path, "--canonical", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("exceeds 600 words", result.stdout)

    def test_layer_guard_rejects_duplicate_layers_even_when_count_is_correct(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            source = (AOS_DECISIONS / LAYER_CONTRACTS["L0"][1]).read_text(encoding="utf-8")
            source = source.replace("supersedes: [aos-0010]\n", "")
            first, second = Path(folder) / "first.md", Path(folder) / "second.md"
            first.write_text(source.replace("id: aos-0001", "id: test-0080"), encoding="utf-8")
            second.write_text(source.replace("id: aos-0001", "id: test-0081"), encoding="utf-8")
            result = run(first, second, "--canonical", "--expected-count", "2", "--expected-layers", "L0", "L1", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["count"], 2)
        self.assertIn("expected one canonical ADR per layer", result.stdout)

    def test_layer_guard_rejects_missing_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing-layer.md"
            source = (AOS_DECISIONS / LAYER_CONTRACTS["L0"][1]).read_text(encoding="utf-8")
            source = source.replace("id: aos-0001", "id: test-0082").replace("supersedes: [aos-0010]\n", "")
            path.write_text(source.replace("layer: L0\n", ""), encoding="utf-8")
            result = run(path, "--canonical", "--expected-layers", "L0", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("<missing>", result.stdout)

    def test_layer_guard_rejects_extra_layer(self) -> None:
        result = run(AOS_DECISIONS / LAYER_CONTRACTS["L0"][1],
                     AOS_DECISIONS / LAYER_CONTRACTS["L1"][1],
                     "--canonical", "--expected-layers", "L0", "--json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected one canonical ADR per layer", result.stdout)

    def test_layer_metadata_rejects_invalid_values_and_non_adrs(self) -> None:
        for source_file, layer in ((LAYER_CONTRACTS["L0"][1], "L9"), ("valid-solo-ops-note.md", "L0")):
            with self.subTest(source=source_file), tempfile.TemporaryDirectory() as folder:
                source_root = AOS_DECISIONS if layer == "L9" else FIXTURES
                source = (source_root / source_file).read_text(encoding="utf-8")
                source = source.replace("id: aos-0001", "id: test-0083").replace("supersedes: [aos-0010]\n", "")
                source = source.replace("layer: L0\n", "")
                source = source.replace("schema_version: decision-record/v2", f"schema_version: decision-record/v2\nlayer: {layer}")
                path = Path(folder) / "invalid-layer.md"
                path.write_text(source, encoding="utf-8")
                result = run(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("`layer:`", result.stdout)

    def test_layer_guard_requires_canonical_selection_and_unique_requested_layers(self) -> None:
        target = AOS_DECISIONS / LAYER_CONTRACTS["L0"][1]
        for arguments, error in (
            (("--expected-layers", "L0"), "requires --canonical selection"),
            (("--canonical", "--expected-layers", "L0", "L0"), "must list each layer once"),
        ):
            result = run(target, *arguments)
            self.assertEqual(result.returncode, 2)
            self.assertIn(error, result.stderr)

    def test_relevant_single_layer_can_be_validated_without_loading_all_six_bodies(self) -> None:
        result = run(AOS_DECISIONS / LAYER_CONTRACTS["L3"][1],
                     "--canonical", "--expected-layers", "L3", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["records"][0]["layer"], "L3")
        self.assertNotIn("body", payload["records"][0])

    def test_current_guides_link_to_every_owning_layer(self) -> None:
        for relative in ("AUTHORITIES.md", "00_Agentic-OS/README.md", "00_README/ARCHITECTURE.md"):
            text = (REPO / relative).read_text(encoding="utf-8")
            for _, filename in LAYER_CONTRACTS.values():
                self.assertIn(filename, text, relative)
            self.assertNotIn("two architecture contracts", text)
            self.assertNotIn("two-ADR set", text)

    def test_canonical_adr_local_links_resolve(self) -> None:
        for _, filename in LAYER_CONTRACTS.values():
            path = AOS_DECISIONS / filename
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                target = link.split("#", 1)[0]
                if target and "://" not in target:
                    self.assertTrue((path.parent / target).exists(), f"{filename}: {link}")

    def test_authority_and_operating_reference_links_resolve(self) -> None:
        guides = (
            REPO / "AUTHORITIES.md",
            REPO / "00_Agentic-OS/README.md",
            REPO / "00_README/ARCHITECTURE.md",
            REPO / "AGENTS.md",
            REPO / "02_Workflows/workflows/W5-decide.md",
            SKILL / "SKILL.md",
            SKILL / "references/REFERENCE.md",
            SKILL / "assets/decision-record.template.md",
            SKILL.parent / "drift-check/SKILL.md",
            REPO / "02_Workflows/prompts/drift-check.prompt.md",
        )
        for path in guides:
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                target = link.split("#", 1)[0]
                if target and "://" not in target:
                    self.assertTrue((path.parent / target).exists(), f"{path.relative_to(REPO)}: {link}")

    def test_boot_evidence_pointer_uses_the_existing_authority(self) -> None:
        text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        self.assertNotIn("00_README/_frameworks/evidence-tagging.md", text)
        self.assertIn("00_README/_frameworks/house-principles.md#4-evidence--opinion-but-evidence-is-rare", text)
        self.assertTrue((REPO / "00_README/_frameworks/house-principles.md").is_file())
        for adapter in ("CLAUDE.md", ".github/copilot-instructions.md"):
            self.assertIn("AGENTS.md", (REPO / adapter).read_text(encoding="utf-8"))

    def test_phase_routes_preserve_evidence_without_mandatory_adr_files(self) -> None:
        routes = [REPO / f"02_Workflows/workflows/W{number}-{phase}.md"
                  for number, phase in enumerate(("understand", "design", "build", "learn"), start=1)]
        routes.extend((REPO / "00_README/_frameworks/design-thinking-loop.md",
                       SKILL.parent / "design-thinking-loop/SKILL.md"))
        obsolete = (
            "record an ADR:", "Every decision along the way as an ADR", "Log as ADR via",
            "closed (ADR linked)", "ADR if non-obvious", "Sign the forward-path ADR",
            "ADR logged with clear next-workflow reference", "ADR with the next-loop decision",
            "phase's `decisions/` subfolder AND `_wiki/decisions/`",
        )
        for path in routes:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("W5", text)
                self.assertIn("evidence", text)
                self.assertIn("no new decision file", text)
                for phrase in obsolete:
                    self.assertNotIn(phrase, text)

    def test_phase_templates_do_not_restore_mandatory_adr_paperwork(self) -> None:
        names = (
            "0-0-Ops_execution-plan.template.md",
            "0-2-Ops_operating-rhythm.template.md",
            "1-3b-Understand_jtbd-synthesis.template.md",
            "2-3-Design_PRD.template.md",
            "4-1-Learn_evidence-brief.template.md",
            "4-2-Learn_retro.template.md",
        )
        obsolete = (
            "≥1 ADR", "phase gate ADR", "log as ADR", "logged as ADR", "ADR link once W5",
            "Every decision links to a §B record", "≥2 reviewers from different functions",
            "Traffic Light + ADR",
        )
        for name in names:
            path = REPO / "00_README/_templates" / name
            text = path.read_text(encoding="utf-8")
            with self.subTest(template=name):
                for phrase in obsolete:
                    self.assertNotIn(phrase, text)
                for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                    target = link.split("#", 1)[0]
                    if target and "://" not in target and "<" not in target and "&lt;" not in target:
                        self.assertTrue((path.parent / target).exists(), f"{name}: {link}")

    def test_drift_assessment_routes_to_evidence_not_an_automatic_adr(self) -> None:
        template = SKILL.parent / "drift-check/assets/drift-finding.template.md"
        self.assertEqual(frontmatter(template)["type"], "evaluation")
        self.assertNotIn("record_type", frontmatter(template))
        for path in (template, SKILL.parent / "drift-check/SKILL.md",
                     REPO / "02_Workflows/prompts/drift-check.prompt.md"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("no new decision file", text)
                self.assertIn("W5", text)
                self.assertNotIn("file as an adr", text.lower())
                self.assertNotIn("file it as an adr", text.lower())


if __name__ == "__main__":
    unittest.main()
