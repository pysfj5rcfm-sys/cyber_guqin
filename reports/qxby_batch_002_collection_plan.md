# QXBY_BATCH_002 Collection Plan

## 1. Executive Summary

This C1 plan converts the Phase C0 blind V1-to-canon coverage output into a human OCR / screenshot collection plan. It is derived from C0 machine candidates only; it is not a manually preset gap list.

C1 does not import OCR, does not create `QXBY_BATCH_002`, does not modify canon, does not modify sources, and does not modify V1 runtime data. It only defines collection topics that a human can use when gathering images, OCR excerpts, page numbers, and short source notes.

Recommended collection is narrowed to 7 topics:

1. 三音型：散音 / 按音 / 泛音
2. 指名系统：大指 / 食指 / 中指 / 名指 / 复合触弦
3. 泛音取法：触徽 / 泛音指法 / 左手触徽右手取声
4. 复合泛音撮：双指七徽 + 撮六一
5. 按音取法：按弦 / 左手按音 / 右手取声
6. 承接规则：掐起承前音位 / 省略继承
7. 徽分与弦序结构：徽 / 分 / 七徽九分 / 六一撮

## 2. C0 Raw Candidate Summary

Phase C0 read 51 Xianwengcao score events, 29 gesture templates, and 31 gesture components. It derived 95 coverage items from V1 runtime data.

C0 coverage summary:

- `qxby_batch_001_draft_covered`: 25 items.
- `project_canon_seed_covered`: 7 items.
- `internal_ontology_only`: 1 item.
- `v1_runtime_only`: 62 items.
- `missing_or_unmapped`: 0 items.
- `ambiguous`: 0 items.

C0 recommended Batch002 machine items included:

- `sound_profile:harmonic_compound`
- `component_category:harmonic_pluck`
- `component_category:pressed_pluck`
- `gesture_family:harmonic_pluck`
- `gesture_family:pressed_pluck`
- `sound_type:散音`, `sound_type:按音`, `sound_type:泛音`
- `context_dependency:inherit_previous`
- `harmonic_touch_finger:index/middle/thumb/thumb_middle`
- `left_finger:index/middle/ring/thumb/thumb_middle`
- `right_hand_finger:index/middle/thumb/thumb_middle`

C0 also exposed lower-priority runtime structures such as `hui:*`, `string_number:*`, `string_sequence:6_1`, individual `gesture_id:*`, and `composite_gesture_structure:*`.

## 3. Why Raw Candidate List Cannot Be Used Directly

The raw list is machine-level coverage output. It is valuable for auditing, but not directly usable as a human OCR task list.

Problems:

- It repeats the same human concept across internal fields. For example, `index` appears as `harmonic_touch_finger`, `left_finger`, and `right_hand_finger`.
- It exposes internal enum names such as `harmonic_compound`, `pressed_pluck`, `harmonic_pluck`, and `inherit_previous`, which are not good OCR search terms.
- It mixes reusable source topics with runtime structures such as `gesture_id`, `hui`, and `string_number`.
- It includes canon-seed-covered items that need optional external source evidence, not urgent missing-concept collection.
- It marks some Batch001-covered concepts as already covered and not recommended for duplicate collection.

## 4. Merge Rules

The C1 normalization applies these rules:

- Merge identical human vocabulary across internal roles. `index` / `middle` / `thumb` / `ring` across `harmonic_touch_finger`, `left_finger`, and `right_hand_finger` become one 指名系统 topic.
- Convert internal ontology names to source-searchable琴学 topics:
  - `harmonic_compound` -> 复合泛音 / 双指泛音 / 泛音撮 / 同徽触弦.
  - `inherit_previous` -> 承前音位 / 省略继承 / 掐起承接前一按音位.
  - `pressed_pluck` -> 按音 / 按弦取音 / 左手按弦右手取声.
  - `harmonic_pluck` -> 泛音 / 泛音取法 / 左手触徽右手取声.
- Treat `gesture_id:*` as runtime templates, not OCR keywords.
- Treat `hui:*` and `string_number:*` as contextual location/string fields unless the screenshot also supports a P0/P1 technique topic.
- Preserve C0 priority, but downgrade raw structural values to P2 collection context or defer.
- Do not duplicate QXBY_BATCH_001 draft-covered items unless the new screenshot specifically supports a different C0 topic.

