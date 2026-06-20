from __future__ import annotations

import csv
import json
import os
import tempfile
import unittest
import wave
from pathlib import Path

from app.services import r1_split_store


class R1MarkerSeedTests(unittest.TestCase):
    def test_parent_split_root_discovers_child_batches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            parent = Path(tmp_dir)
            _write_batch(parent / "batch02", "batch02", [{"take": "T011", "duration_s": 0.5}, {"take": "T012", "duration_s": 0.6}])
            _write_batch(parent / "batch08", "batch08", [{"take": "T071", "duration_s": 0.4}])

            with _split_root_env(parent):
                batches = r1_split_store.list_batches()
                batch_ids = [batch.batch_id for batch in batches]
                batch08 = next(batch for batch in batches if batch.batch_id == "batch08")
                batch08_segments = r1_split_store.list_segments("batch08").segments

        self.assertEqual(batch_ids, ["batch02", "batch08"])
        self.assertEqual(batch08.segment_count, 1)
        self.assertEqual(batch08.clean_preview_count, 1)
        self.assertTrue(batch08.ready_for_r1_review)
        self.assertTrue(batch08.split_root.endswith("/batch08"))
        self.assertTrue(batch08.manifest_path.endswith("/batch08/r1_synthetic_split_manifest.json"))
        self.assertEqual([segment.take_id for segment in batch08_segments], ["T071"])
        self.assertEqual(batch08_segments[0].relative_path, "clean_previews/T071_clean_preview.wav")

    def test_single_batch_split_root_remains_compatible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            _write_batch(root, "batch03", [{"take": "T021", "duration_s": 0.5}])

            with _split_root_env(root):
                batches = r1_split_store.list_batches()
                segments = r1_split_store.list_segments("batch03").segments

        self.assertEqual([batch.batch_id for batch in batches], ["batch03"])
        self.assertEqual(batches[0].split_root, str(root.resolve()))
        self.assertEqual(segments[0].take_id, "T021")

    def test_manifest_values_seed_missing_markers_as_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            _write_wav(root / "clean_previews" / "T001_clean_preview.wav", duration_s=1.5, tone_start_s=0.2, tone_end_s=1.0)
            _write_manifest(
                root,
                [
                    {
                        "recording_take_no": "T001",
                        "clean_start_s": "10.000",
                        "duration_s": "1.500",
                        "guqin_start_s": "10.400",
                        "tail_end_s": "11.200",
                    }
                ],
            )
            _write_r1_manifest(root, [{"take": "T001", "duration_s": 1.5}])

            with _split_root_env(root):
                segment = r1_split_store.list_segments("batch01").segments[0]

        self.assertEqual(segment.markers.gesture_start.time_s, 0.4)
        self.assertEqual(segment.markers.render_anchor.time_s, 0.4)
        self.assertEqual(segment.markers.tail_end.time_s, 1.2)
        self.assertEqual(segment.markers.gesture_start.source, "manifest")
        self.assertEqual(segment.markers.render_anchor.source, "manifest")
        self.assertEqual(segment.markers.tail_end.source, "manifest")
        self.assertTrue(all(marker.review_status == "candidate" for marker in _markers(segment)))
        self.assertNotEqual(segment.segment_status, "render_usable")

    def test_audio_seed_is_used_when_manifest_markers_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            _write_wav(root / "clean_previews" / "T002_clean_preview.wav", duration_s=1.0, tone_start_s=0.3, tone_end_s=0.7)
            _write_manifest(
                root,
                [
                    {
                        "recording_take_no": "T002",
                        "clean_start_s": "20.000",
                        "duration_s": "1.000",
                        "guqin_start_s": "",
                        "tail_end_s": "",
                    }
                ],
            )
            _write_r1_manifest(root, [{"take": "T002", "duration_s": 1.0}])

            with _split_root_env(root):
                segment = r1_split_store.list_segments("batch01").segments[0]

        self.assertEqual(segment.markers.gesture_start.source, "audio_seed")
        self.assertEqual(segment.markers.render_anchor.source, "audio_seed")
        self.assertEqual(segment.markers.tail_end.source, "audio_seed")
        self.assertGreaterEqual(segment.markers.gesture_start.time_s, 0.25)
        self.assertLessEqual(segment.markers.gesture_start.time_s, 0.35)
        self.assertGreaterEqual(segment.markers.tail_end.time_s, 0.65)
        self.assertLessEqual(segment.markers.tail_end.time_s, 0.75)
        self.assertTrue(all(marker.review_status == "candidate" for marker in _markers(segment)))

    def test_fallback_default_is_used_when_manifest_and_audio_seed_are_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            _write_wav(root / "clean_previews" / "T003_clean_preview.wav", duration_s=0.3, tone_start_s=None, tone_end_s=None)
            _write_manifest(
                root,
                [
                    {
                        "recording_take_no": "T003",
                        "clean_start_s": "30.000",
                        "duration_s": "0.300",
                        "guqin_start_s": "",
                        "tail_end_s": "",
                    }
                ],
            )
            _write_r1_manifest(root, [{"take": "T003", "duration_s": 0.3}])

            with _split_root_env(root):
                segment = r1_split_store.list_segments("batch01").segments[0]

        times = [
            segment.markers.pre_idle_end.time_s,
            segment.markers.gesture_start.time_s,
            segment.markers.render_anchor.time_s,
            segment.markers.tail_end.time_s,
        ]
        self.assertEqual([marker.source for marker in _markers(segment)], ["fallback_default"] * 4)
        self.assertEqual(times, sorted(times))
        self.assertLessEqual(times[-1], 0.3)
        self.assertTrue(all(marker.review_status == "candidate" for marker in _markers(segment)))


