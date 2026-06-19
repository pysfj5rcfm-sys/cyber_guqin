# CG-RECD2 Baiya Batch01 Controlled Split Preview Report v0.1

Task: `CG-RECD2_BAIYA_BATCH01_CONTROLLED_SPLIT_PREVIEW_FROM_R0`

## Summary

- Final conclusion: `RECD2_READY__R1_INTAKE_READY`
- Recording session: `RS_XWC_002_BAIYA_PILOT`
- Performer: `QINIST_002` / 白牙
- Piece: `XWC` / 仙翁操
- Batch scope: `batch01` / `T001-T010`
- Split preview created rows: `10`
- Blockers: `0`
- R1 intake status: `READY_FOR_R1_REVIEW`
- R1 human review performed: `false`

This run consumed the latest re-exported R0 outputs after the terminal take fix. `T010` is treated as terminal take with `terminal_boundary_policy=raw_end`; both `unit_end_s` and `suggested_clean_end_s` use `115.170476`.

## R0 Exports

Source export directory:

```text
tools/cg-varw/review_outputs/r0/exports/UUlOSVNUXzAwMi9YV0MvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVC9yYXcvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVF9iYXRjaDAxX1QwMDEtVDAxMC53YXY/
```

Archived R0 reviewed outputs:

- `reviewed_slate_anchor_manifest`: source `tools/cg-varw/review_outputs/r0/exports/UUlOSVNUXzAwMi9YV0MvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVC9yYXcvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVF9iYXRjaDAxX1QwMDEtVDAxMC53YXY/reviewed_slate_anchor_manifest.csv` -> archive `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/batch01/reviewed_slate_anchor_manifest.batch01.csv`; sha256 `2c8747a1b6feeb907e99580a23b66a51d0c2ef3b7f8b8ab2c8a1be68a84abd50`
- `raw_marker_review`: source `tools/cg-varw/review_outputs/r0/exports/UUlOSVNUXzAwMi9YV0MvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVC9yYXcvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVF9iYXRjaDAxX1QwMDEtVDAxMC53YXY/raw_marker_review.csv` -> archive `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/batch01/raw_marker_review.batch01.csv`; sha256 `719ea5a5cadc0ee1bfdb3555d5bdbdfe5a2aeb9b9fa6a50a14209e5c87eca09e`
- `split_plan_from_raw_markers`: source `tools/cg-varw/review_outputs/r0/exports/UUlOSVNUXzAwMi9YV0MvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVC9yYXcvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVF9iYXRjaDAxX1QwMDEtVDAxMC53YXY/split_plan_from_raw_markers.csv` -> archive `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/batch01/split_plan_from_raw_markers.batch01.csv`; sha256 `44988aa328c012ed23d3f4c1e3c59a5db6d73c7c65c33a18d5908838b539fd19`

R0 CSV validation result:

```text
reviewed_slate_anchor_manifest.csv rows=10 T001-T010
split_plan_from_raw_markers.csv rows=10 T001-T010
raw_marker_review.csv rows=29
T010 terminal_boundary_policy=raw_end
T010 terminal_unit_end_s=115.170476
T010 next_slate_marker_source=terminal_raw_end
validation=PASS
```

`raw_marker_review.csv` was archived for audit/provenance only and was not used as the primary cutting input.

## Raw Master

- Raw master path: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`
- Checksum sha256: `f9f3c29a0b289c87106cf6994a1d789ee1055ab13230b8fef8dbf0005e1e814e`
- Duration: `115.170476`
- Sample rate: `44100`
- Bit depth: `24`
- Channels: `2`
- Raw master modified: `false`

## Split Preview Outputs

Output root:

```text
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/
```

Generated:

- unit previews: `10`
- clean previews: `10`
- split manifest: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/manifests/recd2_split_preview_manifest.csv`
- R1 intake pointer: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/manifests/r1_intake_pointer.yaml`
- R1 manifest for CG-VARW real split root: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/r1_synthetic_split_manifest.json`

Per-take boundaries:

| take | unit_start_s | unit_end_s | clean_start_s | clean_end_s | clean_duration_s | split_status |
| --- | --- | --- | --- | --- | --- | --- |
| `T001` | `0.890000` | `11.090000` | `4.290000` | `11.090000` | `6.800000` | `preview_created` |
| `T002` | `12.140000` | `22.110000` | `15.950000` | `22.110000` | `6.160000` | `preview_created` |
| `T003` | `22.760000` | `38.580000` | `27.680000` | `38.580000` | `10.900000` | `preview_created` |
| `T004` | `38.580000` | `48.140000` | `40.880000` | `48.140000` | `7.260000` | `preview_created` |
| `T005` | `48.140000` | `57.520000` | `49.540000` | `57.520000` | `7.980000` | `preview_created` |
| `T006` | `57.520000` | `67.320000` | `59.930000` | `67.320000` | `7.390000` | `preview_created` |
| `T007` | `67.320000` | `78.060000` | `69.360000` | `78.060000` | `8.700000` | `preview_created` |
| `T008` | `78.060000` | `88.700000` | `80.560000` | `88.700000` | `8.140000` | `preview_created` |
| `T009` | `88.700000` | `100.060000` | `90.710000` | `100.060000` | `9.350000` | `preview_created` |
| `T010` | `100.060000` | `115.170476` | `102.060000` | `115.170476` | `13.110476` | `preview_created` |

T010 end policy:

```text
terminal_take=T010
terminal_boundary_policy=raw_end
terminal_reason=no_next_slate_in_batch
unit_end_s=115.170476
suggested_clean_end_s=115.170476
next_slate_marker_source=terminal_raw_end
```

## R1 Intake

R1 intake is ready for review-only workflow:

```text
split_root=02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01
batch_id=batch01
manifest=manifests/recd2_split_preview_manifest.csv
r1_status=READY_FOR_R1_REVIEW
requires_r1_review=true
review_only=true
production_grade=false
not_sample_assets=true
```

No R1 review decisions were made. All clean preview segments remain `segment_status=candidate` / `review_status=not_started` in the R1 intake manifest.

## Explicit Non-Actions

- R1 review performed: `false`
- render executed: `false`
- ML training data generated: `false`
- `03_samples/` written by this task: `false` (`pre-existing, not touched`)
- root `sample_assets.csv` written by this task: `false` (`not present`)
- root `recording_segments.csv` written by this task: `false` (`not present`)
- `recording_items_enriched.jsonl` written by this task: `false` (`not present`)
- `04_outputs/` written by this task: `false` (`pre-existing, not touched`)
- raw master modified: `false`
- score events / gesture templates / canon / sources modified: `false`

## Validation Results

R0 export validation:

```text
PASS
reviewed_rows=10
split_rows=10
marker_rows=29
T010 unit_end_s=115.170476
T010 suggested_clean_end_s=115.170476
```

Audio metadata validation:

```text
PASS
rows=10
unit/clean WAV files exist
preview durations match manifest approximately
sample_rate=44100
channels=2
bit_depth=24
```

Final validation commands were run after this report was written:

```text
git diff --check
PASS
```

```text
split manifest validation
PASS
```

```text
forbidden output check
PASS
```

Final git status:

```text
See final assistant response for the fresh command output.
```
