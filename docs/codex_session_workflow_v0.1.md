# Cyber Guqin Codex Session Workflow v0.1

Status: `trial`

本文是 cyber_guqin 的 Codex 会话管理试运行规范。它不是正式主流程变更，不替代 `README.md`、repo-local skills、runbook、report、测试或人工验收结论。

## 1. 总原则

Codex 会话不是长期记忆。长期记忆必须落在仓库资产中，例如 docs、runbooks、reports、examples、tests、fixtures、manifest、index、handoff 文档或 skill。

会话可以承载短期推理、探索、执行和复核，但不得把聊天上下文当作项目权威。任何会影响后续工作的结论，都应当转写为可审计的仓库文件，并说明来源、范围、验证状态和未决风险。

本规范默认遵守当前仓库边界：

- 不把试运行文档升级为正式项目流程。
- 不把低风险任务强制拆成多 Agent。
- 不把 Codex session handoff 当成事实权威，除非它指向了仓库内的验证资产。
- 不以会话记忆替代 canonical authority、accepted baseline、human review 或 runbook。
- 不借会话切换扩大任务范围，例如进入 sample ingest、ML training、second-piece execution、accepted F rerun 或 Arrangement Mode production。

## 2. 会话命名规则

会话名使用 `CG-<level><suffix> <short task>`。

| Name | Role | Default use |
| --- | --- | --- |
| `CG-L1` | Triage / Scout | 初筛、读仓库、确认边界、给出路线建议 |
| `CG-L2A` | Implementation | 低到中风险实现、文档、测试、轻量验证 |
| `CG-L2B` | Independent Audit | 独立复核实现结果、风险、测试缺口 |
| `CG-L3A` | Authority Inspection | 高风险权威输入、canonical/derived 边界审计 |
| `CG-L3B` | Controlled Implementation | 高风险但已授权的受控实现 |
| `CG-L3C` | High-Risk Audit | 高风险变更后的独立审计与回归检查 |
| `CG-L3D` | Assetization | 把会话结论固化为仓库资产 |

示例：

```text
CG-L1 baiya-r2-export-scope
CG-L2A docs-codex-session-workflow
CG-L3A r2-latest-authority-inspection
```

## 3. CG-L1 Triage / Scout

### 角色说明

`CG-L1` 用于任务开场。它只做范围确认、上下文读取、风险分级、路径建议和最小验证建议。除非任务本身是低风险并且用户已明确要求执行，否则 `CG-L1` 不应直接修改项目资产。

### 适用场景

- 用户给出新目标，但边界、路径或权威输入尚不清楚。
- 需要先确认 repo 当前状态、已有 docs、skills、tests、examples、reports。
- 任务可能跨越主流程、审计、实现、清理、数据或音频资产。

### 开场模板

```markdown
# CG-L1 Triage / Scout

Goal:
- <用户目标>

Scope boundary:
- In scope: <本轮允许做什么>
- Out of scope: <本轮明确不做什么>

Inspection plan:
- Read: README.md, relevant docs, skills, tests, examples, reports index.
- Check: current git status, authority files, existing workflows.

Risk guess:
- <low / medium / high>

Expected output:
- Inspection summary.
- Recommended path.
- Stop conditions.
```

## 4. CG-L2A Implementation

### 角色说明

`CG-L2A` 用于低风险或中风险的受控执行。它可以编辑 docs、tests、small scripts 或 narrow patches，但必须保持 scope narrow，并使用仓库已有模式。

### 适用场景

- 文档新增或局部更新。
- 小范围 bugfix 或 guard patch。
- 已有 runbook/test 指明验证命令。
- 低风险任务不需要强制另开 audit agent。

### 开场模板

```markdown
# CG-L2A Implementation

Goal:
- <要实现的具体结果>

Allowed changes:
- <允许修改的文件/目录/类型>

Forbidden changes:
- <不可触碰的文件/目录/流程>

Inputs:
- <权威输入或参考文档>

Verification:
- <轻量验证命令>

Handoff output:
- Changed files.
- Validation evidence.
- Risks and next step.
```

## 5. CG-L2B Independent Audit

### 角色说明

`CG-L2B` 用于独立审计 `CG-L2A` 的结果。它应优先找 bug、越界、权威误用、测试缺口和文档歧义，而不是重写实现。

