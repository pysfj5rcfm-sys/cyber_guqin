# cyber_guqin_mvp_workflow Skill Design and Three Target Coverage v0.1

- Task: `CG-XWC-MVP-P1D_PROCESS_PLAYBOOK_LESSONS_SCRIPT_AUDIT_AND_WORKFLOW_SKILL_DESIGN`
- Phase: `Phase 1F-XWC-MVP Passed / Sweep & Review`
- Mode: design draft only. This is not a real `SKILL.md`.

## 0. 本轮执行声明

本轮未生成真正 `skills/cyber_guqin_mvp_workflow/SKILL.md`，未 patch，未改代码，未改数据，未跑 render，未生成 G/F2，未进入 sample ingest，未训练 ML，未进入第二首。本文只是单一 workflow skill 的设计草案。

## 1. Skill 名称与定位

建议名称：`cyber_guqin_mvp_workflow`

这是一个主流程 skill，不是拆成 4 个分散 skills。工程防坑、音乐防坑、脚本复用都放在 workflow 的 phase gate、authority gate、script registry 中。能工程化解决的问题，不靠 skill 记忆；skill 只负责流程编排、阶段边界、权威文件判断、脚本调用顺序、人工验收点和 stop rules。

## 2. Purpose

帮助 Cyber Guqin 从古谱/谱字输入推进到 Dapu audition MVP，并把中间产物沉淀为未来 digital qinist 数据候选，同时防止把 audition、sample ingest、ML、Arrangement Mode 混成一个任务。

## 3. When to Use

使用时机：

- 新古谱进入 Dapu Mode。
- 需要从谱面生成补录计划、R0/R1/R2、ABCD/E/F。
- 需要判断某个 XWC/Baiya 经验是否可复用到第二首。
- 需要审计脚本是否可跑、只可 dry-run、还是 historical-only。
- 需要确认某个产物能否进入 future sample candidate pool。

不要使用时机：

- 只处理 canon 规则抽取，应使用 `guqin-canon-builder`。
- 只解析具体减字谱 token，应使用 `guqin-dapu-parser`。
- 只做已定义代码 patch，应按具体工程任务执行。
- 进入 production sample ingest / ML training / Arrangement production 前，必须另开 gate。

## 4. Upstream Skills

### 4.1 `guqin-canon-builder`

| Field | Design |
| --- | --- |
| 位置 | 规则层 / canon layer |
| 作用 | 术语、指法、alias、component、gesture family、source evidence 的 canon-ready 结构化。 |
| 输出 | canon rules / ontology / alias mapping，例如 component lexicon、gesture families、alias rules、technique rules、validation rules。 |
| workflow 使用时机 | 遇到未知谱字；指法语义不确定；canon evidence 缺失；parser output 与 canon 冲突。 |
| 边界 | 不解析 concrete score events；不生成 XWC events；不生成 recording items；不修改 V1 runtime。 |

### 4.2 `guqin-dapu-parser`

| Field | Design |
| --- | --- |
| 位置 | 解析层 / score-to-IR layer |
| 作用 | 减字谱 / OCR / 人工谱字 -> Dapu Event IR / semantic recording item。 |
| 输出 | score events、gesture events、recording items、validation report。 |
| workflow 使用时机 | 新谱面 intake；OCR/manual text 转结构化；区分 score facts 与 qinist realization；生成录音 coverage / 补录清单前。 |
| 边界 | 不抽取规则书 canon；不决定三曼/白牙最终演奏风格；不生成 audio；不创建 `recording_items_enriched.jsonl`。 |

## 5. Track A: Dapu Mode / 新古谱到 F

Track A 是当前 MVP 已能覆盖的主闭环。

1. 新谱面输入。
2. 调用 `guqin-canon-builder` 处理未知术语、指法、alias、gesture family。
3. 调用 `guqin-dapu-parser` 把 token/OCR/manual notation 转 Dapu Event IR。
4. 生成 Dapu Event IR、score events、gesture events、recording item candidates。
5. 对照已有样本库和已有录音 coverage。
6. 输出缺失指法、缺失上下文、缺失录音、wrong-take risk。
7. 生成补录计划，必须人审。
8. R0 raw review：slate/marker/accepted units。
9. R1 split review：segments/render anchors/tail policy/QC。
10. R2 render review：ABCD phrase/version review，latest JSON canonical。
11. ABCD experimental render：只在授权后生成。
12. E_REVIEWED：从 R2 latest + co-review 生成 reviewed candidate。
13. F_FINAL_REVIEWED：从 E review + latest JSON 生成 final audition。
14. 人耳验收：pass / residual note / narrow reopen。
15. closeout：报告、lessons、script audit。
16. 第二首复用：只复用 gates 和参数化脚本，不复用 XWC hardcode。

