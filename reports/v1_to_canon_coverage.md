# V1-to-Canon Blind Coverage Audit

## 1. Executive Summary

- Audit type: `blind_v1_to_canon_coverage`.
- Piece: `XWC`.
- Score events read: 51.
- Gesture templates read: 29.
- Gesture components read: 31.
- Coverage items derived from V1 runtime data: 95.
- QXBY_BATCH_001 draft covered items: 25.
- Canon seed covered without QXBY draft evidence: 7.
- Internal ontology only: 1.
- V1 runtime only: 62.

## 2. Blind Audit Declaration

This audit is blind: coverage items were derived from `score_events.csv`, `gesture_templates.csv`, and `gesture_components.csv` before comparison. No manually preset missing-term list was used as evidence or as a candidate source.

## 3. Input Files

- 01_pieces\xianwengcao\score_events.csv
- 00_global\gesture_templates.csv
- 00_global\gesture_components.csv
- 01_pieces\xianwengcao\phrase_structure.csv
- 01_pieces\xianwengcao\recording_script_human.csv
- 01_pieces\xianwengcao\recording_batches.md
- canon\sources.yaml
- canon\terms.yaml
- canon\component_lexicon.yaml
- canon\gesture_families.yaml
- canon\alias_rules.yaml
- canon\technique_rules.yaml
- canon\validation_rules.yaml
- canon\drafts\qxby_batch_001.yaml
- sources\qinxue_beiyao\QXBY_BATCH_001\manifest.yaml
- 00_global\guqin_fingering_ontology.yaml
- 00_global\gesture_component_lexicon.csv
- 00_global\gesture_family_catalog.csv
- 00_global\alias_rules.yaml
- 06_docs\GESTURE_ONTOLOGY.md
- .agents\skills\guqin-canon-builder\SKILL.md
- .agents\skills\guqin-dapu-parser\SKILL.md

## 4. V1.0 Runtime Extraction

### Gesture IDs
- AN_RING_10_8_GOU_3
- AN_RING_10_GOU_1
- AN_RING_10_GOU_2
- AN_RING_10_GOU_4
- AN_RING_10_GOU_5
- AN_RING_10_QIAQI
- AN_THUMB_9_GOU_1
- AN_THUMB_9_GOU_2
- AN_THUMB_9_GOU_3
- AN_THUMB_9_GOU_4
- AN_THUMB_9_GOU_4_ZHUANG
- AN_THUMB_9_GOU_5
- AN_THUMB_9_GOU_6_SHANG_79
- FAN_DA7_ZHONG7_CUO_6_1
- FAN_DA_7_BO_6
- FAN_SHI_7_GOU_4
- FAN_SHI_7_TIAO_4
- FAN_SHI_7_TIAO_6
- FAN_SHI_7_TIAO_7
- FAN_ZHONG_7_GOU_1
- SAN_GOU_2
- SAN_GOU_3
- SAN_GOU_4
- SAN_GOU_5
- SAN_TIAO_3
- SAN_TIAO_4
- SAN_TIAO_5
- SAN_TIAO_6
- SAN_TIAO_7

### Component Names
- bo
- cuo
- gou
- qiaqi
- shang
- tiao
- zhuang

### Primary Sound Types
- 按音
- 散音
- 泛音

### Gesture Families
- harmonic_pluck
- left_hand_sound
- post_motion
- pressed_pluck
- simultaneous_pluck
- single_pluck

### Sound Profiles
- harmonic_compound
- left_hand_sound
- post_motion
- single

### Left/Right Hand Terms
- bo
- cuo
- gou
- index
- middle
- ring
- thumb
- thumb+middle
- tiao

### Hui / String / Context Dependency
- 1
- 10
- 10.8
- 2
- 3
- 4
- 5
- 6
- 6+1
- 7
- 7.9
- 9
- XWC_P09_N01
- inherit_previous

## 5. Canon Seed Coverage Comparison

