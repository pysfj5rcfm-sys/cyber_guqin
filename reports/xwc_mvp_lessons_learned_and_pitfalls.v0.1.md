# XWC MVP Lessons Learned and Pitfalls v0.1

- Task: `CG-XWC-MVP-P1D_PROCESS_PLAYBOOK_LESSONS_SCRIPT_AUDIT_AND_WORKFLOW_SKILL_DESIGN`
- Phase: `Phase 1F-XWC-MVP Passed / Sweep & Review`
- Mode: documentation-only retrospective.

## 0. 本轮执行声明

本轮未 patch，未改代码，未改数据，未跑 render，未生成 G/F2，未进入 sample ingest，未生成真正 skill 文件，未处理 `scripts/generate_baiya_recording_plan.py`。本文只沉淀《仙翁操》白牙 MVP 的经验、坑和 guardrails。

## 1. 核心结论

《仙翁操》白牙 MVP 证明 Track A 的 Dapu audition route 可以闭环到 `F_FINAL_REVIEWED`，但这个闭环成立的前提是严格区分 authority、derived output、human decision 和 engineering guard。最重要的经验不是“多 patch”，而是把每一步的权威输入、禁读路径、禁写路径、人审点写清楚。

当前路线应保持：不要继续一口气做 R012 总重构；不要把 F pass 推进为 sample ingest / ML；先固化 workflow，再做最小脚本工程化，再用第二首小曲验证。

## 2. 具体坑与教训

### 2.1 T008 错误 take

现象：早期 E 曾在 `XWC_P02_N03` 使用 `T008`。T008 原始标注目标是“散挑六” / `SAN_TIAO_6`，但实际白牙演奏为“散挑七”。用户已将 T008 置为排除单元。

教训：

- event-level source identity 必须在最终接受前复核。
- wrong take 不能靠“听起来相近”或上下文猜测替代。
- replacement 必须写 provenance：当前 E/F 使用 `T014 exact SAN_TIAO_6`。
- wrong take 可以保留为 audit evidence，但不得继续进入 current render。

已解决方式：E/F validation 中加入 T008 exclusion；`XWC_P02_N03` 明确使用 `T014`。

### 2.2 P02 语义误解

P02 的用户语义是 `12345——6——`：前五音相对连贯，末音延展，不是六音均分，也不是机械等距。

教训：

- 用户的数字节奏备注是 phrase-level timing intent，不是 raw event 重排命令。
- 后续第二首中，类似“同第2句”的备注必须展开成明确 timing policy，不能自动复制为代码 hardcode。

### 2.3 P09 语义误解

P09 的核心问题是 context take overused。E/F 中需要避免把带上下文的掐起和上下文连接误当作两个上下文音。

教训：

- `T060` / `T071` 是 context candidates，不是 atomic sample 的普通替代。
- P09 的修复是 sample selection / context identity 问题，不是 T008-safe 问题。
- F 中“P09 同第1句”只继承 P01 类 timing 修订，不绑定 T008。

### 2.4 上七九小瑕疵

用户最终确认“F通过，除了上七九的一点点小瑕疵”。该问题应记录为 low-severity residual listening note。

处理原则：

- 不自动重开 G/F2。
- 不重做 F。
- 不进入 full R012 governance。
- 后续如用户要求，可另开窄任务，明确是否只修听感、是否允许 render、是否保留 current F 作为 accepted baseline。

### 2.5 R2 latest JSON vs CSV/YAML 混淆

现象：`r2_review_drafts/latest/` 中同时存在 canonical latest JSON 和 8 个 CSV/YAML。早期容易把 CSV/YAML 当 current authority。

教训：

- current authority 是 `r2_review_state.latest.json`。
- CSV/YAML 是 derived output，供阅读、审计和报告使用。
- restore-from-export 必须是显式 migration/promote，不得作为普通 load。
- Downloads、browser Blob、restore zip、old exports 不能作为 current state。

已工程化解决：P1-B R2 canonical/derived guard 增加 manifest/hash/reload/provenance 字段，标明 `derived_export_only=true`。

### 2.6 R0 raw_root / file_id / include scope 混淆

现象：R0 draft/export 的 `file_id` 依赖相对 `CG_VARW_RAW_ROOT` 的 POSIX 路径。把 root 指到 session `raw/` 目录会生成短 ID，无法匹配既有 draft/export。

教训：

- `CG_VARW_RAW_ROOT` 是 identity boundary。
- `CG_VARW_RAW_INCLUDE_PREFIX` 只是 discovery filter，不参与 `file_id`。
- wide root + include prefix 才能同时保持 ID 兼容和 UI 列表收窄。

已工程化解决：P0-B R0 include prefix patch。

### 2.7 full_tail / smart_fade 默认值问题

现象：旧默认 `smart_fade_100ms` 对古琴尾音不合适，F 初版有尾音截断感。

教训：

- 古琴自然尾音是 musical content，不是可随意裁掉的 noise。
- `full_tail` / natural decay 应为古琴默认。
- smart fade 只能是显式 override 或 click-safe 非破坏性处理。
- tail policy 的工程默认应在 schema/test 层解决，不靠 agent 记忆。

已工程化解决：P1-C full_tail / natural_decay 默认策略。

### 2.8 render_set_id 命名债务

