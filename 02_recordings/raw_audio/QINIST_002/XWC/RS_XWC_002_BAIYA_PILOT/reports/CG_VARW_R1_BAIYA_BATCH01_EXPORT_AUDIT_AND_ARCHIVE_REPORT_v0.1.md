# CG-VARW R1 Baiya Batch01 Export Audit and Archive Report v0.1

Task: `CG-VARW-R1_BAIYA_BATCH01_EXPORT_AUDIT_AND_ARCHIVE`  
Session: `RS_XWC_002_BAIYA_PILOT`  
Batch: `batch01 / T001-T010`  
Conclusion: `R1_EXPORT_AUDIT_READY__BATCH01_CAN_ENTER_SAMPLE_CANDIDATE_GATE`

## 1. R1 Export Source Paths

R1 export three-file set was found:

```text
tools/cg-varw/review_outputs/r1/exports/batch01/reviewed_render_anchors.csv
tools/cg-varw/review_outputs/r1/exports/batch01/split_marker_review.csv
tools/cg-varw/review_outputs/r1/exports/batch01/segment_qc_sheet.csv
```

The source exports were audited in place and were not modified.

## 2. R1 Archive Paths

R1 reviewed outputs were archived to:

```text
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/reviewed_render_anchors.batch01.csv
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/split_marker_review.batch01.csv
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/segment_qc_sheet.batch01.csv
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/r1_review_archive_manifest.yaml
```

Archive checksums:

```text
reviewed_render_anchors.batch01.csv sha256=10c7ce29badf349c7630109a9bc062fa8e778661c50f7cd42767fe6ccd4d7422
split_marker_review.batch01.csv sha256=cb785738013c501cf1a0f52376e0a31b32d378042360a9f39b00aa4af1088d51
segment_qc_sheet.batch01.csv sha256=3f66b9c59c87e687df533597d45232839136c8428e36d3c3b1143d1665a909c7
r1_review_archive_manifest.yaml sha256=d573f682fcc1301e6f4469de248a413f67cacf142871012aaead3042c4990327
```

The archive manifest includes:

```text
review_only=true
production_grade=false
not_sample_assets=true
not_render_executed=true
not_ml_training_data=true
requires_sample_candidate_gate=true
```

## 3. reviewed_render_anchors.csv Validation

Result: passed.

```text
row_count=10
recording_take_no covers T001-T010
recording_session_id=RS_XWC_002_BAIYA_PILOT
qinist_id=QINIST_002
piece_id=XWC
render_anchor_s is non-empty for all rows
render_anchor_s is within clean segment duration for all rows
tail_end_s is within clean segment duration for all rows
review_status is not not_started
segment_status is not candidate/not_started
review_only=true for all rows
production_grade=false for all rows
not_sample_assets=true for all rows
```

Previously blocked T001/T002 tail markers now pass:

```text
T001 tail_end_s=6.757 <= clean duration 6.800
T002 tail_end_s=6.132 <= clean duration 6.160
```

## 4. split_marker_review.csv Validation

Result: passed with one non-blocking warning.

```text
row_count=40
recording_take_no covers T001-T010
each segment has exactly 4 marker rows:
  pre_idle_end
  gesture_start
  render_anchor
  tail_end
all marker time_s values are within clean segment duration
all render_anchor markers are accepted
marker review_status counts:
  accepted=40
production_grade=false for all rows
review_only=true for all rows
not_sample_assets=true for all rows
```

Warning:

```text
T005 render_anchor has adjusted source but nudge_total_ms=0.
This is retained as an audit note only; marker status is accepted and the timestamp is within duration.
```

## 5. segment_qc_sheet.csv Validation

Result: passed.

```text
row_count=10
recording_take_no covers T001-T010
segment_status counts:
  render_usable=10
review_only=true for all rows
production_grade=false for all rows
not_sample_assets=true for all rows
not_render_executed=true for all rows
not_ml_training_data=true for all rows
needs_retake/rejected/excluded: none
```

Note: `render_usable` here is R1 review output status only. It was not promoted to sample asset status and no sample candidate gate was executed.

## 6. Cross-check Against RECD-2 Manifest

RECD-2 manifest:

```text
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/manifests/recd2_split_preview_manifest.csv
```

Clean preview files exist for T001-T010. R1 reviewed rows correspond to the RECD-2 clean previews.

Confirmed WAV duration examples:

```text
T001 clean preview duration_s=6.800000
T002 clean preview duration_s=6.160000
T010 clean preview duration_s=13.110476
```

T010 terminal segment check:

