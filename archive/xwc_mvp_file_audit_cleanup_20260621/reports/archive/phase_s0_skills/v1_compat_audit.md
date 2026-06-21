# V1 Compatibility Audit

## Scope

This audit is for Phase S0 / Skills Foundation. It is read-only with respect to existing Cyber Guqin V1 runtime, renderer, audio generation, smoke tests, ontology, score events, gesture files, sample assets, and the current Xianwengcao recording tasks.

## Current V1 Authority Files

Gesture Ontology v1.1 is present and remains the field authority:

- `00_global/guqin_fingering_ontology.yaml`
- `00_global/gesture_component_lexicon.csv`
- `00_global/gesture_family_catalog.csv`
- `00_global/alias_rules.yaml`
- `00_global/schema_contract.yaml`
- `00_global/sample_selection_policy.yaml`
- `06_docs/GESTURE_ONTOLOGY.md`

No `cyber_guqin_skills_framework_review.md` file was found in the project root during this audit, so this report follows the pasted task requirements and the V1.1 ontology files.

## Existing V1 Data Tables And Fields

Core ontology and catalog files:

- `gesture_component_lexicon.csv`: `component_name`, `zh_name`, `component_category`, `hand`, `standard_internal_name`, `aliases`, `description`
- `gesture_family_catalog.csv`: `gesture_family`, `zh_name`, `description`, `examples`, `requires_components`, `default_requires_context_sample`
- `alias_rules.yaml`: right-hand basic aliases, right-hand sequence aliases, and left-hand sound aliases
- `schema_contract.yaml`: V1.1 constraints for sound type, score events, templates, components, sample assets, notation pre-actions, post motions, and atomics
- `sample_selection_policy.yaml`: Sanman realization preference for default pressed-note `chuo`

Xianwengcao score and recording execution files:

- `score_events.csv`: `event_id`, `piece_id`, `phrase_id`, `event_no`, `raw_input`, `normalized_input`, `gesture_id`, `notation_pre_action`, `notation_vibrato`, `event_role`, `context_dependency`, `inherited_from_event_id`, `parse_status`, `notes`
- `recording_script.csv`: `script_id`, `recording_id`, `order_no`, `event_id`, `event_range`, `gesture_id`, `normalized_name`, `expected_sample_type`, `realization_variant`, `realization_pre_action`, `realization_vibrato`, `recommended_pause_s`, `need_full_decay`, `notes`
- `recording_script_human.csv`: recording take metadata, score linkage, gesture fields, realization fields, pause/full-decay instructions, and human instructions
- `recording_batches.md`: human recording order and execution guidance; it is not score authority

Sample and recording assets:

- `sample_assets.csv`: sample ID, qinist/qin/tuning, gesture and realization fields, file path, quality, source linkage, extraction method, and notes
- `recording_segments.csv`: `segment_id`, `recording_id`, `event_id`, `start_time`, `end_time`, `status`, `notes`

Runtime and review scripts exist under `05_scripts/`, including `render_audio.py`, `smoke_test.py`, recording script generation/export helpers, dummy sample generation, rhythm generation, and audio viability review.

## V1 Structure Found

- Dapu Mode is represented by `01_pieces/xianwengcao/score_events.csv` plus phrase structure.
- Arrangement/realization concerns are represented separately by recording scripts, sample selection policy, and sample assets.
- Digital Qinist Core is represented by `00_global/qinists.csv`, `00_global/qinist_profiles/QINIST_001_sanman.yaml`, qin/tuning tables, and sample assets.
- QINIST_001 / Sanman profile exists at `00_global/qinist_profiles/QINIST_001_sanman.yaml`.
- Parser/validator/renderer surfaces are currently scripts and contracts rather than a formal Dapu IR package.

## Skills Output Mapping

Canon output maps cleanly to existing V1 ontology surfaces for components, gesture families, aliases, and schema rules. A future formal canon table can use the mapping in `references/v1_mapping.md`.

Dapu Event IR maps partially to current `score_events.csv`:

- `event_id` -> `event_id`
- `source_token` -> `raw_input`
- `normalized_token` -> `normalized_input`
- `gesture_id_candidate` -> `gesture_id`
- `notation_pre_action` -> `notation_pre_action`
- `notation_vibrato` -> `notation_vibrato`
- `context_dependency` -> `context_dependency`
- `source_status` -> `parse_status`

Recording script ingest, if later implemented, should be a read-only projection from execution files into semantic recording items. It must not rewrite the 71 recording tasks and must not treat recording batches as score truth.

## Current V1 Field Gaps

The current score table does not have first-class fields for:

- `event_group_id`
- `position`
- `primary_sound_type`
- `sound_profile`
- `gesture_family`
- `components` / `component_json`
- `inherits_string_from_event_id`
- `inherits_position_from_event_id`
- `inherits_right_hand_from_event_id`
- `certainty`
- `needs_review`

`inherited_from_event_id` exists as one coarse field, but Dapu Event IR separates string, position, and right-hand inheritance.

## Recommended Future Minimal Patch

After Phase S0, add a narrow compatibility layer or columns for first-class Dapu Event IR fields: `primary_sound_type`, `sound_profile`, `gesture_family`, `component_json`, `certainty`, `needs_review`, `source_status`, and explicit inheritance fields. Keep Sanman defaults in `sample_selection_policy`, `qinist_profile`, interpretations, realization, and sample selection.

Do not add `pressed_compound_motion` as a gesture family. Keep `compound_pressed_motion` as `sound_profile` only.

## Non-Invasive Confirmations

- This phase does not modify V1 runtime.
- This phase does not modify renderer code.
- This phase does not modify audio generation.
- This phase does not modify `smoke_test.py`.
- This phase does not modify ontology, score events, gesture templates, gesture components, sample assets, recording scripts, recording script human files, or `recording_batches.md`.
- This phase does not reorder, delete, merge, or ingest the current Xianwengcao recording tasks.
- This phase outputs this audit to `reports/v1_compat_audit.md`, not `docs/v1_compat_audit.md`.
