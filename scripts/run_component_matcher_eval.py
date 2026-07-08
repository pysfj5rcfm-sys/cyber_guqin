#!/usr/bin/env python3
"""Run an unlabeled or labeled evaluation pass for the component matcher."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.component_matcher import DEFAULT_INDEX, ComponentImageIndex, ComponentMatcher


def run_eval(
    crop_dir: Path | str,
    *,
    index_path: Path | str = DEFAULT_INDEX,
    repo_root: Path | str = REPO_ROOT,
    output_path: Path | str | None = None,
    labels_path: Path | str | None = None,
    top_k: int = 5,
    unknown_threshold: float = 0.45,
) -> dict[str, Any]:
    root = Path(repo_root)
    labels = _load_labels(labels_path) if labels_path else {}
    matcher = ComponentMatcher(
        ComponentImageIndex.from_file(index_path, repo_root=root),
        unknown_threshold=unknown_threshold,
    )
    crops = sorted(path for path in Path(crop_dir).rglob("*.png") if path.is_file())
    rows = []
    matched = ambiguous = unknown = 0
    labeled_count = 0
    top1_correct = 0
    topk_hit = 0

    for crop in crops:
        crop_id = crop.stem
        result = matcher.match(crop, crop_id=crop_id, top_k=top_k)
        status = result["status"]
        if status == "MATCHED":
            matched += 1
        elif status == "AMBIGUOUS":
            ambiguous += 1
        elif status == "UNKNOWN_COMPONENT":
            unknown += 1

        candidate_ids = [candidate["component_id"] for candidate in result["candidates"]]
        label = labels.get(crop_id) or labels.get(crop.name) or labels.get(str(crop))
        if label:
            labeled_count += 1
            if candidate_ids and candidate_ids[0] == label:
                top1_correct += 1
            if label in candidate_ids:
                topk_hit += 1

        rows.append(
            {
                "crop_id": crop_id,
                "crop_path": _relative_or_string(crop, root),
                "status": status,
                "top1_component_id": candidate_ids[0] if candidate_ids else None,
                "topk_component_ids": candidate_ids,
                "label_component_id": label,
            }
        )

    evaluation_status = "LABELED_EVAL" if labeled_count else "UNLABELED_EVAL"
    result = {
        "eval_id": "CG_LXY_P2B_component_matcher_eval.v0.1",
        "crop_dir": _relative_or_string(Path(crop_dir), root),
        "index_path": _relative_or_string(Path(index_path), root),
        "evaluation_status": evaluation_status,
        "total_crops": len(crops),
        "matched": matched,
        "ambiguous": ambiguous,
        "unknown": unknown,
        "labeled_crops": labeled_count,
        "top1_accuracy": None if not labeled_count else round(top1_correct / labeled_count, 6),
        "topk_recall": None if not labeled_count else round(topk_hit / labeled_count, 6),
        "accuracy_policy": "accuracy_not_computed_without_explicit_labels" if not labeled_count else "explicit_labels_only",
        "rows": rows,
        "authority_flags": {
            "NOT_SCORE_AUTHORITY": True,
            "NOT_DAPU_IR_AUTHORITY": True,
            "NOT_SAMPLE_INGEST": True,
            "NOT_ML_TRAINING_DATA": True,
        },
    }

    if output_path is not None:
        out = Path(output_path)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _load_labels(path: Path | str | None) -> dict[str, str]:
    if not path:
        return {}
    label_path = Path(path)
    if label_path.suffix.lower() == ".json":
        data = json.loads(label_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(key): str(value) for key, value in data.items()}
        if isinstance(data, list):
            return {
                str(item["crop_id"]): str(item["component_id"])
                for item in data
                if isinstance(item, dict) and item.get("crop_id") and item.get("component_id")
            }
        raise ValueError(f"label JSON must be object or list: {label_path}")
    with label_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        labels = {}
        for row in reader:
            crop_id = row.get("crop_id") or row.get("filename") or row.get("crop_path")
            component_id = row.get("component_id") or row.get("label_component_id")
            if crop_id and component_id:
                labels[str(crop_id)] = str(component_id)
        return labels


def _relative_or_string(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate component matcher outputs over a crop directory.")
    parser.add_argument("crop_dir")
    parser.add_argument("--index", default=str(DEFAULT_INDEX))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--output", default="component_matcher_eval_result.json")
    parser.add_argument("--labels")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--unknown-threshold", type=float, default=0.45)
    args = parser.parse_args(argv)

    result = run_eval(
        args.crop_dir,
        index_path=args.index,
        repo_root=args.repo_root,
        output_path=args.output,
        labels_path=args.labels,
        top_k=args.top_k,
        unknown_threshold=args.unknown_threshold,
    )
    print(
        json.dumps(
            {
                "evaluation_status": result["evaluation_status"],
                "total_crops": result["total_crops"],
                "matched": result["matched"],
                "ambiguous": result["ambiguous"],
                "unknown": result["unknown"],
                "top1_accuracy": result["top1_accuracy"],
                "topk_recall": result["topk_recall"],
                "output": args.output,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