| item | type | status | v1 usage | evidence | action |
|---|---|---|---|---|---|
| harmonic_pluck | component_category | project_canon_seed_covered | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06<br>gestures FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, FAN_ZHONG_7_GOU_1 | canon/gesture_families.yaml:harmonic_pluck | Optional external source evidence can be added if this is a reusable canon concept. |
| pressed_pluck | component_category | project_canon_seed_covered | events XWC_P01_N04, XWC_P02_N04, XWC_P02_N06, XWC_P03_N04, XWC_P03_N06, XWC_P04_N04, XWC_P04_N06, XWC_P05_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/gesture_families.yaml:pressed_pluck<br>canon/technique_rules.yaml:fenkai | Optional external source evidence can be added if this is a reusable canon concept. |
| harmonic_pluck | gesture_family | project_canon_seed_covered | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06<br>gestures FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, FAN_ZHONG_7_GOU_1 | canon/gesture_families.yaml:harmonic_pluck | Optional external source evidence can be added if this is a reusable canon concept. |
| pressed_pluck | gesture_family | project_canon_seed_covered | events XWC_P01_N04, XWC_P02_N04, XWC_P02_N06, XWC_P03_N04, XWC_P03_N06, XWC_P04_N04, XWC_P04_N06, XWC_P05_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/gesture_families.yaml:pressed_pluck<br>canon/technique_rules.yaml:fenkai | Optional external source evidence can be added if this is a reusable canon concept. |
| 按音 | sound_type | project_canon_seed_covered | events XWC_P01_N04, XWC_P02_N04, XWC_P02_N06, XWC_P03_N04, XWC_P03_N06, XWC_P04_N04, XWC_P04_N06, XWC_P05_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_RING_10_QIAQI... | canon/terms.yaml:sound_type_an<br>canon/technique_rules.yaml:qiaqi<br>canon/technique_rules.yaml:fanghe<br>canon/technique_rules.yaml:yinghe | Optional external source evidence can be added if this is a reusable canon concept. |
| 散音 | sound_type | project_canon_seed_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01...<br>gestures SAN_GOU_2, SAN_GOU_3, SAN_GOU_4, SAN_GOU_5, SAN_TIAO_3, SAN_TIAO_4... | canon/terms.yaml:sound_type_san | Optional external source evidence can be added if this is a reusable canon concept. |
| 泛音 | sound_type | project_canon_seed_covered | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06, XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1, FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7... | canon/terms.yaml:sound_type_fan | Optional external source evidence can be added if this is a reusable canon concept. |

## 6. QXBY_BATCH_001 Draft Coverage Comparison

| item | type | status | v1 usage | evidence | action |
|---|---|---|---|---|---|
| left_sound | component_category | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| micro_returning_slide | component_category | qxby_batch_001_draft_covered | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>canon/drafts/qxby_batch_001.yaml:QXBY_012 | No duplicate Batch002 evidence recommended. |
| simultaneous_pluck | component_category | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| single_pluck | component_category | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01...<br>gestures SAN_GOU_2, SAN_GOU_3, SAN_GOU_4, SAN_GOU_5, SAN_TIAO_3, SAN_TIAO_4... | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>canon/drafts/qxby_batch_001.yaml:QXBY_002<br>canon/drafts/qxby_batch_001.yaml:QXBY_003<br>canon/drafts/qxby_batch_001.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| single_slide | component_category | qxby_batch_001_draft_covered | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_013<br>canon/drafts/qxby_batch_001.yaml:QXBY_014 | No duplicate Batch002 evidence recommended. |
| bo | component_name | qxby_batch_001_draft_covered | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_001 | No duplicate Batch002 evidence recommended. |
| cuo | component_name | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| gou | component_name | qxby_batch_001_draft_covered | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P03_N04, XWC_P03_N06...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/drafts/qxby_batch_001.yaml:QXBY_005<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_005 | No duplicate Batch002 evidence recommended. |
| qiaqi | component_name | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| tiao | component_name | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01, XWC_P03_N03, XWC_P03_N05...<br>gestures FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, SAN_TIAO_3, SAN_TIAO_4, SAN_TIAO_5... | canon/drafts/qxby_batch_001.yaml:QXBY_004<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| left_hand_sound | gesture_family | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| post_motion | gesture_family | qxby_batch_001_draft_covered | events XWC_P08_N02, XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>canon/drafts/qxby_batch_001.yaml:QXBY_012<br>canon/drafts/qxby_batch_001.yaml:QXBY_013<br>canon/drafts/qxby_batch_001.yaml:QXBY_014 | No duplicate Batch002 evidence recommended. |
| simultaneous_pluck | gesture_family | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| single_pluck | gesture_family | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01...<br>gestures SAN_GOU_2, SAN_GOU_3, SAN_GOU_4, SAN_GOU_5, SAN_TIAO_3, SAN_TIAO_4... | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>canon/drafts/qxby_batch_001.yaml:QXBY_002<br>canon/drafts/qxby_batch_001.yaml:QXBY_003<br>canon/drafts/qxby_batch_001.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| shang | post_motion | qxby_batch_001_draft_covered | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_013<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_013 | No duplicate Batch002 evidence recommended. |
| zhuang | post_motion | qxby_batch_001_draft_covered | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_011 | No duplicate Batch002 evidence recommended. |
| zhuang | post_motion_return_structure | qxby_batch_001_draft_covered | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_011 | No duplicate Batch002 evidence recommended. |
| zhu | pre_action | qxby_batch_001_draft_covered | events XWC_P03_N04, XWC_P09_N01<br>gestures AN_RING_10_8_GOU_3, AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_010<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_010 | No duplicate Batch002 evidence recommended. |
| bo | right_hand_action | qxby_batch_001_draft_covered | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_001 | No duplicate Batch002 evidence recommended. |
| cuo | right_hand_action | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| gou | right_hand_action | qxby_batch_001_draft_covered | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P03_N04, XWC_P03_N06...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/drafts/qxby_batch_001.yaml:QXBY_005<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_005 | No duplicate Batch002 evidence recommended. |
| tiao | right_hand_action | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01, XWC_P03_N03, XWC_P03_N05...<br>gestures FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, SAN_TIAO_3, SAN_TIAO_4, SAN_TIAO_5... | canon/drafts/qxby_batch_001.yaml:QXBY_004<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| left_hand_sound | sound_profile | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| post_motion | sound_profile | qxby_batch_001_draft_covered | events XWC_P08_N02, XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>canon/drafts/qxby_batch_001.yaml:QXBY_012<br>canon/drafts/qxby_batch_001.yaml:QXBY_013<br>canon/drafts/qxby_batch_001.yaml:QXBY_014 | No duplicate Batch002 evidence recommended. |
| single | sound_profile | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P01_N04, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>canon/drafts/qxby_batch_001.yaml:QXBY_002<br>canon/drafts/qxby_batch_001.yaml:QXBY_003<br>canon/drafts/qxby_batch_001.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |

