# CG-VARW R2 稳定化审计与修复报告 v0.1

任务：`CG-VARW-R2_STABILIZATION_AUDIT_AND_REPAIR_XWC_PHRASE_LOCK`

## 1. 本次修复范围

本次只做 R2 正式听评前稳定化：审计并修复 R2 render set 加载、生成《仙翁操》谱面句法锁定草案、恢复 R2 中文 UI、修复 Export Preview 空白问题。

本次未生成 E，未生成新 wav，未重渲染 A/B/C/D，未训练 ML，未写 `sample_assets.csv` / `recording_segments.csv` / `recording_items_enriched.jsonl`。

## 2. R2 硬编码审计

发现运行时硬编码：

- 后端 `r2_mock_store.py` 原先固定读取 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_intake/`。
- 前端 `R2ProjectReviewPage.tsx` 原先固定寻找 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`。
- README 原先把 R2 API 使用说明写成固定 render_set_id。

已修复为：

- 后端优先读取 `CG_VARW_R2_RENDER_ROOT` 与 `CG_VARW_R2_INTAKE_ROOT`。
- 未设置 env 时，后端只做仓库内通用发现：`04_outputs/*/*/abcd_experimental_render/r2_review_intake/r2_render_set_index.json`。
- 前端不再固定 render_set_id，而是调用 `/api/r2/render-sets` 后选择第一个真实 `experimental_render` render set。
- audio 播放仍通过 `/api/r2/render-sets/{render_set_id}/versions/{version_id}/audio`，不把本地绝对路径直接塞给浏览器。
- mock fallback 保留，仅在后端不可用或未返回真实 render set 时启用。

## 3. 《仙翁操》谱面句法概览

句法草案来源为 `01_pieces/xianwengcao/score_events.csv` 的 `phrase_id` / `event_role`，不是 render_event_alignment，也不是 sample_selection_decision。

当前检测到 51 个 score events，分为 10 句：

| 句序 | section_id | phrase_id | event_count |
| --- | --- | --- | --- |
| 1 | XWC_P01 | XWC_P01_LOCAL_PHRASE | 4 |
| 2 | XWC_P02 | XWC_P02_LOCAL_PHRASE | 6 |
| 3 | XWC_P03 | XWC_P03_LOCAL_PHRASE | 6 |
| 4 | XWC_P04 | XWC_P04_LOCAL_PHRASE | 6 |
| 5 | XWC_P05 | XWC_P05_LOCAL_PHRASE | 6 |
| 6 | XWC_P06 | XWC_P06_LOCAL_PHRASE | 4 |
| 7 | XWC_P07 | XWC_P07_LOCAL_PHRASE | 4 |
| 8 | XWC_P08 | XWC_P08_LOCAL_PHRASE | 4 |
| 9 | XWC_P09 | XWC_P09_LOCAL_PHRASE | 4 |
| 10 | XWC_P10 | XWC_P10_LOCAL_PHRASE | 7 |

已新增：

- `phrase_structure_lock/XWC_PHRASE_STRUCTURE_LOCK_DRAFT.csv`
- `phrase_structure_lock/XWC_PHRASE_STRUCTURE_LOCK_DRAFT.md`
- `phrase_structure_lock/XWC_PHRASE_EVENT_DETAIL_DRAFT.csv`
- `phrase_structure_lock/XWC_PHRASE_STRUCTURE_AUDIT.json`

这些文件均为 draft，不是 final / verified。

## 4. R2 seed 审计

当前 `r2_phrase_alignment_seed.csv`：

- unique phrase 数：10
- 数据行数：40
- 预期行数：10 × A/B/C/D = 40
- 每个 phrase 均有 A_LITERAL / B_PHRASE / C_QINIST_STYLE / D_TEACHING_DIAGNOSTIC 四行
- event_range 与 `score_events.csv` 的 `XWC_Pxx` 分句一致

结论：当前 seed 与谱面句法一致，因此本次未生成 `r2_phrase_alignment_seed.from_score_phrase_lock.csv`，也未覆盖旧 seed。

## 5. R2 前端修复

R2 左侧 phrase list 现在按 unique phrase 展示：

- 第几句
- phrase_id
- event_range
- event_count
- 指法/归一名简述

选中某句后，右侧显示：

- 本句 event 明细列表
- A/B/C/D 各自 start/end
- 每版播放按钮
- A→B→C→D 顺序播放

前端仍按每个版本自己的 `phrase_start_s` / `phrase_end_s` 播放，不按同一绝对时间点切换版本。

## 6. 中文 UI 恢复

已把 R2 固定界面文案恢复为中文，包括：

- 当前曲目、当前乐句、第几句、事件范围、事件数
- 版本、开始、结束、播放、停止、顺序播放 A→B→C→D
- 问题类型、严重程度、偏好版本、评论、修订建议
- 导出预览、导出听评草稿 JSON
- E 未生成、实验渲染、非生产级、模拟数据兜底

保留英文仅限 `version_id`、JSON key、enum、文件路径与 API path。

## 7. Export Preview 修复

原问题：页面底部只显示 render set / versions / API 摘要，没有始终渲染正式导出 payload；当没有填评论或某些字段为空时，用户看到的 Export Preview 可能为空白或无法确认导出内容。

修复方式：

- 新增统一的 `buildDraftExportPayload(...)`。
- Export Preview 始终显示 JSON skeleton。
- 未填写任何评论时也显示 `reviews: []` 与 `draft_count: 0`。
- 只填写 comment 或 suggested_revision 也会保留 review，不要求 issue_type 非空。
- preferred_version 未设置时导出为 `null`。
- 下载的 JSON 与页面 Export Preview 使用同一个 payload。

本轮不会生成最终 `listening_review.yaml`，也不会生成 `e_revision_plan.yaml`。

## 8. 禁写路径

本次未修改：

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`
- `score_events`
- `gesture_templates`
- `canon`
- `sources`
- raw master
- R0/R1 archive

`scripts/generate_baiya_recording_plan.py` 仍为既有未跟踪文件，不纳入本次提交。

## 9. 后续验收方式

1. 设置 `CG_VARW_R2_RENDER_ROOT` 与 `CG_VARW_R2_INTAKE_ROOT`，启动后端。
2. 打开 R2 页面，确认页面显示真实 render_set_id、`experimental_render=true`、`production_grade=false`、`e_generated=false`。
3. 左侧应显示 10 个谱面句，而不是 40 个 version-row，也不是 51 个 event。
4. 选中任一句，确认右侧显示本句 event 明细与 A/B/C/D 各自 start/end。
5. 播放单版与顺序播放 A→B→C→D，确认使用各版本自己的 phrase_start / phrase_end。
6. 不填写任何草稿时，Export Preview 仍显示 skeleton。
7. 填写 comment-only 草稿后，Export Preview 与导出的 JSON 应同步更新。
8. 进入后续 Human+GPT co-review 前，仍不得自动生成 E。
