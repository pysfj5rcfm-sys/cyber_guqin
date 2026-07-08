#!/usr/bin/env python3
"""Visual component candidate matcher for single guqin component crops.

This module is intentionally model-agnostic. The default backend is a small
stdlib template matcher over registry reference images; embedding and vision
model backends share the same adapter shape but are not bound here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = REPO_ROOT / "references" / "qxby_component_atlas" / "component_visual_index.v0.1.json"

AUTHORITY_FLAGS = {
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_CANON_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
}

FAILURE_CLASSIFICATIONS = {
    "IMAGE_INDEX_ERROR",
    "MATCHER_LOGIC_ERROR",
    "REGISTRY_MAPPING_ERROR",
    "INPUT_FORMAT_ERROR",
    "UNKNOWN_THRESHOLD_ERROR",
}

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class ComponentMatcherError(RuntimeError):
    """Base error for component matcher setup failures."""


class ImageDecodeError(ComponentMatcherError):
    """Raised when an image crop cannot be decoded by the stdlib PNG reader."""


@dataclass(frozen=True)
class ComponentIndexEntry:
    component_id: str
    label: str
    category: str
    image_path: str | None
    image_hash: str | None
    image_dimensions: dict[str, int] | None
    normalized_reference: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComponentIndexEntry":
        return cls(
            component_id=str(data["component_id"]),
            label=str(data.get("label", "")),
            category=str(data.get("category", "")),
            image_path=data.get("image_path"),
            image_hash=data.get("image_hash"),
            image_dimensions=data.get("image_dimensions"),
            normalized_reference=dict(data.get("normalized_reference") or {}),
        )

    @property
    def matchable(self) -> bool:
        return bool(self.image_path and self.normalized_reference.get("matchable"))

    def absolute_image_path(self, repo_root: Path) -> Path:
        if not self.image_path:
            raise ComponentMatcherError(f"component has no image_path: {self.component_id}")
        path = Path(self.image_path)
        return path if path.is_absolute() else repo_root / path


class ComponentImageIndex:
    """Registry-backed component visual index."""

    def __init__(self, data: dict[str, Any], *, repo_root: Path | str = REPO_ROOT) -> None:
        self.data = data
        self.repo_root = Path(repo_root)
        self.entries = [ComponentIndexEntry.from_dict(item) for item in data.get("components", [])]
        self.entries_by_id = {entry.component_id: entry for entry in self.entries}

    @classmethod
    def from_file(cls, path: Path | str, *, repo_root: Path | str | None = None) -> "ComponentImageIndex":
        index_path = Path(path)
        data = _load_json(index_path)
        root = Path(repo_root) if repo_root is not None else REPO_ROOT
        return cls(data, repo_root=root)

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, repo_root: Path | str = REPO_ROOT) -> "ComponentImageIndex":
        return cls(data, repo_root=repo_root)

    @property
    def component_index_count(self) -> int:
        return int(self.data.get("component_index_count", len(self.entries)))

    @property
    def image_reference_count(self) -> int:
        return int(self.data.get("image_reference_count", len(self.matchable_entries)))

    @property
    def matchable_entries(self) -> list[ComponentIndexEntry]:
        return [entry for entry in self.entries if entry.matchable]

    def get(self, component_id: str) -> ComponentIndexEntry:
        return self.entries_by_id[component_id]


@dataclass(frozen=True)
class GrayscaleImage:
    width: int
    height: int
    pixels: tuple[int, ...]


@dataclass(frozen=True)
class ImageFeature:
    width: int
    height: int
    grid: tuple[float, ...]
    dhash: int
    ink_ratio: float
    aspect_ratio: float
    empty: bool


@dataclass(frozen=True)
class ComponentCandidateEvidence:
    component: ComponentIndexEntry
    raw_score: float
    raw_score_type: str
    visual_similarity: dict[str, Any]
    notes: str


class ComponentMatcherBackend(Protocol):
    backend_id: str

    def score(
        self,
        crop_feature: ImageFeature,
        image_index: ComponentImageIndex,
    ) -> list[ComponentCandidateEvidence]:
        ...


class TemplateMatcherBackend:
    """Simple deterministic template scorer over normalized grayscale crops."""

    backend_id = "template_matching"

    def __init__(self) -> None:
        self._feature_cache: dict[str, ImageFeature] = {}

    def score(
        self,
        crop_feature: ImageFeature,
        image_index: ComponentImageIndex,
    ) -> list[ComponentCandidateEvidence]:
        evidence: list[ComponentCandidateEvidence] = []
        for entry in image_index.matchable_entries:
            reference_path = entry.absolute_image_path(image_index.repo_root)
            cache_key = str(reference_path)
            if cache_key not in self._feature_cache:
                self._feature_cache[cache_key] = extract_image_feature(reference_path)
            reference_feature = self._feature_cache[cache_key]
            score = compare_features(crop_feature, reference_feature)
            evidence.append(
                ComponentCandidateEvidence(
                    component=entry,
                    raw_score=score,
                    raw_score_type="HEURISTIC_TEMPLATE_SIMILARITY",
                    visual_similarity={
                        "score_type": "HEURISTIC_TEMPLATE_SIMILARITY",
                        "rank_score": round(score, 3),
                        "calibrated_probability": False,
                        "backend": self.backend_id,
                    },
                    notes="shape and normalized registry reference compared by template backend",
                )
            )
        return evidence


class EmbeddingMatcherBackend:
    """Replaceable embedding backend slot; intentionally unbound in P2-B MVP."""

    backend_id = "embedding_matching"

    def score(
        self,
        crop_feature: ImageFeature,
        image_index: ComponentImageIndex,
    ) -> list[ComponentCandidateEvidence]:
        raise NotImplementedError("P2-B MVP defines the embedding backend interface but does not bind a model")


class VisionModelMatcherBackend:
    """Replaceable vision-model backend slot; intentionally unbound in P2-B MVP."""

    backend_id = "vision_model_matching"

    def score(
        self,
        crop_feature: ImageFeature,
        image_index: ComponentImageIndex,
    ) -> list[ComponentCandidateEvidence]:
        raise NotImplementedError("P2-B MVP defines the vision backend interface but does not bind a model")


class ComponentMatcher:
    def __init__(
        self,
        image_index: ComponentImageIndex,
        *,
        backend: ComponentMatcherBackend | None = None,
        unknown_threshold: float = 0.45,
        ambiguity_margin: float = 0.025,
    ) -> None:
        self.image_index = image_index
        self.backend = backend or TemplateMatcherBackend()
        self.unknown_threshold = float(unknown_threshold)
        self.ambiguity_margin = float(ambiguity_margin)

    def match(self, image_crop: Path | str, top_k: int = 5, crop_id: str | None = None) -> dict[str, Any]:
        crop_path = Path(image_crop)
        stable_crop_id = crop_id or crop_path.stem or "crop"
        bounded_top_k = max(1, min(int(top_k), 10))
        warnings: list[str] = []

        if not self.image_index.matchable_entries:
            return self._unknown_response(
                stable_crop_id,
                bounded_top_k,
                failure_classification="IMAGE_INDEX_ERROR",
                warnings=["NO_MATCHABLE_IMAGE_REFERENCES"],
            )

        try:
            crop_feature = extract_image_feature(crop_path)
        except ImageDecodeError as exc:
            return self._unknown_response(
                stable_crop_id,
                bounded_top_k,
                failure_classification="INPUT_FORMAT_ERROR",
                warnings=[str(exc)],
            )

        if crop_feature.empty:
            return self._unknown_response(
                stable_crop_id,
                bounded_top_k,
                failure_classification="INPUT_FORMAT_ERROR",
                warnings=["EMPTY_IMAGE"],
            )

        try:
            raw_evidence = self.backend.score(crop_feature, self.image_index)
        except Exception as exc:  # noqa: BLE001 - classify backend failures for callers.
            return self._unknown_response(
                stable_crop_id,
                bounded_top_k,
                failure_classification="MATCHER_LOGIC_ERROR",
                warnings=[str(exc)],
            )

        if not raw_evidence:
            return self._unknown_response(
                stable_crop_id,
                bounded_top_k,
                failure_classification="IMAGE_INDEX_ERROR",
                warnings=["BACKEND_RETURNED_NO_EVIDENCE"],
            )

        sorted_evidence = sorted(
            raw_evidence,
            key=lambda item: (
                -_confidence_sort_value(item.raw_score),
                -round(item.raw_score, 6),
                item.component.component_id,
            ),
        )
        top_evidence = sorted_evidence[:bounded_top_k]
        top1_score = top_evidence[0].raw_score

        if top1_score < self.unknown_threshold:
            return self._unknown_response(
                stable_crop_id,
                bounded_top_k,
                failure_classification="UNKNOWN_THRESHOLD_ERROR",
                warnings=[
                    f"TOP1_BELOW_THRESHOLD:{round(top1_score, 3)}<{round(self.unknown_threshold, 3)}"
                ],
            )

        status = "MATCHED"
        if len(top_evidence) > 1 and top1_score - top_evidence[1].raw_score <= self.ambiguity_margin:
            status = "AMBIGUOUS"

        candidates = [
            self._candidate_from_evidence(item, rank)
            for rank, item in enumerate(top_evidence, start=1)
        ]
        return {
            "crop_id": stable_crop_id,
            "status": status,
            "candidates": candidates,
            "authority_flags": dict(AUTHORITY_FLAGS),
            "matcher_trace": {
                "backend_id": self.backend.backend_id,
                "failure_classification": None,
                "warnings": warnings,
                "top_k_requested": top_k,
                "top_k_returned": len(candidates),
                "unknown_threshold": round(self.unknown_threshold, 3),
                "confidence_is_probability": False,
            },
        }

    def _candidate_from_evidence(self, evidence: ComponentCandidateEvidence, rank: int) -> dict[str, Any]:
        entry = evidence.component
        return {
            "component_id": entry.component_id,
            "label": entry.label,
            "category": entry.category,
            "rank": rank,
            "confidence_level": confidence_level(evidence.raw_score),
            "evidence": {
                "visual_similarity": evidence.visual_similarity,
                "source_image_reference": entry.image_path or "",
                "notes": evidence.notes,
            },
        }

    def _unknown_response(
        self,
        crop_id: str,
        top_k: int,
        *,
        failure_classification: str,
        warnings: list[str],
    ) -> dict[str, Any]:
        if failure_classification not in FAILURE_CLASSIFICATIONS:
            failure_classification = "MATCHER_LOGIC_ERROR"
        return {
            "crop_id": crop_id,
            "status": "UNKNOWN_COMPONENT",
            "candidates": [],
            "authority_flags": dict(AUTHORITY_FLAGS),
            "matcher_trace": {
                "backend_id": self.backend.backend_id,
                "failure_classification": failure_classification,
                "warnings": warnings,
                "top_k_requested": top_k,
                "top_k_returned": 0,
                "unknown_threshold": round(self.unknown_threshold, 3),
                "confidence_is_probability": False,
            },
        }


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ComponentMatcherError(f"JSON root must be object: {path}")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_png_dimensions(path: Path | str) -> dict[str, int]:
    image_path = Path(path)
    data = image_path.read_bytes()
    if len(data) < 33 or not data.startswith(PNG_SIGNATURE):
        raise ImageDecodeError(f"INVALID_PNG:{image_path}")
    if data[12:16] != b"IHDR":
        raise ImageDecodeError(f"PNG_MISSING_IHDR:{image_path}")
    width, height = struct.unpack(">II", data[16:24])
    return {"width": int(width), "height": int(height)}


def read_png_grayscale(path: Path | str) -> GrayscaleImage:
    image_path = Path(path)
    data = image_path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ImageDecodeError(f"INVALID_PNG:{image_path}")

    offset = len(PNG_SIGNATURE)
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    while offset + 8 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        payload_start = offset + 8
        payload_end = payload_start + length
        if payload_end + 4 > len(data):
            raise ImageDecodeError(f"TRUNCATED_PNG_CHUNK:{image_path}")
        payload = data[payload_start:payload_end]
        offset = payload_end + 4
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(">IIBBBBB", payload)
        elif kind == b"IDAT":
            idat.extend(payload)
        elif kind == b"IEND":
            break

    if width is None or height is None or bit_depth is None or color_type is None:
        raise ImageDecodeError(f"PNG_MISSING_IHDR:{image_path}")
    if bit_depth != 8:
        raise ImageDecodeError(f"UNSUPPORTED_PNG_BIT_DEPTH:{bit_depth}")
    if interlace != 0:
        raise ImageDecodeError("UNSUPPORTED_INTERLACED_PNG")

    channels_by_type = {0: 1, 2: 3, 4: 2, 6: 4}
    if color_type not in channels_by_type:
        raise ImageDecodeError(f"UNSUPPORTED_PNG_COLOR_TYPE:{color_type}")
    channels = channels_by_type[color_type]
    row_length = width * channels
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ImageDecodeError(f"PNG_ZLIB_ERROR:{exc}") from exc

    expected = (row_length + 1) * height
    if len(raw) < expected:
        raise ImageDecodeError(f"PNG_PIXEL_DATA_TOO_SHORT:{image_path}")

    rows: list[bytearray] = []
    cursor = 0
    previous = bytearray(row_length)
    for _row_index in range(height):
        filter_type = raw[cursor]
        cursor += 1
        scanline = bytearray(raw[cursor : cursor + row_length])
        cursor += row_length
        reconstructed = _unfilter_scanline(scanline, previous, channels, filter_type)
        rows.append(reconstructed)
        previous = reconstructed

    pixels: list[int] = []
    for row in rows:
        for x in range(width):
            idx = x * channels
            if color_type == 0:
                gray = row[idx]
            elif color_type == 2:
                gray = _rgb_to_gray(row[idx], row[idx + 1], row[idx + 2])
            elif color_type == 4:
                gray = _composite_on_white(row[idx], row[idx + 1])
            else:
                gray = _composite_on_white(_rgb_to_gray(row[idx], row[idx + 1], row[idx + 2]), row[idx + 3])
            pixels.append(gray)
    return GrayscaleImage(width=int(width), height=int(height), pixels=tuple(pixels))


def _unfilter_scanline(scanline: bytearray, previous: bytearray, bpp: int, filter_type: int) -> bytearray:
    result = bytearray(len(scanline))
    for i, value in enumerate(scanline):
        left = result[i - bpp] if i >= bpp else 0
        up = previous[i] if previous else 0
        up_left = previous[i - bpp] if previous and i >= bpp else 0
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
            raise ImageDecodeError(f"UNSUPPORTED_PNG_FILTER:{filter_type}")
        result[i] = (value + predictor) & 0xFF
    return result


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _rgb_to_gray(red: int, green: int, blue: int) -> int:
    return max(0, min(255, int(round(0.299 * red + 0.587 * green + 0.114 * blue))))


def _composite_on_white(gray: int, alpha: int) -> int:
    return max(0, min(255, int(round((gray * alpha + 255 * (255 - alpha)) / 255))))


def extract_image_feature(path: Path | str, *, grid_size: int = 32) -> ImageFeature:
    image = read_png_grayscale(path)
    ink_points = [
        (idx % image.width, idx // image.width)
        for idx, value in enumerate(image.pixels)
        if value < 245
    ]
    if not ink_points:
        return ImageFeature(
            width=image.width,
            height=image.height,
            grid=tuple(0.0 for _ in range(grid_size * grid_size)),
            dhash=0,
            ink_ratio=0.0,
            aspect_ratio=1.0,
            empty=True,
        )

    xs = [point[0] for point in ink_points]
    ys = [point[1] for point in ink_points]
    left, right = min(xs), max(xs)
    top, bottom = min(ys), max(ys)
    box_width = max(1, right - left + 1)
    box_height = max(1, bottom - top + 1)
    side = max(box_width, box_height)
    center_x = (left + right + 1) / 2
    center_y = (top + bottom + 1) / 2
    square_left = center_x - side / 2
    square_top = center_y - side / 2

    grid: list[float] = []
    for gy in range(grid_size):
        for gx in range(grid_size):
            src_x = int(square_left + (gx + 0.5) * side / grid_size)
            src_y = int(square_top + (gy + 0.5) * side / grid_size)
            if 0 <= src_x < image.width and 0 <= src_y < image.height:
                gray = image.pixels[src_y * image.width + src_x]
            else:
                gray = 255
            grid.append(round((255 - gray) / 255, 6))

    return ImageFeature(
        width=image.width,
        height=image.height,
        grid=tuple(grid),
        dhash=_dhash_from_grid(grid, grid_size),
        ink_ratio=len(ink_points) / (image.width * image.height),
        aspect_ratio=box_width / box_height,
        empty=False,
    )


def _dhash_from_grid(grid: list[float], grid_size: int) -> int:
    bits = 0
    for row in range(8):
        src_y = int((row + 0.5) * grid_size / 8)
        for col in range(8):
            left_x = int((col + 0.5) * grid_size / 9)
            right_x = int((col + 1.5) * grid_size / 9)
            left = grid[src_y * grid_size + left_x]
            right = grid[src_y * grid_size + min(right_x, grid_size - 1)]
            bits = (bits << 1) | int(left > right)
    return bits


def compare_features(crop: ImageFeature, reference: ImageFeature) -> float:
    if crop.empty or reference.empty:
        return 0.0
    cosine = _cosine_similarity(crop.grid, reference.grid)
    dhash = _hash_similarity(crop.dhash, reference.dhash)
    aspect = _aspect_similarity(crop.aspect_ratio, reference.aspect_ratio)
    ink = max(0.0, 1.0 - min(1.0, abs(crop.ink_ratio - reference.ink_ratio) / max(crop.ink_ratio, reference.ink_ratio, 0.001)))
    score = 0.72 * cosine + 0.14 * dhash + 0.10 * aspect + 0.04 * ink
    return max(0.0, min(1.0, score))


def _cosine_similarity(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norm_left = math.sqrt(sum(a * a for a in left))
    norm_right = math.sqrt(sum(b * b for b in right))
    if norm_left == 0 or norm_right == 0:
        return 0.0
    return dot / (norm_left * norm_right)


def _hash_similarity(left: int, right: int) -> float:
    return 1.0 - (bin(left ^ right).count("1") / 64)


def _aspect_similarity(left: float, right: float) -> float:
    if left <= 0 or right <= 0:
        return 0.0
    return max(0.0, 1.0 - min(1.0, abs(math.log(left / right))))


def confidence_level(score: float) -> str:
    if score >= 0.88:
        return "HIGH"
    if score >= 0.65:
        return "MEDIUM"
    return "LOW"


def _confidence_sort_value(score: float) -> int:
    return {"HIGH": 3, "MEDIUM": 2, "LOW": 1}[confidence_level(score)]


def load_default_matcher(
    *,
    index_path: Path | str = DEFAULT_INDEX,
    repo_root: Path | str = REPO_ROOT,
    unknown_threshold: float = 0.45,
) -> ComponentMatcher:
    return ComponentMatcher(
        ComponentImageIndex.from_file(index_path, repo_root=repo_root),
        unknown_threshold=unknown_threshold,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Match one component crop against the component visual index.")
    parser.add_argument("image_crop")
    parser.add_argument("--index", default=str(DEFAULT_INDEX))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--crop-id")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--unknown-threshold", type=float, default=0.45)
    args = parser.parse_args(argv)

    matcher = load_default_matcher(
        index_path=args.index,
        repo_root=args.repo_root,
        unknown_threshold=args.unknown_threshold,
    )
    result = matcher.match(args.image_crop, crop_id=args.crop_id, top_k=args.top_k)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