## 7. internal_ontology_only Items

| item | type | status | v1 usage | evidence | action |
|---|---|---|---|---|---|
| harmonic_compound | sound_profile | internal_ontology_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Add external source evidence if this observed V1 concept should be promoted into canon evidence. |

## 8. v1_runtime_only Items

| item | type | status | v1 usage | evidence | action |
|---|---|---|---|---|---|
| AN_RING_10_QIAQI | composite_gesture_structure | v1_runtime_only | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_4_ZHUANG | composite_gesture_structure | v1_runtime_only | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_6_SHANG_79 | composite_gesture_structure | v1_runtime_only | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_DA7_ZHONG7_CUO_6_1 | composite_gesture_structure | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| inherit_previous | context_dependency | v1_runtime_only | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_RING_10_8_GOU_3 | gesture_id | v1_runtime_only | events XWC_P03_N04<br>gestures AN_RING_10_8_GOU_3 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_RING_10_GOU_1 | gesture_id | v1_runtime_only | events XWC_P05_N04<br>gestures AN_RING_10_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_RING_10_GOU_2 | gesture_id | v1_runtime_only | events XWC_P04_N04<br>gestures AN_RING_10_GOU_2 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_RING_10_GOU_4 | gesture_id | v1_runtime_only | events XWC_P02_N04, XWC_P09_N04<br>gestures AN_RING_10_GOU_4 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_RING_10_GOU_5 | gesture_id | v1_runtime_only | events XWC_P01_N04<br>gestures AN_RING_10_GOU_5 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_RING_10_QIAQI | gesture_id | v1_runtime_only | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_1 | gesture_id | v1_runtime_only | events XWC_P05_N06, XWC_P06_N02<br>gestures AN_THUMB_9_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_2 | gesture_id | v1_runtime_only | events XWC_P04_N06, XWC_P06_N04<br>gestures AN_THUMB_9_GOU_2 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_3 | gesture_id | v1_runtime_only | events XWC_P03_N06, XWC_P07_N02<br>gestures AN_THUMB_9_GOU_3 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_4 | gesture_id | v1_runtime_only | events XWC_P02_N06, XWC_P07_N04, XWC_P08_N04<br>gestures AN_THUMB_9_GOU_4 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_4_ZHUANG | gesture_id | v1_runtime_only | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_5 | gesture_id | v1_runtime_only | events XWC_P08_N01<br>gestures AN_THUMB_9_GOU_5 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| AN_THUMB_9_GOU_6_SHANG_79 | gesture_id | v1_runtime_only | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_DA7_ZHONG7_CUO_6_1 | gesture_id | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_DA_7_BO_6 | gesture_id | v1_runtime_only | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_SHI_7_GOU_4 | gesture_id | v1_runtime_only | events XWC_P10_N01<br>gestures FAN_SHI_7_GOU_4 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_SHI_7_TIAO_4 | gesture_id | v1_runtime_only | events XWC_P10_N04<br>gestures FAN_SHI_7_TIAO_4 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_SHI_7_TIAO_6 | gesture_id | v1_runtime_only | events XWC_P10_N03<br>gestures FAN_SHI_7_TIAO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_SHI_7_TIAO_7 | gesture_id | v1_runtime_only | events XWC_P10_N02<br>gestures FAN_SHI_7_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| FAN_ZHONG_7_GOU_1 | gesture_id | v1_runtime_only | events XWC_P10_N05<br>gestures FAN_ZHONG_7_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_GOU_2 | gesture_id | v1_runtime_only | events XWC_P05_N02<br>gestures SAN_GOU_2 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_GOU_3 | gesture_id | v1_runtime_only | events XWC_P04_N02<br>gestures SAN_GOU_3 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_GOU_4 | gesture_id | v1_runtime_only | events XWC_P03_N02<br>gestures SAN_GOU_4 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_GOU_5 | gesture_id | v1_runtime_only | events XWC_P01_N02, XWC_P02_N02<br>gestures SAN_GOU_5 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_TIAO_3 | gesture_id | v1_runtime_only | events XWC_P05_N03<br>gestures SAN_TIAO_3 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_TIAO_4 | gesture_id | v1_runtime_only | events XWC_P04_N03, XWC_P05_N01, XWC_P05_N05, XWC_P06_N01<br>gestures SAN_TIAO_4 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_TIAO_5 | gesture_id | v1_runtime_only | events XWC_P03_N03, XWC_P04_N01, XWC_P04_N05, XWC_P06_N03<br>gestures SAN_TIAO_5 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_TIAO_6 | gesture_id | v1_runtime_only | events XWC_P02_N03, XWC_P03_N01, XWC_P03_N05, XWC_P07_N01, XWC_P09_N03<br>gestures SAN_TIAO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| SAN_TIAO_7 | gesture_id | v1_runtime_only | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N05, XWC_P07_N03, XWC_P08_N03<br>gestures SAN_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| index | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04<br>gestures FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| middle | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N05<br>gestures FAN_ZHONG_7_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb+middle | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 10 | hui | v1_runtime_only | events XWC_P01_N04, XWC_P02_N04, XWC_P04_N04, XWC_P05_N04, XWC_P09_N02, XWC_P09_N04<br>gestures AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 10.8 | hui | v1_runtime_only | events XWC_P03_N04<br>gestures AN_RING_10_8_GOU_3 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 7 | hui | v1_runtime_only | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06, XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1, FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 9 | hui | v1_runtime_only | events XWC_P02_N06, XWC_P03_N06, XWC_P04_N06, XWC_P05_N06, XWC_P06_N02, XWC_P06_N04, XWC_P07_N02, XWC_P07_N04...<br>gestures AN_THUMB_9_GOU_1, AN_THUMB_9_GOU_2, AN_THUMB_9_GOU_3, AN_THUMB_9_GOU_4, AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_5... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 7.9 | hui_target | v1_runtime_only | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| XWC_P09_N02 inherits XWC_P09_N01 | inherited_context_structure | v1_runtime_only | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| index | left_finger | v1_runtime_only | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04<br>gestures FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| middle | left_finger | v1_runtime_only | events XWC_P10_N05<br>gestures FAN_ZHONG_7_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| ring | left_finger | v1_runtime_only | events XWC_P01_N04, XWC_P02_N04, XWC_P03_N04, XWC_P04_N04, XWC_P05_N04, XWC_P09_N02, XWC_P09_N04<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb | left_finger | v1_runtime_only | events XWC_P02_N06, XWC_P03_N06, XWC_P04_N06, XWC_P05_N06, XWC_P06_N02, XWC_P06_N04, XWC_P07_N02, XWC_P07_N04...<br>gestures AN_THUMB_9_GOU_1, AN_THUMB_9_GOU_2, AN_THUMB_9_GOU_3, AN_THUMB_9_GOU_4, AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_5... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb+middle | left_finger | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| index | right_hand_finger | v1_runtime_only | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01, XWC_P03_N03, XWC_P03_N05...<br>gestures FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, SAN_TIAO_3, SAN_TIAO_4, SAN_TIAO_5... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| middle | right_hand_finger | v1_runtime_only | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P03_N04, XWC_P03_N06...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb | right_hand_finger | v1_runtime_only | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb+middle | right_hand_finger | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 1 | string_number | v1_runtime_only | events XWC_P05_N04, XWC_P05_N06, XWC_P06_N02, XWC_P10_N05<br>gestures AN_RING_10_GOU_1, AN_THUMB_9_GOU_1, FAN_ZHONG_7_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 2 | string_number | v1_runtime_only | events XWC_P04_N04, XWC_P04_N06, XWC_P05_N02, XWC_P06_N04<br>gestures AN_RING_10_GOU_2, AN_THUMB_9_GOU_2, SAN_GOU_2 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 3 | string_number | v1_runtime_only | events XWC_P03_N04, XWC_P03_N06, XWC_P04_N02, XWC_P05_N03, XWC_P07_N02<br>gestures AN_RING_10_8_GOU_3, AN_THUMB_9_GOU_3, SAN_GOU_3, SAN_TIAO_3 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 4 | string_number | v1_runtime_only | events XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P04_N03, XWC_P05_N01, XWC_P05_N05, XWC_P06_N01, XWC_P07_N04...<br>gestures AN_RING_10_GOU_4, AN_THUMB_9_GOU_4, AN_THUMB_9_GOU_4_ZHUANG, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, SAN_GOU_4... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 5 | string_number | v1_runtime_only | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P03_N03, XWC_P04_N01, XWC_P04_N05, XWC_P06_N03, XWC_P08_N01<br>gestures AN_RING_10_GOU_5, AN_THUMB_9_GOU_5, SAN_GOU_5, SAN_TIAO_5 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 6 | string_number | v1_runtime_only | events XWC_P02_N03, XWC_P03_N01, XWC_P03_N05, XWC_P07_N01, XWC_P08_N02, XWC_P09_N03, XWC_P10_N03, XWC_P10_N06<br>gestures AN_THUMB_9_GOU_6_SHANG_79, FAN_DA_7_BO_6, FAN_SHI_7_TIAO_6, SAN_TIAO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 6+1 | string_number | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 7 | string_number | v1_runtime_only | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N05, XWC_P07_N03, XWC_P08_N03, XWC_P10_N02<br>gestures FAN_SHI_7_TIAO_7, SAN_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| 6+1 | string_sequence | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |

