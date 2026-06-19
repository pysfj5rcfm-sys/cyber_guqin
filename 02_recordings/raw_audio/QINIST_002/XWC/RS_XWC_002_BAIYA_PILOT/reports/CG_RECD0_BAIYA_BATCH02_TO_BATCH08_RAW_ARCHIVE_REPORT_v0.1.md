# CG-RECD0 Baiya Batch02 To Batch08 Raw Archive Report v0.1

## Final Conclusion

RECD0_BATCH_ARCHIVE_READY__BATCH02_TO_BATCH08_REGISTERED

## Source And Target WAV Paths

| batch_id | source WAV | target raw archive | action |
| --- | --- | --- | --- |
| batch02 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch02.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav` | copied_byte_for_byte |
| batch03 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch03.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav` | copied_byte_for_byte |
| batch04 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch04.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.wav` | copied_byte_for_byte |
| batch05 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch05.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.wav` | copied_byte_for_byte |
| batch06 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch06.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.wav` | copied_byte_for_byte |
| batch07 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch07.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.wav` | copied_byte_for_byte |
| batch08 | `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch08.wav` | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.wav` | copied_byte_for_byte |

## Per-Batch Actual Range And WAV Metadata

| batch_id | actual_range | sample_rate | bit_depth | channels | duration_s | file_size_bytes | checksum_sha256 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| batch02 | T011-T020 | 44100 | 24 | 2 | 104.024898 | 27526584 | `d1495dfe494c2bba16c0bd2499af3b86fbec27502646c9e4763677825c9d9184` |
| batch03 | T021-T030 | 44100 | 24 | 2 | 103.281859 | 27329966 | `40954782138936a68b4e2e15758a4d38b24623bdfa54e7ddc8b7360ffd4e9219` |
| batch04 | T031-T040 | 44100 | 24 | 2 | 103.281859 | 27329968 | `c4094f6a621aeba91ad4a79392f6dc04104538f6be0470b7c8d35fc5fbf50b12` |
| batch05 | T041-T050 | 44100 | 24 | 2 | 100.309705 | 26543478 | `9de28c4a6c4f5db0a3d139266f30d493c2de70670327f9c0ce064e9a2e65a6c3` |
| batch06 | T051-T060 | 44100 | 24 | 2 | 107.740091 | 28509668 | `f546c7373dc1949ee1c1a62ee80cce780e762aced787e87a65ca13e0466db374` |
| batch07 | T061-T070 | 44100 | 24 | 2 | 98.080590 | 25953640 | `08a1c9d97e0fd6905e9fe46c8060e5ab3e5519b460f6208ac93493b924582f4f` |
| batch08 | T071 | 44100 | 24 | 2 | 17.832426 | 4719216 | `702c7df516aac29f8e6340e348d5030d211802341b40857cab5aa89b2017b978` |

## Batch Range Reconciliation Summary

| batch_id | planned_range | actual_range | take_count | range_status | notes |
| --- | --- | --- | ---: | --- | --- |
| batch02 | T011-T020 | T011-T020 | 10 | as_planned | actual recording matches original plan |
| batch03 | T021-T030 | T021-T030 | 10 | as_planned | actual recording matches original plan |
| batch04 | T031-T040 | T031-T040 | 10 | as_planned | actual recording matches original plan |
| batch05 | T041-T050 | T041-T050 | 10 | as_planned | actual recording matches original plan |
| batch06 | T051-T060 | T051-T060 | 10 | as_planned | actual recording matches original plan |
| batch07 | T061-T071 | T061-T070 | 10 | range_adjusted | planned terminal T071 moved out of batch07 based on actual recording fact |
| batch08 | <none> | T071 | 1 | added_single_take_batch | T071 recorded as standalone batch08; not a retake; not part of batch07 raw file. |

## Manifest Update Summary

- `session_manifest.yaml` now registers `batch01` through `batch08` and records actual WAV metadata under `actual_audio` without assuming 48kHz/24-bit.
- `raw_audio_inventory.csv` now covers `batch01` through `batch08`; new rows are `review_only=true`, `production_grade=false`, `not_sample_assets=true`, `not_render_executed=true`, `not_ml_training_data=true`, and `raw_master_readonly=true`.
- `take_manifest.csv` now covers `T001-T071` exactly once, with batch02-batch08 rows inherited from `reports/rs_xwc_002_baiya_recording_take_plan.csv` and actual batch boundaries applied.
- `batch_range_reconciliation.csv` records the plan-vs-actual correction around `T071`.

## T071 Placement Confirmation

`T071` is registered as `recording_take_no=T071`, `batch_id=batch08`, `batch_take_no=001`, `source_raw_audio=RS_XWC_002_BAIYA_PILOT_batch08_T071.wav`. It is not a retake and is not part of the batch07 raw file.

## Batch07 / Batch08 Correction Explanation

The source plan originally placed `T071` in `batch07` as `batch_take_no=011`. The actual recording fact supersedes that plan: `batch07` contains `T061-T070`, while `batch08` is a terminal single-take batch containing only `T071`. Therefore batch07 is not incomplete; its actual range has been revised.

## Boundary Confirmation

- No ASR was run.
- No ASR candidates were generated.
- No R0 was started.
- No `reviewed_slate_anchor_manifest.csv`, `raw_marker_review.csv`, or `split_plan_from_raw_markers.csv` was generated for batch02-batch08.
- No split was executed.
- No unit preview or clean preview was generated.
- No R1 was started.
- No `03_samples/`, `sample_assets.csv`, `recording_segments.csv`, `recording_items_enriched.jsonl`, or `04_outputs/` output was written by this task.
- No render was executed.
- No ML training data was created.

## Validation Command Results

- `git diff --check`: PASS, exit code 0, no output.
- Manifest validation: PASS, `manifest_validation_errors: 0`.
- `raw_audio_inventory.csv`: covers `batch01,batch02,batch03,batch04,batch05,batch06,batch07,batch08`.
- `take_manifest.csv`: `take_count: 71`; covers `T001-T071` exactly once; no duplicate `recording_take_no`.
- `batch07` take coverage: `T061,T062,T063,T064,T065,T066,T067,T068,T069,T070`.
- `T071`: `batch08`, `batch_take_no=001`, `source_raw_audio=02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.wav`, `retake_no=''`.
- Every batch02-batch08 row has `source_raw_audio`; every target raw WAV exists; every target raw WAV checksum matches inventory; every batch02-batch08 raw master has no write bit set.
- New rows keep `production_grade=false`, `review_only=true`, and `not_sample_assets=true`.
- Forbidden-output check:
  - `03_samples/`: pre-existing, not touched.
  - `04_outputs/`: pre-existing, not touched.
  - `sample_assets.csv`: absent.
  - `recording_segments.csv`: absent.
  - `recording_items_enriched.jsonl`: absent.
  - `tools/cg-varw/review_outputs/`: pre-existing, not touched.

## Git Status Result

`git status --short --untracked-files=all`:

```text
 M 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/raw_audio_inventory.csv
 M 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/session_manifest.yaml
 M 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/take_manifest.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/batch_range_reconciliation.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_RECD0_BAIYA_BATCH02_TO_BATCH08_RAW_ARCHIVE_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

`scripts/generate_baiya_recording_plan.py` was pre-existing untracked workspace state and was not touched by this task.
