from __future__ import annotations

import wave
from datetime import datetime, timezone
from pathlib import Path

from app.schemas import MetadataResponse
from app.services.raw_root import relative_to_raw_root


BROWSER_PLAYBACK_SUFFIXES = {".wav", ".wave", ".mp3", ".m4a", ".flac", ".aiff", ".aif"}


def wav_metadata(path: Path) -> tuple[float, int, int, int]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_rate = handle.getframerate()
        frames = handle.getnframes()
        bit_depth = handle.getsampwidth() * 8
    return frames / sample_rate, sample_rate, bit_depth, channels


def metadata_for_file(file_id: str, path: Path) -> MetadataResponse:
    suffix = path.suffix.lower()
    stat = path.stat()
    warning = None
    duration_s: float | None = None
    sample_rate: int | None = None
    bit_depth: int | None = None
    channels: int | None = None
    waveform_supported = suffix in {".wav", ".wave"}

    if waveform_supported:
        try:
            duration_s, sample_rate, bit_depth, channels = wav_metadata(path)
        except wave.Error as exc:
            waveform_supported = False
            warning = f"WAV metadata parse failed: {exc}"
    else:
        warning = "Non-WAV waveform extraction may require ffmpeg or another decoder."

    return MetadataResponse(
        file_id=file_id,
        source_audio=relative_to_raw_root(path),
        duration_s=duration_s,
        sample_rate=sample_rate,
        bit_depth=bit_depth,
        channels=channels,
        source_format=suffix.lstrip("."),
        size_bytes=stat.st_size,
        modified_time=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        waveform_supported=waveform_supported,
        browser_playback_likely=suffix in BROWSER_PLAYBACK_SUFFIXES,
        warning=warning,
    )