## 5. Recommended Batch002 OCR / Screenshot Collection Topics

### QXBY_B002_TOPIC_001

- `collection_topic_id`: `QXBY_B002_TOPIC_001`
- `human_topic_name`: 三音型：散音 / 按音 / 泛音
- `related_c0_items`: `sound_type:散音`, `sound_type:按音`, `sound_type:泛音`, `component_category:pressed_pluck`, `component_category:harmonic_pluck`, `gesture_family:pressed_pluck`, `gesture_family:harmonic_pluck`
- `related_xianwengcao_events`: broad coverage across `XWC_P01_*`, `XWC_P02_*`, `XWC_P08_*`, `XWC_P09_*`, `XWC_P10_*`
- `related_gestures`: `SAN_GOU_2`, `SAN_TIAO_7`, `AN_RING_10_GOU_5`, `AN_THUMB_9_GOU_4_ZHUANG`, `FAN_SHI_7_GOU_4`, `FAN_DA7_ZHONG7_CUO_6_1`
- `current_coverage_status`: `project_canon_seed_covered`
- `canon_target_type`: `term`, `technique_rule`
- `suggested_search_terms_zh`: 散音, 按音, 泛音, 三音, 三声, 空弦, 按弦取音, 触徽取声
- `source_material_needed`: rule-book page explaining the three sound types; OCR excerpt; page number; short note linking to Xianwengcao sound_type usage
- `priority`: `P1`
- `notes`: Evidence enrichment only. C0 says the concepts are already canon-seed covered.

### QXBY_B002_TOPIC_002

- `collection_topic_id`: `QXBY_B002_TOPIC_002`
- `human_topic_name`: 指名系统：大指 / 食指 / 中指 / 名指 / 复合触弦
- `related_c0_items`: all `harmonic_touch_finger:*`, `left_finger:*`, and `right_hand_finger:*` recommended C0 items
- `related_xianwengcao_events`: `XWC_P01_N01`, `XWC_P01_N04`, `XWC_P02_N04`, `XWC_P06_N02`, `XWC_P09_N02`, `XWC_P10_N01`, `XWC_P10_N05`, `XWC_P10_N06`, `XWC_P10_N07`
- `related_gestures`: `SAN_TIAO_7`, `SAN_GOU_5`, `AN_RING_10_QIAQI`, `AN_THUMB_9_GOU_6_SHANG_79`, `FAN_SHI_7_TIAO_4`, `FAN_ZHONG_7_GOU_1`, `FAN_DA_7_BO_6`, `FAN_DA7_ZHONG7_CUO_6_1`
- `current_coverage_status`: `v1_runtime_only`
- `canon_target_type`: `component`, `alias_rule`
- `suggested_search_terms_zh`: 大指, 食指, 中指, 名指, 左指, 右指, 触弦指, 泛音用指, 双指触弦
- `source_material_needed`: pages defining finger names or identifying which finger performs a technique; examples for right-hand pluck and left-hand press/touch; page number; note distinguishing role names from standalone terms
- `priority`: `P0`
- `notes`: This replaces many duplicated machine items with one executable collection topic.

### QXBY_B002_TOPIC_003

- `collection_topic_id`: `QXBY_B002_TOPIC_003`
- `human_topic_name`: 泛音取法：触徽 / 泛音指法 / 左手触徽右手取声
- `related_c0_items`: `component_category:harmonic_pluck`, `gesture_family:harmonic_pluck`, `sound_type:泛音`, `harmonic_touch_finger:index`, `harmonic_touch_finger:middle`, `harmonic_touch_finger:thumb`
- `related_xianwengcao_events`: `XWC_P10_N01` through `XWC_P10_N06`
- `related_gestures`: `FAN_SHI_7_GOU_4`, `FAN_SHI_7_TIAO_4`, `FAN_SHI_7_TIAO_6`, `FAN_SHI_7_TIAO_7`, `FAN_ZHONG_7_GOU_1`, `FAN_DA_7_BO_6`
- `current_coverage_status`: `project_canon_seed_covered`, `v1_runtime_only`
- `canon_target_type`: `component`, `technique_rule`
- `suggested_search_terms_zh`: 泛音, 泛音取法, 触徽, 左手轻触, 右手取声, 七徽泛音, 泛食, 泛中, 泛大
- `source_material_needed`: page describing how泛音 is produced; example showing left-hand touch at hui and right-hand pluck; examples naming touch fingers if available
- `priority`: `P0`
- `notes`: C0 split this across sound type, gesture family, and finger-role fields. Human collection should keep it together.

