from __future__ import annotations

import csv
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
from app.services.waveform_service import waveform_peaks_for_path


MARKER_LABELS = {
    "pre_idle_end": "前置空白结束",
    "gesture_start": "前导起势",
    "render_anchor": "渲染锚点",
    "tail_end": "尾音结束",
}
MARKER_ORDER = ("pre_idle_end", "gesture_start", "render_anchor", "tail_end")
R1_SEED_SOURCES = ("manifest", "audio_seed", "fallback_default")
SUPPORTED_AUDIO_SUFFIXES = {".wav", ".wave", ".mp3", ".m4a", ".flac", ".aiff", ".aif"}


def get_split_root() -> Path:
    return load_settings().split_root


def get_split_root_mode() -> str:
    return load_settings().split_root_mode


def list_batches() -> list[SplitBatch]:
    root = get_split_root()
    batch_roots = _discover_batch_roots(root)
    if batch_roots == [root]:
        manifest = _load_manifest(root)
        manifest_batches = manifest.get("batches", []) if manifest else []
        if len(manifest_batches) > 1:
            return [_batch_from_root(root, batch) for batch in manifest_batches if isinstance(batch, dict)]
    return [_batch_from_root(batch_root) for batch_root in batch_roots]


def list_segments(batch_id: str) -> R1SegmentsResponse:
    batch_root = _batch_root_for(batch_id)
    segments = _segments_from_manifest(batch_id, batch_root) or _segments_from_files(batch_id, batch_root)
    return R1SegmentsResponse(batch_id=batch_id, segments=segments)


def get_segment(segment_id: str) -> SplitSegment:
    for batch in list_batches():
        for segment in list_segments(batch.batch_id).segments:
            if segment.segment_id == segment_id:
                return segment
    raise ValueError(f"unknown R1 segment_id: {segment_id}")


def resolve_segment_path(segment_id: str) -> Path:
    segment = get_segment(segment_id)
    batch_root = _batch_root_for(segment.batch_id)
    return ensure_within_root(get_split_root(), batch_root / segment.relative_path)


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
        recording_session_id=segment.recording_session_id,
        recording_id=segment.recording_id,
        piece_id=segment.piece_id,
        qinist_id=segment.qinist_id,
        recording_take_no=segment.recording_take_no,
        batch_take_no=segment.batch_take_no,
        script_id=segment.script_id,
        source_raw_audio=segment.source_raw_audio,
        source_split_audio=segment.source_split_audio or segment.relative_path,
        event_id=segment.event_id,
        event_range=segment.event_range,
        gesture_id=segment.gesture_id,
        realization_variant=segment.realization_variant or segment.variant,
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
    waveform = waveform_peaks_for_path(path, points)
    return R1WaveformResponse(
        segment_id=segment_id,
        duration_s=metadata.duration_s,
        points=waveform.points,
        peaks=waveform.peaks,
        waveform_supported=waveform.waveform_supported,
        fallback_reason=waveform.warning,
    )


def _discover_batch_roots(root: Path) -> list[Path]:
    if not root.exists():
        return []
    if _is_batch_root(root):
        return [root]
    return sorted(path for path in root.iterdir() if path.is_dir() and _is_batch_root(path))


def _is_batch_root(path: Path) -> bool:
    return any(
        candidate.exists()
        for candidate in (
            path / "r1_synthetic_split_manifest.json",
            path / "manifests" / "recd2_split_preview_manifest.csv",
            path / "manifests" / "r1_intake_pointer.yaml",
            path / "clean_previews",
        )
    )


def _batch_root_for(batch_id: str) -> Path:
    root = get_split_root()
    for batch_root in _discover_batch_roots(root):
        if any(batch.batch_id == batch_id for batch in _batches_for_root(batch_root)):
            return batch_root
    raise ValueError(f"unknown R1 batch_id: {batch_id}")


def _batches_for_root(batch_root: Path) -> list[SplitBatch]:
    manifest = _load_manifest(batch_root)
    manifest_batches = manifest.get("batches", []) if manifest else []
    if len(manifest_batches) > 1:
        return [_batch_from_root(batch_root, batch) for batch in manifest_batches if isinstance(batch, dict)]
    return [_batch_from_root(batch_root)]


