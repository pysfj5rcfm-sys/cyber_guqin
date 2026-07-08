import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from scripts.visual_decomposition_runtime import (
    VisualDecomposer,
    VisualStructurePatternRegistry,
    validate_visual_decomposition,
)


def write_pgm(path, width, height, rectangles):
    pixels = [[255 for _ in range(width)] for _ in range(height)]
    for x0, y0, x1, y1 in rectangles:
        for y in range(y0, y1):
            for x in range(x0, x1):
                pixels[y][x] = 0

    rows = ["P2", f"{width} {height}", "255"]
    rows.extend(" ".join(str(value) for value in row) for row in pixels)
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def write_png(path, width, height, rectangles):
    pixels = [[255 for _ in range(width)] for _ in range(height)]
    for x0, y0, x1, y1 in rectangles:
        for y in range(y0, y1):
            for x in range(x0, x1):
                pixels[y][x] = 0

    def chunk(kind, payload):
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(row) for row in pixels)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def write_rgb_png(path, width, height, black_rectangles, red_rectangles):
    pixels = [[[255, 255, 255] for _ in range(width)] for _ in range(height)]
    for x0, y0, x1, y1 in black_rectangles:
        for y in range(y0, y1):
            for x in range(x0, x1):
                pixels[y][x] = [0, 0, 0]
    for x0, y0, x1, y1 in red_rectangles:
        for y in range(y0, y1):
            for x in range(x0, x1):
                pixels[y][x] = [255, 0, 0]

    def chunk(kind, payload):
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    raw_rows = []
    for row in pixels:
        flat = []
        for red, green, blue in row:
            flat.extend([red, green, blue])
        raw_rows.append(b"\x00" + bytes(flat))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(b"".join(raw_rows))) + chunk(b"IEND", b"")
    )


def write_nested_notation_unit(path):
    rectangles = [
        (18, 10, 46, 30),
        (66, 8, 98, 32),
        (18, 56, 34, 102),
        (62, 54, 108, 60),
        (62, 96, 108, 102),
        (62, 54, 68, 102),
        (102, 54, 108, 102),
        (80, 72, 90, 84),
    ]
    write_pgm(path, 128, 120, rectangles)


def write_fragmented_five_unit_notation(path):
    rectangles = [
        (25, 25, 64, 65),
        (42, 21, 53, 22),
        (68, 18, 126, 61),
        (82, 11, 86, 12),
        (25, 77, 42, 87),
        (23, 95, 37, 108),
        (23, 102, 49, 134),
        (19, 85, 20, 113),
        (75, 62, 115, 76),
        (56, 78, 142, 84),
        (56, 122, 142, 128),
        (56, 78, 62, 128),
        (136, 78, 142, 128),
        (118, 92, 124, 100),
        (74, 130, 95, 133),
    ]
    write_pgm(path, 150, 150, rectangles)


def collect_roles(node):
    roles = [node["visual_role"]]
    for child in node.get("children", []):
        roles.extend(collect_roles(child))
    return roles


def find_role(node, role):
    if node["visual_role"] == role:
        return node
    for child in node.get("children", []):
        found = find_role(child, role)
        if found:
            return found
    return None