### 适用场景

- 中风险变更完成后需要第二视角。
- 低风险任务但用户明确要求 review。
- 文档或代码将被后续工作复用。

### 开场模板

```markdown
# CG-L2B Independent Audit

Audit target:
- <commit/diff/files>

Original scope:
- <用户目标和边界>

Checkpoints:
- Scope compliance.
- Authority/provenance correctness.
- Missing tests or validation.
- User-facing ambiguity.

Output format:
- Findings first, ordered by severity.
- Open questions.
- Residual risk.
```

## 6. CG-L3A Authority Inspection

### 角色说明

`CG-L3A` 用于高风险任务的权威输入审计。它只确认 canonical source、derived export、forbidden authority、accepted baseline、human review state 和 stop rules，不做实现。

### 适用场景

- 涉及 R2 latest JSON、accepted F、review outputs、recording plans、audio assets。
- 可能误把 Downloads、old exports、archive、browser Blob、derived CSV/YAML 当作权威。
- 用户强调“先只读审计”“不要猜”“不要改状态”。

### 开场模板

```markdown
# CG-L3A Authority Inspection

Goal:
- <要判断的权威问题>

Read-only scope:
- <只读文件/目录>

Authority candidates:
- Canonical: <候选>
- Derived: <候选>
- Forbidden: <候选>

Checks:
- Existence.
- Hash/provenance if available.
- Contract/schema fit.
- Stop conditions.

Output:
- Authority decision.
- Evidence paths.
- Do-not-use list.
- Whether implementation may proceed.
```

## 7. CG-L3B Controlled Implementation

### 角色说明

`CG-L3B` 用于高风险但已经过 `CG-L3A` 审计且获得明确授权的实现。它必须小步修改、可回溯、先 dry-run，避免触碰 accepted baseline 或不可逆资产。

### 适用场景

- 需要修改 review state、export guard、render planning、workflow script 或 authority validator。
- 需要写入受控 sandbox。
- 用户明确允许实现，而不是只要审计或设计。

### 开场模板

```markdown
# CG-L3B Controlled Implementation

Authorization:
- <用户授权原文摘要>

Authority inspection:
- <CG-L3A 结论和证据路径>

Allowed writes:
- <明确允许写入的位置>

Protected surfaces:
- <不可触碰路径>

Execution plan:
- Step 1: narrow edit.
- Step 2: smallest relevant verification.
- Step 3: broaden only if needed.

Rollback/stop:
- <发现什么就停止>
```

## 8. CG-L3C High-Risk Audit

### 角色说明

`CG-L3C` 用于高风险实现后的独立审计。它不假设实现正确，应从 authority、scope、diff、tests、runtime outputs 和 protected paths 重新检查。

### 适用场景

- 高风险实现已完成。
- 有写入 canonical state、review exports、render outputs、recording metadata 或 workflow scripts 的可能。
- 需要确认没有扩大到 sample ingest、ML、second piece 或 accepted baseline overwrite。

### 开场模板

```markdown
# CG-L3C High-Risk Audit

Audit target:
- <diff/files/output directories>

Expected allowed writes:
- <来自 CG-L3B 的 allowed writes>

Protected surfaces:
- <必须确认未触碰的路径>

Checks:
- Git diff scope.
- Contract/schema validation.
- Dry-run or test evidence.
- Output path containment.
- Forbidden authority scan.

Output:
- PASS/FAIL.
- Findings.
- Residual risk.
- Required assetization.
```

## 9. CG-L3D Assetization

### 角色说明

`CG-L3D` 用于把会话成果固化为仓库资产。它不应重新发明主流程，而应把已验证的规则、模板、命令、pitfalls、handoff 和边界写入合适位置。

### 适用场景

- 会话中形成了可复用 workflow。
- 需要把临时结论转为 docs/runbooks/reports/examples/tests。
- 需要为后续 Codex 或人工操作者留下可验证入口。

### 开场模板

```markdown
# CG-L3D Assetization

Source sessions:
- <相关会话/任务摘要，不复制聊天全文>

Assets to create/update:
- <docs/runbooks/reports/examples/tests>

What becomes durable:
- <规则/命令/模板/边界>

What stays non-authority:
- <会话推理/未验证假设/草案>

Validation:
- Markdown/lint/checks.
- Link/path checks if applicable.

Output:
- Changed files.
- How to use the new asset.
- Remaining gaps.
```

