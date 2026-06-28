# LXY Phrase 3 Component-Guided Candidates v0.1

Task id: `CG-LXY-COMPONENT-GUIDED-TRANSCRIPTION-SKILL-AND-PHRASE3-PHRASE4-v0.3_STAGE_A`

Status labels: `LXY_TRANSCRIPTION_DRAFT`, `USER_COMPONENT_LABEL_GUIDED`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`.

This is a report-only component-guided transcription draft. It is not score import, canon authority, Dapu IR authority, sample ingest, ML training data, recording plan, or render output.

## Inputs Used

- `/Users/chenyulin/Downloads/basic_components_named_v0.2.zip` (`sha256=ac4330df2c5d8b234d6cdb16ab9141692faf7553ab599391047b7a6a4a9817ac`): base user-provided components COMP-001..COMP-020.
- `/Users/chenyulin/Downloads/basic_components_named_v0.3.zip` (`sha256=77bf5daaffeb9a1c7b0dab6241a2d89ca0bd20cff0c0e73c9070fbaac34c50b5`): additional user-confirmed components COMP-021..COMP-027.
- `/Users/chenyulin/Desktop/截屏2026-06-28 20.24.15.png`: `1302x150`, `sha256=5fb99156e293feacef37ddc8640732bccaf1e9def4c32b85b9dae649d448c303`.
- `/Users/chenyulin/Desktop/截屏2026-06-28 20.24.30.png`: `154x150`, `sha256=6eb89dccad7b2d83611d508a03f717947d3043bb473e34a205e20169ad105edf`.

## Method Boundary

- Component names are user-provided guidance, not canon authority.
- QXBY / v0.3.1 reports are draft lookup evidence only.
- Jianpu, OCR surface text, old CSV rows, and page layout were not used as score facts.
- Every candidate remains `NEEDS_HUMAN_REVIEW`.

## User Corrections Applied In This Update

- G01 is phrase3 opening; cross-phrase inheritance looks back to phrase2 final `大指六二徽` context.
- G04 is not `COMP-027`; it reads `大指注下七徽，抹七弦`, with `注下` as a lead-in before the target hui.
- G05 is `吟`.
- G06 is `上六二`.
- G07 is read by analogy with G04.
- G08 lower component is `掐起`; user/theory-assisted candidate is `名指七六徽，掐起七弦`.
- G09 is kept as a separate visible glyph candidate.
- G10 upper component is `COMP-027 散音起始`; lower host remains unresolved.

## Continuous Candidate Reading

- 第三句候选：承前大指六二徽背锁；进五六复，就；大指注下七徽，抹七弦；吟；上六二；大指注下七徽，抹七弦；名指七六徽，掐起七弦；G09未定（下部六？）；散音起始，下部未定，句号。

## Summary Counts

- `component_labels_loaded`: 27
- `glyph_groups_segmented`: 10
- `matched_component_instances`: 23
- `score_event_candidates`: 10
- `unresolved_or_low_confidence_candidates`: 4

## Glyph Group Candidate Table

| glyph_group_id | source_image | bbox | matched_components | candidate_reading | confidence | review reason |
|---|---|---:|---|---|---|---|
| `LXY-P01-PH03-G001` | `截屏2026-06-28 20.24.15.png` | `19,11,118,138` | COMP-021 背锁(high) | right_hand_action_candidate=背锁; left_hand_candidate=大指 (context_inherited from phrase2 final); string_no_candidate=unknown_from_crop; hui_position_candidate=六二徽 (context_inherited from phrase2 final) | seg=high; match=high; parse=medium | G01 is phrase3 opening; inherited left-hand/hui must look back into phrase2, but 背锁 string span remains review-needed. |
| `LXY-P01-PH03-G002` | `截屏2026-06-28 20.24.15.png` | `271,20,332,139` | COMP-024 进复(high); COMP-004 五(medium); COMP-006 六(medium) | left_hand_candidate=position transition; hui_position_candidate=五六徽 candidate; position_transition_candidate=进五六复 | seg=medium; match=medium; parse=medium | Position-transition attachment and scope need review. |
| `LXY-P01-PH03-G003` | `截屏2026-06-28 20.24.15.png` | `360,16,430,149` | COMP-023 就(medium) | left_hand_candidate=context_inherited=true; hui_position_candidate=context_inherited from G002 五六徽 candidate; position_transition_candidate=就 | seg=medium; match=medium; parse=medium_low | Confirm whether 就 inherits G002 position into the following note. |
| `LXY-P01-PH03-G004` | `截屏2026-06-28 20.24.15.png` | `525,16,613,132` | COMP-012 大指(medium_high); COMP-007 七(medium); COMP-025 注(medium); COMP-007 七(medium) | right_hand_action_candidate=抹; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=七徽; position_transition_candidate=注下 | seg=medium_high; match=medium_high; parse=high | User corrected reading; remains report-only and needs final human confirmation. |
| `LXY-P01-PH03-G005` | `截屏2026-06-28 20.24.15.png` | `648,80,697,127` | COMP-010 吟(high) | left_hand_candidate=大指 / 七徽 context_inherited from G004; hui_position_candidate=七徽 context_inherited; ornament_candidate=吟 | seg=high; match=high; parse=high | User corrected G05 as 吟; attachment to G004 position remains review-needed. |
| `LXY-P01-PH03-G006` | `截屏2026-06-28 20.24.15.png` | `792,31,858,132` | COMP-026 上(high); COMP-006 六(medium); COMP-015 二(medium) | left_hand_candidate=position transition; hui_position_candidate=六二徽 candidate; position_transition_candidate=上六二 | seg=high; match=high; parse=high | User corrected G06 as 上六二; host/continuation scope needs review. |
| `LXY-P01-PH03-G007` | `截屏2026-06-28 20.24.15.png` | `956,21,1044,137` | COMP-012 大指(medium); COMP-007 七(medium); COMP-025 注(medium); COMP-007 七(medium) | right_hand_action_candidate=抹; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=七徽; position_transition_candidate=注下 | seg=medium; match=medium; parse=medium | User asked to compare with G04; exact visual components still need confirmation. |
| `LXY-P01-PH03-G008` | `截屏2026-06-28 20.24.15.png` | `1066,7,1156,129` | COMP-022 掐起(high); COMP-008 名指(low); COMP-007 七(medium_low) | right_hand_action_candidate=掐起 sounding action candidate; left_hand_candidate=名指 (human correction; upper unclear); string_no_candidate=七; hui_position_candidate=七六徽 (theory_assisted_review_evidence); special_technique_candidate=掐起 | seg=medium; match=medium_low; parse=medium | Upper component is unclear; 名指七六徽 comes from user/theory-assisted correction, not crop-only evidence. |
| `LXY-P01-PH03-G009` | `截屏2026-06-28 20.24.15.png` | `1179,19,1281,132` | COMP-006 六(medium) | right_hand_action_candidate=unknown_from_crop; left_hand_candidate=unknown_from_crop; string_no_candidate=六? unresolved slot semantics; hui_position_candidate=六? unresolved slot semantics; special_technique_candidate=unknown_from_crop | seg=medium_high; match=medium_low; parse=low | User noted G09 was missed; keep separate and request human reading. |
| `LXY-P01-PH03-G010` | `截屏2026-06-28 20.24.30.png` | `36,24,131,132` | COMP-027 散音起始(high); COMP-005 句号(high) | right_hand_action_candidate=unknown_from_crop; string_no_candidate=unknown_from_crop; sound_state_transition_candidate=散音起始; punctuation_candidate=句号 | seg=high; match=medium_high; parse=medium_low | User corrected upper as COMP-027; lower host remains unresolved. |

## Safety Boundary Confirmation

- No score import was performed.
- No canon authority or repo contract was created.
- No Dapu IR was written.
- No sample ingest, ML training data, recording plan, render output, or R0/R1/R2/E/F output was created.
