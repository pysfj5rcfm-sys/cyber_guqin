from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.schemas import Marker, R1Marker, R1MarkerSet, R1SegmentQC, ExportReviewRequest, R1ReviewExportRequest, ReviewUnit, SplitSegment
from app.services import r0_export_writer, r1_review_store, review_unit_builder


class R0ExportSafetyTests(unittest.TestCase):
    def test_r0_export_writes_manifest_and_reload_validation_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            request = ExportReviewRequest(file_id="raw_batch01", source_audio="raw/batch01.wav", units=[_r0_unit()])

            with patch.object(r0_export_writer, "REVIEW_OUTPUT_ROOT", review_root):
                result = r0_export_writer.export_review_csv(request)

            manifest_path = Path(result["manifest_path"])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual("R0", manifest["stage"])
        self.assertEqual("active_internal_state", manifest["canonical_source_role"])
        self.assertTrue(manifest["derived_export_only"])
        self.assertTrue(manifest["compatibility_export_only"])
        self.assertEqual(1, manifest["row_counts"]["reviewed_slate_anchor_manifest.csv"])
        self.assertEqual(5, manifest["row_counts"]["raw_marker_review.csv"])
        self.assertEqual(1, manifest["row_counts"]["split_plan_from_raw_markers.csv"])
        self.assertEqual("pass", manifest["reload_validation"]["status"])
        self.assertEqual(
            sorted(["reviewed_slate_anchor_manifest.csv", "raw_marker_review.csv", "split_plan_from_raw_markers.csv"]),
            sorted(item["path"] for item in manifest["output_hashes"]),
        )

    def test_r0_reload_validation_fails_on_row_count_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            with patch.object(r0_export_writer, "REVIEW_OUTPUT_ROOT", review_root):
                result = r0_export_writer.export_review_csv(
                    ExportReviewRequest(file_id="raw_batch01", source_audio="raw/batch01.wav", units=[_r0_unit()])
                )
            export_dir = Path(result["path"])
            _drop_last_csv_row(export_dir / "raw_marker_review.csv")

            validation = r0_export_writer.validate_r0_export_reload(export_dir)

        self.assertEqual("fail", validation["status"])
        self.assertTrue(any("raw_marker_review.csv row_count mismatch" in note for note in validation["notes"]))

    def test_r0_reload_validation_fails_on_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            with patch.object(r0_export_writer, "REVIEW_OUTPUT_ROOT", review_root):
                result = r0_export_writer.export_review_csv(
                    ExportReviewRequest(file_id="raw_batch01", source_audio="raw/batch01.wav", units=[_r0_unit()])
                )
            export_dir = Path(result["path"])
            with (export_dir / "raw_marker_review.csv").open("a", encoding="utf-8") as handle:
                handle.write("\n")

            validation = r0_export_writer.validate_r0_export_reload(export_dir)

        self.assertEqual("fail", validation["status"])
        self.assertTrue(any("output_hash stale: raw_marker_review.csv" in note for note in validation["notes"]))

    def test_r0_csv_fallback_without_manifest_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "batch01.wav"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(b"not-real-audio")
            review_root = root / "review_outputs"
            export_dir = review_root / "r0" / "exports" / "raw_batch01"
            export_dir.mkdir(parents=True, exist_ok=True)
            _write_r0_raw_marker_review(export_dir / "raw_marker_review.csv", "raw_batch01")

            with patch.object(review_unit_builder, "REVIEW_OUTPUT_ROOT", review_root):
                restored = review_unit_builder.load_units_from_exported_csv("raw_batch01", raw_path)

        self.assertIsNone(restored)

    def test_r0_csv_fallback_with_manifest_records_restore_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "batch01.wav"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(b"not-real-audio")
            review_root = root / "review_outputs"
            request = ExportReviewRequest(file_id="raw_batch01", source_audio=raw_path.name, units=[_r0_unit()])

            with patch.object(r0_export_writer, "REVIEW_OUTPUT_ROOT", review_root):
                r0_export_writer.export_review_csv(request)
            with patch.object(review_unit_builder, "REVIEW_OUTPUT_ROOT", review_root):
                restored = review_unit_builder.load_units_from_exported_csv("raw_batch01", raw_path)

        self.assertIsNotNone(restored)
        assert restored is not None
        self.assertEqual("exported_csv_manifest_guarded", restored["source"])
        self.assertTrue(restored["restored_from_export"])
        self.assertTrue(restored["compatibility_restore"])
        self.assertFalse(restored["canonical_active_draft"])
        self.assertIn("fallback_manifest", restored["provenance"])


