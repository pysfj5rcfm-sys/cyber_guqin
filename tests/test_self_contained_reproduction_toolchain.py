import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

RECORDING_SCRIPT = ROOT / "scripts" / "generate_recording_plan_from_dapu_ir.py"
ABCD_SCRIPT = ROOT / "scripts" / "render_abcd_from_manifest.py"
FINAL_SCRIPT = ROOT / "tools" / "cg-varw" / "backend" / "scripts" / "generate_final_reviewed_render.py"
VERIFY_SCRIPT = ROOT / "tools" / "cg-varw" / "backend" / "scripts" / "verify_r2_render_manifest.py"

EXAMPLES = ROOT / "examples" / "cyber_guqin"
RECORDING_CONFIG = EXAMPLES / "xwc_recording_plan_config.yaml"
DAPU_FIXTURE = EXAMPLES / "xwc_dapu_ir_minimal_fixture.jsonl"
ABCD_MANIFEST = EXAMPLES / "xwc_abcd_render_manifest.yaml"
FINAL_MANIFEST = EXAMPLES / "xwc_final_render_manifest.yaml"
VERIFY_MANIFEST = EXAMPLES / "xwc_r2_render_verify_manifest.yaml"

RUNBOOK = ROOT / "docs" / "cyber_guqin" / "XWC_F_REPRODUCTION_RUNBOOK.md"
REGISTRY = ROOT / "docs" / "cyber_guqin" / "SCRIPT_REGISTRY.md"
WORKFLOW_SKILL = ROOT / ".agents" / "skills" / "cyber_guqin_mvp_workflow" / "SKILL.md"

BAIYA_PLAN_SCRIPT = ROOT / "scripts" / "generate_baiya_recording_plan.py"
BAIYA_PLAN_SHA256 = "34ee60f94f64e7f14161f583fd29ac8ddbe256055e00fe12439e03c7b167d7de"
FULL_TAIL_SCRIPT = ROOT / "tools" / "cg-varw" / "backend" / "scripts" / "refresh_xwc_r1_full_tail_and_regenerate_f.py"


