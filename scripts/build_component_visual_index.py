#!/usr/bin/env python3
"""Build the P2-B component visual index from the registry and source images."""

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

from scripts.component_matcher import read_png_dimensions, sha256_file

DEFAULT_REGISTRY = REPO_ROOT / "references" / "qxby_component_atlas" / "component_registry.reindexed.v0.2.json"
DEFAULT_OUTPUT = REPO_ROOT / "references" / "qxby_component_atlas" / "component_visual_index.v0.1.json"


def build_component_visual_index(
    registry_path: Path | str = DEFAULT_REGISTRY,
    *,
    repo_root: Path | str = REPO_ROOT,
    output_path: Path | str | None = None,
) -> dict[str, Any]:
    root = Path(repo_root)
    registry_file = Path(registry_path)
    registry = _load_json(registry_file)
    entries = []
    missing_images = []

    for component in registry.get("components", []):
        entry = _entry_from_component(component, root, source_registry="components")
        if entry["normalized_reference"]["matchable"] is False:
            missing_images.append(component.get("component_id"))
        entries.append(entry)

    for component in registry.get("auxiliary_components", []):
        entries.append(_entry_from_component(component, root, source_registry="auxiliary_components"))

    entries.sort(key=lambda item: item["component_id"])
    image_reference_count = sum(1 for item in entries if item["normalized_reference"]["matchable"])
    index = {
        "index_id": "CG_LXY_P2B_component_visual_index.v0.1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_path": _relative_or_string(registry_file, root),
        "component_index_count": len(entries),
        "image_reference_count": image_reference_count,
        "source_image_missing_count": len(missing_images),
        "missing_component_ids": missing_images,
        "components": entries,
        "authority_flags": {
            "NOT_SCORE_AUTHORITY": True,
            "NOT_DAPU_IR_AUTHORITY": True,
            "NOT_CANON_AUTHORITY": True,
            "NOT_SCORE_EVENT_AUTHORITY": True,
            "NOT_SAMPLE_INGEST": True,
            "NOT_ML_TRAINING_DATA": True,
        },
        "readiness": {
            "ready_for_P2C_visual_lattice_design": True,
            "ready_for_LXY_phrase_reading": False,
            "ready_for_training_model": False,
        },
    }

    if output_path is not None:
        out = Path(output_path)
        out.write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return index


def _entry_from_component(component: dict[str, Any], repo_root: Path, *, source_registry: str) -> dict[str, Any]:
    image_path = component.get("source_image_path_v0_1")
    image_hash = None
    image_dimensions = None
    matchable = False
    reason = "NO_REPO_SOURCE_IMAGE"
    hash_matches_registry = None

    if image_path:
        absolute_image_path = Path(image_path)
        if not absolute_image_path.is_absolute():
            absolute_image_path = repo_root / absolute_image_path
        if absolute_image_path.is_file():
            image_hash = sha256_file(absolute_image_path)
            image_dimensions = read_png_dimensions(absolute_image_path)
            matchable = True
            reason = "REGISTRY_SOURCE_IMAGE_AVAILABLE"
            registry_hash = component.get("image_sha256")
            hash_matches_registry = None if not registry_hash else registry_hash == image_hash
        else:
            reason = "MISSING_REPO_SOURCE_IMAGE"
    elif source_registry == "auxiliary_components":
        ref = component.get("reference_evidence") or {}
        image_hash = ref.get("image_sha256")

    return {
        "component_id": component.get("component_id"),
        "label": component.get("label_zh") or component.get("label") or "",
        "category": component.get("component_family") or component.get("category") or component.get("source_category") or "",
        "image_path": image_path,
        "image_hash": image_hash,
        "image_dimensions": image_dimensions,
        "normalized_reference": {
            "reference_type": "registry_component_image" if source_registry == "components" else "registry_auxiliary_reference",
            "source_registry": source_registry,
            "matchable": matchable,
            "reason": reason,
            "registry_image_hash": component.get("image_sha256"),
            "image_hash_matches_registry": hash_matches_registry,
        },
    }


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def _relative_or_string(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build component_visual_index from registry source image references.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    index = build_component_visual_index(args.registry, repo_root=args.repo_root, output_path=args.output)
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
