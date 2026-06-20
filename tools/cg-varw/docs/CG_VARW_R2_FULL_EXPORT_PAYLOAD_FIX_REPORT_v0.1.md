# CG-VARW R2 全曲导出 Payload 修复报告 v0.1

任务名称：CG-VARW-R2_FIX_FULL_EXPORT_PAYLOAD_ONLY

## 1. 原问题

R2 页面工作台已经恢复，但部分导出 payload 仍沿用了“当前选中 phrase”的局部语义：

- `render_phrase_alignment.csv` 只导出当前 phrase 的 A/B/C/D 4 行；
- `phrase_boundary_decision.csv` 只导出当前 phrase 的 A/B/C/D 4 行；
- `render_revision_log.yaml` 只导出当前 phrase / 当前 review 的一条修订记录。

这会导致“导出全部”时看似导出了 8 个文件，但 alignment / boundary / revision 三类文件不能代表全曲听评状态。

## 2. 本次修复方式

本次未改页面布局，未改后端，只把 R2 导出 payload builder 抽成纯函数：

- `src/utils/r2ExportPayload.ts`
- `buildRenderPhraseAlignmentCsv`
- `buildPhraseBoundaryDecisionCsv`
- `buildRenderRevisionLogYaml`
- `buildR2PreviewTables`

`R2ExportPreviewPanel` 仍保持旧工作台导出区结构，只调用新的纯 builder。

## 3. render_phrase_alignment.csv

修复后，`render_phrase_alignment.csv` 使用页面已加载的全部 `alignments`，不再按 `activePhraseId` 过滤。

对当前真实《仙翁操》R2 render set，预期为：

- 10 个 phrase；
- A/B/C/D 4 个版本；
- 共 40 行数据行。

保留字段包括 `phrase_play_start_s`、`phrase_play_end_s`、`phrase_tail_end_s`、`next_phrase_first_attack_s`、`phrase_end_policy` 等 playback-safe 字段；`phrase_tail_end_s` 仍只是尾音参考，不作为默认播放终点。

## 4. phrase_boundary_decision.csv

修复后，`phrase_boundary_decision.csv` 同样使用全部 `alignments`，不再只导出当前 phrase。

对当前真实 render set，预期为 40 行数据行。`breath_points_s`、`cadence_point_s` 沿用 alignment 中的现有数据，但作用范围扩大到全部 phrase/version。

## 5. render_revision_log.yaml

修复后，`render_revision_log.yaml` 从全部 review drafts 生成：

- 遍历所有 `listeningReviewByKey`；
- 只有 `suggested_revision` 非空的 review draft 才进入 revision log；
- comment-only 且 `suggested_revision` 为空的 review 不进入 revision log；
- `revision_id` 使用 `R2_REVISION_{phrase_id}_{version_id}`，避免多句覆盖。

因此，如果用户全曲 10 句均填写了非空 `suggested_revision`，该 YAML 应导出 10 条 revision rows，而不是 1 条。

## 6. 保持不变的导出语义

本次没有重写以下导出语义：

- `listening_review.csv` 继续覆盖全部 review drafts；
- `listening_review.yaml` 继续覆盖全部 review drafts；
- `preferred_version_summary.csv` 继续覆盖全部 10 句；
- `issue_list.csv` 继续只导出有明确 `issue_type` 的条目；
- `phrase_structure_review.yaml` 继续覆盖全部 phrase。

所有导出仍保留 draft / review-only 安全标记：

- `gpt_review_pending=true`
- `e_revision_plan_generated=false`
- `e_generated=false`
- `experimental_render=true`
- `review_only=true`
- `production_grade=false`

## 7. 验证

新增轻量验证脚本：

`tools/cg-varw/frontend/scripts/verify-r2-export-payload.mjs`

该脚本使用 10 句 × 4 版本的 real-like 数据验证：

- `render_phrase_alignment.csv` 生成 40 行；
- `phrase_boundary_decision.csv` 生成 40 行；
- `render_revision_log.yaml` 从所有非空 `suggested_revision` 生成多条 rows；
- comment-only review 不进入 revision log；
- CSV/YAML 文本可做基本解析；
- 安全 flags 未丢失。

## 8. 禁止事项确认

本次未改 R2 页面布局，未改后端，未重渲染 A/B/C/D，未生成 E，未生成 `e_revision_plan.yaml`，未训练 ML，未写：

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`

本次未修改 `score_events` / `gesture_templates` / `canon` / `sources`，未修改 raw master / R0/R1 archive。

## 9. 用户验收方式

在 R2 工作台完成若干句听评后点击“导出全部”：

1. 打开 `render_phrase_alignment.csv`，确认数据行约为 40 行；
2. 打开 `phrase_boundary_decision.csv`，确认数据行约为 40 行；
3. 打开 `render_revision_log.yaml`，确认每条非空 `suggested_revision` 都生成一条 revision row；
4. 确认 comment-only 记录仍留在 `listening_review.csv` / `listening_review.yaml`，但不进入 revision log；
5. 确认所有文件仍标记为 draft / review-only，且未生成 E。
