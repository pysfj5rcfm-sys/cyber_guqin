from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
TOOL_DIR = BACKEND_DIR.parent
DEMO_RAW_ROOT = TOOL_DIR / "sample_workspace" / "raw_audio"
REVIEW_OUTPUT_ROOT = TOOL_DIR / "review_outputs"


@dataclass(frozen=True)
class Settings:
    raw_root: Path
    raw_root_mode: str
    review_only: bool = True
    production_grade: bool = False


def load_settings() -> Settings:
    env_root = os.environ.get("CG_VARW_RAW_ROOT")
    if env_root:
        return Settings(raw_root=Path(env_root).expanduser().resolve(), raw_root_mode="real")

    local_config = BACKEND_DIR / "config.local.json"
    if local_config.exists():
        with local_config.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        configured = data.get("raw_root")
        if configured:
            return Settings(raw_root=Path(configured).expanduser().resolve(), raw_root_mode="real")

    return Settings(raw_root=DEMO_RAW_ROOT.resolve(), raw_root_mode="demo")


def ensure_within_root(root: Path, candidate: Path) -> Path:
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    if resolved_candidate != resolved_root and resolved_root not in resolved_candidate.parents:
        raise ValueError(f"path outside configured raw root: {candidate}")
    return resolved_candidate
