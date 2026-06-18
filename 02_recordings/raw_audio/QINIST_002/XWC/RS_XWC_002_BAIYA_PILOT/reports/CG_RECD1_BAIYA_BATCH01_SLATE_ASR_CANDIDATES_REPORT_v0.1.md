# CG-RECD1 Baiya Batch01 Slate ASR Candidates Report v0.1

Task: `CG-RECD1_BAIYA_BATCH01_SLATE_ASR_CANDIDATES`

## Summary

- Final conclusion: `RECD1_READY__R0_CANDIDATES_PARTIAL`
- Recording session: `RS_XWC_002_BAIYA_PILOT`
- Performer: `QINIST_002` / 白牙
- Piece: `XWC` / 仙翁操
- Batch scope: `batch01` / `T001-T010` only
- R1 status: `NOT_STARTED`
- R1 reason: `R1 requires RECD-2 controlled split preview outputs after R0 reviewed anchors.`

The ASR runtime was available and produced real transcript timestamps. Candidate rows were generated for all expected takes, but `T004` and `T008` have duplicate ASR matches and must be resolved during human R0 review.

## Inputs

- Input raw WAV: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`
- Input take manifest: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/manifests/take_manifest.csv`
- Raw master checksum before/after RECD-1: `f9f3c29a0b289c87106cf6994a1d789ee1055ab13230b8fef8dbf0005e1e814e`
- Raw master modified: `false`

First inspection confirmed:

- `take_manifest.csv` contains exactly 10 rows.
- `batch_id=batch01` for every row.
- `recording_take_no=T001-T010`.
- `batch_take_no=001-010`.
- `slate_no=001-010`.
- `source_raw_audio` points to the registered raw master.

## ASR Runtime

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
- Transcript segment count: `12`

Runtime notes:

- The model loaded from local Hugging Face cache: `models--Systran--faster-whisper-medium`.
- A cache write warning was emitted while writing the model ref, but ASR completed.
- `faster_whisper.feature_extractor` emitted numeric runtime warnings during feature extraction; transcript output was still produced and preserved as diagnostic data.

## Outputs

