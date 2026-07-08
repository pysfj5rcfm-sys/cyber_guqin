import copy
import tempfile
import unittest
from pathlib import Path

from scripts.notation_unit_analyzer import NotationUnitAnalyzer, validate_visual_slot_lattice


FORBIDDEN_P2_KEYS = {
    "semantic_role",
    "semantic_role_assigned",
    "reading",
    "surface_reading",
    "surface_reading_candidate",
    "canonical_reading",
    "phrase_reading",
    "complete_reading",
    "slot_meaning",
    "dapu_ir",
    "Dapu_IR",
}

FORBIDDEN_P2_TEXT = {
    "大指",
    "九徽",
    "绰上",
    "绰上九徽",
    "勾六弦",
}


class FakeComponentMatcher:
    def __init__(self, payloads):
        self.payloads = payloads

    def match(self, crop, top_k=5, crop_id=None, grammar_context=None):
        result = copy.deepcopy(self.payloads[crop_id])
        result["crop_id"] = crop_id
        return result


def candidate_set(*candidates):
    return {
        "status": "MATCHED",
        "candidates": [
            {
                "component_id": component_id,
                "label": display_name,
                "category": "debug_display_only",
                "lexical_component_type": lexical_type,
                "visual_score": score,
                "rank": rank,
                "evidence": {"display_name": display_name},
                "score_breakdown": {"final": score},
            }
            for rank, (component_id, display_name, lexical_type, score) in enumerate(candidates)
        ],
    }


def write_pgm(path, width, height, rectangles):
    pixels = [[255 for _ in range(width)] for _ in range(height)]
    for x0, y0, x1, y1 in rectangles:
        for y in range(y0, y1):
            for x in range(x0, x1):
                pixels[y][x] = 0

    rows = ["P2", f"{width} {height}", "255"]
    rows.extend(" ".join(str(value) for value in row) for row in pixels)
    path.write_text("\n".join(rows) + "\n", encoding="ascii")


def walk_keys_and_strings(value):
    keys = set()
    strings = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            child_keys, child_strings = walk_keys_and_strings(child)
            keys.update(child_keys)
            strings.extend(child_strings)
    elif isinstance(value, list):
        for child in value:
            child_keys, child_strings = walk_keys_and_strings(child)
            keys.update(child_keys)
            strings.extend(child_strings)
    elif isinstance(value, str):
        strings.append(value)
    return keys, strings


def assert_p2_identity_only(testcase, lattice):
    keys, strings = walk_keys_and_strings(lattice)
    testcase.assertEqual(keys.intersection(FORBIDDEN_P2_KEYS), set())
    testcase.assertEqual(set(strings).intersection(FORBIDDEN_P2_TEXT), set())
    testcase.assertTrue(validate_visual_slot_lattice(lattice))

    for slot in lattice["slots"]:
        for candidate in slot["candidates"]:
            testcase.assertIn("component_id", candidate)
            testcase.assertIn("confidence", candidate)
            testcase.assertNotIn("label", candidate)
            testcase.assertNotIn("lexical_component_type", candidate)

    for candidate in lattice["p3_handoff_projection"]["component_candidates"]:
        testcase.assertEqual(
            set(candidate),
            {"slot_id", "source_region_id", "component_id", "confidence", "visual_score"},
        )


class ComponentIdentityBoundaryTests(unittest.TestCase):
    def analyze(self, rectangles, payloads):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "unit.pgm"
            write_pgm(image, 120, 100, rectangles)
            analyzer = NotationUnitAnalyzer(component_matcher=FakeComponentMatcher(payloads))
            return analyzer.analyze(
                {
                    "notation_unit_id": "unit_identity_boundary",
                    "crop_image_reference": {
                        "path_or_uri": str(image),
                        "reference_type": "notation_unit_crop",
                    },
                    "analyzer_options": {"region_merge_gap_px": 0},
                }
            )

    def test_case_1_left_finger_visual_identity_is_component_id_not_dazhi_reading(self):
        lattice = self.analyze(
            [(44, 42, 62, 62)],
            {
                "region_001": candidate_set(
                    ("COMP-091", "大指", "LEFT_FINGER_NAME_COMPONENT", 0.86),
                )
            },
        )

        assert_p2_identity_only(self, lattice)
        self.assertEqual(lattice["slots"][0]["candidates"][0]["component_id"], "COMP-091")

    def test_case_2_numeric_nine_stays_numeric_component_not_hui_reading(self):
        lattice = self.analyze(
            [(44, 42, 62, 62)],
            {
                "region_001": candidate_set(
                    ("NUM-009", "九", "NUMERIC_COMPONENT", 0.82),
                )
            },
        )

        assert_p2_identity_only(self, lattice)
        self.assertEqual(lattice["slots"][0]["candidates"][0]["component_id"], "NUM-009")

    def test_case_3_chuo_action_stays_component_identity_not_surface_phrase(self):
        lattice = self.analyze(
            [(44, 42, 62, 62)],
            {
                "region_001": candidate_set(
                    ("COMP-426", "绰", "LEFT_HAND_ACTION_COMPONENT", 0.8),
                )
            },
        )

        assert_p2_identity_only(self, lattice)
        self.assertEqual(lattice["slots"][0]["candidates"][0]["component_id"], "COMP-426")

    def test_case_4_notation_unit_outputs_multiple_component_candidates_without_surface_reading(self):
        lattice = self.analyze(
            [(8, 8, 24, 24), (58, 8, 74, 24), (10, 62, 26, 78), (58, 62, 74, 78)],
            {
                "region_001": candidate_set(
                    ("COMP-091", "大指", "LEFT_FINGER_NAME_COMPONENT", 0.86),
                    ("COMP-092", "食指", "LEFT_FINGER_NAME_COMPONENT", 0.42),
                ),
                "region_002": candidate_set(
                    ("NUM-009", "九", "NUMERIC_COMPONENT", 0.82),
                ),
                "region_003": candidate_set(
                    ("COMP-426", "绰", "LEFT_HAND_ACTION_COMPONENT", 0.8),
                ),
                "region_004": candidate_set(
                    ("COMP-103", "勾", "RIGHT_HAND_ACTION_COMPONENT", 0.79),
                ),
            },
        )

        assert_p2_identity_only(self, lattice)
        component_ids = {
            candidate["component_id"]
            for slot in lattice["slots"]
            for candidate in slot["candidates"]
        }
        self.assertEqual(component_ids, {"COMP-091", "COMP-092", "NUM-009", "COMP-426", "COMP-103"})


if __name__ == "__main__":
    unittest.main()
