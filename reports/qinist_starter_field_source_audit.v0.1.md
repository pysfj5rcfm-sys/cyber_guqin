# Qinist Starter Field Source Audit v0.1

任务：`CG-QINIST-STARTER-KIT-AND-SANMAN-INSTANCE-DESIGN-v0.1`

状态：设计审计稿。不是生产契约，不是 sample ingest，不是 ML training data。

## 1. 审计结论

当前主线已由 repo `README.md`、外部 `Core_Instructions_v1.6.md` 和 handoff 共同确认：

```text
QINIST_STARTER_COLLECTION_KIT
-> first instance: QINIST_001_SANMAN
```

`QINIST_002 / Baiya` 的角色只能是 XWC accepted baseline、workflow regression case、engineering reference、comparison qinist。Baiya 数据不能替代 Sanman 指法数组或 Sanman style data。

字段审计的核心结论：

- Repo 已有正式 Dapu Event IR schema：`schemas/dapu_event_ir.schema.json`。
- Repo 也有 P1-F dry-run minimal fixture / generic recording-plan script，字段形状与正式 Dapu schema 不完全一致。
- `primary_sound_type` 在正式 Dapu schema / ontology 中是权威音型字段，只允许 `散音` / `按音` / `泛音`。
- `sound_type`、`string`、`hui_position` 已存在于 dry-run fixture/script，但 starter-kit 设计应显式映射到 `primary_sound_type`、`string_no`、`hui` / `hui_target`，不要直接冻结为最终 parser contract。
- RECD/VARW R0/R1 的身份与 provenance 字段已经较清楚：`recording_session_id`、`recording_id`、`piece_id`、`qinist_id`、`recording_take_no`、`batch_take_no`、`script_id`、`source_raw_audio`、`source_split_audio`。
- `take_id`、`source_audio`、`variant`、`anchor_type` 是兼容/显示别名，不能成为 canonical。
- R2 profile mapping 必须从现有 VARW R2 字段出发：`r2_review_state.latest.json` 中的 `listeningReviewByKey`、`preferredVersionByPhrase`、`phrase_alignments`，以及其派生 CSV/YAML。
- `candidate_id`、`starter_item_id`、`kit_id`、`prompt_manifest_id`、`profile_signal_id` 等 starter/profile/sidecar 新字段目前没有 repo 实现，必须标为 `proposed_extension_field`。

## 2. 外部文档读取情况

已读取：

- `/Users/chenyulin/Downloads/Core_Instructions_v1.6.md`
- `/Users/chenyulin/Downloads/NEXT_CHAT_HANDOFF_SANMAN_DIGITIZATION_STARTUP_v0.2.md`
- `/Users/chenyulin/Downloads/CYBER_GUQIN_PROJECT_KNOWLEDGE_IMPORT_v1.4.md`
- `/Users/chenyulin/Downloads/CYBER_GUQIN_LONG_TERM_CREATIVE_ML_ROADMAP_v1.4.md`
- `/Users/chenyulin/Downloads/Skills_Cyber_Guqin_v1.1.md`
- `/Users/chenyulin/Downloads/RECD_VARW_Cyber_Guqin_v1.1.md`
- `/Users/chenyulin/Downloads/CYBER_GUQIN_FULL_EVOLUTION_HISTORY_v1.4.md`

未找到：

- `/Users/chenyulin/Downloads/RECD&VARW · Cyber Guqin v1.0.txt`

repo 内未发现同名外部同步文件。已创建 `reports/qinist_starter_missing_inputs.v0.1.md` 记录缺失。

## 2.1 附件与 Repo 版本比较

按文件名精确比较：

