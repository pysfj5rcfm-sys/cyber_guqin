# CG-VARW R2 持久化失败修复报告 v0.1

任务名称：CG-VARW-R2_PERSISTENCE_FAILURE_FIX_AND_RESTORE_STATE

## 1. 失败原因

0147249 已经新增了工程目录 draft API 与 `r2_review_drafts/latest/`，但 R2 页面仍保留旧的 browser/local save 路径：

- `R2ProjectReviewPage.tsx` 中旧函数 `saveDraft()` 写入 `localStorage`；
- 右侧“句读听评编辑”区域的“保存 draft”按钮仍调用该旧函数；
- 底部导出区还保留“保存浏览器 draft”按钮；
- 旧函数成功后显示 `draft 已保存到浏览器；未生成 E 或 e_revision_plan。`

因此用户点击页面里的“保存 draft”时，实际命中 browser/local save，而不是 `POST /api/r2/render-sets/{render_set_id}/review-draft/save`。这就是验收失败的直接原因。

## 2. 本次修复

本次不改 R2 页面布局，只修保存路径与状态适配：

- 右侧默认“保存 draft”现在调用工程目录保存；
- 底部主按钮“保存草稿到工程目录”继续调用工程目录保存；
- browser/local 保存改名为“临时保存到浏览器”；
- browser/local 保存文案改为明确警告：后端保存未执行，仅临时保存到浏览器，刷新/换浏览器可能丢失；
- 工程目录保存成功文案包含实际 `r2_review_state.latest.json` 路径；
- 状态栏显示 draft 来源：
  - `engineering_dir_latest`
  - `restored_from_exports`
  - `browser_fallback_temp`
  - `none`

## 3. 后端保存路径

工程目录保存继续使用：

- `GET /api/r2/render-sets/{render_set_id}/review-draft/latest`
- `POST /api/r2/render-sets/{render_set_id}/review-draft/save`
- `POST /api/r2/render-sets/{render_set_id}/review-draft/restore-from-export-dir`

保存成功会写：

- `r2_review_drafts/latest/r2_review_state.latest.json`
- `r2_review_drafts/latest/r2_review_state_manifest.json`
- `r2_review_drafts/latest/` 下 8 个 CSV/YAML
- `r2_review_drafts/archive/YYYYMMDD_HHMMSS/` 备份

同一秒内多次保存时，archive 目录会追加后缀，避免覆盖旧备份。

## 4. 页面加载 latest

页面加载真实 render set 后会调用 latest API。若 `has_draft=true`，前端 adapter 会恢复：

- `listeningReviewByKey`
- `preferredVersionByPhrase`
- `boundaryStatusByKey`
- 当前 phrase / 当前 version
- comment / issue_type / severity / suggested_revision

新增 `r2ReviewDraftState.ts` 作为纯状态 adapter，并用前端脚本验证 latest state 可还原为页面状态。

## 5. 用户 8 文件恢复

已重新从用户导出的 zip 恢复 latest draft：

输入：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_exports/2026-06-20_user_review_restore_input/R2_review_export_restore_input_8files.zip`

输出：

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/archive/20260620_110916/`

恢复统计：

- `review_count = 28`
- `phrase_count = 10`
- `preferred_version_count = 10`
- `suggested_revision_count = 10`
- `warning_count = 3`

## 6. 不完整旧导出处理

恢复时发现：

- `render_phrase_alignment.csv` 只有 P10 的 4 行，未作为全曲 alignment 权威来源；
- `phrase_boundary_decision.csv` 只有 P10 的 4 行，只恢复显式 boundary status；
- `render_revision_log.yaml` 只有 P10 的 1 条，已从 `listening_review.csv` 中 10 条非空 `suggested_revision` 重新生成 revision log。

主权威仍为 `listening_review.csv` / `listening_review.yaml`。

## 7. 验证

已执行：

- backend compileall；
- backend R2 tests；
- R2 persistence tests；
- frontend `npm run typecheck`；
- frontend export payload 验证；
- frontend persistence UI / state adapter 验证；
- restore-from-export-dir 真实运行；
- latest JSON/CSV/YAML 解析验证；
- grep 确认页面成功路径不再出现旧 browser save 成功文案；
- `git diff --check`。

## 8. 禁止事项确认

本次未生成 E_REVIEWED，未生成 `e_revision_plan.yaml`，未重渲染 A/B/C/D，未训练 ML，未写：

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`

本次未修改 `score_events` / `gesture_templates` / `canon` / `sources`，未修改 raw master / R0/R1 archive。