def _batch_from_root(batch_root: Path, manifest_batch: dict[str, Any] | None = None) -> SplitBatch:
    manifest = _load_manifest(batch_root) or {}
    manifest_batches = [batch for batch in manifest.get("batches", []) if isinstance(batch, dict)]
    manifest_segments = [segment for segment in manifest.get("segments", []) if isinstance(segment, dict)]
    manifest_batch = manifest_batch or (manifest_batches[0] if manifest_batches else {})
    batch_id = str(manifest_batch.get("batch_id") or _batch_id_from_segments(manifest_segments) or batch_root.name)
    clean_preview_count = _clean_preview_count(batch_root)
    segment_count = int(manifest_batch.get("segment_count") or _manifest_segment_count(manifest_segments, batch_id) or clean_preview_count)
    manifest_path = _manifest_path(batch_root)
    return SplitBatch(
        batch_id=batch_id,
        display_name=str(manifest_batch.get("display_name") or batch_id),
        segment_count=segment_count,
        source="real_split_root" if get_split_root_mode() == "real" else "synthetic_demo",
        split_root=str(batch_root),
        manifest_path=str(manifest_path) if manifest_path else "",
        clean_preview_count=clean_preview_count,
        ready_for_r1_review=clean_preview_count > 0 and manifest_path is not None,
    )


def _batch_id_from_segments(segments: list[dict[str, Any]]) -> str:
    for segment in segments:
        batch_id = str(segment.get("batch_id") or "")
        if batch_id:
            return batch_id
    return ""


def _manifest_segment_count(segments: list[dict[str, Any]], batch_id: str) -> int:
    if not segments:
        return 0
    matched = [segment for segment in segments if str(segment.get("batch_id") or batch_id) == batch_id]
    return len(matched)


def _manifest_path(root: Path) -> Path | None:
    for candidate in (
        root / "r1_synthetic_split_manifest.json",
        root / "manifests" / "recd2_split_preview_manifest.csv",
        root / "manifests" / "r1_intake_pointer.yaml",
    ):
        if candidate.exists():
            return candidate
    return None


def _clean_preview_count(root: Path) -> int:
    clean_dir = root / "clean_previews"
    if clean_dir.exists():
        return sum(1 for path in clean_dir.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_SUFFIXES)
    return sum(1 for path in root.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_SUFFIXES)


def _load_manifest(root: Path) -> dict[str, Any] | None:
    path = root / "r1_synthetic_split_manifest.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _segments_from_manifest(batch_id: str, root: Path) -> list[SplitSegment]:
    manifest = _load_manifest(root)
    if not manifest:
        return []
    recd2_rows = _load_recd2_rows(root)
    manifest_scope = {
        "recording_session_id": str(manifest.get("recording_session_id") or ""),
        "piece_id": str(manifest.get("piece_id") or ""),
        "qinist_id": str(manifest.get("qinist_id") or ""),
    }
    return [
        _with_seed_markers(SplitSegment(**_validated_manifest_segment(segment, batch_id, root, manifest_scope)), root, recd2_rows)
        for segment in manifest.get("segments", [])
        if segment.get("batch_id") == batch_id
    ]


def _validated_manifest_segment(segment: dict[str, Any], batch_id: str, root: Path, manifest_scope: dict[str, str]) -> dict[str, Any]:
    segment_id = str(segment.get("segment_id") or "")
    if not segment_id:
        raise ValueError(f"R1 manifest segment in {batch_id}: segment_id is required; file-derived segment_id cannot replace manifest identity")
    if str(segment.get("batch_id") or "") != batch_id:
        raise ValueError(f"R1 manifest segment {segment_id}: batch_id mismatch")
    for field, expected in manifest_scope.items():
        actual = str(segment.get(field) or "")
        if expected and actual and actual != expected:
            raise ValueError(f"R1 manifest segment {segment_id}: {field} mismatch with manifest scope")
    if segment.get("take_id") and not segment.get("recording_take_no"):
        raise ValueError(f"R1 manifest segment {segment_id}: take_id cannot replace recording_take_no")
    relative_path = str(segment.get("relative_path") or "")
    source_split_audio = str(segment.get("source_split_audio") or "")
    if not source_split_audio:
        raise ValueError(f"R1 manifest segment {segment_id}: source_split_audio is required")
    if source_split_audio != relative_path:
        raise ValueError(f"R1 manifest segment {segment_id}: source_split_audio must match manifest relative_path")
    ensure_within_root(root, root / source_split_audio)
    return segment