### QXBY_B002_TOPIC_004

- `collection_topic_id`: `QXBY_B002_TOPIC_004`
- `human_topic_name`: 复合泛音撮：双指七徽 + 撮六一
- `related_c0_items`: `sound_profile:harmonic_compound`, `harmonic_touch_finger:thumb_middle`, `left_finger:thumb_middle`, `right_hand_finger:thumb_middle`, `composite_gesture_structure:FAN_DA7_ZHONG7_CUO_6_1`, `string_number:6_1`, `string_sequence:6_1`
- `related_xianwengcao_events`: `XWC_P10_N07`
- `related_gestures`: `FAN_DA7_ZHONG7_CUO_6_1`
- `current_coverage_status`: `internal_ontology_only`, `v1_runtime_only`, `qxby_batch_001_draft_covered`
- `canon_target_type`: `component`, `technique_rule`, `dapu_rule`
- `suggested_search_terms_zh`: 复合泛音, 双指泛音, 同徽触弦, 大指七徽, 中指七徽, 撮六一, 泛音撮, 齐撮
- `source_material_needed`: screenshot/OCR showing撮 in a泛音 or mixed-sound context; evidence for simultaneous two-string pluck as one sound; if available, two left fingers touching the same hui
- `priority`: `P0`
- `notes`: Basic撮 is already covered by Batch001. The new collection target is the复合泛音 context.

### QXBY_B002_TOPIC_005

- `collection_topic_id`: `QXBY_B002_TOPIC_005`
- `human_topic_name`: 按音取法：按弦 / 左手按音 / 右手取声
- `related_c0_items`: `component_category:pressed_pluck`, `gesture_family:pressed_pluck`, `sound_type:按音`, `left_finger:ring`, `left_finger:thumb`
- `related_xianwengcao_events`: `XWC_P01_N04`, `XWC_P02_N04`, `XWC_P02_N06`, `XWC_P03_N04`, `XWC_P03_N06`, `XWC_P04_N04`, `XWC_P04_N06`, `XWC_P05_N04`, `XWC_P05_N06`, `XWC_P06_N02`, `XWC_P06_N04`, `XWC_P07_N02`, `XWC_P07_N04`, `XWC_P08_N01`, `XWC_P08_N02`, `XWC_P08_N04`, `XWC_P09_N01`, `XWC_P09_N04`
- `related_gestures`: `AN_RING_10_GOU_1`, `AN_RING_10_GOU_2`, `AN_RING_10_GOU_4`, `AN_RING_10_GOU_5`, `AN_RING_10_8_GOU_3`, `AN_THUMB_9_GOU_1`, `AN_THUMB_9_GOU_6_SHANG_79`
- `current_coverage_status`: `project_canon_seed_covered`, `v1_runtime_only`
- `canon_target_type`: `term`, `component`, `technique_rule`
- `suggested_search_terms_zh`: 按音, 按弦, 左手按弦, 右手取声, 名指按, 大指按, 九徽按音, 十徽按音
- `source_material_needed`: page explaining按音 as left-hand pressed sound; examples stating left finger and hui position; page number; note separating按音取法 from Batch001 post-motion entries
- `priority`: `P1`
- `notes`: `pressed_pluck` is not an OCR keyword. Search for按音 and按弦取音.

### QXBY_B002_TOPIC_006