## 10. Rollover / Handoff

### 触发条件

出现以下任一情况，应写 handoff，而不是依赖当前会话继续记忆：

- 会话接近上下文上限，或已经发生摘要压缩。
- 任务从 inspection 转为 implementation、从 implementation 转为 audit、从 audit 转为 assetization。
- 风险等级从低/中升为高。
- 发现 authority ambiguity、protected path、dirty worktree、未验证输出或用户未授权的写入需求。
- 需要另一个会话独立复核。
- 任务会暂停，后续需要别人继续。
- 任何结论会影响后续仓库操作。

### Handoff 模板

```markdown
# Codex Handoff

Session:
- Name: CG-<level> <short task>
- Date: YYYY-MM-DD
- Status: in_progress | blocked | ready_for_audit | complete

User goal:
- <用户目标>

Scope:
- In scope:
- Out of scope:

Current repo state:
- Branch:
- Git status summary:
- Dirty files relevant to task:
- Dirty files ignored as unrelated:

Authority and evidence:
- Canonical inputs:
- Derived/reference inputs:
- Forbidden inputs:
- Evidence files:

Work completed:
- <事实，不写隐藏推理>

Validation run:
- Command:
- Result:

Risks:
- <剩余风险>

Stop rules:
- <下一会话必须停止的条件>

Next recommended action:
- <一个明确下一步>
```

## 11. 风险分级规则

### 低风险

低风险任务通常可以由单个 `CG-L2A` 会话完成，不应强制多 Agent。

常见低风险范围：

- 新增或更新非权威 docs。
- 更新索引、说明文字、模板或 README 中的小范围引用。
- 只读 inspection summary。
- 不改变 runtime behavior 的文字修正。
- 运行 `git diff --check`、markdown lint、unit-level read-only checks。

低风险 stop rules：

- 发现需要修改 canonical state、review outputs、accepted baseline、audio/data assets。
- 发现用户未授权的正式流程变更。
- 发现 task scope 依赖缺失权威判断。

### 中风险

中风险任务通常由 `CG-L2A` 执行，并可按需使用 `CG-L2B` 独立审计。

常见中风险范围：

- 小范围脚本、validator、frontend/backend guard patch。
- 新增或调整 tests/fixtures/examples。
- 修改 docs/runbooks 中的可执行命令。
- 更新 workflow-adjacent 文档，但不改正式 skill。

中风险 stop rules：

- 变更会写入 review state、render outputs、recording metadata、sample metadata。
- 需要真实音频读写。
- 需要从 derived export 推回 canonical authority。
- 需要触碰 protected historical template 或 accepted baseline。

### 高风险

高风险任务必须先用 `CG-L3A` 做 authority inspection，再决定是否进入 `CG-L3B`。实现后建议使用 `CG-L3C`，并用 `CG-L3D` 固化结论。

常见高风险范围：

- 修改 canonical authority、latest JSON、review outputs、accepted F、recording/session metadata。
- 生成或覆盖 render/audio/alignment artifacts。
- 进入 sample ingest、ML training、Arrangement Mode、second-piece execution。
- 恢复、迁移、清理、归档大量文件。
- 使用 Downloads、archive、browser Blob、old exports 等存在 authority 风险的来源。
- 任何用户明确要求“不要猜”“先只读审计”“不要改状态”的任务。

高风险 stop rules：

- authority 不清楚。
- 写入路径不是明确授权的 sandbox。
- 验证命令准备触碰 protected surface。
- 任务需要正式流程变更，但当前只授权试运行或文档草案。

## 12. 低风险任务不过载原则

低风险任务不应强制多 Agent，不应自动升级为 L3 流程，也不应为了形式完整而要求额外 handoff、audit 或 assetization。

推荐默认：

- 单文件 docs 变更：`CG-L2A` 即可。
- 小范围文字或索引修正：`CG-L2A` 即可。
- 用户只要 inspection：`CG-L1` 即可。
- 用户明确要独立 review，或变更会被后续复用：再加入 `CG-L2B`。

流程的目标是降低风险，不是增加仪式。只要任务边界清楚、写入面小、验证直接、没有 authority 争议，就保持轻量。
