#!/usr/bin/env python3
"""Audit QXBY batch source-image archives without modifying inputs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH_ID = "QXBY_BATCH_001"
DEFAULT_DRAFT = ROOT / "canon" / "drafts" / "qxby_batch_001.yaml"
DEFAULT_SOURCE_DIR = ROOT / "sources" / "qinxue_beiyao" / "QXBY_BATCH_001"
DEFAULT_MANIFEST = DEFAULT_SOURCE_DIR / "manifest.yaml"
DEFAULT_REPORT_MD = ROOT / "reports" / "qxby_batch_001_source_audit.md"
DEFAULT_REPORT_JSON = ROOT / "reports" / "qxby_batch_001_source_audit.json"
DEFAULT_EXPECTED_COUNT = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", default=DEFAULT_BATCH_ID)
    parser.add_argument("--draft", default=relative(DEFAULT_DRAFT))
    parser.add_argument("--source-dir", default=relative(DEFAULT_SOURCE_DIR))
    parser.add_argument("--manifest", default=relative(DEFAULT_MANIFEST))
    parser.add_argument("--expected-count", type=int, default=DEFAULT_EXPECTED_COUNT)
    parser.add_argument("--report-md", default=relative(DEFAULT_REPORT_MD))
    parser.add_argument("--report-json", default=relative(DEFAULT_REPORT_JSON))
    return parser.parse_args()


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value in {"null", "~"}:
        return None
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
    active_list_owner: dict[str, Any] | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line == "items:":
            root["items"] = items
            current = None
            active_list_key = None
            active_list_owner = None
            continue

        if line.startswith("- "):
            payload = line[2:]
            if active_list_owner is not None and active_list_key is not None:
                active_list_owner.setdefault(active_list_key, []).append(parse_scalar(payload))
            elif indent in {0, 2} and "items" in root:
                current = {}
                items.append(current)
                active_list_key = None
                active_list_owner = None
                if payload:
                    key, sep, value = payload.partition(":")
                    if not sep:
                        raise ValueError(f"cannot parse item line: {raw_line}")
                    current[key.strip()] = parse_scalar(value)
            else:
                raise ValueError(f"unsupported list indentation: {raw_line}")
            continue

        if indent == 0:
            key, sep, value = line.partition(":")
            if not sep:
                raise ValueError(f"cannot parse line: {raw_line}")
            key = key.strip()
            if value.strip():
                root[key] = parse_scalar(value)
                active_list_key = None
                active_list_owner = None
            else:
                root[key] = []
                active_list_key = key
                active_list_owner = root
            current = None
            continue

        if current is not None and indent > 0:
            key, sep, value = line.partition(":")
            if not sep:
                raise ValueError(f"cannot parse item field: {raw_line}")
            key = key.strip()
            if value.strip():
                current[key] = parse_scalar(value)
                active_list_key = None
                active_list_owner = None
            else:
                current[key] = []
                active_list_key = key
                active_list_owner = current
            continue

        raise ValueError(f"unsupported YAML fallback line: {raw_line}")

    root.setdefault("items", items)
    return root


def load_yaml(path: Path, warnings: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except Exception:
        data = fallback_yaml(text)
    if not isinstance(data, dict):
        raise ValueError(f"{relative(path)} root must be an object")
    return data


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def image_path_from_source_image(source_image: str) -> Path:
    path = Path(source_image)
    return path if path.is_absolute() else ROOT / path


def first_present(item: dict[str, Any], keys: tuple[str, ...]) -> tuple[str, Any]:
    for key in keys:
        if key in item and item.get(key) not in {None, ""}:
            return key, item.get(key)
    return "", None


def main() -> int:
    args = parse_args()
    batch_id = args.batch_id
    draft_path = resolve_path(args.draft)
    source_dir = resolve_path(args.source_dir)
    manifest_path = resolve_path(args.manifest)
    image_dir = source_dir / "images"
    report_md = resolve_path(args.report_md)
    report_json = resolve_path(args.report_json)

    errors: list[str] = []
    warnings: list[str] = []

    add(errors, source_dir.exists(), f"source folder missing: {relative(source_dir)}")
    add(errors, image_dir.exists(), f"images directory missing: {relative(image_dir)}")
    add(errors, manifest_path.exists(), f"manifest missing: {relative(manifest_path)}")
    add(errors, draft_path.exists(), f"draft missing: {relative(draft_path)}")

    image_files = sorted(path for path in image_dir.glob("*") if path.is_file()) if image_dir.exists() else []
    add(errors, len(image_files) == args.expected_count, f"images directory should contain {args.expected_count} files, found {len(image_files)}")

    draft: dict[str, Any] = {}
    manifest: dict[str, Any] = {}
    if draft_path.exists():
        try:
            draft = load_yaml(draft_path, warnings)
        except Exception as exc:
            errors.append(str(exc))
    if manifest_path.exists():
        try:
            manifest = load_yaml(manifest_path, warnings)
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

    add(errors, draft.get("batch_id") in {None, batch_id}, f"draft batch_id should be {batch_id}, got {draft.get('batch_id')!r}")
    add(errors, manifest.get("batch_id") in {None, batch_id}, f"manifest batch_id should be {batch_id}, got {manifest.get('batch_id')!r}")
    add(errors, len(draft_items) == args.expected_count, f"draft should contain {args.expected_count} items, found {len(draft_items)}")
    add(errors, len(manifest_items) == args.expected_count, f"manifest should contain {args.expected_count} items, found {len(manifest_items)}")

    draft_ids = [str(item.get("item_id")) for item in draft_items if isinstance(item, dict)]
    manifest_ids = [str(item.get("item_id")) for item in manifest_items if isinstance(item, dict)]
    draft_by_id = {str(item.get("item_id")): item for item in draft_items if isinstance(item, dict)}
    manifest_by_id = {str(item.get("item_id")): item for item in manifest_items if isinstance(item, dict)}

    add(errors, len(draft_ids) == len(draft_items), "every draft item must be an object with item_id")
    add(errors, len(manifest_ids) == len(manifest_items), "every manifest item must be an object with item_id")
    add(errors, not duplicates(draft_ids), f"duplicate draft item_id values: {duplicates(draft_ids)}")
    add(errors, not duplicates(manifest_ids), f"duplicate manifest item_id values: {duplicates(manifest_ids)}")
    add(
        errors,
        set(draft_ids) == set(manifest_ids),
        f"draft/manifest item_id mismatch: draft_only={sorted(set(draft_ids) - set(manifest_ids))}, manifest_only={sorted(set(manifest_ids) - set(draft_ids))}",
    )

    manifest_image_files = [str(item.get("image_file")) for item in manifest_items if isinstance(item, dict)]
    add(errors, not duplicates(manifest_image_files), f"duplicate manifest image_file values: {duplicates(manifest_image_files)}")

    all_image_rel = {path.relative_to(source_dir).as_posix() for path in image_files}
    manifest_image_rel = set(manifest_image_files)
    orphan_images = sorted(all_image_rel - manifest_image_rel)
    add(errors, not orphan_images, f"image files not referenced by manifest: {orphan_images}")

    manifest_missing: list[str] = []
    draft_missing: list[str] = []
    term_mismatches: list[str] = []
    internal_name_mismatches: list[str] = []
    missing_draft_internal_names: list[str] = []
    missing_mapped_component_names: list[str] = []
    filename_mismatches: list[str] = []
    source_image_outside_source_dir: list[str] = []

    for item_id, manifest_item in manifest_by_id.items():
        image_file = str(manifest_item.get("image_file", ""))
        image_path = source_dir / image_file
        if not image_path.exists():
            manifest_missing.append(f"{item_id}: {image_file}")

        draft_item = draft_by_id.get(item_id)
        if draft_item is None:
            continue
        term_key, term_value = first_present(draft_item, ("term", "normalized_term", "source_term"))
        term = str(term_value or "")
        manifest_term = str(manifest_item.get("term", ""))
        if manifest_term != term:
            term_mismatches.append(
                f"{item_id}: draft {term_key or 'term'}={term!r}, manifest term={manifest_term!r}"
            )
        draft_internal_name = draft_item.get("internal_name")
        manifest_internal_name = manifest_item.get("internal_name")
        if draft_internal_name in {None, ""}:
            missing_draft_internal_names.append(item_id)
        elif manifest_internal_name != draft_internal_name:
            internal_name_mismatches.append(
                f"{item_id}: draft internal_name={draft_internal_name!r}, manifest internal_name={manifest_internal_name!r}"
            )
        if "mapped_component_name" in draft_item and draft_item.get("mapped_component_name") in {None, ""}:
            missing_mapped_component_names.append(item_id)
        filename = Path(image_file).name
        if term and f"_{term}_" not in filename:
            filename_mismatches.append(f"{item_id}: {filename} does not contain _{term}_")

    for item_id, draft_item in draft_by_id.items():
        source_image = str(draft_item.get("source_image", ""))
        source_path = image_path_from_source_image(source_image)
        if not source_image:
            draft_missing.append(f"{item_id}: source_image is empty")
            continue
        if not source_path.exists():
            draft_missing.append(f"{item_id}: {source_image}")
        if not is_relative_to(source_path, image_dir):
            source_image_outside_source_dir.append(f"{item_id}: {source_image}")

        manifest_item = manifest_by_id.get(item_id)
        if manifest_item is not None:
            manifest_image = (source_dir / str(manifest_item.get("image_file", ""))).resolve()
            if source_path.exists() and manifest_image.exists() and source_path.resolve() != manifest_image:
                errors.append(f"{item_id}: draft source_image and manifest image_file point to different files")

    add(errors, not manifest_missing, f"manifest references missing files: {manifest_missing}")
    add(errors, not draft_missing, f"draft references missing files: {draft_missing}")
    add(errors, not source_image_outside_source_dir, f"draft source_image values outside source images dir: {source_image_outside_source_dir}")
    add(errors, not term_mismatches, f"term mismatches: {term_mismatches}")
    add(errors, not internal_name_mismatches, f"internal_name mismatches: {internal_name_mismatches}")
    add(errors, not missing_mapped_component_names, f"draft mapped_component_name present but empty: {missing_mapped_component_names}")
    if missing_draft_internal_names and batch_id != DEFAULT_BATCH_ID:
        warnings.append(
            "draft internal_name missing for item_id values; source audit skipped manifest.internal_name equality for these items: "
            f"{missing_draft_internal_names}"
        )
    if filename_mismatches:
        warnings.append(f"filename term readability mismatches: {filename_mismatches}")

    summary = {
        "batch_id": batch_id,
        "draft_items": len(draft_items),
        "manifest_items": len(manifest_items),
        "image_files": len(image_files),
        "expected_count": args.expected_count,
        "item_ids_match": set(draft_ids) == set(manifest_ids),
        "orphan_images": orphan_images,
        "manifest_missing_files": manifest_missing,
        "draft_missing_files": draft_missing,
        "source_image_outside_source_dir": source_image_outside_source_dir,
        "term_mismatches": term_mismatches,
        "internal_name_mismatches": internal_name_mismatches,
        "missing_draft_internal_names": missing_draft_internal_names,
        "missing_mapped_component_names": missing_mapped_component_names,
        "filename_mismatches": filename_mismatches,
        "semantic_rules": {
            "manifest_internal_name": "matches draft.internal_name when present",
            "mapped_component_name": "checked as a non-empty draft semantic mapping field when present; not compared to manifest.internal_name",
            "filename": "checked as human-readable metadata only; mismatches warn when referenced files exist",
        },
    }
    return write_reports(errors, warnings, summary, draft_path, manifest_path, image_dir, report_md, report_json, args)


def write_reports(
    errors: list[str],
    warnings: list[str],
    summary: dict[str, Any],
    draft_path: Path,
    manifest_path: Path,
    image_dir: Path,
    report_md: Path,
    report_json: Path,
    args: argparse.Namespace,
) -> int:
    status = "fail" if errors else ("warning" if warnings else "pass")
    report = {
        "auditor": "audit_qxby_batch_sources.py",
        "batch_id": args.batch_id,
        "expected_count": args.expected_count,
        "status": status,
        "passed": not errors,
        "inputs": {
            "draft": relative(draft_path),
            "manifest": relative(manifest_path),
            "images": relative(image_dir),
        },
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {args.batch_id} Source Audit",
        "",
        f"- status: `{status}`",
        f"- passed: `{str(not errors).lower()}`",
        f"- draft: `{relative(draft_path)}`",
        f"- manifest: `{relative(manifest_path)}`",
        f"- images: `{relative(image_dir)}`",
        "",
        "## Summary",
        "",
        f"- draft items: {summary.get('draft_items')}",
        f"- manifest items: {summary.get('manifest_items')}",
        f"- image files: {summary.get('image_files')}",
        f"- expected count: {summary.get('expected_count')}",
        f"- item ids match: {summary.get('item_ids_match')}",
        f"- orphan images: {summary.get('orphan_images')}",
        f"- manifest missing files: {summary.get('manifest_missing_files')}",
        f"- draft missing files: {summary.get('draft_missing_files')}",
        f"- source_image outside source dir: {summary.get('source_image_outside_source_dir')}",
        f"- term mismatches: {summary.get('term_mismatches')}",
        f"- internal_name mismatches: {summary.get('internal_name_mismatches')}",
        f"- draft items missing internal_name: {summary.get('missing_draft_internal_names')}",
        f"- draft mapped_component_name empty: {summary.get('missing_mapped_component_names')}",
        f"- filename mismatches: {summary.get('filename_mismatches')}",
        "",
        "## Semantic Rules",
        "",
        "- `manifest.internal_name` is aligned with draft `internal_name` when that field is present.",
        "- `mapped_component_name` is a semantic mapping field in the draft and is no longer required to equal manifest `internal_name`.",
        "- Source image filenames are human-readable archive aids; filename term mismatches are warnings when referenced files exist.",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in warnings) if warnings else lines.append("- none")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
