# Skills V1 Integration Report

## Status

Warning / partial pass.

Schemas, references, validators, fixtures, and reports have been created and verified. The only remaining installation step is moving the staged skill docs into `.agents/skills/`, which was blocked by the prior managed sandbox permissions. After the staged `SKILL.md` files are installed to `.agents/skills`, Phase S0 can be treated as complete.

## Phase

Phase S0 / Skills Foundation was executed as a non-invasive initialization pass. Existing V1 runtime, renderer, audio generation, smoke tests, ontology files, score events, gesture files, sample assets, and Xianwengcao recording task files were not modified.

## Files Created

Created foundation files:

- `schemas/canon_component.schema.json`
- `schemas/canon_gesture_family.schema.json`
- `schemas/canon_alias_rule.schema.json`
- `schemas/canon_technique.schema.json`
- `schemas/dapu_token.schema.json`
- `schemas/dapu_event_ir.schema.json`
- `references/v1_mapping.md`
- `references/normalization_rules.md`
- `references/validation_rules.md`
- `scripts/validate_canon.py`
- `scripts/validate_dapu_ir.py`
- `scripts/check_v1_compat.py`
- `tests/fixtures/canon_minimal.yaml`
- `tests/fixtures/xianwengcao_tokens_minimal.jsonl`
- `tests/fixtures/xianwengcao_events_minimal.jsonl`
- `reports/v1_compat_audit.md`
- `reports/validate_canon_report.json`
- `reports/validate_dapu_ir_report.json`
- `reports/check_v1_compat_report.json`
- `reports/skills_v1_integration_report.md`
- `reports/skill_install_staging/guqin-canon-builder/SKILL.md`
- `reports/skill_install_staging/guqin-dapu-parser/SKILL.md`
- `reports/skill_install_instructions.md`

Blocked by sandbox permissions:

- `.agents/skills/guqin-canon-builder/SKILL.md`
- `.agents/skills/guqin-dapu-parser/SKILL.md`

The `.agents` directory was readable but not writable in the managed sandbox used during the prior run, so the skill docs could not be created at the requested path. They have now been staged under `reports/skill_install_staging/`, with installation instructions in `reports/skill_install_instructions.md`.

## Validator Results

The command `python` is not available on this machine. The scripts were run with `python3`.

- `python3 scripts/validate_canon.py`: passed
- `python3 scripts/validate_dapu_ir.py`: passed
- `python3 scripts/check_v1_compat.py`: passed

The JSON outputs were written to:

- `reports/validate_canon_report.json`
- `reports/validate_dapu_ir_report.json`
- `reports/check_v1_compat_report.json`

## Minimal Fixtures

`canon_minimal.yaml` covers:

- `bo=擘`, with `pi`/`劈` as aliases only
- `po=泼`, `la=剌`, `yan=罨`
- `chuo=绰`, `zhu=注`, `shang=上`, `zhuang=撞`
- `qiaqi=掐起`, `cuo=撮`, `fanghe=放合`, `yinghe=应合`, `fenkai=分开`
- `fenkai` as `gesture_family=compound_both_hands` and `sound_profile=compound_pressed_motion`

`xianwengcao_events_minimal.jsonl` covers:

- `SAN_TIAO_7`
- `AN_RING_10_GOU_5`
- `AN_RING_10_8_GOU_3` with `notation_pre_action=zhu`
- `AN_THUMB_9_GOU_6_SHANG_79`
- `AN_THUMB_9_GOU_4_ZHUANG` with `notation_pre_action=zhu`
- `AN_RING_10_QIAQI`
- `FAN_DA7_ZHONG7_CUO_6_1`

The fixture keeps default Sanman `chuo` out of event facts, preserves explicit `zhu`, encodes `上` and `撞` as components, classifies `撞` as `micro_returning_slide`, `掐起` as `left_hand_sound`, and `撮` as `simultaneous_pluck`.

## V1 Field Gaps

The compatibility check recommends a later minimal patch for first-class Dapu Event IR fields:

- `certainty`
- `components`
- `event_group_id`
- `gesture_family`
- `inherits_position_from_event_id`
- `inherits_right_hand_from_event_id`
- `inherits_string_from_event_id`
- `needs_review`
- `position`
- `primary_sound_type`
- `sound_profile`

Current V1 maps core score facts through `score_events.csv` fields such as `event_id`, `raw_input`, `normalized_input`, `gesture_id`, `notation_pre_action`, `notation_vibrato`, `context_dependency`, and `parse_status`.

## Non-Invasive Confirmations

- No V1 runtime patch was executed.
- No renderer refactor was executed.
- No audio generation change was executed.
- No `smoke_test.py` change was executed.
- No ontology or existing V1 data file was modified.
- No `recording_batches.md` ingest was implemented.
- No `recording_items_enriched.jsonl` was generated.
- No `enrich_recording_batches.py` or `validate_recording_items.py` was created.
- The current Xianwengcao recording tasks were not modified, reordered, deleted, merged, or enriched.

## Next Steps

1. Install the staged skill docs from `reports/skill_install_staging/` into `.agents/skills/` using `reports/skill_install_instructions.md`.
2. After the skill docs exist at `.agents/skills/guqin-canon-builder/SKILL.md` and `.agents/skills/guqin-dapu-parser/SKILL.md`, Phase S0 can be considered complete.
3. In a later phase, implement only the recommended minimal V1 compatibility patch after review.
4. Defer recording script ingest and `recording_items_enriched.jsonl` generation to the later dedicated phase.