## 9. missing_or_unmapped Items

_None._

## 10. ambiguous Items

_None._

## 11. Recommended QXBY_BATCH_002 Items

| item | type | status | v1 usage | evidence | action |
|---|---|---|---|---|---|
| harmonic_compound | sound_profile | internal_ontology_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Add external source evidence if this observed V1 concept should be promoted into canon evidence. |
| harmonic_pluck | component_category | project_canon_seed_covered | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06<br>gestures FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, FAN_ZHONG_7_GOU_1 | canon/gesture_families.yaml:harmonic_pluck | Optional external source evidence can be added if this is a reusable canon concept. |
| pressed_pluck | component_category | project_canon_seed_covered | events XWC_P01_N04, XWC_P02_N04, XWC_P02_N06, XWC_P03_N04, XWC_P03_N06, XWC_P04_N04, XWC_P04_N06, XWC_P05_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/gesture_families.yaml:pressed_pluck<br>canon/technique_rules.yaml:fenkai | Optional external source evidence can be added if this is a reusable canon concept. |
| harmonic_pluck | gesture_family | project_canon_seed_covered | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06<br>gestures FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, FAN_ZHONG_7_GOU_1 | canon/gesture_families.yaml:harmonic_pluck | Optional external source evidence can be added if this is a reusable canon concept. |
| pressed_pluck | gesture_family | project_canon_seed_covered | events XWC_P01_N04, XWC_P02_N04, XWC_P02_N06, XWC_P03_N04, XWC_P03_N06, XWC_P04_N04, XWC_P04_N06, XWC_P05_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/gesture_families.yaml:pressed_pluck<br>canon/technique_rules.yaml:fenkai | Optional external source evidence can be added if this is a reusable canon concept. |
| 按音 | sound_type | project_canon_seed_covered | events XWC_P01_N04, XWC_P02_N04, XWC_P02_N06, XWC_P03_N04, XWC_P03_N06, XWC_P04_N04, XWC_P04_N06, XWC_P05_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_RING_10_QIAQI... | canon/terms.yaml:sound_type_an<br>canon/technique_rules.yaml:qiaqi<br>canon/technique_rules.yaml:fanghe<br>canon/technique_rules.yaml:yinghe | Optional external source evidence can be added if this is a reusable canon concept. |
| 散音 | sound_type | project_canon_seed_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01...<br>gestures SAN_GOU_2, SAN_GOU_3, SAN_GOU_4, SAN_GOU_5, SAN_TIAO_3, SAN_TIAO_4... | canon/terms.yaml:sound_type_san | Optional external source evidence can be added if this is a reusable canon concept. |
| 泛音 | sound_type | project_canon_seed_covered | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04, XWC_P10_N05, XWC_P10_N06, XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1, FAN_DA_7_BO_6, FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7... | canon/terms.yaml:sound_type_fan | Optional external source evidence can be added if this is a reusable canon concept. |
| inherit_previous | context_dependency | v1_runtime_only | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| index | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04<br>gestures FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| middle | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N05<br>gestures FAN_ZHONG_7_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb+middle | harmonic_touch_finger | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| index | left_finger | v1_runtime_only | events XWC_P10_N01, XWC_P10_N02, XWC_P10_N03, XWC_P10_N04<br>gestures FAN_SHI_7_GOU_4, FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| middle | left_finger | v1_runtime_only | events XWC_P10_N05<br>gestures FAN_ZHONG_7_GOU_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| ring | left_finger | v1_runtime_only | events XWC_P01_N04, XWC_P02_N04, XWC_P03_N04, XWC_P04_N04, XWC_P05_N04, XWC_P09_N02, XWC_P09_N04<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_RING_10_QIAQI |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb | left_finger | v1_runtime_only | events XWC_P02_N06, XWC_P03_N06, XWC_P04_N06, XWC_P05_N06, XWC_P06_N02, XWC_P06_N04, XWC_P07_N02, XWC_P07_N04...<br>gestures AN_THUMB_9_GOU_1, AN_THUMB_9_GOU_2, AN_THUMB_9_GOU_3, AN_THUMB_9_GOU_4, AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_5... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb+middle | left_finger | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| index | right_hand_finger | v1_runtime_only | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01, XWC_P03_N03, XWC_P03_N05...<br>gestures FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, SAN_TIAO_3, SAN_TIAO_4, SAN_TIAO_5... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| middle | right_hand_finger | v1_runtime_only | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P03_N04, XWC_P03_N06...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb | right_hand_finger | v1_runtime_only | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |
| thumb+middle | right_hand_finger | v1_runtime_only | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 |  | Map against ontology/canon first; request source evidence only if the runtime structure represents a canon concept. |

