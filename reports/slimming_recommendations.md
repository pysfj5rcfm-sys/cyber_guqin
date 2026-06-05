# Phase R0 Slimming Recommendations

Date: 2026-06-05

This document recommends cleanup only. No deletion, move, rename, or mainline data edit was performed in Phase R0.

## Safe Now

These can be safely handled in a cleanup-only pass because they are disposable and already ignored:

- Delete the ignored root `.DS_Store`.
- Continue ignoring `.DS_Store`, `__pycache__/`, `*.pyc`, and `.pytest_cache/`; `.gitignore` already covers all four.
- Keep the working tree free of untracked nonignored files before the next ingest phase.

No `__pycache__`, `.pytest_cache`, or `*.pyc` files were found in the live project scan.

## After Confirmation

These need user confirmation because they affect project history, report organization, or script behavior:

- Archive historical reports into `reports/archive/`:
  - `reports/skills_v1_integration_report.md`
  - `reports/v1_compat_audit.md`
  - `reports/qxby_batch_001_report.md`
- Archive or remove install staging now that `.agents/skills` exists:
  - `reports/skill_install_staging/`
  - `reports/skill_install_instructions.md`
- Decide whether regenerable validator outputs should stay in `reports/` root, move into per-batch/per-run locations, or become ignored generated outputs:
  - `reports/check_v1_compat_report.json`
  - `reports/validate_canon_report.json`
  - `reports/validate_canon_seed_report.json`
  - `reports/validate_dapu_ir_report.json`
  - `reports/validate_qxby_batch_001_report.json`
  - `reports/qxby_batch_001_source_audit.json`
  - `reports/qxby_batch_001_source_audit.md`
- Parameterize batch-specific scripts before `QXBY_BATCH_002`:
  - `scripts/validate_qxby_batch.py`
  - `scripts/audit_qxby_batch_sources.py`
- Document script safety levels in `06_docs/PROJECT_STRUCTURE.md`:
  - read-only validators
  - validators that overwrite reports
  - runtime generators that modify V1 data
  - smoke tests that regenerate multiple outputs
- Mark `05_scripts/make_dummy_samples.py` as bootstrap/dummy-only so it is not mistaken for real recording ingest.
- Consider parameterizing piece-specific runtime scripts by `piece_id` after the real `xianwengcao` recording workflow stabilizes:
  - `05_scripts/generate_recording_script.py`
  - `05_scripts/generate_rhythm.py`
  - `05_scripts/export_recording_checklist.py`
  - `05_scripts/render_audio.py`

## Do Not Touch

Do not move, rename, delete, or rewrite these during slimming:

- `00_global/`
- `01_pieces/`
- `02_recordings/`
- `03_samples/`
- `04_outputs/`
- `05_scripts/`
- `06_docs/`
- `.agents/skills/`
- `canon/*.yaml`
- `canon/drafts/qxby_batch_001.yaml`
- `sources/qinxue_beiyao/QXBY_BATCH_001/`
- `tests/fixtures/`
- `schemas/`
- `references/`

Also do not create recording ingest, do not create `recording_items_enriched.jsonl`, do not modify `sample_assets.csv`, and do not modify the `xianwengcao` recording checklist in this phase.

## Boundary Recommendation

Do not immediately rename files to solve naming inconsistency. The current naming split is understandable:

- `05_scripts/` means V1 runtime scripts.
- `scripts/` means skills/canon/validator scripts.
- uppercase batch ids identify source directories.
- lowercase batch ids identify draft/report filenames.

The recommended next step is to update `06_docs/PROJECT_STRUCTURE.md` in a later confirmed phase so the boundaries are explicit. Once the boundary doc is accepted, archive and parameterization changes can happen without destabilizing the V1 runtime.

## Next-Phase Intake Guardrails

Before OCR Batch 002:

- Create a batch directory contract for `sources/qinxue_beiyao/QXBY_BATCH_002/`.
- Require `manifest.yaml`, `images/`, and `transcriptions/`.
- Require `canon/drafts/qxby_batch_002.yaml` to reference source images and transcription ids.
- Parameterize the QXBY validator and source audit scripts.
- Keep batch reports named with the batch id.

Before real `xianwengcao` recording ingest:

- Put raw audio under `02_recordings/xianwengcao/<session_id>/raw/`.
- Put session metadata under `02_recordings/xianwengcao/<session_id>/session_manifest.yaml`.
- Treat slicing as a manifest-backed step before updating `03_samples/sample_assets.csv`.
- Keep dummy sample generation separate from real sample ingest.