当前 render set ID 如 `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e` 强绑定 XWC/Baiya/ABCD。它对当前历史可追溯有价值，但不是第二首的通用命名规范。

建议：

- 第二首前定义 `{piece_id}_{session_id}_{stage}_{hash}` 或 manifest-driven naming。
- render_set_id 不应暗含 F/E 状态，也不应替代 manifest。
- 旧 ID 保留历史，不做本轮重命名。

### 2.9 token 消耗教训

高 token 消耗主要来自把多个阶段揉在一起：

- F 生成同时牵涉 latest authority、E/F timing、source selection、audio metadata、R2 export sync、reports。
- full_tail 同时牵涉 R1 policy、preview refresh、F regeneration、validation。
- cleanup/archive 同时牵涉大量路径和 must_keep 分组。

降低成本的方式：

- 每轮先声明 canonical authority。
- 只读 metadata，不读 audio binary。
- 把 render/generate、validate、report sync、archive 分开。
- 对不确定项先做 dry-run report，不直接 patch。

### 2.10 old exports / Downloads / restore zip / browser Blob forbidden authority

这些路径可以是历史证据，但不能是 current authority：

- Downloads。
- browser Blob downloads。
- restore zip。
- archived old exports。
- `r2_review_exports/` 旧导出。
- quarantine/archive 旧副本。

只有在用户明确授权 restore/migration 时，才可读取为显式恢复输入，并必须写 source path、hash、warnings、reviewer、reason。

## 3. 为什么不要一口气做 R012 总重构

R0/R1/R2 共享“review/export/manifest”主题，但它们的业务 identity 完全不同：

- R0 是 raw file + slate/marker identity。
- R1 是 split segment + render anchor identity。
- R2 是 phrase/version review state identity。

一口气总重构会把已通过的 F baseline、R0 recovery、R1 tail policy、R2 latest guard 混在一起，风险大、验证面大、用户听评语义容易被工程抽象吞掉。正确方式是先保留已落地的小 guard，再用第二首暴露真实复用点，最后抽共享 manifest/script registry。

## 4. 为什么 sample ingest / ML 需要 gating review

F pass 只证明 Dapu audition 当前版本可听，不证明每个 segment 都可进样本库。

进入 sample ingest / ML 前至少需要：

- sample ingest schema 明确。
- `sample_assets.csv` 与 `recording_segments.csv` contract 冻结。
- 每个 candidate 有 score_event 对齐、R1/R2/human labels、source_take provenance。
- failed take / wrong take / context-only / retake 排除规则明确。
- qinist realization 与 score facts 分离。
- 跨曲目数据量与质量门禁足够。

当前可以积累 ML-ready candidates 的证据，但不能直接训练。

## 5. 第二首曲子开始前必须遵守的 guardrails

- 不复用 XWC/Baiya hardcoded 脚本作为默认执行入口。
- 新曲必须先确认 score authority 和 canon/parser gate。
- 新曲的 recording plan 不得由 legacy XWC 71-task bridge 生成。
- R0 保持 root/scope 分离。
- R2 latest JSON 为 canonical，CSV/YAML derived。
- 古琴默认 `full_tail`，除非人工显式 override。
- wrong take 必须排除并写 replacement provenance。
- 人耳验收与 sample ingest 分开。
- 不进入 Arrangement Mode。
- 不训练 ML。
- 不处理 REVIEW/DELETE_CANDIDATE cleanup，除非另开任务。

## 6. 哪些防坑已工程化解决

| 防坑 | 已落地方式 | 仍需注意 |
| --- | --- | --- |
| R0 include prefix | `CG_VARW_RAW_INCLUDE_PREFIX` 只过滤 discovery，不改 file_id。 | 新 session 仍需设置正确 wide root。 |
| R2 canonical/derived guard | manifest/hash/reload/provenance 标明 latest JSON primary、CSV/YAML derived-only。 | restore endpoint 仍只能显式使用。 |
| full_tail 默认策略 | 古琴上下文缺失 `tail_policy` 默认 `full_tail`，测试覆盖。 | 显式旧 `smart_fade_100ms` 数据要单独审计，不能自动覆盖。 |

## 7. 哪些防坑仍需流程 gate，而不是继续 patch

| 防坑 | 为什么不继续 patch | Gate |
| --- | --- | --- |
| P02/P09 语义理解 | 属于 musical intent 和用户偏好，不是纯代码规则。 | 人工听评 + report 解释。 |
| 上七九 minor issue | 当前是 accepted F 的 residual note，不是 blocker。 | 用户明确 reopen 才修。 |
| render_set_id 命名债务 | 重命名会污染历史与报告，不影响当前 F。 | 第二首前设计命名规范。 |
| sample ingest / ML | schema、数据量、门禁未完成。 | sample ingest review gate。 |
| Arrangement Mode | 现代曲到减字谱还缺 planner/search/review 闭环。 | future track gate。 |
| 脚本参数化 | 当前 hardcoded 脚本能说明历史，但直接改会扩大范围。 | 先脚本工程化计划，再 patch。 |

## 8. 下一步建议

下一步建议进入 `cyber_guqin_mvp_workflow` 真正 skill 文件生成。再下一步进入脚本工程化，把 XWC/Baiya hardcode 拆成 manifest/config-driven registry。最后进入第二首小曲验证，但应只验证最小 Track A 闭环，不扩展到 sample ingest / ML / Arrangement Mode。