```text
recording_take_no=T010
clean_start_s=102.060000
clean_end_s=115.170476
duration_s=13.110476
RECD-2 notes=terminal take uses raw_end policy; no real next slate
R1 render_anchor_s=2.775
R1 tail_end_s=4.475
T010 marker times are within clean segment duration
```

T010 passes the terminal segment audit.

## 7. T001-T010 R1 Status Summary

| take | segment_id | duration_s | render_anchor_s | tail_end_s | review_status | segment_status | marker status summary |
|---|---|---:|---:|---:|---|---|---|
| T001 | RECD2_BATCH01_T001 | 6.800000 | 2.716 | 6.757 | accepted | render_usable | accepted=4 |
| T002 | RECD2_BATCH01_T002 | 6.160000 | 1.717 | 6.132 | accepted | render_usable | accepted=4 |
| T003 | RECD2_BATCH01_T003 | 10.900000 | 1.235 | 6.641 | accepted | render_usable | accepted=4 |
| T004 | RECD2_BATCH01_T004 | 7.260000 | 0.498 | 2.606 | accepted | render_usable | accepted=4 |
| T005 | RECD2_BATCH01_T005 | 7.980000 | 2.046 | 4.753 | accepted | render_usable | accepted=4 |
| T006 | RECD2_BATCH01_T006 | 7.390000 | 0.423 | 1.915 | accepted | render_usable | accepted=4 |
| T007 | RECD2_BATCH01_T007 | 8.700000 | 0.513 | 2.796 | accepted | render_usable | accepted=4 |
| T008 | RECD2_BATCH01_T008 | 8.140000 | 0.316 | 4.341 | accepted | render_usable | accepted=4 |
| T009 | RECD2_BATCH01_T009 | 9.350000 | 1.526 | 3.766 | accepted | render_usable | accepted=4 |
| T010 | RECD2_BATCH01_T010 | 13.110476 | 2.775 | 4.475 | accepted | render_usable | accepted=4 |

## 8. Sample Candidate Gate Recommendation

Recommendation:

```text
Batch01 can enter sample candidate gate.
```

Boundary:

```text
This task did not execute sample candidate gate.
The archived R1 outputs remain review-only and are not sample assets.
A separate sample candidate gate task is required before any 03_samples/sample_assets work.
```

## 9. Boundary Confirmations

Confirmed:

```text
No 03_samples/ files were written.
No sample_assets.csv was written.
No recording_segments.csv was written.
No recording_items_enriched.jsonl was written.
No 04_outputs/ files were written.
No render was executed.
No ML training data was generated.
Raw master was not modified.
RECD-2 manifest was not modified.
R0 reviewed CSVs were not modified.
R1 source exports were not modified.
```

Pre-existing directories, not touched:

```text
03_samples/
04_outputs/
tools/cg-varw/review_outputs/
```

## 10. Validation Command Results

Initial inspection:

```text
git status --short --untracked-files=all
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R1_BAIYA_BATCH01_EXPORT_AUDIT_AND_ARCHIVE_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

R1 export discovery:

```text
reviewed_render_anchors.csv: found
split_marker_review.csv: found
segment_qc_sheet.csv: found
```

CSV audit:

```text
reviewed_render_anchors rows=10
split_marker_review rows=40
segment_qc_sheet rows=10
CSV validation result=PASS
warnings:
  T005 render_anchor adjusted source but nudge_total_ms=0
```

Archive validation:

```text
r1_review/batch01 exists=true
reviewed_render_anchors.batch01.csv exists=true rows=10 sha256=10c7ce29badf349c7630109a9bc062fa8e778661c50f7cd42767fe6ccd4d7422
split_marker_review.batch01.csv exists=true rows=40 sha256=cb785738013c501cf1a0f52376e0a31b32d378042360a9f39b00aa4af1088d51
segment_qc_sheet.batch01.csv exists=true rows=10 sha256=3f66b9c59c87e687df533597d45232839136c8428e36d3c3b1143d1665a909c7
r1_review_archive_manifest.yaml exists=true sha256=d573f682fcc1301e6f4469de248a413f67cacf142871012aaead3042c4990327
production_grade=true rows=0
```

Forbidden output git check:

```text
git status --short -- 03_samples 04_outputs sample_assets.csv recording_segments.csv recording_items_enriched.jsonl tools/cg-varw/review_outputs
<no output>
```

Git status after archive:

```text
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/r1_review_archive_manifest.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/reviewed_render_anchors.batch01.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/segment_qc_sheet.batch01.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/split_marker_review.batch01.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R1_BAIYA_BATCH01_EXPORT_AUDIT_AND_ARCHIVE_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

## 11. Final Conclusion

```text
R1_EXPORT_AUDIT_READY__BATCH01_CAN_ENTER_SAMPLE_CANDIDATE_GATE
```
