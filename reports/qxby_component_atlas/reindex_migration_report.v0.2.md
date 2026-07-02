# QXBY Full Atlas Reindex Migration Report v0.2

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `CATEGORY_REINDEXED_COMPONENT_IDS`, `SOURCE_REFERENCE_IMAGE`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`

## Scope Confirmation

This task is only QXBY full atlas category-based reindexing, legacy alias normalization, construction template migration, regression goldset migration, and skill ID-normalization update.

It is not score import, LXY P7 processing, Dapu IR authority, parser finalization, recording plan, sample ingest, ML training, render, R0/R1/R2/E/F, or Sanman formal collection plan.

## Results

- v0.1 registry found: `true`
- v0.2 reindexed registry created: `true`
- Full atlas components represented: `174`
- Auxiliary numeric components: `7`
- Auxiliary left-finger-name components: `5`
- Legacy `COMP-001..038` mapping count: `38`
- v0.1 `COMP-100..273` mapping count: `174`
- Construction templates migrated: `50`
- P1-P6 goldset fixture produced: `true`
- P1-P6 forbidden-output fixture produced: `true`

## Category Ranges

| Category | Family | Assigned count | Assigned range |
| --- | --- | --- | --- |
| 右手指法-一弦单弹 | right_hand_single_string_family | 23 | COMP-101..COMP-123 |
| 右手指法-两弦双弹 | right_hand_two_string_family | 17 | COMP-201..COMP-217 |
| 右手指法-数弦连弹 | right_hand_multi_string_family | 9 | COMP-301..COMP-309 |
| 左手指法-本位取音 | left_hand_base_position_family | 38 | COMP-401..COMP-438 |
| 左手指法-隔位取音 | left_hand_interval_position_family | 33 | COMP-501..COMP-533 |
| 左手指法-散弦取音 | left_hand_open_string_family | 9 | COMP-601..COMP-609 |
| 音位谱字 | sound_position_marker_family | 8 | COMP-701..COMP-708 |
| 节奏谱字 | rhythm_marker_family | 22 | COMP-801..COMP-822 |
| 通用谱字 | generic_score_marker_family | 15 | COMP-901..COMP-915 |

## Left Finger Name Reference

`左手指名.zip` was read as user-authorized reference evidence only. It contains: `中指, 名指, 大指, 跪指, 食指`. Images were not copied into `sources/`.

## Boundary

No source zip extraction was rerun for the full atlas, no source images were rewritten, and the v0.1 registry was not overwritten.

## Validation

- JSON validation: `PASS`
- Reindex sanity: `PASS full=174 aux=12 legacy=38 source_v01=174 templates=50 gold_phrases=6 forbidden=23`
- `git diff --check`: `PASS`
- Note: v0.2 primary IDs intentionally overlap some v0.1 numeric strings; identity is disambiguated by `primary_id_system=category_based_v0_2` versus `source_component_id_v0_1` fields.
