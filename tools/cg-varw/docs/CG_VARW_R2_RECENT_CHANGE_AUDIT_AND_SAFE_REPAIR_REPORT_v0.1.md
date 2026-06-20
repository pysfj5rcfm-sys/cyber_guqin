# CG-VARW R2 最近变更审计与安全修复报告 v0.1

任务：`CG-VARW-R2_RECENT_CHANGE_AUDIT_AND_SAFE_REPAIR`

## 1. 近期 R2 commits 审计

### `b69df22 feat(varw): ingest XWC ABCD render set for R2 review`

主要改动：

- 新增 `r2_review_intake` 的 render set index、phrase alignment seed、intake report、validation。
- 后端 `r2_mock_store.py` 增加真实 ABCD render set 读取能力。
- 后端 schema/test 增加 R2 intake 覆盖。
- README 增加 R2 render-set intake 说明。

应保留：

- render set index 与 seed 的 intake 入口。
- 后端读取真实 A/B/C/D render set 的能力。
- 不生成 E、不进入 production ingest 的 safety flags。

风险：

- 初始 seed 的 `phrase_end_s` 来源偏工程尾部，后续被前端当作默认播放终点时会带出下一句。

### `babf0df feat(varw): wire R2 frontend to real ABCD render set API`

主要改动：

- 新增 `frontend/src/api/cgVarwApi.ts`。
- 后端新增 R2 audio endpoint，前端通过后端 URL 播放 wav。
- `R2ProjectReviewPage.tsx` 大幅改写：约 1142 行 diff，442 行新增、700 行删除。
- 保留 mock fallback，同时加载真实 versions / phrase-alignments。

应保留：

- 真实 API 接线。
- 后端 audio endpoint。
- mock fallback。
- 不显示 E_REVIEWED。

风险：

- 这是页面结构“变陌生”的主要来源：页面文件被大幅替换，原来某些 R2 工作台布局和文案被压缩。
- 初版曾固定寻找 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`，后续已在 `24aee5c` 修掉。
- 当默认 API base 仍为 `8787` 时，用户后端跑在 `8788` 会 `Failed to fetch` 并 fallback mock；该 API base 修复在本轮前尚未提交。

### `24aee5c fix(varw): stabilize R2 phrase structure and review draft workflow`

主要改动：

- 新增 `phrase_structure_lock/` 下 4 个谱面句法锁定草案文件。
- 后端改为 env-driven：优先读取 `CG_VARW_R2_RENDER_ROOT` / `CG_VARW_R2_INTAKE_ROOT`。
- 前端不再固定真实 render_set_id，而是从 `/api/r2/render-sets` 选择真实 experimental render set。
- 前端恢复中文 UI，左侧按 unique phrase 展示 10 个谱面句。
- 新增 Export Preview payload builder。

应保留：

- env-driven 后端 intake。
- phrase_structure_lock 草案。
- unique phrase 的 10 句显示。
- 中文 UI 与 mock fallback。

风险：

- Export Preview 虽已改用 builder，但选中 phrase 为空时仍返回空字符串而不是 `null`。
- 播放仍直接使用 `alignment.start_s` / `alignment.end_s`，没有使用独立 playback-safe 边界。

### 最新 API base 修复

审计 `git log --oneline -- tools/cg-varw/frontend/src/api/cgVarwApi.ts tools/cg-varw/README.md` 后确认：本轮开始时，`cgVarwApi.ts` 默认 backend URL 从 `8787` 改到 `8788` 的修复尚未形成 commit，只存在工作树 diff 中。

本轮保留并纳入当前修复范围：

- `cgVarwApi.ts` 默认 API base：`http://127.0.0.1:8788`
- README R2 启动说明：后端端口 `8788`，可用 `VITE_CG_VARW_API_BASE` 覆盖。

## 2. 硬编码与 env-driven 审计

运行时结论：

