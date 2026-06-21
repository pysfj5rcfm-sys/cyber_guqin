# CG-XWC-MVP-P1C full_tail / natural_decay 默认策略固化报告

## 结论

本轮只固化古琴 `tail_policy` 默认策略、测试与文档；未重跑 render，未生成 G/F2，未修改真实 R0/R1/R2/F 数据，未进入 sample ingest。

古琴上下文中缺失 `tail_policy` 的 R1 `SplitSegment` 现在默认补为 `full_tail`。显式 `full_tail` 原样保留；显式 `smart_fade_100ms` 也原样保留，视为人工 override。synthetic demo 仍保留 legacy demo 默认，避免误改非古琴/demo fixture。

## 修改文件列表

- `tools/cg-varw/backend/app/schemas.py`
- `tools/cg-varw/backend/app/tests/test_csv_contracts.py`
- `tools/cg-varw/backend/app/tests/test_r2_review_draft_persistence.py`
- `tools/cg-varw/README.md`
- `reports/full_tail_natural_decay_default_patch.md`

## tail_policy 当前入口审计

- 当前 `tail_policy` 默认值入口在 `tools/cg-varw/backend/app/schemas.py` 的 `SplitSegment.tail_policy` 字段。修复前字段默认值为 `smart_fade_100ms`，会在 R1 输入缺失该字段时自动补入。
- R1 preview / split preview 不执行 fade 或 render。`tools/cg-varw/backend/app/services/r1_split_store.py` 只从 manifest/audio/fallback seed `pre_idle_end`、`gesture_start`、`render_anchor`、`tail_end` 标记，不生成 `tail_policy`。
- R1 export 在 `tools/cg-varw/backend/app/services/r1_review_store.py` 中消费 `segment.tail_policy`，写入 `reviewed_render_anchors.csv`，不生成音频、不写 sample assets。
- R1 前端 `tools/cg-varw/frontend/src/pages/R1SplitReviewPage.tsx` 只展示和手动选择 `tail_policy`，不产生后端默认值；本轮未改前端。
- F_FINAL_REVIEWED 生成脚本 `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py` 已将 F alignment rows 写为 `tail_policy=full_tail`、`source_tail_policy=full_tail`、`tail_preservation_policy=full_tail_no_smart_fade`，并在 render plan 中写 `safe_trim_smart_fade: false`、`aggressive_tail_fade: false`、`click_safe_fade_ms: 0`。
- F render 音频路径按完整 source chunk 混入，输出时长取 `phrase_tail_end_s` 与 source natural duration 的最大值；未按 `phrase_play_end_s` 裁切 source chunk。
- 旧刷新脚本 `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py` 会重写 R1/F 数据并复生成 F。本轮仅审计，不运行、不改，属于历史修复脚本，不应作为 P1-C 默认策略执行入口。
- `scripts/render_xwc_abcd_from_planning.py` 消费 planning/source map 中已有 `tail_policy` 并将 clean preview 全量混入；本轮不重跑 ABCD render，不改该历史 experimental render 脚本。

## 默认策略说明

- 古琴 render/review 输入缺失 `tail_policy` 时，默认策略为 `full_tail`，等价于本轮要求中的自然尾音保留 / `natural_decay` 默认行为。
- 显式 `tail_policy` 优先级高于默认值；人工显式设置的 `smart_fade_100ms` 不会被自动覆盖。
- `safe_trim_smart_fade` 不再通过 R1 缺失字段默认进入古琴 render path。
- click-safe fade 只能作为非破坏性防 click 处理存在；不得缩短 `tail_end_s`、`phrase_tail_end_s`、source preview duration 或 full_tail 语义。
- destructive trim 必须是显式 override / 非默认路径，并需要在 render plan/report 中说明原因。

## 是否修改真实数据

否。本轮未修改真实 R0/R1/R2 review 数据、F_FINAL_REVIEWED 输出、render 输出、sample ingest 文件、score/canon/source/schema、archive 文件，也未触碰 `scripts/generate_baiya_recording_plan.py`。

## 是否影响 F_FINAL_REVIEWED

不影响。本轮没有读取 F wav 内容，没有重跑 F，没有生成 G/F2。新增测试只加载 F 生成脚本的纯函数并 patch source duration，不读取或写入 F 输出。

## Tests 结果

- RED 先证实：`python3 -m unittest app.tests.test_csv_contracts` 在修复前失败 2 项，缺失 `tail_policy` 的古琴 segment 与 R1 export 都得到 `smart_fade_100ms`。
- `python3 -m unittest app.tests.test_csv_contracts`：8 tests OK。
- `python3 -m unittest app.tests.test_r2_review_draft_persistence.R2ReviewDraftPersistenceTests.test_f_alignment_rows_use_full_tail_policy_without_smart_fade app.tests.test_r2_review_draft_persistence.R2ReviewDraftPersistenceTests.test_f_full_tail_duration_uses_source_natural_decay_not_play_end`：2 tests OK。
- `python3 -m compileall app`：OK。
- `python3 -m unittest discover -s app/tests`：37 tests OK。
- `python3 -m pytest tools/cg-varw/backend/app/tests/test_csv_contracts.py -q`：未执行成功，当前 bundled Python 环境没有 `pytest` 模块；已用 `unittest` 跑同等 targeted/backend 测试。

## git diff --check 结果

`git diff --check`：通过，无输出。

## git status --short 结果

```text
 M tools/cg-varw/README.md
 M tools/cg-varw/backend/app/schemas.py
 M tools/cg-varw/backend/app/tests/test_csv_contracts.py
 M tools/cg-varw/backend/app/tests/test_r2_review_draft_persistence.py
?? reports/full_tail_natural_decay_default_patch.md
?? scripts/generate_baiya_recording_plan.py
```

其中 `scripts/generate_baiya_recording_plan.py` 为本轮开始前已存在的未跟踪文件；本轮未读取、未修改、未处理。

## 风险与回滚

- 风险：古琴上下文识别使用 `qinist_id` / `piece_id` / session/path 中的 `QINIST`、`XWC`、`GUQIN` 线索。若未来古琴项目不带这些线索，仍可能落到 legacy demo 默认；后续新曲应确保上下文 metadata 带有 `qinist_id` 或曲目/session 标识。
- 风险：显式 `smart_fade_100ms` 被保留，这是为了尊重人工 override；若某条旧数据曾被错误显式写入，需要单独审计数据，不在本轮自动改真实数据。
- 回滚：恢复 `tools/cg-varw/backend/app/schemas.py` 中 `SplitSegment` 的 before-validator 与默认策略常量，并移除本轮测试/文档/report 即可；不会涉及音频或真实 review 数据回滚。

## 是否建议提交

建议提交。变更范围小，测试覆盖缺失默认、显式保留、demo 不误改、R1 export、F full_tail/no smart fade 与自然尾音时长语义。

## 下一步

建议下一步进入《仙翁操》全流程固化与 MVP 经验文档，但保持为独立任务；不要把本轮 P1-C 与 F 重渲染、G/F2、sample ingest 或 R012 总重构合并。
