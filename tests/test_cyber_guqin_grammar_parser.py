import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class GrammarParserTargetedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts.cyber_guqin_grammar_parser import GrammarParser

        cls.GrammarParser = GrammarParser

    def parser(self, *, allow_abstract_component_ids=True):
        return self.GrammarParser.from_repo_root(
            ROOT,
            allow_abstract_component_ids=allow_abstract_component_ids,
        )

    def token(self, token_id, index, component_id, label, lexical_type, **extra):
        token = {
            "token_id": token_id,
            "sequence_index": index,
            "component_id_v0_2": component_id,
            "label_zh": label,
            "lexical_component_type": lexical_type,
            "normalization_status": extra.pop("normalization_status", "ABSTRACT_PRIMARY"),
            "source_component_id": extra.pop("source_component_id", None),
            "legacy_component_id": extra.pop("legacy_component_id", None),
            "semantic_role_hint": extra.pop("semantic_role_hint", None),
            "relation_to_previous": extra.pop("relation_to_previous", None),
            "relation_to_next": extra.pop("relation_to_next", None),
            "metadata": extra.pop("metadata", {}),
        }
        token.update(extra)
        return token

    def test_runtime_projection_files_load(self):
        parser = self.parser()
        self.assertEqual("P1_GRAMMAR_PARSER_MVP", parser.runtime_contract["runtime_contract_id"])
        self.assertIn("PR-RH-STRING", parser.rule_by_id)
        self.assertIn("HARD_REJECT", parser.guard_actions)

    def test_input_contract_invalid_for_empty_input(self):
        result = self.parser().parse([])
        self.assertEqual("INPUT_CONTRACT_INVALID", result["parse_status"])
        self.assertEqual([], result["accepted_candidates"])
        self.assertTrue(result["input_contract_errors"])

    def test_default_mode_rejects_abstract_component_ids(self):
        tokens = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        result = self.parser(allow_abstract_component_ids=False).parse(tokens)
        self.assertEqual("COMPONENT_ID_NORMALIZATION_GAP", result["parse_status"])

    def test_rh_string_without_context_is_ambiguous_not_san_default(self):
        tokens = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        result = self.parser().parse(tokens)
        self.assertEqual("VALID_AMBIGUOUS", result["parse_status"])
        candidate = result["accepted_candidates"][0]
        self.assertEqual(["PR-RH-STRING"], candidate["applied_rule_ids"])
        self.assertIsNone(candidate["sound_type_candidate"])
        self.assertEqual("AMBIGUOUS", candidate["sound_type_resolution_status"])
        self.assertIn("open_string_candidate", json.dumps(candidate["structured_parse"], ensure_ascii=False))

    def test_rh_string_no_inherited_context_resolves_to_open_string(self):
        tokens = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-ONE", "一", "NUMERIC_COMPONENT"),
        ]
        result = self.parser().parse(tokens, context_input={"no_inherited_context": True})
        self.assertEqual("VALID_COMPLETE", result["parse_status"])
        candidate = result["accepted_candidates"][0]
        self.assertEqual("散", candidate["sound_type_candidate"])
        self.assertEqual("RESOLVED", candidate["sound_type_resolution_status"])

    def test_explicit_context_yields_valid_with_context(self):
        tokens = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-THREE", "三", "NUMERIC_COMPONENT"),
        ]
        context = {
            "context_ref": "CTX-UNIT",
            "context_required": True,
            "inherited_context": {
                "LEFT_FINGER": "abstract_left_finger",
                "HUI_POSITION": "abstract_hui",
                "SOUND_STATE": "按",
            },
        }
        result = self.parser().parse(tokens, context_input=context)
        self.assertEqual("VALID_WITH_CONTEXT", result["parse_status"])
        self.assertEqual("PR-RH-STRING-CONTEXT", result["accepted_candidates"][0]["applied_rule_ids"][0])

    def test_all_production_families_are_reachable(self):
        p = self.parser()
        cases = {
            "PR-LF-HUI-RH-STRING": [
                self.token("lf", 0, "ABS-LF-MING", "名指", "LEFT_FINGER_NAME_COMPONENT"),
                self.token("hui", 1, "ABS-NUM-SEVEN", "七", "NUMERIC_COMPONENT"),
                self.token("rh", 2, "ABS-RH-TIAO", "挑", "RIGHT_HAND_ACTION_COMPONENT"),
                self.token("str", 3, "ABS-NUM-SIX", "六", "NUMERIC_COMPONENT"),
            ],
            "PR-STATE-START": [
                self.token("state", 0, "ABS-STATE-FANQI", "泛起", "STATE_MARKER_COMPONENT", semantic_role_hint="STATE_START")
            ],
            "PR-STATE-END": [
                self.token("state", 0, "ABS-STATE-FANZHI", "泛止", "STATE_MARKER_COMPONENT", semantic_role_hint="STATE_END")
            ],
            "PR-TIMING": [
                self.token("timing", 0, "ABS-TIME-SHAOXI", "少息", "TIMING_MARKER_COMPONENT")
            ],
            "PR-PRE-MOTION": [
                self.token("motion", 0, "ABS-LH-CHUO", "绰", "LEFT_HAND_ACTION_COMPONENT", semantic_role_hint="PRE_SOUND_MOTION"),
                self.token("lf", 1, "ABS-LF-MING", "名指", "LEFT_FINGER_NAME_COMPONENT"),
                self.token("hui", 2, "ABS-NUM-SEVEN", "七", "NUMERIC_COMPONENT"),
                self.token("rh", 3, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
                self.token("str", 4, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
            ],
            "PR-POST-MOTION": [
                self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
                self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
                self.token("motion", 2, "ABS-LH-UP", "上", "LEFT_HAND_ACTION_COMPONENT", semantic_role_hint="POST_SOUND_MOTION"),
            ],
            "PR-SPECIAL-TECHNIQUE": [
                self.token("special", 0, "ABS-SPEC-QIAQI", "掐起", "SPECIAL_TECHNIQUE_COMPONENT", semantic_role_hint="SPECIAL_TECHNIQUE")
            ],
            "PR-GENERIC-MARKER": [
                self.token(
                    "mark",
                    0,
                    "ABS-GEN-PUNCT",
                    "句",
                    "GENERIC_MARKER_COMPONENT",
                    semantic_role_hint="punctuation",
                    metadata={"registered_subtype": "punctuation", "behavior_whitelisted": True},
                )
            ],
            "PR-UNKNOWN": [
                self.token("unk", 0, "ABS-UNKNOWN", "未知", "UNKNOWN_COMPONENT")
            ],
        }
        context = {
            "context_ref": "CTX-HOST",
            "inherited_context": {"LEFT_FINGER": "abstract_left_finger", "HUI_POSITION": "abstract_hui", "SOUND_STATE": "按"},
            "context_required": True,
        }
        seen = {"PR-RH-STRING", "PR-RH-STRING-CONTEXT"}
        for rule_id, tokens in cases.items():
            result = p.parse(tokens, context_input=context if rule_id in {"PR-POST-MOTION", "PR-SPECIAL-TECHNIQUE"} else None)
            payload = json.dumps(result, ensure_ascii=False)
            self.assertIn(rule_id, payload)
            seen.add(rule_id)
        self.assertEqual(set(p.rule_by_id), seen)

    def test_dynamic_fixture_runner_passes_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "fixture_results.json"
            result = subprocess.run(
                [
                    PYTHON,
                    str(ROOT / "scripts" / "run_cyber_guqin_grammar_fixtures.py"),
                    "--repo-root",
                    str(ROOT),
                    "--fixture-dir",
                    str(ROOT / "tests" / "fixtures" / "cyber_guqin" / "component_guided_transcription"),
                    "--output",
                    str(output),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(0, payload["fail_count"])
            self.assertGreater(payload["discovered_fixture_count"], 0)
            self.assertGreater(payload["discovered_case_count"], 0)
            self.assertFalse(payload["fixed_case_count_detected"])
            self.assertFalse(payload["case_id_hardcoding_detected"])
            self.assertFalse(payload["oracle_leakage_detected"])


if __name__ == "__main__":
    unittest.main()
