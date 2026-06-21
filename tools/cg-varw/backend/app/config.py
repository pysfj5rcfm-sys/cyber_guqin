from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
TOOL_DIR = BACKEND_DIR.parent
DEMO_RAW_ROOT = TOOL_DIR / "sample_workspace" / "raw_audio"
DEMO_SPLIT_ROOT = TOOL_DIR / "sample_workspace" / "split_audio"
REVIEW_OUTPUT_ROOT = TOOL_DIR / "review_outputs"


@dataclass(frozen=True)
class Settings:
    raw_root: Path
    raw_root_mode: str
    raw_include_prefix: str | None
    split_root: Path
    split_root_mode: str
    review_only: bool = True
    production_grade: bool = False


def load_settings() -> Settings:
    split_root, split_root_mode = _load_split_root()
    env_root = os.environ.get("CG_VARW_RAW_ROOT")
    if env_root:
        return Settings(
            raw_root=Path(env_root).expanduser().resolve(),
            raw_root_mode="real",
            raw_include_prefix=_load_raw_include_prefix(),
            split_root=split_root,
            split_root_mode=split_root_mode,
        )

    local_config = BACKEND_DIR / "config.local.json"
    if local_config.exists():
        with local_config.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        configured = data.get("raw_root")
        if configured:
            return Settings(
                raw_root=Path(configured).expanduser().resolve(),
                raw_root_mode="real",
                raw_include_prefix=_load_raw_include_prefix(data),
                split_root=split_root,
                split_root_mode=split_root_mode,
            )

    return Settings(
        raw_root=DEMO_RAW_ROOT.resolve(),
        raw_root_mode="demo",
        raw_include_prefix=_load_raw_include_prefix(),
        split_root=split_root,
        split_root_mode=split_root_mode,
    )


def _load_split_root() -> tuple[Path, str]:
    env_root = os.environ.get("CG_VARW_SPLIT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve(), "real"

    local_config = BACKEND_DIR / "config.local.json"
    if local_config.exists():
        with local_config.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        configured = data.get("split_root")
        if configured:
            return Path(configured).expanduser().resolve(), "real"

    return DEMO_SPLIT_ROOT.resolve(), "demo"


def _load_raw_include_prefix(config_data: dict[str, object] | None = None) -> str | None:
    raw_value = os.environ.get("CG_VARW_RAW_INCLUDE_PREFIX")
    if raw_value is None and config_data:
        configured = config_data.get("raw_include_prefix")
        raw_value = configured if isinstance(configured, str) else None
    return normalize_raw_include_prefix(raw_value)


def normalize_raw_include_prefix(raw_value: str | None) -> str | None:
    value = (raw_value or "").strip().replace("\\", "/")
    if not value:
        return None
    if value.startswith("/"):
        return None
    parts = [part for part in value.split("/") if part]
    if not parts or any(part == ".." for part in parts):
        return None
    return "/".join(parts)


def ensure_within_root(root: Path, candidate: Path) -> Path:
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    if resolved_candidate != resolved_root and resolved_root not in resolved_candidate.parents:
        raise ValueError(f"path outside configured raw root: {candidate}")
    return resolved_candidate
