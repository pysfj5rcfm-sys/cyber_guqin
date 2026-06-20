# CG-VARW R2 E_REVIEWED 生成报告 v0.1

任务：`CG-VARW-R2_GENERATE_XWC_E_REVIEWED_FROM_CANONICAL_LATEST`

## 权威输入路径

本次只读取工程目录 latest：

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/render_revision_log.yaml`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/preferred_version_summary.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/listening_review.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/render_phrase_alignment.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/phrase_boundary_decision.csv`

未读取 Downloads、`r2_review_exports`、旧 zip 或旧 archive 作为当前状态。

## latest review 计数

- `review_count = 29`
- `phrase_count = 10`
- `preferred_version_count = 10`
- `suggested_revision_count = 13`
- `issue_count = 6`
- `render_phrase_alignment.csv = 40 行`
- `phrase_boundary_decision.csv = 40 行`
- duplicate phrase/version keys = 0

## 13 条 suggested_revision 如何进入 E

- `XWC_P01_LOCAL_PHRASE` `C_QINIST_STYLE` -> `C_QINIST_STYLE`：123——4——
- `XWC_P02_LOCAL_PHRASE` `C_QINIST_STYLE` -> `C_QINIST_STYLE`：12345——6——
- `XWC_P03_LOCAL_PHRASE` `C_QINIST_STYLE` -> `C_QINIST_STYLE`：同第2句
- `XWC_P04_LOCAL_PHRASE` `C_QINIST_STYLE` -> `C_QINIST_STYLE`：同第2句
- `XWC_P05_LOCAL_PHRASE` `C_QINIST_STYLE` -> `C_QINIST_STYLE`：同第2句
- `XWC_P06_LOCAL_PHRASE` `B_PHRASE` -> `B_PHRASE`：同第1句
- `XWC_P06_LOCAL_PHRASE` `C_QINIST_STYLE` -> `B_PHRASE`：同第1句
- `XWC_P07_LOCAL_PHRASE` `C_QINIST_STYLE` -> `B_PHRASE`：同第1句
- `XWC_P07_LOCAL_PHRASE` `B_PHRASE` -> `B_PHRASE`：同第1句
- `XWC_P08_LOCAL_PHRASE` `C_QINIST_STYLE` -> `B_PHRASE`：同第1句
- `XWC_P08_LOCAL_PHRASE` `B_PHRASE` -> `B_PHRASE`：同第1句
- `XWC_P09_LOCAL_PHRASE` `D_TEACHING_DIAGNOSTIC` -> `A_LITERAL`：把带上下文的掐起和上下文连接，这样不是就有2个上下文的音了？
- `XWC_P10_LOCAL_PHRASE` `A_LITERAL` -> `A_LITERAL`：1——234——5——6——7——

## 每句 base version 与 GPT 共评决策

- `XWC_P01_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；前三音相对紧凑，第四音延展；不做四音均分。；takes `T001, T002, T003, T005`。
- `XWC_P02_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；前五音连贯，末音延展；不做六音均分。；takes `T006, T007, T008, T010, T011, T013`。
- `XWC_P03_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；语义展开“同第2句”：前五音连贯，末音延展。；takes `T014, T015, T016, T018, T019, T021`。
- `XWC_P04_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；语义展开“同第2句”：前五音连贯，末音延展。；takes `T022, T023, T024, T026, T027, T029`。
- `XWC_P05_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；语义展开“同第2句”：前五音连贯，末音延展。；takes `T030, T031, T032, T034, T035, T037`。
- `XWC_P06_LOCAL_PHRASE`：base/preferred `B_PHRASE`，E source `B_PHRASE`；语义展开“同第1句”：前三音紧凑，第四音延展。；takes `T038, T039, T041, T043`。
- `XWC_P07_LOCAL_PHRASE`：base/preferred `B_PHRASE`，E source `B_PHRASE`；语义展开“同第1句”：前三音紧凑，第四音延展。；takes `T044, T045, T047, T049`。
- `XWC_P08_LOCAL_PHRASE`：base/preferred `B_PHRASE`，E source `B_PHRASE`；语义展开“同第1句”：前三音紧凑，第四音延展。；takes `T050, T052, T054, T056`。
- `XWC_P09_LOCAL_PHRASE`：base/preferred `A_LITERAL`，E source `A_LITERAL`；context_take_overused 强修复：只用 A_LITERAL 的当前谱面事件，避免整段 context take。；takes `T057, T059, T061, T062`。
- `XWC_P10_LOCAL_PHRASE`：base/preferred `A_LITERAL`，E source `A_LITERAL`；第一音延展，2/3/4 紧凑成组，5/6/7 分别拉开；good 作为正向偏好。；takes `T064, T065, T066, T067, T068, T069, T070`。

## P01/P02/P09/P10 特殊处理

- P01：保留用户 `123——4——`，前三音相对紧凑，第四音延展，不做四音均分。
- P02：保留用户 `12345——6——`，前五音相对连贯，末音延展，不做六音均分。
- P09：按 `context_take_overused` 强修复；E 使用 `A_LITERAL` 的 `T057/T059/T061/T062`，未直接使用 `T060/T071` 整段 context take，避免两个上下文音。
- P10：按用户最新 `A_LITERAL` 正向偏好 `1——234——5——6——7——`；第一音延展，2/3/4 成组，5/6/7 分别拉开；`good` 不是负面问题。

## 输出结果

- 已生成 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED/e_revision_plan.yaml`
- 已生成 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED/XWC_BAIYA_E_REVIEWED.wav`
- 已生成 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED/render_event_alignment.E_REVIEWED.csv`
- 已生成 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED/e_reviewed_render_report.md`
- 已生成 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED/e_reviewed_validation.json`

## E wav 元数据

- 时长：123.489592 秒
- 采样率：44100 Hz
- 位深：24-bit PCM (`sample_width_bytes = 3`)
- 声道：2
- 与 ABCD 采样率/位深/声道一致：true

## 边界确认

- `e_generated=true` 仅记录在 E_REVIEWED 输出验证/报告中，未反写 latest draft。
- E 是 `experimental_only`，`experimental_render=true`，`production_grade=false`。
- A/B/C/D 原 wav 与 alignment hash 生成前后一致，未重渲染 A/B/C/D。
- 未写 `03_samples/sample_assets.csv`。
- 未写 `03_samples/recording_segments.csv`。
- 未创建 `recording_items_enriched.jsonl`。
- 未修改 R2 前端、R2 导出逻辑、Downloads 逻辑或底部按钮。
- 未修改 raw master、R0/R1 archive、score_events、gesture_templates、canon 或 sources。
- 未训练 ML，未 ingest 到 sample library。

## 用户下一步如何在 R2 中听 E

当前任务按边界只生成 E 输出文件，不修改 R2 页面、不启用 E_REVIEWED 版本按钮。下一步若要在 R2 中听 E，可以在后续独立任务中只读接入 `E_REVIEWED/XWC_BAIYA_E_REVIEWED.wav` 和 `render_event_alignment.E_REVIEWED.csv`；本轮未做该 UI/Downloads 改动。