Phase gate:

- 任何从 score/canon 到 recording plan 的转移，都必须确认 score facts 与 qinist realization 分离。
- 任何从 R2 到 E/F 的转移，都必须确认 canonical latest JSON。
- 任何 F pass 之后进入 sample ingest，都必须另开 gate。

## 6. Track B: Qinist Digitalization / 三曼数字琴人数据积累

Track B 从 Track A 每首曲子的产物中积累 future ML-ready candidates，但当前不是 ML training。

可积累：

- score_event 对齐明确的 accepted segments。
- R1 accepted / QC passed / render anchor 明确的 segment。
- R2 preferred/human labels。
- F accepted 的 phrase-level preference。
- source_take provenance、wrong take exclusion、replacement provenance。
- qinist realization fields，例如 default chuo / yin-nao / tempo preference，必须与 score facts 分离。

必须排除：

- failed take。
- wrong take，例如 T008。
- context-only take 当作 atomic sample。
- bad retake 或未经人审的 take。
- 只在 render 中作为过渡参考的 context candidate。

human preference labels 记录方式：

- phrase-level：preferred version、comment、severity、suggested_revision。
- segment-level：accepted/rejected、render_anchor、tail_policy、human_accepted。
- sample-level candidate：source_take_id、score_event_id、realization_variant、review labels、exclusion reason。

为什么当前仍不是 ML training：

- `sample_assets.csv` 未生成。
- `recording_segments.csv` 未生成。
- `recording_items_enriched.jsonl` 未生成。
- sample ingest schema 未冻结。
- 跨曲目数据量不足。
- 质量门禁和 negative labels 还未系统化。

未来 sample ingest gating 条件：

- schema freeze。
- source authority freeze。
- segment-to-score alignment proof。
- human labels complete。
- failed/wrong/context-only exclusion rules。
- cross-piece validation。

## 7. Track C: Arrangement Mode / 现代曲到古琴化减字谱

Track C 是 future track。当前只能覆盖设计，不能宣称生产级可用。

未来输入：

- 简谱。
- 五线谱。
- MIDI。
- MusicXML。

未来流程：

1. pitch/rhythm/phrase 解析。
2. 旋律范围、调式、句法和可奏性分析。
3. 古琴可奏性映射：弦序、徽位、散/按/泛选择。
4. 指法搜索：右手、左手、滑音、吟猱、上下进复、上下文连接。
5. 古琴化编配：保留旋律骨架，处理不可奏音、音区迁移、余韵和句法。
6. 生成减字谱 proposal。
7. 人工审校和回放验证。

当前缺口：

- Arrangement Planner。
- Fingering Search。
- Guqinization Review。
- 人审闭环。
- 与 canon/parser 的双向验证。
- 现代曲版权/来源处理。

为什么本阶段不能宣称已可可靠反推现代曲减字谱：当前成功的是古谱到 audition F，不是现代曲到古琴谱；Track C 需要完全不同的 planning/search/review stack。

## 8. 三目标覆盖判断

### 8.1 新古谱 -> 补录 -> F

判断：MVP 级可以覆盖。

依据：

- XWC/Baiya 已从 recording plan、R0/R1/R2、ABCD、E 到 F 完成一次闭环。
- authority gates 已明确：R2 latest JSON canonical、CSV/YAML derived。
- wrong take / tail policy / R0 root-scope 关键坑已有工程化防护。

下一步：第二首小曲应验证。

缺口：

- OCR 自动化。
- coverage diff 工程化。
- recording plan 从 Dapu Event IR 自动生成仍需参数化。
- ABCD/E/F 脚本需去 XWC hardcode。

### 8.2 三曼数字化 / ML 输入

判断：可以开始积累有效 ML-ready candidates，但不能直接训练。

依据：

- Track A 产物包含 score_event、source_take、R1/R2/human preference 的组合证据。
- wrong take 和 context-only 排除规则已经被实践证明必要。

缺口：

- sample ingest schema。
- `sample_assets.csv`。
- `recording_segments.csv`。
- 跨曲目数据量。
- 质量门禁。
- negative labels 和 preference labels 的一致 contract。

### 8.3 现代曲 -> 古琴减字谱

判断：当前只能覆盖 future design，不能生产级使用。

缺口：

- Arrangement Planner。
- Fingering Search。
- Guqinization Review。
- 人审闭环。
- 现代输入格式到 guqin score proposal 的 validation stack。

## 9. Workflow Skill 结构草案

