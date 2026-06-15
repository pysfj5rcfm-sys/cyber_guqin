# CG-VARW R2A Functional Closure And Version Switcher Repair Report v0.1

## 1. 前置检查结论

- `git diff --name-only` 显示本轮相关 tracked diff 集中在 R2 UI、R2 mock 数据、共享导出表格恢复和样式文件。
- `R0RawReviewPage.tsx` / `R1SplitReviewPage.tsx` diff 为空，本轮没有对 R0/R1 页面产生业务改动。
- `ExportPanel.tsx` 已恢复为普通导出表格组件，不包含 R2 分类 tab、phrase export 或 R2 preview rows 逻辑。
- `R2ExportPreviewPanel.tsx` 是 R2 专用组件，只由 `R2ProjectReviewPage.tsx` 使用；R0/R1 未引用。

## 2. 上一轮 A/B/C/D/E 不闭环原因

上一轮 R2 页面虽然保留了 active version 文案，但中间栏缺少明确、可点击、状态联动完整的 A/B/C/D/E 版本切换区。版本切换没有形成统一入口，也没有把 waveform markers、右栏状态、播放范围、导出 preview 和底部状态栏绑定到同一个 `activeVersionId` 状态源。

## 3. Version Switcher 修复

- `ABCDEPhrasePlayer.tsx` 改为明确的“版本切换 / 当前 phrase 对齐”区域，放在 R2 中间栏标题区下方、waveform 上方。
- A/B/C/D/E 五行全部可点击，并提供独立的“设为偏好”和“播放”按钮。
- 当前 active version 使用高亮行；preferred version 使用独立“偏好”标识。
- 主 UI 只显示中文版本名，如 `B 句法呼吸版`；internal key 仅作为 `title` / `data-version-id` 辅助信息。

## 4. Version State 联动

`R2ProjectReviewPage.tsx` 统一维护：

- `activePhraseId`
- `activeVersionId`
- `preferredVersionId`
- `selectedMarkerId`
- `markers`
- `review`
- `playback`
- `lastActionMessage`

点击版本后会同步更新：

- active version 高亮；
- 当前 phrase + version 的 alignment；
- waveform marker 数据；
- 右栏“当前版本”；
- 播放 range；
- R2 export preview rows 中的 `active_version_id`；
- 底部状态栏最近动作。

## 5. Mock Playback 修复

R2 播放控件从 no-op 改为可观察 mock player state：

- `播放 / 暂停` 切换 `isPlaying`；
- `currentTimeS` 在播放时按 `playbackRate` 推进；
- `从句头播放` 跳到当前 active version 的 phrase start；
- `从当前标记播放` 跳到 selected marker time；
- `前滚 300ms` 使用 `max(marker_time - 0.3, phrase_start)`；
- `循环当前 phrase` toggle 后在 phrase end 回到 start；
- `0.5x / 1x / 1.5x` 更新 rate 并高亮；
- `上一 phrase / 下一 phrase` 切换 phrase 并刷新 markers/range；
- `顺播 A→B→C→D→E` 使用当前 phrase 的各 version range；
- `播放偏好版本` 使用 preferred version range；
- `A/B 对比播放` 使用当前 phrase 的 A/B range。

## 6. Marker 状态修复

- 右栏主句读标记只保留 `句头 / 句尾 / 气口 / 收束`。
- 点击主句读标记会更新 `selectedMarkerId`。
- 微调按钮会修改 selected marker 的 `time_s`。
- review status 下拉会修改 selected marker 的 `review_status`。
- notes textarea 会修改 selected marker 的 `notes`。
- waveform marker label/color/selected state 使用同一份 `markers` 状态。
- draft save/load 使用当前 phrase markers，不写真实 render/sample 输出。
- `Section 上下文` 不显示 timed `section_start` 卡，不参与主操作。

## 7. Export Preview 修复为 Actual Rows

`R2ExportPreviewPanel.tsx` 已从 schema/字段说明表改为 actual export preview rows：

- `全部` 只显示文件属性表。
- `句读结构` 展示 `phrase_structure_review.yaml` / `phrase_boundary_decision.csv` 的实际 preview rows。
- `版本对齐` 展示 `render_phrase_alignment.csv` 的实际 preview rows。
- `听评记录` 展示 `listening_review.yaml` / `issue_list.csv` 的实际 preview rows。
- `修订依据` 展示 `render_revision_log.yaml` 的实际 preview rows。
- `汇总` 展示 `preferred_version_summary.csv` 的实际 preview rows。
- 每个 preview table 的列名是导出字段，每行是将要导出的记录；不再使用 `字段 / 示例值 / 说明`。
- 文件“预览”按钮会切换/聚焦对应 preview table，不再是无动作按钮。

