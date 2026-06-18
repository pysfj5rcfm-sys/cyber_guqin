# CG-RECD0 Baiya Batch01 Raw Archive Report v0.1

Task: `CG-RECD0_BAIYA_BATCH01_RAW_ARCHIVE_AND_R0_INTAKE_PREP`

## Summary

- Final conclusion: `RAW_ARCHIVE_READY__R0_WAITING_FOR_ASR_CANDIDATES`
- Recording session: `RS_XWC_002_BAIYA_PILOT`
- Performer: `QINIST_002` / 白牙
- Piece: `XWC` / 仙翁操
- Batch scope: `batch01` / `T001-T010` only
- R1 status: `NOT_STARTED`
- R1 reason: `R1 requires RECD-2 controlled split preview outputs after R0 reviewed anchors.`

## Source And Target

- Source WAV path inspected: `/Users/chenyulin/Library/Mobile Documents/com~apple~CloudDocs/batch01.wav`
- Target raw archive path: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`
- Raw file action: `copied`
- Raw master readonly: `true` (`0444`)
- Original user file modified: `false`
- Raw audio transformed: `false`
- Raw audio split: `false`

## WAV Metadata

| Field | Value |
| --- | --- |
| file_name | `RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav` |
| source_input_name | `batch01.wav` |
| relative_path | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav` |
| file_format | `wav` |
| codec_or_encoding | `NONE (not compressed)` |
| sample_rate | `44100` |
| bit_depth | `24` |
| channels | `2` |
| duration_s | `115.170476` |
| file_size_bytes | `30475814` |
| checksum_sha256 | `f9f3c29a0b289c87106cf6994a1d789ee1055ab13230b8fef8dbf0005e1e814e` |
| source_created_or_modified_at_utc | `2026-06-18T23:03:53+00:00` |
| registered_at | `2026-06-19T07:22:08+08:00` |

Preferred capture remains `48000 Hz / 24-bit`, but actual archived audio is recorded honestly as `44100 Hz / 24-bit`.

## Manifests

- Session manifest: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/session_manifest.yaml`
- Raw audio inventory: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/raw_audio_inventory.csv`
- Take manifest: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/take_manifest.csv`

`raw_audio_inventory.csv` contains one row for `batch01`.

`take_manifest.csv` contains exactly 10 rows, sourced from `reports/rs_xwc_002_baiya_recording_take_plan.csv`:

| take_label | recording_take_no | batch_take_no | slate_no | gesture_id | event_id | realization_variant |
| --- | --- | --- | --- | --- | --- | --- |
| `T001` | `T001` | `001` | `001` | `SAN_TIAO_7` | `XWC_P01_N01` | `straight` |
| `T002` | `T002` | `002` | `002` | `SAN_GOU_5` | `XWC_P01_N02` | `straight` |
| `T003` | `T003` | `003` | `003` | `SAN_TIAO_7` | `XWC_P01_N03` | `straight` |
| `T004` | `T004` | `004` | `004` | `AN_RING_10_GOU_5` | `XWC_P01_N04` | `straight` |
| `T005` | `T005` | `005` | `005` | `AN_RING_10_GOU_5` | `XWC_P01_N04` | `chuo` |
| `T006` | `T006` | `006` | `006` | `SAN_TIAO_7` | `XWC_P02_N01` | `straight` |
| `T007` | `T007` | `007` | `007` | `SAN_GOU_5` | `XWC_P02_N02` | `straight` |
| `T008` | `T008` | `008` | `008` | `SAN_TIAO_6` | `XWC_P02_N03` | `straight` |
| `T009` | `T009` | `009` | `009` | `AN_RING_10_GOU_4` | `XWC_P02_N04` | `straight` |
| `T010` | `T010` | `010` | `010` | `AN_RING_10_GOU_4` | `XWC_P02_N04` | `chuo` |

For all rows:

- `long_tail_required=false`
- `tail_silence_required_s=1.2`
- `take_status=candidate`
- `review_only=true`
- `production_grade=false`
- `not_sample_assets=true`
- `not_render_executed=true`
- `not_ml_training_data=true`

## R0 Intake Readiness

- `RAW_ARCHIVE_READY=true`
- `R0_RAW_SCAN_SUPPORTED=true`
- Suggested R0 raw root: `CG_VARW_RAW_ROOT=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio`
- R0 scanner result: `raw_root_mode=real`, `matched_count=1`
- R0-readable raw file relative path: `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`
- Existing R0 input convention: raw files are discovered from `CG_VARW_RAW_ROOT`; ASR candidate sidecars are loaded from the raw file directory.
- `review_inputs/r0` convention found: `false`
- `R0_REQUIRES_ASR_CANDIDATES=true`
- `ASR_CANDIDATES_GENERATED=false`
- `NEXT_ACTION=run RECD-1 slate anchor recognition`

ASR candidates were not generated in this task because the existing `scripts/slate_number_recognizer.py` only creates expected slate variant framework artifacts; it does not run real ASR and cannot produce honest `asr_start_s` / `asr_end_s` timestamps for this WAV.

No R0 reviewed anchors were created. In particular, this task did not create:

- `reviewed_slate_anchor_manifest.csv`
- `raw_marker_review.csv`
- `split_plan_from_raw_markers.csv`

## Explicit Non-Actions

- Split executed: `false`
- Clean segment generated: `false`
- Unit preview generated: `false`
- R1 started: `false`
- `03_samples/` written by this task: `false` (`pre-existing, not touched`)
- `04_outputs/` written by this task: `false` (`pre-existing, not touched`)
- `sample_assets.csv` at repo root written by this task: `false` (`not present`)
- `recording_segments.csv` at repo root written by this task: `false` (`not present`)
- `recording_items_enriched.jsonl` written by this task: `false` (`not present`)
- `tools/cg-varw/review_outputs/` written by this task: `false` (`pre-existing .gitignore/README only, not touched`)
- Render executed: `false`
- ML training data generated: `false`
- `QINIST_001` modified: `false`
- score events / gesture templates / canon / sources modified: `false`

## Validation Results

Initial inspection:

```text
git status --short --untracked-files=all
?? scripts/generate_baiya_recording_plan.py
```

WAV metadata/checksum smoke test:

```text
file_format=wav
codec_or_encoding=NONE (not compressed)
sample_rate=44100
bit_depth=24
channels=2
duration_s=115.170476
file_size_bytes=30475814
checksum_sha256=f9f3c29a0b289c87106cf6994a1d789ee1055ab13230b8fef8dbf0005e1e814e
copy_checksum_match=true
target_mode=0444
```

R0 raw scanner smoke test:

```text
CG_VARW_RAW_ROOT=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio
raw_root_mode real
matched_count 1
matched_file RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav 30475814 wav
```

Final validation commands were run after report creation:

```text
git diff --check
PASS
```

```text
manifest row validation
PASS
```

```text
forbidden output check
PASS: no forbidden root outputs created; legacy 03_samples/, 04_outputs/, and tools/cg-varw/review_outputs/ were pre-existing and not touched.
```

Final git status:

```text
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/raw_audio_inventory.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/session_manifest.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/take_manifest.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_RECD0_BAIYA_BATCH01_RAW_ARCHIVE_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

`scripts/generate_baiya_recording_plan.py` was pre-existing before this task and was not modified.
