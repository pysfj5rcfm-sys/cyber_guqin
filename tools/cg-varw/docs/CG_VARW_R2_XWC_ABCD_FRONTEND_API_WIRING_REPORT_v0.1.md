# CG-VARW R2 XWC ABCD Frontend API Wiring Report v0.1

任务名称：`CG-VARW-R2_FRONTEND_API_WIRING_FROM_MOCK_TO_REAL`

## 1. 原因

上一轮后端已经能从 `r2_review_intake/` 读取真实 render set，但前端 `R2ProjectReviewPage.tsx` 仍静态 import `mock/projectReviewMock.ts`。因此页面显示的是 mock render set、mock audio path 与 mock A/B/C/D/E 数据。

## 2. 本次接入的 API

R2 页面加载时优先调用：

- `GET /api/r2/render-sets`
- `GET /api/r2/render-sets/{render_set_id}/versions`
- `GET /api/r2/render-sets/{render_set_id}/phrases`
- `GET /api/r2/render-sets/{render_set_id}/phrase-alignments`

若后端返回 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`，前端使用真实 A/B/C/D 数据；否则保留 mock fallback。

## 3. 真实 render set 判断

页面顶部显示 `render_set_id`，并标注数据源为 `真实 API` 或 `mock fallback`。真实模式下只显示：

- `A_LITERAL`
- `B_PHRASE`
- `C_QINIST_STYLE`
- `D_TEACHING_DIAGNOSTIC`

不显示 `E_REVIEWED`。

## 4. wav / audio URL

浏览器不直接读取本地文件路径。后端新增真实 intake 的 R2 audio resolver，并通过：

`GET /api/r2/render-sets/{render_set_id}/versions/{version_id}/audio`

返回 `FileResponse(audio/wav)`。前端把这个 endpoint 作为 `<audio>` 的 source。mock fallback 下不访问本地文件，仍使用模拟播放状态。

## 5. phrase-aligned 播放

前端播放当前 phrase 时，按 `phrase_id + version_id` 查找该版本自己的 `start_s` / `end_s`。播放时 seek 到该版本的 `start_s`，并用定时器在 `end_s` 停止。A→B→C→D 顺序播放逐版读取各自 phrase range，不按同一绝对时间点切换。

## 6. mock fallback

mock fallback 保留。后端不可用、没有真实 render set、或 API 请求失败时，R2 页面仍能以旧 mock 数据打开，避免阻塞 UI 调试。

## 7. E 边界

本轮未生成 E，未显示 E，未自动判断最佳版，未生成 `e_revision_plan.yaml`。Review Draft JSON 只包含用户草稿字段，并标记 `gpt_review_pending=true` 与 `e_revision_plan_generated=false`。

## 8. 禁写路径

本轮未写 `03_samples/sample_assets.csv`，未写 `03_samples/recording_segments.csv`，未创建 `recording_items_enriched.jsonl`，未训练 ML，未修改 score/canon/sources/raw/R0/R1 archive，也未提交 frontend `dist` 或 cache。

## 9. 后续使用

1. 启动后端，确保 `/api/r2/render-sets` 返回 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`。
2. 启动前端并打开 R2 页面。
3. 选择 phrase，再选择 A/B/C/D 版本播放。
4. 填写 `issue_type`、`severity`、`preferred_version`、`comment`、`suggested_revision`。
5. 使用 `Export Review Draft JSON` 导出草稿，后续交给 GPT 共评；本轮不生成最终听评 YAML 或 E。