- `collection_topic_id`: `QXBY_B002_TOPIC_006`
- `human_topic_name`: 承接规则：掐起承前音位 / 省略继承
- `related_c0_items`: `context_dependency:inherit_previous`, `inherited_context_structure:XWC_P09_N02_inherits_XWC_P09_N01`, `gesture_id:AN_RING_10_QIAQI`, `composite_gesture_structure:AN_RING_10_QIAQI`
- `related_xianwengcao_events`: `XWC_P09_N01`, `XWC_P09_N02`
- `related_gestures`: `AN_THUMB_9_GOU_4_ZHUANG`, `AN_RING_10_QIAQI`
- `current_coverage_status`: `v1_runtime_only`, `qxby_batch_001_draft_covered`
- `canon_target_type`: `dapu_rule`, `technique_rule`
- `suggested_search_terms_zh`: 掐起, 搯起, 承前, 承接前一按音, 省略音位, 前一按位, 按下位, 上一位
- `source_material_needed`: screenshot/OCR around掐起/搯起 explaining required prior pressed position; source note about whether previous position is inherited; page number
- `priority`: `P0`
- `notes`: Search for source language around the dapu rule, not for `inherit_previous`.

### QXBY_B002_TOPIC_007

- `collection_topic_id`: `QXBY_B002_TOPIC_007`
- `human_topic_name`: 徽分与弦序结构：徽 / 分 / 七徽九分 / 六一撮
- `related_c0_items`: `hui:7`, `hui:9`, `hui:10`, `hui:10_8`, `hui_target:7_9`, `string_number:1..7`, `string_number:6_1`, `string_sequence:6_1`
- `related_xianwengcao_events`: `XWC_P03_N04`, `XWC_P08_N02`, `XWC_P09_N01`, `XWC_P10_N01`, `XWC_P10_N07`
- `related_gestures`: `AN_RING_10_8_GOU_3`, `AN_THUMB_9_GOU_6_SHANG_79`, `FAN_SHI_7_GOU_4`, `FAN_DA7_ZHONG7_CUO_6_1`
- `current_coverage_status`: `v1_runtime_only`
- `canon_target_type`: `term`, `dapu_rule`
- `suggested_search_terms_zh`: 徽, 分, 十徽八, 七徽, 九徽, 七徽九分, 六一, 弦序, 撮六一
- `source_material_needed`: collect only when the same screenshot also supports a P0/P1 topic; note whether the number is a location/string structure rather than standalone term
- `priority`: `P2`
- `notes`: Use as context, not as standalone OCR collection unless canon scope expands.

## 6. Already Covered, Not Recommended For Duplicate Images

Do not repeat image collection for these C0 items unless the same page is needed for a higher-priority Batch002 topic:

- `component_category:left_sound`
- `component_category:micro_returning_slide`
- `component_category:simultaneous_pluck`
- `component_category:single_pluck`
- `component_category:single_slide`
- `component_name:bo`
- `component_name:cuo`
- `component_name:gou`
- `component_name:qiaqi`
- `component_name:tiao`
- `gesture_family:left_hand_sound`
- `gesture_family:post_motion`
- `gesture_family:simultaneous_pluck`
- `gesture_family:single_pluck`
- `post_motion:shang`
- `post_motion:zhuang`
- `post_motion_return_structure:zhuang`
- `pre_action:zhu`
- `right_hand_action:bo`
- `right_hand_action:cuo`
- `right_hand_action:gou`
- `right_hand_action:tiao`
- `sound_profile:left_hand_sound`
- `sound_profile:post_motion`
- `sound_profile:single`

## 7. Deferred Items

Temporarily defer:

- Individual `gesture_id:*` items. They are runtime template names, not source search terms.
- Standalone `composite_gesture_structure:*` values, except when bundled into a human topic such as复合泛音撮 or掐起承接.
- Standalone `hui:*`, `hui_target:*`, `string_number:*`, and `string_sequence:*` values. Collect them as screenshot context only.
- Batch001-covered basic technique items, including basic撮,勾,挑,掐起,撞,上,注, and single pluck categories.

## 8. Next Collection Advice For User

Please prioritize screenshots/OCR in this order:

1. A page explaining泛音取法, especially left-hand touch at hui plus right-hand pluck.
2. A page or passage showing复合泛音 / 泛音撮 / double-finger same-hui touch, ideally connected to撮六一 or two-string simultaneous pluck.
3. A page explaining指名 vocabulary: 大指, 食指, 中指, 名指, and how those names apply to left/right hand or泛音 touch.
4. A page around掐起/搯起 that states how the pressed position is supplied or inherited from the previous context.
5. Optional enrichment pages for三音型 and按音取法 if they are easy to capture.

For each image/OCR packet, include original screenshot, OCR text, page or section marker, and a short note saying which C1 topic it supports.
