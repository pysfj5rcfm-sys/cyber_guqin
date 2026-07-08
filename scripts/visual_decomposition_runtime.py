#!/usr/bin/env python3
"""P2G visual decomposition runtime for notation-unit crops.

This layer is visual-only. It proposes decomposition trees and review packets
from image geometry. It does not call P2B, does not call P1/P3, and does not
emit component ids, readings, score facts, or Dapu IR.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


AUTHORITY_FLAGS = {
    "VISUAL_DECOMPOSITION_ONLY": True,
    "NOT_COMPONENT_ID_AUTHORITY": True,
    "NOT_GRAMMAR_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_SCORE_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
    "NEEDS_HUMAN_REVIEW": True,
}

CONTRACT_ID = "CG_LXY_P2G_visual_decomposition.v0.1"
RUNTIME_LAYER = "P2G_VISUAL_DECOMPOSITION_RUNTIME_MVP"

SEMANTIC_FORBIDDEN_KEYS = {
    "component_id",
    "label",
    "lexical_component_type",
    "semantic_role",
    "semantic_role_assigned",
    "reading",
    "surface_reading",
    "surface_reading_candidate",
    "score_fact",
    "score_event",
    "dapu_ir",
}
SEMANTIC_FORBIDDEN_VALUES = {
    "LEFT_FINGER",
    "HUI_POSITION",
    "RIGHT_HAND_ACTION",
    "STRING_NUMBER",
    "PRE_SOUND_MOTION",
    "POST_SOUND_MOTION",
    "SOUND_STATE",
    "SPECIAL_TECHNIQUE",
}

LAYOUT_FAMILIES = {
    "UPPER_LOWER",
    "UPPER_MIDDLE_LOWER",
    "LOWER_ONLY",
    "LEFT_RIGHT",
    "ENCLOSURE_WITH_INNER",
    "ATTACHED_MARKS",
    "SCATTERED_OR_AMBIGUOUS",
}


try:  # pragma: no cover - local environments may not have Pillow.
    from PIL import Image
except Exception:  # pragma: no cover
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

    def to_list(self) -> list[int]:
        return [self.x, self.y, self.width, self.height]

    def to_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}


@dataclass(frozen=True)
class Region:
    region_id: str
    bbox: BBox
    ink_area: int
    role_hint: str = "unknown_visual_region"

    @property
    def center(self) -> tuple[float, float]:
        return self.bbox.center


@dataclass(frozen=True)
class VisualStructurePattern:
    pattern_id: str
    status: str
    layout_family: str
    visual_only: bool
    allowed_roles: tuple[str, ...]
    decomposition_rules: tuple[str, ...]
    quality_metrics: dict[str, Any]
    forbidden: tuple[str, ...]
    authority_flags: dict[str, Any]


class VisualStructurePatternRegistry:
    """Configuration-only registry for human-reviewed visual patterns."""

    def __init__(self, registry_id: str, patterns: list[VisualStructurePattern]) -> None:
        self.registry_id = registry_id
        self.patterns = list(patterns)

    @classmethod
    def from_file(cls, path: Path | str) -> "VisualStructurePatternRegistry":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VisualStructurePatternRegistry":
        patterns = []
        for item in data.get("patterns") or []:
            patterns.append(
                VisualStructurePattern(
                    pattern_id=str(item.get("pattern_id")),
                    status=str(item.get("status")),
                    layout_family=str(item.get("layout_family")),
                    visual_only=bool(item.get("visual_only")),
                    allowed_roles=tuple(str(value) for value in item.get("allowed_roles") or []),
                    decomposition_rules=tuple(str(value) for value in item.get("decomposition_rules") or []),
                    quality_metrics=dict(item.get("quality_metrics") or {}),
                    forbidden=tuple(str(value) for value in item.get("forbidden") or []),
                    authority_flags=dict(item.get("authority_flags") or {}),
                )
            )
        return cls(str(data.get("registry_id") or "INLINE_VISUAL_STRUCTURE_PATTERNS"), patterns)

    @classmethod
    def empty(cls) -> "VisualStructurePatternRegistry":
        return cls("NO_VISUAL_STRUCTURE_PATTERN_REGISTRY", [])

    def active_patterns(self) -> list[VisualStructurePattern]:
        return [pattern for pattern in self.patterns if pattern.status == "HUMAN_REVIEWED_ACTIVE"]

    def trace(self) -> dict[str, Any]:
        active = self.active_patterns()
        semantic_count = sum(0 if pattern.visual_only else 1 for pattern in active)
        return {
            "registry_id": self.registry_id,
            "active_pattern_ids": [pattern.pattern_id for pattern in active],
            "semantic_patterns_loaded": semantic_count,
            "visual_only": semantic_count == 0,
        }


class VisualDecomposer:
    """Build visual-only segmentation tree candidates from an image crop."""

    def __init__(
        self,
        *,
        pattern_registry: VisualStructurePatternRegistry | None = None,
        ink_threshold: int = 245,
        min_region_area: int = 4,
    ) -> None:
        self.pattern_registry = pattern_registry or VisualStructurePatternRegistry.empty()
        self.ink_threshold = int(ink_threshold)
        self.min_region_area = int(min_region_area)

    def decompose(self, image_crop: Path | str | dict[str, Any], *, notation_unit_id: str | None = None) -> dict[str, Any]:
        request = _normalize_request(image_crop, notation_unit_id)
        matrix, width, height = _load_image_matrix(Path(request["path_or_uri"]))
        raw_regions = _detect_regions(
            matrix,
            width,
            height,
            ink_threshold=self.ink_threshold,
            min_region_area=self.min_region_area,
        )

        if not raw_regions:
            return self._empty_response(request["notation_unit_id"], width, height)

        regions = _merge_fragments_to_visual_units(raw_regions)
        total = _union_many([region.bbox for region in regions])
        bands = _assign_bands(regions, total)
        layout = _layout_family(bands, regions)
        tree = _build_tree(regions, bands, total, layout)
        component_regions = _component_region_candidates(tree)
        quality = _quality_metrics(regions, total, width, height, tree, raw_region_count=len(raw_regions))
        failure_flags = _failure_flags(layout, regions, tree, quality)

        candidate = {
            "candidate_id": "SEG001",
            "layout_family": layout,
            "visual_score": quality["segmentation_confidence"],
            "tree": tree,
        }
        return {
            "contract_id": CONTRACT_ID,
            "notation_unit_id": request["notation_unit_id"],
            "layout_candidates": [
                {
                    "layout_family": layout,
                    "visual_score": quality["segmentation_confidence"],
                    "evidence": {
                        "region_count": len(regions),
                        "upper_count": len(bands["upper"]),
                        "middle_count": len(bands["middle"]),
                        "lower_count": len(bands["lower"]),
                    },
                }
            ],
            "segmentation_tree_candidates": [candidate],
            "component_region_candidates": component_regions,
            "quality_metrics": quality,
            "failure_flags": failure_flags,
            "review_packet": _review_packet(regions, total, bands, failure_flags),
            "pattern_registry_trace": self.pattern_registry.trace(),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "decomposition_trace": {
                "runtime_layer": RUNTIME_LAYER,
                "p2b_matcher_called": False,
                "p1_parse_called": False,
                "p3_grammar_called": False,
                "component_ids_generated": False,
                "notation_text_generated": False,
                "dapu_ir_generated": False,
                "deterministic": True,
                "image_size": {"width": width, "height": height},
                "source_path": request["path_or_uri"],
                "raw_ink_region_count": len(raw_regions),
                "visual_unit_count": len(regions),
            },
        }

    def _empty_response(self, notation_unit_id: str, width: int, height: int) -> dict[str, Any]:
        return {
            "contract_id": CONTRACT_ID,
            "notation_unit_id": notation_unit_id,
            "layout_candidates": [{"layout_family": "SCATTERED_OR_AMBIGUOUS", "visual_score": 0.0, "evidence": {"region_count": 0}}],
            "segmentation_tree_candidates": [],
            "component_region_candidates": [],
            "quality_metrics": {
                "coverage_ratio": 0.0,
                "unassigned_ink_ratio": 1.0,
                "segmentation_confidence": 0.0,
            },
            "failure_flags": ["NO_INK_DETECTED", "UNKNOWN_STRUCTURE_CANDIDATE"],
            "review_packet": {
                "review_status": "NEEDS_HUMAN_STRUCTURE_REVIEW",
                "proposed_regions": [],
                "unassigned_ink": [],
                "debug_features": {"projection_peaks": [], "containment_candidates": []},
            },
            "pattern_registry_trace": self.pattern_registry.trace(),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "decomposition_trace": {
                "runtime_layer": RUNTIME_LAYER,
                "p2b_matcher_called": False,
                "p1_parse_called": False,
                "p3_grammar_called": False,
                "component_ids_generated": False,
                "notation_text_generated": False,
                "dapu_ir_generated": False,
                "deterministic": True,
                "image_size": {"width": width, "height": height},
            },
        }


def validate_visual_decomposition(result: dict[str, Any], *, return_errors: bool = False) -> bool | list[str]:
    errors: list[str] = []
    required = {
        "contract_id",
        "notation_unit_id",
        "layout_candidates",
        "segmentation_tree_candidates",
        "component_region_candidates",
        "quality_metrics",
        "failure_flags",
        "review_packet",
        "pattern_registry_trace",
        "authority_flags",
        "decomposition_trace",
    }
    missing = sorted(required - set(result))
    if missing:
        errors.append(f"missing keys: {missing}")
    if result.get("contract_id") != CONTRACT_ID:
        errors.append(f"unexpected contract id: {result.get('contract_id')}")
    for key, expected in AUTHORITY_FLAGS.items():
        if (result.get("authority_flags") or {}).get(key) is not expected:
            errors.append(f"authority flag must be true: {key}")
    for candidate in result.get("layout_candidates") or []:
        if candidate.get("layout_family") not in LAYOUT_FAMILIES:
            errors.append(f"unsupported layout family: {candidate.get('layout_family')}")
    for candidate in result.get("segmentation_tree_candidates") or []:
        tree = candidate.get("tree")
        if not isinstance(tree, dict):
            errors.append(f"segmentation candidate missing tree: {candidate.get('candidate_id')}")
        else:
            errors.extend(_validate_node(tree))
    forbidden = _find_forbidden_semantic_content(result)
    if forbidden:
        errors.append(f"forbidden semantic/component content present: {forbidden}")
    return errors if return_errors else not errors


def _normalize_request(image_crop: Path | str | dict[str, Any], notation_unit_id: str | None) -> dict[str, str]:
    if isinstance(image_crop, (str, Path)):
        path = Path(image_crop)
        return {
            "path_or_uri": str(path),
            "notation_unit_id": notation_unit_id or path.stem or "notation_unit",
        }
    if not isinstance(image_crop, dict):
        raise TypeError("image_crop must be a path or dict")
    ref = image_crop.get("crop_image_reference") or {}
    path = image_crop.get("path_or_uri") or image_crop.get("image_path") or ref.get("path_or_uri") or ref.get("path")
    if not path:
        raise ValueError("image crop must include a path")
    return {
        "path_or_uri": str(path),
        "notation_unit_id": notation_unit_id or str(image_crop.get("notation_unit_id") or Path(path).stem or "notation_unit"),
    }


def _load_image_matrix(path: Path) -> tuple[list[list[int]], int, int]:
    if Image is not None:
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            width, height = rgba.size
            values = [_visual_gray_from_rgba(*pixel) for pixel in rgba.getdata()]
            return [values[row * width : (row + 1) * width] for row in range(height)], width, height
    raw = path.read_bytes()
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return _read_png(raw)
    return _read_netpbm(raw)


def _read_png(raw: bytes) -> tuple[list[list[int]], int, int]:
    offset = 8
    width = height = bit_depth = color_type = compression = filter_method = interlace = None
    idat_parts: list[bytes] = []

    while offset + 8 <= len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        kind = raw[offset + 4 : offset + 8]
        payload = raw[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", payload)
        elif kind == b"IDAT":
            idat_parts.append(payload)
        elif kind == b"IEND":
            break

    if width is None or height is None:
        raise ValueError("PNG image is missing IHDR")
    if bit_depth != 8 or compression != 0 or filter_method != 0 or interlace != 0:
        raise ValueError("unsupported PNG encoding without Pillow")

    channels_by_color = {0: 1, 2: 3, 4: 2, 6: 4}
    channels = channels_by_color.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported PNG color type without Pillow: {color_type}")

    stride = width * channels
    data = zlib.decompress(b"".join(idat_parts))
    rows: list[list[int]] = []
    previous = [0] * stride
    pos = 0
    for _ in range(height):
        if pos >= len(data):
            raise ValueError("PNG image data is shorter than expected")
        filter_type = data[pos]
        pos += 1
        scanline = list(data[pos : pos + stride])
        pos += stride
        if len(scanline) != stride:
            raise ValueError("PNG scanline is shorter than expected")
        row = _png_unfilter(scanline, previous, filter_type, channels)
        rows.append(_png_row_to_gray(row, width, color_type, channels))
        previous = row
    return rows, width, height


def _png_unfilter(scanline: list[int], previous: list[int], filter_type: int, bytes_per_pixel: int) -> list[int]:
    row = list(scanline)
    for index, value in enumerate(scanline):
        left = row[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
        up = previous[index]
        up_left = previous[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
        if filter_type == 0:
            predictor = 0
        elif filter_type == 1:
            predictor = left
        elif filter_type == 2:
            predictor = up
        elif filter_type == 3:
            predictor = (left + up) // 2
        elif filter_type == 4:
            predictor = _paeth(left, up, up_left)
        else:
            raise ValueError(f"unsupported PNG filter type: {filter_type}")
        row[index] = (value + predictor) & 0xFF
    return row


def _paeth(left: int, up: int, up_left: int) -> int:
    p = left + up - up_left
    pa = abs(p - left)
    pb = abs(p - up)
    pc = abs(p - up_left)
    if pa <= pb and pa <= pc:
        return left
    if pb <= pc:
        return up
    return up_left


def _png_row_to_gray(row: list[int], width: int, color_type: int, channels: int) -> list[int]:
    gray: list[int] = []
    for x in range(width):
        pixel = row[x * channels : (x + 1) * channels]
        if color_type == 0:
            value = pixel[0]
            gray.append(value)
        elif color_type == 2:
            gray.append(_visual_gray_from_rgba(pixel[0], pixel[1], pixel[2], 255))
        elif color_type == 4:
            value = pixel[0]
            alpha = pixel[1]
            gray.append(round(value * alpha / 255 + 255 * (1 - alpha / 255)))
        else:
            gray.append(_visual_gray_from_rgba(pixel[0], pixel[1], pixel[2], pixel[3]))
    return gray


def _visual_gray_from_rgba(red: int, green: int, blue: int, alpha: int = 255) -> int:
    alpha_ratio = alpha / 255
    channels = [
        round(red * alpha_ratio + 255 * (1 - alpha_ratio)),
        round(green * alpha_ratio + 255 * (1 - alpha_ratio)),
        round(blue * alpha_ratio + 255 * (1 - alpha_ratio)),
    ]
    if max(channels) - min(channels) > 50:
        return 255
    return round(sum(channels) / 3)


def _read_netpbm(raw: bytes) -> tuple[list[list[int]], int, int]:
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
        gray = []
        for index in range(0, expected, 3):
            gray.append(round(sum(values[index : index + 3]) / 3))
        values = gray
    else:
        values = values[:expected]
    if max_value != 255:
        values = [round(value * 255 / max(1, max_value)) for value in values]
    return [values[row * width : (row + 1) * width] for row in range(height)], width, height


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
) -> list[Region]:
    mask = [[pixel < ink_threshold for pixel in row] for row in matrix]
    visited = [[False for _ in range(width)] for _ in range(height)]
    boxes: list[tuple[BBox, int]] = []

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
                boxes.append((BBox(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1), area))

    return [
        Region(f"R{index:03d}", bbox, area)
        for index, (bbox, area) in enumerate(sorted(boxes, key=lambda item: (item[0].y, item[0].x)), start=1)
    ]


def _merge_fragments_to_visual_units(regions: list[Region]) -> list[Region]:
    if len(regions) <= 1:
        return regions

    total = _union_many([region.bbox for region in regions])
    total_ink = sum(region.ink_area for region in regions)
    anchor_min = max(40, int(total_ink * 0.018))
    anchors = [region for region in regions if region.ink_area >= anchor_min]
    if not anchors:
        return regions

    groups = [[region] for region in anchors]
    small_regions = [region for region in regions if region.ink_area < anchor_min]
    groups = _merge_anchor_groups(groups, total, total_ink)

    for region in small_regions:
        nearest_index, nearest_distance = _nearest_group(region, groups)
        attach_distance = max(8.0, total.height * 0.08)
        if nearest_index is not None and (
            nearest_distance <= attach_distance or (region.ink_area <= 12 and nearest_distance <= attach_distance * 2)
        ):
            groups[nearest_index].append(region)

    visual_units = []
    for index, group in enumerate(sorted(groups, key=lambda item: (_union_many([region.bbox for region in item]).y, _union_many([region.bbox for region in item]).x)), start=1):
        bbox = _union_many([region.bbox for region in group])
        visual_units.append(Region(f"V{index:03d}", bbox, sum(region.ink_area for region in group)))
    return visual_units


def _merge_anchor_groups(groups: list[list[Region]], total: BBox, total_ink: int) -> list[list[Region]]:
    large_anchor_min = max(350, int(total_ink * 0.10))
    changed = True
    while changed:
        changed = False
        for left_index in range(len(groups)):
            if changed:
                break
            for right_index in range(left_index + 1, len(groups)):
                if _should_merge_anchor_groups(groups[left_index], groups[right_index], total, large_anchor_min):
                    groups[left_index].extend(groups.pop(right_index))
                    changed = True
                    break
    return groups


def _should_merge_anchor_groups(left: list[Region], right: list[Region], total: BBox, large_anchor_min: int) -> bool:
    left_bbox = _union_many([region.bbox for region in left])
    right_bbox = _union_many([region.bbox for region in right])
    left_ink = sum(region.ink_area for region in left)
    right_ink = sum(region.ink_area for region in right)
    if left_ink >= large_anchor_min and right_ink >= large_anchor_min:
        return False

    overlap = _x_overlap_ratio(left_bbox, right_bbox)
    vertical_gap = _axis_gap(left_bbox.y, left_bbox.y2, right_bbox.y, right_bbox.y2)
    combined = _union_many([left_bbox, right_bbox])
    compact_width = combined.width <= total.width * 0.36
    compact_gap = vertical_gap <= max(8, total.height * 0.07)
    if overlap >= 0.25 and compact_width and compact_gap:
        return True

    distance = _bbox_distance(left_bbox, right_bbox)
    return distance <= max(8.0, total.height * 0.06) and compact_width


def _nearest_group(region: Region, groups: list[list[Region]]) -> tuple[int | None, float]:
    nearest_index: int | None = None
    nearest_distance = math.inf
    for index, group in enumerate(groups):
        bbox = _union_many([item.bbox for item in group])
        distance = _bbox_distance(region.bbox, bbox)
        if distance < nearest_distance:
            nearest_index = index
            nearest_distance = distance
    return nearest_index, nearest_distance


def _x_overlap_ratio(left: BBox, right: BBox) -> float:
    overlap = max(0, min(left.x2, right.x2) - max(left.x, right.x))
    return overlap / max(1, min(left.width, right.width))


def _axis_gap(left_start: int, left_end: int, right_start: int, right_end: int) -> int:
    if left_end < right_start:
        return right_start - left_end
    if right_end < left_start:
        return left_start - right_end
    return 0


def _bbox_distance(left: BBox, right: BBox) -> float:
    dx = _axis_gap(left.x, left.x2, right.x, right.x2)
    dy = _axis_gap(left.y, left.y2, right.y, right.y2)
    return math.hypot(dx, dy)


def _assign_bands(regions: list[Region], total: BBox) -> dict[str, list[Region]]:
    upper_cut = total.y + total.height * 0.38
    lower_cut = total.y + total.height * 0.62
    bands = {"upper": [], "middle": [], "lower": []}
    for region in regions:
        _, cy = region.center
        if cy <= upper_cut:
            bands["upper"].append(region)
        elif cy >= lower_cut:
            bands["lower"].append(region)
        else:
            bands["middle"].append(region)
    for key in bands:
        bands[key].sort(key=lambda item: (item.bbox.x, item.bbox.y, item.region_id))
    return bands


def _layout_family(bands: dict[str, list[Region]], regions: list[Region]) -> str:
    if _is_scattered_unknown(bands, regions):
        return "SCATTERED_OR_AMBIGUOUS"
    if bands["upper"] and bands["middle"] and bands["lower"]:
        return "UPPER_MIDDLE_LOWER"
    if bands["upper"] and bands["lower"]:
        return "UPPER_LOWER"
    if bands["lower"] and not bands["upper"] and not bands["middle"]:
        return "LOWER_ONLY"
    if len(regions) == 2:
        return "LEFT_RIGHT"
    if _containment_pairs(regions):
        return "ENCLOSURE_WITH_INNER"
    return "SCATTERED_OR_AMBIGUOUS"


def _is_scattered_unknown(bands: dict[str, list[Region]], regions: list[Region]) -> bool:
    if len(regions) != 3:
        return False
    if not (len(bands["upper"]) == len(bands["middle"]) == len(bands["lower"]) == 1):
        return False
    if _containment_pairs(regions):
        return False
    centers = [region.center for region in sorted(regions, key=lambda item: item.bbox.y)]
    return centers[0][0] < centers[1][0] < centers[2][0]


def _build_tree(regions: list[Region], bands: dict[str, list[Region]], total: BBox, layout: str) -> dict[str, Any]:
    idgen = _NodeId()
    root = _node(idgen, "root", total)
    if layout == "SCATTERED_OR_AMBIGUOUS":
        root["children"] = [_node(idgen, "unknown_visual_region", region.bbox, source_region_id=region.region_id) for region in regions]
        return root

    for band_name in ("upper", "middle", "lower"):
        band_regions = bands[band_name]
        if not band_regions:
            continue
        band_node = _node(idgen, f"{band_name}_band", _union_many([region.bbox for region in band_regions]))
        band_node["children"] = _region_nodes_for_band(idgen, band_name, band_regions)
        root["children"].append(band_node)
    return root


def _region_nodes_for_band(idgen: "_NodeId", band_name: str, regions: list[Region]) -> list[dict[str, Any]]:
    if band_name == "upper":
        return _linear_nodes(idgen, "upper", regions)
    if band_name == "middle":
        return _linear_nodes(idgen, "middle", regions)
    return _lower_nodes(idgen, regions)


def _linear_nodes(idgen: "_NodeId", prefix: str, regions: list[Region]) -> list[dict[str, Any]]:
    sorted_regions = sorted(regions, key=lambda item: (item.bbox.x, item.bbox.y, item.region_id))
    if len(sorted_regions) == 1:
        return [_node(idgen, f"{prefix}_region", sorted_regions[0].bbox, source_region_id=sorted_regions[0].region_id)]
    roles = [f"{prefix}_left_region", f"{prefix}_right_region"]
    nodes = []
    for index, region in enumerate(sorted_regions):
        role = roles[index] if index < len(roles) else f"{prefix}_attached_mark"
        nodes.append(_node(idgen, role, region.bbox, source_region_id=region.region_id))
    return nodes


def _lower_nodes(idgen: "_NodeId", regions: list[Region]) -> list[dict[str, Any]]:
    contained_to_host = _contained_to_host(regions)
    host_ids = set(contained_to_host.values())
    child_by_host: dict[str, list[Region]] = {}
    for child_id, host_id in contained_to_host.items():
        child = next(region for region in regions if region.region_id == child_id)
        child_by_host.setdefault(host_id, []).append(child)

    top_level = [region for region in regions if region.region_id not in contained_to_host]
    top_level.sort(key=lambda item: (item.bbox.x, item.bbox.y, item.region_id))
    nodes = []
    for index, region in enumerate(top_level):
        if region.region_id in host_ids:
            role = "lower_outer_region"
        elif index == 0:
            role = "lower_left_region"
        elif index == len(top_level) - 1:
            role = "lower_right_region"
        else:
            role = "lower_inner_region"
        node = _node(idgen, role, region.bbox, source_region_id=region.region_id)
        for child in sorted(child_by_host.get(region.region_id, []), key=lambda item: (item.bbox.x, item.bbox.y)):
            node["children"].append(_node(idgen, "lower_inner_region", child.bbox, source_region_id=child.region_id))
        nodes.append(node)
    return nodes


def _node(idgen: "_NodeId", role: str, bbox: BBox, *, source_region_id: str | None = None) -> dict[str, Any]:
    node = {
        "node_id": idgen.next(),
        "visual_role": role,
        "bbox": bbox.to_list(),
        "children": [],
        "relations": [],
        "confidence": _role_confidence(role),
    }
    if source_region_id:
        node["source_region_id"] = source_region_id
    return node


class _NodeId:
    def __init__(self) -> None:
        self.value = 0

    def next(self) -> str:
        self.value += 1
        return f"N{self.value:03d}"


def _role_confidence(role: str) -> float:
    if role in {"root", "upper_band", "middle_band", "lower_band"}:
        return 0.86
    if "unknown" in role:
        return 0.25
    if "inner" in role or "outer" in role:
        return 0.78
    return 0.74


def _component_region_candidates(tree: dict[str, Any]) -> list[dict[str, Any]]:
    regions = []
    for node in _walk_nodes(tree):
        role = node["visual_role"]
        if role == "root" or role.endswith("_band"):
            continue
        regions.append(
            {
                "region_id": node.get("source_region_id") or node["node_id"],
                "node_id": node["node_id"],
                "visual_role": role,
                "bbox": list(node["bbox"]),
                "parent_node_id": _find_parent_id(tree, node["node_id"]),
                "confidence": node["confidence"],
            }
        )
    return sorted(regions, key=lambda item: item["node_id"])


def _quality_metrics(
    regions: list[Region],
    total: BBox,
    width: int,
    height: int,
    tree: dict[str, Any],
    *,
    raw_region_count: int,
) -> dict[str, Any]:
    ink_area = sum(region.ink_area for region in regions)
    coverage = 1.0 if ink_area else 0.0
    bbox_ratio = total.area / max(1, width * height)
    unknown_nodes = sum(1 for node in _walk_nodes(tree) if "unknown" in node["visual_role"])
    confidence = max(0.0, min(1.0, 0.88 - unknown_nodes * 0.2 - max(0.0, bbox_ratio - 0.75) * 0.2))
    return {
        "coverage_ratio": round(coverage, 3),
        "unassigned_ink_ratio": round(1.0 - coverage, 3),
        "ink_region_count": len(regions),
        "raw_ink_region_count": raw_region_count,
        "visual_unit_count": len(regions),
        "notation_unit_bbox": total.to_dict(),
        "notation_unit_bbox_area_ratio": round(bbox_ratio, 3),
        "segmentation_confidence": round(confidence, 3),
    }


def _failure_flags(layout: str, regions: list[Region], tree: dict[str, Any], quality: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    if layout == "SCATTERED_OR_AMBIGUOUS":
        flags.append("UNKNOWN_STRUCTURE_CANDIDATE")
    if len(regions) == 1 and quality.get("notation_unit_bbox_area_ratio", 0.0) > 0.55:
        flags.append("OVER_MERGED_REGION")
    if any(node["visual_role"] == "lower_outer_region" and not node.get("children") for node in _walk_nodes(tree)):
        flags.append("ENCLOSURE_INNER_NOT_FOUND")
    return flags


def _review_packet(regions: list[Region], total: BBox, bands: dict[str, list[Region]], failure_flags: list[str]) -> dict[str, Any]:
    return {
        "review_status": "NEEDS_HUMAN_STRUCTURE_REVIEW" if failure_flags else "OPTIONAL_REVIEW",
        "proposed_regions": [
            {
                "region_id": region.region_id,
                "bbox": region.bbox.to_dict(),
                "visual_band": _band_for_region(region, bands),
            }
            for region in regions
        ],
        "unassigned_ink": [],
        "debug_features": {
            "projection_peaks": _projection_peaks(regions, total),
            "containment_candidates": [
                {"inner_region_id": child, "outer_region_id": host}
                for child, host in sorted(_contained_to_host(regions).items())
            ],
        },
    }


def _band_for_region(region: Region, bands: dict[str, list[Region]]) -> str:
    for name, values in bands.items():
        if any(item.region_id == region.region_id for item in values):
            return name
    return "unknown"


def _projection_peaks(regions: list[Region], total: BBox) -> list[dict[str, Any]]:
    peaks = []
    for region in sorted(regions, key=lambda item: (item.bbox.y, item.bbox.x)):
        cx, cy = region.center
        peaks.append(
            {
                "region_id": region.region_id,
                "center_norm": [
                    round((cx - total.x) / max(1, total.width), 3),
                    round((cy - total.y) / max(1, total.height), 3),
                ],
            }
        )
    return peaks


def _validate_node(node: dict[str, Any]) -> list[str]:
    errors = []
    required = {"node_id", "visual_role", "bbox", "children", "relations", "confidence"}
    missing = sorted(required - set(node))
    if missing:
        errors.append(f"node missing keys: {missing}")
    if not isinstance(node.get("children"), list):
        errors.append(f"node children must be list: {node.get('node_id')}")
    for child in node.get("children") or []:
        errors.extend(_validate_node(child))
    return errors


def _walk_nodes(node: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield node
    for child in node.get("children") or []:
        yield from _walk_nodes(child)


def _find_parent_id(root: dict[str, Any], node_id: str, parent_id: str | None = None) -> str | None:
    if root.get("node_id") == node_id:
        return parent_id
    for child in root.get("children") or []:
        found = _find_parent_id(child, node_id, root.get("node_id"))
        if found:
            return found
    return None


def _find_forbidden_semantic_content(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in SEMANTIC_FORBIDDEN_KEYS:
                found.append(child_path)
            found.extend(_find_forbidden_semantic_content(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_forbidden_semantic_content(child, f"{path}[{index}]"))
    elif isinstance(value, str) and value in SEMANTIC_FORBIDDEN_VALUES:
        found.append(path)
    return found


def _union_many(boxes: list[BBox]) -> BBox:
    x0 = min(box.x for box in boxes)
    y0 = min(box.y for box in boxes)
    x1 = max(box.x2 for box in boxes)
    y1 = max(box.y2 for box in boxes)
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


def _contained_to_host(regions: list[Region]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for source in regions:
        hosts = [
            candidate
            for candidate in regions
            if candidate.region_id != source.region_id and _containment_ratio(source.bbox, candidate.bbox) >= 0.8
        ]
        if hosts:
            host = sorted(hosts, key=lambda item: (-item.bbox.area, item.region_id))[0]
            mapping[source.region_id] = host.region_id
    return mapping


def _containment_pairs(regions: list[Region]) -> list[tuple[str, str]]:
    return sorted(_contained_to_host(regions).items())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run P2G visual decomposition on a notation-unit crop.")
    parser.add_argument("image_crop")
    parser.add_argument("--notation-unit-id")
    parser.add_argument("--pattern-registry")
    args = parser.parse_args(argv)
    registry = (
        VisualStructurePatternRegistry.from_file(args.pattern_registry)
        if args.pattern_registry
        else VisualStructurePatternRegistry.empty()
    )
    result = VisualDecomposer(pattern_registry=registry).decompose(
        args.image_crop,
        notation_unit_id=args.notation_unit_id,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
