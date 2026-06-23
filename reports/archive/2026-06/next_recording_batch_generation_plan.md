# Next Recording Batch Generation Plan

## Scope

Do not generate a new `recording_batch.md` in this reset. The next stage should use Cyber Guqin skills to generate a Baiya-focused recording batch draft.

## Skill Path

Use `guqin-dapu-parser` and related Cyber Guqin skills to produce the next recording plan from canon-backed / Dapu Event IR / XWC recording-plan inputs.

## Expected Output Fields

- `batch_id`
- `recording_take_no`
- `script_id`
- `gesture_id`
- `normalized_name`
- `expected_sample_type`
- `realization_variant`
- `realization_pre_action`
- human instruction
- slate number
- recording gap instruction

## Baiya Priority

The new script should serve `RS_XWC_002_BAIYA_PILOT` first. It must not overwrite old `recording_batches.md` files. The first output should be a draft in `reports/` or `06_docs/`.

## Recording Gap Rule

Every generated take instruction should include:

- spoken slate
- at least 0.8 seconds silence
- guqin performance
- full tail decay
- at least 1.2 seconds silence before the next slate
