# CG-VARW R2 前端工作台恢复报告 v0.1

任务名称：CG-VARW-R2_RESTORE_FRONTEND_FROM_4A26CB5_REAL_API_ONLY

## 1. 恢复范围

本次以 `4a26cb5 fix(cg-varw): polish final R0 R1 R2 review UI` 中的 R2 中文听评工作台为 UI source of truth，恢复 `R2ProjectReviewPage.tsx` 的工作台式结构，而不是继续使用轻量 API 调试页。

已恢复的核心结构包括：

- 左侧项目 / session / section / phrase 列表；
- 中央 R2 句读听评工作区；
- A/B/C/D 版本切换播放器；
- `AudioCanvas` 波形 / marker 区；
- 播放 / 暂停、从句头播放、从当前标记播放、前滚播放、循环当前 phrase、A/B 对比播放、A→B→C→D 顺播；
- 右侧 marker 选择 / 微调、section 上下文、边界状态、当前版本听评批注；
- 底部“导出与评审历史”工作区。

## 2. 真实 API 接入方式

旧工作台结构现在优先读取当前 R2 真实 API：

- `GET /api/r2/render-sets`
- `GET /api/r2/render-sets/{render_set_id}/versions`
- `GET /api/r2/render-sets/{render_set_id}/phrases`
- `GET /api/r2/render-sets/{render_set_id}/phrase-alignments`
- `GET /api/r2/render-sets/{render_set_id}/versions/{version_id}/audio`

前端通过 `cgVarwApi.ts` 读取 `VITE_CG_VARW_API_BASE`，未设置时默认使用 `http://127.0.0.1:8788`。页面不硬编码 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`、`XWC`、`354811e` 或本地绝对路径，而是选择后端返回的真实 experimental render set。

后端不可用或未返回真实 render set 时，保留 4a26cb5 工作台的模拟数据兜底。

## 3. 后端能力保留

本次未修改后端。当前前端仍依赖并保留下列能力：

- env-driven loader：`CG_VARW_R2_RENDER_ROOT` / `CG_VARW_R2_INTAKE_ROOT`；
- R2 audio endpoint；
- `phrase_structure_lock`；
- `r2_phrase_alignment_seed.playback_safe.csv`；
- `r2_phrase_playback_boundary_validation.json`；
- `phrase_play_start_s` / `phrase_play_end_s` / `phrase_tail_end_s` / `next_phrase_first_attack_s`。

## 4. E 禁用

页面只显示与播放 A/B/C/D：

- `A_LITERAL`
- `B_PHRASE`
- `C_QINIST_STYLE`
- `D_TEACHING_DIAGNOSTIC`

`E_REVIEWED` 不显示为可用版本，不参与播放，不参与导出，不生成音频，也不生成 `e_revision_plan.yaml`。

## 5. Playback-safe 边界

恢复旧版播放器结构时，默认 phrase 播放边界改为优先使用：

- `phrase_play_start_s`
- `phrase_play_end_s`

`phrase_tail_end_s` 只作为尾音参考显示，不作为默认 phrase 播放终点。`next_phrase_first_attack_s` 保留为越界校验参考。A→B→C→D 顺序播放同样使用每个版本自己的 playback-safe 起止点，不按同一绝对时间点切换。

## 6. 导出区恢复

底部导出区恢复旧版 CSV/YAML 工作台式体验，并把 mock payload 替换为当前真实 render set / phrase / review state。

当前浏览器下载支持：

- `render_phrase_alignment.csv`
- `listening_review.csv`
- `preferred_version_summary.csv`
- `issue_list.csv`
- `phrase_boundary_decision.csv`
- `listening_review.yaml`
- `render_revision_log.yaml`

导出内容标记为 draft / review-only：

- `review_status: draft`
- `gpt_review_pending: true`
- `e_revision_plan_generated: false`
- `e_generated: false`
- `experimental_render: true`
- `production_grade: false`

comment-only / suggested_revision-only 草稿保留在 draft state 中，不会因为 issue_type 为空而被丢弃。

## 7. 禁写与禁止事项

本次未重渲染 A/B/C/D，未生成 E，未生成 `e_revision_plan.yaml`，未进入 ML，未写：

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`

本次未修改 `score_events` / `gesture_templates` / `canon` / `sources`，未修改 raw master / R0/R1 archive。

## 8. 验收方式

启动后端并设置 R2 root 后，进入前端 R2 页面：

1. 确认页面显示中文 R2 工作台，而不是 API 调试页；
2. 确认状态栏显示真实 API render set 已加载；
3. 确认左侧按 phrase 展示；
4. 确认 A/B/C/D 可播放，且不显示可用 E；
5. 确认当前 phrase 播放范围显示“尾音参考”，默认播放不使用尾音参考作为终点；
6. 在听评区填写 comment-only 或 suggested_revision-only 草稿后，确认底部导出预览和下载内容保留该草稿；
7. 确认导出文件均为 draft / review-only，不生成 E 或 production artifact。