- 后端真实 intake 仍通过 `CG_VARW_R2_RENDER_ROOT` / `CG_VARW_R2_INTAKE_ROOT` 读取。
- 未设置 env 时，仅做仓库内通用发现：`04_outputs/*/*/abcd_experimental_render/r2_review_intake/r2_render_set_index.json`。
- 前端不再硬编码 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e`。
- README / docs / intake 文件中保留的 `XWC`、`354811e`、`R2_XWC...` 是本次 XWC 数据包 provenance 或历史报告，不是运行时选择逻辑。
- 后端测试中保留 `R2_XWC...` 作为当前 fixture 断言，不影响 env-driven loader。

mock fallback 仍保留；中文 UI 仍保留；左侧仍按 10 个 unique phrase 展示谱面句。

## 3. 是否建议回滚

不建议整体回滚到 mock 或回滚后端数据层。

建议策略：局部修。

理由：

- b69df22 的真实 intake 与后端读取能力是 R2 正式听评所需。
- babf0df 改动较大，是页面陌生感的主要来源，但也带来了真实 API、audio endpoint、A/B/C/D 加载。
- 24aee5c 修复了 env-driven、10 句谱面结构和中文 UI，应保留。
- 当前明确 bug 可通过局部修复解决，不需要放弃真实 ABCD 听评能力。

若用户后续仍认为页面结构不可接受，建议 rollback plan 是：

1. 保留后端 `r2_mock_store.py` 的 env-driven intake、audio endpoint、safe seed 读取。
2. 保留 `phrase_structure_lock` 与 playback-safe seed。
3. 只回滚或重写 `R2ProjectReviewPage.tsx` 到更接近旧中文工作台的结构。
4. 重新接最小 API：render sets / versions / phrase-alignments / audio。
5. 不回滚到纯 mock。

本任务未执行回滚。

## 4. phrase 播放边界 bug

根因：

- `r2_phrase_alignment_seed.csv` 的 `phrase_end_s` 实际是当前 phrase 最后一个 event 的工程尾部/preview 末尾。
- 后端 `/api/r2/render-sets/{render_set_id}/phrase-alignments` 直接把 seed 的 `phrase_end_s` 返回为 `end_s`。
- 前端播放定时器直接用 `alignment.end_s` 停止。
- 数据检查显示，除最后一句外，原 `phrase_end_s` 普遍越过下一句 first attack：
  - A_LITERAL P01：`phrase_end_s=20.877`，下一句 first attack `16.815`，越界 `4.062s`
  - B_PHRASE P08：越界 `5.292s`
  - C_QINIST_STYLE P08：越界 `5.953s`

修复方式：

- 不覆盖原 seed，不修改 render_event_alignment。
- 新增 `r2_phrase_alignment_seed.playback_safe.csv`。
- 新增字段：
  - `phrase_play_start_s`
  - `phrase_play_end_s`
  - `phrase_tail_end_s`
  - `next_phrase_first_attack_s`
  - `phrase_end_policy`
- 非最后一句的 `phrase_play_end_s = next phrase first target_attack_time_s - 0.03s`。
- 原 `phrase_end_s` 保留为 `phrase_tail_end_s`，用于尾音专项检查，不再作为默认播放终点。
- 后端优先读取 playback-safe seed。
- 前端播放和 A→B→C→D 顺序播放优先使用 `phrase_play_start_s` / `phrase_play_end_s`，旧数据缺字段时才 fallback 到 `start_s` / `end_s`。
- 表格显示区分播放开始、播放结束、尾音参考、下一句首音。

验证文件：

- `r2_phrase_playback_boundary_validation.json`
- 40 行 safe seed，36 个非末句版本行全部通过：
  `phrase_play_end_s <= next_phrase_first_attack_s`

## 5. Export Preview / JSON 导出 bug

检查结果：

- 页面已经使用 `buildDraftExportPayload(...)` 同时供 Preview 和下载使用。
- comment-only / suggested_revision-only 草稿的过滤逻辑可以保留。
- 问题点是没有有效 phrase 时，selected 字段返回空字符串，不符合最小 skeleton 的 `null 或当前值` 要求。

本轮修复：

- `selected_phrase_id` / `selected_event_range` 现在在无有效 phrase 时返回 `null`。
- 真实 API 与 mock fallback 继续共用同一个 payload builder。
- 下载 JSON 继续直接使用页面 Preview 的同一份 payload。
- 未填写草稿时仍显示：
  - `draft_count: 0`
  - `reviews: []`
- 只填 comment 或 suggested_revision 时会生成 review。
- preferred_version 未选时导出为 `null`。

本轮未生成 `listening_review.yaml`，未生成 `e_revision_plan.yaml`，未自动判断最佳版本。

## 6. 安全边界

本轮未生成 E_REVIEWED，未生成新 wav，未重渲染 A/B/C/D，未训练 ML。

本轮未写：

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`

本轮未修改：

- `score_events`
- `gesture_templates`
- `canon`
- `sources`
- raw master
- R0/R1 archive

## 7. 后续用户验收

1. 启动后端在 `http://127.0.0.1:8788`，并设置 `CG_VARW_R2_RENDER_ROOT` / `CG_VARW_R2_INTAKE_ROOT`。
2. 启动前端；若未设置 `VITE_CG_VARW_API_BASE`，R2 默认连 `http://127.0.0.1:8788`。
3. 打开 R2 页面，确认仍显示真实 render set，而不是 mock fallback。
4. 选第 1 句播放：播放应在第 2 句 first attack 前约 0.03s 停止，不再带出第 2 句主发声。
5. 检查表格中播放结束与尾音参考不同：尾音参考可晚于下一句首音，但默认播放结束不得越界。
6. 填写 comment-only 草稿，确认 Export Preview 出现一条 review。
7. 点击导出 JSON，确认下载内容与页面 Export Preview 完全一致。
