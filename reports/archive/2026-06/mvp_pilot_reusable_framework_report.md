# MVP Pilot Reusable Framework Report

## Kept Framework Scripts

### `scripts/slate_number_recognizer.py`

Purpose: prepare slate-number expectations for ASR or manual recognition.

Required framework arguments:

- `--session-id`
- `--raw-audio-dir`
- `--take-plan`
- `--batch-range-map`
- `--output-dir`
- `--execute`

Default behavior: dry-run input validation and JSON summary to stdout.

### `scripts/finalize_reviewed_unit_previews.py`

Purpose: preserve the reviewed-anchor to anchor-locked unit preview handoff.

Required framework arguments:

- `--session-id`
- `--raw-audio-dir`
- `--take-plan`
- `--batch-range-map`
- `--output-dir`
- `--execute`

Optional input: `--reviewed-anchor-manifest`.

### `scripts/trim_clean_experimental_segments.py`

Purpose: prepare clean experimental trim metadata after reviewed unit previews exist.

Required framework arguments:

- `--session-id`
- `--raw-audio-dir`
- `--take-plan`
- `--batch-range-map`
- `--output-dir`
- `--execute`

Optional input: `--reviewed-unit-preview-manifest`.

### `scripts/split_framework_common.py`

Purpose: shared CSV, batch range, raw audio, and non-production guardrail helpers.

### `scripts/slate_based_experimental_split.py`

Status: deprecated compatibility notice.

Reason: pure energy sequential alignment is a discarded workflow after this failed pilot. Running the file without `--explain` exits non-zero and points users to the explicit-input framework helpers.

## Removed Assumptions

- No default `RS_XWC_001_MVP_PILOT` failed artifact paths.
- No hardcoded Sanman performer assumption.
- No hardcoded failed clean segment repair targets.
- No default XWC legacy report path.
- No production sample creation path.

## Future Baiya Example

```bash
python3 scripts/slate_number_recognizer.py \
  --session-id RS_XWC_002_BAIYA_PILOT \
  --raw-audio-dir 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw \
  --take-plan reports/rs_xwc_002_baiya_recording_take_plan.csv \
  --batch-range-map reports/rs_xwc_002_baiya_batch_ranges.csv \
  --output-dir reports/rs_xwc_002_baiya_split_framework
```

Add `--execute` only when intentionally writing framework artifacts.

## Guardrails

All framework reports and manifests must state:

- experimental_only: true
- production_grade: false
- not_standard_sample_library: true

No framework artifact is a sample candidate until a later human listening QC acceptance and explicit sample-ingest authorization.
