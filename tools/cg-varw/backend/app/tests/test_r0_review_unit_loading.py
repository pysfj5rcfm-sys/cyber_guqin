import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.services import review_unit_builder
from app.services.export_safety_manifest import sha256_path


class R0ReviewUnitLoadingTests(unittest.TestCase):
    def test_load_or_build_review_units_uses_manifest_guarded_exported_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "batch01.wav"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(b"not-a-real-wav")
            review_root = root / "review_outputs"
            file_id = "batch01_wav"
            export_dir = review_root / "r0" / "exports" / file_id
            export_dir.mkdir(parents=True, exist_ok=True)
            write_raw_marker_review(export_dir / "raw_marker_review.csv", file_id)
            write_export_manifest(export_dir)

            with patch.object(review_unit_builder, "REVIEW_OUTPUT_ROOT", review_root):
                result = review_unit_builder.load_or_build_review_units(file_id, raw_path)

        self.assertEqual("exported_csv_manifest_guarded", result["source"])
        self.assertIn("导出 CSV", result["message"])
        self.assertTrue(result["restored_from_export"])
        self.assertTrue(result["compatibility_restore"])
        self.assertFalse(result["canonical_active_draft"])
        self.assertEqual(1, len(result["units"]))
        unit = result["units"][0]
        self.assertEqual("T001", unit["id"])
        self.assertEqual("accepted", unit["review_status"])
        self.assertEqual("render_usable", unit["unit_status"])
        self.assertEqual("SAN_TIAO_6", unit["gesture_id"])
        markers = {marker["key"]: marker for marker in unit["markers"]}
        self.assertEqual({"slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"}, set(markers))
        self.assertEqual("human_adjusted", markers["guqin_start"]["source"])
        self.assertEqual(12, markers["guqin_start"]["nudge_total_ms"])


def write_raw_marker_review(path: Path, file_id: str) -> None:
    rows = []
    marker_times = {
        "slate_start": "0.100",
        "slate_end": "0.550",
        "guqin_start": "0.820",
        "tail_end": "2.300",
        "next_slate_start": "2.700",
    }
    for marker_type, time_s in marker_times.items():
        rows.append(
            {
                "file_id": file_id,
                "unit_id": "T001",
                "sequence": "1",
                "take_id": "TAKE_T001",
                "unit_status": "render_usable",
                "review_status": "accepted",
                "marker_type": marker_type,
                "marker_label_zh": marker_type,
                "time_s": time_s,
                "source": "human_adjusted",
                "confidence": "0.93",
                "nudge_total_ms": "12" if marker_type == "guqin_start" else "0",
                "notes": "已复盘",
                "boundary_type": "next_slate_start",
                "source_raw_audio": "batch01.wav",
                "recording_session_id": "RS_XWC_002_BAIYA_PILOT",
                "recording_id": "RECD_002",
                "piece_id": "XWC",
                "qinist_id": "QINIST_002",
                "batch_id": "batch01",
                "recording_take_no": "001",
                "batch_take_no": "001",
                "script_id": "RS_XWC_002_BAIYA_PILOT_SCRIPT",
                "event_id": "XWC_P01_N01",
                "event_range": "XWC_P01_N01",
                "gesture_id": "SAN_TIAO_6",
                "expected_sample_type": "atomic",
            }
        )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_export_manifest(export_dir: Path) -> None:
    csv_path = export_dir / "raw_marker_review.csv"
    payload = {
        "manifest_version": "varw_export_contract.v0.1",
        "stage": "R0",
        "row_counts": {"raw_marker_review.csv": 5},
        "output_hashes": [{"path": "raw_marker_review.csv", "algorithm": "sha256", "sha256": sha256_path(csv_path)}],
        "fallback_guard": {
            "source_path": "raw_marker_review.csv",
            "source_hash": sha256_path(csv_path),
            "row_count": 5,
            "stage": "R0",
            "reason": "test compatibility restore",
            "restore_mode_required": True,
        },
    }
    (export_dir / "export_manifest.json").write_text(json.dumps(payload), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
