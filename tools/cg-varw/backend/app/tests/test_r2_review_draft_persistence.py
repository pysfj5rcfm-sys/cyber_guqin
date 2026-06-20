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
RESTORE_EXPORT_DIR = R2_RENDER_ROOT / "r2_review_exports" / "2026-06-20_user_review_restore_input"
RENDER_SET_ID = "R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"


class R2ReviewDraftPersistenceTests(unittest.TestCase):
    def test_latest_draft_missing_returns_has_draft_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.load_project_review_draft_latest(RENDER_SET_ID)

        self.assertFalse(result["has_draft"])
        self.assertEqual(RENDER_SET_ID, result["render_set_id"])

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
                "export_tables": {
                    "listening_review.csv": {
                        "file": "listening_review.csv",
                        "columns": ["review_id", "render_set_id", "phrase_id", "active_version_id", "comment", "suggested_revision", "gpt_review_pending", "e_revision_plan_generated", "e_generated", "experimental_render", "production_grade"],
                        "rows": [{
                            "review_id": "R2_REVIEW_XWC_P01_LOCAL_PHRASE_C_QINIST_STYLE",
                            "render_set_id": RENDER_SET_ID,
                            "phrase_id": "XWC_P01_LOCAL_PHRASE",
                            "active_version_id": "C_QINIST_STYLE",
                            "comment": "测试评论",
                            "suggested_revision": "测试修订",
                            "gpt_review_pending": "true",
                            "e_revision_plan_generated": "false",
                            "e_generated": "false",
                            "experimental_render": "true",
                            "production_grade": "false",
                        }],
                    },
                    "listening_review.yaml": {
                        "file": "listening_review.yaml",
                        "columns": ["review_id", "phrase_id", "comment"],
                        "rows": [{"review_id": "R2_REVIEW_XWC_P01_LOCAL_PHRASE_C_QINIST_STYLE", "phrase_id": "XWC_P01_LOCAL_PHRASE", "comment": "测试评论"}],
                    },
                },
            }
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.save_project_review_draft(RENDER_SET_ID, payload)
                latest = store.load_project_review_draft_latest(RENDER_SET_ID)

            latest_dir = Path(result["latest_dir"])
            archive_dir = Path(result["archive_dir"])
            self.assertTrue(latest["has_draft"])
            self.assertTrue((latest_dir / "r2_review_state.latest.json").exists())
            self.assertTrue((latest_dir / "listening_review.csv").exists())
            self.assertTrue((archive_dir / "r2_review_state.latest.json").exists())
            self.assertEqual(1, latest["draft"]["review_count"])
            self.assertFalse(latest["draft"]["e_generated"])

    def test_restore_from_user_export_zip_prefers_listening_review_and_warns_on_partial_alignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.restore_project_review_draft_from_export_dir(RENDER_SET_ID, RESTORE_EXPORT_DIR)
                latest = store.load_project_review_draft_latest(RENDER_SET_ID)

            state_path = Path(result["state_path"])
            state = json.loads(state_path.read_text(encoding="utf-8"))

        self.assertTrue(latest["has_draft"])
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


if __name__ == "__main__":
    unittest.main()
