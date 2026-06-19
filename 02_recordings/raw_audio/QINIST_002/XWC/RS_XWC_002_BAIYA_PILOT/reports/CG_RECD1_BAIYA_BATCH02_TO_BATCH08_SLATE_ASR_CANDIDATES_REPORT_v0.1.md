# CG-RECD1 Baiya Batch02 To Batch08 Slate ASR Candidates Report v0.1

## Final Conclusion

RECD1_BATCH_ASR_READY__BATCH02_TO_BATCH08_CANDIDATES_READY

## ASR Runtime / Model

- ASR tool: `faster-whisper`
- Runtime: `.venv-asr`
- Package version: `faster-whisper 1.2.1`
- Model: `medium`
- Device: `cpu`
- Compute type: `int8`
- Language: `zh`
- Word timestamps: `true`
- Beam size: `5`
- Runtime available: `true`

## Per-Batch Inputs And Outputs

| batch_id | raw WAV | expected range | candidate manifest | transcript segments | match report | raw JSON sidecar | raw CSV pointer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| batch02 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav` | T011-T020 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02/batch02_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02/batch02_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02/batch02_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.slate_anchor_candidates.csv` |
| batch03 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav` | T021-T030 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch03/batch03_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch03/batch03_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch03/batch03_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.slate_anchor_candidates.csv` |
| batch04 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.wav` | T031-T040 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch04/batch04_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch04/batch04_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch04/batch04_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.slate_anchor_candidates.csv` |
| batch05 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.wav` | T041-T050 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch05/batch05_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch05/batch05_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch05/batch05_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.slate_anchor_candidates.csv` |
| batch06 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.wav` | T051-T060 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch06/batch06_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch06/batch06_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch06/batch06_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.slate_anchor_candidates.csv` |
| batch07 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.wav` | T061-T070 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch07/batch07_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch07/batch07_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch07/batch07_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.slate_anchor_candidates.csv` |
| batch08 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.wav` | T071 | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch08/batch08_slate_anchor_candidates.csv` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch08/batch08_asr_transcript_segments.jsonl` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch08/batch08_asr_match_report.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.asr_candidates.json` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.slate_anchor_candidates.csv` |

## Per-Batch Candidate Counts

| batch_id | expected | rows | matched | ambiguous | duplicate | unmatched | failed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| batch02 | 10 | 10 | 9 | 1 | 1 | 0 | 0 |
| batch03 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| batch04 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| batch05 | 10 | 10 | 9 | 1 | 1 | 0 | 0 |
| batch06 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| batch07 | 10 | 10 | 8 | 2 | 2 | 0 | 0 |
| batch08 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |

## Combined Summary

- Total expected takes: `61`
- Total candidate rows: `61`
- Total matched rows: `57`
- Total ambiguous rows: `4`
- Total duplicate rows: `4`
- Total unmatched rows: `0`
- Total failed rows: `0`
- Summary CSV: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02_to_batch08_asr_summary.csv`
- Summary JSON: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02_to_batch08_asr_summary.json`

## T071 Placement Confirmation

`T071` remains `recording_take_no=T071`, `batch_id=batch08`, `batch_take_no=001`, and uses `source_raw_audio=02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.wav`. It is not `batch07_take_011` and is not a retake.

## Batch08 Single-Take Handling

`batch08` was processed as a terminal single-take batch with expected range `T071` only. No `T072` was expected, no missing next slate was treated as a failure, and `batch08` was not merged into `batch07`.

## R0 Intake Compatibility Result

R0 raw root used for smoke test:

```text
CG_VARW_RAW_ROOT=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio
```

Smoke test command used the Codex primary Python runtime because system `python3` did not have `pydantic`; this was an environment dependency issue, not a candidate sidecar issue.

```text
raw_root_mode real
raw_total_count 35
batch02 candidate_count 10 review_unit_count 10 unit_ids T011-T020
batch03 candidate_count 10 review_unit_count 10 unit_ids T021-T030
batch04 candidate_count 10 review_unit_count 10 unit_ids T031-T040
batch05 candidate_count 10 review_unit_count 10 unit_ids T041-T050
batch06 candidate_count 10 review_unit_count 10 unit_ids T051-T060
batch07 candidate_count 10 review_unit_count 10 unit_ids T061-T070
batch08 candidate_count 1 review_unit_count 1 unit_ids T071
expected_review_unit_total 61
actual_review_unit_total 61
r0_smoke_errors 0
```

## Boundary Confirmation

- No reviewed anchors were created.
- No `reviewed_slate_anchor_manifest.csv` was generated for batch02-batch08.
- No `raw_marker_review.csv` was generated for batch02-batch08.
- No `split_plan_from_raw_markers.csv` was generated for batch02-batch08.
- No R0 human review was performed.
- No split was executed.
- No unit preview or clean preview was generated.
- No R1 was started.
- No `03_samples/`, `sample_assets.csv`, `recording_segments.csv`, `recording_items_enriched.jsonl`, or `04_outputs/` output was written by this task.
- No render was executed.
- No ML training data was created.
- No raw master WAV was modified.
- Batch01 completed archive outputs were not modified.

## Validation Command Results

- First inspection: `take_manifest_validation_errors: 0`.
- ASR runtime: `.venv-asr`, `faster_whisper 1.2.1`, `WhisperModel` import OK, model loaded as `medium/cpu/int8`.
- ASR execution: all batch02-batch08 raw WAV files processed independently; no batch failed.
- Candidate validation: `candidate_validation_errors: 0`.
- Candidate rows: `candidate_row_count: 61`, `candidate_range: T011 T071`.
- Batch coverage:
  - batch02: `T011-T020`
  - batch03: `T021-T030`
  - batch04: `T031-T040`
  - batch05: `T041-T050`
  - batch06: `T051-T060`
  - batch07: `T061-T070`
  - batch08: `T071`
- `T071`: `batch08`, `batch_take_no=001`.
- Candidate status counts: `candidate=57`, `ambiguous=4`.
- Match status counts: `matched=57`, `duplicate=4`.
- No candidate row has `accepted`, `reviewed`, `human_verified`, `render_usable`, `sample_candidate`, or production-use status text.
- All candidate rows have `requires_manual_review=true`, `review_only=true`, `production_grade=false`, `not_sample_assets=true`, `not_render_executed=true`, and `not_ml_training_data=true`.
- Forbidden-output check:
  - `03_samples/`: pre-existing, not touched.
  - `04_outputs/`: pre-existing, not touched.
  - `sample_assets.csv`: absent.
  - `recording_segments.csv`: absent.
  - `recording_items_enriched.jsonl`: absent.
  - `tools/cg-varw/review_outputs/`: pre-existing, not touched.
- `git diff --check`: PASS, exit code 0, no output.

## Git Status Result

`git status --short --untracked-files=all`:

```text
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02/batch02_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02/batch02_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02/batch02_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02_to_batch08_asr_summary.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch02_to_batch08_asr_summary.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch03/batch03_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch03/batch03_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch03/batch03_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch04/batch04_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch04/batch04_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch04/batch04_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch05/batch05_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch05/batch05_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch05/batch05_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch06/batch06_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch06/batch06_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch06/batch06_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch07/batch07_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch07/batch07_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch07/batch07_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch08/batch08_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch08/batch08_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch08/batch08_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_RECD1_BAIYA_BATCH02_TO_BATCH08_SLATE_ASR_CANDIDATES_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

`scripts/generate_baiya_recording_plan.py` was pre-existing untracked workspace state and was not touched by this task.
