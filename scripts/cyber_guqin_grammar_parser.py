#!/usr/bin/env python3
"""Executable P1 local grammar parser for normalized jianzipu component tokens."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any


AUTHORITY_FLAGS = {
    "not_repo_contract": True,
    "not_canon_authority": True,
    "not_dapu_ir_authority": True,
    "not_score_event_authority": True,
    "not_sample_ingest": True,
    "not_ml_training_data": True,
    "not_render_output": True,
    "needs_human_review": True,
}

PRIMARY_LABELS = {
    "COMP-081": "一",
    "COMP-082": "二",
    "COMP-083": "三",
    "COMP-084": "四",
    "COMP-085": "五",
    "COMP-086": "六",
    "COMP-087": "七",
}

CONTEXT_KEYS = {"LEFT_FINGER", "HUI_POSITION", "SOUND_STATE"}
VALID_SOUNDS = {"散", "按", "泛", None}
CORE_TOKEN_FIELDS = {
    "token_id",
    "sequence_index",
    "component_id_v0_2",
    "label_zh",
    "lexical_component_type",
    "normalization_status",
}
OPTIONAL_AUDIT_FIELDS = {"source_category", "confidence_input"}
ID_RE = re.compile(r"^(COMP-[0-9]{3}|ABS-[A-Z0-9-]+)$")


class ParserLoadError(RuntimeError):
    """Raised when the parser runtime reference files are missing or malformed."""


@dataclass(frozen=True)
class TokenView:
    raw: dict[str, Any]
    token_id: str
    sequence_index: int
    component_id: str | None
    label: str
    lexical_type: str
    semantic_hint: str | None
    metadata: dict[str, Any]
    normalized_component_id: str | None
    normalization_status: str
    normalization_trace: dict[str, Any]


def load_default_parser(repo_root: Path) -> "GrammarParser":
    return GrammarParser.from_repo_root(repo_root)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ParserLoadError(f"missing JSON file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ParserLoadError(f"JSON root must be object: {path}")
    return data


def _sha_text(value: Any, length: int = 14) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length]


class GrammarParser:
    def __init__(
        self,
        *,
        repo_root: Path,
        runtime_contract: dict[str, Any],
        component_registry: dict[str, Any],
        alias_map: dict[str, Any],
        canon_crosswalk: dict[str, Any],
        guard_projection: dict[str, Any],
        allow_abstract_component_ids: bool,
    ) -> None:
        self.repo_root = repo_root
        self.runtime_contract = runtime_contract
        self.component_registry = component_registry
        self.alias_map = alias_map
        self.canon_crosswalk = canon_crosswalk
        self.guard_projection = guard_projection
        self.allow_abstract_component_ids = allow_abstract_component_ids

        self.rule_by_id = {
            item["rule_id"]: item
            for item in runtime_contract.get("production_rules", [])
            if isinstance(item, dict) and item.get("rule_id")
        }
        self.rule_order = list(runtime_contract.get("rule_ordering", {}).get("production_priority", self.rule_by_id))
        self.parser_statuses = set(runtime_contract.get("parser_statuses", []))
        self.lexical_types = set(runtime_contract.get("lexical_types", []))
        self.guard_actions = set(runtime_contract.get("guard_actions", []))
        self.component_by_id = self._index_components(component_registry)
        self.legacy_to_primary, self.source_to_primary = self._index_aliases(alias_map)
        self.guard_by_id = {
            item["guard_id"]: item
            for item in guard_projection.get("guards", [])
            if isinstance(item, dict) and item.get("guard_id")
        }

    @classmethod
    def from_repo_root(
        cls,
        repo_root: Path,
        *,
        allow_abstract_component_ids: bool = False,
    ) -> "GrammarParser":
        root = Path(repo_root)
        ref_root = root / "references" / "qxby_component_atlas"
        return cls(
            repo_root=root,
            runtime_contract=_load_json(ref_root / "p1_grammar_runtime_contract.v0.1.json"),
            component_registry=_load_json(ref_root / "component_registry.reindexed.v0.2.json"),
            alias_map=_load_json(ref_root / "component_legacy_alias_map.reindexed.v0.2.json"),
            canon_crosswalk=_load_json(ref_root / "component_to_canon_crosswalk.seed.reindexed.v0.2.json"),
            guard_projection=_load_json(ref_root / "p1_generation_safe_guards.v0.1.json"),
            allow_abstract_component_ids=allow_abstract_component_ids,
        )

    def parse(
        self,
        tokens: list[dict[str, Any]],
        *,
        context_input: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = dict(context_input or {})
        opts = dict(options or {})
        contract_errors = self._validate_call(tokens, context_input, options)
        if contract_errors:
            return self._response(
                input_tokens=tokens if isinstance(tokens, list) else [],
                parse_status="INPUT_CONTRACT_INVALID",
                normalized_tokens=[],
                input_contract_errors=contract_errors,
                unconsumed_tokens=self._safe_token_ids(tokens),
            )

        ordered = sorted(tokens, key=lambda item: item["sequence_index"])
        normalized, gaps = self._normalize_tokens(ordered)
        if gaps:
            return self._response(
                input_tokens=ordered,
                normalized_tokens=normalized,
                parse_status="COMPONENT_ID_NORMALIZATION_GAP",
                unconsumed_tokens=[t.token_id for t in normalized],
                guard_actions=["HARD_REJECT"],
                normalization_gaps=gaps,
                rejected_candidates=[
                    self._rejected("PR-UNKNOWN", [], "COMPONENT_ID_NORMALIZATION_GAP", "component id could not normalize", ["HARD_REJECT"])
                ],
            )

        if context.get("implicit_backward_scan_depth", 0) not in (0, None):
            if [t.lexical_type for t in normalized] == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
                return self._rh_string_incomplete_or_unresolved(ordered, normalized, "UNSUPPORTED", "implicit context scan is outside P1", ["NEEDS_CONTEXT"], context)
            return self._unresolved_response(ordered, normalized, "UNSUPPORTED", "implicit context scan is outside P1", ["NEEDS_CONTEXT"], rule_id="PR-RH-STRING-CONTEXT")

        result = self._parse_normalized(ordered, normalized, context, opts)
        return result

    def run_combinatorial_smoke(self, max_cases_per_family: int = 4) -> dict[str, Any]:
        examples = {
            "RIGHT_HAND_ACTION_COMPONENT": [("COMP-103", "勾"), ("COMP-116", "挑")],
            "NUMERIC_COMPONENT": [("COMP-081", "一"), ("COMP-084", "四"), ("COMP-086", "六")],
            "LEFT_FINGER_NAME_COMPONENT": [("COMP-091", "大指"), ("COMP-094", "名指")],
            "LEFT_HAND_ACTION_COMPONENT": [("COMP-426", "绰"), ("COMP-527", "进复")],
            "STATE_MARKER_COMPONENT": [("COMP-705", "散"), ("COMP-708", "泛起")],
            "TIMING_MARKER_COMPONENT": [("COMP-806", "少息")],
            "GENERIC_MARKER_COMPONENT": [("COMP-906", "句"), ("COMP-907", "就")],
        }
        cases: list[tuple[list[dict[str, Any]], dict[str, Any] | None]] = []
        for rh, num in itertools.islice(itertools.product(examples["RIGHT_HAND_ACTION_COMPONENT"], examples["NUMERIC_COMPONENT"]), max_cases_per_family):
            cases.append(([self._smoke_token("rh", 0, rh, "RIGHT_HAND_ACTION_COMPONENT"), self._smoke_token("num", 1, num, "NUMERIC_COMPONENT")], None))
        for lf, hui, rh, string in itertools.islice(
            itertools.product(
                examples["LEFT_FINGER_NAME_COMPONENT"],
                examples["NUMERIC_COMPONENT"],
                examples["RIGHT_HAND_ACTION_COMPONENT"],
                examples["NUMERIC_COMPONENT"],
            ),
            max_cases_per_family,
        ):
            cases.append(
                (
                    [
                        self._smoke_token("lf", 0, lf, "LEFT_FINGER_NAME_COMPONENT"),
                        self._smoke_token("hui", 1, hui, "NUMERIC_COMPONENT"),
                        self._smoke_token("rh", 2, rh, "RIGHT_HAND_ACTION_COMPONENT"),
                        self._smoke_token("str", 3, string, "NUMERIC_COMPONENT"),
                    ],
                    None,
                )
            )
        for marker_type, values in [
            ("STATE_MARKER_COMPONENT", examples["STATE_MARKER_COMPONENT"]),
            ("TIMING_MARKER_COMPONENT", examples["TIMING_MARKER_COMPONENT"]),
            ("GENERIC_MARKER_COMPONENT", examples["GENERIC_MARKER_COMPONENT"]),
        ]:
            for idx, item in enumerate(values[:max_cases_per_family]):
                metadata = {"registered_subtype": "punctuation", "behavior_whitelisted": True} if marker_type == "GENERIC_MARKER_COMPONENT" else {}
                cases.append(([self._smoke_token(f"m{idx}", 0, item, marker_type, metadata=metadata)], None))
        cases.append(
            (
                [
                    self._smoke_token("motion", 0, examples["LEFT_HAND_ACTION_COMPONENT"][0], "LEFT_HAND_ACTION_COMPONENT", hint="PRE_SOUND_MOTION"),
                    self._smoke_token("lf", 1, examples["LEFT_FINGER_NAME_COMPONENT"][0], "LEFT_FINGER_NAME_COMPONENT"),
                    self._smoke_token("hui", 2, examples["NUMERIC_COMPONENT"][0], "NUMERIC_COMPONENT"),
                    self._smoke_token("rh", 3, examples["RIGHT_HAND_ACTION_COMPONENT"][0], "RIGHT_HAND_ACTION_COMPONENT"),
                    self._smoke_token("str", 4, examples["NUMERIC_COMPONENT"][1], "NUMERIC_COMPONENT"),
                ],
                None,
            )
        )
        contexts = [
            None,
            {"no_inherited_context": True},
            {"context_ref": "CTX", "context_required": True, "inherited_context": {"LEFT_FINGER": "COMP-091", "HUI_POSITION": "COMP-087", "SOUND_STATE": "按"}},
            {"context_ref": "BAD", "context_required": True, "inherited_context": {"TIMING_MARKER": "COMP-806"}},
            {"context_required": True},
        ]
        cases.extend(([
            self._smoke_token("rh", 0, examples["RIGHT_HAND_ACTION_COMPONENT"][0], "RIGHT_HAND_ACTION_COMPONENT"),
            self._smoke_token("num", 1, examples["NUMERIC_COMPONENT"][0], "NUMERIC_COMPONENT"),
        ], ctx) for ctx in contexts)

        failures: list[dict[str, Any]] = []
        rules: set[str] = set()
        lexical: set[str] = set()
        for tokens, context in cases:
            result = self.parse(tokens, context_input=context)
            for token in tokens:
                lexical.add(token["lexical_component_type"])
            for candidate in result["accepted_candidates"]:
                rules.update(candidate["applied_rule_ids"])
                consumed = candidate["consumed_token_ids"]
                unconsumed = candidate["unconsumed_token_ids"]
                ids = {t["token_id"] for t in tokens}
                if len(consumed) != len(set(consumed)) or set(consumed) & set(unconsumed) or set(consumed) | set(unconsumed) != ids:
                    failures.append({"tokens": [t["token_id"] for t in tokens], "reason": "token conservation failed"})
                if candidate.get("sound_type_candidate") not in VALID_SOUNDS:
                    failures.append({"tokens": [t["token_id"] for t in tokens], "reason": "sound type closure failed"})
        return {
            "generated_case_count": len(cases),
            "lexical_type_coverage": sorted(lexical),
            "rule_family_coverage": sorted(rules),
            "invariant_failures": failures,
        }

    def _parse_normalized(
        self,
        raw_tokens: list[dict[str, Any]],
        tokens: list[TokenView],
        context: dict[str, Any],
        options: dict[str, Any],
    ) -> dict[str, Any]:
        guard_actions = self._guard_actions_for(tokens, context)
        hard_guard = "HARD_REJECT" in guard_actions
        if hard_guard:
            rule_id = self._guess_rule_id(tokens, context)
            hard_sound = "散" if context.get("no_inherited_context") and [t.lexical_type for t in tokens] == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"] else None
            return self._response(
                input_tokens=raw_tokens,
                normalized_tokens=tokens,
                parse_status="FORBIDDEN_GUARD_REJECTED",
                unconsumed_tokens=[],
                guard_actions=guard_actions,
                rejected_candidates=[
                    self._rejected(
                        rule_id,
                        [t.token_id for t in tokens],
                        "FORBIDDEN_GUARD_REJECTED",
                        "scoped guard hard reject",
                        guard_actions,
                        sound_type=hard_sound,
                        sound_status="RESOLVED" if hard_sound else "UNRESOLVED",
                    )
                ],
            )

        if any(t.metadata.get("component_id_label_conflict") for t in tokens):
            return self._unresolved_response(raw_tokens, tokens, "UNRESOLVED", "component id and label conflict", ["FORCE_UNRESOLVED"], rule_id=self._guess_rule_id(tokens, context))

        lexical = [t.lexical_type for t in tokens]
        hints = [t.semantic_hint for t in tokens]
        token_ids = [t.token_id for t in tokens]

        if len(tokens) == 1:
            token = tokens[0]
            return self._parse_single(raw_tokens, token, context, guard_actions)

        if lexical == ["STATE_MARKER_COMPONENT", "RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
            sound = self._state_sound(tokens[0])
            candidate = self._candidate(
                rules=["PR-STATE-START", "PR-RH-STRING"],
                status="VALID_COMPLETE",
                tokens=tokens,
                consumed=token_ids,
                unconsumed=[],
                slots={
                    "STATE_START": self._slot(tokens[0]),
                    "RIGHT_HAND_ACTION": self._slot(tokens[1]),
                    "STRING_NUMBER": self._slot(tokens[2], numeric_role="string_number"),
                    "SOUND_STATE": {"value": sound, "sound_type_candidate": sound, "sound_type_resolution_status": "RESOLVED"},
                },
                parse_type="state_plus_right_hand_string_unit",
                sound_type=sound,
                sound_status="RESOLVED",
                guard_actions=guard_actions,
                reason="explicit state marker resolves local right-hand/string unit",
            )
            return self._response(raw_tokens, tokens, "VALID_COMPLETE", accepted_candidates=[candidate], guard_actions=guard_actions)

        if lexical == ["LEFT_FINGER_NAME_COMPONENT", "NUMERIC_COMPONENT", "RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
            candidate = self._pressed_candidate(tokens, guard_actions)
            return self._response(raw_tokens, tokens, "VALID_COMPLETE", accepted_candidates=[candidate], guard_actions=guard_actions)

        if lexical == ["LEFT_HAND_ACTION_COMPONENT", "LEFT_FINGER_NAME_COMPONENT", "NUMERIC_COMPONENT", "RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"] and hints[0] == "PRE_SOUND_MOTION":
            slots = {
                "PRE_SOUND_MOTION": self._slot(tokens[0]),
                "LEFT_FINGER": self._slot(tokens[1]),
                "HUI_POSITION": self._slot(tokens[2], numeric_role="hui_position"),
                "RIGHT_HAND_ACTION": self._slot(tokens[3]),
                "STRING_NUMBER": self._slot(tokens[4], numeric_role="string_number"),
                "SOUND_STATE": {"value": "按", "sound_type_candidate": "按", "sound_type_resolution_status": "RESOLVED"},
            }
            candidate = self._candidate(
                rules=["PR-PRE-MOTION", "PR-LF-HUI-RH-STRING"],
                status="VALID_COMPLETE",
                tokens=tokens,
                consumed=token_ids,
                unconsumed=[],
                slots=slots,
                parse_type="ornamented_attack",
                sound_type="按",
                sound_status="RESOLVED",
                guard_actions=guard_actions,
                reason="pre-sound motion attaches to following pressed host",
            )
            return self._response(raw_tokens, tokens, "VALID_COMPLETE", accepted_candidates=[candidate], guard_actions=guard_actions)

        if lexical == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT", "LEFT_HAND_ACTION_COMPONENT"] and hints[2] == "POST_SOUND_MOTION":
            if self._has_compatible_context(context):
                candidate = self._post_motion_candidate(tokens, context, guard_actions)
                return self._response(raw_tokens, tokens, "VALID_WITH_CONTEXT", accepted_candidates=[candidate], guard_actions=guard_actions)
            return self._unresolved_response(raw_tokens, tokens, "INCOMPLETE", "post-sound motion requires explicit host context", ["NEEDS_CONTEXT"], rule_id="PR-POST-MOTION", consumed=token_ids)

        if lexical == ["LEFT_FINGER_NAME_COMPONENT", "NUMERIC_COMPONENT"]:
            actions = self._prefer_guard(guard_actions, ["NEEDS_CONTEXT"])
            candidate = self._candidate(
                rules=["PR-LF-HUI-RH-STRING"],
                status="INCOMPLETE",
                tokens=tokens,
                consumed=token_ids,
                unconsumed=[],
                slots={
                    "LEFT_FINGER": self._slot(tokens[0]),
                    "HUI_POSITION": self._slot(tokens[1], numeric_role="hui_position"),
                    "RIGHT_HAND_ACTION": {"value": None, "missing": True},
                    "STRING_NUMBER": {"value": None, "missing": True},
                    "SOUND_STATE": {"value": None, "sound_type_candidate": None, "sound_type_resolution_status": "UNRESOLVED"},
                },
                parse_type="incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=actions,
                reason="pressed position lacks sounding action and string",
            )
            return self._response(raw_tokens, tokens, "INCOMPLETE", accepted_candidates=[candidate], guard_actions=actions)

        if lexical == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
            return self._parse_rh_string(raw_tokens, tokens, context, guard_actions)

        if lexical == ["NUMERIC_COMPONENT", "RIGHT_HAND_ACTION_COMPONENT"]:
            return self._unresolved_response(raw_tokens, tokens, "INVALID_ORDER", "string number appears before right-hand action", ["HARD_REJECT"], rule_id="PR-RH-STRING")

        if lexical == ["TIMING_MARKER_COMPONENT", "RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
            candidate = self._candidate(
                rules=["PR-TIMING", "PR-RH-STRING"],
                status="INVALID_TYPE_COMBINATION",
                tokens=tokens,
                consumed=[],
                unconsumed=token_ids,
                slots={"TIMING_MARKER": self._slot(tokens[0]), "UNRESOLVED": {"token_ids": [tokens[1].token_id, tokens[2].token_id], "value": [tokens[1].token_id, tokens[2].token_id]}},
                parse_type="incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=["HARD_REJECT"],
                reason="timing marker cannot mix into sounding slots without boundary",
            )
            return self._response(raw_tokens, tokens, "INVALID_TYPE_COMBINATION", accepted_candidates=[candidate], guard_actions=["HARD_REJECT"], unconsumed_tokens=token_ids)

        if lexical == ["RIGHT_HAND_ACTION_COMPONENT", "RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
            candidate = self._candidate(
                rules=["PR-RH-STRING"],
                status="VALID_AMBIGUOUS",
                tokens=tokens,
                consumed=[],
                unconsumed=token_ids,
                slots={"RIGHT_HAND_ACTION": {"token_ids": [tokens[0].token_id, tokens[1].token_id], "component_ids": [tokens[0].normalized_component_id, tokens[1].normalized_component_id], "value": [tokens[0].label, tokens[1].label]}, "STRING_NUMBER": self._slot(tokens[2], numeric_role="string_number")},
                parse_type="incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="AMBIGUOUS",
                guard_actions=["SOFT_PENALTY"],
                reason="multiple right-hand actions compete for one slot",
            )
            return self._response(raw_tokens, tokens, "VALID_AMBIGUOUS", accepted_candidates=[candidate], guard_actions=["SOFT_PENALTY"], unconsumed_tokens=token_ids)

        if lexical == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT", "NUMERIC_COMPONENT"]:
            if tokens[2].lexical_type == "UNKNOWN_COMPONENT":
                return self._partial_rh_string(raw_tokens, tokens, context, guard_actions)
            actions = guard_actions or ["NOT_APPLICABLE"]
            candidate = self._candidate(
                rules=["PR-RH-STRING"],
                status="VALID_AMBIGUOUS",
                tokens=tokens,
                consumed=[],
                unconsumed=token_ids,
                slots={"RIGHT_HAND_ACTION": self._slot(tokens[0]), "STRING_NUMBER": {"token_ids": [tokens[1].token_id, tokens[2].token_id], "component_ids": [tokens[1].normalized_component_id, tokens[2].normalized_component_id], "value": [tokens[1].label, tokens[2].label]}},
                parse_type="incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="AMBIGUOUS",
                guard_actions=actions,
                reason="numeric cluster cannot be collapsed into one string slot",
            )
            return self._response(raw_tokens, tokens, "VALID_AMBIGUOUS", accepted_candidates=[candidate], guard_actions=actions, unconsumed_tokens=token_ids)

        if lexical[:2] == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"] and len(tokens) > 2:
            return self._partial_rh_string(raw_tokens, tokens, context, guard_actions)

        return self._fallback(raw_tokens, tokens, context, guard_actions)

    def _parse_single(
        self,
        raw_tokens: list[dict[str, Any]],
        token: TokenView,
        context: dict[str, Any],
        guard_actions: list[str],
    ) -> dict[str, Any]:
        if token.lexical_type == "NUMERIC_COMPONENT":
            return self._unresolved_response(raw_tokens, [token], "VALID_AMBIGUOUS", "numeric role unresolved without grammar context", ["NOT_APPLICABLE"], rule_id="PR-UNKNOWN")
        if token.lexical_type == "RIGHT_HAND_ACTION_COMPONENT":
            actions = self._prefer_guard(guard_actions, ["FORCE_UNRESOLVED"] if "FORCE_UNRESOLVED" in guard_actions else ["NEEDS_CONTEXT"])
            status = "UNRESOLVED" if "FORCE_UNRESOLVED" in actions else "INCOMPLETE"
            candidate = self._candidate(
                rules=["PR-RH-STRING"],
                status=status,
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={
                    "RIGHT_HAND_ACTION": self._slot(token),
                    "STRING_NUMBER": {"value": None, "missing": True},
                    "SOUND_STATE": {"value": None, "sound_type_candidate": None, "sound_type_resolution_status": "UNRESOLVED"},
                },
                parse_type="incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=actions,
                reason="missing string number",
            )
            return self._response(raw_tokens, [token], status, accepted_candidates=[candidate], guard_actions=actions)
        if token.lexical_type == "LEFT_FINGER_NAME_COMPONENT":
            actions = self._prefer_guard(guard_actions, ["NEEDS_CONTEXT"])
            candidate = self._candidate(
                rules=["PR-LF-HUI-RH-STRING"],
                status="INCOMPLETE",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={
                    "LEFT_FINGER": self._slot(token),
                    "HUI_POSITION": {"value": None, "missing": True},
                    "RIGHT_HAND_ACTION": {"value": None, "missing": True},
                    "STRING_NUMBER": {"value": None, "missing": True},
                    "SOUND_STATE": {"value": None, "sound_type_candidate": None, "sound_type_resolution_status": "UNRESOLVED"},
                },
                parse_type="incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=actions,
                reason="left finger lacks hui and sounding action",
            )
            return self._response(raw_tokens, [token], "INCOMPLETE", accepted_candidates=[candidate], guard_actions=actions)
        if token.lexical_type == "LEFT_HAND_ACTION_COMPONENT":
            hint = token.semantic_hint
            if hint not in {"PRE_SOUND_MOTION", "POST_SOUND_MOTION"}:
                return self._unresolved_response(raw_tokens, [token], "UNRESOLVED", "left-hand action lacks P1 host role", self._prefer_guard(guard_actions, ["FORCE_UNRESOLVED"]), rule_id="PR-UNKNOWN")
            rule_id = "PR-PRE-MOTION" if hint == "PRE_SOUND_MOTION" else "PR-POST-MOTION"
            slot = "PRE_SOUND_MOTION" if hint == "PRE_SOUND_MOTION" else "POST_SOUND_MOTION"
            actions = self._prefer_guard(guard_actions, ["NEEDS_CONTEXT"])
            motion_sound_status = "CONTEXT_REQUIRED" if context.get("context_required") else "UNRESOLVED"
            candidate = self._candidate(
                rules=[rule_id],
                status="INCOMPLETE",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={slot: self._slot(token), "HOST_UNIT": {"value": None, "missing": True}},
                parse_type="motion_requires_host",
                sound_type=None,
                sound_status=motion_sound_status,
                guard_actions=actions,
                reason="motion requires explicit host unit",
            )
            return self._response(
                raw_tokens,
                [token],
                "INCOMPLETE",
                accepted_candidates=[candidate],
                guard_actions=actions,
                context_requirements=[self._context_requirement("HOST_UNIT", "motion host")],
            )
        if token.lexical_type == "STATE_MARKER_COMPONENT":
            is_end = token.semantic_hint == "STATE_END" or "止" in token.label
            rule_id = "PR-STATE-END" if is_end else "PR-STATE-START"
            slot_name = "STATE_END" if is_end else "STATE_START"
            sound = None
            candidate = self._candidate(
                rules=[rule_id],
                status="VALID_COMPLETE",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={slot_name: self._slot(token), "SOUND_STATE": {"value": sound, "sound_type_candidate": sound, "sound_type_resolution_status": "RESOLVED"}},
                parse_type="non_sounding_state_marker",
                sound_type=sound,
                sound_status="RESOLVED",
                guard_actions=guard_actions or ["NOT_APPLICABLE"],
                reason="state marker is non-sounding in P1",
            )
            return self._response(raw_tokens, [token], "VALID_COMPLETE", accepted_candidates=[candidate], guard_actions=guard_actions or ["NOT_APPLICABLE"])
        if token.lexical_type == "TIMING_MARKER_COMPONENT":
            if "FORCE_UNRESOLVED" in guard_actions:
                return self._unresolved_response(raw_tokens, [token], "UNRESOLVED", "timing marker evidence conflict", guard_actions, rule_id="PR-TIMING")
            actions = guard_actions or ["NOT_APPLICABLE"]
            candidate = self._candidate(
                rules=["PR-TIMING"],
                status="VALID_COMPLETE",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={"TIMING_MARKER": self._slot(token)},
                parse_type="non_sounding_timing_marker",
                sound_type=None,
                sound_status="RESOLVED",
                guard_actions=actions,
                reason="timing marker is non-sounding",
            )
            return self._response(raw_tokens, [token], "VALID_COMPLETE", accepted_candidates=[candidate], guard_actions=actions)
        if token.lexical_type == "GENERIC_MARKER_COMPONENT":
            return self._parse_generic_marker(raw_tokens, token, context, guard_actions)
        if token.lexical_type == "SPECIAL_TECHNIQUE_COMPONENT":
            return self._parse_special(raw_tokens, token, context, guard_actions)
        if token.lexical_type == "UNKNOWN_COMPONENT":
            return self._unresolved_response(raw_tokens, [token], "UNRESOLVED", "unknown component preserved for review", guard_actions or ["NOT_APPLICABLE"], rule_id="PR-UNKNOWN")
        return self._unresolved_response(raw_tokens, [token], "UNSUPPORTED", "lexical type outside P1 local grammar", ["FORCE_UNRESOLVED"], rule_id="PR-UNKNOWN")

    def _parse_rh_string(
        self,
        raw_tokens: list[dict[str, Any]],
        tokens: list[TokenView],
        context: dict[str, Any],
        guard_actions: list[str],
    ) -> dict[str, Any]:
        if "FORCE_UNRESOLVED" in guard_actions:
            return self._rh_string_incomplete_or_unresolved(raw_tokens, tokens, "UNRESOLVED", "guard requires unresolved review", guard_actions, context)
        if context.get("context_required") and not self._has_any_context(context):
            return self._rh_string_incomplete_or_unresolved(raw_tokens, tokens, "INCOMPLETE", "declared context is missing", self._prefer_guard(guard_actions, ["NEEDS_CONTEXT"]), context)
        if self._has_any_context(context) and not self._has_compatible_context(context):
            return self._rh_string_incomplete_or_unresolved(raw_tokens, tokens, "UNRESOLVED", "context exists but is incompatible", self._prefer_guard(guard_actions, ["FORCE_UNRESOLVED"]), context)

        candidates = []
        if context.get("no_inherited_context"):
            if self._has_compatible_context(context):
                candidate = self._rh_string_candidate(tokens, "VALID_AMBIGUOUS", None, "AMBIGUOUS", ["PR-RH-STRING"], guard_actions, "conflicting explicit context and no-inherited declaration remain ambiguous")
                rejected = self._rejected("PR-RH-STRING-CONTEXT", [t.token_id for t in tokens], "VALID_WITH_CONTEXT", "context-dependent alternative ranked behind context-free interpretation", ["NOT_APPLICABLE"])
                return self._response(raw_tokens, tokens, "VALID_AMBIGUOUS", accepted_candidates=[candidate], rejected_candidates=[rejected], guard_actions=guard_actions or ["NOT_APPLICABLE"])
            candidates.append(self._rh_string_candidate(tokens, "VALID_COMPLETE", "散", "RESOLVED", ["PR-RH-STRING"], guard_actions, "caller declared no inherited context"))
            return self._response(raw_tokens, tokens, "VALID_COMPLETE", accepted_candidates=candidates, guard_actions=guard_actions or ["NOT_APPLICABLE"])
        if self._has_compatible_context(context):
            candidate = self._rh_string_context_candidate(tokens, context, guard_actions)
            return self._response(raw_tokens, tokens, "VALID_WITH_CONTEXT", accepted_candidates=[candidate], guard_actions=guard_actions or ["NOT_APPLICABLE"])
        candidate = self._rh_string_candidate(tokens, "VALID_AMBIGUOUS", None, "AMBIGUOUS", ["PR-RH-STRING"], guard_actions, "open and inherited-context interpretations remain possible")
        return self._response(raw_tokens, tokens, "VALID_AMBIGUOUS", accepted_candidates=[candidate], guard_actions=guard_actions or ["NOT_APPLICABLE"])

    def _rh_string_incomplete_or_unresolved(
        self,
        raw_tokens: list[dict[str, Any]],
        tokens: list[TokenView],
        status: str,
        reason: str,
        guard_actions: list[str],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        slots = {
            "RIGHT_HAND_ACTION": self._slot(tokens[0]),
            "STRING_NUMBER": self._slot(tokens[1], numeric_role="string_number"),
            "CONTEXT_SOURCE": {"value": context.get("context_ref"), "context_inherited": bool(context.get("context_ref"))},
            "SOUND_STATE": {"value": None, "sound_type_candidate": None, "sound_type_resolution_status": "CONTEXT_REQUIRED" if status in {"INCOMPLETE", "UNSUPPORTED"} else "UNRESOLVED"},
        }
        candidate = self._candidate(
            rules=["PR-RH-STRING-CONTEXT"],
            status=status,
            tokens=tokens,
            consumed=[t.token_id for t in tokens],
            unconsumed=[],
            slots=slots,
            parse_type="context_inherited_sounding_unit",
            sound_type=None,
            sound_status="CONTEXT_REQUIRED" if status in {"INCOMPLETE", "UNSUPPORTED"} else "UNRESOLVED",
            guard_actions=guard_actions,
            reason=reason,
        )
        return self._response(
            raw_tokens,
            tokens,
            status,
            accepted_candidates=[candidate],
            guard_actions=guard_actions,
            context_requirements=[self._context_requirement("CONTEXT_SOURCE", reason)],
        )

    def _partial_rh_string(
        self,
        raw_tokens: list[dict[str, Any]],
        tokens: list[TokenView],
        context: dict[str, Any],
        guard_actions: list[str],
    ) -> dict[str, Any]:
        consumed = [tokens[0].token_id, tokens[1].token_id]
        unconsumed = [t.token_id for t in tokens[2:]]
        actions = self._prefer_guard(guard_actions, ["FORCE_UNRESOLVED"]) if any(t.lexical_type == "UNKNOWN_COMPONENT" for t in tokens[2:]) else guard_actions
        candidate = self._rh_string_candidate(tokens[:2], "UNRESOLVED", "散" if context.get("no_inherited_context") else None, "RESOLVED" if context.get("no_inherited_context") else "AMBIGUOUS", ["PR-RH-STRING", "PR-UNKNOWN"], actions, "local parse leaves unresolved tokens")
        candidate["unconsumed_token_ids"] = unconsumed
        candidate["unresolved_items"] = [{"token_id": tid, "reason": "unconsumed token"} for tid in unconsumed]
        candidate["slots"]["UNRESOLVED"] = {"token_ids": unconsumed, "value": unconsumed}
        candidate["structured_parse"]["slots"] = candidate["slots"]
        candidate["surface_reading_candidate"] = f"{candidate['surface_reading_candidate']} + unresolved"
        candidate["reading_candidate"] = candidate["surface_reading_candidate"]
        return self._response(raw_tokens, tokens, "UNRESOLVED", accepted_candidates=[candidate], unconsumed_tokens=unconsumed, guard_actions=actions or ["NOT_APPLICABLE"])

    def _parse_generic_marker(
        self,
        raw_tokens: list[dict[str, Any]],
        token: TokenView,
        context: dict[str, Any],
        guard_actions: list[str],
    ) -> dict[str, Any]:
        subtype = token.metadata.get("registered_subtype") or token.semantic_hint
        whitelisted = token.metadata.get("behavior_whitelisted", subtype in {"punctuation", "repeat_marker", "section_marker"})
        if not subtype:
            return self._unresolved_response(raw_tokens, [token], "UNSUPPORTED", "unregistered generic marker", self._prefer_guard(guard_actions, ["FORCE_UNRESOLVED"]), rule_id="PR-GENERIC-MARKER")
        if not whitelisted:
            actions = self._prefer_guard(guard_actions, ["NEEDS_HUMAN_REVIEW"])
            candidate = self._candidate(
                rules=["PR-GENERIC-MARKER"],
                status="UNRESOLVED",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={"GENERIC_MARKER": self._slot(token)},
                parse_type="non_sounding_or_context_marker",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=actions,
                reason="generic marker subtype needs human review before behavior is whitelisted",
            )
            return self._response(raw_tokens, [token], "UNRESOLVED", accepted_candidates=[candidate], guard_actions=actions)
        candidate = self._candidate(
            rules=["PR-GENERIC-MARKER"],
            status="VALID_COMPLETE",
            tokens=[token],
            consumed=[token.token_id],
            unconsumed=[],
            slots={"GENERIC_MARKER": self._slot(token)},
            parse_type="non_sounding_or_context_marker",
            sound_type=None,
            sound_status="RESOLVED",
            guard_actions=guard_actions or ["NOT_APPLICABLE"],
            reason="registered generic marker with whitelisted behavior",
        )
        return self._response(raw_tokens, [token], "VALID_COMPLETE", accepted_candidates=[candidate], guard_actions=guard_actions or ["NOT_APPLICABLE"])

    def _parse_special(
        self,
        raw_tokens: list[dict[str, Any]],
        token: TokenView,
        context: dict[str, Any],
        guard_actions: list[str],
    ) -> dict[str, Any]:
        if token.metadata.get("bad_candidate_sound_type"):
            candidate = self._candidate(
                rules=["PR-SPECIAL-TECHNIQUE"],
                status="INVALID_TYPE_COMBINATION",
                tokens=[token],
                consumed=[],
                unconsumed=[token.token_id],
                slots={"SPECIAL_TECHNIQUE": self._slot(token)},
                parse_type="special_technique_unit",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=["HARD_REJECT"],
                reason="special technique cannot become a fourth sound type",
            )
            return self._response(raw_tokens, [token], "INVALID_TYPE_COMBINATION", accepted_candidates=[candidate], guard_actions=["HARD_REJECT"], unconsumed_tokens=[token.token_id])
        if context.get("context_required") and not self._has_any_context(context):
            return self._unresolved_response(raw_tokens, [token], "INCOMPLETE", "special technique attachment context is missing", self._prefer_guard(guard_actions, ["NEEDS_CONTEXT"]), rule_id="PR-SPECIAL-TECHNIQUE", consumed=[token.token_id])
        if token.metadata.get("sounding_policy_known") is False:
            actions = self._prefer_guard(guard_actions, ["NEEDS_HUMAN_REVIEW"])
            sound = context.get("inherited_context", {}).get("SOUND_STATE") if isinstance(context.get("inherited_context"), dict) else None
            candidate = self._candidate(
                rules=["PR-SPECIAL-TECHNIQUE"],
                status="UNRESOLVED",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={
                    "SPECIAL_TECHNIQUE": self._slot(token),
                    "CONTEXT_SOURCE": {"value": context.get("context_ref"), "context_inherited": bool(context.get("context_ref"))},
                    "SOUND_STATE": {"value": sound, "sound_type_candidate": sound, "sound_type_resolution_status": "UNRESOLVED"},
                },
                parse_type="special_technique_unit",
                sound_type=sound,
                sound_status="UNRESOLVED",
                guard_actions=actions,
                reason="special technique sounding policy remains unclear",
            )
            return self._response(raw_tokens, [token], "UNRESOLVED", accepted_candidates=[candidate], guard_actions=actions)
        if self._has_compatible_context(context):
            actions = self._prefer_guard(guard_actions, ["NEEDS_HUMAN_REVIEW"])
            sound = context.get("inherited_context", {}).get("SOUND_STATE")
            candidate = self._candidate(
                rules=["PR-SPECIAL-TECHNIQUE"],
                status="VALID_WITH_CONTEXT",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={
                    "SPECIAL_TECHNIQUE": self._slot(token),
                    "CONTEXT_SOURCE": {"value": context.get("context_ref"), "context_inherited": True},
                    "SOUND_STATE": {"value": sound, "sound_type_candidate": sound, "sound_type_resolution_status": "RESOLVED"},
                },
                parse_type="special_technique_unit",
                sound_type=sound,
                sound_status="RESOLVED",
                guard_actions=actions,
                reason="special technique attaches to explicit caller context",
            )
            return self._response(raw_tokens, [token], "VALID_WITH_CONTEXT", accepted_candidates=[candidate], guard_actions=actions)
        if self._has_any_context(context):
            actions = self._prefer_guard(guard_actions, ["NEEDS_HUMAN_REVIEW"])
            candidate = self._candidate(
                rules=["PR-SPECIAL-TECHNIQUE"],
                status="UNRESOLVED",
                tokens=[token],
                consumed=[token.token_id],
                unconsumed=[],
                slots={
                    "SPECIAL_TECHNIQUE": self._slot(token),
                    "CONTEXT_SOURCE": {"value": context.get("context_ref"), "context_inherited": True},
                },
                parse_type="special_technique_unit",
                sound_type=None,
                sound_status="UNRESOLVED",
                guard_actions=actions,
                reason="special technique attachment context is incomplete",
            )
            return self._response(raw_tokens, [token], "UNRESOLVED", accepted_candidates=[candidate], guard_actions=actions)
        return self._unresolved_response(raw_tokens, [token], "INCOMPLETE", "special technique requires attachment review", self._prefer_guard(guard_actions, ["NEEDS_CONTEXT"]), rule_id="PR-SPECIAL-TECHNIQUE", consumed=[token.token_id])

    def _fallback(
        self,
        raw_tokens: list[dict[str, Any]],
        tokens: list[TokenView],
        context: dict[str, Any],
        guard_actions: list[str],
    ) -> dict[str, Any]:
        if any(t.lexical_type == "POSITION_COMPONENT" for t in tokens):
            return self._unresolved_response(raw_tokens, tokens, "UNSUPPORTED", "position sequence outside P1 local grammar", self._prefer_guard(guard_actions, ["FORCE_UNRESOLVED"]), rule_id="PR-UNKNOWN")
        if any(t.lexical_type == "UNKNOWN_COMPONENT" for t in tokens):
            return self._unresolved_response(raw_tokens, tokens, "UNRESOLVED", "unknown token preserved", guard_actions or ["NOT_APPLICABLE"], rule_id="PR-UNKNOWN")
        return self._unresolved_response(raw_tokens, tokens, "UNSUPPORTED", "no local production matched", guard_actions or ["NOT_APPLICABLE"], rule_id="PR-UNKNOWN")

    def _pressed_candidate(self, tokens: list[TokenView], guard_actions: list[str]) -> dict[str, Any]:
        return self._candidate(
            rules=["PR-LF-HUI-RH-STRING"],
            status="VALID_COMPLETE",
            tokens=tokens,
            consumed=[t.token_id for t in tokens],
            unconsumed=[],
            slots={
                "LEFT_FINGER": self._slot(tokens[0]),
                "HUI_POSITION": self._slot(tokens[1], numeric_role="hui_position"),
                "RIGHT_HAND_ACTION": self._slot(tokens[2]),
                "STRING_NUMBER": self._slot(tokens[3], numeric_role="string_number"),
                "SOUND_STATE": {"value": "按", "sound_type_candidate": "按", "sound_type_resolution_status": "RESOLVED"},
            },
            parse_type="pressed_sounding_unit",
            sound_type="按",
            sound_status="RESOLVED",
            guard_actions=guard_actions or ["NOT_APPLICABLE"],
            reason="all pressed sounding unit slots are explicit",
        )

    def _post_motion_candidate(self, tokens: list[TokenView], context: dict[str, Any], guard_actions: list[str]) -> dict[str, Any]:
        sound = context.get("inherited_context", {}).get("SOUND_STATE")
        return self._candidate(
            rules=["PR-POST-MOTION", "PR-RH-STRING-CONTEXT"],
            status="VALID_WITH_CONTEXT",
            tokens=tokens,
            consumed=[t.token_id for t in tokens],
            unconsumed=[],
            slots={
                "RIGHT_HAND_ACTION": self._slot(tokens[0]),
                "STRING_NUMBER": self._slot(tokens[1], numeric_role="string_number"),
                "POST_SOUND_MOTION": self._slot(tokens[2]),
                "CONTEXT_SOURCE": {"value": context.get("context_ref"), "context_inherited": True},
                "SOUND_STATE": {"value": sound, "sound_type_candidate": sound, "sound_type_resolution_status": "RESOLVED"},
            },
            parse_type="post_sound_motion_unit",
            sound_type=sound,
            sound_status="RESOLVED",
            guard_actions=guard_actions or ["NOT_APPLICABLE"],
            reason="post motion attaches to explicit caller context",
        )

    def _rh_string_context_candidate(self, tokens: list[TokenView], context: dict[str, Any], guard_actions: list[str]) -> dict[str, Any]:
        sound = context.get("inherited_context", {}).get("SOUND_STATE")
        return self._candidate(
            rules=["PR-RH-STRING-CONTEXT"],
            status="VALID_WITH_CONTEXT",
            tokens=tokens,
            consumed=[t.token_id for t in tokens],
            unconsumed=[],
            slots={
                "RIGHT_HAND_ACTION": self._slot(tokens[0]),
                "STRING_NUMBER": self._slot(tokens[1], numeric_role="string_number"),
                "CONTEXT_SOURCE": {"value": context.get("context_ref"), "context_inherited": True},
                "SOUND_STATE": {"value": sound, "sound_type_candidate": sound, "sound_type_resolution_status": "RESOLVED"},
            },
            parse_type="context_inherited_sounding_unit",
            sound_type=sound,
            sound_status="RESOLVED",
            guard_actions=guard_actions or ["NOT_APPLICABLE"],
            reason="right-hand/string unit uses explicit inherited context",
        )

    def _rh_string_candidate(
        self,
        tokens: list[TokenView],
        status: str,
        sound_type: str | None,
        sound_status: str,
        rules: list[str],
        guard_actions: list[str],
        reason: str,
    ) -> dict[str, Any]:
        slots = {
            "RIGHT_HAND_ACTION": self._slot(tokens[0]),
            "STRING_NUMBER": self._slot(tokens[1], numeric_role="string_number"),
            "SOUND_STATE": {"value": sound_type, "sound_type_candidate": sound_type, "sound_type_resolution_status": sound_status},
        }
        structured_extra = {}
        if status == "VALID_AMBIGUOUS":
            structured_extra["interpretation_options"] = [
                {"option_id": "open_string_candidate", "sound_type_candidate": "散", "requires_no_inherited_context_or_open_evidence_to_resolve": True},
                {"option_id": "inherited_context_candidate", "sound_type_candidate": None, "requires_context_ref_or_inherited_context": True},
            ]
        return self._candidate(
            rules=rules,
            status=status,
            tokens=tokens,
            consumed=[t.token_id for t in tokens],
            unconsumed=[],
            slots=slots,
            parse_type="right_hand_string_ambiguous_or_resolved_unit",
            sound_type=sound_type,
            sound_status=sound_status,
            guard_actions=guard_actions or ["NOT_APPLICABLE"],
            reason=reason,
            structured_extra=structured_extra,
        )

    def _candidate(
        self,
        *,
        rules: list[str],
        status: str,
        tokens: list[TokenView],
        consumed: list[str],
        unconsumed: list[str],
        slots: dict[str, Any],
        parse_type: str,
        sound_type: str | None,
        sound_status: str,
        guard_actions: list[str],
        reason: str,
        structured_extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {
            "rules": rules,
            "status": status,
            "consumed": consumed,
            "slots": self._slot_identity(slots),
            "sound_type": sound_type,
        }
        candidate_id = "cand_" + _sha_text(payload)
        surface = self._render_surface(slots, parse_type, status)
        rule_meta = [self.rule_by_id.get(rule, {}) for rule in rules]
        specificity = max((item.get("specificity", 0) for item in rule_meta), default=0)
        priority = max((item.get("priority", 0) for item in rule_meta), default=0)
        unresolved_count = len(slots.get("UNRESOLVED", {}).get("token_ids", [])) if isinstance(slots.get("UNRESOLVED"), dict) else 0
        context_deps = len([slot for slot in slots if slot == "CONTEXT_SOURCE"])
        score_breakdown = {
            "grammar_score": 1 if status.startswith("VALID") else 0,
            "specificity_score": specificity,
            "completeness_score": len(consumed),
            "guard_penalty": len([a for a in guard_actions if a in {"SOFT_PENALTY", "NEEDS_HUMAN_REVIEW"}]),
            "context_penalty": context_deps,
            "unresolved_penalty": unresolved_count,
            "ambiguity_penalty": 1 if status == "VALID_AMBIGUOUS" else 0,
            "final_score": len(consumed) + specificity + priority - unresolved_count - context_deps,
            "score_explanation": "deterministic heuristic grammar score",
        }
        structured = {
            "slots": slots,
            "surface_reading_derivation": "surface is derived from structured slots",
        }
        if structured_extra:
            structured.update(structured_extra)
        return {
            "candidate_id": candidate_id,
            "rank": 1,
            "reading_candidate": surface,
            "structured_parse": structured,
            "surface_reading_candidate": surface,
            "literal_component_gloss": [{"token_id": t.token_id, "literal_gloss": t.label, "component_id": t.normalized_component_id} for t in tokens],
            "parse_type": parse_type,
            "status": status,
            "consumed_token_ids": consumed,
            "unconsumed_token_ids": unconsumed,
            "slots": slots,
            "applied_rule_ids": rules,
            "applied_guard_ids": [a for a in guard_actions if a != "NOT_APPLICABLE"],
            "guard_actions": guard_actions,
            "context_requirements": [] if "CONTEXT_SOURCE" in slots or status not in {"VALID_AMBIGUOUS", "INCOMPLETE"} else [self._context_requirement("CONTEXT_SOURCE", "inherited-context interpretation")],
            "unresolved_items": [],
            "score": score_breakdown["final_score"],
            "score_type": "HEURISTIC_GRAMMAR_SCORE",
            "score_breakdown": score_breakdown,
            "reason": reason,
            "authority_flags": dict(AUTHORITY_FLAGS),
            "sound_type_candidate": sound_type,
            "sound_type_resolution_status": sound_status,
        }

    def _response(
        self,
        input_tokens: list[dict[str, Any]],
        normalized_tokens: list[TokenView],
        parse_status: str,
        *,
        accepted_candidates: list[dict[str, Any]] | None = None,
        rejected_candidates: list[dict[str, Any]] | None = None,
        unconsumed_tokens: list[str] | None = None,
        guard_actions: list[str] | None = None,
        input_contract_errors: list[dict[str, Any]] | None = None,
        normalization_gaps: list[dict[str, Any]] | None = None,
        context_requirements: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        accepted = self._rank(accepted_candidates or [])
        top_unconsumed = unconsumed_tokens
        if top_unconsumed is None:
            if accepted:
                top_unconsumed = accepted[0]["unconsumed_token_ids"]
            else:
                top_unconsumed = [t.token_id for t in normalized_tokens]
        actions = guard_actions or ["NOT_APPLICABLE"]
        return {
            "parser_contract_version": self.runtime_contract.get("version", "v0.1"),
            "parser_runtime_contract_id": self.runtime_contract.get("runtime_contract_id"),
            "input_tokens": deepcopy(input_tokens),
            "normalization_summary": self._normalization_summary(normalized_tokens, normalization_gaps or []),
            "parse_status": parse_status,
            "accepted_candidates": accepted,
            "rejected_candidates": rejected_candidates or [],
            "unconsumed_tokens": top_unconsumed,
            "consumed_token_ids": accepted[0]["consumed_token_ids"] if accepted else [],
            "context_requirements": context_requirements or self._collect_context_requirements(accepted),
            "guard_summary": {
                "guard_actions": actions,
                "guards_checked": list(self.guard_by_id),
                "guards_applied": [a for a in actions if a != "NOT_APPLICABLE"],
                "guards_rejected": [a for a in actions if a == "HARD_REJECT"],
                "scope_mismatch_guards": [a for a in actions if a == "NOT_APPLICABLE"],
                "literal_global_ban_used": False,
                "guard_action_enum": sorted(self.guard_actions),
            },
            "authority_flags": dict(AUTHORITY_FLAGS),
            "input_contract_errors": input_contract_errors or [],
        }

    def _unresolved_response(
        self,
        raw_tokens: list[dict[str, Any]],
        tokens: list[TokenView],
        status: str,
        reason: str,
        guard_actions: list[str],
        *,
        rule_id: str,
        consumed: list[str] | None = None,
    ) -> dict[str, Any]:
        consumed_ids = consumed or []
        unconsumed = [t.token_id for t in tokens if t.token_id not in consumed_ids]
        slots: dict[str, Any] = {}
        if consumed_ids:
            for token in tokens:
                if token.token_id in consumed_ids:
                    slot = self._slot_from_hint_or_type(token)
                    slots[slot] = self._slot(token)
        if unconsumed:
            slots["UNRESOLVED"] = {"token_ids": unconsumed, "value": unconsumed}
        candidate = None
        if consumed_ids or status in {"VALID_AMBIGUOUS", "UNRESOLVED", "INCOMPLETE"}:
            candidate = self._candidate(
                rules=[rule_id],
                status=status,
                tokens=tokens,
                consumed=consumed_ids,
                unconsumed=unconsumed,
                slots=slots,
                parse_type="unresolved_parse_candidate" if rule_id == "PR-UNKNOWN" else "incomplete_or_unresolved_candidate",
                sound_type=None,
                sound_status="UNRESOLVED" if status != "INCOMPLETE" else "CONTEXT_REQUIRED",
                guard_actions=guard_actions,
                reason=reason,
            )
            candidate["unresolved_items"] = [{"token_id": tid, "reason": reason} for tid in unconsumed]
        accepted = [candidate] if candidate is not None and rule_id != "PR-UNKNOWN" else []
        rejected = [] if accepted else [self._rejected(rule_id, consumed_ids, status, reason, guard_actions)]
        context_reqs = [self._context_requirement("HOST_UNIT", reason)] if "host" in reason else []
        return self._response(raw_tokens, tokens, status, accepted_candidates=accepted, rejected_candidates=rejected, unconsumed_tokens=unconsumed, guard_actions=guard_actions, context_requirements=context_reqs)

    def _rejected(
        self,
        rule_id: str,
        consumed: list[str],
        status: str,
        reason: str,
        guards: list[str],
        *,
        sound_type: str | None = None,
        sound_status: str = "UNRESOLVED",
    ) -> dict[str, Any]:
        return {
            "candidate_id": "reject_" + _sha_text({"rule": rule_id, "consumed": consumed, "status": status, "reason": reason}),
            "attempted_rule_id": rule_id,
            "consumed_token_ids": consumed,
            "rejection_status": status,
            "rejection_reason": reason,
            "guard_ids": [g for g in guards if g != "NOT_APPLICABLE"],
            "guard_actions": guards,
            "recoverable": status not in {"INPUT_CONTRACT_INVALID", "FORBIDDEN_GUARD_REJECTED"},
            "suggested_next_action": "human_review_or_future_phase",
            "sound_type_candidate": sound_type,
            "sound_type_resolution_status": sound_status,
        }

    def _rank(self, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        def key(candidate: dict[str, Any]) -> tuple[Any, ...]:
            status = candidate["status"]
            complete = status in {"VALID_COMPLETE", "VALID_WITH_CONTEXT", "VALID_AMBIGUOUS"}
            specificity = candidate["score_breakdown"]["specificity_score"]
            context_deps = candidate["score_breakdown"]["context_penalty"]
            unresolved = candidate["score_breakdown"]["unresolved_penalty"]
            coverage = len(candidate["consumed_token_ids"])
            priority = max((self.rule_by_id.get(rule, {}).get("priority", 0) for rule in candidate["applied_rule_ids"]), default=0)
            return (not complete, -specificity, context_deps, unresolved, -coverage, -priority, candidate["candidate_id"])

        ranked = sorted(candidates, key=key)
        for idx, candidate in enumerate(ranked, start=1):
            candidate["rank"] = idx
        return ranked

    def _guard_actions_for(self, tokens: list[TokenView], context: dict[str, Any]) -> list[str]:
        ref = context.get("d3a_guard_ref") or context.get("d3a_scope_case")
        scope = context.get("scope_match")
        labels = {t.label for t in tokens}
        lex = {t.lexical_type for t in tokens}
        if ref == "ABSTRACT_FORBID_BARE_GOU":
            return ["HARD_REJECT"]
        if ref == "FORBID-MING-7-6-GOU-4-AS-GOU-5-6":
            return ["SOFT_PENALTY"] if "RIGHT_HAND_ACTION_COMPONENT" in lex else ["NOT_APPLICABLE"]
        if scope is False:
            return ["NOT_APPLICABLE"]
        if ref == "FORBID-GOU-4-AS-UNKNOWN" and (scope is True or context.get("candidate_surface_under_review") == "勾？"):
            return ["HARD_REJECT"]
        if ref == "FORBID-MARKER-SOUNDING-UNIT" and scope is True:
            return ["HARD_REJECT"]
        if ref == "FORBID-SHAOXI-AS-JIU":
            if any(t.metadata.get("component_id_label_conflict") for t in tokens):
                return ["FORCE_UNRESOLVED"]
            return ["SOFT_PENALTY"] if "TIMING_MARKER_COMPONENT" in lex else ["NOT_APPLICABLE"]
        if ref == "FORBID-RH-ACTION-STRING-BARE-GOU":
            return ["FORCE_UNRESOLVED"] if scope == "partial" else ["NOT_APPLICABLE"]
        if ref in {"FORBID-ZHUXIA-TIAO-7-DROP-CONTEXT", "FORBID-P4-MISSING-PRE-JI-JINFU-PLUCK"}:
            return ["NEEDS_CONTEXT"]
        if ref == "FORBID-QIAQI-INDEPENDENT":
            return ["NEEDS_HUMAN_REVIEW"]
        if ref == "FORBID-JIU-AS-SHAOXI":
            return ["NEEDS_HUMAN_REVIEW"] if scope is True or "就" in labels else ["NOT_APPLICABLE"]
        return ["NOT_APPLICABLE"]

    def _prefer_guard(self, current: list[str], desired: list[str]) -> list[str]:
        if not current or current == ["NOT_APPLICABLE"]:
            return desired
        merged = list(current)
        for item in desired:
            if item not in merged:
                merged.append(item)
        return merged

    def _validate_call(self, tokens: Any, context_input: Any, options: Any) -> list[dict[str, Any]]:
        errors: list[dict[str, Any]] = []
        if context_input is not None and not isinstance(context_input, dict):
            errors.append({"field": "context_input", "reason": "context_input must be object"})
        if options is not None and not isinstance(options, dict):
            errors.append({"field": "options", "reason": "options must be object"})
        if not isinstance(tokens, list):
            errors.append({"field": "tokens", "reason": "tokens must be list"})
            return errors
        if not tokens:
            errors.append({"field": "tokens", "reason": "empty input"})
            return errors
        ids: set[str] = set()
        indexes: set[int] = set()
        for idx, token in enumerate(tokens):
            if not isinstance(token, dict):
                errors.append({"field": f"tokens[{idx}]", "reason": "token must be object"})
                continue
            missing = sorted(
                field
                for field in CORE_TOKEN_FIELDS
                if field not in token and not (field == "component_id_v0_2" and token.get("normalization_status") == "COMPONENT_ID_NORMALIZATION_GAP")
            )
            if missing:
                errors.append({"field": f"tokens[{idx}]", "reason": "missing required field", "missing": missing})
                continue
            token_id = token.get("token_id")
            seq = token.get("sequence_index")
            component_id = token.get("component_id_v0_2")
            if not isinstance(token_id, str) or not token_id:
                errors.append({"field": "token_id", "reason": "token_id must be non-empty string"})
            elif token_id in ids:
                errors.append({"field": "token_id", "reason": "duplicate token_id", "token_id": token_id})
            else:
                ids.add(token_id)
            if not isinstance(seq, int) or seq < 0:
                errors.append({"field": "sequence_index", "reason": "sequence_index must be non-negative integer"})
            elif seq in indexes:
                errors.append({"field": "sequence_index", "reason": "duplicate sequence_index", "sequence_index": seq})
            else:
                indexes.add(seq)
            if component_id is not None:
                if not isinstance(component_id, str) or not ID_RE.match(component_id):
                    errors.append({"field": "component_id_v0_2", "reason": "malformed component id", "component_id_v0_2": component_id})
            elif token.get("normalization_status") != "COMPONENT_ID_NORMALIZATION_GAP":
                errors.append({"field": "component_id_v0_2", "reason": "missing primary id without normalization gap"})
            if not isinstance(token.get("label_zh"), str):
                errors.append({"field": "label_zh", "reason": "label_zh must be string"})
            lexical = token.get("lexical_component_type")
            if not isinstance(lexical, str) or lexical not in self.lexical_types:
                errors.append({"field": "lexical_component_type", "reason": "invalid lexical type", "value": lexical})
            if not isinstance(token.get("normalization_status"), str):
                errors.append({"field": "normalization_status", "reason": "normalization_status must be string"})
            if "metadata" in token and not isinstance(token["metadata"], dict):
                errors.append({"field": "metadata", "reason": "metadata must be object"})
            for field in OPTIONAL_AUDIT_FIELDS:
                if field in token and token[field] is None:
                    errors.append({"field": field, "reason": "audit field must not be null when present"})
        return errors

    def _normalize_tokens(self, tokens: list[dict[str, Any]]) -> tuple[list[TokenView], list[dict[str, Any]]]:
        views: list[TokenView] = []
        gaps: list[dict[str, Any]] = []
        for token in tokens:
            component_id = token.get("component_id_v0_2")
            status = token.get("normalization_status")
            trace = {
                "input_component_id_v0_2": component_id,
                "source_component_id": token.get("source_component_id"),
                "legacy_component_id": token.get("legacy_component_id"),
                "normalization_status": status,
            }
            normalized_id: str | None = component_id
            if component_id is None or status == "COMPONENT_ID_NORMALIZATION_GAP":
                normalized_id = None
                gaps.append({"token_id": token.get("token_id"), "reason": "normalization gap", "legacy_component_id": token.get("legacy_component_id")})
            elif str(component_id).startswith("ABS-"):
                if not self.allow_abstract_component_ids:
                    gaps.append({"token_id": token["token_id"], "component_id": component_id, "reason": "abstract ids disabled"})
                    normalized_id = None
            elif component_id in self.component_by_id:
                normalized_id = component_id
            elif token.get("legacy_component_id") in self.legacy_to_primary:
                normalized_id = self.legacy_to_primary[token.get("legacy_component_id")]
                trace["normalized_from_legacy"] = normalized_id
            elif token.get("source_component_id") in self.source_to_primary:
                normalized_id = self.source_to_primary[token.get("source_component_id")]
                trace["normalized_from_source"] = normalized_id
            else:
                gaps.append({"token_id": token["token_id"], "component_id": component_id, "reason": "id not in D1 registry or alias map"})
                normalized_id = None
            metadata = token.get("metadata") if isinstance(token.get("metadata"), dict) else {}
            views.append(
                TokenView(
                    raw=deepcopy(token),
                    token_id=token["token_id"],
                    sequence_index=token["sequence_index"],
                    component_id=component_id,
                    label=token["label_zh"],
                    lexical_type=token["lexical_component_type"],
                    semantic_hint=token.get("semantic_role_hint"),
                    metadata=metadata,
                    normalized_component_id=normalized_id,
                    normalization_status=status,
                    normalization_trace=trace,
                )
            )
        return views, gaps

    def _normalization_summary(self, tokens: list[TokenView], gaps: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "all_primary_ids_v0_2": not gaps and all(t.normalized_component_id and not t.normalized_component_id.startswith("ABS-") for t in tokens),
            "abstract_ids_seen": len([t for t in tokens if t.component_id and t.component_id.startswith("ABS-")]),
            "legacy_ids_seen": len([t for t in tokens if t.raw.get("legacy_component_id")]),
            "source_v0_1_ids_seen": len([t for t in tokens if t.raw.get("source_component_id")]),
            "normalization_gaps": gaps,
            "normalization_status": "COMPONENT_ID_NORMALIZATION_GAP" if gaps else "NORMALIZED",
            "tokens": [
                {
                    "token_id": t.token_id,
                    "normalized_component_id": t.normalized_component_id,
                    "normalization_status": t.normalization_status,
                    "source_component_id": t.raw.get("source_component_id"),
                    "legacy_component_id": t.raw.get("legacy_component_id"),
                    "normalization_trace": t.normalization_trace,
                }
                for t in tokens
            ],
        }

    def _safe_token_ids(self, tokens: Any) -> list[str]:
        if not isinstance(tokens, list):
            return []
        return [t.get("token_id") for t in tokens if isinstance(t, dict) and isinstance(t.get("token_id"), str)]

    def _slot(self, token: TokenView, *, numeric_role: str | None = None) -> dict[str, Any]:
        data = {
            "token_ids": [token.token_id],
            "component_ids": [token.normalized_component_id],
            "value": token.label,
            "component_id": token.normalized_component_id,
            "context_inherited": False,
        }
        if numeric_role:
            data["numeric_role_assigned_by_rule"] = numeric_role
        return data

    def _slot_from_hint_or_type(self, token: TokenView) -> str:
        if token.semantic_hint in {"PRE_SOUND_MOTION", "POST_SOUND_MOTION", "SPECIAL_TECHNIQUE"}:
            return token.semantic_hint
        return {
            "RIGHT_HAND_ACTION_COMPONENT": "RIGHT_HAND_ACTION",
            "NUMERIC_COMPONENT": "UNRESOLVED",
            "LEFT_FINGER_NAME_COMPONENT": "LEFT_FINGER",
            "LEFT_HAND_ACTION_COMPONENT": "LEFT_HAND_ACTION",
            "STATE_MARKER_COMPONENT": "STATE_START",
            "TIMING_MARKER_COMPONENT": "TIMING_MARKER",
            "GENERIC_MARKER_COMPONENT": "GENERIC_MARKER",
            "SPECIAL_TECHNIQUE_COMPONENT": "SPECIAL_TECHNIQUE",
            "UNKNOWN_COMPONENT": "UNRESOLVED",
        }.get(token.lexical_type, "UNRESOLVED")

    def _slot_identity(self, slots: dict[str, Any]) -> dict[str, Any]:
        identity: dict[str, Any] = {}
        for key, value in slots.items():
            if isinstance(value, dict):
                identity[key] = {
                    "token_ids": value.get("token_ids"),
                    "component_ids": value.get("component_ids"),
                    "value": value.get("value"),
                }
            else:
                identity[key] = value
        return identity

    def _render_surface(self, slots: dict[str, Any], parse_type: str, status: str) -> str:
        def val(name: str) -> str:
            item = slots.get(name, {})
            if isinstance(item, dict):
                return str(item.get("value") or "")
            return ""

        if parse_type == "pressed_sounding_unit":
            return f"{val('LEFT_FINGER')}{val('HUI_POSITION')}徽{val('RIGHT_HAND_ACTION')}{val('STRING_NUMBER')}弦"
        if parse_type == "ornamented_attack":
            return f"{val('PRE_SOUND_MOTION')}+{val('LEFT_FINGER')}{val('HUI_POSITION')}徽{val('RIGHT_HAND_ACTION')}{val('STRING_NUMBER')}弦"
        if parse_type == "post_sound_motion_unit":
            return f"{val('RIGHT_HAND_ACTION')}{val('STRING_NUMBER')}弦+{val('POST_SOUND_MOTION')}"
        if parse_type == "state_plus_right_hand_string_unit":
            return f"{val('STATE_START')}，{val('RIGHT_HAND_ACTION')}{val('STRING_NUMBER')}弦"
        if parse_type == "context_inherited_sounding_unit":
            return f"{val('RIGHT_HAND_ACTION')}{val('STRING_NUMBER')}弦(承前)"
        if parse_type == "right_hand_string_ambiguous_or_resolved_unit":
            suffix = "" if status == "VALID_COMPLETE" else "?"
            return f"{val('RIGHT_HAND_ACTION')}{val('STRING_NUMBER')}弦{suffix}"
        if parse_type == "special_technique_unit":
            return f"{val('SPECIAL_TECHNIQUE')}(承前位置)" if slots.get("CONTEXT_SOURCE") else val("SPECIAL_TECHNIQUE")
        for marker in ("STATE_START", "STATE_END", "TIMING_MARKER", "GENERIC_MARKER"):
            if marker in slots:
                return val(marker)
        return "<UNRESOLVED>"

    def _state_sound(self, token: TokenView) -> str | None:
        if "散" in token.label:
            return "散"
        if "泛" in token.label:
            return "泛"
        return None

    def _has_any_context(self, context: dict[str, Any]) -> bool:
        return bool(context.get("context_ref") or context.get("inherited_context"))

    def _has_compatible_context(self, context: dict[str, Any]) -> bool:
        inherited = context.get("inherited_context")
        return isinstance(inherited, dict) and bool(CONTEXT_KEYS & set(inherited))

    def _context_requirement(self, required_for: str, label: str) -> dict[str, Any]:
        return {
            "requirement_id": "ctx_" + _sha_text({"required_for": required_for, "label": label}, 10),
            "required_for": required_for,
            "label": label,
            "accepted_input_fields": ["context_ref", "inherited_context"],
            "implicit_backward_scan_depth": 0,
            "status_if_declared_required_but_missing": "INCOMPLETE",
        }

    def _collect_context_requirements(self, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: dict[str, dict[str, Any]] = {}
        for candidate in candidates:
            for item in candidate.get("context_requirements", []):
                seen[item["requirement_id"]] = item
        return list(seen.values())

    def _guess_rule_id(self, tokens: list[TokenView], context: dict[str, Any]) -> str:
        lexical = [t.lexical_type for t in tokens]
        if lexical == ["RIGHT_HAND_ACTION_COMPONENT", "NUMERIC_COMPONENT"]:
            return "PR-RH-STRING-CONTEXT" if context.get("context_required") else "PR-RH-STRING"
        if lexical and lexical[0] == "TIMING_MARKER_COMPONENT":
            return "PR-TIMING"
        if lexical and lexical[0] == "GENERIC_MARKER_COMPONENT":
            return "PR-GENERIC-MARKER"
        if lexical and lexical[0] == "SPECIAL_TECHNIQUE_COMPONENT":
            return "PR-SPECIAL-TECHNIQUE"
        if lexical and lexical[0] == "LEFT_HAND_ACTION_COMPONENT":
            return "PR-PRE-MOTION" if tokens[0].semantic_hint == "PRE_SOUND_MOTION" else "PR-POST-MOTION"
        return "PR-UNKNOWN"

    def _smoke_token(
        self,
        token_id: str,
        index: int,
        component: tuple[str, str],
        lexical: str,
        *,
        hint: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "token_id": token_id,
            "sequence_index": index,
            "component_id_v0_2": component[0],
            "label_zh": component[1],
            "lexical_component_type": lexical,
            "normalization_status": "NORMALIZED_V0_2_PRIMARY",
            "source_component_id": None,
            "legacy_component_id": None,
            "semantic_role_hint": hint,
            "relation_to_previous": None,
            "relation_to_next": None,
            "metadata": metadata or {},
        }

    def _index_components(self, registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
        components: dict[str, dict[str, Any]] = {}
        for item in registry.get("components", []) + registry.get("auxiliary_components", []):
            if isinstance(item, dict) and item.get("component_id"):
                components[item["component_id"]] = item
        return components

    def _index_aliases(self, alias_map: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
        legacy: dict[str, str] = {}
        source: dict[str, str] = {}
        for item in alias_map.get("legacy_to_reindexed", []):
            if isinstance(item, dict) and item.get("legacy_component_id") and item.get("reindexed_component_id_v0_2"):
                legacy[item["legacy_component_id"]] = item["reindexed_component_id_v0_2"]
        for item in alias_map.get("source_v0_1_to_reindexed", []):
            if isinstance(item, dict) and item.get("source_component_id_v0_1") and item.get("reindexed_component_id_v0_2"):
                source[item["source_component_id_v0_1"]] = item["reindexed_component_id_v0_2"]
        return legacy, source
