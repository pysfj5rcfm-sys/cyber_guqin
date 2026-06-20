# CG-VARW R2 review state restore after dedupe report v0.1

任务：CG-VARW-R2_RESTORE_LISTENING_REVIEW_STATE_AFTER_DEDUPE

## 结论

680eb7d 后页面只剩 preferred version 的根因不是 latest JSON 丢失听评内容，而是前端 key mapping 不一致。

后端 canonical latest state 在去重后使用 `phrase_id:version_id` 作为 `listeningReviewByKey` key，例如：

`XWC_P01_LOCAL_PHRASE:C_QINIST_STYLE`

R2 页面右侧听评区读取时使用 `phrase_id::version_id`，例如：

`XWC_P01_LOCAL_PHRASE::C_QINIST_STYLE`

因此 preferred version 能恢复，因为它按 `phrase_id` 读取；comment / issue_type / severity / suggested_revision 查不到，因为页面用双冒号 key 取不到单冒号 key 下的 review。

根因判定：A + D。

- A: latest JSON 仍有 review，但前端 adapter 没恢复到页面可读 key；
- D: 前端 key 生成规则与后端 canonical key 不一致。

## 只读审计结果

`r2_review_drafts/latest/r2_review_state.latest.json` 仍包含去重后的 current review：

- current review_count: 29
- 非空 comment_count: 15
- 非空 suggested_revision_count: 13
- 非空 issue key count: 6
- issue item count: 6
- `review_history_archived` 存在，包含被移走的旧 review 历史

`latest/listening_review.csv`：

- 数据行: 29
- 非空 comment: 15
- 非空 suggested_revision: 13
- 非空 issue_type: 6

API / service 层 `load_project_review_draft_latest()` 返回：

- `has_draft=true`
- `draft_source=engineering_dir_latest`
- `review_count=29`
- `phrase_count=10`
- `preferred_version_count=10`
- `suggested_revision_count=13`
- draft 内 `listeningReviewByKey` key_count=29

## 修复内容

只修改前端 draft state adapter：

`tools/cg-varw/frontend/src/utils/r2ReviewDraftState.ts`

adapter 现在会把后端返回的 review key 统一转换为页面内部使用的双冒号 key：

- `phrase_id:version_id` -> `phrase_id::version_id`
- 已是 `phrase_id::version_id` 的 key 保持兼容

同时 adapter 会保留并规范化：

- `comment`
- `issue_type`
- `severity`
- `suggested_revision`
- `reviewer`
- `reviewed_at`
- `updated_at`

`boundaryStatusByKey` 和 `markersByKey` 也统一做 key normalize，避免同类问题再次出现。

## 防止空占位覆盖有内容 review

本次没有修改 dedupe 和 export CSV 逻辑，也没有写回 latest。页面加载时 adapter 先把 latest 中的 29 条 current review 放入 `listeningReviewByKey`，并使用页面实际读取的 key。右侧组件读取 `listeningReviewByKey[phraseVersionKey(activePhraseId, activeVersionId)]` 时，会先命中已恢复 review；只有 key 不存在时才生成空占位。

因此空占位不会覆盖 latest 中已有内容。

## 硬验收项

前端 adapter 验证结果：

- `listeningReviewByKey` key_count: 29
- comment_count: 15
- suggested_revision_count: 13
- issue_key_count: 6
- P01 C: `试试其它节拍` / `123——4——`
- P02 C: `试试其它节拍` / `12345——6——`
- P09 B/C/D: `把带上下文的掐起和上下文连接，这样不是就有2个上下文的音了？`
- P10 A: `试试其它节拍` / `1——234——5——6——7——`

页面刷新后，只要后端仍返回 latest draft，adapter 会再次执行同样 key normalize，听评内容仍应可见。

## 未触碰范围

本次未修改导出 CSV 逻辑，未修改 Downloads 逻辑，未修改底部按钮布局，未重渲染 A/B/C/D，未生成 E，未生成 `e_revision_plan.yaml`，未写 sample ingest 文件，未修改 R0/R1，未清空 latest，未覆盖 archive，未保存当前页面空 state。
