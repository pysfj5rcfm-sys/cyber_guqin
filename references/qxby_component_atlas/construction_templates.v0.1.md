# QXBY Construction Templates v0.1

Task id: `CG-LXY-THREE-LAYER-COMPONENT-GUIDED-REGRESSION-v0.1`

Status labels: `CONSTRUCTION_TEMPLATE_REFERENCE`, `USER_REVIEWED_CONSTRUCTION_GUIDANCE`, `TRANSCRIPTION_DRAFT_SUPPORT_ONLY`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`.

This is layer 2 of the component-guided transcription stack. It records reusable P1-P6 construction templates, not canon authority, not repo contract, and not Dapu IR authority.

## Required Read Order

```text
component_registry.v0.1.json
→ construction_templates.v0.1.json
→ regression gold / forbidden fixtures
→ task-approved QXBY and v0.3.1 reports
→ current phrase crop
```

## Template Groups

### basic_right_hand_string

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-GOU-1` | 勾一 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-GOU-2` | 勾二 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-GOU-3` | 勾三 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-TUO-7` | 托七 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-TIAO-6` | 挑六 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-TIAO-4` | 挑四 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-TI-4` | 剔四弦 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |

### compound_right_hand_sequence

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-LI-5-4` | 历五四 | should_have | 历 is 连挑; when user confirms 历五四, read 五到四, not layout-derived order.; Do not use jianpu or spacing to infer the span. |
| `TEMPLATE-LUN-7` | 轮七 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-SHUANGTAN-3` | 双弹三弦 | supporting | COMP-038 双弹 must not be confused with COMP-034 双吟 or COMP-032 如一声.; Do not expand 双弹 into final Dapu IR without human review. |
| `TEMPLATE-BEISUO` | 背锁 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |

### state_plus_right_hand_string

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-SAN-TIAO-5` | 散音，挑五 | must_have | COMP-027 散音起始 is the upper/open-string state layer; lower 挑五 supplies the right-hand/string construction.; Do not misread the connected grass-head-like COMP-027 as 大指 plus hui number. |
| `TEMPLATE-SAN-GOU-1` | 散音，勾一弦 | must_have | COMP-027 散音起始 must be recognized as a whole open-string state layer before local numeric matching.; Do not split the connected COMP-027 shape into 五, 六, 大指, or hui fragments. |

### left_hand_hui_right_hand

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-DA-6-2-LUN-7` | 大指六二徽，轮七弦 | must_have | Preserve v0.4 correction: COMP-029 is 轮 and COMP-028 is 撞.; Do not fall back to raw_001=轮 or raw_003=撞 mappings. |
| `TEMPLATE-ZHUXIA-MO-7` | 大指注下七徽，抹七弦 | must_have | Read visible 抹 as the right-hand action; do not substitute 挑 unless COMP-018 is visible.; 注下 remains an approach/lead-in candidate and stays reviewable. |
| `TEMPLATE-ZHUXIA-TIAO-7` | 大指注下七徽，挑七弦 | must_have | Blank upper slots may inherit the current left-hand/hui context; do not silently drop the inherited left-hand/hui fields.; Do not copy 抹 from a neighboring template when the visible right-hand action is COMP-018 挑. |
| `TEMPLATE-DA-CHUOSHANG-7-GOU-6` | 大指绰上七徽，勾六弦 | must_have | 绰 and 注 are paired approach concepts; read 绰 + 七徽 as 绰上七徽 when construction supports it.; Do not require a separate free-standing 上 component before allowing 绰上. |
| `TEMPLATE-ZHUXIA-MOTIAO-7` | 大指注下七徽，抹挑七弦 | must_have | COMP-031 抹挑 is a compound right-hand action and must not be confused with COMP-036 掩.; Expansion of 抹挑 remains report-only and needs human review. |
| `TEMPLATE-MING-ZHUXIA-7-9-GOU-3` | 名指注下七九徽，勾三弦 | should_have | 七九 is a hui-position candidate in the upper/right-upper context, not a string pair.; 勾 + 三 must be read as 勾三弦 when construction supports it. |
| `TEMPLATE-YAN-3` | 大指七徽，掩三弦 | should_have | COMP-036 掩 plus 三 is read as 掩三弦 when construction supports it.; Do not confuse 掩 with COMP-031 抹挑. |
| `TEMPLATE-DA-6-2-TUO-7` | 大指六二徽，托七弦 | should_have | 数字六二 in right-upper slot is hui position, not strings.; Embedded 七 inside/near 托 is string number. |
| `TEMPLATE-MING-7-6-GOU-4` | 名指七六徽，勾四弦 | must_have | Run this compound template before generic 勾 + numeric decomposition when 名指 + right-upper 七六 + 勾四 is visible.; Do not output 勾五六？, bare 五六, or unresolved numeric strings. |

