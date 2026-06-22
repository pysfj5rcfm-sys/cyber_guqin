# 赛博古琴 Cyber Guqin v1.0

当前阶段：Phase 0.1 / Gesture Ontology v1.1 + Dummy Audio Skeleton
当前模式：Dapu Mode 古谱打谱模式
第一位数字琴人：QINIST_001 三曼
当前曲目：仙翁操 XWC

当前目标：用《仙翁操》51 个事件跑通 dummy audio 全链路，并固化古琴指法本体。本轮不是最终音频效果，只是工程骨架。

## 如何运行 smoke test

```bash
python 05_scripts/smoke_test.py
```

如果本机 `python` 不在 PATH，也可以用可用的 Python 3.11+ 解释器直接运行该脚本。

## 各目录用途

- `00_global/`：琴人、曲目、琴、调弦、schema contract、parse rules、指法本体、gesture templates 与 components。
- `01_pieces/xianwengcao/`：《仙翁操》句法结构、51 个 score events、recording script、rhythm candidates 与 review 占位。
- `02_recordings/`：真实录音 session 与 raw audio 占位。
- `03_samples/`：dummy samples 与 sample_assets 索引。
- `04_outputs/xianwengcao/`：dummy render wav 与 viability reports。
- `05_scripts/`：Phase 0.1 标准库流水线脚本。
- `06_docs/`：阶段说明与 gesture ontology 硬声明。

## 当前不做

本轮不做 OCR / Web UI / 机器学习 / 真实切分 / Arrangement Mode / reference performance 对齐 / DDSP / 神经音频生成。

下一步是真实录音与 `split_recording_session.py` 实现。再下一步才是 reference_performance、timing_profile、sample_selection_policy 真实化、review_taxonomy。

## XWC F 自包含 dry-run 复现

当前 Phase 1F 已增加一条 manifest-driven / dry-run-first 的复现工具链，用于让用户不依赖 Codex 也能理解《仙翁操》`F_FINAL_REVIEWED` 的工程生成路径。

入口文档：

- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `examples/cyber_guqin/`

generic scripts：

- `scripts/generate_recording_plan_from_dapu_ir.py`
- `scripts/render_abcd_from_manifest.py`
- `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py`
- `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py`

默认规则：

- 默认 `--dry-run`，只打印 summary 和 planned paths。
- `--execute` 才写文件，render/final execute 必须写入 `reproduction_runs/<RUN_ID>/` sandbox。
- 不覆盖 accepted `F_FINAL_REVIEWED`。
- 不直接运行 XWC/Baiya hardcoded historical scripts。
- 不写 `sample_assets.csv`、`recording_segments.csv` 或 `recording_items_enriched.jsonl`。
- 不进入第二首、sample ingest、ML training 或 Arrangement Mode。

第二首启动前应先准备新曲的谱面 authority、piece/session/qinist config、Dapu IR、recording config、ABCD render manifest 和 final render manifest，然后只用 generic tools 做 dry-run。