- `Core_Instructions_v1.6.md`：repo 内未发现同名文件；使用 Downloads 附件作为 phase/mainline/stop rules 来源。
- `NEXT_CHAT_HANDOFF_SANMAN_DIGITIZATION_STARTUP_v0.2.md`：repo 内未发现同名文件；使用 Downloads 附件作为当前 handoff 来源。
- `CYBER_GUQIN_PROJECT_KNOWLEDGE_IMPORT_v1.4.md`：repo 内未发现同名文件；使用 Downloads 附件作为 project knowledge 来源。
- `CYBER_GUQIN_LONG_TERM_CREATIVE_ML_ROADMAP_v1.4.md`：repo 内未发现同名文件；使用 Downloads 附件作为 ML-ready sidecar / ML boundary 来源。
- `Skills_Cyber_Guqin_v1.1.md`：repo 内未发现同名文件；同时读取 repo `.agents/skills/*/SKILL.md` 作为实际可执行 skill 边界。
- `RECD_VARW_Cyber_Guqin_v1.1.md`：repo 内未发现同名文件；同时读取 `tools/cg-varw/docs/RECD_VARW_CSV_CONTRACT_SPEC_v0.1.md`、`RECD_VARW_CSV_CONTRACT_AUDIT.md`、`RECD_VARW_CSV_WRITER_PATCH_REPORT_v0.1.md` 作为本地字段契约补充。两者不冲突：附件给出项目级字段流，repo docs 给出当前 R0/R1 CSV 具体字段。
- `CYBER_GUQIN_FULL_EVOLUTION_HISTORY_v1.4.md`：repo 内未发现同名文件；使用 Downloads 附件作为历史背景与主线转折来源。
- `RECD&VARW · Cyber Guqin v1.0.txt`：Downloads 与 repo 均未找到；不推断其内容。

## 3. Repo 路径检查

重点读取/抽查：

