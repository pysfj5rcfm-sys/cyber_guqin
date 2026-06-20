from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
from typing import Any


EXPECTED_FILES = [
    "listening_review.csv",
    "listening_review.yaml",
    "issue_list.csv",
    "preferred_version_summary.csv",
    "phrase_structure_review.yaml",
    "render_phrase_alignment.csv",
    "phrase_boundary_decision.csv",
    "render_revision_log.yaml",
]


def main() -> int:
    render_root = resolve_render_root()
    draft_root = render_root / "r2_review_drafts"
    latest_dir = draft_root / "latest"
    state_path = latest_dir / "r2_review_state.latest.json"
    manifest_path = latest_dir / "r2_review_state_manifest.json"
    failures: list[str] = []

    state = read_json(state_path, failures)
    manifest = read_json(manifest_path, failures)
    if not state or not manifest:
        return fail(failures)

    require(manifest.get("canonical_source") == "r2_review_state.latest.json", failures, "manifest canonical_source is not r2_review_state.latest.json")
    require(Path(str(manifest.get("canonical_state_path", ""))) == state_path, failures, "manifest canonical_state_path does not point to latest JSON")
    require(manifest.get("no_downloads_policy") is True, failures, "manifest no_downloads_policy is not true")
    require(manifest.get("current_page_load_source") != "r2_review_exports", failures, "r2_review_exports is marked as current page load source")

    for file_name in EXPECTED_FILES:
        require((latest_dir / file_name).exists(), failures, f"latest missing {file_name}")

    require(csv_count(latest_dir / "render_phrase_alignment.csv") == 40, failures, "render_phrase_alignment.csv data rows != 40")
    require(csv_count(latest_dir / "phrase_boundary_decision.csv") == 40, failures, "phrase_boundary_decision.csv data rows != 40")

    counts = state_counts(state)
    for key, expected in counts.items():
        require(manifest.get(key) == expected, failures, f"manifest {key}={manifest.get(key)} does not match latest state {expected}")
    require(state.get("review_count") == counts["review_count"], failures, "state review_count does not match latest reviews")
    require(state.get("preferred_version_count") == counts["preferred_version_count"], failures, "state preferred_version_count does not match latest preferred versions")
    require(yaml_row_count(latest_dir / "render_revision_log.yaml") == counts["suggested_revision_count"], failures, "render_revision_log.yaml rows do not match non-empty suggested_revision count")

    exports_root = render_root / "r2_review_exports"
    leftover_zips = list(exports_root.rglob("*.zip")) if exports_root.exists() else []
    require(not leftover_zips, failures, f"temporary restore zip still exists: {[str(path) for path in leftover_zips]}")

    if failures:
        return fail(failures)
    print("PASS R2 canonical draft verification")
    print(json.dumps({"render_root": str(render_root), **counts}, ensure_ascii=False, indent=2))
    return 0


def resolve_render_root() -> Path:
    configured = os.environ.get("CG_VARW_R2_RENDER_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[4]
    return repo_root / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render"


def read_json(path: Path, failures: list[str]) -> dict[str, Any]:
    if not path.exists():
        failures.append(f"missing JSON: {path}")
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        failures.append(f"JSON root is not object: {path}")
        return {}
    return data


def csv_count(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def yaml_row_count(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "-":
            count += 1
    return count


def state_counts(state: dict[str, Any]) -> dict[str, int]:
    reviews = state.get("listeningReviewByKey") or state.get("listening_review_by_key") or {}
    if not isinstance(reviews, dict):
        reviews = {}
    review_items = [item for item in reviews.values() if isinstance(item, dict)]
    preferred = state.get("preferredVersionByPhrase") or state.get("preferred_version_by_phrase") or {}
    if not isinstance(preferred, dict):
        preferred = {}
    return {
        "review_count": len(review_items),
        "phrase_count": len({str(item.get("phrase_id", "")) for item in review_items if item.get("phrase_id")}),
        "preferred_version_count": len([value for value in preferred.values() if value]),
        "suggested_revision_count": len([item for item in review_items if str(item.get("suggested_revision", "")).strip()]),
        "issue_count": sum(len(item.get("issue_type") or []) for item in review_items if isinstance(item.get("issue_type"), list)),
    }


def require(condition: bool, failures: list[str], message: str) -> None:
    if not condition:
        failures.append(message)


def fail(failures: list[str]) -> int:
    print("FAIL R2 canonical draft verification", file=sys.stderr)
    for item in failures:
        print(f"- {item}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
