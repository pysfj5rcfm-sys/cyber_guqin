from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from app.config import load_settings
from app.schemas import RawFileItem, RawFilesResponse
from app.services.raw_root import encode_file_id


SUPPORTED_AUDIO_SUFFIXES = {".wav", ".wave", ".m4a", ".mp3", ".flac", ".aiff", ".aif"}


def scan_raw_files() -> RawFilesResponse:
    settings = load_settings()
    files: list[RawFileItem] = []
    if settings.raw_root.exists():
        for path in sorted(settings.raw_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_AUDIO_SUFFIXES:
                continue
            relative = path.relative_to(settings.raw_root).as_posix()
            stat = path.stat()
            files.append(
                RawFileItem(
                    file_id=encode_file_id(relative),
                    name=path.name,
                    relative_path=relative,
                    size_bytes=stat.st_size,
                    modified_time=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                    source_format=path.suffix.lower().lstrip("."),
                )
            )
    return RawFilesResponse(raw_root=str(settings.raw_root), raw_root_mode=settings.raw_root_mode, files=files)
