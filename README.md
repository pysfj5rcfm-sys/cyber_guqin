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
