from __future__ import annotations

import math
import wave
from pathlib import Path

from app.schemas import WaveformResponse


def waveform_for_file(file_id: str, path: Path, points: int = 1600) -> WaveformResponse:
    points = max(1, min(points, 20000))
    if path.suffix.lower() not in {".wav", ".wave"}:
        return WaveformResponse(
            file_id=file_id,
            waveform_supported=False,
            points=points,
            peaks=[],
            warning="Non-WAV waveform extraction may require ffmpeg or another decoder.",
        )

    try:
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            sample_width = handle.getsampwidth()
            frame_count = handle.getnframes()
            frames = handle.readframes(frame_count)
    except wave.Error as exc:
        return WaveformResponse(file_id=file_id, waveform_supported=False, points=points, peaks=[], warning=str(exc))

    if sample_width not in {1, 2, 3, 4}:
        return WaveformResponse(
            file_id=file_id,
            waveform_supported=False,
            points=points,
            peaks=[],
            warning=f"Unsupported WAV sample width: {sample_width}",
        )

    bucket_size = max(1, math.ceil(frame_count / points))
    peaks: list[float] = []

    for bucket_start in range(0, frame_count, bucket_size):
        bucket_end = min(frame_count, bucket_start + bucket_size)
        peak = 0.0
        for frame_index in range(bucket_start, bucket_end):
            for channel_index in range(channels):
                offset = (frame_index * channels + channel_index) * sample_width
                peak = max(peak, abs(_sample_value(frames, offset, sample_width)))
        peaks.append(round(min(1.0, peak), 6))

    while len(peaks) < points:
        peaks.append(0.0)

    return WaveformResponse(file_id=file_id, waveform_supported=True, points=points, peaks=peaks[:points])


def _sample_value(data: bytes, offset: int, sample_width: int) -> float:
    if sample_width == 1:
        return (data[offset] - 128) / 128
    if sample_width == 2:
        return int.from_bytes(data[offset : offset + 2], "little", signed=True) / 32768
    if sample_width == 3:
        raw = int.from_bytes(data[offset : offset + 3], "little", signed=False)
        if raw & 0x800000:
            raw -= 0x1000000
        return raw / 8388608
    return int.from_bytes(data[offset : offset + 4], "little", signed=True) / 2147483648
