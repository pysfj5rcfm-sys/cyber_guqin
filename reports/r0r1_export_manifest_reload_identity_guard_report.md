# R0/R1 Export Manifest Reload Identity Guard Report

任务：`CG-VARW-R0R1_EXPORT_MANIFEST_RELOAD_AND_IDENTITY_GUARD`

日期：2026-06-22

## 修改文件列表

- `tools/cg-varw/backend/app/services/export_safety_manifest.py`
- `tools/cg-varw/backend/app/services/r0_export_writer.py`
- `tools/cg-varw/backend/app/services/review_unit_builder.py`
- `tools/cg-varw/backend/app/services/r1_review_store.py`
- `tools/cg-varw/backend/app/services/r1_split_store.py`
- `tools/cg-varw/backend/app/services/export_context_resolver.py`
- `tools/cg-varw/backend/app/tests/test_r0_r1_export_safety.py`
- `tools/cg-varw/backend/app/tests/test_r0_review_unit_loading.py`
- `tools/cg-varw/backend/app/tests/test_r1_marker_seed.py`

## R0 manifest / reload / fallback guard

- R0 export now writes `export_manifest.json` beside the three derived CSVs.
- Manifest includes `manifest_version`, `stage=R0`, `canonical_source`, `canonical_source_role=active_internal_state`, `input_state_hash`, `row_counts`, `output_hashes`, `reload_validation`, `forbidden_authority`, `generated_at`, `generator`, and warnings.
- R0 `reload_validation` read-back parses `reviewed_slate_anchor_manifest.csv`, `raw_marker_review.csv`, and `split_plan_from_raw_markers.csv`; it checks row counts, required identity fields, marker type validity, and output sha256 hashes.
- R0 `raw_marker_review.csv` fallback now requires `export_manifest.json` plus `fallback_guard` with source path, sha256, row count, stage, and reason.
- Guarded fallback returns `restored_from_export=true`, `compatibility_restore=true`, and `canonical_active_draft=false`; it does not silently promote CSV back to active canonical draft.
- Missing manifest, wrong stage, hash mismatch, row-count mismatch, or missing fallback reason refuses fallback.

## R1 manifest / reload / identity guard

- R1 export now writes `export_manifest.json` beside `reviewed_render_anchors.csv`, `split_marker_review.csv`, and `segment_qc_sheet.csv`.
- Manifest includes `stage=R1`, active-state input hash, per-file row counts, per-file sha256 output hashes, reload validation, forbidden authority list, generator, and warnings.
- R1 reload validation read-back parses all three CSVs and checks row counts, required identity/provenance fields, and output hashes.
- R1 export now fails fast when canonical identity is missing, including `recording_take_no`, `batch_take_no`, `script_id`, `source_split_audio`, `event_id`, `event_range`, `gesture_id`, `realization_variant`, and `reviewed_at`.
- `take_id` cannot replace `recording_take_no`; `variant` cannot replace `realization_variant`; `updated_at` cannot replace `reviewed_at`; `anchor_type` cannot replace `render_anchor_type`.
- `source_split_audio` is treated as the canonical split audio path and must match the manifest-relative split path for export.
- R1 split-root manifest loading now rejects missing manifest `segment_id`, `take_id` without `recording_take_no`, `source_split_audio` mismatch, root escape, and manifest scope mismatch for session/piece/qinist when the top-level manifest declares those fields.
- File-derived `segment_id` remains only a no-manifest fallback behavior; when manifest identity exists, manifest `segment_id` wins.

## R2 status

- R2 business logic was not modified.
- R2 tests were run to guard the existing canonical/latest-derived export behavior.

## Validation results

- R0/R1 targeted tests:
  - Command: `/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_r0_r1_export_safety app.tests.test_csv_contracts app.tests.test_r0_review_unit_loading app.tests.test_r1_marker_seed`
  - Result: `Ran 27 tests in 0.037s - OK`
- R2 regression tests:
  - Command: `/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_r2_review_draft_persistence app.tests.test_r2_render_set_intake`
  - Result: `Ran 16 tests in 0.081s - OK`
- Backend compile check:
  - Command: `/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m compileall app`
  - Result: exit 0
- P1-F self-contained reproduction tests:
  - Command: `/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest tests.test_self_contained_reproduction_toolchain`
  - Result: `Ran 16 tests in 0.536s - OK`
- `git diff --check`:
  - Result: exit 0, no output.
- `git diff -- scripts/generate_baiya_recording_plan.py`:
  - Result: no output.

## Safety boundary

- Real audio binary read: No.
- Test-created tiny WAV fixtures: Yes, only existing R1 unit-test fixture generation under `tempfile`.
- Sample ingest written: No.
- `sample_assets.csv` modified: No.
- `recording_segments.csv` modified: No.
- `recording_items_enriched.jsonl` modified: No.
- Accepted render outputs modified: No.
- `F_FINAL_REVIEWED` modified: No.
- R2 business logic modified: No.
- `scripts/generate_baiya_recording_plan.py` modified: No.
- Second-piece / Sanman采集实现 / true render / ML training: Not entered.

## git status

Expected final status after this report file is added:

```text
 M tools/cg-varw/backend/app/services/export_context_resolver.py
 M tools/cg-varw/backend/app/services/r0_export_writer.py
 M tools/cg-varw/backend/app/services/r1_review_store.py
 M tools/cg-varw/backend/app/services/r1_split_store.py
 M tools/cg-varw/backend/app/services/review_unit_builder.py
 M tools/cg-varw/backend/app/tests/test_r0_review_unit_loading.py
 M tools/cg-varw/backend/app/tests/test_r1_marker_seed.py
?? reports/r0r1_export_manifest_reload_identity_guard_report.md
?? scripts/generate_baiya_recording_plan.py
?? tools/cg-varw/backend/app/services/export_safety_manifest.py
?? tools/cg-varw/backend/app/tests/test_r0_r1_export_safety.py
```

`scripts/generate_baiya_recording_plan.py` remains an unrelated pre-existing untracked worktree item and was not modified.

## 下一步建议

1. If future explicit restore/migration work is opened, add a separate R0/R1 restore command that consumes these manifests and writes an explicit restored draft with user-supplied reason.
2. Keep R2 canonical/latest guard separate; reuse only the safety contract helpers where they do not alter R2 business schema.
3. Before Sanman real data intake, add a dry-run export smoke using temp output roots for one synthetic R0 file and one synthetic R1 batch.
