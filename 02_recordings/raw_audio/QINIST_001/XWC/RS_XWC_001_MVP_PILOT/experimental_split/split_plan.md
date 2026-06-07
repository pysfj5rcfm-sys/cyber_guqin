# Slate-Based Split Plan

## Input Strategy

The `legacy_xwc_preview` adapter reads the 71-row legacy take preview and
normalizes each row to the reusable take-plan schema:

`recording_take_no, batch_take_no, script_id, event_id, event_range, gesture_id, normalized_name, expected_sample_type, realization_variant, realization_pre_action, notes`

Future formal sampling should replace this adapter with
`dapu_event_ir_recording_plan`, fed by guqin-dapu-parser, Dapu Event IR, and a
canon-backed recording plan.

## Split Strategy

Derived working WAV files are scanned for energy windows. Windows are aligned
sequentially to expected takes across raw batch order. Spoken slate text is not
invented; without ASR, the method is `energy_sequential_alignment`.

## Parameters

- pre_roll_s: 0.08
- min_tail_s: 1.2
- default_tail_s: 2.0
- min_segment_s: 0.3
- max_segment_s: 8.0