class R1ExportSafetyTests(unittest.TestCase):
    def test_r1_export_writes_manifest_and_reload_validation_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            with patch.object(r1_review_store, "REVIEW_OUTPUT_ROOT", review_root):
                result = r1_review_store.export_r1_csv(R1ReviewExportRequest(batch_id="batch01", segments=[_r1_segment()]))

            manifest = json.loads(Path(result["manifest_path"]).read_text(encoding="utf-8"))

        self.assertEqual("R1", manifest["stage"])
        self.assertEqual("active_internal_state", manifest["canonical_source_role"])
        self.assertTrue(manifest["derived_export_only"])
        self.assertEqual(1, manifest["row_counts"]["reviewed_render_anchors.csv"])
        self.assertEqual(4, manifest["row_counts"]["split_marker_review.csv"])
        self.assertEqual(1, manifest["row_counts"]["segment_qc_sheet.csv"])
        self.assertEqual("pass", manifest["reload_validation"]["status"])

    def test_r1_reload_validation_fails_on_row_count_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            with patch.object(r1_review_store, "REVIEW_OUTPUT_ROOT", review_root):
                result = r1_review_store.export_r1_csv(R1ReviewExportRequest(batch_id="batch01", segments=[_r1_segment()]))
            export_dir = Path(result["path"])
            _drop_last_csv_row(export_dir / "split_marker_review.csv")

            validation = r1_review_store.validate_r1_export_reload(export_dir)

        self.assertEqual("fail", validation["status"])
        self.assertTrue(any("split_marker_review.csv row_count mismatch" in note for note in validation["notes"]))

    def test_r1_reload_validation_fails_on_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            with patch.object(r1_review_store, "REVIEW_OUTPUT_ROOT", review_root):
                result = r1_review_store.export_r1_csv(R1ReviewExportRequest(batch_id="batch01", segments=[_r1_segment()]))
            export_dir = Path(result["path"])
            with (export_dir / "reviewed_render_anchors.csv").open("a", encoding="utf-8") as handle:
                handle.write("\n")

            validation = r1_review_store.validate_r1_export_reload(export_dir)

        self.assertEqual("fail", validation["status"])
        self.assertTrue(any("output_hash stale: reviewed_render_anchors.csv" in note for note in validation["notes"]))

    def test_r1_reload_validation_rejects_alias_only_identity_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            with patch.object(r1_review_store, "REVIEW_OUTPUT_ROOT", review_root):
                result = r1_review_store.export_r1_csv(R1ReviewExportRequest(batch_id="batch01", segments=[_r1_segment()]))
            export_dir = Path(result["path"])
            _blank_csv_field(export_dir / "reviewed_render_anchors.csv", "recording_take_no")
            _blank_csv_field(export_dir / "reviewed_render_anchors.csv", "realization_variant")
            _blank_csv_field(export_dir / "reviewed_render_anchors.csv", "render_anchor_type")
            _blank_csv_field(export_dir / "segment_qc_sheet.csv", "reviewed_at")

            validation = r1_review_store.validate_r1_export_reload(export_dir)

        self.assertEqual("fail", validation["status"])
        self.assertTrue(any("recording_take_no missing" in note for note in validation["notes"]))
        self.assertTrue(any("realization_variant missing" in note for note in validation["notes"]))
        self.assertTrue(any("render_anchor_type missing" in note for note in validation["notes"]))
        self.assertTrue(any("reviewed_at missing" in note for note in validation["notes"]))

    def test_r1_export_refuses_take_id_as_recording_take_no(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            segment = _r1_segment(recording_take_no="")

            with patch.object(r1_review_store, "REVIEW_OUTPUT_ROOT", review_root):
                with self.assertRaisesRegex(ValueError, "recording_take_no"):
                    r1_review_store.export_r1_csv(R1ReviewExportRequest(batch_id="batch01", segments=[segment]))

    def test_r1_export_refuses_variant_as_realization_variant(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_root = Path(tmp) / "review_outputs"
            segment = _r1_segment(realization_variant=None)

            with patch.object(r1_review_store, "REVIEW_OUTPUT_ROOT", review_root):
                with self.assertRaisesRegex(ValueError, "realization_variant"):
                    r1_review_store.export_r1_csv(R1ReviewExportRequest(batch_id="batch01", segments=[segment]))


def _r0_unit() -> ReviewUnit:
    return ReviewUnit(
        id="T001",
        sequence=1,
        unit_status="candidate",
        review_status="accepted",
        source="manual",
        takeId="DISPLAY_T001",
        recording_session_id="RS_XWC_002_BAIYA_PILOT",
        recording_id="RECD_002",
        piece_id="XWC",
        qinist_id="QINIST_002",
        batch_id="batch01",
        recording_take_no="T001",
        batch_take_no="001",
        script_id="RS_XWC_002_BAIYA_PILOT_SCRIPT",
        source_raw_audio="raw/batch01.wav",
        event_id="XWC_P01_N01",
        event_range="XWC_P01_N01",
        gesture_id="SAN_TIAO_6",
        expected_sample_type="atomic",
        markers=[
            Marker(key="slate_start", label="口播起始", time=0.1, review_status="accepted"),
            Marker(key="slate_end", label="口播结束", time=0.5, review_status="accepted"),
            Marker(key="guqin_start", label="古琴起声", time=0.8, review_status="accepted"),
            Marker(key="tail_end", label="尾音结束", time=2.3, review_status="accepted"),
            Marker(key="next_slate_start", label="下一口播起始", time=2.7, review_status="accepted"),
        ],
    )


def _r1_segment(**overrides) -> SplitSegment:
    payload = {
        "segment_id": "SEG_001",
        "batch_id": "batch01",
        "take_id": "DISPLAY_T001",
        "file_name": "T001_clean_preview.wav",
        "relative_path": "clean_previews/T001_clean_preview.wav",
        "recording_session_id": "RS_XWC_002_BAIYA_PILOT",
        "recording_id": "RECD_002",
        "piece_id": "XWC",
        "qinist_id": "QINIST_002",
        "recording_take_no": "T001",
        "batch_take_no": "001",
        "script_id": "RS_XWC_002_BAIYA_PILOT_SCRIPT",
        "source_raw_audio": "raw/batch01.wav",
        "source_split_audio": "clean_previews/T001_clean_preview.wav",
        "event_id": "XWC_P01_N01",
        "event_range": "XWC_P01_N01",
        "gesture_id": "SAN_TIAO_6",
        "realization_variant": "clean",
        "duration_s": 2.5,
        "reviewed_by": "reviewer",
        "reviewed_at": "2026-06-22T00:00:00+08:00",
        "markers": R1MarkerSet(
            pre_idle_end=R1Marker(marker_id="SEG_001:pre_idle_end", segment_id="SEG_001", marker_type="pre_idle_end", marker_label_zh="前置空白结束", time_s=0.1, review_status="accepted"),
            gesture_start=R1Marker(marker_id="SEG_001:gesture_start", segment_id="SEG_001", marker_type="gesture_start", marker_label_zh="前导起势", time_s=0.4, review_status="accepted"),
            render_anchor=R1Marker(marker_id="SEG_001:render_anchor", segment_id="SEG_001", marker_type="render_anchor", marker_label_zh="渲染锚点", time_s=0.45, review_status="accepted"),
            tail_end=R1Marker(marker_id="SEG_001:tail_end", segment_id="SEG_001", marker_type="tail_end", marker_label_zh="尾音结束", time_s=2.2, review_status="accepted"),
        ),
        "qc": R1SegmentQC(),
    }
    payload.update(overrides)
    return SplitSegment(**payload)


def _drop_last_csv_row(path: Path) -> None:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows[:-1])


def _blank_csv_field(path: Path, field: str) -> None:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    for row in rows:
        row[field] = ""
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_r0_raw_marker_review(path: Path, file_id: str) -> None:
    unit = _r0_unit()
    rows = [
        {
            "file_id": file_id,
            "unit_id": unit.id,
            "sequence": str(unit.sequence),
            "take_id": unit.takeId,
            "unit_status": unit.unit_status,
            "review_status": marker.review_status,
            "marker_type": marker.key,
            "marker_label_zh": marker.label,
            "time_s": f"{marker.time:.3f}",
            "source": marker.source,
            "confidence": "",
            "nudge_total_ms": "0",
            "notes": "",
            "source_raw_audio": unit.source_raw_audio,
            "recording_session_id": unit.recording_session_id,
            "recording_id": unit.recording_id,
            "piece_id": unit.piece_id,
            "qinist_id": unit.qinist_id,
            "batch_id": unit.batch_id,
            "recording_take_no": unit.recording_take_no,
            "batch_take_no": unit.batch_take_no,
            "script_id": unit.script_id,
            "event_id": unit.event_id,
            "event_range": unit.event_range,
            "gesture_id": unit.gesture_id,
            "expected_sample_type": unit.expected_sample_type,
        }
        for marker in unit.markers
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
