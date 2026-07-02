# QXBY Component ID Reindex Policy v0.2

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `CATEGORY_REINDEXED_COMPONENT_IDS`, `SOURCE_REFERENCE_IMAGE`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`

This policy defines the category-based primary ID system for the QXBY full component atlas. It is reference-only and is not score-event authority, Dapu IR authority, sample ingest, ML training data, or render output.

## Reserved Families

| Reserved ID | Meaning |
| --- | --- |
| COMP-000 | unused |
| COMP-080 | numeric_component_family_reserved |
| COMP-090 | left_finger_name_family_reserved |
| COMP-100 | right_hand_single_string_family_reserved |
| COMP-200 | right_hand_two_string_family_reserved |
| COMP-300 | right_hand_multi_string_family_reserved |
| COMP-400 | left_hand_base_position_family_reserved |
| COMP-500 | left_hand_interval_position_family_reserved |
| COMP-600 | left_hand_open_string_family_reserved |
| COMP-700 | sound_position_marker_family_reserved |
| COMP-800 | rhythm_marker_family_reserved |
| COMP-900 | generic_score_marker_family_reserved |

## Auxiliary Numeric Components

| Label | Component ID |
| --- | --- |
| 一 | COMP-081 |
| 二 | COMP-082 |
| 三 | COMP-083 |
| 四 | COMP-084 |
| 五 | COMP-085 |
| 六 | COMP-086 |
| 七 | COMP-087 |

## Auxiliary Left-Finger-Name Components

| Label | Component ID |
| --- | --- |
| 大指 | COMP-091 |
| 食指 | COMP-092 |
| 中指 | COMP-093 |
| 名指 | COMP-094 |
| 跪指 | COMP-095 |

The left-finger-name labels were checked against the user-authorized `左手指名.zip` reference. Its images were not copied into the repo.

## Full Atlas Category Ranges

| Category | Family | Reserved range | Assigned count | Assigned range |
| --- | --- | --- | --- | --- |
| 右手指法-一弦单弹 | right_hand_single_string_family | COMP-101..COMP-199 | 23 | COMP-101..COMP-123 |
| 右手指法-两弦双弹 | right_hand_two_string_family | COMP-201..COMP-299 | 17 | COMP-201..COMP-217 |
| 右手指法-数弦连弹 | right_hand_multi_string_family | COMP-301..COMP-399 | 9 | COMP-301..COMP-309 |
| 左手指法-本位取音 | left_hand_base_position_family | COMP-401..COMP-499 | 38 | COMP-401..COMP-438 |
| 左手指法-隔位取音 | left_hand_interval_position_family | COMP-501..COMP-599 | 33 | COMP-501..COMP-533 |
| 左手指法-散弦取音 | left_hand_open_string_family | COMP-601..COMP-699 | 9 | COMP-601..COMP-609 |
| 音位谱字 | sound_position_marker_family | COMP-701..COMP-799 | 8 | COMP-701..COMP-708 |
| 节奏谱字 | rhythm_marker_family | COMP-801..COMP-899 | 22 | COMP-801..COMP-822 |
| 通用谱字 | generic_score_marker_family | COMP-901..COMP-999 | 15 | COMP-901..COMP-915 |

## Traceability Rules

- Primary IDs are v0.2 category-based IDs.
- Legacy `COMP-001..038` IDs are aliases only and belong in `legacy_refs`.
- v0.1 full-atlas IDs belong in `source_component_id_v0_1` or `source_component_refs_v0_1`.
- Some v0.2 primary IDs reuse numeric strings that were also present in v0.1. The field name and `primary_id_system=category_based_v0_2` disambiguate identity.
