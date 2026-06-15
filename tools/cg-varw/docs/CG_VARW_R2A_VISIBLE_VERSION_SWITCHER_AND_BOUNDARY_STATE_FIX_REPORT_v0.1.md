# CG-VARW R2A Visible Version Switcher And Boundary State Fix Report v0.1

## 1. 前置检查

- `R0RawReviewPage.tsx` diff 为空，本轮未改 R0 页面。
- `R1SplitReviewPage.tsx` diff 为空，本轮未改 R1 页面。
- `ABCDEPhrasePlayer` 已在 `R2ProjectReviewPage.tsx` import，并实际 render 在 R2 中间栏标题区下方、waveform 区域上方。
- 版本切换不可见风险来自旧表头/row 列数不一致和中间栏 flex 区域可能压缩该块；本轮只修组件表头和 CSS 可见性。
- 右侧边界状态之前写入单个临时 `boundaryStatus`，版本切换区仍读取原始 `phraseAlignments.review_status`，左侧进度概览则是静态 mock 数字。

## 2. Version Switcher 可见性修复

- `ABCDEPhrasePlayer.tsx` 的表头改为与实际 row 一致的五列：版本、本句范围、边界状态、偏好、操作。
- `.version-switcher` 增加 `flex: 0 0 auto`、`display: block`、更明显的边框和标题样式，避免被中间栏 flex/overflow 压缩到不可见。
- 版本切换区仍位于 R2 中间标题区下方、waveform 上方。
- A/B/C/D/E 入口仍通过 `onSelect={selectVersion}` 切换 active version，并保留 `设为偏好` / `播放`。

## 3. Active Version 联动

点击版本后仍由 `selectVersion` 更新：

- `activeVersionId`
- 当前 phrase markers
- selected marker
- playback range
- right panel 当前版本
- R2 export preview 中的 active version
- 底部最近动作提示

本轮未重写已通过的 playback mock state 或 R2 actual export rows preview。

## 4. Boundary State 修复

边界状态改为写入：

```ts
type BoundaryStatusByKey = Record<string, MarkerReviewStatus>;
```

key 使用：

```ts
`${phraseId}::${versionId}`
```

`reviewedAlignments` 从 `phraseAlignments` 派生，并用 `boundaryStatusByKey` 覆盖对应 `review_status`。因此同一份 state 会同步驱动：

- 右侧边界状态按钮 active；
- 版本切换区该 version 行状态；
- `render_phrase_alignment.csv` preview rows 的 `review_status`；
- `phrase_boundary_decision.csv` preview rows 的 `boundary_status`；
- draft save/reload；
- 左侧本曲进度概览。

## 5. 左侧进度概览

左侧“本曲进度概览”不再是固定 mock 数字，改为从 `reviewedAlignments` 派生：

- `totalPhraseCount`
- `reviewedPhraseCount`
- `pendingPhraseCount`
- `unclearBoundaryCount`
- `needsRetakeCount`
- `preferredVersionCount`

当当前 phrase/version 的边界状态改为 `accepted`、`unclear` 或 `needs_retake` 时，左侧计数会立即从同一份 state 更新。

## 6. Draft Save/Reload

- 保存 draft 时，`phrase_alignments` 写入 `reviewedAlignments`，包含当前 phrase/version boundary status。
- reload draft 时，通过 `makeBoundaryStatusByKey(payload.phrase_alignments)` 恢复边界状态表。
- reload 后右侧边界状态、版本切换区状态、导出 preview rows、左侧进度概览都从恢复后的状态表派生。

## 7. R0/R1 保护

- 本轮未修改 `R0RawReviewPage.tsx`。
- 本轮未修改 `R1SplitReviewPage.tsx`。
- `R0RawReviewPage.tsx` / `R1SplitReviewPage.tsx` / `ExportPanel.tsx` 未引用 `R2ExportPreviewPanel`。
- R0/R1 与共享 `ExportPanel` 未出现 R2 分类文案或 `导出当前 phrase`。

## 8. Source-Level Checks

- `R2ProjectReviewPage.tsx` 存在 `import { ABCDEPhrasePlayer }`。
- `R2ProjectReviewPage.tsx` 实际 render `<ABCDEPhrasePlayer />`。
- `ABCDEPhrasePlayer.tsx` 的 version row/button 绑定 `onClick={() => onSelect(version.version_id)}`。
- 右侧边界状态按钮是 controlled UI，值来自 `boundaryStatus`，点击写入 `updateBoundaryStatus`。
- 左侧 progress overview 接收 `progress={progress}`，由 `deriveProgressOverview(reviewedAlignments, preferredVersionId)` 派生。
- R0/R1 没有 import R2 专用导出组件。
- `ExportPanel` 不含 R2 分类逻辑。
- Browser QA 已尝试启动本地 dev server 并连接 Codex Browser 插件，但 Windows sandbox 仍返回 `CreateProcessAsUserW failed: 5`，因此本轮以 source-level checks、typecheck 和 build 作为验证依据。

## 9. 验证命令结果

- `cd tools/cg-varw/frontend && npm run typecheck`: 通过。
- `cd tools/cg-varw/frontend && npm run build`: 通过；生成的 `frontend/dist/` 已清理。
- `cd tools/cg-varw/backend && python -m compileall app`: 本机 `python` 不在 PATH，命令解析失败。
- `cd tools/cg-varw/backend && C:\Users\11028\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m compileall app`: 通过。
- `git diff --check`: 通过。

## 10. Git Status

本轮报告生成前，工作区包含此前 R2A 修复遗留的预期源码 diff 和报告文件；本轮新增：

- `tools/cg-varw/docs/CG_VARW_R2A_VISIBLE_VERSION_SWITCHER_AND_BOUNDARY_STATE_FIX_REPORT_v0.1.md`

## 11. 禁止目录确认

- 未改 R0/R1 页面。
- 未改 R0/R1 导出预览。
- 未接真实 render。
- 未生成 render。
- 未写 `03_samples/`。
- 未写 `04_outputs/`。
- 未写 `sample_assets.csv`。
- 未训练 ML。
- 未写 `tools/cg-varw/review_outputs/r2/drafts/`。
- 未写 `tools/cg-varw/review_outputs/r2/exports/`。
