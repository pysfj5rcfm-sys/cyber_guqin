import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GrammarParserMetamorphicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts.cyber_guqin_grammar_parser import GrammarParser

        cls.GrammarParser = GrammarParser

    def parser(self):
        return self.GrammarParser.from_repo_root(ROOT, allow_abstract_component_ids=True)

    def token(self, token_id, index, component_id, label, lexical_type, **extra):
        token = {
            "token_id": token_id,
            "sequence_index": index,
            "component_id_v0_2": component_id,
            "label_zh": label,
            "lexical_component_type": lexical_type,
            "normalization_status": "ABSTRACT_PRIMARY",
            "source_component_id": None,
            "legacy_component_id": None,
            "semantic_role_hint": extra.pop("semantic_role_hint", None),
            "relation_to_previous": None,
            "relation_to_next": None,
            "metadata": extra.pop("metadata", {}),
        }
        token.update(extra)
        return token

    def rh_string(self):
        return [
            self.token("rh", 0, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]

    def test_remove_required_string_downgrades_complete_parse(self):
        parser = self.parser()
        complete = parser.parse(self.rh_string(), context_input={"no_inherited_context": True})
        missing = parser.parse([self.rh_string()[0]], context_input={"no_inherited_context": True})
        self.assertEqual("VALID_COMPLETE", complete["parse_status"])
        self.assertNotEqual("VALID_COMPLETE", missing["parse_status"])

    def test_remove_right_hand_action_drops_sounding_parse(self):
        parser = self.parser()
        complete = parser.parse(self.rh_string(), context_input={"no_inherited_context": True})
        numeric_only = parser.parse([self.rh_string()[1]], context_input={"no_inherited_context": True})
        self.assertEqual("VALID_COMPLETE", complete["parse_status"])
        self.assertNotIn("RIGHT_HAND_ACTION", str(numeric_only.get("accepted_candidates")))

    def test_replace_rh_with_timing_marker_blocks_original_sounding_parse(self):
        parser = self.parser()
        mutated = [
            self.token("timing", 0, "ABS-TIME-SHAOXI", "少息", "TIMING_MARKER_COMPONENT"),
            self.token("num", 1, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        result = parser.parse(mutated, context_input={"no_inherited_context": True})
        self.assertNotEqual("VALID_COMPLETE", result["parse_status"])

    def test_add_unknown_token_is_not_silently_ignored(self):
        parser = self.parser()
        tokens = self.rh_string() + [
            self.token("unk", 2, "ABS-UNKNOWN", "未知", "UNKNOWN_COMPONENT")
        ]
        result = parser.parse(tokens, context_input={"no_inherited_context": True})
        self.assertIn("unk", result["unconsumed_tokens"])
        self.assertNotEqual("VALID_COMPLETE", result["parse_status"])

    def test_add_explicit_context_changes_rh_string_status(self):
        parser = self.parser()
        no_context = parser.parse(self.rh_string())
        with_context = parser.parse(
            self.rh_string(),
            context_input={
                "context_ref": "CTX",
                "context_required": True,
                "inherited_context": {"LEFT_FINGER": "lf", "HUI_POSITION": "hui", "SOUND_STATE": "按"},
            },
        )
        self.assertEqual("VALID_AMBIGUOUS", no_context["parse_status"])
        self.assertEqual("VALID_WITH_CONTEXT", with_context["parse_status"])

    def test_declare_no_inherited_context_resolves_rh_string_to_san(self):
        parser = self.parser()
        ambiguous = parser.parse(self.rh_string())
        resolved = parser.parse(self.rh_string(), context_input={"no_inherited_context": True})
        self.assertEqual("VALID_AMBIGUOUS", ambiguous["parse_status"])
        self.assertEqual("VALID_COMPLETE", resolved["parse_status"])
        self.assertEqual("散", resolved["accepted_candidates"][0]["sound_type_candidate"])

    def test_reverse_motion_attachment_does_not_preserve_legal_result(self):
        parser = self.parser()
        legal = [
            self.token("motion", 0, "ABS-LH-CHUO", "绰", "LEFT_HAND_ACTION_COMPONENT", semantic_role_hint="PRE_SOUND_MOTION"),
            self.token("lf", 1, "ABS-LF-MING", "名指", "LEFT_FINGER_NAME_COMPONENT"),
            self.token("hui", 2, "ABS-NUM-SEVEN", "七", "NUMERIC_COMPONENT"),
            self.token("rh", 3, "ABS-RH-GOU", "勾", "RIGHT_HAND_ACTION_COMPONENT"),
            self.token("str", 4, "ABS-NUM-FOUR", "四", "NUMERIC_COMPONENT"),
        ]
        reversed_order = [dict(t, sequence_index=i) for i, t in enumerate(legal[1:] + legal[:1])]
        self.assertEqual("VALID_COMPLETE", parser.parse(legal)["parse_status"])
        self.assertNotEqual("VALID_COMPLETE", parser.parse(reversed_order)["parse_status"])

    def test_scope_mismatched_guard_is_not_applicable(self):
        parser = self.parser()
        result = parser.parse(
            [
                self.token(
                    "mark",
                    0,
                    "ABS-GEN-JIU",
                    "就",
                    "GENERIC_MARKER_COMPONENT",
                    semantic_role_hint="context_marker",
                    metadata={"registered_subtype": "context_marker", "behavior_whitelisted": True},
                )
            ],
            context_input={"d3a_guard_ref": "FORBID-SHAOXI-AS-JIU", "scope_match": False},
        )
        self.assertEqual("VALID_COMPLETE", result["parse_status"])
        self.assertIn("NOT_APPLICABLE", result["guard_summary"]["guard_actions"])


if __name__ == "__main__":
    unittest.main()