### left_hand_position_transition

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-ZHUANG` | 撞 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-JI-JINFU` | 急进复 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-JINFU-5-6` | 进五六复 | should_have | 进五六复 is a left-hand position/hui transition candidate; 五六 is not a string span here.; Do not infer this from jianpu or spacing. |
| `TEMPLATE-SHANG-6-2` | 上六二 | should_have | 上六二 is a left-hand position/hui transition candidate; nearby 六二 is read as hui target by construction.; Do not read it as strings 六 and 二. |
| `TEMPLATE-SHANG-6-4` | 上六四 | should_have | 上六四 is a hui-position transition candidate, not strings 六 and 四.; Do not output 上六？ when 四 is visible. |
| `TEMPLATE-XIA-7` | 下七 | supporting | Do not treat 下七 as an independent plucked note by default.; Attachment to following 名指七六徽，掐起 remains reviewable. |

### context_inheritance_marker

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-JIU-CONTEXT` | 就=承前 | must_have | 就 is a context-inheritance marker and is normally rendered as 承前 behavior in continuous reading.; Do not confuse 就 with 少息. |

### non_sounding_marker

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-FAN-QI` | 泛起 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-FAN-ZHI` | 泛止 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-SHAOXI` | 少息 | must_have | 少息 is a timing marker, not 就.; Do not generate a sounding_unit for 少息. |
| `TEMPLATE-JUHAO` | 句号 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |

### special_technique_attachment

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-LH-7-6-QIAQI-7` | 名指七六徽，掐起七弦 | must_have | 掐起七弦 remains a special-technique reading candidate and needs review for sounding policy.; Do not detach 掐起 from its left-hand/hui context. |
| `TEMPLATE-YIN` | 吟 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-ZHAOQI` | 爪起 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-MING-7-6-QIAQI` | 名指七六徽，掐起 | must_have | 掐起 binds to a held left-hand position, often 名指 or 跪指, but the target hui must not be hardcoded generically as 七六徽.; If 三分损益法 or tuning logic is used to infer hui, record it as human/theory-assisted review evidence, not crop-only evidence. |
| `TEMPLATE-SHUANGYIN` | 双吟 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-LUOZHI-NAO` | 落指猱 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |
| `TEMPLATE-RUYISHENG` | 如一声 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |

### general_construction_template

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-MING-7-TIAO-6` | 名指七九徽，挑六弦 | supporting | Template reuse remains report-only and NEEDS_HUMAN_REVIEW. |

### context_inheritance_and_right_hand_string

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-INHERIT-TIAO-4` | 挑四弦（空上部时可承前） | must_have | COMP-018 挑 must not be dropped or read as a bare string number.; Do not hardcode the inherited left-hand/hui value; resolve it from the nearest explicit prior context and mark context_inherited=true. |
| `TEMPLATE-GOU-4` | 勾四弦（空上部时可承前） | must_have | Do not output 裸勾 or 勾？ when 四 is visibly embedded/lower/nearby and construction supports right-hand string reading.; Do not make 承前 inherent to all 勾四 cases; only mark context_inherited when upper left-hand/hui slots are blank and a prior context exists. |

### layered_open_string_construction

| template_id | reading_pattern | priority | guardrail summary |
| --- | --- | --- | --- |
| `TEMPLATE-TI-4-SAN-3-RUYI` | 剔四弦，散三如一 | must_have | COMP-037 剔 plus 四 must be read as 剔四弦 when construction supports it.; Do not merge final 句号 into a sounding unit. |
| `TEMPLATE-SAN-3-RUYI` | 散三如一 | must_have | Read from top to bottom as 散音 layer, 三弦 layer, 如一声 layer.; Do not directly expand 如一声 into final Dapu IR at this stage. |

## Boundary

- Reusing a template must record the `template_id`.
- Reusing a template remains `NEEDS_HUMAN_REVIEW`.
- `承前` must resolve from nearest explicit prior context; do not hardcode `大指七徽` or any other value unless visible/reviewed.
- Do not use jianpu, old OCR, old CSV rows, page layout, or spacing as score authority.
