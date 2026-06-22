# Engineering Tail Backlog v0.1

- Task: `CG-ENGINEERING-CLOSEOUT-MINIPATCH-v0.1`
- Current phase: `XWC_MVP_REPRODUCTION_READY__RETURN_TO_SANMAN_DIGITAL_QINIST`
- Current mainline: `QINIST_001_SANMAN_DIGITIZATION_STARTUP`
- Baseline: XWC / 《仙翁操》 / QINIST_002 白牙 / `RS_XWC_002_BAIYA_PILOT` / `F_FINAL_REVIEWED`

## 1. Executive Summary

XWC / Baiya / `F_FINAL_REVIEWED` 已作为工程基线收口。P1-F self-contained dry-run reproduction toolchain 已完成，当前 repo 可以通过 workflow skill、runbook、script registry、examples 与 generic scripts dry-run 复现 XWC F 的工程路径。

当前主线回到 `QINIST_001` 三曼数字琴人：采集协议、controlled fingering samples、ML-ready candidate sidecar，以及真实 R0/R1 数据接入前的工程护栏。本 backlog 只记录工程尾巴，不进入三曼采集实现，不做 sample ingest，不训练 ML，不执行真实 render，也不重跑 accepted F。

## 2. Closed Items

### E0 README 顶部状态修正

Status: 本轮处理。

README 顶部已从旧 `Phase 0.1 / Dummy Audio Skeleton` 当前阶段说明，更新为：

- XWC F reproduction ready / Sanman digitization startup。
- XWC / Baiya / `F_FINAL_REVIEWED` 是工程基线。
- 当前主线是 `QINIST_001` 三曼数字琴人。
- 当前不是第二首执行、sample ingest、ML training、Arrangement Mode production 或 accepted F 重跑。

### E1 P1-F commit / git status

Status: 已完成。

P1-F self-contained dry-run reproduction toolchain 已完成并提交。本轮仅保留 `scripts/generate_baiya_recording_plan.py` 警戒：该脚本仍应视为 historical template，不运行、不删除、不移动、不归档、不 stage、不误提交。

## 3. Active Engineering Tail Items

### E2/E3/E4 CG-VARW-R0R1_EXPORT_MANIFEST_RELOAD_AND_IDENTITY_GUARD

Status: 下一优先级 blocker。

合并范围：

- R0/R1 export manifest。
- reload validation。
- R0 CSV fallback manifest guard。
- R1 split root identity guard。

Reason: 这是三曼真实 R0/R1 数据接入前 blocker。真实录音进入 review 前，需要先保证 export/reload 不会丢失 manifest 身份、不会把 fallback CSV 当作无约束 authority，也不会把 R1 split root 指向错误 session/root。

### E5 legacy/mock R2 endpoints hardening

Status: 待处理。

目标是收紧 legacy/mock R2 endpoints 的默认行为和边界，防止旧端点在新主线中被误当成 production authority。该项只做 hardening，不应引入新的 R2 review 行为，也不应改写已 accepted 的 XWC/F 数据。

### E7 SANMAN_COLLECTION_COVERAGE_DIFF_ENGINE

Status: Sanman startup 前置设计项。

该项应提前作为三曼采集缺口计算器设计：从三曼采集协议、controlled fingering sample 目标、Dapu/gesture/canon 需求与已有可用候选之间做 coverage diff，输出缺口、上下文 take 风险、不可作为 atomic sample 的候选与需要人工确认的项。

### E8 render_set_id 命名债务

Status: 记录债务；不回改 XWC。

XWC 既有 `render_set_id` 不回改，避免扰动 accepted baseline 与历史报告。下一 session 开始使用新规范命名，并在新 manifest/report 中明确 render set 与 session/qinist/piece 的身份边界。

### E9 ML-ready candidate sidecar / sample candidate gate

Status: 纳入 Sanman startup。

该项用于定义 future Track B 候选证据 sidecar 与 sample candidate gate：保留 score event、take/session、R1 labels、R2/F preference labels、qinist realization 等证据边界，同时明确 wrong take、failed take、context-only take、render-only helper 的排除规则。当前不训练 ML。

### E10 production sample ingest schema

Status: 只定边界，不落地。

当前只做 schema/gate 边界设计，不写 `sample_assets.csv`、`recording_segments.csv` 或 `recording_items_enriched.jsonl`。sample ingest 需要单独授权、schema freeze、source authority freeze、segment-to-score proof、完整人工标签、wrong/failed/context-only exclusion checks 与跨曲验证。

## 4. Not-Now Items

### E6 generic real audio renderer

Status: 延后到真实新曲 F 前。

当前 generic render 工具链是 metadata-only / dry-run-first 工程复现路径，不是真实 wav renderer。generic real audio renderer 应延后到真实新曲进入 F 前，再以单独任务定义输入 authority、output sandbox、音频读写权限、验证策略和人工 gate。

当前也不做：

- 第二首执行。
- 三曼采集实现。
- production sample ingest。
- ML training。
- Arrangement Mode production。
- accepted `F_FINAL_REVIEWED` 重跑。
- XWC/Baiya historical scripts 参数化或执行。

## 5. Sanman Startup Dependencies

三曼启动依赖应按以下顺序处理：

1. 先完成 `CG-VARW-R0R1_EXPORT_MANIFEST_RELOAD_AND_IDENTITY_GUARD`，作为真实 R0/R1 数据接入前 blocker。
2. 将 `SANMAN_COLLECTION_COVERAGE_DIFF_ENGINE` 纳入 startup，用于采集缺口计算，而不是事后靠人工补漏。
3. 将 ML-ready candidate sidecar / sample candidate gate 纳入 startup，但只积累候选证据与 gate 设计，不触发 ML training。
4. 将 production sample ingest schema 限定为边界设计，不落地写入 sample ingest 文件。

## 6. Hard Boundaries

- 不进入第二首执行。
- 不进入三曼采集实现。
- 不运行真实 render。
- 不读取真实 audio binary。
- 不写 sample ingest。
- 不训练 ML。
- 不做 R0/R1 export hardening；本轮只记录 backlog。
- 不修改 R0/R1/R2 逻辑。
- 不修改 render 输出、`F_FINAL_REVIEWED`、canon、score、source files、raw audio 或 examples。
- 不处理旧 untracked `scripts/generate_baiya_recording_plan.py`：不运行、不删除、不移动、不归档、不 stage。

## 7. Recommended Next Tasks

### Next 1

`CG-VARW-R0R1_EXPORT_MANIFEST_RELOAD_AND_IDENTITY_GUARD`

E2/E3/E4 是三曼真实 R0/R1 数据接入前 blocker。建议下一轮先做 read-only audit，再实现 R0/R1 export manifest、reload validation、R0 CSV fallback manifest guard 与 R1 split root identity guard。

### Next 2

`CG-SANMAN-DIGITIZATION-STARTUP-v0.1`

Sanman startup 应纳入 E7 与 E9：先设计 `SANMAN_COLLECTION_COVERAGE_DIFF_ENGINE` 与 ML-ready candidate sidecar / sample candidate gate。E10 当前只做 production sample ingest schema 边界设计，不写 `sample_assets.csv`、`recording_segments.csv` 或 `recording_items_enriched.jsonl`。

## Historical Script Watch

`scripts/generate_baiya_recording_plan.py` 当前仍应保持 historical template / no-run 状态。它不应作为三曼 startup 或第二首入口，不应被 stage、提交、删除、移动或归档。
