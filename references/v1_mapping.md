# V1 Mapping

## 1. Background

Phase S0 creates non-invasive skill infrastructure for canon building and dapu parsing. Gesture Ontology v1.1 remains the field authority. Existing V1 runtime, renderer, smoke tests, score events, gesture templates, gesture components, sample assets, and recording task files are not modified in this phase.

## 2. Canon To V1 Mapping

| Skill output | V1 target or compatible location |
| --- | --- |
| `technique_id` | `canon_techniques.id` or equivalent future V1 canon key |
| `name_zh` | `canon_techniques.name_zh` |
| `category` | `canon_techniques.category` |
| `definition` | `canon_techniques.definition` |
| `primary_sound_type` | `canon_techniques.primary_sound_type` |
| `sound_profile` | `canon_techniques.sound_profile` |
| `gesture_family` | `canon_techniques.gesture_family` |
| `component_rules` | `canon_techniques.component_json` or `mapping_json` |
| `cyber_guqin_mapping` | `canon_techniques.mapping_json` |
| `source_refs` | `canon_sources` or `canon_refs` |
| `review_status` | `canon_techniques.review_status` |
| `confidence` | `canon_techniques.confidence` |

Current V1 already has ontology-level CSV/YAML equivalents for components, families, aliases, schema contract, and sample selection policy under `00_global/`. Phase S0 fixtures do not replace those files.

## 3. Dapu Event IR To V1 Mapping

| Dapu Event IR field | V1 target or suggested target |
| --- | --- |
| `event_id` | `events.id` or current `score_events.event_id` |
| `event_group_id` | `events.event_group_id` |
| `source_token` | `events.source_token` or current `score_events.raw_input` |
| `normalized_token` | current `score_events.normalized_input` |
| `position` | `events.position_index` or future structured position fields |
| `primary_sound_type` | `events.primary_sound_type`; current V1 may infer from `gesture_id` or require minimal patch |
| `sound_profile` | `events.sound_profile` or `events.context_json` |
| `gesture_family` | `events.gesture_family` or `events.context_json` |
| `components` | `events.component_json` or `events.context_json` |
| `notation_pre_action` | current `score_events.notation_pre_action` |
| `notation_vibrato` | current `score_events.notation_vibrato` |
| `context_dependency` | current `score_events.context_dependency` |
| `inherits_string_from_event_id` | `events.inherits_string_from_event_id` |
| `inherits_position_from_event_id` | `events.inherits_position_from_event_id` |
| `inherits_right_hand_from_event_id` | `events.inherits_right_hand_from_event_id` |
| `certainty` | `events.certainty` |
| `needs_review` | `events.needs_review` |
| `source_status` | `events.source_status` or current `score_events.parse_status` |

## 4. Recording Script Ingest Future Mapping

Future `recording_script_ingest` may read `recording_batches.md`, `recording_script.csv`, and `recording_script_human.csv` as legacy execution artifacts. It must not treat them as score authority and must not rewrite, reorder, delete, or merge the current 71 recording tasks. A future enriched recording item may link `script_id`, `recording_take_no`, realization fields, and sample instructions back to immutable score event IDs.

## 5. Current V1 Missing Fields

Current `score_events.csv` has `event_id`, `raw_input`, `normalized_input`, `gesture_id`, `notation_pre_action`, `notation_vibrato`, `context_dependency`, `inherited_from_event_id`, and `parse_status`. It does not yet expose first-class `primary_sound_type`, `sound_profile`, `gesture_family`, `components`, per-inheritance fields, `certainty`, `needs_review`, or `source_status`.

## 6. Suggested Minimal Patch

Later, after Phase S0, add a narrow event-side compatibility layer or columns for `primary_sound_type`, `sound_profile`, `gesture_family`, `component_json`, `certainty`, `needs_review`, `source_status`, and explicit inheritance fields. Keep realization defaults in `sample_selection_policy` and sample assets, not in score facts.

## 7. No Patch In This Phase

This phase does not execute any V1 patch. It creates schemas, validators, fixtures, reports, and skill documentation only.
