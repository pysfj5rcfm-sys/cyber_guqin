#!/usr/bin/env python3
"""Bridge P2G visual decomposition regions into P2B component lattices.

This runtime consumes a visual-only P2G decomposition tree, crops each visual
region, calls the P2B component matcher, and builds a component candidate
lattice. It does not parse grammar, emit readings, create score facts, or
produce Dapu IR.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import zlib
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.component_candidate_lattice import CandidateLattice
from scripts.component_matcher_runtime import load_default_matcher
from scripts.visual_decomposition_runtime import _load_image_matrix


CONTRACT_ID = "CG_LXY_P2G_P2B_component_lattice.v0.1"
RUNTIME_LAYER = "P2G_TO_P2B_COMPONENT_LATTICE_RUNTIME"

AUTHORITY_FLAGS = {
    "GPT_TRANSCRIPTION_DRAFT": True,
    "NEEDS_HUMAN_REVIEW": True,
    "VISUAL_DECOMPOSITION_SOURCE_NOT_COMPONENT_AUTHORITY": True,
    "P2B_COMPONENT_CANDIDATES_DRAFT": True,
    "NOT_GRAMMAR_AUTHORITY": True,
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_CANON_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
}

FORBIDDEN_KEYS = {
    "reading",
    "surface_reading",
    "surface_reading_candidate",
    "phrase_reading",
    "canonical_reading",
    "score_fact",
    "score_event",
    "dapu_ir",
    "Dapu_IR",
}


class P2GComponentLatticeRuntime:
    """Project P2G visual regions into P2B component candidate sets."""

    def __init__(
        self,
        *,
        matcher: Any | None = None,
        crop_output_dir: Path | str | None = None,
        crop_padding_px: int = 0,
    ) -> None:
        self.matcher = matcher or load_default_matcher()
        self.crop_output_dir = Path(crop_output_dir) if crop_output_dir is not None else Path("/private/tmp/cg_p2g_region_crops")
        self.crop_padding_px = max(0, int(crop_padding_px))

    def build(
        self,
        decomposition: dict[str, Any],
        *,
        source_image_path: Path | str | None = None,
        top_k: int = 5,
    ) -> dict[str, Any]:
        notation_unit_id = str(decomposition.get("notation_unit_id") or "notation_unit")
        source = _source_path(decomposition, source_image_path)
        matrix, width, height = _load_image_matrix(source)
        regions = [dict(region) for region in decomposition.get("component_region_candidates") or []]

        self.crop_output_dir.mkdir(parents=True, exist_ok=True)
        candidate_sets = []
        for index, region in enumerate(regions, start=1):
            region_id = str(region.get("region_id") or f"region_{index:03d}")
            bbox = _sanitize_bbox(region.get("bbox"), width, height, padding=self.crop_padding_px)
            crop_path = self.crop_output_dir / f"{_safe_name(notation_unit_id)}__{_safe_name(region_id)}.png"
            _write_grayscale_png(crop_path, _crop_matrix(matrix, bbox))
            crop_id = region_id
            candidate_set = self._match_crop(crop_path, top_k=top_k, crop_id=crop_id)
            candidate_set["visual_region"] = {
                "region_id": region_id,
                "node_id": region.get("node_id"),
                "visual_role": region.get("visual_role"),
                "bbox": bbox,
                "p2g_confidence": region.get("confidence"),
            }
            candidate_set["crop_image_reference"] = {
                "path_or_uri": str(crop_path),
                "reference_type": "p2g_visual_region_crop",
                "source_image_path": str(source),
            }
            candidate_sets.append(candidate_set)

        lattice = CandidateLattice().build(candidate_sets)
        failure_flags = _failure_flags(candidate_sets, regions)
        return {
            "contract_id": CONTRACT_ID,
            "notation_unit_id": notation_unit_id,
            "status": _status(candidate_sets),
            "source_image_reference": {
                "path_or_uri": str(source),
                "reference_type": "notation_unit_crop",
            },
            "component_candidate_sets": candidate_sets,
            "component_candidate_lattice": lattice,
            "p3_handoff_projection": {
                "component_candidates": _projection(candidate_sets),
            },
            "failure_flags": failure_flags,
            "authority_flags": dict(AUTHORITY_FLAGS),
            "runtime_trace": {
                "runtime_layer": RUNTIME_LAYER,
                "p2g_decomposition_supplied": True,
                "component_matcher_called": bool(candidate_sets),
                "p1_parse_called": False,
                "p3_grammar_called": False,
                "grammar_context_used": False,
                "component_region_count": len(regions),
                "crop_files_written": len(candidate_sets),
                "top_k": int(top_k),
                "deterministic": True,
            },
        }

    def _match_crop(self, crop_path: Path, *, top_k: int, crop_id: str) -> dict[str, Any]:
        try:
            return self.matcher.match(crop_path, top_k=top_k, crop_id=crop_id, grammar_context=None)
        except TypeError:
            return self.matcher.match(crop_path, top_k=top_k, crop_id=crop_id)


def validate_p2g_component_lattice(result: dict[str, Any], *, return_errors: bool = False) -> bool | list[str]:
    errors: list[str] = []
    required = {
        "contract_id",
        "notation_unit_id",
        "status",
        "component_candidate_sets",
        "component_candidate_lattice",
        "p3_handoff_projection",
        "failure_flags",
        "authority_flags",
        "runtime_trace",
    }
    missing = sorted(required - set(result))
    if missing:
        errors.append(f"missing result keys: {missing}")
    if result.get("contract_id") != CONTRACT_ID:
        errors.append(f"invalid contract_id: {result.get('contract_id')}")
    if result.get("status") not in {"MATCHED", "PARTIAL", "UNRESOLVED"}:
        errors.append(f"invalid status: {result.get('status')}")
    flags = result.get("authority_flags") or {}
    for key in ("NOT_GRAMMAR_AUTHORITY", "NOT_DAPU_IR_AUTHORITY", "NOT_SCORE_EVENT_AUTHORITY"):
        if flags.get(key) is not True:
            errors.append(f"authority flag must be true: {key}")
    trace = result.get("runtime_trace") or {}
    if trace.get("p1_parse_called") is not False or trace.get("p3_grammar_called") is not False:
        errors.append("runtime must not call P1 or P3")
    forbidden = _find_forbidden_keys(result)
    if forbidden:
        errors.append(f"forbidden parse/reading keys present: {sorted(forbidden)}")
    return errors if return_errors else not errors


def _source_path(decomposition: dict[str, Any], source_image_path: Path | str | None) -> Path:
    if source_image_path is not None:
        return Path(source_image_path)
    trace = decomposition.get("decomposition_trace") or {}
    ref = decomposition.get("crop_image_reference") or {}
    path = trace.get("source_path") or decomposition.get("source_path") or ref.get("path_or_uri") or ref.get("path")
    if not path:
        raise ValueError("P2G decomposition must include source image path or caller must pass source_image_path")
    return Path(path)


def _sanitize_bbox(value: Any, width: int, height: int, *, padding: int) -> list[int]:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise ValueError(f"invalid bbox: {value}")
    x, y, w, h = [int(round(float(item))) for item in value]
    x0 = max(0, x - padding)
    y0 = max(0, y - padding)
    x1 = min(width, x + max(1, w) + padding)
    y1 = min(height, y + max(1, h) + padding)
    return [x0, y0, max(1, x1 - x0), max(1, y1 - y0)]


def _crop_matrix(matrix: list[list[int]], bbox: list[int]) -> list[list[int]]:
    x, y, width, height = bbox
    return [row[x : x + width] for row in matrix[y : y + height]]


def _write_grayscale_png(path: Path, matrix: list[list[int]]) -> None:
    height = len(matrix)
    width = len(matrix[0]) if matrix else 1
    rows = matrix or [[255]]
    raw = b"".join(b"\x00" + bytes(max(0, min(255, int(pixel))) for pixel in row) for row in rows)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"IDAT", zlib.compress(raw)) + _png_chunk(b"IEND", b""))


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def _safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return cleaned.strip("._") or "crop"


def _status(candidate_sets: list[dict[str, Any]]) -> str:
    if not candidate_sets or all(not item.get("candidates") for item in candidate_sets):
        return "UNRESOLVED"
    if any(not item.get("candidates") for item in candidate_sets):
        return "PARTIAL"
    return "MATCHED"


def _failure_flags(candidate_sets: list[dict[str, Any]], regions: list[dict[str, Any]]) -> list[str]:
    flags: list[str] = []
    if not regions:
        flags.append("NO_COMPONENT_REGIONS")
    if any(not item.get("candidates") for item in candidate_sets):
        flags.append("P2B_UNKNOWN_COMPONENT")
    return flags


def _projection(candidate_sets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projected = []
    for candidate_set in candidate_sets:
        region = candidate_set.get("visual_region") or {}
        for candidate in candidate_set.get("candidates") or []:
            final = (candidate.get("score_breakdown") or {}).get("final", candidate.get("visual_score", 0.0))
            projected.append(
                {
                    "region_id": region.get("region_id"),
                    "node_id": region.get("node_id"),
                    "visual_role": region.get("visual_role"),
                    "bbox": list(region.get("bbox") or []),
                    "component_id": candidate.get("component_id"),
                    "confidence": round(float(final), 3),
                    "visual_score": round(float(candidate.get("visual_score", 0.0)), 3),
                }
            )
    return projected


def _find_forbidden_keys(value: Any) -> set[str]:
    seen: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_KEYS:
                seen.add(str(key))
            seen.update(_find_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            seen.update(_find_forbidden_keys(child))
    return seen


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build P2B component lattice from a P2G decomposition JSON.")
    parser.add_argument("decomposition_json")
    parser.add_argument("--source-image")
    parser.add_argument("--crop-output-dir", default="/private/tmp/cg_p2g_region_crops")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args(argv)

    decomposition = json.loads(Path(args.decomposition_json).read_text(encoding="utf-8"))
    runtime = P2GComponentLatticeRuntime(crop_output_dir=args.crop_output_dir)
    result = runtime.build(decomposition, source_image_path=args.source_image, top_k=args.top_k)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
