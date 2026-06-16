# CG-VARW R0/R1/R2 Final UI Regression Polish Report v0.1

## 1. 断点续跑检查

续跑时工作区已有 R0/R2/UI 样式相关修改，未推倒重做。已继续确认并保留的修改：

- R0 假重命名入口已移除，不再保留自动追加 `_R` 的误导行为。
- R0/R1 主工作区已调整为可滚动主栏，避免导出预览压住波形与播放控件。
- R2 draft key 已包含 session / piece / render_set，save/load 使用同一 key，并保留 legacy key 读取。
- R2 marker state 已改为 phrase+version 维度的 `markersByKey`，覆盖 marker position / review_status / notes。
- R2 marker review status 已改为按钮组，写入当前 selected marker state。
- R2 boundary status 已使用按钮组状态色。
- R2 操作按钮已使用 `review-actions`，与 R0/R1 保存/导出按钮风格靠齐，并与分类 tab 区分。
- R2 左侧进度概览中的旧边界不确定文案已统一为“待复核边界”。

继续补齐的事项：

- 清理验证过程中产生的 `tools/cg-varw/frontend/tsconfig.tsbuildinfo` 变更，避免生成物污染。
- 补跑 typecheck / backend compileall / git diff check。
- 记录 Vite dev/build 在当前执行环境下的 `spawn EPERM` 阻断。

## 2. R0/R1 Export Preview 遮挡修复

修复方式：

- `theme.css` 中 `.main-panel` 改为 `overflow: auto`，并保证 `.side-panel, .main-panel, .bottom-panel` 具备 `min-height: 0`。
- 导出预览未改为 fixed / sticky / absolute 覆盖层，仍保留在页面布局流内。
- R0/R1 原三文件导出预览未变，未引入 R2 分类 tab。

R0 文件仍为：

- `reviewed_slate_anchor_manifest.csv`
- `raw_marker_review.csv`
- `split_plan_from_raw_markers.csv`

R1 文件仍为：

- `reviewed_render_anchors.csv`
- `split_marker_review.csv`
- `segment_qc_sheet.csv`

## 3. R0 “重命名当前T”处理

已隐藏该误导入口：

- 移除 `renameSelectedUnit()`。
- 移除左侧单元操作中的“重命名当前 T”按钮。
- 未修改 `recording_take_no` / `batch_take_no` / `script_id` / `event_id` / `gesture_id` / `normalized_name`。
- 未改变 R0 导出主键或 CSV contract。

后续若需要人工别名，应另开 R0 unit alias patch，使用独立 alias / notes state。

## 4. R2 操作按钮样式

R2 `保存 draft` / `导出全部` / `导出当前 phrase` 所在容器改为：

- `export-actions review-actions`

并由 `theme.css` 中 `.review-actions button` 控制高度、字号、padding、圆角，与 R0/R1 保存/导出按钮更一致。分类 tab 仍使用独立 tab 样式，不混同为操作按钮。

## 5. R2 待复核计数

处理方式：

- 左侧进度概览统一显示 `待复核边界`。
- 计数从 live `phraseAlignments` / `boundaryStatusByKey` 派生后的 alignment review status 计算。
- 右侧 boundary status 按钮组提供对应 `unclear -> 待复核` 入口。
- 未保留不可解释的旧边界不确定计数文案。

## 6. R2 Draft Save/Load

当前 draft key：

```ts
const draftKey = `cg-varw:r2:draft:${renderSet.recording_session_id}:${renderSet.piece_id}:${renderSet.render_set_id}`;
```

并保留 legacy key 只读 fallback：

```ts
const legacyDraftKey = `cg-varw:r2:${renderSet.render_set_id}:draft`;
```

save/load 覆盖：

- `activePhraseId`
- `activeVersionId`
- `preferredVersionByPhrase`
- `boundaryStatusByKey`
- `listeningReviewByKey`
- `markersByKey`
- marker positions
- marker `review_status`
- marker `notes`
- `issue_type`
- `severity`
- `quick_judgement`
- `comment`
- `suggested_revision`
- `playbackRate`
- `loopPhrase`

page mount 时自动执行 draft load；手动加载失败会显示反馈，不静默吞掉。

不持久化：

- `isPlaying`
- `currentTimeS`
- `sequenceQueue`
- `currentQueueIndex`

## 7. R2 状态颜色映射

R2 boundary / marker 状态复用 shared review UI mapping：

- `candidate -> 待确认 -> neutral`
- `accepted -> 已确认 -> green/success`
- `unclear -> 待复核 -> amber/warning`
- `needs_retake -> 需重录 -> red/danger`
- `rejected -> 已排除 -> muted danger`

按钮使用 `status-option status-${statusToneClass(status)}`，active 状态有明确视觉反馈。

## 8. R2 Marker Review Status

