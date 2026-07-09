import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from scripts.build_component_visual_index import build_component_visual_index
from scripts.component_matcher_runtime import ComponentMatcher
from scripts.component_visual_index import ComponentVisualIndex
from scripts.p2g_component_lattice_runtime import P2GComponentLatticeRuntime, validate_p2g_component_lattice


def png_chunk(kind, payload):
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def glyph_rows(kind, size=20):
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    rows = [[white for _ in range(size)] for _ in range(size)]
    if kind == "vertical":
        for y in range(3, size - 3):
            rows[y][size // 2] = black
            rows[y][size // 2 - 1] = black
    elif kind == "horizontal":
        for x in range(3, size - 3):
            rows[size // 2][x] = black
            rows[size // 2 - 1][x] = black
    else:
        raise ValueError(kind)
    return rows


def write_rgba_png(path, rows):
    height = len(rows)
    width = len(rows[0]) if rows else 0
    raw = bytearray()
    for row in rows:
        raw.append(0)
        for pixel in row:
            raw.extend(pixel)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + png_chunk(b"IDAT", zlib.compress(bytes(raw)))
        + png_chunk(b"IEND", b"")
    )


def write_source_png(path):
    white = (255, 255, 255, 255)
    rows = [[white for _ in range(60)] for _ in range(30)]
    for y, source_row in enumerate(glyph_rows("vertical")):
        for x, pixel in enumerate(source_row):
            rows[y + 4][x + 4] = pixel
    for y, source_row in enumerate(glyph_rows("horizontal")):
        for x, pixel in enumerate(source_row):
            rows[y + 4][x + 34] = pixel
    write_rgba_png(path, rows)


def write_registry(root):
    registry = {
        "registry_id": "TEST_P2G_P2B_REGISTRY",
        "components": [
            {
                "component_id": "COMP-V",
                "label_zh": "竖",
                "component_family": "debug_visual_family",
                "source_category": "debug_visual_family",
                "source_image_path_v0_1": "vertical.png",
            },
            {
                "component_id": "COMP-H",
                "label_zh": "横",
                "component_family": "debug_visual_family",
                "source_category": "debug_visual_family",
                "source_image_path_v0_1": "horizontal.png",
            },
        ],
        "auxiliary_components": [],
    }
    path = root / "component_registry.json"
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_matcher(root):
    write_rgba_png(root / "vertical.png", glyph_rows("vertical"))
    write_rgba_png(root / "horizontal.png", glyph_rows("horizontal"))
    index_data = build_component_visual_index(write_registry(root), repo_root=root)
    return ComponentMatcher(ComponentVisualIndex.from_dict(index_data, repo_root=root), unknown_threshold=0.2)


class P2GComponentLatticeRuntimeTests(unittest.TestCase):
    def test_builds_component_lattice_from_p2g_regions_without_grammar(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "notation.png"
            write_source_png(source)
            matcher = build_matcher(root)
            decomposition = {
                "notation_unit_id": "nu_adapter",
                "component_region_candidates": [
                    {
                        "region_id": "V001",
                        "node_id": "N010",
                        "visual_role": "upper_left_region",
                        "bbox": [4, 4, 20, 20],
                        "confidence": 0.84,
                    },
                    {
                        "region_id": "V002",
                        "node_id": "N011",
                        "visual_role": "upper_right_region",
                        "bbox": [34, 4, 20, 20],
                        "confidence": 0.82,
                    },
                ],
                "decomposition_trace": {
                    "source_path": str(source),
                    "p1_parse_called": False,
                    "p3_grammar_called": False,
                },
            }

            result = P2GComponentLatticeRuntime(
                matcher=matcher,
                crop_output_dir=root / "region_crops",
            ).build(decomposition, top_k=1)

            self.assertEqual(validate_p2g_component_lattice(result, return_errors=True), [])
            self.assertEqual(result["notation_unit_id"], "nu_adapter")
            self.assertEqual(result["status"], "MATCHED")
            self.assertEqual(len(result["component_candidate_sets"]), 2)
            self.assertEqual(
                [item["candidates"][0]["component_id"] for item in result["component_candidate_sets"]],
                ["COMP-V", "COMP-H"],
            )

            crop_paths = [Path(item["crop_image_reference"]["path_or_uri"]) for item in result["component_candidate_sets"]]
            self.assertTrue(all(path.is_file() for path in crop_paths))
            self.assertTrue(all(path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n") for path in crop_paths))

            lattice = result["component_candidate_lattice"]
            self.assertEqual([node["component_id"] for node in lattice["nodes"]], ["COMP-V", "COMP-H"])
            self.assertEqual(len(lattice["edges"]), 1)

            projection = result["p3_handoff_projection"]["component_candidates"]
            self.assertEqual(
                set(projection[0]),
                {"region_id", "node_id", "visual_role", "bbox", "component_id", "confidence", "visual_score"},
            )
            self.assertFalse(result["runtime_trace"]["p1_parse_called"])
            self.assertFalse(result["runtime_trace"]["p3_grammar_called"])
            self.assertTrue(result["runtime_trace"]["component_matcher_called"])
            self.assertFalse(result["runtime_trace"]["grammar_context_used"])


if __name__ == "__main__":
    unittest.main()
