# XWC Baiya E_REVIEWED Render Report

生成对象：`XWC_BAIYA_E_REVIEWED.wav`

## 权威输入

仅读取工程目录 `latest`：

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/render_revision_log.yaml`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/preferred_version_summary.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/listening_review.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/render_phrase_alignment.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/phrase_boundary_decision.csv`

未读取 Downloads、旧 zip、旧 archive 或 `r2_review_exports` 作为当前状态。

## latest 计数

- review_count: 29
- phrase_count: 10
- preferred_version_count: 10
- suggested_revision_count: 13
- issue_count: 6
- render_phrase_alignment.csv: 40 行
- phrase_boundary_decision.csv: 40 行
- duplicate phrase/version keys: 0

## 13 条 suggested_revision 进入 E

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

## 每句 E 决策

- `XWC_P01_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；前三音相对紧凑，第四音延展；不做四音均分。；takes `T001, T002, T003, T005`。
- `XWC_P02_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；前五音连贯，末音延展；不做六音均分。；takes `T006, T007, T014, T010, T011, T013`。
- `XWC_P03_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；语义展开“同第2句”：前五音连贯，末音延展。；takes `T014, T015, T016, T018, T019, T021`。
- `XWC_P04_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；语义展开“同第2句”：前五音连贯，末音延展。；takes `T022, T023, T024, T026, T027, T029`。
- `XWC_P05_LOCAL_PHRASE`：base/preferred `C_QINIST_STYLE`，E source `C_QINIST_STYLE`；语义展开“同第2句”：前五音连贯，末音延展。；takes `T030, T031, T032, T034, T035, T037`。
- `XWC_P06_LOCAL_PHRASE`：base/preferred `B_PHRASE`，E source `B_PHRASE`；语义展开“同第1句”：前三音紧凑，第四音延展。；takes `T038, T039, T041, T043`。
- `XWC_P07_LOCAL_PHRASE`：base/preferred `B_PHRASE`，E source `B_PHRASE`；语义展开“同第1句”：前三音紧凑，第四音延展。；takes `T044, T045, T047, T049`。
- `XWC_P08_LOCAL_PHRASE`：base/preferred `B_PHRASE`，E source `B_PHRASE`；语义展开“同第1句”：前三音紧凑，第四音延展。；takes `T050, T052, T054, T056`。
- `XWC_P09_LOCAL_PHRASE`：base/preferred `A_LITERAL`，E source `A_LITERAL`；context_take_overused 强修复：只用 A_LITERAL 的当前谱面事件，避免整段 context take。；takes `T057, T059, T061, T062`。
- `XWC_P10_LOCAL_PHRASE`：base/preferred `A_LITERAL`，E source `A_LITERAL`；第一音延展，2/3/4 紧凑成组，5/6/7 分别拉开；good 作为正向偏好。；takes `T064, T065, T066, T067, T068, T069, T070`。

## P09 硬约束验证

- 是否使用 context take：否。
- 是否裁掉上下文音：未使用 T060/T071 整段 context take，因此无需裁切；E 使用 A_LITERAL 的 T057/T059/T061/T062。
- 是否避免两个上下文音：是，未把 context take 中的上下文音与当前谱面上下文重复拼入。
- 采用 source version/sample：`A_LITERAL`；`T057`, `T059`, `T061`, `T062`。

## P10 正向偏好验证

- 第一音是否延展：是。
- 2/3/4 是否成组：是。
- 5/6/7 是否分别放慢：是。
- `issue_type=good` 是否作为正向偏好处理：是。

## 音频元数据

- duration_s: 123.489592
- sample_rate_hz: 44100
- sample_width_bytes: 3（24-bit PCM）
- channels: 2
- 与 ABCD 采样率/位深/声道一致：true

## 安全边界

- e_generated=true 仅记录在 E_REVIEWED 输出验证/报告中，不反写 latest draft。
- experimental_render=true
- production_grade=false
- experimental_only=true
- 未修改 A/B/C/D 原 wav/alignment。
- 未写 `03_samples/sample_assets.csv`、`03_samples/recording_segments.csv` 或 `recording_items_enriched.jsonl`。
- 未修改 R2 页面、Downloads、R2 导出逻辑、raw master、R0/R1 archive、score/canon/source。


## T008 安全修复审计

- 审计结论：原 E_REVIEWED 使用了 `T008`，位置为 `XWC_P02_N03`；`T008` 标注目标为“散挑六”，实际误弹为“散挑七”，因此不能继续作为 E 听评音频来源。
- 原始 E 归档：`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED_ORIGINAL_BEFORE_T008_FIX`。
- 当前 E 修复：`XWC_P02_N03` 已替换为 `T014`，来源为白牙 `batch02` exact `SAN_TIAO_6` / “散挑六”，未使用“散挑七”冒充。
- 替代优先级：a. 白牙其它 exact “散 + 挑 + 六弦”。
- 当前 E T008-safe：`true`；alignment flags 写入 `t008_excluded=true`、`t008_safe_replacement=T014`、`replacement_priority=exact_baiya_san_tiao_6`。
- E wav hash：before `2e5b2b545e0b54e3d5a937a6e7bef45f4b20ad2d7dc2882a7dde1280f0bd3d6c`；after `2b0e4271928e4af71c57df2f70efb8300f42caf9e93797cdfbb6868b2fce752a`。