def _split_root_env(root: Path):
    class SplitRootEnv:
        def __enter__(self):
            self.previous = os.environ.get("CG_VARW_SPLIT_ROOT")
            os.environ["CG_VARW_SPLIT_ROOT"] = str(root)

        def __exit__(self, exc_type, exc, tb):
            if self.previous is None:
                os.environ.pop("CG_VARW_SPLIT_ROOT", None)
            else:
                os.environ["CG_VARW_SPLIT_ROOT"] = self.previous

    return SplitRootEnv()


def _markers(segment):
    return [
        segment.markers.pre_idle_end,
        segment.markers.gesture_start,
        segment.markers.render_anchor,
        segment.markers.tail_end,
    ]


def _write_r1_manifest(root: Path, segments: list[dict[str, object]]) -> None:
    payload = {
        "batches": [{"batch_id": "batch01", "display_name": "batch01", "segment_count": len(segments), "source": "real_split_root"}],
        "segments": [
            {
                "segment_id": f"RECD2_BATCH01_{segment['take']}",
                "batch_id": "batch01",
                "take_id": segment["take"],
                "file_name": f"{segment['take']}_clean_preview.wav",
                "relative_path": f"clean_previews/{segment['take']}_clean_preview.wav",
                "recording_take_no": segment["take"],
                "source_split_audio": f"clean_previews/{segment['take']}_clean_preview.wav",
                "duration_s": segment["duration_s"],
                "markers": {"pre_idle_end": None, "gesture_start": None, "render_anchor": None, "tail_end": None},
                "segment_status": "candidate",
                "review_status": "not_started",
                "synthetic_demo": False,
            }
            for segment in segments
        ],
    }
    (root / "r1_synthetic_split_manifest.json").write_text(json.dumps(payload), encoding="utf-8")


def _write_batch(root: Path, batch_id: str, segments: list[dict[str, object]]) -> None:
    for segment in segments:
        _write_wav(
            root / "clean_previews" / f"{segment['take']}_clean_preview.wav",
            duration_s=float(segment["duration_s"]),
            tone_start_s=0.1,
            tone_end_s=max(0.1, float(segment["duration_s"]) - 0.1),
        )
    _write_manifest(
        root,
        [
            {
                "recording_take_no": str(segment["take"]),
                "clean_start_s": "0.000",
                "duration_s": str(segment["duration_s"]),
                "guqin_start_s": "",
                "tail_end_s": "",
            }
            for segment in segments
        ],
    )
    (root / "manifests" / "r1_intake_pointer.yaml").write_text("ready_for_r1_review: true\n", encoding="utf-8")
    _write_r1_manifest_for_batch(root, batch_id, segments)


def _write_r1_manifest_for_batch(root: Path, batch_id: str, segments: list[dict[str, object]]) -> None:
    payload = {
        "batches": [{"batch_id": batch_id, "display_name": batch_id, "segment_count": len(segments), "source": "real_split_root"}],
        "segments": [
            {
                "segment_id": f"RECD2_{batch_id.upper()}_{segment['take']}",
                "batch_id": batch_id,
                "take_id": segment["take"],
                "file_name": f"{segment['take']}_clean_preview.wav",
                "relative_path": f"clean_previews/{segment['take']}_clean_preview.wav",
                "recording_take_no": segment["take"],
                "source_split_audio": f"clean_previews/{segment['take']}_clean_preview.wav",
                "duration_s": segment["duration_s"],
                "markers": {"pre_idle_end": None, "gesture_start": None, "render_anchor": None, "tail_end": None},
                "segment_status": "candidate",
                "review_status": "not_started",
                "synthetic_demo": False,
            }
            for segment in segments
        ],
    }
    (root / "r1_synthetic_split_manifest.json").write_text(json.dumps(payload), encoding="utf-8")


def _write_manifest(root: Path, rows: list[dict[str, str]]) -> None:
    manifest_dir = root / "manifests"
    manifest_dir.mkdir(parents=True)
    path = manifest_dir / "recd2_split_preview_manifest.csv"
    fieldnames = ["recording_take_no", "clean_start_s", "duration_s", "guqin_start_s", "tail_end_s"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_wav(path: Path, duration_s: float, tone_start_s: float | None, tone_end_s: float | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sample_rate = 1000
    frame_count = int(duration_s * sample_rate)
    frames = bytearray()
    for index in range(frame_count):
        time_s = index / sample_rate
        active = tone_start_s is not None and tone_end_s is not None and tone_start_s <= time_s <= tone_end_s
        sample = 12000 if active else 0
        frames.extend(sample.to_bytes(2, "little", signed=True))
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(bytes(frames))


if __name__ == "__main__":
    unittest.main()
