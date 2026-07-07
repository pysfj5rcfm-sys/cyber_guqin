# 赛博古琴 · 良宵引读谱系统 1-3-6 Phase 建设需求文档 v0.1

> 文档状态：设计需求 / Codex 开工前上下文统一稿  
> 项目：赛博古琴 / Cyber Guqin v1.0  
> 子任务：LXY / 《良宵引》读谱 skill 系统化升级  
> 版本：CG-LXY-136-PHASE-BUILD-REQUIREMENTS-v0.1  
> 当前定位：不是 Codex 执行提示词，不要求立即写代码；用于让 Codex 先理解整套系统边界、资产分层、Phase 顺序与验收口径。

---

## 0. 总结：什么是 1-3-6

本设计将《良宵引》读谱系统重构为一个 **1 个读谱 Skill、3 层沉淀物、6 个工程 Phase** 的可执行体系。

```text
1 Skill：cyber_guqin_component_guided_transcription
3 Deposits：
  D1 Component Reference Layer / 构件参考层
  D2 Construction Grammar Layer / 构形语法层
  D3 Regression Guard & Oracle Layer / 回归护栏与评估层
6 Phases：
  P1 Grammar Parser MVP
  P2 Visual Component Candidate Layer
  P3 Parser + Lattice
  P4 Line-level Context
  P5 Phrase-level Reconstruction
  P6 Human Review as Active Learning
```

核心原则：

```text
禁止答案，不禁止技能。
禁止旧 reports，不禁止三层沉淀。
生成端可以读构件、模板、护栏；不能读 phrase-level oracle。
评估端可以读 oracle；不能回写 prediction。
人审不是长期代读，而是 active learning 的增量校正机制。
```

---

## 1. 背景与问题定义

### 1.1 已发现的问题

此前多轮 P1–P6 / line01 实验暴露了一个根本问题：

```text
LLM/Codex 直接看谱图 + prompt 读谱，在无答案、无旧 reports 的条件下，不稳定。
```

具体失败模式包括：

- 裸眼盲读时无法稳定识别减字构件；
- no-answer runtime pack 过度切断三层沉淀，导致 skill 能力被剥离；
- 直接读整行图时，visual block、notation unit、component、construction、phrase boundary 混成一个任务；
- P1–P6 goldset 作为完整 oracle 泄题，不能直接给生成端读取；
- reports 中混有历史候选、人审痕迹和答案，不能作为生成端依据；
- 当前三层沉淀仍偏“资料层”，需要升级为可执行 parser / detector / scorer。

### 1.2 目标方向

不接受长期“人给答案，Codex 解释答案”的模式。长期路线必须是：

```text
有限构件集
+ 构形语法
+ 视觉空间约束
+ candidate lattice / beam search
+ n-best parse
+ 人审只校正失败样本
+ 失败样本反哺三层沉淀
```

---

## 2. 权威边界与红线

### 2.1 本系统的输出边界

所有读谱输出在本阶段都必须保持：