class VisualDecompositionRuntimeTests(unittest.TestCase):
    def test_nested_notation_unit_returns_visual_only_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "nested.pgm"
            write_nested_notation_unit(image)

            result = VisualDecomposer().decompose(image, notation_unit_id="nu_nested")

        errors = validate_visual_decomposition(result, return_errors=True)
        self.assertEqual(errors, [])
        self.assertEqual(result["notation_unit_id"], "nu_nested")
        self.assertTrue(result["authority_flags"]["VISUAL_DECOMPOSITION_ONLY"])
        self.assertTrue(result["authority_flags"]["NOT_COMPONENT_ID_AUTHORITY"])
        self.assertFalse(result["decomposition_trace"]["p1_parse_called"])
        self.assertFalse(result["decomposition_trace"]["p2b_matcher_called"])

        candidate = result["segmentation_tree_candidates"][0]
        self.assertEqual(candidate["layout_family"], "UPPER_LOWER")
        roles = set(collect_roles(candidate["tree"]))
        self.assertIn("upper_left_region", roles)
        self.assertIn("upper_right_region", roles)
        self.assertIn("lower_left_region", roles)
        self.assertIn("lower_outer_region", roles)
        self.assertIn("lower_inner_region", roles)
        self.assertNotIn("OVER_MERGED_REGION", result["failure_flags"])

        lower_outer = find_role(candidate["tree"], "lower_outer_region")
        self.assertIsNotNone(lower_outer)
        self.assertIn("lower_inner_region", {child["visual_role"] for child in lower_outer["children"]})

        serialized = json.dumps(result, ensure_ascii=False)
        for forbidden in ("LEFT_FINGER", "HUI_POSITION", "RIGHT_HAND_ACTION", "STRING_NUMBER", "surface_reading"):
            self.assertNotIn(forbidden, serialized)
        self.assertFalse(any("component_id" in region for region in result["component_region_candidates"]))

    def test_scattered_unknown_structure_emits_review_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "scattered.pgm"
            write_pgm(
                image,
                120,
                120,
                [
                    (8, 8, 20, 20),
                    (48, 36, 60, 48),
                    (96, 82, 108, 94),
                ],
            )

            result = VisualDecomposer().decompose(image, notation_unit_id="nu_scattered")

        self.assertIn("UNKNOWN_STRUCTURE_CANDIDATE", result["failure_flags"])
        packet = result["review_packet"]
        self.assertEqual(packet["review_status"], "NEEDS_HUMAN_STRUCTURE_REVIEW")
        self.assertEqual(len(packet["proposed_regions"]), 3)
        self.assertIn("projection_peaks", packet["debug_features"])
        self.assertIn("containment_candidates", packet["debug_features"])

    def test_human_reviewed_pattern_registry_is_loaded_without_semantics(self):
        registry_payload = {
            "registry_id": "TEST_VISUAL_STRUCTURE_PATTERNS",
            "patterns": [
                {
                    "pattern_id": "VSP-TEST-ENCLOSURE-INNER",
                    "status": "HUMAN_REVIEWED_ACTIVE",
                    "layout_family": "ENCLOSURE_WITH_INNER",
                    "visual_only": True,
                    "allowed_roles": ["lower_outer_region", "lower_inner_region"],
                    "decomposition_rules": ["outer_bbox_contains_inner_bbox"],
                    "quality_metrics": {"min_coverage": 0.9},
                    "forbidden": ["INNER_COMPONENT_OUTSIDE_PARENT"],
                    "authority_flags": {
                        "NOT_COMPONENT_ID_AUTHORITY": True,
                        "NOT_GRAMMAR_AUTHORITY": True,
                        "NOT_DAPU_IR_AUTHORITY": True,
                    },
                }
            ],
        }
        registry = VisualStructurePatternRegistry.from_dict(registry_payload)

        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "nested.pgm"
            write_nested_notation_unit(image)

            result = VisualDecomposer(pattern_registry=registry).decompose(image, notation_unit_id="nu_registry")

        self.assertEqual(result["pattern_registry_trace"]["registry_id"], "TEST_VISUAL_STRUCTURE_PATTERNS")
        self.assertEqual(result["pattern_registry_trace"]["active_pattern_ids"], ["VSP-TEST-ENCLOSURE-INNER"])
        self.assertEqual(result["pattern_registry_trace"]["semantic_patterns_loaded"], 0)

    def test_fragmented_ink_regions_are_grouped_into_visual_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "fragmented.pgm"
            write_fragmented_five_unit_notation(image)

            result = VisualDecomposer().decompose(image, notation_unit_id="nu_fragmented")

        self.assertEqual(validate_visual_decomposition(result, return_errors=True), [])
        self.assertEqual(len(result["component_region_candidates"]), 5)
        self.assertEqual(result["quality_metrics"]["visual_unit_count"], 5)
        self.assertGreater(result["quality_metrics"]["raw_ink_region_count"], result["quality_metrics"]["visual_unit_count"])

        candidate = result["segmentation_tree_candidates"][0]
        self.assertEqual(candidate["layout_family"], "UPPER_MIDDLE_LOWER")
        roles = set(collect_roles(candidate["tree"]))
        self.assertIn("upper_left_region", roles)
        self.assertIn("upper_right_region", roles)
        self.assertIn("middle_region", roles)
        self.assertIn("lower_left_region", roles)
        self.assertIn("lower_right_region", roles)

    def test_default_visual_structure_registry_is_visual_only(self):
        registry_path = Path("references/qxby_component_atlas/visual_structure_patterns.v0.1.json")

        registry = VisualStructurePatternRegistry.from_file(registry_path)

        trace = registry.trace()
        self.assertEqual(trace["semantic_patterns_loaded"], 0)
        self.assertTrue(trace["visual_only"])
        self.assertGreaterEqual(len(trace["active_pattern_ids"]), 3)
        self.assertIn("VSP-UPPER-LOWER-001", trace["active_pattern_ids"])
        self.assertIn("VSP-ENCLOSURE-INNER-001", trace["active_pattern_ids"])

    def test_png_input_is_supported_without_pillow_requirement(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "nested.png"
            rectangles = [
                (18, 10, 46, 30),
                (66, 8, 98, 32),
                (18, 56, 34, 102),
                (62, 54, 108, 60),
                (62, 96, 108, 102),
                (62, 54, 68, 102),
                (102, 54, 108, 102),
                (80, 72, 90, 84),
            ]
            write_png(image, 128, 120, rectangles)

            result = VisualDecomposer().decompose(image, notation_unit_id="nu_png")

        self.assertEqual(validate_visual_decomposition(result, return_errors=True), [])
        self.assertEqual(result["decomposition_trace"]["image_size"], {"width": 128, "height": 120})
        self.assertGreaterEqual(len(result["component_region_candidates"]), 5)

    def test_rgb_png_red_review_marks_are_not_treated_as_ink(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "red_marks.png"
            write_rgb_png(
                image,
                80,
                80,
                black_rectangles=[(12, 12, 24, 24), (50, 50, 62, 62)],
                red_rectangles=[(0, 34, 80, 38), (36, 0, 40, 80)],
            )

            result = VisualDecomposer().decompose(image, notation_unit_id="nu_red_marks")

        self.assertEqual(result["quality_metrics"]["ink_region_count"], 2)
        for region in result["component_region_candidates"]:
            self.assertLess(region["bbox"][2], 30)
            self.assertLess(region["bbox"][3], 30)


if __name__ == "__main__":
    unittest.main()
