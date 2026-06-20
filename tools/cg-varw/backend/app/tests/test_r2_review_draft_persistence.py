import csv
import json
import tempfile
import unittest
from os import environ
from pathlib import Path
from unittest.mock import patch

from app.services import r2_mock_store as store


REPO_ROOT = Path(__file__).resolve().parents[5]
R2_RENDER_ROOT = REPO_ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render"
R2_INTAKE_ROOT = R2_RENDER_ROOT / "r2_review_intake"
RENDER_SET_ID = "R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"


class R2ReviewDraftPersistenceTests(unittest.TestCase):
    def test_latest_draft_missing_returns_has_draft_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.load_project_review_draft_latest(RENDER_SET_ID)

        self.assertFalse(result["has_draft"])
        self.assertEqual(RENDER_SET_ID, result["render_set_id"])
        self.assertEqual("none", result["draft_source"])

    def test_save_project_review_draft_writes_latest_archive_and_export_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = {
                "render_set_id": RENDER_SET_ID,
                "data_source": "api",
                "review_status": "draft",
                "active_phrase_id": "XWC_P01_LOCAL_PHRASE",
                "active_version_id": "C_QINIST_STYLE",
                "listeningReviewByKey": {
                    "XWC_P01_LOCAL_PHRASE:C_QINIST_STYLE": {
                        "phrase_id": "XWC_P01_LOCAL_PHRASE",
                        "version_id": "C_QINIST_STYLE",
                        "issue_type": ["phrase_unclear"],
                        "severity": "low",
                        "comment": "测试评论",
                        "suggested_revision": "测试修订",
                        "reviewer": "human",
                        "reviewed_at": "2026-06-20T00:00:00.000Z",
                    }
                },
                "preferredVersionByPhrase": {"XWC_P01_LOCAL_PHRASE": "C_QINIST_STYLE"},
            }
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.save_project_review_draft(RENDER_SET_ID, payload)
                latest = store.load_project_review_draft_latest(RENDER_SET_ID)

            latest_dir = Path(result["latest_dir"])
            archive_dir = Path(result["archive_dir"])
            manifest = json.loads((latest_dir / "r2_review_state_manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(latest["has_draft"])
            self.assertEqual("engineering_dir_latest", latest["draft_source"])
            self.assertTrue((latest_dir / "r2_review_state.latest.json").exists())
            for file_name in store.expected_export_files():
                self.assertTrue((latest_dir / file_name).exists(), file_name)
            self.assertTrue((archive_dir / "r2_review_state.latest.json").exists())
            self.assertEqual(1, latest["draft"]["review_count"])
            self.assertEqual(1, latest["draft"]["phrase_count"])
            self.assertEqual(1, latest["draft"]["suggested_revision_count"])
            self.assertEqual("r2_review_state.latest.json", manifest["canonical_source"])
            self.assertEqual(str(latest_dir / "r2_review_state.latest.json"), manifest["canonical_state_path"])
            self.assertTrue(manifest["no_downloads_policy"])
            self.assertFalse(latest["draft"]["e_generated"])

    def test_restore_from_user_export_zip_prefers_listening_review_and_warns_on_partial_alignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_dir = Path(tmp) / "restore_input"
            write_restore_input(source_dir)
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.restore_project_review_draft_from_export_dir(RENDER_SET_ID, source_dir)
                latest = store.load_project_review_draft_latest(RENDER_SET_ID)

            state_path = Path(result["state_path"])
            state = json.loads(state_path.read_text(encoding="utf-8"))
            manifest = json.loads((state_path.parent / "r2_review_state_manifest.json").read_text(encoding="utf-8"))

        self.assertTrue(latest["has_draft"])
        self.assertEqual("engineering_dir_latest", latest["draft_source"])
        self.assertEqual(28, latest["review_count"])
        self.assertEqual(10, latest["phrase_count"])
        self.assertEqual(10, latest["preferred_version_count"])
        self.assertEqual(28, result["restored_review_count"])
        self.assertEqual(10, result["phrase_count"])
        self.assertEqual(10, result["preferred_version_count"])
        self.assertGreaterEqual(result["suggested_revision_count"], 10)
        self.assertTrue(any("render_phrase_alignment.csv" in warning for warning in result["restore_warnings"]))
        self.assertTrue(any("render_revision_log.yaml" in warning for warning in result["restore_warnings"]))
        self.assertEqual(28, state["review_count"])
        self.assertFalse(state["e_generated"])
        self.assertFalse(state["e_revision_plan_generated"])
        self.assertIn("XWC_P01_LOCAL_PHRASE:C_QINIST_STYLE", state["listeningReviewByKey"])
        self.assertTrue(manifest["restored_from_exports"])
        self.assertEqual(28, manifest["review_count"])
        self.assertEqual(10, manifest["phrase_count"])
        self.assertEqual(10, manifest["preferred_version_count"])
        self.assertEqual(10, manifest["suggested_revision_count"])
        self.assertEqual(3, manifest["warning_count"])
        self.assertEqual("r2_review_state.latest.json", manifest["canonical_source"])
        self.assertEqual(str(state_path), manifest["canonical_state_path"])
        self.assertEqual(str(state_path.parent), manifest["generated_exports_path"])
        self.assertEqual(RENDER_SET_ID, manifest["active_render_set_id"])
        self.assertEqual("engineering_dir_latest", manifest["current_page_load_source"])
        self.assertTrue(manifest["no_downloads_policy"])
        self.assertEqual("XWC_P01_LOCAL_PHRASE", manifest["active_phrase_id"])
        self.assertEqual("C_QINIST_STYLE", manifest["active_version_id"])


def write_restore_input(source_dir: Path) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    phrase_ids = [f"XWC_P{index:02d}_LOCAL_PHRASE" for index in range(1, 11)]
    version_ids = ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC"]
    combos = [("XWC_P01_LOCAL_PHRASE", "C_QINIST_STYLE")]
    combos.extend(
        (phrase_id, version_id)
        for version_id in version_ids
        for phrase_id in phrase_ids
        if (phrase_id, version_id) not in combos
    )
    review_rows = []
    for index in range(28):
        phrase_id, version_id = combos[index]
        review_rows.append(
            {
                "review_id": f"R2_REVIEW_{phrase_id}_{version_id}_{index}",
                "render_set_id": RENDER_SET_ID,
                "phrase_id": phrase_id,
                "section_id": f"XWC_SEC_{1 + index // 14:02d}",
                "event_range": f"{phrase_id}_N01_to_N04",
                "active_version_id": version_id,
                "preferred_version_id": "C_QINIST_STYLE" if index < 5 else "B_PHRASE",
                "quick_judgement": "needs_revision" if index < 10 else "",
                "issue_type": "[\"phrase_unclear\"]" if index < 4 else "[]",
                "severity": "low",
                "comment": f"测试听评 {index}",
                "suggested_revision": f"测试修订 {index}" if index < 10 else "",
                "reviewer": "human",
                "reviewed_at": "2026-06-20T00:00:00+00:00",
                "updated_at": "2026-06-20T00:00:00+00:00",
            }
        )
    preferred_rows = [
        {
            "render_set_id": RENDER_SET_ID,
            "phrase_id": phrase_id,
            "preferred_version_id": "C_QINIST_STYLE" if index < 5 else "B_PHRASE",
        }
        for index, phrase_id in enumerate(phrase_ids)
    ]
    issue_rows = [
        {
            "review_id": row["review_id"],
            "phrase_id": row["phrase_id"],
            "version_id": row["active_version_id"],
            "issue_type": "phrase_unclear",
            "severity": "low",
        }
        for row in review_rows[:4]
    ]
    partial_alignment_rows = [
        {"phrase_id": "XWC_P10_LOCAL_PHRASE", "version_id": version_id, "boundary_status": "candidate"}
        for version_id in ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC"]
    ]
    write_csv(source_dir / "listening_review.csv", review_rows)
    write_table_yaml(source_dir / "listening_review.yaml", review_rows)
    write_csv(source_dir / "preferred_version_summary.csv", preferred_rows)
    write_csv(source_dir / "issue_list.csv", issue_rows)
    write_table_yaml(source_dir / "phrase_structure_review.yaml", [{"phrase_id": phrase_id} for phrase_id in phrase_ids])
    write_csv(source_dir / "render_phrase_alignment.csv", partial_alignment_rows)
    write_csv(source_dir / "phrase_boundary_decision.csv", partial_alignment_rows)
    write_table_yaml(source_dir / "render_revision_log.yaml", [{"revision_id": "R2_REVISION_XWC_P10_LOCAL_PHRASE_A_LITERAL"}])


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0].keys()) if rows else ["empty"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_table_yaml(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0].keys()) if rows else []
    lines = ["file: \"test\"", "rows:"]
    for row in rows:
        lines.append("  -")
        for field in fields:
            lines.append(f"      {field}: {json.dumps(row.get(field, ''), ensure_ascii=False)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
