import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_component_visual_index import build_component_visual_index
from scripts.component_matcher import ComponentImageIndex, ComponentMatcher


def _png_chunk(kind, payload):
    import binascii

    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)
    )


def write_rgba_png(path, rows):
    height = len(rows)
    width = len(rows[0]) if rows else 0
    raw = bytearray()
    for row in rows:
        raw.append(0)
        for pixel in row:
            raw.extend(pixel)
    payload = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)),
            _png_chunk(b"IDAT", zlib.compress(bytes(raw))),
            _png_chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(payload)


def glyph_rows(kind, size=16):
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    rows = [[white for _ in range(size)] for _ in range(size)]
    if kind == "vertical":
        for y in range(2, size - 2):
            rows[y][size // 2] = black
            rows[y][size // 2 - 1] = black
    elif kind == "horizontal":
        for x in range(2, size - 2):
            rows[size // 2][x] = black
            rows[size // 2 - 1][x] = black
    elif kind == "cross":
        for idx in range(2, size - 2):
            rows[idx][size // 2] = black
            rows[size // 2][idx] = black
    elif kind == "blank":
        pass
    else:
        raise ValueError(kind)
    return rows


def write_registry(root, components, auxiliaries=None):
    registry = {
        "registry_id": "TEST_REGISTRY",
        "components": components,
        "auxiliary_components": auxiliaries or [],
    }
    path = root / "component_registry.json"
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def component(component_id, label, family, image_path):
    return {
        "component_id": component_id,
        "label_zh": label,
        "component_family": family,
        "source_category": family,
        "source_image_path_v0_1": image_path,
    }


class ComponentMatcherTests(unittest.TestCase):
    def test_registry_index_loading_includes_components_and_auxiliary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("horizontal"))
            registry_path = write_registry(
                root,
                [
                    component("COMP-101", "甲", "family_a", "a.png"),
                    component("COMP-102", "乙", "family_b", "b.png"),
                ],
                [
                    {
                        "component_id": "COMP-081",
                        "label_zh": "一",
                        "component_family": "numeric_component_family",
                        "category": "auxiliary_numeric_components",
                        "source_image_path_v0_1": None,
                    }
                ],
            )

            index_data = build_component_visual_index(registry_path, repo_root=root)
            index = ComponentImageIndex.from_dict(index_data, repo_root=root)

            self.assertEqual(index.component_index_count, 3)
            self.assertEqual(index.image_reference_count, 2)
            self.assertEqual(index.get("COMP-081").normalized_reference["matchable"], False)

    def test_image_reference_exists_for_matchable_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            registry_path = write_registry(root, [component("COMP-101", "甲", "family_a", "a.png")])

            index_data = build_component_visual_index(registry_path, repo_root=root)

            matchable = [item for item in index_data["components"] if item["normalized_reference"]["matchable"]]
            self.assertEqual(len(matchable), 1)
            self.assertTrue((root / matchable[0]["image_path"]).is_file())
            self.assertEqual(matchable[0]["image_dimensions"], {"width": 16, "height": 16})

    def test_same_image_returns_deterministic_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("horizontal"))
            registry_path = write_registry(
                root,
                [
                    component("COMP-101", "甲", "family_a", "a.png"),
                    component("COMP-102", "乙", "family_b", "b.png"),
                ],
            )
            matcher = ComponentMatcher(ComponentImageIndex.from_dict(build_component_visual_index(registry_path, repo_root=root), repo_root=root))

            first = matcher.match(root / "a.png", crop_id="crop_a", top_k=2)
            second = matcher.match(root / "a.png", crop_id="crop_a", top_k=2)

            self.assertEqual(first, second)
            self.assertEqual(first["status"], "MATCHED")
            self.assertEqual(first["candidates"][0]["component_id"], "COMP-101")
            self.assertEqual(first["authority_flags"]["NOT_DAPU_IR_AUTHORITY"], True)

    def test_top_k_sorting_is_deterministic_for_ties(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("vertical"))
            registry_path = write_registry(
                root,
                [
                    component("COMP-102", "乙", "family_b", "b.png"),
                    component("COMP-101", "甲", "family_a", "a.png"),
                ],
            )
            matcher = ComponentMatcher(ComponentImageIndex.from_dict(build_component_visual_index(registry_path, repo_root=root), repo_root=root))

            result = matcher.match(root / "a.png", crop_id="tie_crop", top_k=2)

            self.assertEqual(result["status"], "AMBIGUOUS")
            self.assertEqual([candidate["component_id"] for candidate in result["candidates"]], ["COMP-101", "COMP-102"])
            self.assertEqual([candidate["rank"] for candidate in result["candidates"]], [1, 2])

    def test_unknown_threshold_does_not_force_component(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "crop.png", glyph_rows("horizontal"))
            registry_path = write_registry(root, [component("COMP-101", "甲", "family_a", "a.png")])
            matcher = ComponentMatcher(
                ComponentImageIndex.from_dict(build_component_visual_index(registry_path, repo_root=root), repo_root=root),
                unknown_threshold=0.99,
            )

            result = matcher.match(root / "crop.png", crop_id="unknown_crop", top_k=1)

            self.assertEqual(result["status"], "UNKNOWN_COMPONENT")
            self.assertEqual(result["candidates"], [])
            self.assertEqual(result["matcher_trace"]["failure_classification"], "UNKNOWN_THRESHOLD_ERROR")

    def test_empty_image_returns_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "blank.png", glyph_rows("blank"))
            registry_path = write_registry(root, [component("COMP-101", "甲", "family_a", "a.png")])
            matcher = ComponentMatcher(ComponentImageIndex.from_dict(build_component_visual_index(registry_path, repo_root=root), repo_root=root))

            result = matcher.match(root / "blank.png", crop_id="blank_crop")

            self.assertEqual(result["status"], "UNKNOWN_COMPONENT")
            self.assertIn("EMPTY_IMAGE", result["matcher_trace"]["warnings"])

    def test_invalid_image_returns_input_format_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            invalid = root / "invalid.png"
            invalid.write_bytes(b"not a png")
            registry_path = write_registry(root, [component("COMP-101", "甲", "family_a", "a.png")])
            matcher = ComponentMatcher(ComponentImageIndex.from_dict(build_component_visual_index(registry_path, repo_root=root), repo_root=root))

            result = matcher.match(invalid, crop_id="invalid_crop")

            self.assertEqual(result["status"], "UNKNOWN_COMPONENT")
            self.assertEqual(result["matcher_trace"]["failure_classification"], "INPUT_FORMAT_ERROR")

    def test_new_component_registry_extension_requires_only_rebuilt_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "new.png", glyph_rows("cross"))
            registry_path = write_registry(root, [component("COMP-274", "新", "extension_family", "new.png")])
            index_data = build_component_visual_index(registry_path, repo_root=root)
            matcher = ComponentMatcher(ComponentImageIndex.from_dict(index_data, repo_root=root))

            result = matcher.match(root / "new.png", crop_id="extension_crop", top_k=1)

            self.assertEqual(index_data["component_index_count"], 1)
            self.assertEqual(result["status"], "MATCHED")
            self.assertEqual(result["candidates"][0]["component_id"], "COMP-274")


if __name__ == "__main__":
    unittest.main()
