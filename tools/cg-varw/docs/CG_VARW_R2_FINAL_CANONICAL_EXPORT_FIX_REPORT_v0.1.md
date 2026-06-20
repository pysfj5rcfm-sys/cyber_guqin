# CG-VARW R2 final canonical export fix report v0.1

任务：CG-VARW-R2_FINALIZE_CANONICAL_DRAFT_AND_PROJECT_EXPORT_ONLY

## 结论

本次将 R2 当前权威状态固定为工程目录 latest JSON：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`

latest 下的 8 个 CSV/YAML 均由该 JSON 重新派生，不再作为反向覆盖 JSON 的来源。`r2_review_exports/`、旧 zip、旧浏览器下载文件和旧 archive 只作为历史输入或只读备份，不参与页面当前加载。

## 为什么之前会反复导出到 Downloads

R2 旧工作台恢复后，底部“导出与评审历史”区域仍保留浏览器副本导出路径：前端会用 `Blob`、`URL.createObjectURL`、`link.download`、`link.click()` 触发浏览器下载。该路径和工程目录保存并存，导致用户看见多个来源：Downloads 副本、latest 派生文件、latest JSON、archive、restore input。它们没有清晰主从关系，因此出现新旧听评混合和“哪个是权威”的混淆。

本次已从 R2 页面主流程移除浏览器下载入口。R2 主流程现在只通过后端写工程目录。

## 当前保存与导出路径

保存 draft：

`POST /api/r2/render-sets/{render_set_id}/review-draft/save`

写入：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`

并同步写 latest 下 8 个派生文件与 archive 备份。

导出 CSV：

`POST /api/r2/render-sets/{render_set_id}/review-draft/export-csv`

从 canonical latest state 重新生成 latest 下 8 个 CSV/YAML，返回工程目录路径和文件清单，不返回 blob，不触发浏览器下载。

## 去重规则与结果

去重 key：

`phrase_id + active_version_id`

同一 key 只保留当前 review。优先级为：用户明确指定的新内容、较新的 `updated_at` / `saved_at` / `created_at` / `reviewed_at`、信息完整度、原始顺序。旧记录进入 `review_history_archived`，不留在 latest 当前听评表。

去重前：

- `listening_review.csv`: 50 行
- duplicate phrase/version keys: 21
- `render_revision_log.yaml`: 23 行
- `issue_list.csv`: 11 行

去重后：

- `review_count`: 29
- `phrase_count`: 10
- `preferred_version_count`: 10
- `suggested_revision_count`: 13
- `issue_count`: 6
- duplicate phrase/version keys: 0
- archived duplicate rows: 21

duplicate phrase/version 清单：

- `XWC_P01_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P02_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P03_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P04_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P05_LOCAL_PHRASE / B_PHRASE`
- `XWC_P05_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P06_LOCAL_PHRASE / A_LITERAL`
- `XWC_P06_LOCAL_PHRASE / B_PHRASE`
- `XWC_P06_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P07_LOCAL_PHRASE / A_LITERAL`
- `XWC_P07_LOCAL_PHRASE / B_PHRASE`
- `XWC_P07_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P08_LOCAL_PHRASE / A_LITERAL`
- `XWC_P08_LOCAL_PHRASE / B_PHRASE`
- `XWC_P08_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P09_LOCAL_PHRASE / A_LITERAL`
- `XWC_P09_LOCAL_PHRASE / B_PHRASE`
- `XWC_P09_LOCAL_PHRASE / C_QINIST_STYLE`
- `XWC_P09_LOCAL_PHRASE / D_TEACHING_DIAGNOSTIC`
- `XWC_P10_LOCAL_PHRASE / A_LITERAL`
- `XWC_P10_LOCAL_PHRASE / D_TEACHING_DIAGNOSTIC`

已保留用户指定的新内容：

- P01 / C_QINIST_STYLE: `试试其它节拍`，`123——4——`
- P02 / C_QINIST_STYLE: `试试其它节拍`，`12345——6——`
- P09 / B、C、D: `把带上下文的掐起和上下文连接，这样不是就有2个上下文的音了？`
- P10 / A_LITERAL: `试试其它节拍`，`1——234——5——6——7——`，`issue_type=good`

旧 P09 表述与旧 P10 D_TEACHING_DIAGNOSTIC 节拍建议已移入 history/archive，不再出现在 latest 当前 review 中。

## latest 8 文件最终行数

- `listening_review.csv`: 29 行
- `listening_review.yaml`: 29 行
- `issue_list.csv`: 6 行
- `preferred_version_summary.csv`: 10 行
- `phrase_structure_review.yaml`: 10 行
- `render_phrase_alignment.csv`: 40 行
- `phrase_boundary_decision.csv`: 40 行
- `render_revision_log.yaml`: 13 行

## 页面按钮

R2 底部“导出与评审历史”区域现在只保留两个主按钮：

- `保存 draft`
- `导出 CSV`

已移除或隐藏：

- 导出全部副本
- 导出当前 phrase 副本
- 临时保存到浏览器
- 从导出文件恢复草稿
- 从工程目录重新加载草稿
- 行级下载副本

预览表格仍保留，用于查看即将写入工程目录的派生文件内容。

## 与 R0/R1 的一致性

R0/R1 的主流程是保存 draft / 导出 CSV，并由后端写工程目录。R2 现在采用同一语义：

- 保存 draft 写 latest JSON、latest 派生文件和 archive；
- 导出 CSV 写工程目录 latest；
- 浏览器下载不再是主保存或主导出路径；
- 刷新页面后仍从工程目录 latest 加载。

## 清理状态

latest 目录仅保留 canonical JSON、manifest 和当前 8 个派生文件。`r2_review_exports/` 当前为空，不参与当前状态。清理 manifest 写入：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/_quarantine/final_canonical_cleanup_20260620_122000/cleanup_manifest.json`

旧的 pre-finalization archive `20260620_120110` 已移动到同一 quarantine 目录下，只作为历史备查，不作为当前加载来源。

archive 目录作为只读备份保留，当前最新有效 archive 为：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/archive/20260620_121933/`

## 禁止事项

本次未生成 E_REVIEWED，未生成 `e_revision_plan.yaml`，未重渲染 A/B/C/D，未训练 ML，未写 `03_samples/sample_assets.csv`、`03_samples/recording_segments.csv` 或 `recording_items_enriched.jsonl`，未修改 score_events / gesture_templates / canon / sources / raw master / R0/R1 archive。

## 用户验收方式

1. 打开 R2 页面，底部“导出与评审历史”只应看到 `保存 draft` 和 `导出 CSV` 两个主按钮。
2. 点击 `保存 draft`，页面应提示工程目录 latest JSON 路径。
3. 点击 `导出 CSV`，页面应提示 CSV 已导出到工程目录，并显示文件数量；系统 Downloads 不应新增 R2 文件。
4. 检查 latest：
   - `render_phrase_alignment.csv` 为 40 行；
   - `phrase_boundary_decision.csv` 为 40 行；
   - `listening_review.csv` 无同一 phrase/version 重复；
   - `render_revision_log.yaml` 行数等于非空 suggested_revision 数。