- `README.md`
- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- `.agents/skills/guqin-canon-builder/SKILL.md`
- `.agents/skills/guqin-dapu-parser/SKILL.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- `00_global/schema_contract.yaml`
- `00_global/guqin_fingering_ontology.yaml`
- `00_global/gesture_templates.csv`
- `00_global/gesture_components.csv`
- `00_global/gesture_component_lexicon.csv`
- `00_global/gesture_family_catalog.csv`
- `00_global/sample_selection_policy.yaml`
- `00_global/alias_rules.yaml`
- `00_global/parse_rules.yaml`
- `00_global/qinist_profiles/QINIST_001_sanman.yaml`
- `06_docs/GESTURE_ONTOLOGY.md`
- `references/normalization_rules.md`
- `references/validation_rules.md`
- `references/v1_mapping.md`
- `schemas/dapu_event_ir.schema.json`
- `schemas/dapu_token.schema.json`
- `01_pieces/xianwengcao/score_events.csv`
- `01_pieces/xianwengcao/recording_script_human.csv`
- `examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl`
- `examples/cyber_guqin/xwc_recording_plan_config.yaml`
- `examples/cyber_guqin/xwc_abcd_render_manifest.yaml`
- `examples/cyber_guqin/xwc_final_render_manifest.yaml`
- `tools/cg-varw/backend/app/schemas.py`
- `tools/cg-varw/backend/app/services/csv_contract_validator.py`
- `tools/cg-varw/backend/app/services/export_context_resolver.py`
- `tools/cg-varw/backend/app/services/r0_export_writer.py`
- `tools/cg-varw/backend/app/services/r1_review_store.py`
- `tools/cg-varw/backend/app/services/r2_mock_store.py`
- `tools/cg-varw/docs/RECD_VARW_CSV_CONTRACT_SPEC_v0.1.md`
- `tools/cg-varw/docs/RECD_VARW_CSV_WRITER_PATCH_REPORT_v0.1.md`
- `reports/r0r1_export_manifest_reload_identity_guard_report.md`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/*`
- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`

没有读取真实 audio binary，没有读取 Downloads 作为 R2 authority，没有读取或运行 `scripts/generate_baiya_recording_plan.py`。

## 4. 当前字段库存摘要

### Score / Canon / Dapu

现有字段包括：

```text
event_id, work_id, piece_id, phrase_id, event_group_id,
source_token, raw_input, normalized_token, normalized_input, normalized_name,
primary_sound_type, sound_type, sound_profile, gesture_family, gesture_id,
gesture_id_candidate, technique, special_technique, components,
component_name, component_category, component_role, component_hand,
component_sound_type, string_no, string, hui, hui_position, hui_target,
motion_returns, notation_pre_action, notation_vibrato, context_dependency,
needs_context_take, requires_context_sample, needs_long_tail, needs_review,
source_status, parse_status, source_confidence, certainty, source_refs
```

重要解释：

- `primary_sound_type` 是 formal Dapu / ontology 字段。
- `sound_type` 是 P1-F dry-run fixture/script 字段，不能无审计地替代 `primary_sound_type`。
- `string` / `hui_position` 与 `string_no` / `hui` 的关系需要显式 mapping。
- 按音不能只看 `primary_sound_type=按音`；必须检查 `components`、`hui`、`hui_target`、`motion_returns`、pre/post/vibrato 字段。

### RECD / VARW R0/R1

现有字段包括：

```text
recording_session_id, session_id, recording_id, recording_take_no,
batch_id, batch_take_no, script_id, source_raw_audio, source_split_audio,
source_audio, take_id, segment_id, event_range, expected_sample_type,
realization_variant, variant, realization_pre_action, realization_vibrato,
tail_policy, pre_attack_music_policy, render_anchor_type, anchor_type,
marker_type, review_status, segment_status, human_accepted, reviewed_by,
reviewer, reviewed_at, updated_at, wrong_take
```

别名边界：

- `take_id` 只能是 UI/display alias，不能替代 `recording_take_no`。
- `source_audio` 是 stage-specific alias，R0 对应 `source_raw_audio`，R1 对应 `source_split_audio`。
- `variant` 只能兼容 `realization_variant`。
- `anchor_type` 只能兼容 `render_anchor_type`。
- `updated_at` 不能替代 `reviewed_at`。

### R2 / Profile Mapping

现有字段包括：

```text
render_set_id, version_id, active_version_id, preferred_version_id,
preferredVersionByPhrase, listeningReviewByKey, issue_type, severity,
comment, suggested_revision, start_s, end_s, phrase_play_start_s,
phrase_play_end_s, phrase_tail_end_s, breath_points_s, cadence_point_s,
phrase_end_policy, boundary_source, boundary_confidence
```

`r2_review_state.latest.json` 当前是 canonical，CSV/YAML exports 是 derived。profile signal 只能是映射层，不应创建脱离 VARW 的 R2 label system。

## 5. 字段分类摘要

完整矩阵见：

```text
reports/qinist_starter_field_source_matrix.v0.1.json
```

分类统计按设计相关字段归纳：

- `existing_code_field`：正式 schema、repo CSV/YAML/JSON、writer/tests、fixtures 中出现的字段。
- `documented_contract_field`：外部 Core/ML/RECD/VARW 文档或 repo docs 明确要求，但 repo 未必已有冻结实现的字段。
- `legacy_alias`：兼容或 UI/display alias，不能作为 canonical。
- `proposed_extension_field`：starter kit / prompt manifest / sidecar / profile mapping 必须新增的草案字段。
- `rejected_or_unsafe_field`：会触发样本入库、ML、混淆 score facts 与 qinist realization，或破坏 parser 边界的字段。

## 6. Legacy Alias List

以下字段不得成为新 schema 的 canonical：

- `take_id` -> display alias only; do not replace `recording_take_no`.
- `source_audio` -> stage-specific alias; do not replace `source_raw_audio` / `source_split_audio`.
- `variant` -> alias only; do not replace `realization_variant`.
- `anchor_type` -> alias only; do not replace `render_anchor_type`.
- `planned_unit_start_s` / `planned_clean_start_s` style fields -> older planning aliases; prefer explicit reviewed boundary fields.
- `raw_input` / `normalized_input` -> V1 score CSV equivalents; Dapu IR uses `source_token` / `normalized_token`.
- `sound_type` / `string` / `hui_position` -> existing dry-run shape; starter intake must normalize to formal Dapu/canon fields before any production freeze.

## 7. Unsafe / Rejected Field List

Rejected fields or semantics:

- `sample_id` for starter sidecar identity: unsafe because it belongs to `sample_assets.csv`.
- `sample_asset_created`: unsafe because sidecar/human acceptance must not imply sample asset creation.
- `recording_segments_write`: unsafe because this task must not write `recording_segments.csv`.
- `recording_items_enriched_jsonl`: unsafe because this task must not write `recording_items_enriched.jsonl`.
- `baiya_as_sanman_style`: rejected; Baiya cannot become Sanman style data.
- `multi_piece_parser_input`: rejected; parser remains single-piece.
- Any new R2 label enum disconnected from `listeningReviewByKey` / `preferredVersionByPhrase` / existing R2 exports.
- Any field that writes qinist realization back into score facts.

## 8. Starter Kit Field Gaps

The repo lacks frozen fields for:

- universal kit identity: `kit_id`
- starter item identity: `starter_item_id`
- priority tier: `priority_tier`
- coverage diff status: `coverage_status`
- prompt manifest identity: `prompt_manifest_id`
- prompt item identity: `prompt_id`
- concise prompt text: `prompt_text_zh`
- trigger text: `trigger_text`
- next-prompt interval: `prompt_interval_s`
- candidate sidecar identity: `candidate_id`
- sidecar exclusion detail: `exclusion_reason`
- profile signal identity/type: `profile_signal_id`, `profile_signal_type`
- evidence cross-reference array: `evidence_refs`

These are necessary because existing repo fields either belong to score facts, recording/review outputs, or production sample ingest, and none can safely carry starter/profile/sidecar semantics without mixing authorities.

## 9. Proposed Minimal Extension Fields

| Field | Why needed | Existing field insufficient | Stage owner | Artifact only? | Needs approval |
| --- | --- | --- | --- | --- | --- |
| `kit_id` | separate universal kit from Sanman instance | `piece_id` / `qinist_id` do not name kit | starter_kit | draft schema / fixture | yes |
| `starter_item_id` | identify one requested collection item | `script_id` implies a concrete plan/run | starter_kit | draft schema / fixture | yes |
| `priority_tier` | P0/P1/P2/P3/SKIP strategy | no existing priority field | starter_kit | report / draft schema | yes |
| `coverage_status` | diff output such as missing/must_record_atomic | `review_status` is VARW review state | starter_kit | report / draft schema | yes |
| `prompt_manifest_id` | identify prompt batch manifest | `batch_id` is recording/review batch | prompt_manifest | draft schema / fixture | yes |
| `prompt_id` | identify one prompt before take creation | `recording_take_no` should not exist before recording | prompt_manifest | draft schema / fixture | yes |
| `prompt_text_zh` | concise qinist-facing prompt | `human_instruction` is long recording prose | prompt_manifest | draft schema / fixture | yes |
| `trigger_text` | 发令枪 field | no current field | prompt_manifest | draft schema / fixture | yes |
| `prompt_interval_s` | next-prompt cadence | `recommended_pause_s` is old post-take pause | prompt_manifest | draft schema / fixture | yes |
| `candidate_id` | sidecar row identity | `sample_id` is sample ingest | candidate_sidecar | draft schema / fixture | yes |
| `exclusion_reason` | explicit wrong/failed/context exclusion | `reject_reason` is R1 QC-specific | candidate_sidecar | draft schema / fixture | yes |
| `profile_signal_id` | derived profile signal identity | R2 review_id is evidence, not profile row | profile_signal_extension | draft schema / fixture | yes |
| `profile_signal_type` | timing/tail/ornament/etc grouping | existing issue_type is R2 issue taxonomy | profile_signal_extension | draft schema / fixture | yes |
| `evidence_refs` | cross-stage traceability | `source_refs` is parser/canon-oriented | profile/sidecar/starter | draft schema / fixture | yes |
| `not_recording_items_enriched` | explicit hard red-line flag | no current safety flag | safety | draft schema / fixture | yes |

## 10. Unresolved Questions Requiring User Confirmation

1. Whether future implementation should normalize the P1-F dry-run Dapu fixture from `sound_type/string/hui_position` to `primary_sound_type/string_no/hui` before starter-kit execution.
2. Whether `score_event_id` should remain a sidecar alias mapped to repo `event_id`, or become a future first-class field in a sidecar-only schema.
3. Whether Sanman starter kit P0 should start from open/harmonic full coverage plus only selected pressed sounds, or require a stricter first-piece demand threshold before any pressed-sound item is promoted to P0.
4. Whether prompt manifests should use `recording_session_id` immediately, or stay session-draft-only until a real recording session is approved.
5. Whether profile signal extraction should initially be report-only, or produce a draft sidecar once enough Sanman R2 evidence exists.