## 12. Items Not Recommended For Duplicate Evidence

| item | type | status | v1 usage | evidence | action |
|---|---|---|---|---|---|
| left_sound | component_category | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| micro_returning_slide | component_category | qxby_batch_001_draft_covered | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>canon/drafts/qxby_batch_001.yaml:QXBY_012 | No duplicate Batch002 evidence recommended. |
| simultaneous_pluck | component_category | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| single_pluck | component_category | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01...<br>gestures SAN_GOU_2, SAN_GOU_3, SAN_GOU_4, SAN_GOU_5, SAN_TIAO_3, SAN_TIAO_4... | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>canon/drafts/qxby_batch_001.yaml:QXBY_002<br>canon/drafts/qxby_batch_001.yaml:QXBY_003<br>canon/drafts/qxby_batch_001.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| single_slide | component_category | qxby_batch_001_draft_covered | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_013<br>canon/drafts/qxby_batch_001.yaml:QXBY_014 | No duplicate Batch002 evidence recommended. |
| bo | component_name | qxby_batch_001_draft_covered | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_001 | No duplicate Batch002 evidence recommended. |
| cuo | component_name | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| gou | component_name | qxby_batch_001_draft_covered | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P03_N04, XWC_P03_N06...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/drafts/qxby_batch_001.yaml:QXBY_005<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_005 | No duplicate Batch002 evidence recommended. |
| qiaqi | component_name | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| tiao | component_name | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01, XWC_P03_N03, XWC_P03_N05...<br>gestures FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, SAN_TIAO_3, SAN_TIAO_4, SAN_TIAO_5... | canon/drafts/qxby_batch_001.yaml:QXBY_004<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| left_hand_sound | gesture_family | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| post_motion | gesture_family | qxby_batch_001_draft_covered | events XWC_P08_N02, XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>canon/drafts/qxby_batch_001.yaml:QXBY_012<br>canon/drafts/qxby_batch_001.yaml:QXBY_013<br>canon/drafts/qxby_batch_001.yaml:QXBY_014 | No duplicate Batch002 evidence recommended. |
| simultaneous_pluck | gesture_family | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| single_pluck | gesture_family | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01...<br>gestures SAN_GOU_2, SAN_GOU_3, SAN_GOU_4, SAN_GOU_5, SAN_TIAO_3, SAN_TIAO_4... | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>canon/drafts/qxby_batch_001.yaml:QXBY_002<br>canon/drafts/qxby_batch_001.yaml:QXBY_003<br>canon/drafts/qxby_batch_001.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| shang | post_motion | qxby_batch_001_draft_covered | events XWC_P08_N02<br>gestures AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_013<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_013 | No duplicate Batch002 evidence recommended. |
| zhuang | post_motion | qxby_batch_001_draft_covered | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_011 | No duplicate Batch002 evidence recommended. |
| zhuang | post_motion_return_structure | qxby_batch_001_draft_covered | events XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_011 | No duplicate Batch002 evidence recommended. |
| zhu | pre_action | qxby_batch_001_draft_covered | events XWC_P03_N04, XWC_P09_N01<br>gestures AN_RING_10_8_GOU_3, AN_THUMB_9_GOU_4_ZHUANG | canon/drafts/qxby_batch_001.yaml:QXBY_010<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_010 | No duplicate Batch002 evidence recommended. |
| bo | right_hand_action | qxby_batch_001_draft_covered | events XWC_P10_N06<br>gestures FAN_DA_7_BO_6 | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_001 | No duplicate Batch002 evidence recommended. |
| cuo | right_hand_action | qxby_batch_001_draft_covered | events XWC_P10_N07<br>gestures FAN_DA7_ZHONG7_CUO_6_1 | canon/drafts/qxby_batch_001.yaml:QXBY_016<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_016 | No duplicate Batch002 evidence recommended. |
| gou | right_hand_action | qxby_batch_001_draft_covered | events XWC_P01_N02, XWC_P01_N04, XWC_P02_N02, XWC_P02_N04, XWC_P02_N06, XWC_P03_N02, XWC_P03_N04, XWC_P03_N06...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/drafts/qxby_batch_001.yaml:QXBY_005<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_005 | No duplicate Batch002 evidence recommended. |
| tiao | right_hand_action | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N03, XWC_P02_N01, XWC_P02_N03, XWC_P02_N05, XWC_P03_N01, XWC_P03_N03, XWC_P03_N05...<br>gestures FAN_SHI_7_TIAO_4, FAN_SHI_7_TIAO_6, FAN_SHI_7_TIAO_7, SAN_TIAO_3, SAN_TIAO_4, SAN_TIAO_5... | canon/drafts/qxby_batch_001.yaml:QXBY_004<br>sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |
| left_hand_sound | sound_profile | qxby_batch_001_draft_covered | events XWC_P09_N02<br>gestures AN_RING_10_QIAQI | canon/drafts/qxby_batch_001.yaml:QXBY_015 | No duplicate Batch002 evidence recommended. |
| post_motion | sound_profile | qxby_batch_001_draft_covered | events XWC_P08_N02, XWC_P09_N01<br>gestures AN_THUMB_9_GOU_4_ZHUANG, AN_THUMB_9_GOU_6_SHANG_79 | canon/drafts/qxby_batch_001.yaml:QXBY_011<br>canon/drafts/qxby_batch_001.yaml:QXBY_012<br>canon/drafts/qxby_batch_001.yaml:QXBY_013<br>canon/drafts/qxby_batch_001.yaml:QXBY_014 | No duplicate Batch002 evidence recommended. |
| single | sound_profile | qxby_batch_001_draft_covered | events XWC_P01_N01, XWC_P01_N02, XWC_P01_N03, XWC_P01_N04, XWC_P02_N01, XWC_P02_N02, XWC_P02_N03, XWC_P02_N04...<br>gestures AN_RING_10_8_GOU_3, AN_RING_10_GOU_1, AN_RING_10_GOU_2, AN_RING_10_GOU_4, AN_RING_10_GOU_5, AN_THUMB_9_GOU_1... | canon/drafts/qxby_batch_001.yaml:QXBY_001<br>canon/drafts/qxby_batch_001.yaml:QXBY_002<br>canon/drafts/qxby_batch_001.yaml:QXBY_003<br>canon/drafts/qxby_batch_001.yaml:QXBY_004 | No duplicate Batch002 evidence recommended. |

