# CG-VARW R0/R1 Shared Bulk Review Usability Patch Report v0.1

任务：`CG-VARW-R0_R1_SHARED_BULK_REVIEW_USABILITY_PATCH`

结论：

```text
CG_VARW_USABILITY_READY__BULK_R1_REVIEW_CAN_CONTINUE
```

## 1. 修改文件列表

- `tools/cg-varw/README.md`
- `tools/cg-varw/backend/README.md`
- `tools/cg-varw/backend/app/schemas.py`
- `tools/cg-varw/backend/app/services/r1_split_store.py`
- `tools/cg-varw/backend/app/services/waveform_service.py`
- `tools/cg-varw/backend/app/tests/test_r1_marker_seed.py`
- `tools/cg-varw/backend/app/tests/test_waveform_service.py`
- `tools/cg-varw/frontend/src/components/AudioCanvas.tsx`
- `tools/cg-varw/frontend/src/components/MarkerNudgeControls.tsx`
- `tools/cg-varw/frontend/src/components/ReviewPrimarySelector.tsx`
- `tools/cg-varw/frontend/src/components/ReviewSecondarySearchList.tsx`
- `tools/cg-varw/frontend/src/components/WaveformAsyncLayer.tsx`
- `tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx`
- `tools/cg-varw/frontend/src/pages/R1SplitReviewPage.tsx`
- `tools/cg-varw/frontend/src/styles/theme.css`
- `tools/cg-varw/frontend/src/types/cgVarw.ts`
- `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R0_R1_SHARED_BULK_REVIEW_USABILITY_PATCH_REPORT_v0.1.md`

## 2. R0/R1 共享组件与共享逻辑

- 新增 `ReviewPrimarySelector`：R0 用于 Raw 文件一级选择，R1 用于 Split batch 一级选择。
- 新增 `ReviewSecondarySearchList`：R0 用于当前 raw 下 T unit 搜索，R1 用于当前 batch 下 segment/clean preview 搜索。
- 新增 `WaveformAsyncLayer`：统一前端 waveform 异步请求、`AbortController` 取消、前端内存 cache、防止旧请求串图。
- 新增 `MarkerNudgeControls`：统一 R0/R1 微调按钮为 `-500ms/-50ms/-5ms/+5ms/+50ms/+500ms`，并显示 `nudge_total_ms`。
- `AudioCanvas` 改为纯视觉层，只消费后端 downsampled peaks，不再下载完整音频做浏览器端 WAV 解析。

## 3. R1 父级 split root discovery

- `CG_VARW_SPLIT_ROOT` 指向父级 `split_preview` 时，后端会发现子目录 `batchXX`。
- batch 识别依据包含：
  - `r1_synthetic_split_manifest.json`
  - `manifests/recd2_split_preview_manifest.csv`
  - `manifests/r1_intake_pointer.yaml`
  - `clean_previews/`
- `/api/r1/batches` 返回 `batch_id`、`segment_count`、`source`、`split_root`、`manifest_path`、`clean_preview_count`、`ready_for_r1_review`。
- 每个 batch 保持独立 root；不会把多个 batch 合并成一个大 batch。

## 4. single batch root 兼容

- `CG_VARW_SPLIT_ROOT` 直接指向 `split_preview/batch02` 一类单 batch root 时仍可用。
- 旧 demo root 中单 manifest 含多个 batch 的模式也保持兼容。
- 新增测试覆盖 parent root 和 single batch root。

## 5. 左栏一级选择

- R0：一级为 Raw 文件搜索筛选框，搜索字段包含 batch、T 范围、文件名、relative path。
- R1：一级为 Split batch 搜索筛选框，搜索字段包含 batch id、display name、数量信息。
- 两者都有 loading/empty/error 状态结构，并保持当前选中高亮。

## 6. 左栏二级搜索

- R0：选择 raw 后只加载并显示当前 raw 的 T units；二级搜索字段包含 `T`、`unit_id`、`batch_id`、`script_id`、`event_id`、`source_raw_audio`。
- R1：选择 batch 后只加载并显示当前 batch 的 clean previews/segments；二级搜索字段包含 `take_id`、`recording_take_no`、`segment_id`、`event_id`、`gesture_id`、文件名、`source_split_audio`。
- 切换一级对象时二级搜索自动清空；每个一级对象会优先恢复上次选中的二级对象，否则选第一个。

## 7. 播放与 waveform 解耦

- R0/R1 的 `<audio>` 是播放主通道，切换对象后先设置 audio src。
- waveform 请求由 `WaveformAsyncLayer` 异步发起，不阻塞播放按钮、播放速度或循环试听。
- waveform loading 时显示 skeleton；marker 文本仍可在右栏查看和微调。
- waveform 请求支持 abort；旧请求返回后不会覆盖当前音频。
- `AudioCanvas` 不再 fetch 整段音频，因此不会因长 raw 音频阻塞首屏。

## 8. waveform 性能优化与 cache

- R0/R1 后端共用 `waveform_service.waveform_peaks_for_path`。
- 返回固定 points 的 downsampled peaks，默认 R0 请求 2000 points，R1 请求 1600 points。
- cache key 为 `path + mtime_ns + size + points`。
- cache 为进程内 LRU，最多 128 条；不写 `02_recordings/`、`03_samples/`、`04_outputs/` 或 repo asset 目录。
- 因未写磁盘 cache，无需新增 `tools/cg-varw/.cache/` 或 `.gitignore` 项。

