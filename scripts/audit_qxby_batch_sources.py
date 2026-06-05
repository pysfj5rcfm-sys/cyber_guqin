#!/usr/bin/env python3
"""Audit QXBY_BATCH_001 source-image archive without modifying inputs."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "canon" / "drafts" / "qxby_batch_001.yaml"
SOURCE_DIR = ROOT / "sources" / "qinxue_beiyao" / "QXBY_BATCH_001"
MANIFEST = SOURCE_DIR / "manifest.yaml"
IMAGE_DIR = SOURCE_DIR / "images"
REPORT_MD = ROOT / "reports" / "qxby_batch_001_source_audit.md"
REPORT_JSON = ROOT / "reports" / "qxby_batch_001_source_audit.json"

EXPECTED_COUNT = 16


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    return value


def fallback_yaml(text: str) -> dict[str, Any]:
    """Parse the simple mapping/list shape used by the QXBY draft and manifest."""
    root: dict[str, Any] = {}
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    active_list_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line == "items:":
            root["items"] = items
            current = None
            active_list_key = None
            continue

        if line.startswith("- "):
            payload = line[2:]
            if "items" not in root:
                root["items"] = items
            key, sep, value = payload.partition(":")
            if sep:
                current = {key.strip(): parse_scalar(value)}
                items.append(current)
                active_list_key = None
            elif current is not None and active_list_key is not None:
                current.setdefault(active_list_key, []).append(parse_scalar(payload))
            else:
                raise ValueError(f"cannot parse list line: {raw_line}")
            continue

        if current is not None and indent > 0:
            key, sep, value = line.partition(":")
            if not sep:
                raise ValueError(f"cannot parse item field: {raw_line}")
            if value.strip():
                current[key] = parse_scalar(value)
                active_list_key = None
            else:
                current[key] = []
                active_list_key = key
            continue

        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"cannot parse line: {raw_line}")
        root[key] = parse_scalar(value)
        active_list_key = None

    root.setdefault("items", items)
    return root


def load_yaml(path: Path, warnings: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except Exception:
        data = fallback_yaml(text)
        warnings.append(f"{path.relative_to(ROOT)} parsed with built-in YAML fallback")
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} root must be an object")
    return data


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def warn(warnings: list[str], condition: bool, message: str) -> None:
    if not condition:
        warnings.append(message)


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    add(errors, SOURCE_DIR.exists(), f"source folder missing: {rel(SOURCE_DIR)}")
    add(errors, SOURCE_DIR == ROOT / "sources" / "qinxue_beiyao" / "QXBY_BATCH_001", "source folder must be under sources/qinxue_beiyao/QXBY_BATCH_001/")
    add(errors, IMAGE_DIR.exists(), f"images directory missing: {rel(IMAGE_DIR)}")
    add(errors, MANIFEST.exists(), f"manifest missing: {rel(MANIFEST)}")
    add(errors, DRAFT.exists(), f"draft missing: {rel(DRAFT)}")

    image_files = sorted(path for path in IMAGE_DIR.glob("*") if path.is_file()) if IMAGE_DIR.exists() else []
    add(errors, len(image_files) == EXPECTED_COUNT, f"images directory should contain {EXPECTED_COUNT} files, found {len(image_files)}")

    draft: dict[str, Any] = {}
    manifest: dict[str, Any] = {}
    if DRAFT.exists():
        try:
            draft = load_yaml(DRAFT, warnings)
        except Exception as exc:
            errors.append(str(exc))
    if MANIFEST.exists():
        try:
            manifest = load_yaml(MANIFEST, warnings)
        except Exception as exc:
            errors.append(str(exc))

    draft_items = draft.get("items", [])
    manifest_items = manifest.get("items", [])
    add(errors, isinstance(draft_items, list), "draft items must be a list")
    add(errors, isinstance(manifest_items, list), "manifest items must be a list")
    if not isinstance(draft_items, list):
        draft_items = []
    if not isinstance(manifest_items, list):
        manifest_items = []

    add(errors, len(draft_items) == EXPECTED_COUNT, f"draft should contain {EXPECTED_COUNT} items, found {len(draft_items)}")
    add(errors, len(manifest_items) == EXPECTED_COUNT, f"manifest should contain {EXPECTED_COUNT} items, found {len(manifest_items)}")

    draft_by_id = {str(item.get("item_id")): item for item in draft_items if isinstance(item, dict)}
    manifest_by_id = {str(item.get("item_id")): item for item in manifest_items if isinstance(item, dict)}
    draft_ids = [str(item.get("item_id")) for item in draft_items if isinstance(item, dict)]
    manifest_ids = [str(item.get("item_id")) for item in manifest_items if isinstance(item, dict)]

    add(errors, not duplicates(draft_ids), f"duplicate draft item_id values: {duplicates(draft_ids)}")
    add(errors, not duplicates(manifest_ids), f"duplicate manifest item_id values: {duplicates(manifest_ids)}")
    add(errors, set(draft_ids) == set(manifest_ids), f"draft/manifest item_id mismatch: draft_only={sorted(set(draft_ids) - set(manifest_ids))}, manifest_only={sorted(set(manifest_ids) - set(draft_ids))}")

    manifest_image_files = [str(item.get("image_file")) for item in manifest_items if isinstance(item, dict)]
    add(errors, not duplicates(manifest_image_files), f"duplicate manifest image_file values: {duplicates(manifest_image_files)}")

    all_image_rel = {path.relative_to(SOURCE_DIR).as_posix() for path in image_files}
    manifest_image_rel = set(manifest_image_files)
    orphan_images = sorted(all_image_rel - manifest_image_rel)
    add(errors, not orphan_images, f"image files not referenced by manifest: {orphan_images}")

    manifest_missing: list[str] = []
    draft_missing: list[str] = []
    term_mismatches: list[str] = []
    filename_mismatches: list[str] = []

    for item_id, manifest_item in manifest_by_id.items():
        image_file = str(manifest_item.get("image_file", ""))
        image_path = SOURCE_DIR / image_file
        if not image_path.exists():
            manifest_missing.append(f"{item_id}: {image_file}")

        draft_item = draft_by_id.get(item_id)
        if draft_item is None:
            continue
        term = str(draft_item.get("normalized_term", ""))
        internal = str(draft_item.get("mapped_component_name", ""))
        if manifest_item.get("term") != term or manifest_item.get("internal_name") != internal:
            term_mismatches.append(
                f"{item_id}: draft term/internal={term}/{internal}, manifest={manifest_item.get('term')}/{manifest_item.get('internal_name')}"
            )
        filename = Path(image_file).name
        if f"_{term}_" not in filename:
            filename_mismatches.append(f"{item_id}: {filename} does not contain _{term}_")

    for item_id, draft_item in draft_by_id.items():
        source_image = str(draft_item.get("source_image", ""))
        source_path = ROOT / source_image
        if not source_path.exists():
            draft_missing.append(f"{item_id}: {source_image}")
        if not source_image.replace("\\", "/").startswith("sources/qinxue_beiyao/QXBY_BATCH_001/images/"):
            errors.append(f"{item_id}: source_image is outside sources/qinxue_beiyao/QXBY_BATCH_001/images/")

        manifest_item = manifest_by_id.get(item_id)
        if manifest_item is not None:
            manifest_image = (SOURCE_DIR / str(manifest_item.get("image_file", ""))).resolve()
            if source_path.exists() and manifest_image.exists() and source_path.resolve() != manifest_image:
                errors.append(f"{item_id}: draft source_image and manifest image_file point to different files")

    add(errors, not manifest_missing, f"manifest references missing files: {manifest_missing}")
    add(errors, not draft_missing, f"draft references missing files: {draft_missing}")
    add(errors, not term_mismatches, f"term/internal_name mismatches: {term_mismatches}")
    add(errors, not filename_mismatches, f"filename term mismatches: {filename_mismatches}")

    summary = {
        "draft_items": len(draft_items),
        "manifest_items": len(manifest_items),
        "image_files": len(image_files),
        "item_ids_match": set(draft_ids) == set(manifest_ids),
        "orphan_images": orphan_images,
        "manifest_missing_files": manifest_missing,
        "draft_missing_files": draft_missing,
        "term_mismatches": term_mismatches,
        "filename_mismatches": filename_mismatches,
    }
    return write_reports(errors, warnings, summary)


def write_reports(errors: list[str], warnings: list[str], summary: dict[str, Any]) -> int:
    status = "fail" if errors else ("warning" if warnings else "pass")
    report = {
        "auditor": "audit_qxby_batch_sources.py",
        "status": status,
        "passed": not errors,
        "inputs": {
            "draft": rel(DRAFT),
            "manifest": rel(MANIFEST),
            "images": rel(IMAGE_DIR),
        },
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# QXBY_BATCH_001 Source Audit",
        "",
        f"- status: `{status}`",
        f"- passed: `{str(not errors).lower()}`",
        f"- draft: `{rel(DRAFT)}`",
        f"- manifest: `{rel(MANIFEST)}`",
        f"- images: `{rel(IMAGE_DIR)}`",
        "",
        "## Summary",
        "",
        f"- draft items: {summary.get('draft_items')}",
        f"- manifest items: {summary.get('manifest_items')}",
        f"- image files: {summary.get('image_files')}",
        f"- item ids match: {summary.get('item_ids_match')}",
        f"- orphan images: {summary.get('orphan_images')}",
        f"- manifest missing files: {summary.get('manifest_missing_files')}",
        f"- draft missing files: {summary.get('draft_missing_files')}",
        f"- term mismatches: {summary.get('term_mismatches')}",
        f"- filename mismatches: {summary.get('filename_mismatches')}",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in warnings) if warnings else lines.append("- none")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
