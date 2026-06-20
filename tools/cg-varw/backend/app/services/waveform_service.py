from __future__ import annotations

import math
import wave
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

from app.schemas import WaveformResponse


MAX_POINTS = 20000
MAX_CACHE_ENTRIES = 128


@dataclass(frozen=True)
class WaveformPeaks:
    waveform_supported: bool
    points: int
    peaks: list[float]
    warning: str | None = None


_WaveformCacheKey = tuple[str, int, int, int]
_waveform_cache: OrderedDict[_WaveformCacheKey, WaveformPeaks] = OrderedDict()


def waveform_for_file(file_id: str, path: Path, points: int = 1600) -> WaveformResponse:
    result = waveform_peaks_for_path(path, points)
    return WaveformResponse(
        file_id=file_id,
        waveform_supported=result.waveform_supported,
        points=result.points,
        peaks=result.peaks,
        warning=result.warning,
    )


def waveform_peaks_for_path(path: Path, points: int = 1600) -> WaveformPeaks:
    points = max(1, min(points, MAX_POINTS))
    cache_key = _cache_key(path, points)
    cached = _waveform_cache.get(cache_key)
    if cached is not None:
        _waveform_cache.move_to_end(cache_key)
        return cached

    result = _build_waveform_peaks(path, points)
    _waveform_cache[cache_key] = result
    _waveform_cache.move_to_end(cache_key)
    while len(_waveform_cache) > MAX_CACHE_ENTRIES:
        _waveform_cache.popitem(last=False)
    return result


def clear_waveform_cache() -> None:
    _waveform_cache.clear()


def _cache_key(path: Path, points: int) -> _WaveformCacheKey:
    stat = path.stat()
    return (str(path.resolve()), stat.st_mtime_ns, stat.st_size, points)


def _build_waveform_peaks(path: Path, points: int) -> WaveformPeaks:
    if path.suffix.lower() not in {".wav", ".wave"}:
        return WaveformPeaks(
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
        return WaveformPeaks(waveform_supported=False, points=points, peaks=[], warning=str(exc))

    if sample_width not in {1, 2, 3, 4}:
        return WaveformPeaks(
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

    return WaveformPeaks(waveform_supported=True, points=points, peaks=peaks[:points])


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
