# RECD / VARW CSV Writer Patch Report v0.1

Task: `CG-RECD_VARW_CSV_WRITER_PATCH_v0.1`  
Date: 2026-06-12  
Scope: CG-VARW R0/R1 review-only CSV writer contract alignment

## 1. Modified areas

- Backend schemas: `tools/cg-varw/backend/app/schemas.py`
- Backend resolver: `tools/cg-varw/backend/app/services/export_context_resolver.py`
- Backend validator: `tools/cg-varw/backend/app/services/csv_contract_validator.py`
- R0 writer/build path: `tools/cg-varw/backend/app/services/r0_export_writer.py`, `tools/cg-varw/backend/app/services/review_unit_builder.py`, `tools/cg-varw/backend/app/api/r0_reviews.py`
- R1 writer/metadata path: `tools/cg-varw/backend/app/services/r1_review_store.py`, `tools/cg-varw/backend/app/services/r1_split_store.py`, `tools/cg-varw/backend/app/api/r1_split_review.py`
- Backend contract tests: `tools/cg-varw/backend/app/tests/test_csv_contracts.py`
- Frontend preview/types: `tools/cg-varw/frontend/src/types/cgVarw.ts`, `tools/cg-varw/frontend/src/mock/rawReviewMock.ts`, `tools/cg-varw/frontend/src/components/reviewUi.ts`, `tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx`, `tools/cg-varw/frontend/src/pages/R1SplitReviewPage.tsx`

No split, sample ingest, render, or ML execution was added.

## 2. Resolver and validation

Added `R0ExportContextResolver` and `R1ExportContextResolver`.

- R0 resolver collects session/take/raw provenance from `ReviewUnit` plus the selected raw source path.
- R1 resolver collects split/segment provenance from `SplitSegment`; `relative_path` is treated as split segment metadata for `source_split_audio` when a dedicated `source_split_audio` field is absent.
- `take_id` remains a display alias only. It is not copied into `recording_take_no`.
- Missing upstream provenance is surfaced as `contract_warnings`.

Added `validate_csv_contract`.

Validation covers required columns, safety flags, active status enums, active render anchor enum, alias conflicts, R0 split boundary fields, R1 QC human fields, and R1 `not_render_executed` / `not_ml_training_data`.

## 3. CSV field additions

### R0 `reviewed_slate_anchor_manifest.csv`

Added canonical fields:

`recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `batch_id`, `script_id`, `source_raw_audio`, `take_id`.

Existing boundary and review fields are retained. `source_audio` is retained only as alias for `source_raw_audio`.

### R0 `raw_marker_review.csv`

Added provenance fields:

`recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `batch_id`, `batch_take_no`, `script_id`, `source_raw_audio`, `source_audio`, `take_id`, `event_id`, `event_range`, `gesture_id`, `expected_sample_type`, `not_sample_assets`.

`source` remains marker source, not audio path.

### R0 `split_plan_from_raw_markers.csv`

Added canonical split plan fields:

`recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `batch_id`, `script_id`, `source_raw_audio`, `event_id`, `event_range`, `gesture_id`, `unit_start_s`, `unit_end_s`, `slate_start_s`, `slate_end_s`, `next_slate_start_s`, `suggested_clean_start_s`, `suggested_clean_end_s`, `tail_end_s`, `split_plan_role`, `updated_at`.

Legacy `planned_*` fields are retained as aliases. `suggested_clean_end_s` follows `unit_end_s` / `next_slate_start_s`; it is not defaulted to `tail_end_s`.

### R1 `reviewed_render_anchors.csv`

Added canonical fields:

`recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `recording_take_no`, `batch_take_no`, `script_id`, `source_split_audio`, `gesture_id`, `realization_variant`, `render_anchor_type`, `segment_status`, `not_ml_training_data`.

Aliases retained:

`source_audio`, `variant`, `anchor_type`.

### R1 `split_marker_review.csv`

Added provenance and safety fields:

`recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `recording_take_no`, `batch_take_no`, `script_id`, `source_split_audio`, `source_audio`, `event_id`, `event_range`, `gesture_id`, `realization_variant`, `variant`, `not_sample_assets`, `not_render_executed`, `not_ml_training_data`.

`source` remains marker source, not audio path.

### R1 `segment_qc_sheet.csv`

Added canonical QC fields:

`recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `recording_take_no`, `batch_take_no`, `script_id`, `source_split_audio`, `event_id`, `event_range`, `gesture_id`, `realization_variant`, `segment_status`, `excluded`, `human_accepted`, `reviewed_by`, `reviewed_at`, `not_ml_training_data`.

`source_audio` and `variant` are retained only as aliases.

## 4. Field sources

Manifest / raw review state:

- R0 identity fields come from `ReviewUnit` fields when upstream candidates or saved drafts provide them.
- `source_raw_audio` comes from explicit unit provenance or the selected raw source path.
- R0 event/gesture/sample fields come from `ReviewUnit`.
- R0 marker times and review states come from R0 marker review state.

Split manifest / segment metadata:

- R1 identity fields come from `SplitSegment` when the split manifest or draft provides them.
- `source_split_audio` comes from `SplitSegment.source_split_audio` or segment `relative_path`.
- R1 event/gesture/variant fields come from segment metadata.
- R1 marker times and policies come from R1 segment review state.

Derived fields:

- R0 `unit_start_s = slate_start_s`.
- R0 `unit_end_s = next_slate_start_s`.
- R0 `suggested_clean_start_s = guqin_start_s` when present, otherwise `slate_end_s`.
- R0 `suggested_clean_end_s = unit_end_s`.
- R1 QC booleans derive from `segment_status`.
- R1 `human_accepted` uses explicit `human_accepted` when present; otherwise v0.1 transitional derivation is `segment_status == render_usable`. This remains review-only and does not mean sample asset creation.

Aliases:

- R0 `source_audio = source_raw_audio`.
- R1 `source_audio = source_split_audio`.
- R1 `variant = realization_variant`.
- R1 `anchor_type = render_anchor_type`.

## 5. Warnings and synthetic demo status

The validator returns `contract_warnings` for present-but-empty required provenance in primary CSVs. Current synthetic demo data may still warn for fields that the fixture does not genuinely provide, especially session/person/piece identity and stable `recording_take_no`.

Synthetic demo audio provenance is mock/demo provenance only:

- R0 demo can carry `source_raw_audio` from the selected raw fixture path.
- R1 demo can carry `source_split_audio` from split segment metadata `relative_path`.
- Missing identity fields are not guessed from filenames.

`reviewed_at` is never populated from `updated_at`. If no human action timestamp exists, it remains empty and is reported as a warning.

## 6. Safety boundaries

All writers preserve:

`review_only=true`, `production_grade=false`, `not_sample_assets=true`.

R0 split plan also preserves:

`not_executed=true`, `not_recording_segments=true`.

R1 outputs also preserve:

`not_render_executed=true`, `not_ml_training_data=true`.

This patch did not write `02_recordings/`, `03_samples/`, `04_outputs/`, `sample_assets.csv`, `recording_segments.csv`, or `recording_items_enriched.jsonl`.
