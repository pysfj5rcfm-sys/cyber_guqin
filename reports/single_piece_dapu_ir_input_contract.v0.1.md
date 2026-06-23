# Single-Piece Dapu IR Input Contract v0.1

状态：设计稿。不是生产 schema，不改变 `guqin-dapu-parser`。

## 1. 目的

本文件定义 starter-kit workflow 如何消费“单曲解析输出”。关键边界：

```text
guqin-dapu-parser remains single-piece.
starter-kit may consume many single-piece outputs later.
aggregation belongs to workflow / coverage diff layer.
```

## 2. 当前可用输入来源

Repo 已有三类可用输入：

1. Formal Dapu Event IR schema：
   - `schemas/dapu_event_ir.schema.json`
   - `schemas/dapu_token.schema.json`
2. V1 score/event equivalent：
   - `01_pieces/xianwengcao/score_events.csv`
   - `00_global/gesture_templates.csv`
   - `00_global/gesture_components.csv`
3. P1-F dry-run fixture / recording-plan shape：
   - `examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl`
   - `scripts/generate_recording_plan_from_dapu_ir.py`

设计取舍：starter-kit input contract 优先采用 formal Dapu IR / ontology 字段；P1-F dry-run fixture 可作为当前工具形状参考，但必须通过 adapter 显式映射。

## 3. 单曲输入最小结构

每条 event item 应包含：

| Concept | Preferred field | Matrix status | Notes |
| --- | --- | --- | --- |
| work/piece identity | `work_id` or mapped `piece_id` | `existing_code_field` | `piece_id` exists in V1; Dapu schema uses `work_id`. |
| event identity | `event_id` | `existing_code_field` | Do not use recording task as score authority. |
| phrase grouping | `phrase_id` if available | `existing_code_field` | Existing V1/R2 anchor. |
| event group | `event_group_id` | `existing_code_field` | Formal Dapu schema. |
| source notation | `source_token` | `existing_code_field` | V1 alias: `raw_input`. |
| normalized notation | `normalized_token` | `existing_code_field` | V1 alias: `normalized_input`. |
| sound type | `primary_sound_type` | `existing_code_field` | Only `散音` / `按音` / `泛音`. |
| gesture family | `gesture_family` | `existing_code_field` | Must align with `00_global/gesture_family_catalog.csv`. |
| sound profile | `sound_profile` | `existing_code_field` | Required for complex pressed-sound validation. |
| components | `components` | `existing_code_field` | Required for pressed/post-motion logic. |
| score pre-action | `notation_pre_action` | `existing_code_field` | Score-marked only. |
| score vibrato | `notation_vibrato` | `existing_code_field` | Score-marked only. |
| context dependency | `context_dependency` | `existing_code_field` | Drives context-take demand. |
| confidence | `certainty` | `existing_code_field` | Dry-run alias: `source_confidence`. |
| review gate | `needs_review` / `source_status` | `existing_code_field` | OCR candidates and uncertain inheritance must stay review-blocked. |

## 4. Adapter From Current Dry-Run Fixture

Current P1-F fixture fields include:

```text
sound_type, string, hui_position, technique, special_technique,
needs_context_take, needs_long_tail, source_confidence
```

Adapter mapping:

| Fixture field | Target concept | Decision |
| --- | --- | --- |
| `sound_type` | `primary_sound_type` | Normalize before any future schema freeze. |
| `string` | component `string_no` | Keep original value as evidence if needed. |
| `hui_position` | component `hui` / `hui_target` | Pressed motion may need both. |
| `technique` | `component_name` or human prompt term | Do not replace components. |
| `special_technique` | separate special/diagnostic tag | Do not create fourth sound type. |
| `needs_context_take` | workflow demand flag | Do not make context take atomic sample. |
| `needs_long_tail` | starter tail demand | Map to `tail_policy=full_tail` planning. |
| `source_confidence` | `certainty` | Keep review threshold explicit. |

## 5. Missing For Sanman Instance

No current formal `QINIST_001_SANMAN` starter Dapu IR exists. The mock fixture created in this task is shape-only and not real Sanman data.

Implementation blocker before any real run:

```text
MISSING_INPUT
QINIST_001 Sanman single-piece Dapu IR input
REQUIRED_BEFORE_IMPLEMENTATION
```

## 6. Safety Rules

- Do not treat `recording_script_human.csv` or `recording_batches.md` as score authority.
- Do not write qinist realization into `score_events.csv` or Dapu `events`.
- Do not introduce multi-piece parser input.
- Do not write `recording_items_enriched.jsonl`.
- Do not write `sample_assets.csv` or `recording_segments.csv`.

