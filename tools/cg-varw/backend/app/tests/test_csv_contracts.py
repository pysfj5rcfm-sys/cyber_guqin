from __future__ import annotations

import unittest

from app.schemas import Marker, R1Marker, R1MarkerSet, R1SegmentQC, ReviewUnit, SplitSegment
from app.services import r0_export_writer, r1_review_store
from app.services.csv_contract_validator import validate_csv_contract


class CsvContractTests(unittest.TestCase):
    def test_r0_rows_include_canonical_provenance_and_split_boundaries(self) -> None:
        unit = ReviewUnit(
            id="UNIT_001",
            sequence=1,
            unit_status="candidate",
            source="asr_candidate",
            takeId="DISPLAY_TAKE_001",
            recording_session_id="RS_TEST",
            recording_id="REC_TEST",
            piece_id="PIECE_TEST",
            qinist_id="QINIST_TEST",
            batch_id="BATCH_TEST",
            recording_take_no="001",
            batch_take_no="A01",
            script_id="SCRIPT_TEST",
            source_raw_audio="raw/test.wav",
            event_id="EVT_001",
            event_range="001",
            gesture_id="GESTURE_001",
            expected_sample_type="single_note",
            markers=[
                Marker(key="slate_start", label="口播起始", time=0.0, review_status="accepted"),
                Marker(key="slate_end", label="口播结束", time=0.3, review_status="accepted"),
                Marker(key="guqin_start", label="古琴起声", time=0.9, review_status="accepted"),
                Marker(key="tail_end", label="尾音结束", time=2.5, review_status="accepted"),
                Marker(key="next_slate_start", label="下一口播起始", time=3.0, review_status="accepted"),
            ],
        )

        manifest = r0_export_writer._manifest_row("FILE_TEST", "raw/test.wav", unit, "2026-06-12T00:00:00+00:00")
        split = r0_export_writer._split_row("FILE_TEST", "raw/test.wav", unit, "2026-06-12T00:00:00+00:00")

        for field in r0_export_writer.MANIFEST_REQUIRED_FIELDS:
            self.assertIn(field, manifest)
        for field in r0_export_writer.SPLIT_REQUIRED_FIELDS:
            self.assertIn(field, split)

        self.assertEqual(manifest["source_raw_audio"], "raw/test.wav")
        self.assertEqual(manifest["source_audio"], "raw/test.wav")
        self.assertEqual(manifest["recording_take_no"], "001")
        self.assertEqual(manifest["take_id"], "DISPLAY_TAKE_001")
        self.assertEqual(split["unit_start_s"], "0.000")
        self.assertEqual(split["unit_end_s"], "3.000")
        self.assertEqual(split["suggested_clean_start_s"], "0.900")
        self.assertEqual(split["suggested_clean_end_s"], "3.000")
        self.assertEqual(split["tail_end_s"], "2.500")
        self.assertEqual(split["split_plan_role"], "clean_preview")
        validate_csv_contract("reviewed_slate_anchor_manifest.csv", [manifest])
        validate_csv_contract("split_plan_from_raw_markers.csv", [split])

    def test_r1_rows_include_canonical_provenance_aliases_and_human_review_fields(self) -> None:
        segment = SplitSegment(
            segment_id="SEG_001",
            batch_id="BATCH_TEST",
            take_id="DISPLAY_TAKE_001",
            file_name="SEG_001.wav",
            relative_path="batch/SEG_001.wav",
            recording_session_id="RS_TEST",
            recording_id="REC_TEST",
            piece_id="PIECE_TEST",
            qinist_id="QINIST_TEST",
            recording_take_no="001",
            batch_take_no="A01",
            script_id="SCRIPT_TEST",
            source_raw_audio="raw/test.wav",
            source_split_audio="split/SEG_001.wav",
            event_id="EVT_001",
            event_range="001",
            gesture_id="GESTURE_001",
            realization_variant="clean",
            duration_s=2.5,
            markers=R1MarkerSet(
                pre_idle_end=R1Marker(marker_id="SEG_001:pre_idle_end", segment_id="SEG_001", marker_type="pre_idle_end", marker_label_zh="前置空白结束", time_s=0.2, review_status="accepted"),
                gesture_start=R1Marker(marker_id="SEG_001:gesture_start", segment_id="SEG_001", marker_type="gesture_start", marker_label_zh="前导起势", time_s=0.4, review_status="accepted"),
                render_anchor=R1Marker(marker_id="SEG_001:render_anchor", segment_id="SEG_001", marker_type="render_anchor", marker_label_zh="渲染锚点", time_s=0.45, review_status="accepted"),
                tail_end=R1Marker(marker_id="SEG_001:tail_end", segment_id="SEG_001", marker_type="tail_end", marker_label_zh="尾音结束", time_s=2.2, review_status="accepted"),
            ),
            qc=R1SegmentQC(),
            reviewed_by="reviewer_test",
            reviewed_at="2026-06-12T00:01:00+00:00",
        )
        segment = r1_review_store.with_derived_state(segment)

        anchor = r1_review_store.reviewed_render_anchor_rows([segment], "2026-06-12T00:02:00+00:00")[0]
        marker = r1_review_store.marker_review_rows([segment], "2026-06-12T00:02:00+00:00")[0]
        qc = r1_review_store.segment_qc_rows([segment], "2026-06-12T00:02:00+00:00")[0]

        for field in r1_review_store.RENDER_ANCHOR_REQUIRED_FIELDS:
            self.assertIn(field, anchor)
        for field in r1_review_store.MARKER_REVIEW_REQUIRED_FIELDS:
            self.assertIn(field, marker)
        for field in r1_review_store.SEGMENT_QC_REQUIRED_FIELDS:
            self.assertIn(field, qc)

        self.assertEqual(anchor["source_split_audio"], "split/SEG_001.wav")
        self.assertEqual(anchor["source_audio"], "split/SEG_001.wav")
        self.assertEqual(anchor["realization_variant"], "clean")
        self.assertEqual(anchor["variant"], "clean")
        self.assertEqual(anchor["render_anchor_type"], "main_attack")
        self.assertEqual(anchor["anchor_type"], "main_attack")
        self.assertEqual(anchor["segment_status"], "render_usable")
        self.assertEqual(qc["human_accepted"], "true")
        self.assertEqual(qc["reviewed_by"], "reviewer_test")
        self.assertEqual(qc["reviewed_at"], "2026-06-12T00:01:00+00:00")
        self.assertNotEqual(qc["reviewed_at"], qc["updated_at"])
        validate_csv_contract("reviewed_render_anchors.csv", [anchor])
        validate_csv_contract("split_marker_review.csv", [marker])
        validate_csv_contract("segment_qc_sheet.csv", [qc])


if __name__ == "__main__":
    unittest.main()
