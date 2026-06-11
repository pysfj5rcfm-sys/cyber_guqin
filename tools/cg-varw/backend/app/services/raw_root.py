from __future__ import annotations

import base64
from pathlib import Path

from app.config import ensure_within_root, load_settings


def get_raw_root() -> Path:
    return load_settings().raw_root


def encode_file_id(relative_path: str) -> str:
    raw = relative_path.replace("\\", "/").encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_file_id(file_id: str) -> str:
    padding = "=" * (-len(file_id) % 4)
    return base64.urlsafe_b64decode((file_id + padding).encode("ascii")).decode("utf-8")


def resolve_file_id(file_id: str) -> Path:
    root = get_raw_root()
    relative = decode_file_id(file_id)
    return ensure_within_root(root, root / relative)


def relative_to_raw_root(path: Path) -> str:
    return path.resolve().relative_to(get_raw_root().resolve()).as_posix()
