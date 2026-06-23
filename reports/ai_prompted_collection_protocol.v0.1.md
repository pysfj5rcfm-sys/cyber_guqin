# AI Prompted Collection Protocol v0.1

状态：设计稿。不生成 TTS，不录音。

## 1. Principle

The qinist is professional; R0 review is professional. Prompt speech should be concise:

```text
编号 / 给琴人听的指法内容 / 发令枪
```

Example:

```text
T001，散挑七弦，开始。
T002，泛七徽六弦，开始。
T003，按七徽九分六弦挑，开始。
```

This is prompt design only. It does not create audio, session files, raw recordings, or review data.

## 2. Prompt Manifest

Draft fields:

- `prompt_manifest_id`
- `qinist_id`
- `session_id` or draft `recording_session_id`
- `batch_id`
- `prompt_id`
- `prompt_order`
- `starter_item_id`
- `event_id` / `score_event_id`
- `normalized_name`
- `prompt_text_zh`
- `trigger_text`
- `prompt_interval_s`
- `retake_policy`
- `bad_take_policy`
- safety flags

All prompt-specific fields are `proposed_extension_field`.

## 3. Prompt Script

Prompt script is derived from prompt manifest:

```text
{prompt_id}，{prompt_text_zh}，{trigger_text}。
```

Do not use long instructional speech unless a specific item requires a human-approved exception. Existing `human_instruction` from old recording scripts is useful evidence but too verbose for the new protocol.

## 4. Collection Batch Plan

Batch plan should group by:

- priority tier
- sound type
- context/tail risk
- expected duration
- retake complexity

No real `recording_take_no` should be assigned until recording is authorized. A prompt order is not a recorded take.

## 5. R0 Prompt Anchor Policy

R0 should align:

- spoken prompt start/end
- qin sound start
- tail end
- next prompt start

ASR is auxiliary. Prompt manifest + R0 human review together provide authority; ASR alone must not be the only authority.

## 6. Retake / Bad Take Handling

Retake design:

- Keep original prompt identity stable.
- Mark bad/retake state before candidate sidecar promotion.
- Never allow bad/failed/context-only rows to become atomic samples.
- Require human review before any candidate status changes.

## 7. Interval Calibration

Initial design:

- Default next prompt target: around 10 seconds after prior prompt end.
- Long-tail items may need longer interval.
- Baiya sampling intervals may inform calibration if available, but only as process evidence, not Sanman style data.
- Do not hardcode a universal interval without a calibration report.

