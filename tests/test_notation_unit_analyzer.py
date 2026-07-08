import copy
import tempfile
import unittest
from pathlib import Path

from scripts.notation_unit_analyzer import NotationUnitAnalyzer, validate_visual_slot_lattice


class FakeComponentMatcher:
    def __init__(self, payloads):
        self.payloads = payloads
        self.calls = []

    def match(self, crop, top_k=5, crop_id=None, grammar_context=None):
        self.calls.append(
            {
                "crop": Path(crop).name,
                "top_k": top_k,
                "crop_id": crop_id,
                "grammar_context": grammar_context,
            }
        )
        payload = self.payloads.get(crop_id)
        if payload is None:
            return {
                "crop_id": crop_id,
                "status": "UNKNOWN_COMPONENT",
                "candidates": [],
                "unknown_component_state": {
                    "status": "UNKNOWN_COMPONENT",
                    "unresolved_reason": "UNKNOWN_COMPONENT",
                    "needs_human_review": True,
                },
            }
        result = copy.deepcopy(payload)
        result["crop_id"] = crop_id
        return result


def candidate_set(component_id, label, lexical_type="UNKNOWN_COMPONENT", score=0.91):
    return {
        "status": "MATCHED",
        "candidates": [
            {
                "component_id": component_id,
                "label": label,
                "category": "test_component_family",
                "lexical_component_type": lexical_type,
                "visual_score": score,
                "rank": 0,
                "evidence": {"fixture": True},
                "score_breakdown": {
                    "visual": score,
                    "lexical": 1.0,
                    "grammar": 0.6,
                    "uncertainty_penalty": 0.0,
                    "final": score,
                },
            }
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


def write_outline_pgm(path, width, height, outline, inner):
    x0, y0, x1, y1 = outline
    rectangles = [
        (x0, y0, x1, y0 + 2),
        (x0, y1 - 2, x1, y1),
        (x0, y0, x0 + 2, y1),
        (x1 - 2, y0, x1, y1),
        inner,
    ]
    write_pgm(path, width, height, rectangles)


class NotationUnitAnalyzerTests(unittest.TestCase):
    def analyze_path(self, image_path, matcher, **options):
        analyzer = NotationUnitAnalyzer(component_matcher=matcher)
        return analyzer.analyze(
            {
                "notation_unit_id": "unit_test",
                "crop_image_reference": {
                    "path_or_uri": str(image_path),
                    "reference_type": "notation_unit_crop",
                },
                "analyzer_options": options,
            }
        )

    def test_single_component_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "single.pgm"
            write_pgm(image, 80, 80, [(30, 30, 50, 52)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-777", "大", "LEFT_FINGER_NAME_COMPONENT"),
                }
            )

            lattice = self.analyze_path(image, matcher)

        self.assertTrue(validate_visual_slot_lattice(lattice))
        self.assertEqual(lattice["status"], "RESOLVED")
        self.assertEqual(len(lattice["slots"]), 1)
        self.assertEqual(lattice["slots"][0]["slot_type"], "MIDDLE")
        self.assertNotIn("semantic_role_assigned", lattice["slots"][0])
        self.assertEqual(lattice["slots"][0]["candidates"][0]["component_id"], "COMP-777")
        self.assertNotIn("label", lattice["slots"][0]["candidates"][0])
        self.assertNotIn("semantic_role", lattice["slots"][0]["candidates"][0])
        self.assertTrue(lattice["authority_flags"]["NOT_SCORE_AUTHORITY"])
        self.assertTrue(lattice["authority_flags"]["NOT_DAPU_IR_AUTHORITY"])
        self.assertIsNone(matcher.calls[0]["grammar_context"])

    def test_two_component_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "two.pgm"
            write_pgm(image, 90, 70, [(8, 10, 28, 30), (60, 10, 78, 30)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-777", "大", "LEFT_FINGER_NAME_COMPONENT"),
                    "region_002": candidate_set("COMP-089", "九", "NUMERIC_COMPONENT"),
                }
            )

            lattice = self.analyze_path(image, matcher)

        self.assertEqual(lattice["status"], "RESOLVED")
        self.assertEqual([slot["slot_type"] for slot in lattice["slots"]], ["LEFT_UPPER", "RIGHT_UPPER"])
        relation_aliases = {(rel["from"], rel["relation"], rel["to"]) for rel in lattice["spatial_relations"]}
        self.assertIn(("region_001", "LEFT_OF", "region_002"), relation_aliases)
        self.assertIn(("region_002", "RIGHT_OF", "region_001"), relation_aliases)

    def test_multi_component_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "multi.pgm"
            write_pgm(image, 90, 90, [(8, 8, 25, 25), (58, 10, 75, 27), (36, 60, 54, 78)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-777", "大", "LEFT_FINGER_NAME_COMPONENT"),
                    "region_002": candidate_set("COMP-089", "九", "NUMERIC_COMPONENT"),
                    "region_003": candidate_set("COMP-103", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
                }
            )

            lattice = self.analyze_path(image, matcher)

        self.assertEqual(lattice["status"], "RESOLVED")
        self.assertEqual(len(lattice["slots"]), 3)
        self.assertGreaterEqual(len(lattice["spatial_relations"]), 4)
        self.assertFalse(any("semantic_role_assigned" in slot for slot in lattice["slots"]))

    def test_missing_component(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "blank.pgm"
            write_pgm(image, 70, 70, [])
            matcher = FakeComponentMatcher({})

            lattice = self.analyze_path(image, matcher, expected_slot_types=["MIDDLE"])

        self.assertEqual(lattice["status"], "UNRESOLVED")
        self.assertEqual(lattice["slots"][0]["slot_status"], "MISSING_COMPONENT")
        self.assertEqual(lattice["slots"][0]["slot_type"], "MIDDLE")
        self.assertEqual(lattice["slots"][0]["candidates"], [])
        self.assertEqual(lattice["unresolved_slots"][0]["status"], "MISSING_COMPONENT")
        self.assertEqual(matcher.calls, [])

    def test_ambiguous_slot(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "ambiguous.pgm"
            write_pgm(image, 100, 80, [(44, 8, 56, 24)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-089", "九", "NUMERIC_COMPONENT"),
                }
            )

            lattice = self.analyze_path(image, matcher, slot_ambiguity_band=0.08)

        self.assertEqual(lattice["status"], "AMBIGUOUS")
        self.assertEqual(lattice["slots"][0]["slot_status"], "AMBIGUOUS_SLOT")
        self.assertEqual(lattice["slots"][0]["slot_type_candidates"], ["LEFT_UPPER", "RIGHT_UPPER"])
        self.assertEqual(lattice["slots"][0]["candidates"][0]["component_id"], "COMP-089")
        self.assertNotIn("lexical_component_type", lattice["slots"][0]["candidates"][0])
        self.assertNotIn("semantic_role", lattice["slots"][0]["candidates"][0])

    def test_spatial_relation_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "relations.pgm"
            write_pgm(image, 90, 90, [(10, 10, 26, 26), (58, 58, 76, 76)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-777", "大", "LEFT_FINGER_NAME_COMPONENT"),
                    "region_002": candidate_set("COMP-086", "六", "NUMERIC_COMPONENT"),
                }
            )

            first = self.analyze_path(image, matcher)
            second = self.analyze_path(image, matcher)

        self.assertEqual(first["spatial_relations"], second["spatial_relations"])

    def test_required_spatial_relation_types_include_inside_and_attached(self):
        with tempfile.TemporaryDirectory() as tmp:
            inside_image = Path(tmp) / "inside.pgm"
            attached_image = Path(tmp) / "attached.pgm"
            write_outline_pgm(inside_image, 90, 90, (10, 10, 70, 62), (35, 32, 45, 42))
            write_pgm(attached_image, 70, 50, [(10, 10, 25, 25), (27, 10, 42, 25)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-777", "大", "LEFT_FINGER_NAME_COMPONENT"),
                    "region_002": candidate_set("COMP-089", "九", "NUMERIC_COMPONENT"),
                }
            )

            inside = self.analyze_path(inside_image, matcher)
            attached = self.analyze_path(attached_image, matcher, region_merge_gap_px=0)

        inside_relations = {(rel["from"], rel["relation"], rel["to"]) for rel in inside["spatial_relations"]}
        attached_relation_types = {rel["relation"] for rel in attached["spatial_relations"]}
        self.assertIn(("region_002", "INSIDE", "region_001"), inside_relations)
        self.assertIn("ATTACHED", attached_relation_types)

    def test_same_image_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "same.pgm"
            write_pgm(image, 90, 80, [(12, 12, 28, 28), (36, 48, 54, 66)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-426", "绰", "LEFT_HAND_ACTION_COMPONENT"),
                    "region_002": candidate_set("COMP-103", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
                }
            )

            analyzer = NotationUnitAnalyzer(component_matcher=matcher)
            payload = {
                "notation_unit_id": "unit_test",
                "crop_image_reference": {"path_or_uri": str(image), "reference_type": "notation_unit_crop"},
            }
            first = analyzer.analyze(payload)
            second = analyzer.analyze(payload)

        self.assertEqual(first, second)

    def test_extension_with_new_component(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "extension.pgm"
            write_pgm(image, 80, 80, [(30, 30, 50, 52)])
            matcher = FakeComponentMatcher(
                {
                    "region_001": candidate_set("COMP-999", "新", "SPECIAL_TECHNIQUE_COMPONENT"),
                }
            )

            lattice = self.analyze_path(image, matcher)

        candidate = lattice["slots"][0]["candidates"][0]
        self.assertEqual(candidate["component_id"], "COMP-999")
        self.assertNotIn("label", candidate)
        self.assertNotIn("semantic_role", candidate)
        self.assertTrue(validate_visual_slot_lattice(lattice))


if __name__ == "__main__":
    unittest.main()
