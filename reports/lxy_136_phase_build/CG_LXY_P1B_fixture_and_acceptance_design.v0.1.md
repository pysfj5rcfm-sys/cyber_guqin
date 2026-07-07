# CG-LXY P1-B Fixture and Acceptance Design v0.1

Status labels:

- P1B_FIXTURE_DESIGN_DRAFT
- NEEDS_USER_REVIEW
- NOT_EXECUTABLE_TEST
- NOT_PARSER_IMPLEMENTATION
- NOT_RUNTIME_SCHEMA
- NOT_REPO_CONTRACT
- NOT_CANON_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA
- NOT_RENDER_OUTPUT

## 1. P1-B 目标与非目标

P1-B 为 Phase 1 Grammar Parser MVP 的实现前准备层。它只定义 mock fixtures、sanitized real-ID fixtures、D3A guard-action fixtures、deterministic ranking fixtures，以及一张 case-level acceptance matrix。

本轮不实现 parser，不新增 Python parser，不新增 Python test，不运行 pytest/unittest，不读取谱图、不做 glyph transcription、不生成 Dapu IR、不修改 skill、D1、D2、D3 或既有 fixture。

## 2. 与 P1-A / P1-C 的边界

P1-A 是已锁定合同：`structured_parse` 为主输出，`surface_reading_candidate` 仅为派生显示，`literal_component_gloss` 保留原始构件释读，`implicit_backward_scan_depth=0`，D3A 使用六级 action enum，abstract 与 sanitized real-ID 双轨并行。

P1-B 只把这些合同转成验收输入和验收矩阵。P1-C 才可以在用户审查 P1-B 后决定是否实现 parser 代码。P1-B 文件不得被当成 runtime schema 或 production test result。

## 3. Fixture Schema

四个 fixture JSON 顶层统一包含：

- `fixture_schema_id`
- `version`
- `fixture_class`
- `phase`
- `source_contracts`
- `status_labels`
- `anti_oracle_boundary`
- `authority_boundary`
- `cases`

每个 case 统一包含任务要求的 case 字段，包括输入 tokens、context input、expected parse status、candidate policy、primary rule ids、slot bindings、consumed/unconsumed token assertions、sound type assertions、guard actions、rank assertions、structured parse assertions、surface assertion、forbidden outcomes、authority flags 和 notes。

`input_tokens` 保留 token 层事实，不在 `metadata` 中藏入最终 slot 答案。数字 token 在输入阶段不预标为徽位或弦数；semantic slot 只出现在 expected parse assertion。

## 4. Abstract Fixture 设计

`p1b_abstract_grammar_fixtures.v0.1.json` 使用稳定 abstract component IDs，覆盖 grammar contract 本身。

它覆盖：

- input contract validation：empty input、missing required token field、duplicate token id、duplicate sequence index、invalid sequence index、malformed component ID、invalid lexical type、invalid field type；
- 11 个 production family；
- 11 个 parser status；
- RH_ACTION + STRING_NUMBER 的 no context / no inherited context / explicit open state / inherited context / context missing 分支；
- explicit-context-only：合法 context、incompatible context、implicit history request、previous-unit scan request、context required but missing；
- pre/post motion host attachment；
- state/timing/generic marker 的 non-sounding 约束；
- special technique 的 attachment 与 sound-type 边界；
- PR-UNKNOWN fallback-only 约束。

## 5. Sanitized Real-ID Fixture 设计

`p1b_sanitized_real_id_fixtures.v0.1.json` 只使用 v0.2 registry 中真实存在的 primary IDs。legacy/source IDs 只出现在 trace 字段。

覆盖类别：

- numeric：`COMP-081`, `COMP-084`, `COMP-086`, `COMP-087`
- left finger：`COMP-091`
- right-hand action：`COMP-103`, `COMP-116`
- left-hand action / position transition：`COMP-426`, `COMP-527`
- state marker：`COMP-705`, `COMP-707`, `COMP-708`
- timing marker：`COMP-806`
- generic marker：`COMP-906`
- special technique：`COMP-515`

Normalization 覆盖：

- primary v0.2 input；
- legacy alias normalization；
- source v0.1 normalization；
- explicit normalization gap。

每个 real-ID surface assertion 都标记 `surface_assertion_scope=LOCAL_NOTATION_UNIT_ONLY` 和 `not_phrase_oracle=true`。

## 6. Guard Fixture 设计

`p1b_guard_action_fixtures.v0.1.json` 覆盖六个 D3A action，每个 action 至少两个 case：

- HARD_REJECT
- SOFT_PENALTY
- FORCE_UNRESOLVED
- NEEDS_CONTEXT
- NEEDS_HUMAN_REVIEW
- NOT_APPLICABLE

Guard fixture 明确区分：

- impossible lexical-type / slot binding；
- marker-as-sounding；
- scoped forbidden parse；
- same literal but scope mismatch；
- known confusable component with legal interpretation；
- evidence conflict；
- missing context；
- human review required only。

`scope mismatch -> NOT_APPLICABLE` 是显式验收点。`forbidden_output` 不是全局字符串黑名单。

## 7. Ranking Fixture 设计

`p1b_deterministic_ranking_fixtures.v0.1.json` 覆盖八个 deterministic ordering criterion：

