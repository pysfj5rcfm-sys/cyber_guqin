# scripts

This directory contains validator/audit scripts, generic dry-run-first reproduction helpers, split/recording helpers, and historical templates. Check `docs/cyber_guqin/SCRIPT_REGISTRY.md` before treating any file here as a workflow entrypoint.

## Validator / Audit

- `validate_canon.py`
- `validate_canon_seed.py`
- `validate_dapu_ir.py`
- `validate_qxby_batch.py`
- `check_v1_compat.py`
- `audit_qxby_batch_sources.py`
- `audit_recording_ingest_readiness.py`
- `audit_v1_to_canon_coverage.py`

These may produce reports depending on their mode. They are not renderer, sample ingest, ML, or second-piece entrypoints.

## Dry-Run-First Reproduction Helpers

- `generate_recording_plan_from_dapu_ir.py`
- `render_abcd_from_manifest.py`
- `cyber_guqin_reproduction_lib.py`

Generic P1-F scripts default to dry-run / metadata planning. Any `--execute` path needs explicit authorization and must use a sandbox such as `reproduction_runs/<RUN_ID>/` when render/final outputs are involved.

## Split / Recording Helpers

- `slate_number_recognizer.py`
- `trim_clean_experimental_segments.py`
- `finalize_reviewed_unit_previews.py`
- `split_framework_common.py`

These require explicit input scope. Any audio read/write or preview materialization needs separate authorization.

## Historical-Only

- `build_xwc_legacy_bridge_preview.py`
- `slate_based_experimental_split.py`
- `register_mvp_pilot_raw_audio.py`
- `render_xwc_abcd_from_planning.py`

`render_xwc_abcd_from_planning.py` must not be run in repo hygiene tasks. It is historical XWC/Baiya render logic and can read/write audio/render outputs.

## Forbidden Without Approval

- `scripts/generate_baiya_recording_plan.py` is absent in current HEAD. If it is restored or appears untracked later, treat it as a protected historical template and forbidden-to-touch: do not run, stage, move, delete, archive, or process it in hygiene tasks.
- Do not write `03_samples/sample_assets.csv`, `03_samples/recording_segments.csv`, or `recording_items_enriched.jsonl`.
- Do not touch accepted `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`.
- Do not run renderer, ingest, ML, frontend build, backend scripts, second-piece, G, or F2 workflows during hygiene/index tasks.

## Authority Boundary

- R2 canonical authority: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML exports are derived.
- `reports/` is audit/status evidence, not runtime output.
- `examples/cyber_guqin/` contains fixtures and mock examples, not accepted baseline authority.
