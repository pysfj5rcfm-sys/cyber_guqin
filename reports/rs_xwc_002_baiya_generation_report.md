# Baiya Recording Plan Generation Report

Status: draft pending user review. 生成后必须等待用户审核；本轮不得自动创建 raw audio folder，不得进入录音登记，不得进入切片。

## Inputs Used

- `reports/xwc_legacy_take_manifest_preview.csv`
- `reports/xwc_legacy_recording_bridge_map.json`
- `01_pieces/xianwengcao/recording_script_human.csv` (read-only)
- `06_docs/NEXT_RECORDING_PLAN_BAIYA.md`
- `06_docs/GUQIN_SLATE_BASED_SPLIT_PIPELINE.md`
- `06_docs/FORMAL_RECORDING_SPLIT_REUSE_PLAN.md`

## Plan Kind

- source_plan_kind: `legacy_xwc_bridge_for_baiya_reshoot`
- future_plan_kind: `dapu_event_ir_recording_plan`
- Dapu Event IR formal recording plan was not generated in this round.
- Legacy `recording_batches.md` was not treated as future source of truth.

## Batch Choice

The draft keeps stable T001-T071 order and uses 7 smaller batches to avoid the previous long-batch spacing problem:

- batch01: T001-T010 (10 takes)
- batch02: T011-T020 (10 takes)
- batch03: T021-T030 (10 takes)
- batch04: T031-T040 (10 takes)
- batch05: T041-T050 (10 takes)
- batch06: T051-T060 (10 takes)
- batch07: T061-T071 (11 takes)

## Coverage

- take_count: 71
- covers T001-T071: True
- all rows use `QINIST_002 = 白牙`: True
- `QINIST_001 = 三曼` was not overwritten.

## Review Warnings

- none

## Guardrails

- Did not modify `01_pieces`.
- Did not write `02_recordings/raw_audio`.
- Did not write `03_samples`.
- Did not write `sample_assets`.
- Did not create `recording_items_enriched`.
- Did not enter recording registration.
- Did not enter slicing.
- Next step is user review, then user recording if approved.

## R1 Human-Readability Fixes

- `spoken_slate_text` is now a single performer-facing yao-style reading.
- ASR-compatible yi/yao variants are stored separately in `asr_accepted_variants`.
- T060 is `context_take_1` and T071 is `context_take_2`; both use event_range `XWC_P09_N01_to_N02`.
- Long-tail rule takes use 2.5 seconds after full natural decay: T052, T053, T057, T058, T059, T060, T070, T071. T059 is included to keep its single-take instruction and tail rule consistent.
- This R1 pass still does not create raw audio folders, recording registration, split outputs, `03_samples`, `sample_assets`, or `recording_items_enriched`.
