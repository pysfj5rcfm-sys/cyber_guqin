# LXY Phrase 4 Component-Guided Candidates v0.1

Task id: `CG-LXY-COMPONENT-GUIDED-TRANSCRIPTION-SKILL-AND-PHRASE3-PHRASE4-v0.5_STAGE_B_CORRECTION`

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
- Prior phrase corrections are reusable construction templates, not canon authority.
- QXBY / v0.3.1 reports are draft lookup evidence only.
- Jianpu, OCR surface text, old CSV rows, and page layout were not used as score facts.
- Every candidate remains `NEEDS_HUMAN_REVIEW`.

## User Corrections Applied In This Update

- P4-G005 corrected from `上六三` to `上六二`.
- Inserted the missing event before `急进复`: `大指注下七徽，挑七弦`.
- `名指七六徽，掐起` corrected to `名指七六徽，掐起七弦`.
- Tail glyphs are renumbered after insertion: G008=`急进复`, G009=`名指七六徽，掐起七弦`, G010=`名指七九徽，挑六弦`, G011=`散音，挑五弦，句号`.

## Continuous Candidate Reading

- 第四句候选：大指六二徽，轮七弦；撞；大指注下七徽，抹七弦；吟；上六二；撞；大指注下七徽，挑七弦；急进复；名指七六徽，掐起七弦；名指七九徽，挑六弦；散音，挑五弦，句号。

## Summary Counts

- `component_labels_loaded`: 30
- `glyph_groups_segmented`: 11
- `matched_component_instances`: 34
- `score_event_candidates`: 11
- `unresolved_or_low_confidence_candidates`: 2

## Glyph Group Candidate Table

| glyph_group_id | source_image | bbox | matched_components | candidate_reading | confidence | review reason |
|---|---|---:|---|---|---|---|
| `LXY-P01-PH04-G001` | `截屏2026-06-28 21.31.57.png` | `2,8,133,131` | COMP-012 大指(high); COMP-006 六(medium); COMP-015 二(medium); COMP-029 轮(high); COMP-007 七(medium) | right_hand_action_candidate=轮; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=六二徽 | seg=high; match=high; parse=high | User correction; 轮 subaction expansion remains parser-stage/review work. |
| `LXY-P01-PH04-G002` | `截屏2026-06-28 21.31.57.png` | `264,57,328,112` | COMP-028 撞(high) | left_hand_candidate=撞; hui_position_candidate=context_inherited from G001 六二徽?; position_transition_candidate=撞 | seg=high; match=high; parse=medium | Host/attachment to preceding G001 position needs review. |
| `LXY-P01-PH04-G003` | `截屏2026-06-28 21.31.57.png` | `427,10,532,123` | COMP-012 大指(medium); COMP-007 七(medium); COMP-025 注(medium); COMP-007 七(medium) | right_hand_action_candidate=抹; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=七徽; position_transition_candidate=注下 | seg=medium_high; match=medium; parse=medium_high | Template reuse from P3-G04; still reviewable. |
| `LXY-P01-PH04-G004` | `截屏2026-06-28 21.31.57.png` | `550,79,597,129` | COMP-010 吟(medium_high) | left_hand_candidate=context_inherited from G003; hui_position_candidate=七徽 context_inherited; ornament_candidate=吟 | seg=high; match=high; parse=medium_high | Attachment to preceding position needs review. |
| `LXY-P01-PH04-G005` | `截屏2026-06-28 21.31.57.png` | `863,40,918,141` | COMP-026 上(high); COMP-006 六(medium); COMP-015 二(medium) | left_hand_candidate=position transition; hui_position_candidate=六二徽 candidate; position_transition_candidate=上六二 | seg=high; match=high; parse=high | User correction from 上六三 to 上六二. |
| `LXY-P01-PH04-G006` | `截屏2026-06-28 21.31.57.png` | `949,73,1012,115` | COMP-028 撞(high) | left_hand_candidate=撞; hui_position_candidate=context_inherited from G005 六三徽?; position_transition_candidate=撞 | seg=high; match=high; parse=medium | Host/attachment to prior position needs review. |
| `LXY-P01-PH04-G007` | `截屏2026-06-28 21.31.57.png` | `1087,14,1195,137` | COMP-012 大指(medium); COMP-007 七(medium); COMP-025 注(medium); COMP-018 挑(high); COMP-007 七(medium) | right_hand_action_candidate=挑; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=七徽; position_transition_candidate=注下 | seg=medium; match=medium_high; parse=high | User correction: this missing event occurs before 急进复. |
| `LXY-P01-PH04-G008` | `截屏2026-06-28 21.31.57.png` | `1196,13,1240,137` | COMP-030 急(high); COMP-024 进复(medium) | timing_marker_candidate=急; position_transition_candidate=进复; left_hand_candidate=position transition; hui_position_candidate=context_inherited? needs review | seg=medium; match=medium; parse=medium_high | Boundary remains approximate after user correction. |
| `LXY-P01-PH04-G009` | `截屏2026-06-28 21.31.57.png` | `1196,13,1285,137` | COMP-008 名指(medium); COMP-007 七(medium); COMP-006 六(medium); COMP-022 掐起(high) | right_hand_action_candidate=掐起 sounding action candidate; left_hand_candidate=名指; string_no_candidate=七; hui_position_candidate=七六徽; special_technique_candidate=掐起 | seg=medium; match=medium; parse=medium_high | User correction adds 七弦 to 掐起. |
| `LXY-P01-PH04-G010` | `截屏2026-06-28 21.31.57.png` | `1245,13,1480,137` | COMP-008 名指(medium); COMP-007 七(medium); COMP-018 挑(high); COMP-006 六(medium) | right_hand_action_candidate=挑; left_hand_candidate=名指; string_no_candidate=六; hui_position_candidate=七九徽 | seg=medium_high; match=medium_high; parse=high | User correction; bbox merges the earlier over-split tail glyphs. |
| `LXY-P01-PH04-G011` | `截屏2026-06-28 21.32.14.png` | `26,22,137,134` | COMP-027 散音起始(high); COMP-018 挑(high); COMP-004 五(medium); COMP-005 句号(high) | right_hand_action_candidate=挑; string_no_candidate=五; sound_state_transition_candidate=散音; punctuation_candidate=句号 | seg=high; match=high; parse=high | User correction: same construction as P3-G10. |

## Safety Boundary Confirmation

- No score import was performed.
- No canon authority or repo contract was created.
- No Dapu IR was written.
- No sample ingest, ML training data, recording plan, render output, or R0/R1/R2/E/F output was created.
