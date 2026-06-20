import csv
import json
import tempfile
import unittest
import wave
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

    def test_save_project_review_draft_dedupes_phrase_version_reviews(self):
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
                        "comment": "旧评论",
                        "suggested_revision": "旧修订",
                        "reviewer": "human",
                        "updated_at": "2026-06-20T00:00:00.000Z",
                    },
                    "XWC_P01_LOCAL_PHRASE::C_QINIST_STYLE": {
                        "phrase_id": "XWC_P01_LOCAL_PHRASE",
                        "version_id": "C_QINIST_STYLE",
                        "issue_type": ["phrase_unclear"],
                        "severity": "medium",
                        "comment": "试试其它节拍",
                        "suggested_revision": "123——4——",
                        "reviewer": "human",
                        "updated_at": "2026-06-20T01:00:00.000Z",
                    },
                },
                "preferredVersionByPhrase": {"XWC_P01_LOCAL_PHRASE": "C_QINIST_STYLE"},
            }
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.save_project_review_draft(RENDER_SET_ID, payload)
                latest = store.load_project_review_draft_latest(RENDER_SET_ID)

            state = latest["draft"]
            self.assertEqual(1, state["review_count"])
            self.assertIn("XWC_P01_LOCAL_PHRASE:C_QINIST_STYLE", state["listeningReviewByKey"])
            self.assertNotIn("XWC_P01_LOCAL_PHRASE::C_QINIST_STYLE", state["listeningReviewByKey"])
            retained = state["listeningReviewByKey"]["XWC_P01_LOCAL_PHRASE:C_QINIST_STYLE"]
            self.assertEqual("试试其它节拍", retained["comment"])
            self.assertEqual("123——4——", retained["suggested_revision"])
            self.assertEqual(1, len(state["review_history_archived"]))
            self.assertEqual(1, len(state["canonical_dedupe_report"]["duplicate_keys_found"]))
            self.assertEqual(1, state["canonical_dedupe_report"]["duplicate_rows_removed_or_archived"])
            self.assertTrue(Path(result["archive_dir"]).exists())

    def test_export_project_review_draft_csv_writes_project_latest_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = {
                "render_set_id": RENDER_SET_ID,
                "data_source": "api",
                "review_status": "draft",
                "active_phrase_id": "XWC_P10_LOCAL_PHRASE",
                "active_version_id": "A_LITERAL",
                "listeningReviewByKey": {
                    "XWC_P10_LOCAL_PHRASE:A_LITERAL": {
                        "phrase_id": "XWC_P10_LOCAL_PHRASE",
                        "version_id": "A_LITERAL",
                        "issue_type": ["good"],
                        "severity": "low",
                        "comment": "试试其它节拍",
                        "suggested_revision": "1——234——5——6——7——",
                        "reviewer": "human",
                        "updated_at": "2026-06-20T01:00:00.000Z",
                    }
                },
                "preferredVersionByPhrase": {"XWC_P10_LOCAL_PHRASE": "A_LITERAL"},
            }
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                store.save_project_review_draft(RENDER_SET_ID, payload)
                result = store.export_project_review_draft_csv(RENDER_SET_ID)

            latest_dir = Path(result["latest_dir"])
            self.assertEqual(str(latest_dir), result["path"])
            self.assertEqual(8, len(result["files"]))
            for file_name in store.expected_export_files():
                self.assertTrue((latest_dir / file_name).exists(), file_name)
            self.assertEqual(50, count_csv_rows(latest_dir / "render_phrase_alignment.csv"))
            self.assertEqual(50, count_csv_rows(latest_dir / "phrase_boundary_decision.csv"))
            self.assertEqual(1, yaml_rows(latest_dir / "render_revision_log.yaml"))

    def test_e_review_persists_as_future_f_input_without_generating_f(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = {
                "render_set_id": RENDER_SET_ID,
                "data_source": "api",
                "review_status": "draft",
                "active_phrase_id": "XWC_P02_LOCAL_PHRASE",
                "active_version_id": "E_REVIEWED",
                "listeningReviewByKey": {
                    "XWC_P02_LOCAL_PHRASE:E_REVIEWED": {
                        "phrase_id": "XWC_P02_LOCAL_PHRASE",
                        "version_id": "E_REVIEWED",
                        "issue_type": ["too_slow"],
                        "severity": "medium",
                        "comment": "整体建议调整为 1.5 倍速",
                        "suggested_revision": "未来 F 按 E 听评统一收束",
                        "reviewer": "human",
                        "updated_at": "2026-06-20T02:00:00.000Z",
                    }
                },
                "preferredVersionByPhrase": {"XWC_P02_LOCAL_PHRASE": "E_REVIEWED"},
            }
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                store.save_project_review_draft(RENDER_SET_ID, payload)
                result = store.export_project_review_draft_csv(RENDER_SET_ID)
                latest = store.load_project_review_draft_latest(RENDER_SET_ID)

            latest_dir = Path(result["latest_dir"])
            state = latest["draft"]
            self.assertTrue(state["f_generation_pending"])
            self.assertEqual("E_REVIEWED_USER_REVIEW", state["f_input_source"])
            self.assertTrue(state["f_not_generated"])
            self.assertFalse(state["e_generated"])
            self.assertIn("XWC_P02_LOCAL_PHRASE:E_REVIEWED", state["listeningReviewByKey"])
            self.assertEqual("E_REVIEWED", state["preferredVersionByPhrase"]["XWC_P02_LOCAL_PHRASE"])
            self.assertEqual(50, count_csv_rows(latest_dir / "render_phrase_alignment.csv"))
            self.assertEqual(1, yaml_rows(latest_dir / "render_revision_log.yaml"))

    def test_f_final_files_make_f_version_playable(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_f_final_outputs(Path(tmp))
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                versions = store.list_versions(RENDER_SET_ID)
                alignments = store.list_alignments(RENDER_SET_ID)
                audio_path = store.resolve_version_audio_path(RENDER_SET_ID, "F_FINAL_REVIEWED")

        f_version = next(version for version in versions if version.version_id == "F_FINAL_REVIEWED")
        self.assertEqual("final_ready", f_version.status)
        self.assertTrue(f_version.playable)
        self.assertTrue(f_version.alignment_available)
        self.assertEqual("f_final_reviewed_generation", f_version.source)
        self.assertEqual("XWC_BAIYA_F_FINAL_REVIEWED.wav", Path(f_version.audio_path).name)
        self.assertEqual("XWC_BAIYA_F_FINAL_REVIEWED.wav", audio_path.name)
        self.assertEqual(10, len([item for item in alignments if item.version_id == "F_FINAL_REVIEWED"]))

    def test_export_preserves_f_completed_state_and_derives_sixty_alignment_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            render_root = Path(tmp)
            write_f_final_outputs(render_root)
            state = {
                "render_set_id": RENDER_SET_ID,
                "data_source": "api",
                "review_status": "final_ready",
                "active_phrase_id": "XWC_P01_LOCAL_PHRASE",
                "active_version_id": "F_FINAL_REVIEWED",
                "listeningReviewByKey": {
                    "XWC_P10_LOCAL_PHRASE:E_REVIEWED": {
                        "phrase_id": "XWC_P10_LOCAL_PHRASE",
                        "version_id": "E_REVIEWED",
                        "issue_type": ["good"],
                        "severity": "low",
                        "comment": "全曲整体略散漫",
                        "suggested_revision": "全曲建议统一提速，听评1.5倍速正好",
                        "reviewer": "human",
                        "updated_at": "2026-06-20T02:00:00.000Z",
                    }
                },
                "preferredVersionByPhrase": {f"XWC_P{index:02d}_LOCAL_PHRASE": "F_FINAL_REVIEWED" for index in range(1, 11)},
                "f_generation_pending": False,
                "f_not_generated": False,
                "f_generation_completed": True,
                "f_input_source": "E_REVIEWED_USER_REVIEW",
                "f_version_id": "F_FINAL_REVIEWED",
                "provenance": {
                    "f_generation_pending": False,
                    "f_not_generated": False,
                    "f_generation_completed": True,
                    "f_input_source": "E_REVIEWED_USER_REVIEW",
                },
            }
            latest_dir = render_root / "r2_review_drafts" / "latest"
            latest_dir.mkdir(parents=True)
            (latest_dir / "r2_review_state.latest.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": tmp, "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
                result = store.export_project_review_draft_csv(RENDER_SET_ID)
                exported_state = json.loads((latest_dir / "r2_review_state.latest.json").read_text(encoding="utf-8"))
                manifest = json.loads((latest_dir / "r2_review_state_manifest.json").read_text(encoding="utf-8"))
                render_alignment_count = count_csv_rows(latest_dir / "render_phrase_alignment.csv")
                boundary_count = count_csv_rows(latest_dir / "phrase_boundary_decision.csv")
                preferred_count = count_csv_rows(latest_dir / "preferred_version_summary.csv")

        self.assertFalse(exported_state["f_generation_pending"])
        self.assertFalse(exported_state["f_not_generated"])
        self.assertTrue(exported_state["f_generation_completed"])
        self.assertEqual("F_FINAL_REVIEWED", exported_state["f_version_id"])
        self.assertFalse(manifest["f_generation_pending"])
        self.assertTrue(manifest["f_generation_completed"])
        self.assertEqual(60, render_alignment_count)
        self.assertEqual(60, boundary_count)
        self.assertEqual(10, preferred_count)
        self.assertEqual(8, len(result["files"]))

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


def write_f_final_outputs(render_root: Path) -> None:
    f_dir = render_root / "F_FINAL_REVIEWED"
    f_dir.mkdir(parents=True, exist_ok=True)
    with wave.open(str(f_dir / "XWC_BAIYA_F_FINAL_REVIEWED.wav"), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(3)
        handle.setframerate(44100)
        handle.writeframes(b"\x00\x00\x00\x00\x00\x00" * 44100)
    rows = []
    for index in range(1, 11):
        start = float(index - 1)
        rows.append(
            {
                "event_id": f"XWC_P{index:02d}_N01",
                "phrase_id": f"XWC_P{index:02d}_LOCAL_PHRASE",
                "section_id": f"XWC_P{index:02d}",
                "source_version_id": "E_REVIEWED",
                "source_sample_id": f"RECD2_BATCH{index:02d}_T{index:03d}",
                "source_take_id": f"T{index:03d}",
                "source_audio": f"split_preview/T{index:03d}_clean_preview.wav",
                "target_attack_time_s": f"{start + 0.100:.3f}",
                "render_anchor_s": "0.000",
                "phrase_play_start_s": f"{start:.3f}",
                "phrase_play_end_s": f"{start + 0.800:.3f}",
                "phrase_tail_end_s": f"{start + 0.900:.3f}",
                "revision_applied": "E_REVIEWED->F_FINAL_REVIEWED",
                "user_review_source": "E_REVIEWED_USER_REVIEW",
                "gpt_review_decision": "test fixture",
                "flags": "experimental_render=true|production_grade=false",
            }
        )
    write_csv(f_dir / "render_event_alignment.F_FINAL_REVIEWED.csv", rows)


def count_csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def yaml_rows(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() == "-")


if __name__ == "__main__":
    unittest.main()
