# MVP Pilot Cleanup Summary

## Preserved Raw Evidence

The following raw M4A files remain preserved and were not modified:

- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a`
- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch02.m4a`
- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch03.m4a`
- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch04.m4a`
- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch05.m4a`
- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch06.m4a`
- `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch07.m4a`

Minimum provenance remains:

- `raw_audio_inventory.csv`
- `session_manifest.yaml`
- `PILOT_FAILURE_NOTE.md`
- `KEEP_RAW_ONLY_POLICY.md`

## Cleared Failed Outputs

`experimental_split/` was cleared of failed generated artifacts and now contains only `README_FAILED_AND_CLEARED.md`.

Cleared categories include:

- working WAVs
- segment candidates
- slate units
- repaired segment candidates
- clean experimental segments
- reviewed unit previews
- anchor previews
- slate snippets
- failed manifests, CSVs, JSON, and Markdown notes from the active sandbox

Obsolete `reports/mvp_*` split/candidate reports from the failed pilot were removed, except for this reset's closure reports.

## Reusable Scripts Kept

- `scripts/slate_number_recognizer.py`
- `scripts/finalize_reviewed_unit_previews.py`
- `scripts/trim_clean_experimental_segments.py`
- `scripts/split_framework_common.py`

These helpers now require explicit input paths, default to dry-run, and label framework outputs as experimental-only and non-production.

`scripts/slate_based_experimental_split.py` is retained only as a deprecated compatibility notice because pure energy sequential alignment is no longer an approved path.

## Review Documents Created

- `06_docs/MVP_PILOT_FAILURE_REVIEW.md`
- `06_docs/GUQIN_SLATE_BASED_SPLIT_PIPELINE.md`
- `06_docs/FORMAL_RECORDING_SPLIT_REUSE_PLAN.md`
- `06_docs/CYBER_GUQIN_V1_EVOLUTION_REVIEW.md`
- `06_docs/NEXT_RECORDING_PLAN_BAIYA.md`
- `06_docs/PROJECT_STATUS_RECORDING_SAMPLE_STAGE.md`

## Negative Guarantees

- No `03_samples` write was made.
- No `sample_assets` write was made.
- No `recording_items_enriched` file was created.
- No raw master was modified.
- The next step is to generate a Baiya recording script, not to continue repairing old audio.