## 8. Main UI Internal Key 清理

- 中间栏和右栏主文案显示中文 label：`A 直译谱面版`、`B 句法呼吸版`、`待确认`、`已确认` 等。
- `A_LITERAL` / `B_PHRASE` / `candidate` 等 internal key 不再作为主 UI 文案并列显示。
- internal key 保留在 `title`、`data-version-id` 或导出字段中，便于调试和导出契约保持稳定。

## 9. R0/R1 防污染确认

源码扫描结果：

- `R0RawReviewPage.tsx`、`R1SplitReviewPage.tsx`、`ExportPanel.tsx` 未引用 `R2ExportPreviewPanel`。
- R0/R1 页面与共享 `ExportPanel` 未出现 R2 分类文案：`句读结构 / 版本对齐 / 听评记录 / 修订依据 / 汇总`。
- R0/R1 页面与共享 `ExportPanel` 未出现 `导出当前 phrase`、`Render 根目录`、R2 preview rows。
- R0/R1 CSV writer 语义和数据模型未修改。

## 10. R2 QA 结果

- A/B/C/D/E version switcher 已恢复在中间栏，五个版本均有 clickable handlers。
- active version 会驱动 waveform markers、右栏当前版本、播放状态、导出 preview 和底部状态。
- 播放/暂停、从句头、从当前标记、前滚 300ms、循环、速度、上一/下一 phrase、顺播、preferred、A/B 对比均有状态更新。
- 句读 marker 选择、time 微调、status 更新、notes 更新均绑定实际 marker state。
- R2 export preview 已改为 actual export rows。
- 浏览器级 QA 尝试使用 Codex Browser 插件，但本机 Windows sandbox 返回 `CreateProcessAsUserW failed: 5`，无法完成 in-app browser 操作；已用 typecheck/build/source-level checks 做替代验证。

## 11. R0/R1 Regression QA 结果

- R0/R1 页面 diff 为空。
- R0/R1 未 import R2 专用 export panel。
- 共享 `ExportPanel` 保持普通文件属性表 + action column，不包含 R2 分类逻辑。
- R0/R1 不显示 R2 category tabs、不显示 `导出当前 phrase`、不显示 Render 根目录文案。

## 12. 验证命令结果

- `cd tools/cg-varw/frontend && npm run typecheck`: 通过。
- `cd tools/cg-varw/frontend && npm run build`: 通过；生成的 `frontend/dist/` 已清理。
- `cd tools/cg-varw/backend && python -m compileall app`: 本机 `python` 不在 PATH，命令解析失败。
- `cd tools/cg-varw/backend && C:\Users\11028\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m compileall app`: 通过。
- Source-level checks: 通过，确认 R2 handlers 存在、R2 preview 不含 schema 表文案、R0/R1 未引用 R2 专用组件。

## 13. Git Status 结果

报告生成前的工作区状态：

- Modified:
  - `tools/cg-varw/frontend/src/components/ABCDEPhrasePlayer.tsx`
  - `tools/cg-varw/frontend/src/components/ExportPanel.tsx`
  - `tools/cg-varw/frontend/src/mock/projectReviewMock.ts`
  - `tools/cg-varw/frontend/src/pages/R2ProjectReviewPage.tsx`
  - `tools/cg-varw/frontend/src/styles/theme.css`
- Untracked:
  - `tools/cg-varw/frontend/src/components/R2ExportPreviewPanel.tsx`
  - prior R2A report docs
  - this report file after creation

## 14. 禁止目录与越界确认

- 未读取真实 render audio。
- 未生成 ABCDE render。
- 未执行 split / sample ingest / ML training。
- 未写 `03_samples/`。
- 未写 `04_outputs/`。
- 未创建 `sample_assets.csv`、`recording_segments.csv`、`recording_items_enriched.jsonl`。
- 未写 `tools/cg-varw/review_outputs/r2/drafts/`。
- 未写 `tools/cg-varw/review_outputs/r2/exports/`。
- R2 仍保持 review-only / non-production mock UI。