## 13. skills-canon-v1 Bridge Assessment

### Validated

- sound_profile:harmonic_compound
- component_category:harmonic_pluck
- component_category:pressed_pluck
- gesture_family:harmonic_pluck
- gesture_family:pressed_pluck
- sound_type:按音
- sound_type:散音
- sound_type:泛音
- component_category:left_sound
- component_category:micro_returning_slide
- component_category:simultaneous_pluck
- component_category:single_pluck
- component_category:single_slide
- component_name:bo
- component_name:cuo
- component_name:gou
- component_name:qiaqi
- component_name:tiao
- gesture_family:left_hand_sound
- gesture_family:post_motion
- gesture_family:simultaneous_pluck
- gesture_family:single_pluck
- post_motion:shang
- post_motion:zhuang
- post_motion_return_structure:zhuang
- pre_action:zhu
- right_hand_action:bo
- right_hand_action:cuo
- right_hand_action:gou
- right_hand_action:tiao
- sound_profile:left_hand_sound
- sound_profile:post_motion
- sound_profile:single

### Gaps Exposed

- composite_gesture_structure:AN_RING_10_QIAQI
- composite_gesture_structure:AN_THUMB_9_GOU_4_ZHUANG
- composite_gesture_structure:AN_THUMB_9_GOU_6_SHANG_79
- composite_gesture_structure:FAN_DA7_ZHONG7_CUO_6_1
- context_dependency:inherit_previous
- gesture_id:AN_RING_10_8_GOU_3
- gesture_id:AN_RING_10_GOU_1
- gesture_id:AN_RING_10_GOU_2
- gesture_id:AN_RING_10_GOU_4
- gesture_id:AN_RING_10_GOU_5
- gesture_id:AN_RING_10_QIAQI
- gesture_id:AN_THUMB_9_GOU_1
- gesture_id:AN_THUMB_9_GOU_2
- gesture_id:AN_THUMB_9_GOU_3
- gesture_id:AN_THUMB_9_GOU_4
- gesture_id:AN_THUMB_9_GOU_4_ZHUANG
- gesture_id:AN_THUMB_9_GOU_5
- gesture_id:AN_THUMB_9_GOU_6_SHANG_79
- gesture_id:FAN_DA7_ZHONG7_CUO_6_1
- gesture_id:FAN_DA_7_BO_6
- gesture_id:FAN_SHI_7_GOU_4
- gesture_id:FAN_SHI_7_TIAO_4
- gesture_id:FAN_SHI_7_TIAO_6
- gesture_id:FAN_SHI_7_TIAO_7
- gesture_id:FAN_ZHONG_7_GOU_1
- gesture_id:SAN_GOU_2
- gesture_id:SAN_GOU_3
- gesture_id:SAN_GOU_4
- gesture_id:SAN_GOU_5
- gesture_id:SAN_TIAO_3
- gesture_id:SAN_TIAO_4
- gesture_id:SAN_TIAO_5
- gesture_id:SAN_TIAO_6
- gesture_id:SAN_TIAO_7
- harmonic_touch_finger:index
- harmonic_touch_finger:middle
- harmonic_touch_finger:thumb
- harmonic_touch_finger:thumb_middle
- hui:10
- hui:10_8
- hui:7
- hui:9
- hui_target:7_9
- inherited_context_structure:XWC_P09_N02_inherits_XWC_P09_N01
- left_finger:index
- left_finger:middle
- left_finger:ring
- left_finger:thumb
- left_finger:thumb_middle
- right_hand_finger:index
- right_hand_finger:middle
- right_hand_finger:thumb
- right_hand_finger:thumb_middle
- string_number:1
- string_number:2
- string_number:3
- string_number:4
- string_number:5
- string_number:6
- string_number:6_1
- string_number:7
- string_sequence:6_1

### Fields That May Need Future V1 Minimal Patch

- Standalone hand/finger role vocabulary if these should become canonized terms instead of component attributes.
- Explicit source-evidence mapping for string/hui structural values if future canon scope requires location evidence.
- A clearer split between gesture_id runtime templates and reusable canon technique IDs.

## 14. Next Steps

- Review P0/P1 candidate list and decide which runtime-observed items are true canon-source targets.
- Add external evidence only for candidates produced by this blind comparison.
- Keep QXBY_BATCH_001 draft status separate from verified evidence until human review is complete.
