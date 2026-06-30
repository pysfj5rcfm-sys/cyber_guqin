# LXY Phrase 5 Component-Guided Candidates v0.1

Task id: `CG-LXY-PHRASE-05-COMPONENT-GUIDED-CANDIDATES-v0.1`

Status labels: `LXY_TRANSCRIPTION_DRAFT`, `USER_COMPONENT_LABEL_GUIDED`, `REFERENCE_COMPONENT_ATLAS_GUIDED`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`.

This is a report-only transcription draft for human review. It is not score import, canon authority, Dapu IR authority, sample ingest, ML training data, render output, recording plan, or R0/R1/R2/E/F output.

## Inputs Used

- `.agents/skills/cyber_guqin_component_guided_transcription/SKILL.md`: component-guided transcription skill, updated with P5 correction rules.
- `references/qxby_component_atlas/component_registry.v0.1.json`: reference component atlas, updated through `COMP-037 剔`.
- `/Users/chenyulin/Downloads/basic_components_named_v0.5.zip` (`sha256=e6ce2ffbbdfffe6693492aaa02a75bc719a24034712ad7fc11a46ccc16b28740`): user-confirmed component labels `COMP-031..036`.
- `/Users/chenyulin/Desktop/截屏2026-06-29 22.51.49.png` (`sha256=9eb03631a77bc63b5bde6ee59f340fd314636791371c073c5c777ac077405666`): user-confirmed `COMP-037 剔`; binary image not copied into repo.
- `/Users/chenyulin/Desktop/截屏2026-06-29 21.04.27.png`: phrase 5 front half.
- `/Users/chenyulin/Desktop/截屏2026-06-29 21.04.42.png`: phrase 5 back half with visible sentence punctuation.

Read order remains:

```text
references/qxby_component_atlas/component_registry.v0.1.json
→ references/qxby_component_atlas/construction_templates.v0.1.json
→ tests/fixtures/cyber_guqin/component_guided_transcription/lxy_p1_p4_gold_cases.v0.1.json
→ tests/fixtures/cyber_guqin/component_guided_transcription/lxy_p1_p4_forbidden_outputs.v0.1.json
→ 截屏2026-06-29 21.04.27.png
→ 截屏2026-06-29 21.04.42.png（有句号，是后半句）
```

## Continuous Candidate Reading

第五句候选（修订3）：大指绰上七徽，勾六弦；大指注下七徽，挑七弦；大指绰上七徽，勾六弦；上六四；大指注下七徽，抹挑七弦；双吟；名指七六徽，掐起；承前挑四弦；名指注下七九徽，勾三弦；落指猱；大指七徽，掩三弦；承前勾四；少息；上六四；进五六复；下七，名指七六徽，掐起；剔四弦，散三如一，句号。

## Glyph Group Candidate Table

Bounding boxes are approximate visual-inspection boxes in source-image pixel coordinates. They are not parser output.

| glyph_group_id | source image / half | approx_bbox | matched components | candidate reading | confidence | review reason |
|---|---|---:|---|---|---|---|
| `LXY-P01-PH05-G001` | front `21.04.27` | `0,0,205,145` | `COMP-012 大指`; `COMP-033 绰`; `COMP-026 上`; `COMP-007 七`; `COMP-020 勾`; `COMP-006 六` | `大指绰上七徽，勾六弦` | human-corrected medium_high | keep as review draft, not score authority |
| `LXY-P01-PH05-G002` | front `21.04.27` | `108,18,205,130` | `COMP-025 注`; `COMP-018 挑`; `COMP-007 七`; inherited 大指七徽 | `大指注下七徽，挑七弦` | human-corrected high | upper blank inherits prior 大指七徽 |
| `LXY-P01-PH05-G003` | front `21.04.27` | `236,8,330,146` | `COMP-012 大指`; `COMP-033 绰`; `COMP-026 上`; `COMP-007 七`; `COMP-020 勾`; `COMP-006 六` | `大指绰上七徽，勾六弦` | human-corrected high | corrected from previous 注下/勾七 guess |
| `LXY-P01-PH05-G004` | front `21.04.27` | `340,0,405,146` | `COMP-026 上`; `COMP-006 六`; `COMP-011 四` | `上六四` | human-corrected high | non-sounding position transition by default |
| `LXY-P01-PH05-G005` | front `21.04.27` | `558,0,658,147` | `COMP-012 大指`; `COMP-025 注`; `COMP-007 七`; `COMP-031 抹挑` | `大指注下七徽，抹挑七弦` | human-corrected high | compound action expansion remains reviewable |
| `LXY-P01-PH05-G006` | front `21.04.27` | `758,24,840,124` | `COMP-034 双吟` | `双吟` | medium | attachment target needs review |
| `LXY-P01-PH05-G007` | front `21.04.27` | `882,0,962,142` | `COMP-008 名指`; `COMP-007 七`; `COMP-006 六`; `COMP-022 掐起` | `名指七六徽，掐起` | human-corrected high | special-technique sounding policy remains reviewable |
| `LXY-P01-PH05-G008` | front `21.04.27` | `968,0,1172,144` | `COMP-018 挑`; `COMP-011 四`; `COMP-008 名指`; `COMP-025 注`; `COMP-007 七`; `COMP-020 勾`; `COMP-016 三` | `承前挑四弦；名指注下七九徽，勾三弦` | human-corrected high | first event inherits prior context; 七九 is user-corrected evidence |
| `LXY-P01-PH05-G009` | front `21.04.27` | `1180,8,1250,145` | `COMP-035 落指猱` | `落指猱` | medium | host position and sounding policy need review |
| `LXY-P01-PH05-G010` | front `21.04.27` | `1260,0,1356,146` | `COMP-012 大指`; `COMP-007 七`; `COMP-036 掩`; `COMP-016 三` | `大指七徽，掩三弦` | human-corrected high | keep candidate reviewable |
| `LXY-P01-PH05-G011` | back `21.04.42` | `18,16,100,140` | `COMP-020 勾`; `COMP-011 四` | `承前勾四` | human-corrected high | 勾 plus 四 must be read as 勾四 when construction supports it |
| `LXY-P01-PH05-G012` | back `21.04.42` | `150,36,232,128` | `COMP-003 少息` | `少息` | human-corrected medium_high | non-sounding timing marker; not `就` |
| `LXY-P01-PH05-G013` | back `21.04.42` | `276,8,368,144` | `COMP-026 上`; `COMP-006 六`; `COMP-011 四` | `上六四` | human-corrected high | corrected from `上六？` |
| `LXY-P01-PH05-G014` | back `21.04.42` | `420,0,610,148` | `COMP-024 进复`; `COMP-004 五`; `COMP-006 六` | `进五六复` | human-corrected high | corrected from previous uncertain target |
| `LXY-P01-PH05-G015` | back `21.04.42` | `650,0,824,146` | `COMP-007 七`; `COMP-008 名指`; `COMP-006 六`; `COMP-022 掐起` | `下七，名指七六徽，掐起` | human-corrected high | attachment and sounding policy remain reviewable |
| `LXY-P01-PH05-G016` | back `21.04.42` | `916,0,1138,148` | `COMP-037 剔`; `COMP-011 四`; `COMP-027 散音起始`; `COMP-016 三`; `COMP-032 如一声`; `COMP-005 句号` | `剔四弦，散三如一，句号` | human-corrected high | final construction includes newly registered `剔`; punctuation non-sounding |

## Three-Layer Replay Validation

P5 was replayed against the new three-layer stack:

- component registry loaded: `37` components (`COMP-001..037`)
- construction templates loaded: `42` templates
- P1-P4 phrase gold cases loaded: `4`
- forbidden-output guardrails loaded: `13`
- P5 glyph groups replayed: `16` / `16` matched expected template readings
- forbidden-output check: passed (`勾？`, `少息->就`, dropped `挑`, `COMP-027` mis-split, `抹挑->掩`, marker-as-sounding, and jianpu/OCR/CSV/layout authority patterns not present)

This replay is still `LXY_TRANSCRIPTION_DRAFT`, `NEEDS_HUMAN_REVIEW`, and `NOT_DAPU_IR_AUTHORITY`.

## Counts

- component labels loaded: `37`
- glyph groups segmented: `16`
- matched component instances: `58`
- score_event_candidates: `16`
- unresolved / low-confidence candidates: `3`

## Human Review Questions

1. For `G007/G015 掐起`, should a sounding string be recorded explicitly, or remain attached-special-technique only?
2. Are there remaining boundary issues around `G008`'s two-event split?

## Safety Boundary Confirmation

- used_jianpu_for_event_count: `false`
- used_old_csv_as_authority: `false`
- used_ocr_surface_as_score_fact: `false`
- used_page_layout_as_score_fact: `false`
- wrote_canon_authority: `false`
- wrote_dapu_ir: `false`
- wrote_sample_ingest: `false`
- wrote_ml_training_data: `false`
- wrote_render_output: `false`
- wrote_recording_plan: `false`
