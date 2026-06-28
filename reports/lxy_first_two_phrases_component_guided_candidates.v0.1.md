# LXY First Two Phrases Component-Guided Candidates v0.1

Task id: `CG-LXY-FIRST-TWO-PHRASES-COMPONENT-GUIDED-CANDIDATES-v0.1`

Status labels: `LXY_TRANSCRIPTION_DRAFT`, `USER_COMPONENT_LABEL_GUIDED`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`.

This remains a report-only recognition draft. It is not score import, canon authority, Dapu IR authority, sample ingest, ML training data, or render output.

## Inputs Used

- `/Users/chenyulin/Downloads/basic_components_named_v0.2.zip` (`sha256=ac4330df2c5d8b234d6cdb16ab9141692faf7553ab599391047b7a6a4a9817ac`)
- `/Users/chenyulin/Desktop/截屏2026-06-28 17.31.19.png`: original score first line; contains phrase 1 and most of phrase 2.
- `/Users/chenyulin/Desktop/截屏2026-06-28 17.31.36.png`: user clarified this is the final note of phrase 2 at the opening of original score line 2.

## Method Boundary

- Component names are `USER_PROVIDED_LABEL`, not canon authority.
- QXBY lexicon and visual atlas were used only as draft lookup evidence.
- Jianpu, OCR surface text, old CSV rows, and page layout were not used as score facts.
- Every candidate remains `NEEDS_HUMAN_REVIEW`.

## User Corrections Applied

- 数字在右上槽位读作徽位；在中下或右手指法内部读作弦数。
- 无新左手指法/徽位时承前，直到最近明确的左手/徽位或散泛按状态。
- `COMP-018 挑` 是 `乙` 形下承结构；G09 是 `挑六`，G13 是 `挑四`。
- `历=连挑`，因此 `历五四` 按五弦到四弦读。
- 第二张图不是 G06 放大，而是第二句最后一个音。

## Continuous Candidate Reading

- 第一句候选：泛起：中指七徽勾一，名指七徽勾二，承前勾三，泛止；大指按六二徽，托七弦。
- 第二句候选：承前大指六二徽吟，爪起；名指泛七徽挑六，少息，承前历五四，承前勾三，承前挑四，承前勾三，泛止；大指按六二徽，托七弦。

## Summary Counts

- `component_labels_loaded`: 20
- `glyph_groups_segmented`: 16
- `matched_component_instances`: 41
- `score_event_candidates`: 16
- `unresolved_or_low_confidence_candidates`: 3

## Glyph Group Candidate Table

| glyph_group_id | phrase | source_image | bbox | matched_components | candidate_reading | confidence | review reason |
|---|---|---|---:|---|---|---|---|
| `LXY-P01-PH01-G001` | `LXY-P01-PH01` | `截屏2026-06-28 17.31.19.png` | `1,17,73,117` | COMP-002 泛起(high) | fan_state_transition_candidate=enter_harmonic_state_candidate | seg=high; match=high; parse=medium | Confirm scope of 泛起 context across following groups. |
| `LXY-P01-PH01-G002` | `LXY-P01-PH01` | `截屏2026-06-28 17.31.19.png` | `85,17,177,118` | COMP-013 中指(high); COMP-007 七(medium); COMP-020 勾(high); COMP-009 一(medium) | right_hand_action_candidate=勾; left_hand_candidate=中指; string_no_candidate=一; hui_position_candidate=七徽 | seg=high; match=medium; parse=medium | Needs human review before authority; user-guided reading accepted as draft evidence. |
| `LXY-P01-PH01-G003` | `LXY-P01-PH01` | `截屏2026-06-28 17.31.19.png` | `192,20,276,127` | COMP-008 名指(medium); COMP-007 七(medium_low); COMP-020 勾(medium); COMP-015 二(medium) | right_hand_action_candidate=勾; left_hand_candidate=名指; string_no_candidate=二; hui_position_candidate=七徽 | seg=medium; match=medium_low; parse=medium_low | G03 is visually less clean than G02; keep as candidate pending human review. |
| `LXY-P01-PH01-G004` | `LXY-P01-PH01` | `截屏2026-06-28 17.31.19.png` | `297,30,384,118` | COMP-020 勾(high); COMP-016 三(high) | right_hand_action_candidate=勾; left_hand_candidate=名指 (context_inherited); string_no_candidate=三; hui_position_candidate=七徽 (context_inherited) | seg=high; match=high; parse=medium | Confirm that inheritance from G003 applies through this group. |
| `LXY-P01-PH01-G005` | `LXY-P01-PH01` | `截屏2026-06-28 17.31.19.png` | `395,63,448,112` | COMP-017 泛止(medium) | fan_state_transition_candidate=exit_harmonic_state_candidate | seg=high; match=medium; parse=medium | Confirm exact placement of 泛止 boundary. |
| `LXY-P01-PH01-G006` | `LXY-P01-PH01` | `截屏2026-06-28 17.31.19.png` | `460,7,612,128` | COMP-012 大指(high); COMP-006 六(medium); COMP-015 二(medium); COMP-001 托(high); COMP-007 七(medium); COMP-005 句号(high) | right_hand_action_candidate=托; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=六二徽; punctuation_candidate=句号 | seg=high; match=medium; parse=medium | User-provided example confirms this construction pattern; still report-only draft. |
| `LXY-P01-PH02-G001` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `624,69,702,150` | COMP-010 吟(medium) | left_hand_candidate=大指 (context_inherited); hui_position_candidate=六二徽 (context_inherited); ornament_candidate=吟 | seg=medium_low; match=medium; parse=low | Phrase-boundary effect on inheritance must be reviewed. |
| `LXY-P01-PH02-G002` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `802,31,877,133` | COMP-019 爪起(medium) | left_hand_candidate=大指? (context_inherited); hui_position_candidate=六二徽? (context_inherited); special_technique_candidate=爪起 | seg=medium; match=medium; parse=low | Need confirm whether 爪起 attaches to previous pressed position or starts a separate construction. |
| `LXY-P01-PH02-G003` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `922,14,1104,117` | COMP-008 名指(high); COMP-007 七(medium); COMP-018 挑(high); COMP-006 六(medium) | right_hand_action_candidate=挑; left_hand_candidate=名指; string_no_candidate=六; hui_position_candidate=七徽 | seg=high; match=medium; parse=medium | User-corrected draft reading; still not canon authority. |
| `LXY-P01-PH02-G004` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `1125,50,1190,122` | COMP-003 少息(high) | timing_marker_candidate=少息 | seg=high; match=high; parse=medium | Confirm duration/scope of 少息. |
| `LXY-P01-PH02-G005` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `1200,22,1317,135` | COMP-014 历(high); COMP-004 五(high); COMP-011 四(high) | right_hand_action_candidate=历; left_hand_candidate=名指 (context_inherited); string_no_candidate=五四; hui_position_candidate=七徽 (context_inherited) | seg=high; match=high; parse=medium | Confirm sounding-unit split and direction, but user confirmed 五四 order. |
| `LXY-P01-PH02-G006` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `1390,26,1483,125` | COMP-020 勾(high); COMP-016 三(high) | right_hand_action_candidate=勾; left_hand_candidate=名指 (context_inherited); string_no_candidate=三; hui_position_candidate=七徽 (context_inherited) | seg=high; match=high; parse=medium | Confirm inheritance chain G12 -> G11 -> G09. |
| `LXY-P01-PH02-G007` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `1497,58,1598,117` | COMP-018 挑(high); COMP-011 四(high) | right_hand_action_candidate=挑; left_hand_candidate=名指 (context_inherited); string_no_candidate=四; hui_position_candidate=七徽 (context_inherited) | seg=high; match=high; parse=medium | User correction: this is 挑四弦, not bare 四弦. |
| `LXY-P01-PH02-G008` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `1626,25,1718,124` | COMP-020 勾(high); COMP-016 三(high) | right_hand_action_candidate=勾; left_hand_candidate=名指 (context_inherited); string_no_candidate=三; hui_position_candidate=七徽 (context_inherited) | seg=high; match=high; parse=medium | Confirm inheritance across preceding groups. |
| `LXY-P01-PH02-G009` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.19.png` | `1726,60,1788,122` | COMP-017 泛止(medium) | fan_state_transition_candidate=exit_harmonic_state_candidate | seg=high; match=medium; parse=medium | Confirm exact scope of the close marker. |
| `LXY-P01-PH02-G010` | `LXY-P01-PH02` | `截屏2026-06-28 17.31.36.png` | `13,13,138,139` | COMP-012 大指(high); COMP-006 六(medium); COMP-015 二(medium); COMP-001 托(high); COMP-007 七(medium); COMP-005 句号(high) | right_hand_action_candidate=托; left_hand_candidate=大指; string_no_candidate=七; hui_position_candidate=六二徽; punctuation_candidate=句号 | seg=high; match=medium; parse=medium | Final-note placement comes from user clarification; still report-only draft. |

## Safety Boundary Confirmation

- No score import was performed.
- No canon authority or repo contract was created.
- No Dapu IR was written.
- No sample ingest, ML training data, render output, or runtime output was created.
- Only report files under `reports/` were written.