```text
GPT_TRANSCRIPTION_DRAFT
REFERENCE_COMPONENT_ATLAS_GUIDED
NOT_REPO_CONTRACT
NEEDS_HUMAN_REVIEW
NOT_DAPU_IR_AUTHORITY
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

### 2.2 严禁事项

本 1-3-6 系统建设阶段严禁：

```text
直接生成 Dapu IR authority
直接进入 01_pieces production facts
直接生成三曼采集清单
直接写 sample_assets.csv
直接写 recording_segments.csv
直接写 recording_items_enriched.jsonl
进入 R0/R1/R2/E/F
render
sample ingest
ML training
重跑或覆盖 XWC accepted F
把白牙数据计入三曼 inventory
把 score facts 与 qinist realization 混写
```

---

## 3. 1 Skill：读谱 Skill 的角色

### 3.1 Skill 名称

```text
cyber_guqin_component_guided_transcription
```

### 3.2 Skill 不是单个 prompt

它应被理解为一次读谱任务的 runtime orchestrator，负责串联：

```text
输入判定
→ 三层沉淀加载
→ visual block segmentation
→ notation unit decomposition
→ component candidate matching
→ construction grammar parse
→ regression / forbidden guard check
→ context handling
→ coverage ledger
→ draft output
→ evaluation handoff
→ active learning handoff
```

### 3.3 Skill 的三种运行模式

#### A. Generation Mode / 生成模式

生成 candidate，不得读取 phrase-level oracle。

允许读：D1、D2、D3 的 generation-safe guard 部分。  
禁止读：goldset expected reading、旧 reports、旧候选、evaluation / triage oracle。

#### B. Evaluation Mode / 评估模式

评估 frozen prediction，可以读取 goldset oracle。

允许读：prediction + goldset + forbidden fixture。  
禁止做：修改 prediction、补写 candidate、用 reports 修答案。

#### C. Learning Mode / 学习沉淀模式

在人审后，把纠正转化为：

```text
新增 / 修正 component exemplar
新增 / 修正 alias
新增 / 修正 construction grammar
新增 forbidden parse
新增 regression fixture
新增 boundary rule
```

---

## 4. 3 Deposits：三层沉淀物

## D1. Component Reference Layer / 构件参考层

### 真实资产位置

```text
references/qxby_component_atlas/component_registry.reindexed.v0.2.json
references/qxby_component_atlas/component_legacy_alias_map.reindexed.v0.2.json
references/qxby_component_atlas/component_to_canon_crosswalk.seed.reindexed.v0.2.json
sources/qxby_component_atlas/images/
```

### 作用

回答：

```text
这个局部字形可能是什么构件？
```

输出候选：

```text
component_id
label_zh
component_family
category_range
source_image_path
visual_similarity
confidence
```

### 不回答

```text
这一整句怎么读？
这个 event 是否进 Dapu IR？
这是最终 score fact 吗？
```

---

## D2. Construction Grammar Layer / 构形语法层

### 真实资产位置

```text
references/qxby_component_atlas/construction_templates.reindexed.v0.2.json
```

### 作用

回答：

```text
这些构件按这种空间关系组合起来，可能是什么减字谱构式？
```

从 template 升级为 grammar production，例如：

```text
RH_ACTION + STRING_NO → open_or_inherited_sounding_unit
LEFT_FINGER + HUI_POS + RH_ACTION + STRING_NO → pressed_sounding_unit
STATE_START + unit* + STATE_END → state_span
MOTION_PREFIX + pressed_unit → ornamented_attack
sounding_unit + MOTION_SUFFIX → post_sound_motion
TIMING_MARKER → non_sounding_timing_marker
```

### 注意

这一层不是答案库，而是 grammar / construction rules。

---

## D3. Regression Guard & Oracle Layer / 回归护栏与评估层

### 真实资产位置

```text
tests/fixtures/cyber_guqin/component_guided_transcription/lxy_p1_p6_goldset.reindexed.v0.2.json
tests/fixtures/cyber_guqin/component_guided_transcription/lxy_p1_p6_forbidden_outputs.reindexed.v0.2.json
```

### 必须拆成两部分

#### D3A. Generation-safe Guards / 生成期可读护栏

允许生成端读取：

```text
component_match_cases
construction_template_cases
forbidden_output scoped guards
must_not_read_as
component-level known failure guards
construction-level known failure guards
```

#### D3B. Oracle Answers / 评估期 oracle

只能评估端读取：

```text
expected_continuous_reading
must_include
phrase_integration_cases
source_report
old phrase report refs
```

### 核心原则

```text
D3 不是整体禁读，也不是整体可读。
生成期只读 guards。
评估期才读 oracle。
```

---

## 5. 三层沉淀物与 6 Phases 的关系

| Phase | 目标 | D1 构件层 | D2 语法层 | D3 回归层 | 是否碰图 | 主要产物 |
|---|---|---|---|---|---|---|
| P1 Grammar Parser MVP | 已知 component sequence → legal parse | 读 ID / category | 核心使用 | guards only | 否 | parser rules / parse candidates |
| P2 Visual Component Candidate | 图像区域 → component top-k | 核心使用，含 images | 弱使用或不用 | 不用 | 是 | component candidate lattice |
| P3 Parser + Lattice | top-k 构件候选 → n-best legal readings | 使用 | 核心使用 | guards only | 可选 | n-best parse / rejected parse |
| P4 Line-level Context | 一行图 → units + per-unit parses | 使用 | 使用 | guards only | 是 | line unit stream / coverage ledger |
| P5 Phrase-level Reconstruction | units → phrase candidates | 使用 | 使用 span/context grammar | generation guards；evaluation oracle | 是 | phrase candidates / boundary candidates |
| P6 Active Learning | 人审反哺系统 | 新增/修正 | 新增/修正 | 新增 gold/forbidden | 可选 | updated proposals / fixtures |

---

## 6. Phase 1：Grammar Parser MVP

### 6.1 目标

先不碰图片，只验证：

```text
给定已知 component sequence，系统能否解析成合法减字谱读法？
```

### 6.2 输入

```json
[
  {"component_id": "COMP-093", "label_zh": "中指"},
  {"component_id": "COMP-087", "label_zh": "七"},
  {"component_id": "COMP-103", "label_zh": "勾"},
  {"component_id": "COMP-081", "label_zh": "一"}
]
```

### 6.3 输出

```json
{
  "parse_candidates": [
    {
      "reading": "中指七徽勾一",
      "parse_type": "pressed_sounding_unit",
      "slots": {
        "left_finger": "中指",
        "hui": "七徽",
        "right_hand_action": "勾",
        "string": "一弦"
      },
      "confidence": 0.91
    }
  ]
}
```

### 6.4 验收

- 基础 RH_ACTION + STRING_NO 可 parse；
- LEFT_FINGER + HUI + RH_ACTION + STRING_NO 可 parse；
- STATE_START / STATE_END / TIMING_MARKER 可分类；
- 绰 / 注 / 上 / 下 能按前后动作位置分类；
- 非法组合能拒绝；
- 每个 parse 输出 slots、reason、confidence。

---

## 7. Phase 2：Visual Component Candidate Layer

### 7.1 目标

开始碰图片，但不直接读成谱。只做：

```text
局部图像区域 → component top-k candidate lattice
```

### 7.2 输入

```text
single_component_crop
glyph sub-region
visual block crop
```

### 7.3 输出

```json
{
  "visual_block_id": "B001",
  "bbox": [0, 0, 80, 120],
  "component_candidates": [
    {"component_id": "COMP-103", "label_zh": "勾", "confidence": 0.82},
    {"component_id": "COMP-102", "label_zh": "剔", "confidence": 0.37}
  ]
}
```

### 7.4 验收

- 数字一二三四五六七 top-k 可识别；
- 常见右手动作勾、挑、托、剔可识别；
- 左手指名大指、中指、名指可识别；
- 泛起 / 泛止 / 少息 / 急等可识别；
- 输出 top-k，不硬判唯一答案。

---

## 8. Phase 3：Parser + Lattice

### 8.1 目标

把 P1 parser 与 P2 visual candidates 接起来。

输入是每个位置 top-k candidate，输出 n-best legal parse。

### 8.2 输出示例

```json
{
  "parse_candidates": [
    {
      "reading": "中指七徽勾一",
      "score": 0.86,
      "reason": "valid LEFT_FINGER + HUI + RH_ACTION + STRING pattern"
    },
    {
      "reading": "名指七徽勾一",
      "score": 0.52,
      "reason": "valid pattern but lower visual confidence"
    }
  ],
  "rejected_candidates": [
    {"candidate": "七中指勾一", "reason": "invalid slot order"}
  ]
}
```

### 8.3 验收

- 能从 top-k lattice 中找出合法组合；
- 能拒绝 slot 不合法组合；
- 输出 n-best；
- 能解释第一候选优于第二候选；
- 不确定时保留 unresolved。

---

## 9. Phase 4：Line-level Context

### 9.1 目标

处理一整行图像，但仍然不进入 phrase authority。

流程：

```text
line image
→ visual block detection
→ notation unit segmentation
→ per-unit component lattice
→ per-unit parse candidates
→ line-level coverage ledger
```

### 9.2 输出

```json
{
  "line_id": "LXY_LINE01",
  "units": [
    {"unit_id": "U001", "bbox": [0,0,50,80], "parse_candidates": [...]},
    {"unit_id": "U002", "bbox": [60,0,50,80], "parse_candidates": [...]}
  ],
  "coverage_ledger": {...}
}
```

### 9.3 验收

- 一行图能切出合理 notation units；
- 每个 unit 都有 bbox；
- 每个 unit 都有 component lattice；
- 每个 unit 都有 parse candidates；
- coverage ledger 非空；
- unread ink 明确记录；
- 不输出 phrase authority。

---

## 10. Phase 5：Phrase-level Reconstruction

### 10.1 目标

在 unit-level 稳定后，才进入句级。

处理：

```text
句界
承前
就
泛起 / 泛止 span
少息 / 急
重复结构
状态延续
```

### 10.2 输入

来自 P4 的 unit stream。

### 10.3 输出

```json
{
  "phrase_candidates": [
    {
      "boundary_units": ["U001", "U005"],
      "reading": "...",
      "confidence": 0.84,
      "boundary_reason": "state span + punctuation + unit continuity"
    }
  ]
}
```

### 10.4 验收

- 不见点就切；
- 不假设一图一句；
- 能区分内部停顿与 phrase boundary；
- 能处理承前 / 就 / 状态延续；
- 输出多个 boundary candidates；
- phrase candidate 仍是 draft。

---

## 11. Phase 6：Human Review as Active Learning

### 11.1 目标

人审不做长期代读，而是只审系统低置信 / 分歧 / 未解析部分，并把纠错沉淀回三层资产。

### 11.2 输入

```text
top-k candidate readings
confidence
unresolved slots
forbidden violations
unread ink
boundary disputes
```

### 11.3 输出沉淀

```text
新增 component exemplar
新增 component alias
新增 construction grammar
新增 forbidden parse
新增 regression case
新增 boundary rule
```

### 11.4 验收

- 用户不需要逐字给完整答案；
- 用户只审核系统不确定点；
- 每次审核都有结构化沉淀；
- 下次同类错误减少；
- P1–P6 / line01 / P7 都能成为 regression。

---

## 12. 完整读谱 Skill Runtime Flow

### 12.1 Generation Mode 流程

```text
0. authority gate
1. input mode detection
2. load D1/D2/D3 generation-safe guards
3. visual block segmentation
4. notation unit decomposition
5. component candidate matching
6. construction grammar parse
7. lattice scoring
8. regression / forbidden guard check
9. context handling
10. coverage ledger
11. draft output
```

### 12.2 Evaluation Mode 流程

```text
1. freeze prediction
2. load oracle goldset
3. compare exact / equivalent / partial / fail
4. record failure categories
5. do not modify prediction
```

### 12.3 Learning Mode 流程

```text
1. receive human corrections
2. classify correction type
3. propose deposit update
4. validate no authority boundary violation
5. add regression / forbidden cases after approval
```

---

## 13. 数据权限矩阵

| 数据 | Generation | Evaluation | Learning |
|---|---:|---:|---:|
| component registry | 可读 | 可读 | 可更新提案 |
| component images | 可读 | 可读 | 可新增提案 |
| alias map | 可读 | 可读 | 可更新提案 |
| canon seed | 可读 | 可读 | 可更新提案 |
| construction templates | 可读 | 可读 | 可更新提案 |
| forbidden guards | 可读 | 可读 | 可新增 |
| component/construction guards from goldset | 可读 sanitized view | 可读 raw | 可新增 |
| expected_continuous_reading | 禁止 | 可读 | 可新增 after human review |
| must_include | 禁止 | 可读 | 可新增 after human review |
| phrase_integration_cases | 禁止 | 可读 | 可新增 after human review |
| old reports/lxy_* | 禁止 | 一般禁止，除 failure analysis 特批 | 可作为历史参考但非 authority |

---

## 14. Codex 开工前必须理解的关键句

```text
三层沉淀物提供知识与护栏。
六个 Phase 建设能力模块。
读谱 Skill 在运行时把这些模块串成一次可审计的 draft transcription workflow。
```

```text
禁止答案，不禁止技能。
禁止旧 reports，不禁止 references / sources / tests fixtures 的 generation-safe 部分。
生成端不看 oracle；评估端才看 oracle。
```

```text
当前目标不是让 Codex 继续猜图，而是把三层沉淀升级为：
component detector + grammar parser + lattice scorer + active learning loop。
```

---

## 15. 建议实施顺序

### Milestone A：文档与设计锁定

- 本需求文档入 reports；
- 1-3-6 流程图入 reports；
- 不修改 runtime code；
- 不进入 P1 实现。

### Milestone B：Phase 1 Grammar Parser MVP

- mock component sequence fixtures；
- parser rule proposal；
- n-best parse output；
- illegal parse rejection；
- tests。

### Milestone C：Phase 2 Visual Component Candidate Layer

- component image exemplar lookup；
- crop → component top-k；
- confidence + visual evidence；
- no reading yet。

### Milestone D：Phase 3–4 Lattice + Line

- candidate lattice → n-best parse；
- line image → units；
- coverage ledger。

### Milestone E：Phase 5–6 Phrase + Learning

- phrase boundary candidates；
- active learning deposit update proposals；
- regression hardening。

---

## 16. 当前不应做的事

```text
不要继续用 prompt 让 Codex 直接读整行图。
不要把 line01 v0.1/v0.2 失败预测提交为有效读谱产物。
不要把人审读法当长期方案。
不要把 goldset 直接给生成端。
不要再粗暴禁止 references / sources / construction templates。
不要进入 P7。
```

---

## 17. 设计验收口径

本 1-3-6 设计文档完成后，Codex 开工前必须能回答：

1. 什么是 1 Skill？
2. 三层沉淀物分别在哪里？
3. 哪些沉淀可在生成期使用，哪些只能评估期使用？
4. 六个 Phase 的输入、输出、成功标准是什么？
5. 为什么先做 Phase 1，而不是继续直接读图？
6. 为什么 active learning 不是人工代读？
7. 哪些路径绝对不能写？
8. 哪些输出必须保持 draft / non-authority？

只有这些问题都能回答清楚，才进入 Phase 1 Codex 实现。
