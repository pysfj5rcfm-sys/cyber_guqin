#!/usr/bin/env python3
"""Runtime component visual index for the P2 visual component layer."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.build_component_visual_index import build_component_visual_index
from scripts.component_matcher import ComponentImageIndex


DEFAULT_REGISTRY = REPO_ROOT / "references" / "qxby_component_atlas" / "component_registry.reindexed.v0.2.json"
DEFAULT_OUTPUT = REPO_ROOT / "references" / "qxby_component_atlas" / "component_visual_runtime_index.v0.1.json"


AUTHORITY_FLAGS = {
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_CANON_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
}


class ComponentVisualIndex(ComponentImageIndex):
    """Loader for the runtime index shape used by ComponentMatcher."""

    @classmethod
    def from_file(cls, path: Path | str, *, repo_root: Path | str | None = None) -> "ComponentVisualIndex":
        index_path = Path(path)
        data = _load_json(index_path)
        root = Path(repo_root) if repo_root is not None else REPO_ROOT
        return cls(data, repo_root=root)

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, repo_root: Path | str = REPO_ROOT) -> "ComponentVisualIndex":
        return cls(data, repo_root=repo_root)


def build_component_visual_runtime_index(
    registry_path: Path | str = DEFAULT_REGISTRY,
    *,
    repo_root: Path | str = REPO_ROOT,
    output_path: Path | str | None = None,
) -> dict[str, Any]:
    """Build an oracle-free runtime visual index from the component registry."""

    root = Path(repo_root)
    base = build_component_visual_index(registry_path, repo_root=root)
    components = [_runtime_entry(item) for item in base.get("components", [])]
    components.sort(key=lambda item: item["component_id"])

    index = {
        "index_id": "CG_LXY_P2_component_visual_runtime_index.v0.1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_index_id": base.get("index_id"),
        "registry_path": base.get("registry_path"),
        "component_index_count": len(components),
        "image_reference_count": sum(1 for item in components if item["normalized_reference"].get("matchable")),
        "source_image_missing_count": sum(1 for item in components if not item["normalized_reference"].get("matchable")),
        "missing_component_ids": [
            item["component_id"] for item in components if not item["normalized_reference"].get("matchable")
        ],
        "components": components,
        "authority_flags": dict(AUTHORITY_FLAGS),
        "runtime_boundary": {
            "input": "single crop image",
            "output": ["ComponentCandidateSet", "VisualCandidateLattice"],
            "does_not_output": ["phrase", "sentence", "score event", "Dapu IR"],
            "oracle_free": True,
            "goldset_dependency": False,
            "lxy_special_case_dependency": False,
        },
        "readiness": {
            "ready_for_P3_visual_grammar_fusion": True,
            "ready_for_LXY_phrase_reading": False,
            "ready_for_training_model": False,
        },
    }

    if output_path is not None:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return index


def _runtime_entry(entry: dict[str, Any]) -> dict[str, Any]:
    normalized_reference = dict(entry.get("normalized_reference") or {})
    reference_path = entry.get("image_path")
    matchable = bool(normalized_reference.get("matchable"))
    return {
        "component_id": str(entry.get("component_id")),
        "label": entry.get("label") or "",
        "category": entry.get("category") or "",
        "reference_path": reference_path,
        "image_path": reference_path,
        "image_hash": entry.get("image_hash"),
        "image_dimensions": entry.get("image_dimensions"),
        "normalized_image_metadata": {
            "has_reference_image": bool(reference_path and matchable),
            "matchable": matchable,
            "reference_type": normalized_reference.get("reference_type"),
            "source_registry": normalized_reference.get("source_registry"),
            "image_hash_matches_registry": normalized_reference.get("image_hash_matches_registry"),
        },
        "normalized_reference": normalized_reference,
    }


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build P2 runtime component visual index.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    index = build_component_visual_runtime_index(args.registry, repo_root=args.repo_root, output_path=args.output)
    summary = {
        "component_index_count": index["component_index_count"],
        "image_reference_count": index["image_reference_count"],
        "source_image_missing_count": index["source_image_missing_count"],
        "output": args.output,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
