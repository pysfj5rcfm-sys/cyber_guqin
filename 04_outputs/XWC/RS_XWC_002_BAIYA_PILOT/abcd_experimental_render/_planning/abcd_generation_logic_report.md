# 《仙翁操》ABCD/E 生成逻辑计划锁定报告（R0）

任务名称：`CG-XWC_ABCD_E_GENERATION_LOGIC_PLAN_LOCK_R0`

本报告只锁定 `RS_XWC_002_BAIYA_PILOT` 进入 ABCD experimental render 之前的计划层逻辑。本任务没有生成 wav，没有执行音频渲染，也没有创建 production sample ingest 所需资产。

## 1. 本任务只锁定生成逻辑

本次新增文件全部位于：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/_planning/`

它们的作用是描述后续 render 如何读取 71 条 readiness rows、如何区分 A/B/C/D 四版解释策略，以及未来 E_REVIEWED 应如何由 Human+GPT 共评修订产生。当前阶段仍然是 planning-only，不生成 A/B/C/D/E 的任何音频。

注意：用户点名的 `Core_Instructions_v1.4_RENDER_GENERATION_PROPOSED.md`、`Core_Instructions_v1.4.md`、`NEXT_CHAT_HANDOFF_XWC_ABCD_RENDER_GENERATION_v0.1.md` 未在当前 checkout 中找到；本报告按本任务消息与 readiness package 的硬边界执行。

## 2. ABCD 不是随机参数

ABCD 不是四套随机 tempo/crossfade 参数，也不是同一素材的机械拼接。四版共享同一 `render_source_map.local.json` 与同一 score/event order，但分别锁定四套 interpretation policy：

- `A_LITERAL`：直译谱面版，保留谱面骨架，rubato 克制。
- `B_PHRASE`：句法呼吸版，强调句读、气口、段落呼吸。
- `C_QINIST_STYLE`：琴人风格版，在不改谱面事实的前提下更自然地处理白牙样本衔接、尾音与呼吸。
- `D_TEACHING_DIAGNOSTIC`：教学/诊断版，结构、动作、音位边界更清楚，便于听评定位。

## 3. E_REVIEWED 不在本阶段生成

`E_REVIEWED` 的正式定义是 Human+GPT Co-Created Reviewed Dapu。它不是 ABCD 的平均版，不是 Codex 自动最佳版，也不是用户单独打分版。

未来 E 的来源链条必须是：

`ABCD render -> 用户听评 -> GPT 听评/结构分析/工程诊断/打谱解释诊断 -> e_revision_plan -> E render`

本阶段只新增 `e_co_review_schema.local.yaml`，用于定义未来共评输入 schema，并明确 `e_audio_generated: false`。

## 4. render_source_map.local.json 与 sample_assets.csv 的区别

`render_source_map.local.json` 是本次 ABCD experimental render 的局部样本映射，只覆盖 readiness manifest 中 71 条 ready rows。它保留 `source_split_audio`、`clean_preview_audio`、anchor、tail、human accepted 与 render usable 等字段，方便后续 render 读取。

它不是 `03_samples/sample_assets.csv`：

- 不进入正式 sample catalog。
- 不代表 production-grade sample。
- 不作为 ML training data。
- 不替代 `recording_segments.csv`。
- 不改变 R0/R1 archive。

## 5. render_phrase_plan.local.yaml 的边界

`render_phrase_plan.local.yaml` 是 render-local phrase inference。由于 readiness manifest 只有 `XWC_P09_N01_to_N02` 一个显式 transition event_range，其余普通事件的句法分组按现有 event order 与 `XWC_Pxx` 前缀做局部推断，全部标记为 `provisional` / `local_render_only`。

它不得反写 `score_events`，也不得声明为最终 verified dapu interpretation。任何无法从现有数据精确判断的句法，都留在 render-local 层。

## 6. ABCD 四版差异

四版差异被锁定在 `abcd_version_policy.local.yaml`：

- A 使用 `tempo_policy: stable`、`phrase_pause_policy: minimal_but_clear`、`crossfade_policy: conservative`。
- B 使用 `tempo_policy: phrase_shaped`、`phrase_pause_policy: phrase_boundary_sensitive`、`crossfade_policy: phrase_aware`。
- C 使用 `tempo_policy: flexible`、`phrase_pause_policy: natural_performance`、`crossfade_policy: smoother`。
- D 使用 `tempo_policy: slightly_spaced`、`phrase_pause_policy: explicit`、`crossfade_policy: minimal_or_transparent`。

这些差异只用于后续 experimental render，不改变谱面事实、不生成新 score fact。

## 7. T060/T071 context take 处理原则

特殊规则已写入 source map 与 policy：

- `T060 = context_take_1`
- `T071 = context_take_2`
- 二者均属于 `event_range = XWC_P09_N01_to_N02`
- 二者均是同一 transition 的 context references
- 不得强行当普通 atomic sample
- `T071` 必须保持 `batch08 / recording_take_no=T071 / batch_take_no=001`
- `T071` 不是 `batch07_take_011`，不是 retake

## 8. 后续真正 render 时如何使用

后续 render 任务应按以下顺序读取 planning 文件：

1. 读取 `render_source_map.local.json`，只使用其中 `render_usable=true` 且 `dummy_fallback_used=false` 的 71 条 rows。
2. 读取 `render_phrase_plan.local.yaml`，将 phrase pause、breath、cadence 作为 render-local timing hints。
3. 读取 `abcd_version_policy.local.yaml`，按 version policy 分别生成 A/B/C/D。
4. 禁止在 ABCD render 阶段读取或写入 production sample ingest 资产。
5. ABCD 完成并经用户/GPT 共评之后，才允许用 `e_co_review_schema.local.yaml` 收集 E 的 revision inputs。

## 9. 当前禁止事项遵守情况

本任务遵守以下禁止事项：

- 未生成 A/B/C/D/E 任一 wav。
- 未执行音频渲染。
- 未写 `03_samples/sample_assets.csv`。
- 未写 `03_samples/recording_segments.csv`。
- 未创建 `recording_items_enriched.jsonl`。
- 未修改 `score_events`、`gesture_templates`、`canon`、`sources`。
- 未修改 raw master。
- 未修改 R0/R1 archive。
- 未训练 ML。
- 未进入 production sample ingest。

## 10. 本次新增 planning 文件

- `render_source_map.local.json`
- `render_phrase_plan.local.yaml`
- `abcd_version_policy.local.yaml`
- `e_co_review_schema.local.yaml`
- `abcd_generation_logic_report.md`
- `abcd_generation_plan_validation.json`