```markdown
---
name: cyber_guqin_mvp_workflow
description: Use when running or auditing the Cyber Guqin MVP workflow from new dapu score intake through recording review, experimental render, E/F human audition acceptance, and future data-candidate gates.
---

# Cyber Guqin MVP Workflow

## Purpose
...

## When to use
...

## Upstream skills
- guqin-canon-builder
- guqin-dapu-parser

## Track A: Dapu Mode
...

## Track B: Qinist Digitalization
...

## Track C: Arrangement Mode
...

## Phase gates
...

## Authority gates
...

## Script registry
...

## Human review gates
...

## Stop rules
...

## Forbidden authority
...

## What must be engineered instead of remembered by skill
...

## What remains future work
...
```

## 10. Phase Gates

| Gate | Rule |
| --- | --- |
| score gate | Do not proceed until score facts, source evidence, and needs_review are explicit. |
| canon gate | Unknown fingering/alias must go through canon-builder. |
| parser gate | Concrete score tokens must go through dapu-parser. |
| recording plan gate | Human approves take plan, batch ranges, context takes, tail rules. |
| R0 gate | Human accepted raw markers; root/scope identity stable. |
| R1 gate | Human accepted split markers/QC; tail policy explicit. |
| R2 gate | latest JSON is canonical; derived outputs guarded. |
| E gate | E generated only from canonical latest and human/GPT co-review. |
| F gate | F generated only from latest JSON/input snapshot and user acceptance criteria. |
| sample ingest gate | F pass alone is insufficient; requires schema and candidate review. |
| second-piece gate | Do not run hardcoded XWC scripts. |

## 11. Authority Gates

Canonical:

- score/canon authority for score facts。
- active R0/R1 draft JSON for current UI state。
- R2 `r2_review_state.latest.json` for current review state。
- F input snapshot for generated F provenance。

Derived / audit:

- R0/R1 CSV exports。
- R2 latest CSV/YAML。
- reports。
- archive copies。

Forbidden authority:

- Downloads。
- browser Blob downloads。
- restore zip。
- old exports。
- archived old exports as current truth。
- raw audio binary contents unless a task explicitly allows audio processing。

## 12. Script Registry

The workflow skill should maintain a registry but not execute scripts blindly.

Required registry metadata:

- path。
- phase。
- classification。
- input authority。
- outputs。
- default mode。
- hardcoded hazards。
- whether reads/writes audio。
- whether modifies review data。
- whether generates render。
- preflight command。
- human approval requirement。

Initial key entries:

- `scripts/generate_baiya_recording_plan.py`: `reusable_after_parameterization`。
- `scripts/render_xwc_abcd_from_planning.py`: `reusable_after_parameterization`, high-risk render writer。
- `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py`: `reusable_after_parameterization`, current XWC historical。
- `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py`: `historical_only`。
- `tools/cg-varw/backend/scripts/verify_r2_canonical_draft.py`: reusable after render-root parameterization。

## 13. Human Review Gates

- Unknown notation review。
- Recording plan review。
- R0 marker acceptance。
- R1 segment/QC acceptance。
- R2 phrase/version review。
- ABCD listening review。
- E listening review。
- F acceptance。
- Sample ingest candidate review。
- Arrangement proposal review。

## 14. Stop Rules

Stop and ask or write dry-run report when:

- User says “不要猜” or ambiguity affects metadata identity。
- A script is hardcoded to a different piece/session/qinist。
- Current state could be Downloads/restore zip/browser Blob。
- A task would write audio/render/review/sample files outside allowed paths。
- A minor listening issue might trigger G/F2 without explicit approval。
- Any path suggests auth/token/credential/secret/.env。
- The work starts drifting into sample ingest, ML, Arrangement Mode, cleanup, archive/delete, or second piece without authorization。

## 15. What Must Be Engineered Instead of Remembered by Skill

- R0 root/scope and file_id compatibility。
- R2 canonical/derived guard。
- full_tail natural_decay default。
- export manifest/hash/reload validation。
- script parameterization and dry-run default。
- coverage diff。
- sample ingest schema validation。
- automated wrong-take exclusion checks。

## 16. What Remains Future Work

- Generate real `SKILL.md` after user approval。
- Parameterize XWC/Baiya scripts。
- Build generic recording plan generator from Dapu Event IR。
- Build generic ABCD render template。
- Build generic final reviewed render generator。
- Add sample ingest gate and schema。
- Add cross-piece candidate database。
- Build Arrangement Planner / Fingering Search / Guqinization Review。

## 17. Next Recommendation

建议下一步进入真正 `cyber_guqin_mvp_workflow` skill 文件生成，但仍不进入第二首、不跑脚本。再下一步进入脚本工程化。最后再以第二首小曲验证 Track A 的最小闭环，并把 Track B 只作为候选数据积累，不训练 ML；Track C 只保留 future design。
