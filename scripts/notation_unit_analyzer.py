#!/usr/bin/env python3
"""P2D visual slot lattice runtime for whole notation-unit crops.

The analyzer is a visual/layout layer only. It detects visual regions, proposes
visual slots, delegates component identity to P2B, and returns a slot lattice.
It does not assign grammar roles, phrase readings, score facts, or Dapu IR.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_SLOT_CONTRACT = (
    REPO_ROOT / "reports" / "lxy_136_phase_build" / "CG_LXY_P2C_slot_contract.v0.1.json"
)
DEFAULT_VISUAL_INDEX = REPO_ROOT / "references" / "qxby_component_atlas" / "component_visual_runtime_index.v0.1.json"

CONTRACT_ID = "CG_LXY_P2C_slot_contract.v0.1"
RUNTIME_LAYER = "P2D_VISUAL_SLOT_LATTICE_RUNTIME_MVP"

AUTHORITY_FLAGS = {
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
}

DEFAULT_SLOT_TYPES = [
    "LEFT_UPPER",
    "RIGHT_UPPER",
    "MIDDLE",
    "LOWER_OUTER",
    "LOWER_INNER",
    "ATTACHED_MARK",
]
DEFAULT_SLOT_STATUSES = [
    "PRESENT",
    "MISSING_COMPONENT",
    "UNKNOWN_SLOT",
    "UNKNOWN_COMPONENT",
    "AMBIGUOUS_SLOT",
    "EXTRA_INK",
]
FORBIDDEN_SEMANTIC_SLOT_TYPES = {
    "LEFT_FINGER",
    "HUI_POSITION",
    "PRE_SOUND_MOTION",
    "POST_SOUND_MOTION",
    "RIGHT_HAND_ACTION",
    "STRING_NUMBER",
    "SOUND_STATE",
    "SPECIAL_TECHNIQUE",
}
FORBIDDEN_INPUT_FIELDS = {
    "phrase_id",
    "phrase_reading",
    "complete_reading",
    "score_event",
    "score_fact",
    "dapu_ir",
    "sample_asset_ref",
    "training_label",
    "gold_answer_ref",
    "human_corrected_answer",
}
RELATION_TYPES = ["ABOVE", "BELOW", "LEFT_OF", "RIGHT_OF", "INSIDE", "ATTACHED"]
RELATION_ORDER = {name: index for index, name in enumerate(RELATION_TYPES)}


try:  # pragma: no cover - exercised only when Pillow exists in the local env.
    from PIL import Image
except Exception:  # pragma: no cover - deterministic stdlib fallback covers tests.
    Image = None


@dataclass(frozen=True)
class BBox:
    x: int
    y: int
    width: int
    height: int

    @property
    def x2(self) -> int:
        return self.x + self.width

    @property
    def y2(self) -> int:
        return self.y + self.height

    @property
    def area(self) -> int:
        return max(0, self.width) * max(0, self.height)

    @property
    def center(self) -> tuple[float, float]:
        return (self.x + self.width / 2.0, self.y + self.height / 2.0)

    def to_dict(self) -> dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


class NotationUnitAnalyzer:
    """Analyze one notation-unit crop into a VisualSlotLattice."""

    def __init__(
        self,
        component_matcher: Any | None = None,
        *,
        slot_contract_path: Path | str = DEFAULT_SLOT_CONTRACT,
        top_k_components_per_region: int = 5,
        ink_threshold: int = 245,
        min_region_area: int = 4,
    ) -> None:
        self.component_matcher = component_matcher
        self.slot_contract_path = Path(slot_contract_path)
        self.top_k_components_per_region = int(top_k_components_per_region)
        self.ink_threshold = int(ink_threshold)
        self.min_region_area = int(min_region_area)
        self.slot_types, self.slot_statuses = _load_slot_taxonomy(self.slot_contract_path)

    def analyze(self, image_crop: Any) -> dict[str, Any]:
        request = _normalize_input(image_crop)
        options = dict(request.get("analyzer_options") or {})
        notation_unit_id = request["notation_unit_id"]
        expected_slot_types = list(options.get("expected_slot_types") or [])

        try:
            matrix, width, height = _load_image_matrix(Path(request["path_or_uri"]))
            regions = _detect_regions(
                matrix,
                width,
                height,
                ink_threshold=int(options.get("ink_threshold", self.ink_threshold)),
                min_region_area=int(options.get("min_region_area", self.min_region_area)),
                merge_gap_px=options.get("region_merge_gap_px"),
            )
        except Exception as exc:
            return self._unresolved_lattice(
                notation_unit_id,
                status="UNRESOLVED",
                unresolved_status="UNKNOWN_SLOT",
                reason=f"IMAGE_LOAD_OR_REGION_DETECTION_FAILED:{type(exc).__name__}",
            )

        if not regions:
            return self._missing_or_empty_lattice(notation_unit_id, expected_slot_types)

        matcher = self.component_matcher or _load_default_component_matcher()
        slots: list[dict[str, Any]] = []
        unresolved: list[dict[str, Any]] = []
        matcher_statuses: list[str] = []

        with tempfile.TemporaryDirectory(prefix="cg_p2d_regions_") as tmpdir:
            tmp = Path(tmpdir)
            for index, region in enumerate(regions, start=1):
                crop_path = tmp / f"{region['region_id']}.pgm"
                _write_region_crop(matrix, region["bbox_obj"], crop_path)
                slot_type_candidates, slot_status, slot_confidence = self._slot_candidates(
                    region,
                    width,
                    height,
                    options,
                )
                matcher_result = matcher.match(
                    crop_path,
                    top_k=int(options.get("top_k_components_per_region", self.top_k_components_per_region)),
                    crop_id=region["region_id"],
                    grammar_context=None,
                )
                matcher_statuses.append(str(matcher_result.get("status") or "UNKNOWN_COMPONENT"))
                candidates = _slot_component_candidates(matcher_result, region["region_id"])
                if matcher_result.get("status") == "UNKNOWN_COMPONENT" or not candidates:
                    slot_status = "UNKNOWN_COMPONENT"

                slot = {
                    "slot_id": f"slot_{index:03d}",
                    "slot_type": slot_type_candidates[0] if slot_type_candidates else "UNKNOWN_SLOT",
                    "slot_type_candidates": slot_type_candidates or ["UNKNOWN_SLOT"],
                    "slot_status": slot_status,
                    "region_candidate_ids": [region["region_id"]],
                    "candidates": candidates,
                    "slot_confidence": _confidence(slot_confidence),
                    "semantic_role_assigned": False,
                }
                slots.append(slot)

                if slot_status in {"UNKNOWN_SLOT", "UNKNOWN_COMPONENT", "AMBIGUOUS_SLOT", "EXTRA_INK"}:
                    unresolved.append(
                        _unresolved_slot(
                            unresolved_id=f"unresolved_{len(unresolved) + 1:03d}",
                            status=slot_status,
                            reason=_unresolved_reason(slot_status, matcher_result),
                            region_ids=[region["region_id"]],
                        )
                    )

        missing_slots = self._missing_expected_slots(slots, expected_slot_types, unresolved)
        slots.extend(missing_slots)
        spatial_relations = _build_spatial_relations(regions, slots, width, height)
        status = _overall_status(slots, unresolved, matcher_statuses)

        lattice = {
            "contract_id": CONTRACT_ID,
            "notation_unit_id": notation_unit_id,
            "status": status,
            "slots": slots,
            "spatial_relations": spatial_relations,
            "unresolved_slots": unresolved,
            "p3_handoff_projection": _p3_handoff_projection(slots, spatial_relations),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "lattice_trace": {
                "runtime_layer": RUNTIME_LAYER,
                "p1_parse_called": False,
                "phrase_reading_generated": False,
                "context_inheritance_used": False,
                "dapu_ir_generated": False,
                "sample_ingest_used": False,
                "ml_training_used": False,
                "slot_taxonomy_source": str(self.slot_contract_path),
                "deterministic": True,
                "region_count": len(regions),
            },
        }
        return lattice

    def _slot_candidates(
        self,
        region: dict[str, Any],
        width: int,
        height: int,
        options: dict[str, Any],
    ) -> tuple[list[str], str, float]:
        overrides = options.get("region_slot_overrides") or {}
        override = overrides.get(region["region_id"])
        if override:
            values = override if isinstance(override, list) else [override]
            candidates = [str(value) for value in values if str(value) in self.slot_types]
            if not candidates:
                return [], "UNKNOWN_SLOT", 0.2
            status = "AMBIGUOUS_SLOT" if len(candidates) > 1 else "PRESENT"
            return candidates, status, 0.62 if len(candidates) > 1 else 0.85

        bbox: BBox = region["bbox_obj"]
        cx, cy = bbox.center
        cxn = cx / max(1, width)
        cyn = cy / max(1, height)
        ambiguity_band = float(options.get("slot_ambiguity_band", 0.05))
        upper_cutoff = float(options.get("upper_slot_cutoff", 0.38))
        lower_cutoff = float(options.get("lower_slot_cutoff", 0.67))

        if region.get("region_status") == "EXTRA_INK_REGION":
            return ["UNKNOWN_SLOT"], "EXTRA_INK", 0.25

        if cyn < upper_cutoff:
            if abs(cxn - 0.5) <= ambiguity_band and _has_slots(self.slot_types, "LEFT_UPPER", "RIGHT_UPPER"):
                return ["LEFT_UPPER", "RIGHT_UPPER"], "AMBIGUOUS_SLOT", 0.55
            slot_type = "LEFT_UPPER" if cxn < 0.5 else "RIGHT_UPPER"
            return _safe_slot_choice(slot_type, self.slot_types), "PRESENT", 0.84

        if cyn > lower_cutoff:
            if region.get("inside_region_id") and "LOWER_INNER" in self.slot_types:
                return ["LOWER_INNER"], "PRESENT", 0.78
            return _safe_slot_choice("LOWER_OUTER", self.slot_types), "PRESENT", 0.78

        return _safe_slot_choice("MIDDLE", self.slot_types), "PRESENT", 0.82

    def _missing_expected_slots(
        self,
        slots: list[dict[str, Any]],
        expected_slot_types: list[str],
        unresolved: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not expected_slot_types:
            return []
        present = {candidate for slot in slots for candidate in slot.get("slot_type_candidates", [])}
        missing: list[dict[str, Any]] = []
        for slot_type in expected_slot_types:
            if slot_type in present:
                continue
            status = "MISSING_COMPONENT" if slot_type in self.slot_types else "UNKNOWN_SLOT"
            missing.append(
                {
                    "slot_id": f"slot_{len(slots) + len(missing) + 1:03d}",
                    "slot_type": slot_type if slot_type in self.slot_types else "UNKNOWN_SLOT",
                    "slot_type_candidates": [slot_type] if slot_type in self.slot_types else ["UNKNOWN_SLOT"],
                    "slot_status": status,
                    "region_candidate_ids": [],
                    "candidates": [],
                    "slot_confidence": _confidence(0.0),
                    "semantic_role_assigned": False,
                }
            )
            unresolved.append(
                _unresolved_slot(
                    unresolved_id=f"unresolved_{len(unresolved) + 1:03d}",
                    status=status,
                    reason=f"expected visual slot has no detected region: {slot_type}",
                    region_ids=[],
                )
            )
        return missing

    def _missing_or_empty_lattice(self, notation_unit_id: str, expected_slot_types: list[str]) -> dict[str, Any]:
        slots: list[dict[str, Any]] = []
        unresolved: list[dict[str, Any]] = []
        if expected_slot_types:
            for slot_type in expected_slot_types:
                status = "MISSING_COMPONENT" if slot_type in self.slot_types else "UNKNOWN_SLOT"
                slots.append(
                    {
                        "slot_id": f"slot_{len(slots) + 1:03d}",
                        "slot_type": slot_type if slot_type in self.slot_types else "UNKNOWN_SLOT",
                        "slot_type_candidates": [slot_type] if slot_type in self.slot_types else ["UNKNOWN_SLOT"],
                        "slot_status": status,
                        "region_candidate_ids": [],
                        "candidates": [],
                        "slot_confidence": _confidence(0.0),
                        "semantic_role_assigned": False,
                    }
                )
                unresolved.append(
                    _unresolved_slot(
                        unresolved_id=f"unresolved_{len(unresolved) + 1:03d}",
                        status=status,
                        reason=f"expected visual slot has no detected region: {slot_type}",
                        region_ids=[],
                    )
                )
        else:
            slots.append(
                {
                    "slot_id": "slot_001",
                    "slot_type": "UNKNOWN_SLOT",
                    "slot_type_candidates": ["UNKNOWN_SLOT"],
                    "slot_status": "UNKNOWN_SLOT",
                    "region_candidate_ids": [],
                    "candidates": [],
                    "slot_confidence": _confidence(0.0),
                    "semantic_role_assigned": False,
                }
            )
            unresolved.append(
                _unresolved_slot(
                    unresolved_id="unresolved_001",
                    status="UNKNOWN_SLOT",
                    reason="no visual region detected",
                    region_ids=[],
                )
            )
        return {
            "contract_id": CONTRACT_ID,
            "notation_unit_id": notation_unit_id,
            "status": "UNRESOLVED",
            "slots": slots,
            "spatial_relations": [],
            "unresolved_slots": unresolved,
            "p3_handoff_projection": _p3_handoff_projection(slots, []),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "lattice_trace": {
                "runtime_layer": RUNTIME_LAYER,
                "p1_parse_called": False,
                "phrase_reading_generated": False,
                "context_inheritance_used": False,
                "dapu_ir_generated": False,
                "sample_ingest_used": False,
                "ml_training_used": False,
                "slot_taxonomy_source": str(self.slot_contract_path),
                "deterministic": True,
                "region_count": 0,
            },
        }

    def _unresolved_lattice(
        self,
        notation_unit_id: str,
        *,
        status: str,
        unresolved_status: str,
        reason: str,
    ) -> dict[str, Any]:
        slots = [
            {
                "slot_id": "slot_001",
                "slot_type": "UNKNOWN_SLOT",
                "slot_type_candidates": ["UNKNOWN_SLOT"],
                "slot_status": unresolved_status,
                "region_candidate_ids": [],
                "candidates": [],
                "slot_confidence": _confidence(0.0),
                "semantic_role_assigned": False,
            }
        ]
        unresolved = [
            _unresolved_slot(
                unresolved_id="unresolved_001",
                status=unresolved_status,
                reason=reason,
                region_ids=[],
            )
        ]
        return {
            "contract_id": CONTRACT_ID,
            "notation_unit_id": notation_unit_id,
            "status": status,
            "slots": slots,
            "spatial_relations": [],
            "unresolved_slots": unresolved,
            "p3_handoff_projection": _p3_handoff_projection(slots, []),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "lattice_trace": {
                "runtime_layer": RUNTIME_LAYER,
                "p1_parse_called": False,
                "phrase_reading_generated": False,
                "context_inheritance_used": False,
                "dapu_ir_generated": False,
                "sample_ingest_used": False,
                "ml_training_used": False,
                "slot_taxonomy_source": str(self.slot_contract_path),
                "deterministic": True,
                "region_count": 0,
            },
        }


def validate_visual_slot_lattice(lattice: dict[str, Any], *, return_errors: bool = False) -> bool | list[str]:
    errors: list[str] = []
    required = {
        "contract_id",
        "notation_unit_id",
        "status",
        "slots",
        "spatial_relations",
        "unresolved_slots",
        "p3_handoff_projection",
        "authority_flags",
        "lattice_trace",
    }
    missing = sorted(required - set(lattice))
    if missing:
        errors.append(f"missing lattice keys: {missing}")

    if lattice.get("status") not in {"RESOLVED", "AMBIGUOUS", "UNRESOLVED"}:
        errors.append(f"invalid status: {lattice.get('status')}")

    flags = lattice.get("authority_flags") or {}
    for key, expected in AUTHORITY_FLAGS.items():
        if flags.get(key) is not expected:
            errors.append(f"authority flag must be true: {key}")

    for slot in lattice.get("slots") or []:
        slot_type = slot.get("slot_type")
        if slot_type in FORBIDDEN_SEMANTIC_SLOT_TYPES:
            errors.append(f"semantic slot leaked into P2D output: {slot_type}")
        if slot.get("semantic_role_assigned") is not False:
            errors.append(f"slot assigned semantic role: {slot.get('slot_id')}")
        if slot.get("slot_status") not in set(DEFAULT_SLOT_STATUSES):
            errors.append(f"unsupported slot status: {slot.get('slot_status')}")
        for candidate in slot.get("candidates") or []:
            if candidate.get("semantic_role") != "unknown":
                errors.append(f"component semantic role is not unknown: {candidate.get('component_id')}")
            if not str(candidate.get("component_id", "")).startswith("COMP-") and candidate.get("component_id") != "UNKNOWN_COMPONENT":
                errors.append(f"unsupported component id shape: {candidate.get('component_id')}")

    for relation in lattice.get("spatial_relations") or []:
        if relation.get("relation") not in RELATION_TYPES:
            errors.append(f"unsupported relation alias: {relation.get('relation')}")
        if relation.get("relation_type") != str(relation.get("relation", "")).lower():
            errors.append(f"relation alias/type mismatch: {relation.get('relation_id')}")

    forbidden_paths = _find_forbidden_keys(lattice)
    if forbidden_paths:
        errors.append(f"forbidden semantic/authority fields present: {forbidden_paths}")

    return errors if return_errors else not errors


def _normalize_input(image_crop: Any) -> dict[str, Any]:
    if isinstance(image_crop, (str, Path)):
        path = Path(image_crop)
        return {
            "notation_unit_id": path.stem or "notation_unit",
            "path_or_uri": str(path),
            "analyzer_options": {},
        }

    if not isinstance(image_crop, dict):
        raise TypeError("image_crop must be a path or a NotationUnitCrop object")

    forbidden = sorted(FORBIDDEN_INPUT_FIELDS.intersection(image_crop))
    if forbidden:
        raise ValueError(f"P2D input contains forbidden reading/authority fields: {forbidden}")

    ref = dict(image_crop.get("crop_image_reference") or {})
    path = image_crop.get("path_or_uri") or image_crop.get("image_path") or ref.get("path_or_uri") or ref.get("path")
    if not path:
        raise ValueError("NotationUnitCrop must include crop_image_reference.path_or_uri")

    return {
        "notation_unit_id": str(image_crop.get("notation_unit_id") or Path(path).stem or "notation_unit"),
        "path_or_uri": str(path),
        "analyzer_options": dict(image_crop.get("analyzer_options") or {}),
    }


def _load_slot_taxonomy(path: Path) -> tuple[list[str], list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        taxonomy = data.get("visual_slot_taxonomy") or {}
        slot_types = [str(item) for item in taxonomy.get("slot_type_enum") or []]
        statuses = [str(item) for item in taxonomy.get("slot_status_enum") or []]
        return slot_types or list(DEFAULT_SLOT_TYPES), statuses or list(DEFAULT_SLOT_STATUSES)
    except Exception:
        return list(DEFAULT_SLOT_TYPES), list(DEFAULT_SLOT_STATUSES)


def _load_default_component_matcher() -> Any:
    from scripts.component_matcher_runtime import ComponentMatcher
    from scripts.component_visual_index import ComponentVisualIndex

    return ComponentMatcher(ComponentVisualIndex.from_file(DEFAULT_VISUAL_INDEX))


def _load_image_matrix(path: Path) -> tuple[list[list[int]], int, int]:
    if Image is not None:
        with Image.open(path) as image:
            gray = image.convert("L")
            width, height = gray.size
            values = list(gray.getdata())
            matrix = [values[index * width : (index + 1) * width] for index in range(height)]
            return matrix, width, height
    return _read_netpbm(path)


def _read_netpbm(path: Path) -> tuple[list[list[int]], int, int]:
    raw = path.read_bytes()
    tokens = list(_netpbm_tokens(raw))
    if len(tokens) < 4:
        raise ValueError("Netpbm image header is incomplete")
    magic = tokens[0]
    if magic not in {"P2", "P3"}:
        raise ValueError(f"unsupported image format without Pillow: {magic}")
    width = int(tokens[1])
    height = int(tokens[2])
    max_value = int(tokens[3])
    values = [int(token) for token in tokens[4:]]
    expected = width * height * (3 if magic == "P3" else 1)
    if len(values) < expected:
        raise ValueError("Netpbm image data is shorter than expected")
    if magic == "P3":
        gray_values = []
        for index in range(0, expected, 3):
            red, green, blue = values[index : index + 3]
            gray_values.append(round((red + green + blue) / 3))
        values = gray_values
    else:
        values = values[:expected]
    if max_value <= 0:
        raise ValueError("Netpbm max value must be positive")
    if max_value != 255:
        values = [round(value * 255 / max_value) for value in values]
    matrix = [values[row * width : (row + 1) * width] for row in range(height)]
    return matrix, width, height


def _netpbm_tokens(raw: bytes) -> Iterable[str]:
    text = raw.decode("ascii")
    for line in text.splitlines():
        line = line.split("#", 1)[0]
        for token in line.split():
            yield token


def _detect_regions(
    matrix: list[list[int]],
    width: int,
    height: int,
    *,
    ink_threshold: int,
    min_region_area: int,
    merge_gap_px: Any,
) -> list[dict[str, Any]]:
    mask = [[pixel < ink_threshold for pixel in row] for row in matrix]
    visited = [[False for _ in range(width)] for _ in range(height)]
    boxes: list[dict[str, Any]] = []

    for y in range(height):
        for x in range(width):
            if visited[y][x] or not mask[y][x]:
                visited[y][x] = True
                continue
            stack = [(x, y)]
            visited[y][x] = True
            min_x = max_x = x
            min_y = max_y = y
            area = 0
            while stack:
                cx, cy = stack.pop()
                area += 1
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height or visited[ny][nx]:
                        continue
                    visited[ny][nx] = True
                    if mask[ny][nx]:
                        stack.append((nx, ny))
            if area >= min_region_area:
                boxes.append({"bbox": BBox(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1), "ink_area": area})

    merged = _merge_boxes(boxes, _merge_gap(width, height, merge_gap_px))
    regions: list[dict[str, Any]] = []
    for index, item in enumerate(sorted(merged, key=lambda entry: (entry["bbox"].y, entry["bbox"].x)), start=1):
        bbox = item["bbox"]
        region_status = "REGION_CANDIDATE"
        if item["ink_area"] < min_region_area:
            region_status = "EXTRA_INK_REGION"
        regions.append(
            {
                "region_id": f"region_{index:03d}",
                "bbox": bbox.to_dict(),
                "bbox_obj": bbox,
                "ink_coverage": round(item["ink_area"] / max(1, bbox.area), 3),
                "region_status": region_status,
                "crop_reference": {"reference_type": "derived_region_crop"},
            }
        )
    _annotate_inside_regions(regions)
    return regions


def _merge_gap(width: int, height: int, explicit: Any) -> int:
    if explicit is not None:
        return max(0, int(explicit))
    return max(2, round(min(width, height) * 0.025))


def _merge_boxes(boxes: list[dict[str, Any]], gap: int) -> list[dict[str, Any]]:
    items = [dict(item) for item in boxes]
    changed = True
    while changed:
        changed = False
        result: list[dict[str, Any]] = []
        used: set[int] = set()
        for index, item in enumerate(items):
            if index in used:
                continue
            current = dict(item)
            for other_index in range(index + 1, len(items)):
                if other_index in used:
                    continue
                other = items[other_index]
                if _should_merge_regions(current["bbox"], other["bbox"], gap):
                    current = {
                        "bbox": _union_bbox(current["bbox"], other["bbox"]),
                        "ink_area": current["ink_area"] + other["ink_area"],
                    }
                    used.add(other_index)
                    changed = True
            used.add(index)
            result.append(current)
        items = result
    return items


def _should_merge_regions(left: BBox, right: BBox, gap: int) -> bool:
    larger = max(left.area, right.area)
    smaller = min(left.area, right.area)
    if larger and smaller / larger < 0.75:
        if _containment_ratio(left, right) >= 0.8 or _containment_ratio(right, left) >= 0.8:
            return False
    return _bbox_distance(left, right) <= gap


def _annotate_inside_regions(regions: list[dict[str, Any]]) -> None:
    for region in regions:
        bbox = region["bbox_obj"]
        hosts = [
            candidate
            for candidate in regions
            if candidate is not region and _containment_ratio(bbox, candidate["bbox_obj"]) >= 0.8
        ]
        if hosts:
            host = sorted(hosts, key=lambda item: (-item["bbox_obj"].area, item["region_id"]))[0]
            region["inside_region_id"] = host["region_id"]


def _bbox_distance(left: BBox, right: BBox) -> float:
    dx = max(left.x - right.x2, right.x - left.x2, 0)
    dy = max(left.y - right.y2, right.y - left.y2, 0)
    return math.hypot(dx, dy)


def _union_bbox(left: BBox, right: BBox) -> BBox:
    x0 = min(left.x, right.x)
    y0 = min(left.y, right.y)
    x1 = max(left.x2, right.x2)
    y1 = max(left.y2, right.y2)
    return BBox(x0, y0, x1 - x0, y1 - y0)


def _intersection_area(left: BBox, right: BBox) -> int:
    x0 = max(left.x, right.x)
    y0 = max(left.y, right.y)
    x1 = min(left.x2, right.x2)
    y1 = min(left.y2, right.y2)
    if x1 <= x0 or y1 <= y0:
        return 0
    return (x1 - x0) * (y1 - y0)


def _containment_ratio(source: BBox, target: BBox) -> float:
    return _intersection_area(source, target) / max(1, source.area)


def _write_region_crop(matrix: list[list[int]], bbox: BBox, path: Path) -> None:
    pad = 1
    x0 = max(0, bbox.x - pad)
    y0 = max(0, bbox.y - pad)
    x1 = min(len(matrix[0]), bbox.x2 + pad)
    y1 = min(len(matrix), bbox.y2 + pad)
    width = max(1, x1 - x0)
    height = max(1, y1 - y0)
    rows = ["P2", f"{width} {height}", "255"]
    for y in range(y0, y1):
        rows.append(" ".join(str(matrix[y][x]) for x in range(x0, x1)))
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def _slot_component_candidates(matcher_result: dict[str, Any], region_id: str) -> list[dict[str, Any]]:
    candidates = list(matcher_result.get("candidates") or [])
    normalized: list[dict[str, Any]] = []
    for item in sorted(candidates, key=lambda value: (int(value.get("rank", 0)), str(value.get("component_id", "")))):
        visual_score = _candidate_score(item)
        normalized.append(
            {
                "component_id": str(item.get("component_id") or "UNKNOWN_COMPONENT"),
                "label": str(item.get("label") or ""),
                "lexical_component_type": str(item.get("lexical_component_type") or "UNKNOWN_COMPONENT"),
                "visual_score": visual_score,
                "confidence": _confidence(visual_score),
                "p2b_candidate_rank": int(item.get("rank", 0)),
                "source_region_id": region_id,
                "semantic_role": "unknown",
                "evidence": {
                    "p2b_status": matcher_result.get("status"),
                    "p2b_evidence": dict(item.get("evidence") or {}),
                    "score_breakdown": dict(item.get("score_breakdown") or {}),
                },
            }
        )
    return normalized


def _candidate_score(candidate: dict[str, Any]) -> float:
    for key in ("visual_score",):
        try:
            return round(max(0.0, min(1.0, float(candidate.get(key)))), 3)
        except (TypeError, ValueError):
            pass
    breakdown = candidate.get("score_breakdown") or {}
    try:
        return round(max(0.0, min(1.0, float(breakdown.get("final")))), 3)
    except (TypeError, ValueError):
        return 0.0


def _confidence(value: float) -> dict[str, Any]:
    score = round(max(0.0, min(1.0, float(value))), 3)
    if score >= 0.8:
        bucket = "high"
    elif score >= 0.55:
        bucket = "medium"
    elif score >= 0.3:
        bucket = "low"
    else:
        bucket = "very_low"
    return {
        "value": score,
        "bucket": bucket,
        "score_type": "HEURISTIC_VISUAL_CONFIDENCE",
        "calibrated_probability": False,
    }


def _safe_slot_choice(slot_type: str, slot_types: list[str]) -> list[str]:
    return [slot_type] if slot_type in slot_types else []


def _has_slots(slot_types: list[str], *required: str) -> bool:
    available = set(slot_types)
    return all(item in available for item in required)


def _unresolved_reason(slot_status: str, matcher_result: dict[str, Any]) -> str:
    if slot_status == "UNKNOWN_COMPONENT":
        state = matcher_result.get("unknown_component_state") or {}
        return str(state.get("unresolved_reason") or "P2B returned UNKNOWN_COMPONENT")
    if slot_status == "AMBIGUOUS_SLOT":
        return "visual geometry supports multiple slot candidates"
    if slot_status == "EXTRA_INK":
        return "visual ink exists outside supported slot hypotheses"
    return "visual slot could not be resolved"


def _unresolved_slot(unresolved_id: str, status: str, reason: str, region_ids: list[str]) -> dict[str, Any]:
    return {
        "unresolved_id": unresolved_id,
        "status": status,
        "reason": reason,
        "region_candidate_ids": list(region_ids),
        "needs_human_review": True,
    }


def _overall_status(
    slots: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
    matcher_statuses: list[str],
) -> str:
    hard_unresolved = {"UNKNOWN_SLOT", "UNKNOWN_COMPONENT", "MISSING_COMPONENT", "EXTRA_INK"}
    if any(slot.get("slot_status") in hard_unresolved for slot in slots):
        return "UNRESOLVED"
    if any(item.get("status") in hard_unresolved for item in unresolved):
        return "UNRESOLVED"
    if any(slot.get("slot_status") == "AMBIGUOUS_SLOT" for slot in slots):
        return "AMBIGUOUS"
    if any(status == "AMBIGUOUS" for status in matcher_statuses):
        return "AMBIGUOUS"
    return "RESOLVED"


def _build_spatial_relations(
    regions: list[dict[str, Any]],
    slots: list[dict[str, Any]],
    width: int,
    height: int,
) -> list[dict[str, Any]]:
    component_by_region = _top_component_by_region(slots)
    relation_rows: list[dict[str, Any]] = []
    min_axis_delta = max(2.0, min(width, height) * 0.05)
    attached_gap = max(2.0, min(width, height) * 0.04)

    for left_index in range(len(regions)):
        for right_index in range(left_index + 1, len(regions)):
            source = regions[left_index]
            target = regions[right_index]
            source_bbox: BBox = source["bbox_obj"]
            target_bbox: BBox = target["bbox_obj"]
            sx, sy = source_bbox.center
            tx, ty = target_bbox.center
            dx = sx - tx
            dy = sy - ty

            if _containment_ratio(source_bbox, target_bbox) >= 0.8:
                relation_rows.append(_relation_row(source, target, "INSIDE", width, height, component_by_region))
            if _containment_ratio(target_bbox, source_bbox) >= 0.8:
                relation_rows.append(_relation_row(target, source, "INSIDE", width, height, component_by_region))

            if _bbox_distance(source_bbox, target_bbox) <= attached_gap:
                if source_bbox.area <= target_bbox.area:
                    relation_rows.append(_relation_row(source, target, "ATTACHED", width, height, component_by_region))
                else:
                    relation_rows.append(_relation_row(target, source, "ATTACHED", width, height, component_by_region))

            if abs(dy) >= min_axis_delta:
                if sy < ty:
                    relation_rows.append(_relation_row(source, target, "ABOVE", width, height, component_by_region))
                    relation_rows.append(_relation_row(target, source, "BELOW", width, height, component_by_region))
                else:
                    relation_rows.append(_relation_row(target, source, "ABOVE", width, height, component_by_region))
                    relation_rows.append(_relation_row(source, target, "BELOW", width, height, component_by_region))

            if abs(dx) >= min_axis_delta:
                if sx < tx:
                    relation_rows.append(_relation_row(source, target, "LEFT_OF", width, height, component_by_region))
                    relation_rows.append(_relation_row(target, source, "RIGHT_OF", width, height, component_by_region))
                else:
                    relation_rows.append(_relation_row(target, source, "LEFT_OF", width, height, component_by_region))
                    relation_rows.append(_relation_row(source, target, "RIGHT_OF", width, height, component_by_region))

    deduped = {
        (row["source_region_id"], row["relation"], row["target_region_id"]): row
        for row in relation_rows
    }
    sorted_rows = sorted(
        deduped.values(),
        key=lambda row: (
            row["source_region_id"],
            row["target_region_id"],
            RELATION_ORDER[row["relation"]],
        ),
    )
    for index, row in enumerate(sorted_rows, start=1):
        row["relation_id"] = f"rel_{index:03d}"
    return sorted_rows


def _top_component_by_region(slots: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for slot in slots:
        candidates = slot.get("candidates") or []
        top = candidates[0].get("component_id") if candidates else "UNKNOWN_COMPONENT"
        for region_id in slot.get("region_candidate_ids") or []:
            mapping[region_id] = top
    return mapping


def _relation_row(
    source: dict[str, Any],
    target: dict[str, Any],
    relation: str,
    width: int,
    height: int,
    component_by_region: dict[str, str],
) -> dict[str, Any]:
    source_bbox: BBox = source["bbox_obj"]
    target_bbox: BBox = target["bbox_obj"]
    sx, sy = source_bbox.center
    tx, ty = target_bbox.center
    dx = round((sx - tx) / max(1, width), 3)
    dy = round((sy - ty) / max(1, height), 3)
    overlap = _intersection_area(source_bbox, target_bbox) / max(1, min(source_bbox.area, target_bbox.area))
    containment = _containment_ratio(source_bbox, target_bbox)
    edge_distance = _bbox_distance(source_bbox, target_bbox) / max(1, min(width, height))
    axis_signal = max(abs(dx), abs(dy), containment, max(0.0, 1.0 - edge_distance))
    confidence_value = 0.72 if relation == "ATTACHED" else max(0.55, min(0.92, axis_signal))
    return {
        "relation_id": "",
        "source_region_id": source["region_id"],
        "target_region_id": target["region_id"],
        "relation_type": relation.lower(),
        "from": source["region_id"],
        "relation": relation,
        "to": target["region_id"],
        "from_component_id": component_by_region.get(source["region_id"], "UNKNOWN_COMPONENT"),
        "to_component_id": component_by_region.get(target["region_id"], "UNKNOWN_COMPONENT"),
        "geometry_evidence": {
            "source_bbox": source_bbox.to_dict(),
            "target_bbox": target_bbox.to_dict(),
            "center_delta": [dx, dy],
            "overlap_ratio": round(overlap, 3),
            "containment_ratio": round(containment, 3),
            "edge_distance": round(edge_distance, 3),
        },
        "confidence": _confidence(confidence_value),
    }


def _p3_handoff_projection(slots: list[dict[str, Any]], spatial_relations: list[dict[str, Any]]) -> dict[str, Any]:
    slot_candidates = [
        {
            "slot_id": slot.get("slot_id"),
            "slot_type": slot.get("slot_type"),
            "slot_type_candidates": list(slot.get("slot_type_candidates") or []),
            "slot_status": slot.get("slot_status"),
            "region_candidate_ids": list(slot.get("region_candidate_ids") or []),
            "semantic_role_assigned": False,
        }
        for slot in slots
    ]
    component_candidates = []
    for slot in slots:
        for candidate in slot.get("candidates") or []:
            component_candidates.append(
                {
                    "slot_id": slot.get("slot_id"),
                    "source_region_id": candidate.get("source_region_id"),
                    "component_id": candidate.get("component_id"),
                    "label": candidate.get("label"),
                    "lexical_component_type": candidate.get("lexical_component_type"),
                    "semantic_role": "unknown",
                    "visual_score": candidate.get("visual_score"),
                }
            )
    relation_projection = [
        {
            "from": relation.get("from"),
            "relation": relation.get("relation"),
            "to": relation.get("to"),
            "from_component_id": relation.get("from_component_id"),
            "to_component_id": relation.get("to_component_id"),
        }
        for relation in spatial_relations
    ]
    return {
        "slot_candidates": slot_candidates,
        "component_candidates": component_candidates,
        "spatial_relations": relation_projection,
        "confidence": _confidence(0.0 if not slots else min(slot["slot_confidence"]["value"] for slot in slots)),
    }


def _find_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_INPUT_FIELDS:
                found.append(child_path)
            found.extend(_find_forbidden_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_forbidden_keys(child, f"{path}[{index}]"))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze one notation-unit crop into a P2D visual slot lattice.")
    parser.add_argument("image_crop")
    parser.add_argument("--notation-unit-id")
    parser.add_argument("--top-k-components-per-region", type=int, default=5)
    args = parser.parse_args(argv)

    analyzer = NotationUnitAnalyzer(top_k_components_per_region=args.top_k_components_per_region)
    payload = {
        "notation_unit_id": args.notation_unit_id or Path(args.image_crop).stem,
        "crop_image_reference": {
            "path_or_uri": args.image_crop,
            "reference_type": "notation_unit_crop",
        },
    }
    print(json.dumps(analyzer.analyze(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