## 9. 微调按钮与 clamp

- R0/R1 微调按钮统一为：

```text
-500ms -50ms -5ms +5ms +50ms +500ms
```

- R0 marker clamp 到 `0..raw_duration_s`。
- R1 marker clamp 到 `0..clean segment duration_s`。
- `nudge_total_ms` 继续累计，不改变 CSV 字段语义。
- 未新增快捷键。

## 10. 旧功能与数据语义

- 未改 R0/R1 CSV export 字段语义。
- 未把 `take_id` 补成 `recording_take_no`。
- 未自动设置 `accepted`、`render_usable` 或任何人工审校结论。
- 未修改 R0/R1 reviewed outputs。
- R0 terminal take export 和 R1 real split marker seed 通过既有测试回归。

## 11. 验证命令结果

后端：

```text
cd tools/cg-varw/backend
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m compileall app
OK

/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_csv_contracts app.tests.test_r1_marker_seed app.tests.test_waveform_service
Ran 10 tests in 0.011s
OK
```

真实 R1 父级 split root smoke：

```text
CG_VARW_SPLIT_ROOT=.../split_preview
list_batches -> batch01..batch08
batch01: 10
batch02: 10
batch03: 10
batch04: 10
batch05: 10
batch06: 10
batch07: 10
batch08: 1
ready_for_r1_review: true for all discovered batches
```

前端：

```text
cd tools/cg-varw/frontend
npm run typecheck
OK

npm run build
OK
```

说明：`npm run build` 会生成 `frontend/dist/`，该目录在 `tools/cg-varw/frontend/.gitignore` 中，未纳入提交范围。

## 12. Manual QA / smoke test

本次只做工具 UI smoke，不执行 R1 审校、不保存 draft、不导出 CSV。

- Backend 使用真实路径启动：
  - `CG_VARW_RAW_ROOT=.../RS_XWC_002_BAIYA_PILOT/raw`
  - `CG_VARW_SPLIT_ROOT=.../RS_XWC_002_BAIYA_PILOT/split_preview`
- R0 smoke：
  - R0 左栏显示 `Raw 文件` 一级搜索。
  - R0 左栏显示二级 `搜索 T / unit_id / batch_id / event_id`。
  - 搜索 `batch08` 可见 `RS_XWC_002_BAIYA_PILOT_batch08_T071.wav`。
  - 搜索结果未混入 `batch07` raw。
  - 选择 batch08 raw 后，二级列表可见 `T071`，未混入 `T070`。
  - R0 播放按钮可见；waveform 区域可见。
- R1 smoke：
  - R1 左栏显示 `Split 批次` 一级搜索。
  - R1 batch list 可见 `batch01` 到 `batch08`。
  - 搜索 `batch08` 后选择 batch08，当前 batch 切换为 `batch08`。
  - batch08 二级列表显示 `T071_clean_preview`。
  - R1 二级搜索 `T071` 时未混入 `T070`。
  - R1 播放按钮可见；waveform 区域可见。
  - DOM 检查 `emptySrcCount=0`。

## 13. 禁区路径确认

- 未执行 R1 人工审校。
- 未保存 R1 draft。
- 未导出 R1 CSV。
- 未重新 split。
- 未重新生成 unit preview / clean preview。
- 未 render。
- 未训练 ML。
- 未写 `04_outputs/`。
- 未写 `recording_items_enriched.jsonl`。
- 未新增本任务产生的 `03_samples/` 文件。
- 仓库既有 `03_samples/sample_assets.csv` 与 `03_samples/recording_segments.csv` 存在，但本任务未修改。

## 14. git status

最终 `git diff --check`：通过，无输出。

最终 `git status --short --untracked-files=all`：

```text
 M tools/cg-varw/README.md
 M tools/cg-varw/backend/README.md
 M tools/cg-varw/backend/app/schemas.py
 M tools/cg-varw/backend/app/services/r1_split_store.py
 M tools/cg-varw/backend/app/services/waveform_service.py
 M tools/cg-varw/backend/app/tests/test_r1_marker_seed.py
 M tools/cg-varw/frontend/src/components/AudioCanvas.tsx
 M tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx
 M tools/cg-varw/frontend/src/pages/R1SplitReviewPage.tsx
 M tools/cg-varw/frontend/src/styles/theme.css
 M tools/cg-varw/frontend/src/types/cgVarw.ts
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R0_R1_SHARED_BULK_REVIEW_USABILITY_PATCH_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
?? tools/cg-varw/backend/app/tests/test_waveform_service.py
?? tools/cg-varw/frontend/src/components/MarkerNudgeControls.tsx
?? tools/cg-varw/frontend/src/components/ReviewPrimarySelector.tsx
?? tools/cg-varw/frontend/src/components/ReviewSecondarySearchList.tsx
?? tools/cg-varw/frontend/src/components/WaveformAsyncLayer.tsx
```

其中 `scripts/generate_baiya_recording_plan.py` 为本任务开始前已存在的无关未跟踪文件，未读取、未修改、未纳入建议提交范围。
