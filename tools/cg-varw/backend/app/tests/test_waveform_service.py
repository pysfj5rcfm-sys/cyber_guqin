from __future__ import annotations

import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

from app.services import waveform_service


class WaveformServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        waveform_service.clear_waveform_cache()

    def test_waveform_for_file_uses_cache_for_same_file_stat_and_points(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "tone.wav"
            _write_wav(path, frame_count=100, peak_every=10)

            first = waveform_service.waveform_for_file("FILE_1", path, points=20)
            with mock.patch("wave.open", side_effect=AssertionError("cache miss")):
                second = waveform_service.waveform_for_file("FILE_1", path, points=20)

        self.assertTrue(first.waveform_supported)
        self.assertEqual(len(first.peaks), 20)
        self.assertEqual(second.peaks, first.peaks)

    def test_shared_waveform_result_supports_r1_segment_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "segment.wav"
            _write_wav(path, frame_count=40, peak_every=4)

            result = waveform_service.waveform_peaks_for_path(path, points=10)

        self.assertTrue(result.waveform_supported)
        self.assertEqual(result.points, 10)
        self.assertEqual(len(result.peaks), 10)
        self.assertIsNone(result.warning)


def _write_wav(path: Path, frame_count: int, peak_every: int) -> None:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(1000)
        frames = bytearray()
        for index in range(frame_count):
            sample = 16000 if index % peak_every == 0 else 0
            frames.extend(sample.to_bytes(2, "little", signed=True))
        handle.writeframes(bytes(frames))


if __name__ == "__main__":
    unittest.main()
