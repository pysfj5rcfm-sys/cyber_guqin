# XWC Legacy Recording Bridge Plan

## Executive Summary

`RS_XWC_001` is a one-time legacy bridge from the old XWC v1.0 Phase 1A recording scripts into the reusable recording asset model. The old 71 recording tasks remain the recording-day authority for what to play. This bridge only explains how to map those tasks into future `session_manifest`, `take_manifest`, `recording_segments`, and sample provenance.

This plan does not create a real recording session, does not slice audio, does not write real `recording_segments`, and does not write real `sample_assets` rows.

## Why XWC RS_XWC_001 Is Legacy

The current XWC recording plan was generated before the reusable recording asset model existed. Its human execution files are:

- `01_pieces/xianwengcao/recording_script.csv`
- `01_pieces/xianwengcao/recording_script_human.csv`
- `01_pieces/xianwengcao/recording_script_human.md`
- `01_pieces/xianwengcao/recording_batches.md`

Those files are valid for this recording day, but they are not the future standard source of truth. Future pieces should use Dapu Event IR / canon-backed parser output to generate standard recording plans.

## What Is Reusable Vs One-Time

Reusable:

- `templates/recording/session_manifest_template.yaml`
- `templates/recording/take_manifest_template.csv`
- `templates/recording/recording_segments_template.csv`
- the schema guidance in `06_docs/RECORDING_INGEST_SCHEMA.md`
- the separation between score facts, realization, recording execution, and audio provenance

One-time for XWC:

- mapping old `RS_XWC_001_*` script rows into expected take preview rows;
- carrying `recording_batches.md` performer order into `batch_take_no`;
- preserving legacy context warnings without patching source files;
- treating `recording_batches.md` as an execution view only.

## Input Files

- `recording_script.csv`: structured legacy recording task rows.
- `recording_script_human.csv`: performer-facing take numbers, instructions, and batch ordering.
- `recording_batches.md`: human recording execution view. It is not a score source.
- `score_events.csv`: score fact source for event references.
- `gesture_templates.csv`: gesture template reference for `gesture_id`.

## Expected Mapping

- `recording_script` row -> expected take row.
- `recording_take_no` -> stable take number for the full session.
- `batch_take_no` -> performer-facing order from the legacy human script.
- `script_id` -> semantic recording task ID.
- `event_id` -> score event reference.
- `event_range` -> multi-event context reference. Required for context slicing.
- `gesture_id` -> gesture template reference.
- `realization_variant` -> sample realization such as `straight`, `chuo`, `zhu`, `context`, or `atomic`.
- `realization_pre_action` -> performed pre-action such as `none`, `chuo`, or `zhu`.
- `expected_sample_type` -> `atomic` or `context`.

## 71-Task Summary

Derived from `01_pieces/xianwengcao/recording_script.csv` and `recording_script_human.csv`:

- Total tasks: 71
- Atomic count: 69
- Context count: 2
- Straight count: 50
- Chuo count: 16
- Zhu count: 2
- Context rows missing `event_range`: 1

There is also one `realization_variant=atomic` row for the standalone `掐起` atomic task. It is still `expected_sample_type=atomic`.

## One Context Take Missing event_range

The context row missing `event_range` is:

- `script_id`: `RS_XWC_001_060`
- `recording_take_no`: `060`
- `batch_take_no`: `069`
- `event_id`: `XWC_P09_N02`
- `normalized_name`: `名十掐起`
- notes: `掐起 context dummy`

Recommended resolution before slicing: review this row against the intended context transition. If it is meant to cover the same `撞到掐起` transition as `RS_XWC_001_071`, set an explicit future event range in the real take/segment workflow, likely `XWC_P09_N01_to_N02`, after human confirmation. Do not patch the legacy file in this phase.

## Proposed XWC take_manifest Derivation

Auto-filled from legacy script:

- `recording_id`
- `recording_take_no`
- `batch_take_no`
- `script_id`
- `legacy_source_type`
- `legacy_source_path`
- `event_id`
- `event_range` when present
- `gesture_id`
- `normalized_name`
- `expected_sample_type`
- `realization_variant`
- `realization_pre_action`
- `slate_text` from batch or take number

Filled during recording:

- `recording_session_id`
- `source_raw_file`
- actual take start and end time if recording by batch or long file
- performer note
- engineer note
- retake notes
- rough `take_quality`

Filled during split:

- exact take boundaries when not captured during recording;
- candidate segment time ranges;
- source take IDs for segment rows;
- segment file paths.

Filled during QC:

- `attack_marker_ms`
- `release_tail_ms`
- `qc_status`
- `quality_status`
- `needs_reshoot`
- `selected_for_segment`
- `selected_for_sample`

## Context Sample Policy

Context takes remain reference material unless a later selection policy explicitly promotes them. This is especially important for the `撞到掐起` transition: the context take should preserve the full `event_range`, the preceding action, the transition, the `掐起`, and natural decay.

Atomic samples should not be silently replaced by context takes. A context segment can become a special sample candidate only after segment QC and sample-set policy decide how it participates in rendering.

## Risks

- `recording_batches.md` gets treated as a score source.
- `batch_take_no` is confused with score `event_no`.
- A context take without `event_range` loses transition provenance.
- Bad takes are overwritten or deleted instead of preserved and rejected in manifests.
- `chuo` is treated as a notation fact when it is a Sanman realization for unmarked pressed notes.
- Raw audio is cut directly, making later provenance audit difficult.

## Next Step

Create the actual `RS_XWC_001` session manifest only after the user confirms recording settings: date, location, qin, tuning, recorder, microphone, sample rate, bit depth, channel count, and recording mode.

Create the actual expected `take_manifest` only after the user confirms recording mode: continuous batch, per-take, or hybrid.