1. invalid / hard-rejected 不进入 accepted candidate；
2. required slot completeness；
3. specificity；
4. fewer context dependencies；
5. fewer unresolved items；
6. higher consumed-token coverage；
7. production priority；
8. candidate_id deterministic tie-break。

每个 ranking case 声明 `score_type=HEURISTIC_GRAMMAR_SCORE`，`calibrated_probability=false`。排序不能依赖浮点微小差异。

## 8. Acceptance Matrix 说明

`CG_LXY_P1B_acceptance_matrix.v0.1.csv` 一行对应一个 fixture case。矩阵用于从 case_id 检索：

- fixture 文件和类别；
- production rule；
- lexical pattern；
- normalization mode；
- context mode；
- expected status；
- guard action；
- rank order；
- consumed/unconsumed token assertion；
- sound type assertion；
- invalid matrix references；
- oracle-free 与 authority boundary。

矩阵 case 数必须等于四个 fixture JSON 的 case 总数，每个 case_id 精确出现一次。

## 9. Coverage Strategy

总 case 数为 75：

- abstract grammar：43
- sanitized real-ID：12
- guard action：12
- deterministic ranking：8

覆盖目标：

- production family：11/11；
- parser status：11/11；
- guard action：6/6，每个至少两个；
- ranking criterion：8/8；
- P1-A invalid matrix：24/24；
- explicit context/no context/incompatible context；
- partial consumption 与 unconsumed token；
- authority flags。

## 10. Normalization Strategy

P1-B fixtures 将 component identity 分为四类：

- `NORMALIZED_V0_2_PRIMARY`：primary ID already present；
- `NORMALIZED_FROM_LEGACY_ID`：legacy alias normalized before parse；
- `NORMALIZED_FROM_SOURCE_V0_1_ID`：source v0.1 ID normalized before parse；
- `COMPONENT_ID_NORMALIZATION_GAP`：不得伪造 mapping，必须停止在 normalization gap status。

Legacy/source IDs 不得进入 primary slot。它们只用于 trace。

## 11. Anti-Overfit Strategy

Abstract fixtures 不绑定任何真实曲目。Real-ID fixtures 只使用 single notation-unit grammar reading 和 local slot assertions。同一 production 不只使用一套 component IDs；real fixture 分散覆盖 right-hand、left-hand、state、timing、generic、special、numeric 与 transition 类别。

Ranking fixtures 使用 pairwise / small-set 合成候选，不靠曲目答案或浮点微差。

## 12. Anti-Oracle Leakage Strategy

P1-B 未读取 D3B goldset，未读取旧候选/答案/triage 报告，未读取谱图、crop、runtime outputs、archive 或外部聊天导出。

D2 只使用 generation-safe 字段：`template_id`, `reading_pattern`, `slot_semantics`, `component_sequence`, `sound_policy`, `context_inheritance_policy`, `needs_review`, `authority_boundary`, `primary_id_system`。

D3A 只使用 generation-safe 字段：`case_id`, scoped component/label fields, forbidden literal, reason, expected guard, allowed elsewhere, boundary, evaluation rule, primary component refs。

Surface assertions 全部为 local notation-unit scope，不是完整曲目答案。

## 13. Surface Assertion 边界

`surface_reading_candidate` 只能由 `structured_parse` 派生，不能覆盖 slot。Real-ID fixture 的 surface assertion 均标记：

- `surface_assertion_scope: LOCAL_NOTATION_UNIT_ONLY`
- `not_phrase_oracle: true`

Abstract fixture 使用 `ABSTRACT_LOCAL_NOTATION_UNIT_ONLY` 或 `NONE`。

## 14. Invalid Matrix Traceability

P1-A invalid matrix 24 行全部被 fixture case 引用。引用集中在 abstract fixture，并由 guard/matrix 补充验证 scoped guard 与 numeric cluster 行为。

Traceability rule：

- schema-level failures -> `INPUT_CONTRACT_INVALID`；
- order failure -> `INVALID_ORDER`；
- non-sounding marker mixed into sounding slots -> `INVALID_TYPE_COMBINATION` 或 guard hard reject；
- context required but missing -> `INCOMPLETE`；
- identity gap -> `COMPONENT_ID_NORMALIZATION_GAP`；
- scoped hard guard -> `FORBIDDEN_GUARD_REJECTED`。

## 15. Authority Boundary

P1-B 产物不是谱面事实，不是正确答案，不是 canon authority，不是 Dapu IR authority，不是 runtime schema，不是 repo contract，不是 production test result，不是 ML training data，不是 render output。

P1-B fixture 可作为 P1-C parser 的实现与测试输入草案，但 P1-C 仍需用户审查授权。

## 16. P1-C Handoff

P1-C parser implementation 应先通过本轮设计审查，再选择是否把这些 JSON fixture 转换成 executable tests。

P1-C 必须实现：

- schema-level input validation；
- D1 normalization；
- P1-A production matching；
- explicit-context-only；
- scoped D3A guard actions；
- deterministic n-best ordering；
- structured_parse primary output；
- derived surface_reading_candidate；
- literal_component_gloss preservation。

## 17. Unresolved Issues

`unresolved_user_decisions = []`

当前 P1-B 未保留阻塞 P1-C design review 的用户决策项。

## 18. User Decisions Required

`unresolved_user_decisions = []`

用户下一步只需决定是否接受 P1-B fixture/matrix 作为 P1-C implementation design input。P1-C code 仍未授权。
