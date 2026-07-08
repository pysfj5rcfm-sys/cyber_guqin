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

from scripts.component_candidate_lattice import CandidateLattice
from scripts.component_matcher_runtime import ComponentMatcher
from scripts.component_visual_index import ComponentVisualIndex, build_component_visual_runtime_index


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


def build_matcher(root, components, *, unknown_threshold=0.45):
    registry_path = write_registry(root, components)
    index_data = build_component_visual_runtime_index(registry_path, repo_root=root)
    index = ComponentVisualIndex.from_dict(index_data, repo_root=root)
    return ComponentMatcher(index, unknown_threshold=unknown_threshold), index_data


def forbidden_keys_seen(value):
    forbidden = {"phrase", "sentence", "score_event", "dapu_ir", "structured_parse", "surface_reading_candidate"}
    seen = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in forbidden:
                seen.add(key)
            seen.update(forbidden_keys_seen(child))
    elif isinstance(value, list):
        for child in value:
            seen.update(forbidden_keys_seen(child))
    return seen


class ComponentVisualLayerTests(unittest.TestCase):
    def test_index_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("horizontal"))
            registry_path = write_registry(
                root,
                [
                    component("COMP-101", "甲", "right_hand_single_string_family", "a.png"),
                    component("COMP-102", "乙", "left_hand_base_position_family", "b.png"),
                ],
                [{"component_id": "COMP-081", "label_zh": "一", "component_family": "numeric_component_family"}],
            )

            index_data = build_component_visual_runtime_index(registry_path, repo_root=root)
            index = ComponentVisualIndex.from_dict(index_data, repo_root=root)

            self.assertEqual(index.component_index_count, 3)
            self.assertEqual(index.image_reference_count, 2)
            self.assertIn("COMP-101", index.entries_by_id)

    def test_image_reference_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            registry_path = write_registry(root, [component("COMP-101", "甲", "right_hand_single_string_family", "a.png")])

            index_data = build_component_visual_runtime_index(registry_path, repo_root=root)
            matchable = [item for item in index_data["components"] if item["normalized_reference"]["matchable"]]

            self.assertEqual(len(matchable), 1)
            self.assertTrue((root / matchable[0]["reference_path"]).is_file())
            self.assertEqual(matchable[0]["image_dimensions"], {"width": 16, "height": 16})
            self.assertEqual(len(matchable[0]["image_hash"]), 64)

    def test_same_crop_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("horizontal"))
            matcher, _index_data = build_matcher(
                root,
                [
                    component("COMP-101", "甲", "right_hand_single_string_family", "a.png"),
                    component("COMP-102", "乙", "left_hand_base_position_family", "b.png"),
                ],
            )

            first = matcher.match(root / "a.png", crop_id="crop_a", top_k=2)
            second = matcher.match(root / "a.png", crop_id="crop_a", top_k=2)

            self.assertEqual(first, second)
            self.assertEqual(first["status"], "MATCHED")
            self.assertEqual(first["candidates"][0]["component_id"], "COMP-101")
            self.assertIn("score_breakdown", first["candidates"][0])
            self.assertEqual(forbidden_keys_seen(first), set())

    def test_top_k_ordering_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("vertical"))
            matcher, _index_data = build_matcher(
                root,
                [
                    component("COMP-102", "乙", "right_hand_single_string_family", "b.png"),
                    component("COMP-101", "甲", "right_hand_single_string_family", "a.png"),
                ],
            )

            result = matcher.match(root / "a.png", crop_id="tie_crop", top_k=2)

            self.assertEqual(result["status"], "AMBIGUOUS")
            self.assertEqual([candidate["component_id"] for candidate in result["candidates"]], ["COMP-101", "COMP-102"])
            self.assertEqual([candidate["rank"] for candidate in result["candidates"]], [0, 1])

    def test_unknown_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "crop.png", glyph_rows("horizontal"))
            matcher, _index_data = build_matcher(
                root,
                [component("COMP-101", "甲", "right_hand_single_string_family", "a.png")],
                unknown_threshold=0.99,
            )

            result = matcher.match(root / "crop.png", crop_id="unknown_crop", top_k=1)

            self.assertEqual(result["status"], "UNKNOWN_COMPONENT")
            self.assertEqual(result["candidates"], [])
            self.assertEqual(result["unknown_component_state"]["status"], "UNKNOWN_COMPONENT")

    def test_empty_crop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "blank.png", glyph_rows("blank"))
            matcher, _index_data = build_matcher(root, [component("COMP-101", "甲", "right_hand_single_string_family", "a.png")])

            result = matcher.match(root / "blank.png", crop_id="blank_crop")

            self.assertEqual(result["status"], "UNKNOWN_COMPONENT")
            self.assertIn("EMPTY_IMAGE", result["matcher_trace"]["warnings"])

    def test_invalid_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            invalid = root / "invalid.png"
            invalid.write_bytes(b"not a png")
            matcher, _index_data = build_matcher(root, [component("COMP-101", "甲", "right_hand_single_string_family", "a.png")])

            result = matcher.match(invalid, crop_id="invalid_crop")

            self.assertEqual(result["status"], "UNKNOWN_COMPONENT")
            self.assertEqual(result["matcher_trace"]["failure_classification"], "INPUT_FORMAT_ERROR")

    def test_new_component_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "new.png", glyph_rows("cross"))
            matcher, index_data = build_matcher(root, [component("COMP-new", "新", "extension_family", "new.png")])

            result = matcher.match(root / "new.png", crop_id="extension_crop", top_k=1)

            self.assertEqual(index_data["component_index_count"], 1)
            self.assertEqual(result["status"], "MATCHED")
            self.assertEqual(result["candidates"][0]["component_id"], "COMP-new")

    def test_candidate_lattice_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("horizontal"))
            matcher, _index_data = build_matcher(
                root,
                [
                    component("COMP-101", "甲", "right_hand_single_string_family", "a.png"),
                    component("COMP-102", "乙", "left_hand_base_position_family", "b.png"),
                ],
            )
            result = matcher.match(root / "a.png", crop_id="crop_a", top_k=2)
            lattice = CandidateLattice()

            first = lattice.build(result, grammar_context={"allowed_lexical_types": ["RIGHT_HAND_ACTION_COMPONENT"]})
            second = lattice.build(result, grammar_context={"allowed_lexical_types": ["RIGHT_HAND_ACTION_COMPONENT"]})

            self.assertEqual(first, second)
            self.assertEqual(len(first["nodes"]), 2)
            self.assertEqual(first["nodes"][0]["component_id"], "COMP-101")
            self.assertIn("COMP-101", first["ranking"])
            self.assertEqual(forbidden_keys_seen(first), set())

    def test_candidate_count_configurable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_rgba_png(root / "a.png", glyph_rows("vertical"))
            write_rgba_png(root / "b.png", glyph_rows("horizontal"))
            write_rgba_png(root / "c.png", glyph_rows("cross"))
            matcher, _index_data = build_matcher(
                root,
                [
                    component("COMP-101", "甲", "right_hand_single_string_family", "a.png"),
                    component("COMP-102", "乙", "left_hand_base_position_family", "b.png"),
                    component("COMP-103", "丙", "left_hand_base_position_family", "c.png"),
                ],
            )

            one = matcher.match(root / "a.png", crop_id="crop_a", top_k=1)
            two = matcher.match(root / "a.png", crop_id="crop_a", top_k=2)

            self.assertEqual(len(one["candidates"]), 1)
            self.assertEqual(len(two["candidates"]), 2)


if __name__ == "__main__":
    unittest.main()
