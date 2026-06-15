# CG-VARW R2A Phrase Version Review State Fix Report v0.1

## 1. 前置检查

- `R0RawReviewPage.tsx` diff 为空，本轮未改 R0 页面。
- `R1SplitReviewPage.tsx` diff 为空，本轮未改 R1 页面。
- R0/R1 未 import `R2ExportPreviewPanel`。
- 修复前 preferred version 是全局 `preferredVersionId`，会让“设为偏好”看起来作用于整首曲/整个版本。
- 修复前 listening review 是全局 `review`，切换 phrase/version 时只改字段，不保存每个 phrase+version 的独立批注。
- playback 已有 `playMode` / `sequenceQueue`，但缺少 `currentQueueIndex` 和 `playingVersionId`，sequence 播放不可观察地推进版本。
- 左侧进度已从 boundary live state 派生，本轮继续纳入 phrase-level preferred 和 phrase+version review。

## 2. Preferred Version Phrase-Level

新增状态：

```ts
type PreferredVersionByPhrase = Record<string, string>;
```

现在“设为偏好”只更新：

```ts
preferredVersionByPhrase[activePhraseId] = versionId;
```

切换 phrase 后，右栏和版本切换区读取当前 phrase 自己的 preferred version。未设置时显示“未设置偏好”。写批注不会调用 preferred setter，也不会自动设置偏好版本。

## 3. Listening Review Phrase+Version-Level

新增状态：

```ts
type ListeningReviewByKey = Record<string, R2ListeningReviewDraft>;
```

key 为：

```ts
`${phrase_id}::${version_id}`
```

当前右栏 B 区读取 `listeningReviewByKey[activePhraseId::activeVersionId]`。切换 version 或 phrase 后会加载对应组合自己的批注；若不存在则创建空 draft。

## 4. 批注与偏好解耦

- `comment` onChange 只调用 `updateReview({ comment })`。
- `suggested_revision` onChange 只调用 `updateReview({ suggested_revision })`。
- `issue_type`、`severity`、`quick_judgement` 都只写当前 phrase+version review draft。
- 只有版本切换区“设为偏好”按钮和右栏 preferred select 会更新 `preferredVersionByPhrase`。

## 5. 听评批注分类

右栏 B 区改为：

- 当前评审对象
- 快速评价
- 问题类型
- 严重程度
- 文字批注
- 修订建议

分组标题为中文，避免所有字段平铺。

## 6. 本曲进度概览

`deriveProgressOverview` 现在从三类 live state 派生：

- `reviewedAlignments`
- `preferredVersionByPhrase`
- `listeningReviewByKey`

已审 phrase 规则：任一 version boundary accepted，或该 phrase 存在任一非空 listening review。已设偏好 phrase 数从 `preferredVersionByPhrase` 统计。

## 7. Sequence Playback

`R2PlaybackState` 增加：

```ts
currentQueueIndex?: number;
playingVersionId?: string;
```

三类按钮实现：

- 顺播 A→B→C→D→E：queue 为全部版本，playingVersion 从 A 开始，播放到当前 version end 后推进到下一个 version start。
- 播放偏好版本：读取 `preferredVersionByPhrase[activePhraseId]`；未设置时状态栏提示“当前 phrase 尚未设置偏好版本”。
- A/B 对比播放：固定 `A_LITERAL -> B_PHRASE`，不做自定义比较扩展。

## 8. Export Preview Rows

`R2ExportPreviewPanel` 保持 actual export rows preview，不回退 schema 表。

现在 preview rows 读取：

- `preferred_version_id`：来自 `preferredVersionByPhrase[phrase_id]`
- listening rows：来自 `listeningReviewByKey`
- `review_status` / `boundary_status`：来自传入的 `reviewedAlignments`
- `active_version_id`：来自当前 `activeVersionId`

切换 phrase/version，或修改批注/边界/偏好后，preview rows 会从 live props 更新。

## 9. R0/R1 保护

- 本轮未改 R0 页面。
- 本轮未改 R1 页面。
- 本轮未改 R0/R1 export preview。
- `ExportPanel` 仍保持通用组件；R2 逻辑只在 `R2ExportPreviewPanel`。
- 源码检查确认 R0/R1 没有 R2 category tabs 或 `导出当前 phrase`。

## 10. Source-Level Checks

- `preferredVersionByPhrase` 存在，并由当前 phrase 设置。
- `listeningReviewByKey` 按 phrase_id+version_id 存储。
- comment onChange 不调用 preferred setter。
- A/B 对比固定 `["A_LITERAL", "B_PHRASE"]`。
- sequence buttons 写入 `sequenceQueue`、`currentQueueIndex`、`playingVersionId`。
- 本曲进度概览从 live state 派生。
- R2 export preview rows 读取 preferred/listening/boundary live state。
- R0/R1 未 import `R2ExportPreviewPanel`。
- Browser QA 已尝试启动本地 dev server 并连接 Codex Browser 插件，但 Windows sandbox 仍返回 `CreateProcessAsUserW failed: 5`，因此本轮以 source-level checks、typecheck 和 build 作为验证依据。

## 11. 验证命令结果

- `cd tools/cg-varw/frontend && npm run typecheck`: 通过。
- `cd tools/cg-varw/frontend && npm run build`: 通过；生成的 `frontend/dist/` 已清理。
- `cd tools/cg-varw/backend && python -m compileall app`: 本机 `python` 不在 PATH，命令解析失败。
- `cd tools/cg-varw/backend && C:\Users\11028\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m compileall app`: 通过。

## 12. Git Status

报告生成前，工作区包含此前 R2A 修复遗留的预期源码 diff 和报告文件；本轮新增：

- `tools/cg-varw/docs/CG_VARW_R2A_PHRASE_VERSION_REVIEW_STATE_FIX_REPORT_v0.1.md`

## 13. 禁止目录确认

- 未改 R0/R1 页面。
- 未改 R0/R1 导出预览。
- 未接真实 render。
- 未生成 render。
- 未写 `03_samples/`。
- 未写 `04_outputs/`。
- 未写 `sample_assets.csv`。
- 未写 `recording_segments.csv`。
- 未写 `recording_items_enriched.jsonl`。
- 未训练 ML。
- 未写 `tools/cg-varw/review_outputs/r2/drafts/`。
- 未写 `tools/cg-varw/review_outputs/r2/exports/`。
