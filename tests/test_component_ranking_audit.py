import tempfile
import unittest
from pathlib import Path

from scripts.component_ranking_audit import (
    ComponentRankingAudit,
    validate_visual_component_eval_fixture,
)


class ComponentRankingAuditTests(unittest.TestCase):
    def test_visual_component_eval_fixture_rejects_phrase_level_fields(self):
        fixture = {
            "fixture_id": "VISUAL_ONLY_BAD",
            "image_reference": {"path_or_uri": "/tmp/unit.png"},
            "notation_unit_id": "nu_bad",
            "expected_regions": [
                {
                    "region_id": "V001",
                    "visual_role": "upper_left_region",
                    "bbox": [1, 2, 3, 4],
                    "reviewed_component_id": "COMP-091",
                    "phrase_reading": "forbidden",
                    "review_purpose": "P2G_P2B_VISUAL_EVAL_ONLY",
                }
            ],
        }

        errors = validate_visual_component_eval_fixture(fixture, return_errors=True)

        self.assertIn("forbidden phrase/grammar field present: phrase_reading", errors)

    def test_audit_reports_top_k_hits_without_reading_fields(self):
        bridge_result = {
            "notation_unit_id": "nu_rank",
            "component_candidate_sets": [
                {
                    "crop_id": "V001",
                    "visual_region": {
                        "region_id": "V001",
                        "node_id": "N001",
                        "visual_role": "upper_left_region",
                        "bbox": [1, 2, 3, 4],
                    },
                    "candidates": [
                        {"component_id": "COMP-X", "score_breakdown": {"final": 0.81}, "visual_score": 0.80},
                        {"component_id": "COMP-091", "score_breakdown": {"final": 0.72}, "visual_score": 0.71},
                    ],
                },
                {
                    "crop_id": "V002",
                    "visual_region": {
                        "region_id": "V002",
                        "node_id": "N002",
                        "visual_role": "upper_right_region",
                        "bbox": [5, 2, 3, 4],
                    },
                    "candidates": [
                        {"component_id": "COMP-Y", "score_breakdown": {"final": 0.67}, "visual_score": 0.66},
                    ],
                },
            ],
        }
        fixture = {
            "fixture_id": "VISUAL_ONLY_GOOD",
            "image_reference": {"path_or_uri": "/tmp/unit.png"},
            "notation_unit_id": "nu_rank",
            "expected_regions": [
                {
                    "region_id": "V001",
                    "visual_role": "upper_left_region",
                    "bbox": [1, 2, 3, 4],
                    "reviewed_component_id": "COMP-091",
                    "review_purpose": "P2G_P2B_VISUAL_EVAL_ONLY",
                },
                {
                    "region_id": "V002",
                    "visual_role": "upper_right_region",
                    "bbox": [5, 2, 3, 4],
                    "reviewed_component_label": "九",
                    "atlas_status": "NO_INDEPENDENT_COMPONENT_ID",
                    "review_purpose": "P2G_P2B_VISUAL_EVAL_ONLY",
                },
            ],
        }

        report = ComponentRankingAudit().audit_bridge_result(bridge_result, fixture)

        self.assertEqual(report["mode"], "COMPONENT_RECALL_EVAL")
        self.assertEqual(report["summary"]["reviewed_region_count"], 1)
        self.assertEqual(report["summary"]["top3_hit_count"], 1)
        self.assertEqual(report["region_results"][0]["rank_1_based"], 2)
        self.assertEqual(report["region_results"][0]["pass_level"], "PASS_TOP3")
        self.assertEqual(report["region_results"][1]["evaluation_status"], "ATLAS_GAP")
        serialized = str(report)
        self.assertNotIn("phrase_reading", serialized)
        self.assertNotIn("surface_reading", serialized)
        self.assertNotIn("dapu_ir", serialized)

    def test_unlabeled_cross_validation_fixture_is_visual_sanity_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "unlabeled.png"
            image.write_bytes(b"not used by this unit test")
            bridge_result = {
                "notation_unit_id": "nu_cross",
                "component_candidate_sets": [
                    {
                        "crop_id": "V001",
                        "visual_region": {
                            "region_id": "V001",
                            "visual_role": "upper_left_region",
                            "bbox": [1, 1, 10, 10],
                        },
                        "candidates": [{"component_id": "COMP-001", "visual_score": 0.5}],
                    }
                ],
            }
            fixture = {
                "fixture_id": "CROSS_VISUAL_ONLY",
                "image_reference": {"path_or_uri": str(image)},
                "notation_unit_id": "nu_cross",
                "cross_validation_role": "VISUAL_SANITY_ONLY",
                "expected_regions": [],
            }

            report = ComponentRankingAudit().audit_bridge_result(bridge_result, fixture)

        self.assertEqual(report["mode"], "VISUAL_SANITY_ONLY")
        self.assertEqual(report["summary"]["reviewed_region_count"], 0)
        self.assertEqual(report["summary"]["observed_region_count"], 1)
        self.assertTrue(report["authority_flags"]["NOT_PHRASE_READING_AUTHORITY"])

    def test_matchable_false_component_is_counted_as_atlas_gap_not_matcher_miss(self):
        bridge_result = {
            "notation_unit_id": "nu_gap",
            "component_candidate_sets": [
                {
                    "crop_id": "V001",
                    "visual_region": {
                        "region_id": "V001",
                        "visual_role": "middle_region",
                        "bbox": [1, 1, 10, 10],
                    },
                    "candidates": [{"component_id": "COMP-OTHER", "visual_score": 0.7}],
                }
            ],
        }
        fixture = {
            "fixture_id": "MATCHABLE_FALSE_GAP",
            "image_reference": {"path_or_uri": "/tmp/unit.png"},
            "notation_unit_id": "nu_gap",
            "expected_regions": [
                {
                    "region_id": "V001",
                    "visual_role": "middle_region",
                    "bbox": [1, 1, 10, 10],
                    "reviewed_component_id": "COMP-087",
                    "reviewed_component_label": "七",
                    "atlas_status": "MATCHABLE_FALSE",
                    "review_purpose": "P2G_P2B_VISUAL_EVAL_ONLY",
                }
            ],
        }

        report = ComponentRankingAudit().audit_bridge_result(bridge_result, fixture)

        self.assertEqual(report["region_results"][0]["evaluation_status"], "ATLAS_GAP")
        self.assertEqual(report["summary"]["reviewed_region_count"], 0)
        self.assertEqual(report["summary"]["atlas_gap_count"], 1)
        self.assertNotIn("P2B_RECALL_MISS", report["failure_flags"])


if __name__ == "__main__":
    unittest.main()
