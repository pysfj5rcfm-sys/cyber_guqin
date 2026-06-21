import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.services import review_unit_builder
from app.services.raw_file_scanner import scan_raw_files
from app.services.raw_root import encode_file_id


class R0RawFileScopeFilterTests(unittest.TestCase):
    def test_raw_files_listing_is_unchanged_without_include_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baiya = root / "QINIST_002" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "raw"
            other = root / "QINIST_999" / "XWC" / "OTHER_SESSION" / "raw"
            _write_wav(baiya / "RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav")
            _write_wav(other / "OTHER_SESSION_batch01.wav")

            with patch.dict(os.environ, {"CG_VARW_RAW_ROOT": str(root)}, clear=False):
                os.environ.pop("CG_VARW_RAW_INCLUDE_PREFIX", None)
                response = scan_raw_files()

        self.assertEqual(2, len(response.files))
        self.assertEqual(
            [
                "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav",
                "QINIST_999/XWC/OTHER_SESSION/raw/OTHER_SESSION_batch01.wav",
            ],
            [item.relative_path for item in response.files],
        )

    def test_include_prefix_filters_listing_but_keeps_wide_root_file_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prefix = "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw"
            baiya = root / prefix
            other_session = root / "QINIST_999" / "XWC" / "OTHER_SESSION" / "raw"
            preview = root / "QINIST_002" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "split_preview" / "batch01"
            _write_wav(baiya / "RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav")
            _write_wav(baiya / "RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav")
            _write_wav(other_session / "OTHER_SESSION_batch01.wav")
            _write_wav(preview / "T001_clean_preview.wav")

            with patch.dict(
                os.environ,
                {"CG_VARW_RAW_ROOT": str(root), "CG_VARW_RAW_INCLUDE_PREFIX": prefix},
                clear=False,
            ):
                response = scan_raw_files()

        relative_paths = [item.relative_path for item in response.files]
        self.assertEqual(
            [
                "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav",
                "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav",
            ],
            relative_paths,
        )
        self.assertEqual([encode_file_id(path) for path in relative_paths], [item.file_id for item in response.files])

    def test_include_prefix_without_trailing_slash_matches_children_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prefix = "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw"
            _write_wav(root / prefix / "batch01.wav")
            _write_wav(root / "QINIST_002" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "raw_extra" / "wrong.wav")

            with patch.dict(
                os.environ,
                {"CG_VARW_RAW_ROOT": str(root), "CG_VARW_RAW_INCLUDE_PREFIX": prefix},
                clear=False,
            ):
                response = scan_raw_files()

        self.assertEqual([f"{prefix}/batch01.wav"], [item.relative_path for item in response.files])

    def test_dangerous_include_prefixes_are_ignored(self) -> None:
        for bad_prefix in ["/tmp/raw", "../outside", "QINIST_002/../OTHER"]:
            with self.subTest(bad_prefix=bad_prefix), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                _write_wav(root / "QINIST_002" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "raw" / "batch01.wav")
                _write_wav(root / "QINIST_999" / "XWC" / "OTHER_SESSION" / "raw" / "other.wav")

                with patch.dict(
                    os.environ,
                    {"CG_VARW_RAW_ROOT": str(root), "CG_VARW_RAW_INCLUDE_PREFIX": bad_prefix},
                    clear=False,
                ):
                    response = scan_raw_files()

            self.assertEqual(2, len(response.files))

    def test_review_units_loader_still_uses_wide_root_file_id_with_include_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_relative = "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav"
            raw_path = root / raw_relative
            _write_wav(raw_path)
            file_id = encode_file_id(raw_relative)
            review_root = root / "review_outputs"
            draft_path = review_root / "r0" / "drafts" / f"{file_id}.raw_marker_review.json"
            draft_path.parent.mkdir(parents=True)
            draft_path.write_text(
                json.dumps({"file_id": file_id, "source": "saved_draft", "units": [{"id": "T001"}]}),
                encoding="utf-8",
            )

            with patch.dict(
                os.environ,
                {
                    "CG_VARW_RAW_ROOT": str(root),
                    "CG_VARW_RAW_INCLUDE_PREFIX": "QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw",
                },
                clear=False,
            ), patch.object(review_unit_builder, "REVIEW_OUTPUT_ROOT", review_root):
                listed = scan_raw_files()
                loaded = review_unit_builder.load_or_build_review_units(listed.files[0].file_id, raw_path)

        self.assertEqual(file_id, listed.files[0].file_id)
        self.assertEqual("saved_draft", loaded["source"])
        self.assertEqual("T001", loaded["units"][0]["id"])


def _write_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"RIFF\x24\x00\x00\x00WAVEfmt ")


if __name__ == "__main__":
    unittest.main()