R2 marker review status 已从 select 改为按钮组：

- `待确认`
- `已确认`
- `待复核`
- `需重录`
- `已排除`

点击按钮后调用 `updateMarker({ review_status: status })`，写入当前 phrase+version 下 selected marker 的 state。当前 marker 卡片与 marker 状态色从同一 state 派生；draft save/load 覆盖该状态。

## 9. Source-level Checks

结果：

- R0/R1 未 import `R2ExportPreviewPanel`。
- `R2ExportPreviewPanel` 仅由 `R2ProjectReviewPage.tsx` 使用。
- `ExportPanel.tsx` 无 R2 分类逻辑变更。
- R0/R1 未出现 R2 分类 tab、`导出当前 phrase`、Render 根目录文案。
- R0 假重命名入口无残留。
- R2 draft save/load 使用同一 primary key。
- R2 mount 自动 load draft。
- R2 marker review status 是按钮组，并写入 marker state。
- R2 boundary status 有颜色 mapping。
- R2 待复核计数有对应可设置状态。

## 10. QA 结果

R0/R1 source-level QA：

- 波形 / 播放区域所在 `.main-panel` 已改为内部滚动，导出预览不再作为覆盖层遮挡主工作区。
- R0 导出文件仍是原三文件。
- R1 导出文件仍是原三文件。
- R0 假重命名入口已移除。

R2 source-level QA：

- action buttons 已使用 R0/R1 风格按钮 class。
- boundary status button 使用状态色。
- marker review status 已为按钮组。
- marker 状态修改写入当前 marker state。
- draft payload 覆盖必须持久化状态。
- 左侧进度概览从恢复后的 alignment state 派生。

Browser UI QA：

- 未完成实际点击验证。
- 原因：`npm run dev -- --port 5173 --host 127.0.0.1` 在当前执行环境中启动 Vite 失败，报错 `Error: spawn EPERM`。
- 两次尝试请求放权启动 dev server，审批均超时无结果。
- 因 dev server 未能启动，未伪装完成 browser QA。

## 11. Validation Commands

已通过：

```bash
cd tools/cg-varw/frontend
npm run typecheck
```

结果：通过。

```bash
cd tools/cg-varw/backend
python -m compileall app
```

结果：通过。

```bash
git diff --check
```

结果：通过。

未通过 / 环境阻断：

```bash
cd tools/cg-varw/frontend
npm run build
```

结果：失败于 Vite/esbuild `Error: spawn EPERM`。

补充尝试：

```bash
npm run build -- --configLoader runner
npx vite build --configLoader native
```

结果：仍失败于 Vite Windows realpath / child process `spawn EPERM`。两次 build 放权审批均超时无结果。

## 12. Git Status

预期变更文件：

- `tools/cg-varw/frontend/src/components/ABCDEPhrasePlayer.tsx`
- `tools/cg-varw/frontend/src/components/R2ExportPreviewPanel.tsx`
- `tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx`
- `tools/cg-varw/frontend/src/pages/R2ProjectReviewPage.tsx`
- `tools/cg-varw/frontend/src/styles/theme.css`
- `tools/cg-varw/docs/CG_VARW_R0_R1_R2_FINAL_UI_REGRESSION_POLISH_REPORT_v0.1.md`

`tools/cg-varw/frontend/tsconfig.tsbuildinfo` 在验证后已恢复，不应出现在最终 diff 中。

## 13. 禁止目录与生成物

未触碰：

- `03_samples/`
- `04_outputs/`
- `sample_assets.csv`
- `recording_segments.csv`
- `recording_items_enriched.jsonl`
- `tools/cg-varw/review_outputs/r2/drafts/`
- `tools/cg-varw/review_outputs/r2/exports/`

检查结果：

- `tools/cg-varw/frontend/dist/`: not created
- `tools/cg-varw/frontend/.vite/`: not created
- `tools/cg-varw/frontend/.env.local`: not created
- `tools/cg-varw/review_outputs/r2/drafts/`: not created
- `tools/cg-varw/review_outputs/r2/exports/`: not created

仓库中存在 legacy `03_samples/` 与 `04_outputs/`，本轮未修改，记录为 pre-existing, not touched。

## 14. Render / Sample / ML

本轮未生成 render，未执行 split，未写 sample assets，未 sample ingest，未训练 ML。R2 输出仍保持 review-only / non-production 语义。

## 15. 结论

代码修复项已完成；source-level checks 与可运行的静态验证通过。

剩余阻断：

- Browser UI 点击 QA 未完成，原因是 Vite dev server 在当前执行环境被 `spawn EPERM` 阻断。
- Frontend production build 未完成，原因同为 Vite child process `spawn EPERM`，放权审批未返回。

最终状态：`READY_WITH_ENV_BLOCKER`。
