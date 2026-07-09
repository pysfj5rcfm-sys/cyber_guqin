import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NUMERIC_IDS = [f"COMP-{value:03d}" for value in range(81, 88)]
LEFT_FINGER_IDS = [f"COMP-{value:03d}" for value in range(91, 96)]
AUXILIARY_IDS = NUMERIC_IDS + LEFT_FINGER_IDS


class AuxiliaryComponentMatchabilityTests(unittest.TestCase):
    def test_auxiliary_components_are_runtime_matchable_with_reference_images(self):
        index_path = ROOT / "references" / "qxby_component_atlas" / "component_visual_runtime_index.v0.1.json"
        data = json.loads(index_path.read_text(encoding="utf-8"))
        components = {item["component_id"]: item for item in data["components"]}

        missing = sorted(set(AUXILIARY_IDS) - set(components))
        self.assertEqual(missing, [])

        for component_id in AUXILIARY_IDS:
            item = components[component_id]
            normalized = item.get("normalized_reference") or {}
            metadata = item.get("normalized_image_metadata") or {}
            image_path = item.get("image_path")
            with self.subTest(component_id=component_id):
                self.assertTrue(normalized.get("matchable"))
                self.assertTrue(metadata.get("matchable"))
                self.assertTrue(metadata.get("has_reference_image"))
                self.assertTrue(image_path)
                self.assertTrue((ROOT / image_path).is_file())

    def test_numeric_one_to_seven_are_marked_as_provisional_equivalence_references(self):
        index_path = ROOT / "references" / "qxby_component_atlas" / "component_visual_runtime_index.v0.1.json"
        data = json.loads(index_path.read_text(encoding="utf-8"))
        components = {item["component_id"]: item for item in data["components"]}

        for component_id in NUMERIC_IDS:
            normalized = components[component_id].get("normalized_reference") or {}
            with self.subTest(component_id=component_id):
                self.assertTrue(normalized.get("matchable"))
                self.assertEqual(normalized.get("reference_type"), "provisional_numeric_equivalence_reference")
                self.assertEqual(normalized.get("equivalence_scope"), "ONE_TO_SEVEN_ONLY")
                self.assertEqual(normalized.get("not_covered"), ["八", "九", "十", "十一", "十二", "十三"])

    def test_eight_to_thirteen_are_not_minted_as_primary_components_yet(self):
        registry_path = ROOT / "references" / "qxby_component_atlas" / "component_registry.reindexed.v0.2.json"
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        labels = {"八", "九", "十", "十一", "十二", "十三"}
        found = []
        for section in ("components", "auxiliary_components"):
            for item in data.get(section, []):
                label = item.get("label") or item.get("label_zh")
                if label in labels:
                    found.append((item.get("component_id"), label, section))

        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