def _segments_from_files(batch_id: str, root: Path) -> list[SplitSegment]:
    batch_dir = ensure_within_root(get_split_root(), root)
    if not batch_dir.exists() or not batch_dir.is_dir():
        return []

    segments: list[SplitSegment] = []
    audio_paths = sorted((batch_dir / "clean_previews").glob("*.wav")) if (batch_dir / "clean_previews").exists() else sorted(batch_dir.glob("*.wav"))
    for index, path in enumerate(audio_paths, start=1):
        duration_s, sample_rate, bit_depth, channels = wav_metadata(path)
        take_id = path.stem.replace("_clean", "")
        segment_id = f"SPLIT_{batch_id.upper()}_{take_id.upper()}"
        segment = SplitSegment(
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
            markers=_default_markers(segment_id, duration_s),
            synthetic_demo=get_split_root_mode() == "demo",
        )
        segments.append(_with_seed_markers(segment, root, {}))
    return segments


def _default_markers(segment_id: str, duration_s: float) -> dict[str, R1Marker]:
    times = _fallback_marker_values(duration_s)
    return {
        key: R1Marker(
            marker_id=f"{segment_id}:{key}",
            segment_id=segment_id,
            marker_type=key,  # type: ignore[arg-type]
            marker_label_zh=MARKER_LABELS[key],
            time_s=round(time_s, 3),
            source="fallback_default",
            confidence=None,
            notes="R1 seed marker from fallback_default; requires manual review.",
        )
        for key, time_s in times.items()
    }


def _load_recd2_rows(root: Path) -> dict[str, dict[str, str]]:
    path = root / "manifests" / "recd2_split_preview_manifest.csv"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        for key in {row.get("recording_take_no", ""), row.get("batch_take_no", ""), Path(row.get("clean_preview_audio", "")).stem.replace("_clean_preview", "")}:
            if key:
                indexed[key] = row
    return indexed


def _with_seed_markers(segment: SplitSegment, root: Path, recd2_rows: dict[str, dict[str, str]]) -> SplitSegment:
    existing = segment.markers
    if all(getattr(existing, key) is not None for key in MARKER_ORDER):
        return segment

    row = recd2_rows.get(segment.recording_take_no) or recd2_rows.get(segment.take_id) or recd2_rows.get(segment.batch_take_no) or {}
    seed_values = _seed_marker_values(segment, root, row)
    markers = existing.model_copy()
    for key in MARKER_ORDER:
        if getattr(markers, key) is not None:
            continue
        time_s, source = seed_values[key]
        setattr(
            markers,
            key,
            R1Marker(
                marker_id=f"{segment.segment_id}:{key}",
                segment_id=segment.segment_id,
                marker_type=key,  # type: ignore[arg-type]
                marker_label_zh=MARKER_LABELS[key],
                time_s=round(time_s, 3),
                source=source,  # type: ignore[arg-type]
                confidence=_seed_confidence(source),
                review_status="candidate",
                nudge_total_ms=0,
                notes=f"R1 seed marker from {source}; requires manual review.",
            ),
        )
    return segment.model_copy(update={"markers": markers, "segment_status": "candidate", "review_status": "not_started"})


def _seed_marker_values(segment: SplitSegment, root: Path, recd2_row: dict[str, str]) -> dict[str, tuple[float, str]]:
    duration_s = max(0.0, float(segment.duration_s or _float_field(recd2_row, "duration_s") or 0.0))
    candidates = [
        _manifest_marker_values(duration_s, recd2_row),
        _audio_marker_values(root, segment, duration_s),
        {key: (value, "fallback_default") for key, value in _fallback_marker_values(duration_s).items()},
    ]
    values: dict[str, tuple[float, str]] = {}
    for key in MARKER_ORDER:
        for candidate in candidates:
            if key in candidate:
                values[key] = candidate[key]
                break
    return _monotonic_seed_values(values, duration_s)