- Candidate manifest: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_slate_anchor_candidates.csv`
- Transcript segments: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_asr_transcript_segments.jsonl`
- Match report: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_asr_match_report.json`
- R0 JSON sidecar: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.asr_candidates.json`
- R0 CSV candidate pointer: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.slate_anchor_candidates.csv`

The R0 JSON sidecar is intentionally next to the raw WAV because current CG-VARW R0 loads candidates from the raw file directory. The CSV pointer mirrors the RECD-1 candidate manifest fields. The JSON sidecar is loaded first by R0 and omits missing marker keys per row, avoiding empty marker parsing.

## Slate Matching Summary

| take | slate_no | expected | recognized | asr_start_s | asr_end_s | confidence | match_status | candidate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `T001` | `001` | `零零幺` | `001` | `4.140` | `6.940` | `0.933028` | `matched` | `candidate` | High `no_speech_prob=0.782401`; verify boundary. |
| `T002` | `002` | `零零二` | `002` | `6.940` | `16.000` | `0.973611` | `matched` | `candidate` | High `no_speech_prob=0.782401`; verify boundary. |
| `T003` | `003` | `零零三` | `003` | `16.860` | `27.680` | `0.983133` | `matched` | `candidate` | High `no_speech_prob=0.782401`; verify boundary. |
| `T004` | `004` | `零零四` | `004` | `38.580` | `41.380` | `0.961692` | `duplicate` | `ambiguous` | Duplicate ASR segment indices: `3,4`. |
| `T005` | `005` | `零零五` | `005` | `48.140` | `49.540` | `0.848296` | `matched` | `candidate` | Candidate only. |
| `T006` | `006` | `零零六` | `006` | `57.520` | `60.320` | `0.923687` | `matched` | `candidate` | Candidate only. |
| `T007` | `007` | `零零七` | `007` | `67.320` | `69.960` | `0.961818` | `matched` | `candidate` | Candidate only. |
| `T008` | `008` | `零零八` | `008` | `78.060` | `80.860` | `0.893965` | `duplicate` | `ambiguous` | Duplicate ASR segment indices: `8,9`. |
| `T009` | `009` | `零零九` | `009` | `88.700` | `90.600` | `0.706243` | `matched` | `candidate` | Candidate only. |
| `T010` | `010` | `零幺零` | `010` | `100.060` | `102.060` | `0.925955` | `matched` | `candidate` | Candidate only; no next slate marker. |

Counts:

- expected_take_count: `10`
- candidate_row_count: `10`
- matched_count: `8`
- ambiguous_count: `2`
- duplicate_count: `2`
- unmatched_count: `0`

All candidate rows use:

- `requires_manual_review=true`
- `review_only=true`
- `production_grade=false`
- `not_sample_assets=true`
- `not_render_executed=true`
- `not_ml_training_data=true`

No row uses `accepted`, `human_verified`, `reviewed`, `render_usable`, `sample_candidate`, or `production`.

## R0 Intake Compatibility

R0 raw root used for smoke test:

```text
CG_VARW_RAW_ROOT=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio
```

R0 can discover the raw WAV:

```text
raw_root_mode real
raw_matched_count 1
```

R0 can discover the ASR candidate sidecar:

```text
candidate_found True
candidate_source RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.asr_candidates.json
candidate_count 10
review_unit_count 10
unit_ids ['T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008', 'T009', 'T010']
marker_counts [3, 3, 3, 3, 3, 3, 3, 3, 3, 2]
```

The `marker_counts` are candidate-only R0 helpers. They are not reviewed anchors and are not split instructions.

## Explicit Non-Actions

- R0 reviewed anchors created: `false`
- `reviewed_slate_anchor_manifest.csv` created: `false`
- `raw_marker_review.csv` created: `false`
- `split_plan_from_raw_markers.csv` created: `false`
- Split executed: `false`
- Unit preview generated: `false`
- Clean preview generated: `false`
- R1 started: `false`
- Render executed: `false`
- ML training data generated: `false`
- `03_samples/` written by this task: `false` (`pre-existing, not touched`)
- `04_outputs/` written by this task: `false` (`pre-existing, not touched`)
- Root `sample_assets.csv` written by this task: `false` (`not present`)
- Root `recording_segments.csv` written by this task: `false` (`not present`)
- `recording_items_enriched.jsonl` written by this task: `false` (`not present`)
- `tools/cg-varw/review_outputs/` written by this task: `false` (`pre-existing .gitignore/README only, not touched`)
- score events / gesture templates / canon / sources modified: `false`

## Validation Results

Initial git status:

```text
?? scripts/generate_baiya_recording_plan.py
```

Candidate manifest validation:

```text
PASS
rows=10
recording_take_no=T001,T002,T003,T004,T005,T006,T007,T008,T009,T010
candidate_status=candidate,candidate,candidate,ambiguous,candidate,candidate,candidate,ambiguous,candidate,candidate
forbidden_values=[]
```

R0 intake compatibility validation:

```text
PASS
raw_root_mode=real
raw_matched_count=1
candidate_found=True
candidate_count=10
review_unit_count=10
```

Final validation commands:

```text
git diff --check
PASS
```

```text
forbidden output check
PASS: no forbidden root outputs created; legacy 03_samples/, 04_outputs/, and tools/cg-varw/review_outputs/ were pre-existing and not touched.
```

Final git status:

```text
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_asr_match_report.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_asr_transcript_segments.jsonl
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.asr_candidates.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.slate_anchor_candidates.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_RECD1_BAIYA_BATCH01_SLATE_ASR_CANDIDATES_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

`scripts/generate_baiya_recording_plan.py` was pre-existing and was not modified by this task.

## Next Action

Open CG-VARW R0 with:

```bash
CG_VARW_RAW_ROOT=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio
```

Then perform human R0 review of the candidate slate anchors, especially:

- `T001-T003`: verify long ASR segment end times and high `no_speech_prob`.
- `T004`: resolve duplicate slate candidate.
- `T008`: resolve duplicate slate candidate.

Only after human R0 review may `reviewed_slate_anchor_manifest.csv` and downstream RECD-2 split preview inputs be produced by a separate authorized task.

