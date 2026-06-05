# C1 Candidate Normalization Report

## 1. Data Change Statement

C1 did not modify data.

C1 did not create `QXBY_BATCH_002`.

C1 did not import OCR, did not create `recording_items_enriched.jsonl`, did not create recording ingest scripts, did not create V1 patch scripts, did not modify canon, did not modify sources, and did not modify V1 runtime files.

The only C1 outputs are:

- `reports/qxby_batch_002_collection_plan.md`
- `reports/qxby_batch_002_collection_plan.json`
- `reports/c1_candidate_normalization_report.md`

## 2. Basis

C1 is based on the Phase C0 blind V1-to-canon coverage audit:

- `reports/v1_to_canon_coverage.md`
- `reports/v1_to_canon_coverage.json`
- `reports/qxby_batch_002_candidate_list.md`

The C0 audit explicitly derived coverage items from V1 runtime data before comparison. C1 therefore treats the candidate list as machine output and normalizes it into human collection topics. It is not an artificial preset missing-term list.

## 3. How Raw Machine Items Were Merged

C1 merged raw items by source-searchable human topic rather than by internal field name.

Main conversions:

- `index`, `middle`, `thumb`, `ring`, and `thumb_middle` across `harmonic_touch_finger`, `left_finger`, and `right_hand_finger` became one 指名系统 topic.
- `harmonic_pluck` became 泛音取法 / 左手触徽右手取声.
- `pressed_pluck` became 按音取法 / 左手按弦右手取声.
- `harmonic_compound` became 复合泛音 / 双指泛音 / 泛音撮 / 同徽触弦.
- `inherit_previous` became 承前音位 / 省略继承 / 掐起承接前一按音位.
- `hui:*`, `hui_target:*`, `string_number:*`, and `string_sequence:*` became P2 screenshot context rather than standalone OCR tasks.
- `gesture_id:*` and most `composite_gesture_structure:*` items were not treated as OCR search terms.

## 4. Raw Items Merged

Merged into 指名系统:

- `harmonic_touch_finger:index`
- `harmonic_touch_finger:middle`
- `harmonic_touch_finger:thumb`
- `harmonic_touch_finger:thumb_middle`
- `left_finger:index`
- `left_finger:middle`
- `left_finger:ring`
- `left_finger:thumb`
- `left_finger:thumb_middle`
- `right_hand_finger:index`
- `right_hand_finger:middle`
- `right_hand_finger:thumb`
- `right_hand_finger:thumb_middle`

Merged into 三音型 / 泛音取法 / 按音取法:

- `sound_type:散音`
- `sound_type:按音`
- `sound_type:泛音`
- `component_category:harmonic_pluck`
- `component_category:pressed_pluck`
- `gesture_family:harmonic_pluck`
- `gesture_family:pressed_pluck`

Merged into 复合泛音撮:

- `sound_profile:harmonic_compound`
- `harmonic_touch_finger:thumb_middle`
- `left_finger:thumb_middle`
- `right_hand_finger:thumb_middle`
- `composite_gesture_structure:FAN_DA7_ZHONG7_CUO_6_1`
- `string_number:6_1`
- `string_sequence:6_1`

Merged into 承接规则:

- `context_dependency:inherit_previous`
- `inherited_context_structure:XWC_P09_N02_inherits_XWC_P09_N01`
- `gesture_id:AN_RING_10_QIAQI`
- `composite_gesture_structure:AN_RING_10_QIAQI`

Merged into 徽分与弦序 context:

- `hui:7`
- `hui:9`
- `hui:10`
- `hui:10_8`
- `hui_target:7_9`
- `string_number:1`
- `string_number:2`
- `string_number:3`
- `string_number:4`
- `string_number:5`
- `string_number:6`
- `string_number:6_1`
- `string_number:7`
- `string_sequence:6_1`

## 5. Raw Items Downgraded Or Deferred

Downgraded to P2 context:

- `hui:*`
- `hui_target:*`
- `string_number:*`
- `string_sequence:*`

Deferred as non-OCR search targets:

- Individual `gesture_id:*` runtime template names.
- Standalone `composite_gesture_structure:*` values that are already explained by Batch001-covered components or by the higher-level C1 topics.
- Basic pluck and post-motion items already covered in `QXBY_BATCH_001`.

Reason: these are runtime structures or already-covered mechanics. They may help interpret a screenshot, but they should not drive independent OCR collection.

## 6. Batch001 Covered Items Not Recommended For Recollection

Do not collect duplicate images for:

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

These may still appear on useful screenshots, but they should not be the reason for a Batch002 collection item.

## 7. C0 Candidate Prioritization Issues Found

C0 prioritization is useful but too literal for human collection.

Issues:

- It produces duplicate P0 work for the same finger name across several internal fields.
- It recommends canon-seed-covered items alongside truly uncovered runtime concepts, which blurs missing evidence vs optional enrichment.
- It exposes internal enum names as if they were source-searchable terms.
- It leaves `gesture_id`, `hui`, and `string_number` visible as gaps even though many are structural values, not independent canon-source concepts.
- Some Chinese excerpts in generated reports appear with encoding corruption, although internal item IDs and event references remain usable.

## 8. Audit Script Recommendations

Yes, C1 recommends improving the audit script before future batches.

Suggested script improvements:

- Add a semantic grouping layer before producing candidate lists.
- Collapse repeated finger-role values across `harmonic_touch_finger`, `left_finger`, and `right_hand_finger`.
- Translate internal enums to human search topics in the report.
- Separate `missing source evidence`, `optional evidence enrichment`, and `runtime structural context`.
- Suppress or separately bucket raw `gesture_id:*`, `hui:*`, and `string_number:*` from the main recommended OCR list.
- Include a stable `human_collection_topic` field in JSON output.

No audit script was modified in C1.

## 9. Next User OCR / Image Requests

Ask the user for images/OCR in this order:

1. 泛音取法 pages: especially descriptions of触徽, 七徽, and left-hand touch plus right-hand sound production.
2. 复合泛音撮 pages: passages about双指泛音, 同徽触弦, 泛音撮, 撮六一, or mixed sound-type撮.
3. 指名系统 pages: passages naming大指, 食指, 中指, 名指 and showing how finger names map to action roles.
4. 掐起/搯起 pages: passages explaining that掐起 depends on an already pressed position or previous context.
5. Optional pages for三音型 and按音取法 if available without extra search cost.

Each packet should include screenshot, OCR text, page number or section marker, and a one-line note naming the C1 topic it supports.
