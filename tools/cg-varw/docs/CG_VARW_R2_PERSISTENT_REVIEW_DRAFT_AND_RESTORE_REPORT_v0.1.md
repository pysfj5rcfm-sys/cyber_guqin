# CG-VARW R2 持久化听评草稿与导出恢复报告 v0.1

任务名称：CG-VARW-R2_PERSISTENT_REVIEW_DRAFT_AND_RESTORE_FROM_EXPORTS

## 1. 原问题

R2 工作台此前主要依赖浏览器下载 8 个 CSV/YAML 文件保存听评结果。浏览器下载可以留下文件，但不会自动回写工程目录，也不会在页面刷新后恢复 `listeningReviewByKey`、preferred version、boundary status 等前端状态。

这与 R0/R1 的 draft 保存/加载习惯不一致，用户完成一轮听评后容易丢失页面状态，需要重复听评。

## 2. 持久化目录

新增工程内 R2 draft 目录：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/`

当前包含：

- `latest/`：页面自动加载与手动加载的当前 draft；
- `archive/YYYYMMDD_HHMMSS/`：每次保存/恢复的时间戳备份。

`latest/` 的主恢复文件为：

- `r2_review_state.latest.json`
- `r2_review_state_manifest.json`

并同步写出 8 个 review-only CSV/YAML 文件。

## 3. 后端 API

新增最小 R2 持久化 API：

- `GET /api/r2/render-sets/{render_set_id}/review-draft/latest`
- `POST /api/r2/render-sets/{render_set_id}/review-draft/save`
- `POST /api/r2/render-sets/{render_set_id}/review-draft/restore-from-export-dir`

这些 API 写入 `CG_VARW_R2_RENDER_ROOT` 下的 `r2_review_drafts/`，保留旧 `/reviews/draft` mock 风格接口，不影响 R0/R1。

## 4. 前端接入

R2 页面加载真实 render set 后，会自动请求 latest draft：

- 若存在，恢复 `listeningReviewByKey`、`preferredVersionByPhrase`、`boundaryStatusByKey`、当前 phrase / version；
- 若不存在，只显示“工程目录暂无 latest draft”，不阻塞真实 render set。

导出区保留浏览器下载，同时新增：

- 保存草稿到工程目录；
- 从工程目录重新加载草稿；
- 从导出文件恢复草稿。

浏览器下载仍可用，但不再是唯一保存方式。

## 5. 用户 8 文件恢复

恢复输入目录：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_exports/2026-06-20_user_review_restore_input/`

实际输入为 `R2_review_export_restore_input_8files.zip`，后端恢复逻辑已支持从该 zip 读取 8 个文件。

主来源：

- `listening_review.csv`
- `listening_review.yaml` 用于存在性/交叉校验

辅助来源：

- `preferred_version_summary.csv`
- `issue_list.csv`
- `phrase_structure_review.yaml`

谨慎来源：

- `render_phrase_alignment.csv`
- `phrase_boundary_decision.csv`
- `render_revision_log.yaml`

原因：本次用户导出的 `render_phrase_alignment.csv` 与 `phrase_boundary_decision.csv` 只有 P10 的 4 行，不能覆盖当前 R2 全曲 40 行 alignment；`render_revision_log.yaml` 只有 P10 一条，不能覆盖 listening review 中其它 suggested revision。

## 6. 恢复结果

已运行真实 restore，生成：

- `r2_review_drafts/latest/r2_review_state.latest.json`
- `r2_review_drafts/latest/r2_review_state_manifest.json`
- `r2_review_drafts/latest/` 下 8 个 CSV/YAML 文件
- `r2_review_drafts/archive/20260620_105004/` 备份

恢复统计：

- `review_count = 28`
- `phrase_count = 10`
- `preferred_version_count = 10`
- `suggested_revision_count = 10`
- `warning_count = 3`

恢复 warnings：

- `render_phrase_alignment.csv` 只有 4 行，未作为 alignment 权威来源；
- `phrase_boundary_decision.csv` 只有 4 行，只恢复其中显式 boundary status；
- `render_revision_log.yaml` 只有 1 行，已从 `listening_review.csv` 的 10 条非空 `suggested_revision` 重新生成 revision log。

## 7. 安全边界

本次未改 R2 页面布局，未重渲染 A/B/C/D，未生成 E，未生成 `e_revision_plan.yaml`，未训练 ML，未写：

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`

本次未修改 `score_events` / `gesture_templates` / `canon` / `sources`，未修改 raw master / R0/R1 archive。

所有 latest/archive 文件均保持：

- `gpt_review_pending=true`
- `e_revision_plan_generated=false`
- `e_generated=false`
- `experimental_render=true`
- `production_grade=false`

## 8. 验证

已验证：

- 后端 compileall；
- R2 intake tests；
- R2 draft persistence tests；
- 前端 `npm run typecheck`；
- 前端 export payload 验证；
- latest draft JSON/CSV/YAML 解析；
- latest draft 可由后端 loader 读取。

## 9. 用户继续听评方式

1. 启动后端并设置 `CG_VARW_R2_RENDER_ROOT` / `CG_VARW_R2_INTAKE_ROOT`；
2. 启动前端 R2 页面；
3. 页面加载真实 render set 后会自动尝试读取 `r2_review_drafts/latest/r2_review_state.latest.json`；
4. 若需要手动操作，可在底部“导出与评审历史”中使用：
   - 保存草稿到工程目录；
   - 从工程目录重新加载草稿；
   - 从导出文件恢复草稿。
