# QXBY Component Registry v0.1

Task id: `CG-QXBY-COMPONENT-ATLAS-REFERENCE-AND-LXY-P5-VALIDATION-v0.1`

Status labels: `QXBY_COMPONENT_ATLAS_REFERENCE`, `USER_REVIEWED_COMPONENT_LABELS`, `SOURCE_REFERENCE_KNOWLEDGE`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.

This registry converts the already user-reviewed component knowledge used in LXY P1-P4 into a repo-local reference layer. It is a reference atlas for component labels, categories, visual slot semantics, and construction templates. It is not final phrase score authority and must not be treated as Dapu IR authority.

## Registered Components

| component_id | label_zh | category | source_zip | reference only |
| --- | --- | --- | --- | --- |
| `COMP-001` | 托 | 右手指法 | v0.2 | yes |
| `COMP-002` | 泛起 | 泛音起始 | v0.2 | yes |
| `COMP-003` | 少息 | 节奏谱字 | v0.2 | yes |
| `COMP-004` | 五 | 弦数 | v0.2 | yes |
| `COMP-005` | 句号 | 节奏谱字 | v0.2 | yes |
| `COMP-006` | 六 | 弦数 | v0.2 | yes |
| `COMP-007` | 七 | 弦数 | v0.2 | yes |
| `COMP-008` | 名指 | 左手指法 | v0.2 | yes |
| `COMP-009` | 一 | 弦数 | v0.2 | yes |
| `COMP-010` | 吟 | 左手指法 | v0.2 | yes |
| `COMP-011` | 四 | 弦数 | v0.2 | yes |
| `COMP-012` | 大指 | 左手指法 | v0.2 | yes |
| `COMP-013` | 中指 | 左手指法 | v0.2 | yes |
| `COMP-014` | 历 | 右手指法 | v0.2 | yes |
| `COMP-015` | 二 | 弦数 | v0.2 | yes |
| `COMP-016` | 三 | 弦数 | v0.2 | yes |
| `COMP-017` | 泛止 | 泛音停止 | v0.2 | yes |
| `COMP-018` | 挑 | 右手指法 | v0.2 | yes |
| `COMP-019` | 爪起 | 左手指法 | v0.2 | yes |
| `COMP-020` | 勾 | 右手指法 | v0.2 | yes |
| `COMP-021` | 背锁 | 右手指法 | v0.3 | yes |
| `COMP-022` | 掐起 | 左手指法 | v0.3 | yes |
| `COMP-023` | 就 | 左手承前 | v0.3 | yes |
| `COMP-024` | 进复 | 左手取音 | v0.3 | yes |
| `COMP-025` | 注 | 左手取音 | v0.3 | yes |
| `COMP-026` | 上 | 左手取音 | v0.3 | yes |
| `COMP-027` | 散音起始 | 散音起始 | v0.3 | yes |
| `COMP-028` | 撞 | 左手取音 | v0.4 | yes |
| `COMP-029` | 轮 | 右手指法 | v0.4 | yes |
| `COMP-030` | 急 | 节奏谱字 | v0.4 | yes |

All components carry:

- `component_reference: true`
- `score_event_authority: false`
- `dapu_ir_authority: false`
- `sample_ingest: false`
- `ml_training_data: false`

## v0.4 Correction

Preserved mappings:

- `COMP-028 = 撞 / 左手取音`
- `COMP-029 = 轮 / 右手指法`
- `COMP-030 = 急 / 节奏谱字`

Rejected fallback mappings:

- `raw_001=轮`
- `raw_003=撞`

## Construction Templates

The JSON registry contains 26 reusable report-only templates:

`勾一`, `勾二`, `勾三`, `托七`, `挑六`, `挑四`, `历五四`, `散音，挑五`, `大指六二徽，轮七弦`, `轮七`, `撞`, `急进复`, `进五六复`, `上六二`, `就=承前`, `泛起`, `泛止`, `少息`, `句号`, `背锁`, `大指注下七徽，抹七弦`, `大指注下七徽，挑七弦`, `名指七六徽，掐起七弦`, `名指七九徽，挑六弦`, `吟`, `爪起`.

Every template has `not_dapu_ir_authority: true` and must remain `NEEDS_HUMAN_REVIEW` when reused in a new phrase crop.

## Operating Rule

For LXY P5 and later phrase work, first load `component_registry.v0.1.json`. If a crop is missing or ambiguous, write a missing-input report instead of inventing a candidate reading.
