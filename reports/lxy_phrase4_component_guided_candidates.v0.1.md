# LXY Phrase 4 Component-Guided Candidates v0.1

Task id: `CG-LXY-COMPONENT-GUIDED-TRANSCRIPTION-SKILL-AND-PHRASE3-PHRASE4-v0.3_STAGE_B`

Status labels: `LXY_TRANSCRIPTION_DRAFT`, `USER_COMPONENT_LABEL_GUIDED`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`.

This is a report-only component-guided transcription draft. It is not score import, canon authority, Dapu IR authority, sample ingest, ML training data, recording plan, or render output.

## Inputs Used

- `/Users/chenyulin/Downloads/basic_components_named_v0.2.zip` (`sha256=ac4330df2c5d8b234d6cdb16ab9141692faf7553ab599391047b7a6a4a9817ac`): base user-provided components COMP-001..COMP-020.
- `/Users/chenyulin/Downloads/basic_components_named_v0.3.zip` (`sha256=77bf5daaffeb9a1c7b0dab6241a2d89ca0bd20cff0c0e73c9070fbaac34c50b5`): additional user-confirmed components COMP-021..COMP-027.
- `/Users/chenyulin/Downloads/basic_components_named_v0.4.zip` (`sha256=569a74b0d644be8c4bef0a90c44dec19fed9f9073de2c0d8524afb76f4e1cc31`): additional user-confirmed components COMP-028..COMP-030.
- `/Users/chenyulin/Desktop/截屏2026-06-28 21.31.57.png`: `1502x150`, `sha256=8badf5d5b32db4686cac8ff572afaf17e3b62154fda927bdbc14776afda816a3`.
- `/Users/chenyulin/Desktop/截屏2026-06-28 21.32.14.png`: `142x150`, `sha256=45be88df2edc6394c5b965119d01567de833e6bc46791ac80e5c3ed7be6a50d0`.

## Method Boundary

- Component names are user-provided guidance, not canon authority.
- QXBY / v0.3.1 reports are draft lookup evidence only.
- Jianpu, OCR surface text, old CSV rows, and page layout were not used as score facts.
- Every candidate remains `NEEDS_HUMAN_REVIEW`.

## Skill Upgrade Applied

- Used upgraded skill v0.2 with cross-phrase inheritance, `注下` lead-in handling, `掐起` attachment review, and v0.4 component roles.
- v0.4 correction note honored: raw_001=`撞`, raw_002=`轮`, raw_003=`急`; obsolete raw_001=轮/raw_003=撞 mapping was not used.
- G03 and G07 are read by phrase3 G04 pattern but remain human-review candidates.

## Continuous Candidate Reading

- 第四句候选：首字未定；撞；大指注下七徽，抹七弦；吟；上六三；撞；大指注下七徽，抹七弦；急就？；轮？；G10未定（下部六？）；散音起始，下部未定，句号。

## Summary Counts

- `component_labels_loaded`: 30
- `glyph_groups_segmented`: 11
- `matched_component_instances`: 20
- `score_event_candidates`: 11
- `unresolved_or_low_confidence_candidates`: 5

## Glyph Group Candidate Table

| glyph_group_id | source_image | bbox | matched_components | candidate_reading | confidence | review reason |
|---|---|---:|---|---|---|---|
| `LXY-P01-PH04-G001` | `截屏2026-06-28 21.31.57.png` | `2,8,133,131` | unmatched_component_candidate | right_hand_action_candidate=unknown_from_crop; left_hand_candidate=context_inherited? from phrase3 if no new left-hand/hui; string_no_candidate=unknown_from_crop; hui_position_candidate=context_inherited? needs review | seg=medium_high; match=low; parse=low | No confident component match; phrase-opening inheritance source also depends on phrase3 final review. |
| `LXY-P01-PH04-G002` | `截屏2026-06-28 21.31.57.png` | `264,57,328,112` | COMP-028 撞(high) | left_hand_candidate=撞; hui_position_candidate=context_inherited? needs review; position_transition_candidate=撞 | seg=high; match=high; parse=medium | 撞 is a left-hand transition/virtual attack candidate; host note and inherited position need review. |
| `LXY-P01-PH04-G003` | `截屏2026-06-28 21.31.57.png` | `427,10,532,123` | COMP-012 大指(medium); COMP-007 七(medium); COMP-025 注(medium); COMP-007 七(medium) | right_hand_action_candidate=抹; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=七徽; position_transition_candidate=注下 | seg=medium_high; match=medium; parse=medium | Read by upgraded phrase3 pattern; needs human confirmation for phrase4. |
| `LXY-P01-PH04-G004` | `截屏2026-06-28 21.31.57.png` | `550,79,597,129` | COMP-010 吟(medium_high) | left_hand_candidate=context_inherited from G003; hui_position_candidate=七徽 context_inherited; ornament_candidate=吟 | seg=high; match=medium_high; parse=medium_high | 吟 likely attaches to preceding G003 position; needs confirmation. |
| `LXY-P01-PH04-G005` | `截屏2026-06-28 21.31.57.png` | `863,40,918,141` | COMP-026 上(high); COMP-006 六(medium); COMP-016 三(medium) | left_hand_candidate=position transition; hui_position_candidate=六三徽 candidate; position_transition_candidate=上六三 | seg=high; match=high; parse=medium_high | Host/continuation scope needs human review. |
| `LXY-P01-PH04-G006` | `截屏2026-06-28 21.31.57.png` | `949,73,1012,115` | COMP-028 撞(high) | left_hand_candidate=撞; hui_position_candidate=context_inherited? 六三徽 candidate; position_transition_candidate=撞 | seg=high; match=high; parse=medium | 撞 likely modifies or transitions from the prior position; host note needs review. |
| `LXY-P01-PH04-G007` | `截屏2026-06-28 21.31.57.png` | `1087,14,1195,137` | COMP-012 大指(medium); COMP-007 七(medium); COMP-025 注(medium); COMP-007 七(medium) | right_hand_action_candidate=抹; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=七徽; position_transition_candidate=注下 | seg=medium; match=medium; parse=medium | Pattern match is plausible but boundary near following 急/就 needs review. |
| `LXY-P01-PH04-G008` | `截屏2026-06-28 21.31.57.png` | `1196,13,1285,137` | COMP-030 急(high); COMP-023 就(medium_low) | left_hand_candidate=context_inherited=true; hui_position_candidate=context_inherited=true; timing_marker_candidate=急; position_transition_candidate=就? | seg=medium; match=medium; parse=low | 急 is visible, but whether it combines with 就 and its scope need review. |
| `LXY-P01-PH04-G009` | `截屏2026-06-28 21.31.57.png` | `1280,13,1390,137` | COMP-029 轮(low) | right_hand_action_candidate=轮?; left_hand_candidate=context_inherited=true; string_no_candidate=unknown_from_crop; hui_position_candidate=context_inherited? | seg=medium; match=low; parse=low | v0.4 includes 轮 but visual match is weak; do not expand sequence without human review. |
| `LXY-P01-PH04-G010` | `截屏2026-06-28 21.31.57.png` | `1380,20,1480,134` | COMP-006 六(medium) | right_hand_action_candidate=unknown_from_crop; left_hand_candidate=unknown_from_crop; string_no_candidate=六? unresolved slot semantics; hui_position_candidate=六? unresolved slot semantics | seg=medium_high; match=medium_low; parse=low | Visible separate glyph; needs human reading before any parser handoff. |
| `LXY-P01-PH04-G011` | `截屏2026-06-28 21.32.14.png` | `26,22,137,134` | COMP-027 散音起始(high); COMP-005 句号(high) | right_hand_action_candidate=unknown_from_crop; string_no_candidate=unknown_from_crop; sound_state_transition_candidate=散音起始; punctuation_candidate=句号 | seg=high; match=medium_high; parse=medium_low | Upper 散音起始 and 句号 are visible; lower host remains unresolved. |

## Safety Boundary Confirmation

- No score import was performed.
- No canon authority or repo contract was created.
- No Dapu IR was written.
- No sample ingest, ML training data, recording plan, render output, or R0/R1/R2/E/F output was created.
