# LXY Phrase 6 Component-Guided Candidates v0.1

Task id: `CG-LXY-PHRASE-06-COMPONENT-GUIDED-CANDIDATES-v0.1`

Status labels: `LXY_TRANSCRIPTION_DRAFT, USER_COMPONENT_LABEL_GUIDED, REFERENCE_COMPONENT_ATLAS_GUIDED, REFERENCE_CONSTRUCTION_TEMPLATE_GUIDED, NOT_CANON_AUTHORITY, NOT_REPO_CONTRACT, NOT_DAPU_IR_AUTHORITY, NEEDS_HUMAN_REVIEW, NOT_SAMPLE_INGEST, NOT_ML_TRAINING_DATA, NOT_RENDER_OUTPUT`.

This is a report-only transcription draft for human review. It is not canon authority, not Dapu IR authority, not sample ingest, not ML training data, and not render output.

Revision note: old-component rescan applied after user correction. Visible `COMP-001..037` components are reused; jianpu, old OCR, spacing, and layout remain rejected as score authority.

## Inputs Used

- `/Users/chenyulin/Desktop/截屏2026-06-30 19.11.50.png`: phrase6 front half.
- `/Users/chenyulin/Desktop/截屏2026-06-30 19.12.04.png`: phrase6 back half.
- `/Users/chenyulin/Desktop/截屏2026-06-30 19.55.43.png`: `COMP-038 右手指法 双弹`.

Fixed order:

```text
19.11.50 -> phrase6 前半句
19.12.04 -> phrase6 后半句
```

## Continuous Candidate Reading

第六句候选（旧构件复核）：勾五；勾二；勾三；勾五六？；双弹三弦；勾五；勾三；勾三；勾五六？，句号。

## Notes

- `勾五 / 勾二 / 勾三` are read from visible old components in the crop, not from jianpu.
- The two `勾五六？` candidates visibly contain `COMP-004 五`, `COMP-006 六`, and `COMP-020 勾`, but the construction policy for one `勾` plus two string numbers remains unconfirmed.
- `双弹三弦` remains `TEMPLATE-SHUANGTAN-3`; expansion and simultaneity policy need review.

## Visual Block Coverage Ledger

| visual_block_id | source | visual_block_bbox | contained notation units | unread_ink | stop_reason |
| --- | --- | ---: | --- | --- | --- |
| `LXY-P01-PH06-VB001` | phrase6_front_19.11.50 | `3,0,208,149` | `LXY-P01-PH06-VB001-NU001`, `LXY-P01-PH06-VB001-NU002` | none | `all_ink_covered_by_units` |
| `LXY-P01-PH06-VB002` | phrase6_front_19.11.50 | `269,22,354,149` | `LXY-P01-PH06-VB002-NU003` | none | `all_ink_covered_by_units` |
| `LXY-P01-PH06-VB003` | phrase6_back_19.12.04 | `25,1,118,141` | `LXY-P01-PH06-VB003-NU004` | none | `all_visible_components_accounted_but_construction_policy_needs_review` |
| `LXY-P01-PH06-VB004` | phrase6_back_19.12.04 | `207,1,391,141` | `LXY-P01-PH06-VB004-NU005` | none | `all_ink_covered_by_units` |
| `LXY-P01-PH06-VB005` | phrase6_back_19.12.04 | `414,1,597,141` | `LXY-P01-PH06-VB005-NU006`, `LXY-P01-PH06-VB005-NU007` | none | `all_ink_covered_by_units` |
| `LXY-P01-PH06-VB006` | phrase6_back_19.12.04 | `681,28,769,126` | `LXY-P01-PH06-VB006-NU008` | none | `all_ink_covered_by_units` |
| `LXY-P01-PH06-VB007` | phrase6_back_19.12.04 | `930,1,1048,141` | `LXY-P01-PH06-VB007-NU009` | none | `all_visible_components_accounted_but_construction_policy_needs_review` |

## Notation Unit Table

| notation_unit_id | source | approx_bbox | matched components | candidate reading | confidence / review |
| --- | --- | ---: | --- | --- | --- |
| `LXY-P01-PH06-VB001-NU001` | phrase6_front_19.11.50 | `3,0,114,149` | `COMP-020 勾`; `COMP-004 五` | 勾五 | medium / OLD_COMPONENT_RESCAN_MATCHED_GOU_PLUS_VISIBLE_STRING_5 |
| `LXY-P01-PH06-VB001-NU002` | phrase6_front_19.11.50 | `121,0,208,149` | `COMP-020 勾`; `COMP-015 二` | 勾二 | medium_high / OLD_COMPONENT_RESCAN_MATCHED_GOU_PLUS_VISIBLE_STRING_2 |
| `LXY-P01-PH06-VB002-NU003` | phrase6_front_19.11.50 | `269,22,354,149` | `COMP-020 勾`; `COMP-016 三` | 勾三 | high / OLD_COMPONENT_RESCAN_MATCHED_GOU_PLUS_VISIBLE_STRING_3 |
| `LXY-P01-PH06-VB003-NU004` | phrase6_back_19.12.04 | `25,1,118,141` | `COMP-020 勾`; `COMP-004 五`; `COMP-006 六` | 勾五六？ | low / VISIBLE_GOU_PLUS_5_6_BUT_CONSTRUCTION_POLICY_UNCONFIRMED |
| `LXY-P01-PH06-VB004-NU005` | phrase6_back_19.12.04 | `207,1,391,141` | `COMP-038 双弹`; `COMP-016 三` | 双弹三弦 | medium_high / DOUBLE_PLUCK_EXPANSION_AND_SIMULTANEITY_POLICY_NEEDS_REVIEW |
| `LXY-P01-PH06-VB005-NU006` | phrase6_back_19.12.04 | `414,1,500,141` | `COMP-020 勾`; `COMP-004 五` | 勾五 | medium / OLD_COMPONENT_RESCAN_MATCHED_GOU_PLUS_VISIBLE_STRING_5 |
| `LXY-P01-PH06-VB005-NU007` | phrase6_back_19.12.04 | `513,1,597,141` | `COMP-020 勾`; `COMP-016 三` | 勾三 | high / OLD_COMPONENT_RESCAN_MATCHED_GOU_PLUS_VISIBLE_STRING_3 |
| `LXY-P01-PH06-VB006-NU008` | phrase6_back_19.12.04 | `681,28,769,126` | `COMP-020 勾`; `COMP-016 三` | 勾三 | high / OLD_COMPONENT_RESCAN_MATCHED_GOU_PLUS_VISIBLE_STRING_3 |
| `LXY-P01-PH06-VB007-NU009` | phrase6_back_19.12.04 | `930,1,1048,141` | `COMP-020 勾`; `COMP-004 五`; `COMP-006 六`; `COMP-005 句号` | 勾五六？，句号 | low / VISIBLE_GOU_PLUS_5_6_BUT_CONSTRUCTION_POLICY_UNCONFIRMED |

## Counts

- component labels loaded: `38`
- visual blocks segmented: `7`
- notation units decomposed: `9`
- matched component instances: `21`
- construction templates matched: `4`
- score_event_candidates: `9`
- unresolved / low-confidence candidates: `2`

## Safety Boundary Confirmation

- used_jianpu_for_event_count: `false`
- used_jianpu_for_string_or_hui: `false`
- used_old_csv_as_authority: `false`
- used_ocr_surface_as_score_fact: `false`
- used_page_layout_as_score_fact: `false`
- wrote_canon_authority: `false`
- wrote_dapu_ir: `false`
- wrote_sample_ingest: `false`
- wrote_ml_training_data: `false`
- wrote_render_output: `false`