def run_cmd(args, cwd=ROOT, check=True):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed: {' '.join(str(item) for item in args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def load_json_compatible_yaml(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class RecordingPlanToolchainTests(unittest.TestCase):
    def test_recording_plan_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "recording_plan"
            result = run_cmd(
                [
                    PYTHON,
                    str(RECORDING_SCRIPT),
                    "--piece-id",
                    "FIXTURE_PIECE",
                    "--session-id",
                    "RS_FIXTURE",
                    "--recording-id",
                    "REC_FIXTURE",
                    "--qinist-id",
                    "QINIST_FIXTURE",
                    "--qinist-name",
                    "Fixture Qinist",
                    "--dapu-ir",
                    str(DAPU_FIXTURE),
                    "--recording-config",
                    str(RECORDING_CONFIG),
                    "--output-root",
                    str(out),
                    "--dry-run",
                ]
            )
            self.assertIn("DRY_RUN", result.stdout)
            self.assertIn("expected_output_paths", result.stdout)
            self.assertFalse(out.exists())

    def test_recording_plan_execute_writes_five_outputs_to_temp_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "recording_plan"
            run_cmd(
                [
                    PYTHON,
                    str(RECORDING_SCRIPT),
                    "--piece-id",
                    "FIXTURE_PIECE",
                    "--session-id",
                    "RS_FIXTURE",
                    "--recording-id",
                    "REC_FIXTURE",
                    "--qinist-id",
                    "QINIST_FIXTURE",
                    "--qinist-name",
                    "Fixture Qinist",
                    "--dapu-ir",
                    str(DAPU_FIXTURE),
                    "--recording-config",
                    str(RECORDING_CONFIG),
                    "--output-root",
                    str(out),
                    "--execute",
                ]
            )
            expected = {
                "recording_take_plan.csv",
                "recording_batch_plan.csv",
                "recording_coverage_gap.csv",
                "recording_plan_human_review.md",
                "recording_plan_manifest.json",
            }
            self.assertEqual(expected, {path.name for path in out.iterdir()})

    def test_recording_plan_batching_context_tail_manifest_and_slate(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "recording_plan"
            run_cmd(
                [
                    PYTHON,
                    str(RECORDING_SCRIPT),
                    "--piece-id",
                    "FIXTURE_PIECE",
                    "--session-id",
                    "RS_FIXTURE",
                    "--recording-id",
                    "REC_FIXTURE",
                    "--qinist-id",
                    "QINIST_FIXTURE",
                    "--qinist-name",
                    "Fixture Qinist",
                    "--dapu-ir",
                    str(DAPU_FIXTURE),
                    "--recording-config",
                    str(RECORDING_CONFIG),
                    "--output-root",
                    str(out),
                    "--execute",
                ]
            )
            with (out / "recording_take_plan.csv").open(encoding="utf-8-sig", newline="") as handle:
                take_rows = list(csv.DictReader(handle))
            with (out / "recording_batch_plan.csv").open(encoding="utf-8-sig", newline="") as handle:
                batch_rows = list(csv.DictReader(handle))
            manifest = json.loads((out / "recording_plan_manifest.json").read_text(encoding="utf-8"))
            self.assertLessEqual(max(int(row["expected_take_count"]) for row in batch_rows), 10)
            self.assertTrue(any(row["is_context_take"] == "true" and row["event_id"] == "FIXTURE_CONTEXT_A" for row in take_rows))
            self.assertTrue(any(row["tail_policy"] == "full_tail" and row["event_id"] == "FIXTURE_LONG_TAIL" for row in take_rows))
            self.assertEqual(len(take_rows), manifest["row_counts"]["recording_take_plan.csv"])
            self.assertIn("slate", take_rows[0]["spoken_slate_text"].lower())
            self.assertNotIn("T060", RECORDING_SCRIPT.read_text(encoding="utf-8"))
            self.assertNotIn("T071", RECORDING_SCRIPT.read_text(encoding="utf-8"))

    def test_recording_plan_missing_required_fields_fail_clearly(self):
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "broken.jsonl"
            broken.write_text('{"event_id":"ONLY_ID"}\n', encoding="utf-8")
            result = run_cmd(
                [
                    PYTHON,
                    str(RECORDING_SCRIPT),
                    "--piece-id",
                    "FIXTURE_PIECE",
                    "--session-id",
                    "RS_FIXTURE",
                    "--recording-id",
                    "REC_FIXTURE",
                    "--qinist-id",
                    "QINIST_FIXTURE",
                    "--qinist-name",
                    "Fixture Qinist",
                    "--dapu-ir",
                    str(broken),
                    "--recording-config",
                    str(RECORDING_CONFIG),
                    "--output-root",
                    str(Path(tmp) / "out"),
                    "--dry-run",
                ],
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required field", result.stderr)


class RenderToolchainTests(unittest.TestCase):
    def test_abcd_dry_run_does_not_write_audio_and_uses_manifest_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cmd(
                [
                    PYTHON,
                    str(ABCD_SCRIPT),
                    "--render-manifest",
                    str(ABCD_MANIFEST),
                    "--output-root",
                    str(Path(tmp) / "reproduction_runs" / "RUN_ID" / "abcd"),
                    "--dry-run",
                ]
            )
            self.assertIn("DRY_RUN", result.stdout)
            self.assertIn("planned_output_paths", result.stdout)
            self.assertFalse(list(Path(tmp).rglob("*.wav")))

    def test_abcd_manifest_validation_and_baseline_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.yaml"
            bad.write_text(json.dumps({"piece_id": "P", "output_root": "reproduction_runs/RUN/abcd"}), encoding="utf-8")
            result = run_cmd([PYTHON, str(ABCD_SCRIPT), "--render-manifest", str(bad), "--dry-run"], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required manifest field", result.stderr)

            baseline = (
                ROOT
                / "04_outputs"
                / "XWC"
                / "RS_XWC_002_BAIYA_PILOT"
                / "abcd_experimental_render"
                / "F_FINAL_REVIEWED"
            )
            result = run_cmd(
                [
                    PYTHON,
                    str(ABCD_SCRIPT),
                    "--render-manifest",
                    str(ABCD_MANIFEST),
                    "--output-root",
                    str(baseline),
                    "--execute",
                ],
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("accepted baseline", result.stderr)

    def test_abcd_script_has_no_xwc_or_take_hardcode(self):
        text = ABCD_SCRIPT.read_text(encoding="utf-8")
        for forbidden in ["RS_XWC_002_BAIYA_PILOT", "XWC_P09", "T060", "T071", "Baiya", "白牙"]:
            self.assertNotIn(forbidden, text)


class FinalRenderAndVerifierTests(unittest.TestCase):
    def test_final_render_dry_run_does_not_write_and_reports_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cmd(
                [
                    PYTHON,
                    str(FINAL_SCRIPT),
                    "--final-render-manifest",
                    str(FINAL_MANIFEST),
                    "--output-root",
                    str(Path(tmp) / "reproduction_runs" / "RUN_ID" / "final"),
                    "--dry-run",
                ]
            )
            self.assertIn("DRY_RUN", result.stdout)
            self.assertIn("authority_summary", result.stdout)
            self.assertFalse(list(Path(tmp).rglob("*.wav")))

    def test_final_render_rejects_forbidden_authority_and_requires_sandbox(self):
        manifest = load_json_compatible_yaml(FINAL_MANIFEST)
        with tempfile.TemporaryDirectory() as tmp:
            forbidden = dict(manifest)
            forbidden["source_review_state"] = "Downloads/r2_review_state.latest.json"
            bad = Path(tmp) / "bad_final.yaml"
            bad.write_text(json.dumps(forbidden), encoding="utf-8")
            result = run_cmd([PYTHON, str(FINAL_SCRIPT), "--final-render-manifest", str(bad), "--dry-run"], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("forbidden authority", result.stderr)

            no_sandbox = dict(manifest)
            no_sandbox["output_root"] = str(Path(tmp) / "plain_output")
            bad.write_text(json.dumps(no_sandbox), encoding="utf-8")
            result = run_cmd([PYTHON, str(FINAL_SCRIPT), "--final-render-manifest", str(bad), "--execute"], check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reproduction sandbox", result.stderr)

    def test_final_render_refuses_accepted_baseline_and_has_no_xwc_phrase_hardcode(self):
        baseline = (
            ROOT
            / "04_outputs"
            / "XWC"
            / "RS_XWC_002_BAIYA_PILOT"
            / "abcd_experimental_render"
            / "F_FINAL_REVIEWED"
        )
        result = run_cmd(
            [
                PYTHON,
                str(FINAL_SCRIPT),
                "--final-render-manifest",
                str(FINAL_MANIFEST),
                "--output-root",
                str(baseline),
                "--execute",
            ],
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("accepted baseline", result.stderr)
        text = FINAL_SCRIPT.read_text(encoding="utf-8")
        for forbidden in ["T008", "T014", "XWC_P02", "XWC_P09", "RS_XWC_002_BAIYA_PILOT", "白牙"]:
            self.assertNotIn(forbidden, text)

    def test_verifier_accepts_canonical_latest_and_rejects_derived_or_forbidden_sources(self):
        result = run_cmd(
            [
                PYTHON,
                str(VERIFY_SCRIPT),
                "--review-state",
                str(ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render" / "r2_review_drafts" / "latest" / "r2_review_state.latest.json"),
                "--render-manifest",
                str(VERIFY_MANIFEST),
            ]
        )
        self.assertIn("PASS", result.stdout)

        with tempfile.TemporaryDirectory() as tmp:
            derived = dict(load_json_compatible_yaml(VERIFY_MANIFEST))
            derived["source_review_state"] = str(
                ROOT
                / "04_outputs"
                / "XWC"
                / "RS_XWC_002_BAIYA_PILOT"
                / "abcd_experimental_render"
                / "r2_review_drafts"
                / "latest"
                / "listening_review.csv"
            )
            bad = Path(tmp) / "bad_verify.yaml"
            bad.write_text(json.dumps(derived), encoding="utf-8")
            result = run_cmd(
                [
                    PYTHON,
                    str(VERIFY_SCRIPT),
                    "--review-state",
                    str(ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render" / "r2_review_drafts" / "latest" / "r2_review_state.latest.json"),
                    "--render-manifest",
                    str(bad),
                ],
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("derived-only authority", result.stderr)


class DocsExamplesAndLegacySafetyTests(unittest.TestCase):
    def test_examples_parse_successfully(self):
        for path in [RECORDING_CONFIG, ABCD_MANIFEST, FINAL_MANIFEST, VERIFY_MANIFEST]:
            parsed = load_json_compatible_yaml(path)
            self.assertIsInstance(parsed, dict, path)
        lines = [line for line in DAPU_FIXTURE.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(lines), 3)
        self.assertTrue(all(isinstance(json.loads(line), dict) for line in lines))

    def test_runbook_and_registry_cover_replay_and_stop_rules(self):
        runbook = RUNBOOK.read_text(encoding="utf-8")
        registry = REGISTRY.read_text(encoding="utf-8")
        for required in [
            "verify_r2_render_manifest.py",
            "generate_recording_plan_from_dapu_ir.py",
            "render_abcd_from_manifest.py",
            "generate_final_reviewed_render.py",
            "--dry-run",
            "Stop Rules",
            "F_FINAL_REVIEWED",
            "reproduction_runs",
        ]:
            self.assertIn(required, runbook)
        for required in [
            "scripts/generate_recording_plan_from_dapu_ir.py",
            "scripts/render_abcd_from_manifest.py",
            "tools/cg-varw/backend/scripts/generate_final_reviewed_render.py",
            "tools/cg-varw/backend/scripts/verify_r2_render_manifest.py",
            "scripts/generate_baiya_recording_plan.py",
            "refresh_xwc_r1_full_tail_and_regenerate_f.py",
            "historical_only",
        ]:
            self.assertIn(required, registry)

    def test_script_help_is_available_for_fresh_user(self):
        for script in [RECORDING_SCRIPT, ABCD_SCRIPT, FINAL_SCRIPT, VERIFY_SCRIPT]:
            result = run_cmd([PYTHON, str(script), "--help"])
            self.assertIn("usage:", result.stdout)
            self.assertIn("--dry-run", result.stdout + result.stderr)

    def test_old_baiya_script_is_unmodified_and_full_tail_is_historical_only(self):
        self.assertTrue(BAIYA_PLAN_SCRIPT.exists())
        digest = hashlib.sha256(BAIYA_PLAN_SCRIPT.read_bytes()).hexdigest()
        self.assertEqual(BAIYA_PLAN_SHA256, digest)
        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("current untracked / historical template / do not run directly", registry)
        self.assertIn(str(FULL_TAIL_SCRIPT.relative_to(ROOT)), registry)
        self.assertIn("historical_only", registry)

    def test_workflow_skill_exists_and_docs_do_not_require_codex_memory(self):
        self.assertTrue(WORKFLOW_SKILL.exists())
        runbook = RUNBOOK.read_text(encoding="utf-8")
        self.assertNotIn("聊天记录", runbook)
        self.assertIn("用户脱离 Codex", runbook)


if __name__ == "__main__":
    unittest.main()
