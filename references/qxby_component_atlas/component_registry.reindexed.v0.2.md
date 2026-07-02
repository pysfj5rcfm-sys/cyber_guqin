# QXBY Full Component Atlas Reindexed Registry v0.2

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `CATEGORY_REINDEXED_COMPONENT_IDS`, `SOURCE_REFERENCE_IMAGE`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`

Registry ID: `QXBY_FULL_COMPONENT_ATLAS_REINDEXED_v0.2`.

This registry reindexes the v0.1 full atlas into category-based primary IDs. It preserves all 174 v0.1 components by reference, adds 12 auxiliary normalized components, and does not copy or rewrite source images.

## Summary

- Full atlas components: `174`
- Auxiliary components: `12`
- Total primary components: `186`
- Legacy alias mappings: `38`
- v0.1 source mappings: `174`
- Semantic aliases needing review: `3`

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

## Auxiliary Components

| Label | Component ID | Family |
| --- | --- | --- |
| 一 | COMP-081 | numeric_component_family |
| 二 | COMP-082 | numeric_component_family |
| 三 | COMP-083 | numeric_component_family |
| 四 | COMP-084 | numeric_component_family |
| 五 | COMP-085 | numeric_component_family |
| 六 | COMP-086 | numeric_component_family |
| 七 | COMP-087 | numeric_component_family |
| 大指 | COMP-091 | left_finger_name_family |
| 食指 | COMP-092 | left_finger_name_family |
| 中指 | COMP-093 | left_finger_name_family |
| 名指 | COMP-094 | left_finger_name_family |
| 跪指 | COMP-095 | left_finger_name_family |

## Authority Boundary

The registry is authoritative only as a component-reference and ID-normalization layer. It is not canon term authority, not phrase score authority, not Dapu IR authority, not sample ingest, not ML training data, and not render output.
