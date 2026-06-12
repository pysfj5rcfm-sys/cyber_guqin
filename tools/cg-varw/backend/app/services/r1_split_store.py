from __future__ import annotations

import json
import math
import wave
from pathlib import Path
from typing import Any

from app.config import ensure_within_root, load_settings
from app.schemas import (
    R1Marker,
    R1SegmentMetadata,
    R1SegmentsResponse,
    R1WaveformResponse,
    SplitBatch,
    SplitSegment,
)
from app.services.audio_metadata import wav_metadata


MARKER_LABELS = {
    "pre_idle_end": "前置空白结束",
    "gesture_start": "前导起势",
    "render_anchor": "渲染锚点",
    "tail_end": "尾音结束",
}


def get_split_root() -> Path:
    return load_settings().split_root


def get_split_root_mode() -> str:
    return load_settings().split_root_mode


def list_batches() -> list[SplitBatch]:
    root = get_split_root()
    manifest = _load_manifest(root)
    if manifest:
        return [SplitBatch(**batch) for batch in manifest.get("batches", [])]

    batches: list[SplitBatch] = []
    if root.exists():
        for batch_dir in sorted(path for path in root.iterdir() if path.is_dir()):
            segment_count = len(list(batch_dir.glob("*.wav")))
            if segment_count:
                batches.append(
                    SplitBatch(
                        batch_id=batch_dir.name,
                        display_name=batch_dir.name,
                        segment_count=segment_count,
                        source="real_split_root" if get_split_root_mode() == "real" else "synthetic_demo",
                    )
                )
    return batches


def list_segments(batch_id: str) -> R1SegmentsResponse:
    segments = _segments_from_manifest(batch_id) or _segments_from_files(batch_id)
    return R1SegmentsResponse(batch_id=batch_id, segments=segments)


def get_segment(segment_id: str) -> SplitSegment:
    for batch in list_batches():
        for segment in list_segments(batch.batch_id).segments:
            if segment.segment_id == segment_id:
                return segment
    raise ValueError(f"unknown R1 segment_id: {segment_id}")


def resolve_segment_path(segment_id: str) -> Path:
    segment = get_segment(segment_id)
    return ensure_within_root(get_split_root(), get_split_root() / segment.relative_path)


def segment_metadata(segment_id: str) -> R1SegmentMetadata:
    segment = get_segment(segment_id)
    path = resolve_segment_path(segment_id)
    duration_s = segment.duration_s
    sample_rate = segment.sample_rate
    bit_depth = segment.bit_depth
    channels = segment.channels
    if path.suffix.lower() in {".wav", ".wave"}:
        duration_s, sample_rate, bit_depth, channels = wav_metadata(path)

    return R1SegmentMetadata(
        segment_id=segment.segment_id,
        batch_id=segment.batch_id,
        take_id=segment.take_id,
        file_name=segment.file_name,
        relative_path=segment.relative_path,
        duration_s=duration_s,
        sample_rate=sample_rate,
        bit_depth=bit_depth,
        channels=channels,
        source_format=path.suffix.lower().lstrip("."),
        waveform_supported=path.suffix.lower() in {".wav", ".wave"},
        browser_playback_likely=path.suffix.lower() in {".wav", ".wave", ".mp3", ".m4a", ".flac", ".aiff", ".aif"},
        synthetic_demo=segment.synthetic_demo,
    )


def segment_waveform(segment_id: str, points: int = 1600) -> R1WaveformResponse:
    path = resolve_segment_path(segment_id)
    metadata = segment_metadata(segment_id)
    points = max(1, min(points, 20000))
    if path.suffix.lower() not in {".wav", ".wave"}:
        return R1WaveformResponse(
            segment_id=segment_id,
            duration_s=metadata.duration_s,
            points=points,
            peaks=[],
            waveform_supported=False,
            fallback_reason="Non-WAV waveform extraction is not enabled for R1A.",
        )

    try:
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            sample_width = handle.getsampwidth()
            frame_count = handle.getnframes()
            frames = handle.readframes(frame_count)
    except wave.Error as exc:
        return R1WaveformResponse(
            segment_id=segment_id,
            duration_s=metadata.duration_s,
            points=points,
            peaks=[],
            waveform_supported=False,
            fallback_reason=str(exc),
        )

    if sample_width not in {1, 2, 3, 4}:
        return R1WaveformResponse(
            segment_id=segment_id,
            duration_s=metadata.duration_s,
            points=points,
            peaks=[],
            waveform_supported=False,
            fallback_reason=f"Unsupported WAV sample width: {sample_width}",
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

    return R1WaveformResponse(
        segment_id=segment_id,
        duration_s=metadata.duration_s,
        points=points,
        peaks=peaks[:points],
        waveform_supported=True,
    )


def _load_manifest(root: Path) -> dict[str, Any] | None:
    path = root / "r1_synthetic_split_manifest.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _segments_from_manifest(batch_id: str) -> list[SplitSegment]:
    manifest = _load_manifest(get_split_root())
    if not manifest:
        return []
    return [SplitSegment(**segment) for segment in manifest.get("segments", []) if segment.get("batch_id") == batch_id]


def _segments_from_files(batch_id: str) -> list[SplitSegment]:
    root = get_split_root()
    batch_dir = ensure_within_root(root, root / batch_id)
    if not batch_dir.exists() or not batch_dir.is_dir():
        return []

    segments: list[SplitSegment] = []
    for index, path in enumerate(sorted(batch_dir.glob("*.wav")), start=1):
        duration_s, sample_rate, bit_depth, channels = wav_metadata(path)
        take_id = path.stem.replace("_clean", "")
        segment_id = f"SPLIT_{batch_id.upper()}_{take_id.upper()}"
        markers = _default_markers(segment_id, duration_s)
        segments.append(
            SplitSegment(
                segment_id=segment_id,
                batch_id=batch_id,
                take_id=take_id,
                file_name=path.name,
                relative_path=path.relative_to(root).as_posix(),
                event_id=f"EVENT_{take_id.upper()}",
                event_range=f"{index:03d}",
                duration_s=duration_s,
                sample_rate=sample_rate,
                bit_depth=bit_depth,
                channels=channels,
                markers=markers,
                synthetic_demo=get_split_root_mode() == "demo",
            )
        )
    return segments


def _default_markers(segment_id: str, duration_s: float) -> dict[str, R1Marker]:
    times = {
        "pre_idle_end": 0.2,
        "gesture_start": 0.45,
        "render_anchor": 0.45,
        "tail_end": max(0.7, min(duration_s - 0.08, duration_s * 0.86)),
    }
    return {
        key: R1Marker(
            marker_id=f"{segment_id}:{key}",
            segment_id=segment_id,
            marker_type=key,  # type: ignore[arg-type]
            marker_label_zh=MARKER_LABELS[key],
            time_s=round(time_s, 3),
            source="derived_from_fixture",
            confidence=0.92,
        )
        for key, time_s in times.items()
    }


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
