# QXBY Component Registry v0.1
Task id: `CG-QXBY-COMPONENT-ATLAS-REFERENCE-AND-LXY-P5-VALIDATION-v0.1`
Status labels: `QXBY_COMPONENT_ATLAS_REFERENCE`, `USER_REVIEWED_COMPONENT_LABELS`, `SOURCE_REFERENCE_KNOWLEDGE`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.
This registry is layer 1 of the component-guided transcription stack. It records atomic component labels `COMP-001..037`, categories, visual slot semantics, and links to template ids. It is not final phrase score authority and must not be treated as Dapu IR authority.
Layer 2 template definitions now live in `references/qxby_component_atlas/construction_templates.v0.1.json`; layer 3 regression fixtures live under `tests/fixtures/cyber_guqin/component_guided_transcription/`.
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
| `COMP-031` | 抹挑 | 右手指法 | v0.5 | yes |
| `COMP-032` | 如一声 | 两弦双弹 | v0.5 | yes |
| `COMP-033` | 绰 | 左手取音 | v0.5 | yes |
| `COMP-034` | 双吟 | 左手取音 | v0.5 | yes |
| `COMP-035` | 落指猱 | 左手取音 | v0.5 | yes |
| `COMP-036` | 掩 | 左手指法 | v0.5 | yes |
| `COMP-037` | 剔 | 右手指法 | v0.5 | yes |

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

## v0.5 Additions

Registered mappings:

- `COMP-031 = 抹挑 / 右手指法`
- `COMP-032 = 如一声 / 两弦双弹`
- `COMP-033 = 绰 / 左手取音`
- `COMP-034 = 双吟 / 左手取音`
- `COMP-035 = 落指猱 / 左手取音`
- `COMP-036 = 掩 / 左手指法`
- `COMP-037 = 剔 / 右手指法`

`COMP-037` is recorded from the user-provided single component image `/Users/chenyulin/Desktop/截屏2026-06-29 22.51.49.png`; the binary image is not copied into the repo.

## Linked Construction Templates

Template definitions are externalized in `construction_templates.v0.1.json` with `42` reusable report-only templates. Component records may reference template ids, but the registry itself remains the atomic component layer.

Every template has `not_dapu_ir_authority: true` and must remain `NEEDS_HUMAN_REVIEW` when reused in a new phrase crop.

## Operating Rule

For LXY P5 and later phrase work, load three layers before reading the new crop:

```text
component_registry.v0.1.json
→ construction_templates.v0.1.json
→ lxy_p1_p4_gold_cases / forbidden_outputs fixtures
→ current phrase crop
```

If a crop is missing or ambiguous, write a missing-input report instead of inventing a candidate reading.
