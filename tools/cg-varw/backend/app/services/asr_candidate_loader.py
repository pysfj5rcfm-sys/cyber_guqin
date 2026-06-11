from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def load_asr_candidates(raw_path: Path) -> dict[str, Any]:
    for path in candidate_paths(raw_path):
        if path.exists() and path.is_file():
            if path.suffix.lower() == ".json":
                with path.open("r", encoding="utf-8-sig") as handle:
                    data = json.load(handle)
                candidates = data.get("candidates", data if isinstance(data, list) else [])
                return {
                    "found": True,
                    "source": path.name,
                    "message": "",
                    "candidates": candidates,
                    "review_only": True,
                    "production_grade": False,
                }
            if path.suffix.lower() == ".csv":
                with path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                return {
                    "found": True,
                    "source": path.name,
                    "message": "",
                    "candidates": rows,
                    "review_only": True,
                    "production_grade": False,
                }

    return {
        "found": False,
        "source": None,
        "message": "未找到 ASR 候选，可手动新增 T",
        "candidates": [],
        "review_only": True,
        "production_grade": False,
    }


def candidate_paths(raw_path: Path) -> list[Path]:
    stem = raw_path.stem
    parent = raw_path.parent
    return [
        parent / f"{stem}.asr_candidates.json",
        parent / f"{stem}.slate_anchor_candidates.csv",
        parent / "slate_anchor_manifest.csv",
        parent / "asr_candidates.json",
    ]