def _manifest_marker_values(duration_s: float, row: dict[str, str]) -> dict[str, tuple[float, str]]:
    clean_start = _float_field(row, "clean_start_s")
    if clean_start is None:
        return {}

    values: dict[str, tuple[float, str]] = {}
    guqin_start = _local_manifest_time(row, "guqin_start_s", clean_start, duration_s)
    tail_end = _local_manifest_time(row, "tail_end_s", clean_start, duration_s)
    if guqin_start is not None:
        pre_idle_end = max(0.0, guqin_start - min(0.05, duration_s * 0.1))
        values["pre_idle_end"] = (pre_idle_end, "manifest")
        values["gesture_start"] = (guqin_start, "manifest")
        values["render_anchor"] = (guqin_start, "manifest")
    if tail_end is not None:
        values["tail_end"] = (tail_end, "manifest")
    return values


def _audio_marker_values(root: Path, segment: SplitSegment, duration_s: float) -> dict[str, tuple[float, str]]:
    if duration_s <= 0:
        return {}
    path = ensure_within_root(root, root / segment.relative_path)
    if path.suffix.lower() not in {".wav", ".wave"} or not path.exists():
        return {}
    try:
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            sample_width = handle.getsampwidth()
            frame_count = handle.getnframes()
            sample_rate = handle.getframerate()
            frames = handle.readframes(frame_count)
    except wave.Error:
        return {}
    if sample_width not in {1, 2, 3, 4} or frame_count <= 0 or sample_rate <= 0:
        return {}

    frame_peaks: list[float] = []
    max_peak = 0.0
    for frame_index in range(frame_count):
        peak = 0.0
        for channel_index in range(channels):
            offset = (frame_index * channels + channel_index) * sample_width
            peak = max(peak, abs(_sample_value(frames, offset, sample_width)))
        frame_peaks.append(peak)
        max_peak = max(max_peak, peak)
    if max_peak < 0.001:
        return {}

    threshold = max(0.015, max_peak * 0.12)
    active_frames = [index for index, peak in enumerate(frame_peaks) if peak >= threshold]
    if not active_frames:
        return {}
    first_s = active_frames[0] / sample_rate
    last_s = min(duration_s, (active_frames[-1] + 1) / sample_rate)
    pre_idle_end = max(0.0, first_s - min(0.05, duration_s * 0.1))
    return {
        "pre_idle_end": (pre_idle_end, "audio_seed"),
        "gesture_start": (first_s, "audio_seed"),
        "render_anchor": (first_s, "audio_seed"),
        "tail_end": (last_s, "audio_seed"),
    }


def _fallback_marker_values(duration_s: float) -> dict[str, float]:
    duration_s = max(0.0, duration_s)
    return {
        "pre_idle_end": 0.0,
        "gesture_start": min(0.05, duration_s * 0.10),
        "render_anchor": min(0.15, duration_s * 0.20),
        "tail_end": duration_s,
    }


def _monotonic_seed_values(values: dict[str, tuple[float, str]], duration_s: float) -> dict[str, tuple[float, str]]:
    ordered: dict[str, tuple[float, str]] = {}
    previous = 0.0
    for key in MARKER_ORDER:
        time_s, source = values[key]
        clamped = min(duration_s, max(previous, max(0.0, time_s)))
        ordered[key] = (round(clamped, 3), source if source in R1_SEED_SOURCES else "fallback_default")
        previous = clamped
    return ordered


def _local_manifest_time(row: dict[str, str], field: str, clean_start: float, duration_s: float) -> float | None:
    raw_time = _float_field(row, field)
    if raw_time is None:
        return None
    return min(duration_s, max(0.0, raw_time - clean_start))


def _float_field(row: dict[str, str], field: str) -> float | None:
    value = (row.get(field) or "").strip()
    if not value:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def _seed_confidence(source: str) -> float | None:
    if source == "manifest":
        return 0.85
    if source == "audio_seed":
        return 0.55
    return None


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
