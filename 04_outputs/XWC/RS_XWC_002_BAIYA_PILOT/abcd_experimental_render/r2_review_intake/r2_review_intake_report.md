# CG-VARW-R2 《仙翁操》ABCD Render Set Intake Report

任务名称：`CG-VARW-R2_XWC_ABCD_RENDER_SET_INTAKE`

## 1. 任务边界

本任务是 R2 听评接入准备，不是正式听评。当前只建立 ABCD experimental render set 的索引与 phrase-aligned seed，不生成 E，不修改 ABCD wav，不进入 ML，也不写 `sample_assets.csv`、`recording_segments.csv` 或 `recording_items_enriched.jsonl`。

## 2. ABCD render set 识别结果

已识别 source commit：`354811e`。

已识别四版：

- `A_LITERAL`
- `B_PHRASE`
- `C_QINIST_STYLE`
- `D_TEACHING_DIAGNOSTIC`

四个 wav 和四个 `render_event_alignment.<VERSION>.csv` 均已找到。`abcd_render_manifest.csv`、`sample_selection_decision.csv`、`abcd_render_validation.json`、`listening_review_input_guide.md` 与 planning 文件也已纳入 `r2_render_set_index.json`。

## 3. phrase-aligned 逻辑

`r2_phrase_alignment_seed.csv` 从每版自己的 `render_event_alignment` 推导 phrase 范围：同一 `phrase_id` 下取该版本 alignment rows 的最小 `segment_start_s_in_render` 与最大 `segment_end_s_in_render`。因此每个 phrase 在 A/B/C/D 中保留各自版本的 start/end。

当前 seed 行数：`40`，即 `10` 个 local phrase × `4` 个版本。

## 4. 为什么不能按绝对时间点切换版本

A/B/C/D 的 tempo、phrase pause、context take 与 tail 策略不同。同一 phrase 在四版中的实际 start/end 不必相同，也不应被强行压到一个绝对时间窗口。R2 后续应按 `phrase_id + version_id` 找到该版本自己的 phrase range，再播放或比较；这就是 phrase-aligned review，而不是 absolute-time switching。

## 5. 后续用户如何在 R2 中听

后续用户应先选择 `render_set_id=R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`，再按 phrase 切换 A/B/C/D。每次比较时使用 `r2_phrase_alignment_seed.csv` 中该 phrase 在各版本的独立 `phrase_start_s` / `phrase_end_s`。本任务预留 `issue_type`、`severity`、`comment`、`preferred_version` 字段，但不填写正式听评结论。

## 6. GPT 后续如何参与共评

GPT 后续应结合：四版 wav、每版 alignment、`sample_selection_decision.csv`、phrase alignment seed 与用户听评记录，进行结构分析、工程诊断、打谱解释诊断和样本选择诊断。后续输出可包括 `phrase_structure_review.yaml`、`render_phrase_alignment.csv`、`phrase_boundary_decision.csv`、`listening_review.yaml`、`preferred_version_summary.csv`、`issue_list.csv` 与 `e_revision_plan.yaml`。

## 7. E 仍未生成

E_REVIEWED 仍未生成。`e_revision_plan.yaml` 后续必须来自：ABCD render → 用户听评 → GPT 听评 / 结构分析 / 工程诊断 / 打谱解释诊断 → Human+GPT co-review → E_REVIEWED render。

## 8. 禁写路径

本任务未写 `03_samples/sample_assets.csv`，未写 `03_samples/recording_segments.csv`，未创建 `recording_items_enriched.jsonl`，未训练 ML，未修改 score/canon/sources/raw/R0/R1 archive。

## 9. CG-VARW-R2 现有能力与后续最小补丁

现有 CG-VARW-R2 已有 Project Review mock 页面、A/B/C/D/E 版本切换、phrase alignment mock、review draft/export mock。当前不足是后端默认返回 mock render set，前端仍静态导入 mock 数据。本轮 intake 文件为真实 ABCD set 提供索引；本轮已完成最小后端接入：后端 R2 API 会优先读取 `r2_render_set_index.json` 和 `r2_phrase_alignment_seed.csv`，返回真实 A/B/C/D，不返回 E。前端页面仍静态使用 mock 数据，真实 API 数据加载可作为后续最小 UI 接线项。
