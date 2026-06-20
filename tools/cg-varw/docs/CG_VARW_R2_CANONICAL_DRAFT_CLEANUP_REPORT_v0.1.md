# CG-VARW R2 Canonical Draft Cleanup Report v0.1

任务：CG-VARW-R2_CANONICAL_DRAFT_SOURCE_CLEANUP_AND_NO_DOWNLOADS
阶段：Phase 1D-XWC-ABCD Human+GPT Co-Review / R2 Canonical Draft Cleanup

## 1. 当前 R2 权威来源

当前 R2 听评状态的权威顺序已锁定为：

1. 页面当前加载 state；
2. 工程目录 `r2_review_drafts/latest/r2_review_state.latest.json`；
3. `latest/` 下由 latest state 重新生成的 8 个 CSV/YAML；
4. `r2_review_drafts/archive/YYYYMMDD_HHMMSS/` 只读备份；
5. `r2_review_exports/`、浏览器下载、zip、restore input 只作为一次性导入源，不作为当前权威。

本次实际 canonical state：

- canonical source: `r2_review_state.latest.json`
- current page load source: `engineering_dir_latest`
- latest JSON: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- latest manifest: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state_manifest.json`
- retained archive: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/archive/20260620_114355/`

## 2. 非权威来源

以下来源被明确判定为非权威：

- 浏览器下载的 8 文件：只可作为“下载副本”，不用于页面自动加载；
- `r2_review_exports/2026-06-20_user_review_restore_input/`：一次性恢复输入，恢复完成后不参与当前状态；
- `R2_review_export_restore_input_8files.zip`：一次性导入 zip，已删除且不提交；
- 旧 archive：只作为历史备份，不参与当前加载，已移入 quarantine；
- 旧 P10-only 派生文件：不得反向覆盖 latest state。

## 3. 保留与清理

保留：

- `r2_review_drafts/latest/` 下权威 latest JSON、manifest、8 个派生 CSV/YAML；
- `r2_review_drafts/archive/20260620_114355/` 作为最新有效只读备份；
- `r2_review_drafts/_quarantine/stale_sources_20260620_114426/quarantine_manifest.json` 记录清理动作。

移动到 quarantine：

- 旧 archive 目录 22 个，原因均为 `stale_archive_not_current_page_load_source`。

删除：

- `r2_review_exports/.../R2_review_export_restore_input_8files.zip`
- `r2_review_exports/.DS_Store`
- 空的 `r2_review_exports/2026-06-20_user_review_restore_input/`

## 4. latest 8 文件重新生成结果

本次不是复制旧导出文件，而是用 `r2_review_state.latest.json` 和当前 render set alignments 重新生成：

- `listening_review.csv`: 49 行
- `listening_review.yaml`: 49 行
- `preferred_version_summary.csv`: 10 行
- `issue_list.csv`: 11 行
- `phrase_structure_review.yaml`: 10 行
- `render_phrase_alignment.csv`: 40 行
- `phrase_boundary_decision.csv`: 40 行
- `render_revision_log.yaml`: 22 行

当前计数：

- `review_count=49`
- `phrase_count=10`
- `preferred_version_count=10`
- `suggested_revision_count=22`
- `issue_count=11`

## 5. 页面按钮语义

R2 页面保持原工作台布局，只调整保存/下载语义：

- 主保存：`保存草稿到工程目录`
- 重新加载：`从工程目录重新加载草稿`
- 下载：`导出全部副本` / `导出当前 phrase 副本`
- 临时 fallback：`临时保存到浏览器`

工程目录保存成功会显示 latest JSON 路径和计数；下载副本会提示“不作为工程草稿权威来源”。浏览器临时保存不会被称为正式 draft 保存成功。

## 6. 后端与 manifest

后端 `GET /api/r2/render-sets/{render_set_id}/review-draft/latest` 现在返回：

- `has_draft`
- `draft_source=engineering_dir_latest`
- `canonical_state_path`
- `review_count`
- `phrase_count`
- `preferred_version_count`
- `suggested_revision_count`
- `manifest`

`r2_review_state_manifest.json` 现在包含：

- `canonical_source`
- `canonical_state_path`
- `generated_exports_path`
- `active_render_set_id`
- `current_page_load_source`
- `stale_sources_quarantined`
- `stale_sources_deleted`
- `stale_sources_moved`
- `archive_path`
- `no_downloads_policy=true`

## 7. 刷新恢复

页面加载真实 render set 后继续调用 latest draft endpoint。若 `has_draft=true`，前端 state adapter 将 latest JSON 应用到页面 state，包括：

- active phrase / active version；
- `listeningReviewByKey`；
- `preferredVersionByPhrase`；
- `boundaryStatusByKey`；
- marker state；
- E 禁用 flags。

因此刷新页面后应从工程目录 latest 恢复，不依赖浏览器下载文件。

## 8. 禁止事项

本次未生成 E_REVIEWED，未生成 `e_revision_plan.yaml`，未重渲染 A/B/C/D，未训练 ML，未写 `03_samples/sample_assets.csv`、`03_samples/recording_segments.csv` 或 `recording_items_enriched.jsonl`，未修改 score_events / gesture_templates / canon / sources / raw master / R0/R1 archive。

## 9. 用户验收

建议验收：

1. 打开 R2 页面，确认状态栏显示工程目录 latest、latest JSON 路径和计数；
2. 点击“保存草稿到工程目录”，确认成功提示包含 `r2_review_drafts/latest/r2_review_state.latest.json`；
3. 刷新页面，确认 49 条听评状态仍可恢复；
4. 点击“导出全部副本”，确认它只是下载副本，不改变权威来源；
5. 检查 `r2_review_exports/` 下不再有 restore zip；
6. 运行 `tools/cg-varw/backend/scripts/verify_r2_canonical_draft.py`，应输出 `PASS`。
