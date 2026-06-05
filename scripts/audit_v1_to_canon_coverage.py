#!/usr/bin/env python3
"""Blind V1-to-canon coverage audit for Cyber Guqin.

This script intentionally derives coverage items from the current Xianwengcao
V1 runtime CSV files first, then compares those observed items with internal
ontology, canon seed, and QXBY_BATCH_001 draft evidence. It must not use a
manually prepared gap list, and it must not write canon, sources, or V1 inputs.
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"

V1_SCORE = ROOT / "01_pieces" / "xianwengcao" / "score_events.csv"
V1_TEMPLATES = ROOT / "00_global" / "gesture_templates.csv"
V1_COMPONENTS = ROOT / "00_global" / "gesture_components.csv"
V1_PHRASES = ROOT / "01_pieces" / "xianwengcao" / "phrase_structure.csv"
V1_RECORDING_SCRIPT = ROOT / "01_pieces" / "xianwengcao" / "recording_script_human.csv"
V1_RECORDING_BATCHES = ROOT / "01_pieces" / "xianwengcao" / "recording_batches.md"

CANON_FILES = [
    ROOT / "canon" / "sources.yaml",
    ROOT / "canon" / "terms.yaml",
    ROOT / "canon" / "component_lexicon.yaml",
    ROOT / "canon" / "gesture_families.yaml",
    ROOT / "canon" / "alias_rules.yaml",
    ROOT / "canon" / "technique_rules.yaml",
    ROOT / "canon" / "validation_rules.yaml",
]
QXBY_DRAFT = ROOT / "canon" / "drafts" / "qxby_batch_001.yaml"
QXBY_MANIFEST = ROOT / "sources" / "qinxue_beiyao" / "QXBY_BATCH_001" / "manifest.yaml"

ONTOLOGY_FILES = [
    ROOT / "00_global" / "guqin_fingering_ontology.yaml",
    ROOT / "00_global" / "gesture_component_lexicon.csv",
    ROOT / "00_global" / "gesture_family_catalog.csv",
    ROOT / "00_global" / "alias_rules.yaml",
    ROOT / "06_docs" / "GESTURE_ONTOLOGY.md",
]
SKILL_FILES = [
    ROOT / ".agents" / "skills" / "guqin-canon-builder" / "SKILL.md",
    ROOT / ".agents" / "skills" / "guqin-dapu-parser" / "SKILL.md",
]

NONE_VALUES = {"", "none", "null", "n/a", "na", "-"}
FINGER_ZH = {
    "thumb": "大指",
    "index": "食指",
    "middle": "中指",
    "ring": "名指",
    "little": "小指",
}
SOUND_TYPE_IDS = {"散音": "sound_type_san", "按音": "sound_type_an", "泛音": "sound_type_fan"}


@dataclass
class CoverageItem:
    item_type: str
    term: str
    internal_name: str = ""
    source_in_v1: set[str] = field(default_factory=set)
    used_in_events: set[str] = field(default_factory=set)
    used_in_gestures: set[str] = field(default_factory=set)
    aliases: set[str] = field(default_factory=set)
    notes: set[str] = field(default_factory=set)
    evidence_in_canon_seed: list[str] = field(default_factory=list)
    evidence_in_qxby_batch_001: list[str] = field(default_factory=list)
    evidence_in_internal_ontology: list[str] = field(default_factory=list)
    coverage_status: str = ""
    recommended_action: str = ""
    batch002_priority: str = "defer"

    @property
    def item_id(self) -> str:
        base = self.internal_name or self.term
        safe = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", base).strip("_")
        return f"{self.item_type}:{safe}"

    def search_terms(self) -> set[str]:
        terms = {self.term, self.internal_name, *self.aliases}
        if self.term in FINGER_ZH:
            terms.add(FINGER_ZH[self.term])
        if self.internal_name in FINGER_ZH:
            terms.add(FINGER_ZH[self.internal_name])
        if self.term in SOUND_TYPE_IDS:
            terms.add(SOUND_TYPE_IDS[self.term])
        return {clean(v) for v in terms if clean(v)}


def clean(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def is_value(value: Any) -> bool:
    return clean(value).lower() not in NONE_VALUES


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: clean(v) for k, v in row.items()} for row in csv.DictReader(fh)]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_jsonish(path: Path) -> Any:
    text = read_text(path)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def flatten_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        values: list[str] = []
        for key, inner in value.items():
            values.append(clean(key))
            values.extend(flatten_values(inner))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(flatten_values(item))
        return values
    return [clean(value)]


def add_index(index: dict[str, list[str]], token: str, evidence: str) -> None:
    token = clean(token)
    if not token or token.lower() in NONE_VALUES:
        return
    keys = {token}
    if re.match(r"^[A-Za-z0-9_\-]+$", token):
        keys.add(token.lower())
    for key in keys:
        if evidence not in index[key]:
            index[key].append(evidence)


def add_aliases(item: CoverageItem) -> None:
    if item.term in FINGER_ZH:
        item.aliases.add(FINGER_ZH[item.term])
    if item.internal_name in FINGER_ZH:
        item.aliases.add(FINGER_ZH[item.internal_name])
    if item.term in SOUND_TYPE_IDS:
        item.aliases.add(SOUND_TYPE_IDS[item.term])


def build_jsonish_index(path: Path, root_key: str | None, label: str) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    data = load_jsonish(path)
    if data is None:
        text = read_text(path)
        for match in re.findall(r"[\w\u4e00-\u9fff]+", text):
            add_index(index, match, f"{label}:text")
        return index

    nodes: list[Any]
    if root_key and isinstance(data, dict):
        nodes = data.get(root_key, [])
    elif isinstance(data, dict):
        nodes = [data]
    else:
        nodes = data if isinstance(data, list) else []

    for node in nodes:
        if not isinstance(node, dict):
            continue
        evidence_id = (
            node.get("component_name")
            or node.get("technique_id")
            or node.get("gesture_family")
            or node.get("term_id")
            or node.get("alias")
            or label
        )
        evidence = f"{label}:{evidence_id}"
        for value in flatten_values(node):
            add_index(index, value, evidence)
    return index


def build_csv_index(path: Path, key_fields: list[str], label: str) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    if not path.exists():
        return index
    for row in read_csv(path):
        evidence_id = next((row.get(k, "") for k in key_fields if row.get(k)), label)
        evidence = f"{label}:{evidence_id}"
        for value in row.values():
            for part in re.split(r"[|/;,，、\s]+", value):
                add_index(index, part, evidence)
            add_index(index, value, evidence)
    return index


def parse_simple_yaml_items(path: Path, label: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_list_key = ""
    in_items = False
    for raw_line in read_text(path).splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if line == "items:":
            in_items = True
            continue
        if not in_items:
            continue
        if re.match(r"-\s+\w+:", line):
            if current:
                items.append(current)
            current = {}
            current_list_key = ""
            line = line[1:].strip()
        if current is None:
            continue
        key_match = re.match(r"([A-Za-z_][\w_]*):(?:\s*(.*))?$", line)
        if key_match:
            key = key_match.group(1)
            value = clean(key_match.group(2) or "")
            current_list_key = key if value == "" else ""
            if value:
                current[key] = value.strip('"').strip("'")
            else:
                current[key] = []
            continue
        list_match = re.match(r"-\s*(.*)$", line)
        if list_match and current_list_key:
            current.setdefault(current_list_key, []).append(list_match.group(1).strip('"').strip("'"))
    if current:
        items.append(current)
    for item in items:
        item["_label"] = label
    return items


def build_qxby_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for path, label in [(QXBY_DRAFT, "canon/drafts/qxby_batch_001.yaml"), (QXBY_MANIFEST, "sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml")]:
        for item in parse_simple_yaml_items(path, label):
            evidence = f"{label}:{item.get('item_id', item.get('term', 'item'))}"
            for key in [
                "normalized_term",
                "mapped_component_name",
                "mapped_component_category",
                "mapped_gesture_family",
                "mapped_sound_profile",
                "term",
                "internal_name",
                "raw_excerpt",
                "normalized_claim",
            ]:
                value = item.get(key)
                if isinstance(value, list):
                    for inner in value:
                        add_index(index, inner, evidence)
                elif value:
                    add_index(index, value, evidence)
                    if key in {"raw_excerpt", "normalized_claim"}:
                        for match in re.findall(r"[\w\u4e00-\u9fff]+", value):
                            add_index(index, match, evidence)
            for key in ["involved_terms", "aliases_detected"]:
                for inner in item.get(key, []) if isinstance(item.get(key), list) else []:
                    add_index(index, inner, evidence)
    return index


def merge_indexes(*indexes: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = defaultdict(list)
    for index in indexes:
        for key, evidence in index.items():
            for entry in evidence:
                if entry not in merged[key]:
                    merged[key].append(entry)
    return merged


def find_evidence(item: CoverageItem, index: dict[str, list[str]]) -> list[str]:
    if item.item_type in {"string_number", "string_sequence", "hui", "hui_target"}:
        # Avoid false positives from incidental numbers in prose. Location values
        # are reported as V1 runtime structures unless explicitly modeled later.
        return []
    evidence: list[str] = []
    for token in item.search_terms():
        keys = {token}
        if re.match(r"^[A-Za-z0-9_\-]+$", token):
            keys.add(token.lower())
        for key in keys:
            for entry in index.get(key, []):
                if entry not in evidence:
                    evidence.append(entry)
    return evidence


def collect_items(
    score_events: list[dict[str, str]],
    templates: list[dict[str, str]],
    components: list[dict[str, str]],
) -> tuple[dict[str, CoverageItem], dict[str, list[str]]]:
    items: dict[str, CoverageItem] = {}
    summary: dict[str, set[str]] = defaultdict(set)

    events_by_gesture: dict[str, list[str]] = defaultdict(list)
    for row in score_events:
        gid = row.get("gesture_id", "")
        if gid:
            events_by_gesture[gid].append(row.get("event_id", ""))
        for field_name in [
            "gesture_id",
            "raw_input",
            "normalized_input",
            "notation_pre_action",
            "notation_vibrato",
            "context_dependency",
            "inherited_from_event_id",
        ]:
            if is_value(row.get(field_name, "")):
                summary[field_name].add(row[field_name])

    def get(item_type: str, term: str, internal_name: str = "") -> CoverageItem:
        term = clean(term)
        internal_name = clean(internal_name)
        key = f"{item_type}\0{internal_name or term}"
        if key not in items:
            items[key] = CoverageItem(item_type=item_type, term=term, internal_name=internal_name)
            add_aliases(items[key])
        return items[key]

    for row in score_events:
        event_id = row.get("event_id", "")
        gid = row.get("gesture_id", "")
        if is_value(gid):
            item = get("gesture_id", gid, gid)
            item.source_in_v1.add("01_pieces/xianwengcao/score_events.csv:gesture_id")
            item.used_in_events.add(event_id)
            item.used_in_gestures.add(gid)
        if is_value(row.get("notation_pre_action", "")):
            item = get("pre_action", row["notation_pre_action"], row["notation_pre_action"])
            item.source_in_v1.add("01_pieces/xianwengcao/score_events.csv:notation_pre_action")
            item.used_in_events.add(event_id)
            item.used_in_gestures.add(gid)
        if is_value(row.get("notation_vibrato", "")):
            item = get("vibrato", row["notation_vibrato"], row["notation_vibrato"])
            item.source_in_v1.add("01_pieces/xianwengcao/score_events.csv:notation_vibrato")
            item.used_in_events.add(event_id)
            item.used_in_gestures.add(gid)
        if is_value(row.get("context_dependency", "")):
            item = get("context_dependency", row["context_dependency"], row["context_dependency"])
            item.source_in_v1.add("01_pieces/xianwengcao/score_events.csv:context_dependency")
            item.used_in_events.add(event_id)
            item.used_in_gestures.add(gid)
        if is_value(row.get("inherited_from_event_id", "")):
            term = f"{event_id} inherits {row['inherited_from_event_id']}"
            item = get("inherited_context_structure", term, term)
            item.source_in_v1.add("01_pieces/xianwengcao/score_events.csv:inherited_from_event_id")
            item.used_in_events.add(event_id)
            item.used_in_gestures.add(gid)

    for row in templates:
        gid = row.get("gesture_id", "")
        if gid:
            for field_name in [
                "gesture_id",
                "normalized_name",
                "primary_sound_type",
                "sound_profile",
                "gesture_family",
                "primary_string_no",
                "primary_hui",
                "primary_left_finger",
                "primary_right_action",
                "is_composite",
            ]:
                if is_value(row.get(field_name, "")):
                    summary[field_name].add(row[field_name])
        event_ids = events_by_gesture.get(gid, [])
        pairs = [
            ("sound_type", row.get("primary_sound_type", ""), row.get("primary_sound_type", "")),
            ("sound_profile", row.get("sound_profile", ""), row.get("sound_profile", "")),
            ("gesture_family", row.get("gesture_family", ""), row.get("gesture_family", "")),
            ("string_number", row.get("primary_string_no", ""), row.get("primary_string_no", "")),
            ("hui", row.get("primary_hui", ""), row.get("primary_hui", "")),
            ("left_finger", row.get("primary_left_finger", ""), row.get("primary_left_finger", "")),
            ("right_hand_action", row.get("primary_right_action", ""), row.get("primary_right_action", "")),
        ]
        for item_type, term, internal_name in pairs:
            if not is_value(term):
                continue
            item = get(item_type, term, internal_name)
            item.source_in_v1.add(f"00_global/gesture_templates.csv:{item_type}")
            item.used_in_gestures.add(gid)
            item.used_in_events.update(event_ids)
        if clean(row.get("is_composite", "")).lower() == "true":
            item = get("composite_gesture_structure", gid, gid)
            item.source_in_v1.add("00_global/gesture_templates.csv:is_composite")
            item.used_in_gestures.add(gid)
            item.used_in_events.update(event_ids)

    for row in components:
        gid = row.get("gesture_id", "")
        event_ids = events_by_gesture.get(gid, [])
        for field_name in [
            "component_name",
            "component_category",
            "component_sound_type",
            "component_hand",
            "right_action",
            "string_no",
            "string_sequence",
            "hui",
            "hui_target",
            "motion_returns",
            "is_sound_producing",
            "left_finger",
            "right_finger",
            "harmonic_role",
        ]:
            if is_value(row.get(field_name, "")):
                summary[field_name].add(row[field_name])

        component_name = row.get("component_name", "")
        category = row.get("component_category", "")
        if is_value(component_name):
            item_type = "component_name"
            if category in {"pre_slide"}:
                item_type = "pre_action"
            elif category in {"single_slide", "returning_slide", "micro_returning_slide", "slow_slide", "repeated_motion"}:
                item_type = "post_motion"
            elif category == "vibrato":
                item_type = "vibrato"
            item = get(item_type, component_name, component_name)
            item.source_in_v1.add("00_global/gesture_components.csv:component_name")
            item.used_in_gestures.add(gid)
            item.used_in_events.update(event_ids)
            if category:
                item.notes.add(f"component_category={category}")

        pairs = [
            ("component_category", category, category),
            ("sound_type", row.get("component_sound_type", ""), row.get("component_sound_type", "")),
            ("right_hand_action", row.get("right_action", ""), row.get("right_action", "")),
            ("right_hand_finger", row.get("right_finger", ""), row.get("right_finger", "")),
            ("left_finger", row.get("left_finger", ""), row.get("left_finger", "")),
            ("string_number", row.get("string_no", ""), row.get("string_no", "")),
            ("string_sequence", row.get("string_sequence", ""), row.get("string_sequence", "")),
            ("hui", row.get("hui", ""), row.get("hui", "")),
            ("hui_target", row.get("hui_target", ""), row.get("hui_target", "")),
        ]
        if row.get("component_sound_type") == "泛音" and is_value(row.get("left_finger", "")):
            pairs.append(("harmonic_touch_finger", row["left_finger"], row["left_finger"]))
        for item_type, term, internal_name in pairs:
            if not is_value(term):
                continue
            item = get(item_type, term, internal_name)
            item.source_in_v1.add(f"00_global/gesture_components.csv:{item_type}")
            item.used_in_gestures.add(gid)
            item.used_in_events.update(event_ids)

        if clean(row.get("motion_returns", "")).lower() == "true" and is_value(component_name):
            item = get("post_motion_return_structure", component_name, component_name)
            item.source_in_v1.add("00_global/gesture_components.csv:motion_returns")
            item.used_in_gestures.add(gid)
            item.used_in_events.update(event_ids)

    return items, {k: sorted(v) for k, v in summary.items()}


def classify_items(
    items: dict[str, CoverageItem],
    canon_index: dict[str, list[str]],
    qxby_index: dict[str, list[str]],
    internal_index: dict[str, list[str]],
) -> None:
    structural_types = {
        "string_number",
        "string_sequence",
        "hui",
        "hui_target",
        "gesture_id",
        "composite_gesture_structure",
        "inherited_context_structure",
        "post_motion_return_structure",
    }
    for item in items.values():
        item.evidence_in_qxby_batch_001 = find_evidence(item, qxby_index)
        item.evidence_in_canon_seed = find_evidence(item, canon_index)
        item.evidence_in_internal_ontology = find_evidence(item, internal_index)

        if item.evidence_in_qxby_batch_001:
            item.coverage_status = "qxby_batch_001_draft_covered"
            item.recommended_action = "No duplicate Batch002 evidence recommended."
            item.batch002_priority = "defer"
        elif item.evidence_in_canon_seed:
            item.coverage_status = "project_canon_seed_covered"
            item.recommended_action = "Optional external source evidence can be added if this is a reusable canon concept."
            item.batch002_priority = "P1" if item.item_type not in structural_types else "P2"
        elif item.evidence_in_internal_ontology:
            item.coverage_status = "internal_ontology_only"
            item.recommended_action = "Add external source evidence if this observed V1 concept should be promoted into canon evidence."
            item.batch002_priority = "P0" if item.item_type not in structural_types else "P2"
        else:
            item.coverage_status = "v1_runtime_only"
            item.recommended_action = "Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept."
            item.batch002_priority = "P0" if item.item_type not in structural_types else "P2"

        if item.term.isdigit() and item.item_type in {"string_number", "hui", "hui_target"}:
            item.notes.add("Structural pitch/location value; not necessarily a source-evidence term.")


def item_to_json(item: CoverageItem) -> dict[str, Any]:
    return {
        "item_id": item.item_id,
        "term": item.term,
        "internal_name": item.internal_name,
        "item_type": item.item_type,
        "source_in_v1": sorted(item.source_in_v1),
        "coverage_status": item.coverage_status,
        "used_in_events": sorted(item.used_in_events),
        "used_in_gestures": sorted(item.used_in_gestures),
        "evidence_in_canon_seed": item.evidence_in_canon_seed,
        "evidence_in_qxby_batch_001": item.evidence_in_qxby_batch_001,
        "recommended_action": item.recommended_action,
        "batch002_priority": item.batch002_priority,
        "notes": "; ".join(sorted(item.notes)),
    }


def build_report_data(
    score_events: list[dict[str, str]],
    templates: list[dict[str, str]],
    components: list[dict[str, str]],
    items: dict[str, CoverageItem],
    extraction_summary: dict[str, list[str]],
) -> dict[str, Any]:
    sorted_items = sorted(items.values(), key=lambda x: (x.coverage_status, x.item_type, x.internal_name or x.term))
    summary: dict[str, list[str]] = {
        "qxby_batch_001_draft_covered": [],
        "project_canon_seed_covered": [],
        "internal_ontology_only": [],
        "v1_runtime_only": [],
        "missing_or_unmapped": [],
        "ambiguous": [],
        "recommended_batch002": [],
    }
    for item in sorted_items:
        summary.setdefault(item.coverage_status, []).append(item.item_id)
        if item.batch002_priority in {"P0", "P1"}:
            summary["recommended_batch002"].append(item.item_id)

    successful = [
        item.item_id
        for item in sorted_items
        if item.coverage_status in {"qxby_batch_001_draft_covered", "project_canon_seed_covered", "internal_ontology_only"}
    ]
    gaps = [
        item.item_id
        for item in sorted_items
        if item.coverage_status in {"v1_runtime_only", "missing_or_unmapped", "ambiguous"}
    ]
    return {
        "audit_type": "blind_v1_to_canon_coverage",
        "piece_id": "XWC",
        "total_score_events": len(score_events),
        "total_gestures": len({row["gesture_id"] for row in templates if row.get("gesture_id")}),
        "total_components": len(components),
        "coverage_summary": summary,
        "extraction_summary": extraction_summary,
        "items": [item_to_json(item) for item in sorted_items],
        "bridge_assessment": {
            "structure_validated": bool(successful) and len(score_events) > 0,
            "successful_mappings": successful,
            "gaps_found": gaps,
            "risks": [
                "String/hui/location values are observable runtime structures, but they are not all canon source-evidence terms.",
                "English finger role names from V1 are not consistently modeled as standalone canon seed terms.",
                "QXBY_BATCH_001 is draft/manual transcription evidence and should not be treated as verified.",
            ],
        },
    }


def md_list(values: list[str], empty: str = "_None observed._") -> str:
    if not values:
        return empty
    return "\n".join(f"- {value}" for value in values)


def md_table(items: list[dict[str, Any]], limit: int | None = None) -> str:
    rows = items[:limit] if limit else items
    if not rows:
        return "_None._"
    lines = ["| item | type | status | v1 usage | evidence | action |", "|---|---|---|---|---|---|"]
    for item in rows:
        usage_bits = []
        if item["used_in_events"]:
            usage_bits.append("events " + ", ".join(item["used_in_events"][:8]) + ("..." if len(item["used_in_events"]) > 8 else ""))
        if item["used_in_gestures"]:
            usage_bits.append("gestures " + ", ".join(item["used_in_gestures"][:6]) + ("..." if len(item["used_in_gestures"]) > 6 else ""))
        evidence = item["evidence_in_qxby_batch_001"] or item["evidence_in_canon_seed"] or []
        lines.append(
            "| {term} | {typ} | {status} | {usage} | {evidence} | {action} |".format(
                term=item["term"].replace("|", "\\|"),
                typ=item["item_type"],
                status=item["coverage_status"],
                usage="<br>".join(usage_bits) if usage_bits else "",
                evidence="<br>".join(evidence[:4]).replace("|", "\\|") if evidence else "",
                action=item["recommended_action"].replace("|", "\\|"),
            )
        )
    return "\n".join(lines)


def write_markdown(report: dict[str, Any], input_files: list[Path]) -> None:
    items = report["items"]
    by_status: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        by_status[item["coverage_status"]].append(item)

    recommended = [item for item in items if item["batch002_priority"] in {"P0", "P1"}]
    already = by_status["qxby_batch_001_draft_covered"]
    extraction = report["extraction_summary"]

    lines = [
        "# V1-to-Canon Blind Coverage Audit",
        "",
        "## 1. Executive Summary",
        "",
        f"- Audit type: `{report['audit_type']}`.",
        f"- Piece: `{report['piece_id']}`.",
        f"- Score events read: {report['total_score_events']}.",
        f"- Gesture templates read: {report['total_gestures']}.",
        f"- Gesture components read: {report['total_components']}.",
        f"- Coverage items derived from V1 runtime data: {len(items)}.",
        f"- QXBY_BATCH_001 draft covered items: {len(by_status['qxby_batch_001_draft_covered'])}.",
        f"- Canon seed covered without QXBY draft evidence: {len(by_status['project_canon_seed_covered'])}.",
        f"- Internal ontology only: {len(by_status['internal_ontology_only'])}.",
        f"- V1 runtime only: {len(by_status['v1_runtime_only'])}.",
        "",
        "## 2. Blind Audit Declaration",
        "",
        "This audit is blind: coverage items were derived from `score_events.csv`, `gesture_templates.csv`, and `gesture_components.csv` before comparison. No manually preset missing-term list was used as evidence or as a candidate source.",
        "",
        "## 3. Input Files",
        "",
        md_list([str(path.relative_to(ROOT)) + (" (missing)" if not path.exists() else "") for path in input_files]),
        "",
        "## 4. V1.0 Runtime Extraction",
        "",
        "### Gesture IDs",
        md_list(extraction.get("gesture_id", [])),
        "",
        "### Component Names",
        md_list(extraction.get("component_name", [])),
        "",
        "### Primary Sound Types",
        md_list(extraction.get("primary_sound_type", [])),
        "",
        "### Gesture Families",
        md_list(extraction.get("gesture_family", [])),
        "",
        "### Sound Profiles",
        md_list(extraction.get("sound_profile", [])),
        "",
        "### Left/Right Hand Terms",
        md_list(sorted(set(extraction.get("primary_left_finger", []) + extraction.get("left_finger", []) + extraction.get("right_finger", []) + extraction.get("primary_right_action", []) + extraction.get("right_action", [])))),
        "",
        "### Hui / String / Context Dependency",
        md_list(sorted(set(extraction.get("primary_hui", []) + extraction.get("hui", []) + extraction.get("hui_target", []) + extraction.get("primary_string_no", []) + extraction.get("string_no", []) + extraction.get("string_sequence", []) + extraction.get("context_dependency", []) + extraction.get("inherited_from_event_id", [])))),
        "",
        "## 5. Canon Seed Coverage Comparison",
        "",
        md_table(by_status["project_canon_seed_covered"]),
        "",
        "## 6. QXBY_BATCH_001 Draft Coverage Comparison",
        "",
        md_table(by_status["qxby_batch_001_draft_covered"]),
        "",
        "## 7. internal_ontology_only Items",
        "",
        md_table(by_status["internal_ontology_only"]),
        "",
        "## 8. v1_runtime_only Items",
        "",
        md_table(by_status["v1_runtime_only"]),
        "",
        "## 9. missing_or_unmapped Items",
        "",
        md_table(by_status["missing_or_unmapped"]),
        "",
        "## 10. ambiguous Items",
        "",
        md_table(by_status["ambiguous"]),
        "",
        "## 11. Recommended QXBY_BATCH_002 Items",
        "",
        md_table(recommended),
        "",
        "## 12. Items Not Recommended For Duplicate Evidence",
        "",
        md_table(already),
        "",
        "## 13. skills-canon-v1 Bridge Assessment",
        "",
        "### Validated",
        "",
        md_list(report["bridge_assessment"]["successful_mappings"][:80]),
        "",
        "### Gaps Exposed",
        "",
        md_list(report["bridge_assessment"]["gaps_found"]),
        "",
        "### Fields That May Need Future V1 Minimal Patch",
        "",
        md_list(
            [
                "Standalone hand/finger role vocabulary if these should become canonized terms instead of component attributes.",
                "Explicit source-evidence mapping for string/hui structural values if future canon scope requires location evidence.",
                "A clearer split between gesture_id runtime templates and reusable canon technique IDs.",
            ]
        ),
        "",
        "## 14. Next Steps",
        "",
        md_list(
            [
                "Review P0/P1 candidate list and decide which runtime-observed items are true canon-source targets.",
                "Add external evidence only for candidates produced by this blind comparison.",
                "Keep QXBY_BATCH_001 draft status separate from verified evidence until human review is complete.",
            ]
        ),
        "",
    ]
    (REPORT_DIR / "v1_to_canon_coverage.md").write_text("\n".join(lines), encoding="utf-8")


def canon_bucket(item: dict[str, Any]) -> str:
    item_type = item["item_type"]
    if item_type in {"component_name", "component_category", "right_hand_action", "right_hand_finger", "left_finger", "harmonic_touch_finger", "pre_action", "post_motion", "vibrato"}:
        return "component"
    if item_type in {"gesture_family", "sound_profile", "sound_type", "composite_gesture_structure"}:
        return "technique_rule"
    if item_type in {"context_dependency", "inherited_context_structure"}:
        return "dapu_rule"
    if item_type == "alias":
        return "alias_rule"
    return "term"


def required_material(item: dict[str, Any]) -> str:
    if item["batch002_priority"] == "defer":
        return "None; already covered or not recommended for Batch002."
    if item["item_type"] in {"string_number", "hui", "hui_target", "string_sequence"}:
        return "Manual explanation if canon scope expands to structural locations; OCR is not currently recommended."
    return "OCR image, original excerpt, page number, and brief manual note tying the source text to the observed V1 item."


def write_candidate_markdown(report: dict[str, Any]) -> None:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in report["items"]:
        priority = item["batch002_priority"]
        if item["coverage_status"] == "qxby_batch_001_draft_covered":
            priority = "Already covered"
        groups[priority].append(item)

    lines = [
        "# QXBY_BATCH_002 Candidate List",
        "",
        "This candidate list is generated only from the blind V1-to-canon coverage audit. It does not use a manually preset gap list and it does not create QXBY_BATCH_002.",
        "",
    ]
    for title in ["P0", "P1", "P2", "Already covered", "defer"]:
        if title == "defer":
            header = "Deferred / Not Recommended"
        elif title == "Already covered":
            header = "Already covered"
        else:
            header = title
        lines.extend([f"## {header}", ""])
        entries = groups.get(title, [])
        if not entries:
            lines.extend(["_None._", ""])
            continue
        for item in entries:
            reason = {
                "P0": "仙翁操 V1 uses this item and no QXBY draft/canon seed evidence was found at the same level.",
                "P1": "仙翁操 V1 uses this item and canon seed covers it, but QXBY_BATCH_001 draft evidence was not found.",
                "P2": "Observed from V1, but current evidence need is lower because it is structural/location-like or not an immediate source term.",
                "Already covered": "QXBY_BATCH_001 draft already contains matching evidence; duplicate Batch002 evidence is not recommended.",
                "defer": "No Batch002 action recommended.",
            }.get(title, "No Batch002 action recommended.")
            lines.extend(
                [
                    f"### {item['term']} (`{item['item_type']}`)",
                    "",
                    f"- Why: {reason}",
                    f"- V1 source: {', '.join(item['source_in_v1'])}",
                    f"- Events: {', '.join(item['used_in_events']) if item['used_in_events'] else 'not directly event-bound'}",
                    f"- Gestures: {', '.join(item['used_in_gestures']) if item['used_in_gestures'] else 'not directly gesture-bound'}",
                    f"- Current coverage_status: `{item['coverage_status']}`",
                    f"- Canon category: `{canon_bucket(item)}`",
                    f"- Needed user material: {required_material(item)}",
                    "",
                ]
            )
    (REPORT_DIR / "qxby_batch_002_candidate_list.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    score_events = read_csv(V1_SCORE)
    templates = read_csv(V1_TEMPLATES)
    components = read_csv(V1_COMPONENTS)

    items, extraction_summary = collect_items(score_events, templates, components)

    canon_index = merge_indexes(
        build_jsonish_index(ROOT / "canon" / "terms.yaml", "terms", "canon/terms.yaml"),
        build_jsonish_index(ROOT / "canon" / "component_lexicon.yaml", "components", "canon/component_lexicon.yaml"),
        build_jsonish_index(ROOT / "canon" / "gesture_families.yaml", "gesture_families", "canon/gesture_families.yaml"),
        build_jsonish_index(ROOT / "canon" / "alias_rules.yaml", "alias_rules", "canon/alias_rules.yaml"),
        build_jsonish_index(ROOT / "canon" / "technique_rules.yaml", "techniques", "canon/technique_rules.yaml"),
        build_jsonish_index(ROOT / "canon" / "validation_rules.yaml", None, "canon/validation_rules.yaml"),
    )
    internal_index = merge_indexes(
        build_csv_index(ROOT / "00_global" / "gesture_component_lexicon.csv", ["component_name", "zh_name"], "00_global/gesture_component_lexicon.csv"),
        build_csv_index(ROOT / "00_global" / "gesture_family_catalog.csv", ["gesture_family", "zh_name"], "00_global/gesture_family_catalog.csv"),
        build_jsonish_index(ROOT / "00_global" / "guqin_fingering_ontology.yaml", None, "00_global/guqin_fingering_ontology.yaml"),
        build_jsonish_index(ROOT / "00_global" / "alias_rules.yaml", None, "00_global/alias_rules.yaml"),
        build_jsonish_index(ROOT / "06_docs" / "GESTURE_ONTOLOGY.md", None, "06_docs/GESTURE_ONTOLOGY.md"),
    )
    qxby_index = build_qxby_index()
    classify_items(items, canon_index, qxby_index, internal_index)

    report = build_report_data(score_events, templates, components, items, extraction_summary)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "v1_to_canon_coverage.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    input_files = [
        V1_SCORE,
        V1_TEMPLATES,
        V1_COMPONENTS,
        V1_PHRASES,
        V1_RECORDING_SCRIPT,
        V1_RECORDING_BATCHES,
        *CANON_FILES,
        QXBY_DRAFT,
        QXBY_MANIFEST,
        *ONTOLOGY_FILES,
        *SKILL_FILES,
    ]
    write_markdown(report, input_files)
    write_candidate_markdown(report)

    print(f"Wrote {REPORT_DIR / 'v1_to_canon_coverage.md'}")
    print(f"Wrote {REPORT_DIR / 'v1_to_canon_coverage.json'}")
    print(f"Wrote {REPORT_DIR / 'qxby_batch_002_candidate_list.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
