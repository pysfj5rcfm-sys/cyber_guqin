import copy
import importlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GrammarParserPropertyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts.cyber_guqin_grammar_parser import GrammarParser
        from scripts.run_cyber_guqin_grammar_fixtures import discover_fixture_cases, run_fixtures

        cls.GrammarParser = GrammarParser
        cls.discover_fixture_cases = staticmethod(discover_fixture_cases)
        cls.run_fixtures = staticmethod(run_fixtures)

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

    def assert_token_conservation(self, result, token_ids):
        for candidate in result["accepted_candidates"]:
            consumed = candidate["consumed_token_ids"]
            unconsumed = candidate["unconsumed_token_ids"]
            self.assertEqual(len(consumed), len(set(consumed)))
            self.assertEqual(set(), set(consumed) & set(unconsumed))
            self.assertEqual(set(token_ids), set(consumed) | set(unconsumed))

    def test_determinism_and_token_conservation(self):
        tokens = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        parser = self.parser()
        first = parser.parse(tokens)
        second = parser.parse(copy.deepcopy(tokens))
        self.assertEqual(first, second)
        self.assert_token_conservation(first, ["rh", "num"])

    def test_unknown_component_never_valid_complete(self):
        result = self.parser().parse([
            self.token("unk", 0, "ABS-UNKNOWN", "未知", "UNKNOWN_COMPONENT")
        ])
        self.assertEqual("UNRESOLVED", result["parse_status"])
        self.assertFalse(any(c["status"] == "VALID_COMPLETE" for c in result["accepted_candidates"]))

    def test_marker_safety_and_sound_type_closure(self):
        parser = self.parser()
        marker_cases = [
            [self.token("state", 0, "ABS-STATE-FANQI", "泛起", "STATE_MARKER_COMPONENT", semantic_role_hint="STATE_START")],
            [self.token("timing", 0, "ABS-TIME-SHAOXI", "少息", "TIMING_MARKER_COMPONENT")],
            [self.token("generic", 0, "ABS-GEN-PUNCT", "句", "GENERIC_MARKER_COMPONENT", metadata={"registered_subtype": "punctuation", "behavior_whitelisted": True})],
        ]
        for tokens in marker_cases:
            result = parser.parse(tokens)
            self.assertNotIn("RIGHT_HAND_ACTION", json.dumps(result.get("accepted_candidates", []), ensure_ascii=False))
            for candidate in result["accepted_candidates"]:
                self.assertNotEqual("sounding_unit", candidate["parse_type"])
                self.assertIn(candidate["sound_type_candidate"], {"散", "按", "泛", None})

    def test_context_isolation_between_parse_calls(self):
        parser = self.parser()
        tokens = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        with_context = parser.parse(
            tokens,
            context_input={
                "context_ref": "CTX",
                "context_required": True,
                "inherited_context": {"LEFT_FINGER": "lf", "HUI_POSITION": "hui", "SOUND_STATE": "按"},
            },
        )
        without_context = parser.parse(tokens)
        self.assertEqual("VALID_WITH_CONTEXT", with_context["parse_status"])
        self.assertEqual("VALID_AMBIGUOUS", without_context["parse_status"])

    def test_token_id_renaming_invariance(self):
        parser = self.parser()
        original = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        renamed = [
            self.token("a", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("b", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        a = parser.parse(original)
        b = parser.parse(renamed)
        self.assertEqual(a["parse_status"], b["parse_status"])
        self.assertEqual(a["accepted_candidates"][0]["applied_rule_ids"], b["accepted_candidates"][0]["applied_rule_ids"])
        self.assertEqual(
            sorted(a["accepted_candidates"][0]["slots"]),
            sorted(b["accepted_candidates"][0]["slots"]),
        )

    def test_invalid_permutation_does_not_preserve_valid_complete_parse(self):
        parser = self.parser()
        valid = [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        reversed_tokens = [
            self.token("num", 0, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
            self.token("rh", 1, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
        ]
        ok = parser.parse(valid, context_input={"no_inherited_context": True})
        bad = parser.parse(reversed_tokens, context_input={"no_inherited_context": True})
        self.assertEqual("VALID_COMPLETE", ok["parse_status"])
        self.assertNotEqual("VALID_COMPLETE", bad["parse_status"])

    def test_parser_module_does_not_depend_on_fixtures_or_reports(self):
        module = importlib.import_module("scripts.cyber_guqin_grammar_parser")
        source = Path(module.__file__).read_text(encoding="utf-8")
        self.assertNotIn("tests/fixtures", source)
        self.assertNotIn("acceptance_matrix", source)
        self.assertNotIn("expected_", source)
        self.assertNotIn("P1B-ABS", source)
        self.assertNotIn("P1B-REAL", source)
        self.assertNotIn("P1B-GUARD", source)
        self.assertNotIn("P1B-RANK", source)

    def test_dynamic_fixture_discovery_extension(self):
        fixture_dir = ROOT / "tests" / "fixtures" / "cyber_guqin" / "component_guided_transcription"
        baseline = self.discover_fixture_cases(fixture_dir)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            src = fixture_dir / "p1b_abstract_grammar_fixtures.v0.1.json"
            dst = tmp_dir / src.name
            shutil.copy(src, dst)
            data = json.loads(dst.read_text(encoding="utf-8"))
            new_case = copy.deepcopy(data["cases"][8])
            new_case["case_id"] = "P1C-EXTENSION-NEW-CASE"
            new_case["input_tokens"][0]["token_id"] = "rh_ext"
            new_case["input_tokens"][1]["token_id"] = "num_ext"
            new_case["expected_consumed_token_ids"] = ["rh_ext", "num_ext"]
            new_case["expected_slot_bindings"]["RIGHT_HAND_ACTION"] = "rh_ext"
            new_case["expected_slot_bindings"]["STRING_NUMBER"] = "num_ext"
            data["cases"].append(new_case)
            dst.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extended = self.discover_fixture_cases(tmp_dir)
            self.assertEqual(44, len(extended))
            report = self.run_fixtures(ROOT, tmp_dir, allow_abstract_component_ids=True)
            self.assertEqual(0, report["fail_count"])
            self.assertIn("P1C-EXTENSION-NEW-CASE", report["executed_case_ids"])

    def test_combinatorial_smoke_invariants(self):
        parser = self.parser()
        report = parser.run_combinatorial_smoke(max_cases_per_family=4)
        self.assertGreater(report["generated_case_count"], 0)
        self.assertEqual([], report["invariant_failures"])
        self.assertIn("PR-RH-STRING", report["rule_family_coverage"])


if __name__ == "__main__":
    unittest.main()
