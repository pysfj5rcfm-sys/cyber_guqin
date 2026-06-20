# 《仙翁操》白牙 ABCD 共听评输入指南

## 四个 wav 路径

- `A_LITERAL`: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/A_LITERAL/XWC_BAIYA_A_LITERAL.wav`
- `B_PHRASE`: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/B_PHRASE/XWC_BAIYA_B_PHRASE.wav`
- `C_QINIST_STYLE`: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/C_QINIST_STYLE/XWC_BAIYA_C_QINIST_STYLE.wav`
- `D_TEACHING_DIAGNOSTIC`: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/D_TEACHING_DIAGNOSTIC/XWC_BAIYA_D_TEACHING_DIAGNOSTIC.wav`

## 建议听评顺序

1. `A_LITERAL`：先建立直译谱面骨架参照。
2. `D_TEACHING_DIAGNOSTIC`：确认结构、动作与音位边界是否清楚。
3. `B_PHRASE`：比较句读、气口与段落呼吸。
4. `C_QINIST_STYLE`：听白牙样本衔接、自然尾音与 context 连接是否更像演奏。

## 每版听评关注点

- `A_LITERAL`：是否保留谱面骨架；是否有明显 anchor 错位；是否过于机械。
- `B_PHRASE`：phrase boundary 是否清楚；气口是否自然；是否避免固定 gap。
- `C_QINIST_STYLE`：尾音是否保留得当；context take 是否提升连贯性；是否引入非 score fact 的误读。
- `D_TEACHING_DIAGNOSTIC`：动作边界是否可诊断；音位是否清楚；是否牺牲自然性但提升定位能力。

## 问题类型列表

- `too_mechanical`
- `wrong_breath`
- `tail_short`
- `tail_too_long`
- `attack_abrupt`
- `sample_mismatch`
- `phrase_unclear`
- `transition_unnatural`
- `context_take_needed`
- `context_take_overused`
- `anchor_suspect`
- `good`

## 用户主观听评记录方式

建议按 version + event/phrase 记录：先写整体感受，再记录最明显的 3-8 个问题点。每条问题尽量标注版本、时间点、事件或 phrase、问题类型、主观建议，以及是否有偏好的参考版本。

## GPT 后续如何参与 E 共创

GPT 后续应同时读取四个 wav、各版 `render_event_alignment.<VERSION>.csv`、`sample_selection_decision.csv` 与用户听评记录，分层给出：结构/句法诊断、工程对齐诊断、样本选择诊断、打谱解释风险，以及 `e_revision_plan` 草案。

## E_REVIEWED 边界

本阶段不自动生成 E。E 必须来自 ABCD render -> 用户听评 -> GPT 听评/结构分析/工程诊断/打谱解释诊断 -> e_revision_plan -> 用户确认 -> E render。
