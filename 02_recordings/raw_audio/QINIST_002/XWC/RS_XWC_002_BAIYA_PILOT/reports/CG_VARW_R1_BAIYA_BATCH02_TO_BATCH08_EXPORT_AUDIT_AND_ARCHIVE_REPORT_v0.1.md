# CG VARW R1 Baiya Batch02-Batch08 Export Audit And Archive Report v0.1

## Final Conclusion

`R1_EXPORT_AUDIT_READY__BATCH02_TO_BATCH08_CAN_ENTER_HUMAN_LISTENING_GATE`

R1 export structural validation passed for batch02-batch08. The archive covers T011-T071 exactly once; all 61 segment-level rows are `render_usable`; all 244 R1 markers are `accepted`. This is an audit/archive result only, not sample ingest and not render output.

## R1 Export Source Paths

- batch02 (T011-T020):
  - `tools/cg-varw/review_outputs/r1/exports/batch02/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch02/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch02/segment_qc_sheet.csv`
- batch03 (T021-T030):
  - `tools/cg-varw/review_outputs/r1/exports/batch03/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch03/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch03/segment_qc_sheet.csv`
- batch04 (T031-T040):
  - `tools/cg-varw/review_outputs/r1/exports/batch04/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch04/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch04/segment_qc_sheet.csv`
- batch05 (T041-T050):
  - `tools/cg-varw/review_outputs/r1/exports/batch05/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch05/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch05/segment_qc_sheet.csv`
- batch06 (T051-T060):
  - `tools/cg-varw/review_outputs/r1/exports/batch06/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch06/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch06/segment_qc_sheet.csv`
- batch07 (T061-T070):
  - `tools/cg-varw/review_outputs/r1/exports/batch07/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch07/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch07/segment_qc_sheet.csv`
- batch08 (T071):
  - `tools/cg-varw/review_outputs/r1/exports/batch08/reviewed_render_anchors.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch08/split_marker_review.csv`
  - `tools/cg-varw/review_outputs/r1/exports/batch08/segment_qc_sheet.csv`

## Per-Batch Archive Paths

- batch02: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/`
- batch03: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/`
- batch04: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/`
- batch05: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/`
- batch06: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/`
- batch07: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/`
- batch08: `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/`

## Required Row Counts

- `reviewed_render_anchors.csv`: 61 rows
- `segment_qc_sheet.csv`: 61 rows
- `split_marker_review.csv`: 244 rows
- Marker formula: 61 segments x 4 marker types = 244

## Per-Batch Segment And Marker Status Counts

- batch02 (T011-T020): segment_count=10, render_usable=10, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=40, accepted=40, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0
- batch03 (T021-T030): segment_count=10, render_usable=10, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=40, accepted=40, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0
- batch04 (T031-T040): segment_count=10, render_usable=10, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=40, accepted=40, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0
- batch05 (T041-T050): segment_count=10, render_usable=10, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=40, accepted=40, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0
- batch06 (T051-T060): segment_count=10, render_usable=10, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=40, accepted=40, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0
- batch07 (T061-T070): segment_count=10, render_usable=10, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=40, accepted=40, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0
- batch08 (T071): segment_count=1, render_usable=1, reference_only=0, unclear=0, needs_retake=0, rejected=0, excluded=0, candidate=0; markers=4, accepted=4, marker_unclear=0, marker_needs_retake=0, marker_rejected=0, marker_candidate=0

## Marker Type Counts

- `pre_idle_end`: 61
- `gesture_start`: 61
- `render_anchor`: 61
- `tail_end`: 61

## Hard Errors

None.

## Warnings / Blockers

None. No segment has `reference_only`, `unclear`, `needs_retake`, `rejected`, `excluded`, or `candidate`; no marker has non-accepted review status.

## T071 Placement Confirmation

T071 is present exactly once at segment level and belongs to `batch08` with `recording_take_no=T071` and `batch_take_no=001`. `batch07` contains T061-T070 only. No T072 row exists.

## Time Boundary Validation Result

Passed. Every segment satisfies `0 <= pre_idle_end_s <= gesture_start_s <= render_anchor_s <= tail_end_s <= clean_preview_duration_s` within audit tolerance. Every `split_marker_review.time_s` is inside the corresponding clean preview duration.

## Source Split Audio Existence Validation Result

Passed. All 61 `source_split_audio` values resolve to existing clean preview WAV files under `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batchXX/clean_previews/` or an equivalent resolved path.

## Archive Checksum Summary

- batch02:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/reviewed_render_anchors.batch02.csv`: `bbb52b18a40a11bb47b41f56d81eace280fcb11bd65686998d84a3c844a70d72`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/split_marker_review.batch02.csv`: `7941cfcc11728e1f3fd470856aa5d05aa2a7078e6ca2d6762a0efd64877653c4`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/segment_qc_sheet.batch02.csv`: `68a4b3e43388073f7027180f83be5357eb896516a6ad0a898c5d538ad6958288`
- batch03:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/reviewed_render_anchors.batch03.csv`: `5c1fd326b85ad521661bd70d5044b1da8fa51166059af9cd9300cdb46300a0a3`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/split_marker_review.batch03.csv`: `2230d03e78cc2a2e8ade86224f652d6cf2ca591af55735cc8b512de9e27f1714`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/segment_qc_sheet.batch03.csv`: `b5181fa18a8883b94544c9d13045b4ec59a07c9445824f676406e3378c49776d`
- batch04:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/reviewed_render_anchors.batch04.csv`: `6f355a1b019a35d94f189f4969e60b969d771a2bb8263c2a07fb72d89665c7c0`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/split_marker_review.batch04.csv`: `cad501b670d171e79656bea9ca82d8cbebaba0fa3707f918fa88e43362a1dba5`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/segment_qc_sheet.batch04.csv`: `0ec720893e3482bb56b6a42a82c3a12768df7a6827a35e35b74f507af2a21ffe`
- batch05:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/reviewed_render_anchors.batch05.csv`: `b80364a241dbcdc570d21d280e7858d5c1bb375894754f490c96d894728a6858`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/split_marker_review.batch05.csv`: `1acf1ce324dfa39c26001789c2a14b1892787676a49addf414bef6d3354c3c25`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/segment_qc_sheet.batch05.csv`: `cd40f472eb916efff630f537d25f1662931e16b750c83bd70b964e0cd07095c7`
- batch06:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/reviewed_render_anchors.batch06.csv`: `79bfd334e1649d530638acbc16d3af062654529f7f117af48e530143db3cf140`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/split_marker_review.batch06.csv`: `215832ebae67fde615d72aef2be16065d7d206f18522bb68ecdf04ef9fb104be`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/segment_qc_sheet.batch06.csv`: `1fe6baaba548fd6c6302348b9553adf4767e05e4108ba6460f96b531d8dc11b1`
- batch07:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/reviewed_render_anchors.batch07.csv`: `8519b5a1b9a4a262fc6f3680333c6a7a223c8241bd7a199cd1c91e432491817c`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/split_marker_review.batch07.csv`: `9b7d642952b22f121a41967bcca92f636c84b136d2e075abceb37f59814dee3a`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/segment_qc_sheet.batch07.csv`: `2128e47705cf298ac25f3d15e97528f059076870fbc304011222061edf53b89b`
- batch08:
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/reviewed_render_anchors.batch08.csv`: `649c13437b3605198ec026f916fcb75b8f3158d3e9619099e88e3121f87fe5b7`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/split_marker_review.batch08.csv`: `fa4d518c5232b77f691299b73c016428f3ed4955ad64bafaa5f303fe0c471512`
  - `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/segment_qc_sheet.batch08.csv`: `f1f9d2cdf08ddf12547009f0ac94440a4d069ad177afa21a9adbef7ed5ce007c`

## Combined Summary Outputs

- `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02_to_batch08_r1_review_summary.csv`
- `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02_to_batch08_r1_review_summary.json`

## Next Recommended Action

Proceed to human listening gate for batch02-batch08. Do not treat `render_usable` as a sample asset; sample candidate gate remains a separate downstream step.

## Boundary Confirmations

- No sample candidate gate was executed.
- No R1 source export CSV was modified.
- No R1 review was re-run.
- No R1 draft was saved.
- No R1 CSV was re-exported.
- No RECD-2 manifest was modified.
- No split preview was regenerated.
- No raw master was modified.
- No R0 reviewed output was modified.
- No render was executed.
- No ML data was generated.

## Forbidden Output Check

- `03_samples`: pre-existing, not touched
- `04_outputs`: pre-existing, not touched
- `sample_assets.csv`: absent, not written
- `recording_segments.csv`: absent, not written
- `recording_items_enriched.jsonl`: absent, not written

## Validation Command Results

```bash
$ git diff --check
# passed; no output

$ python3 <archive_csv_validation>
csv_validation_errors: 0
reviewed_render_anchors_rows: 61
segment_qc_sheet_rows: 61
split_marker_review_rows: 244
batch_counts: {'batch02': 10, 'batch03': 10, 'batch04': 10, 'batch05': 10, 'batch06': 10, 'batch07': 10, 'batch08': 1}
segment_status_counts: {'render_usable': 61}
marker_status_counts: {'accepted': 244}
marker_type_counts: {'pre_idle_end': 61, 'gesture_start': 61, 'render_anchor': 61, 'tail_end': 61}
t071_anchor: batch08 001

$ python3 <forbidden_output_check>
03_samples pre-existing, not touched
04_outputs pre-existing, not touched
sample_assets.csv absent, not written
recording_segments.csv absent, not written
recording_items_enriched.jsonl absent, not written
```

## Git Status Result

```bash
$ git status --short --untracked-files=all
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/r1_review_archive_manifest.batch02.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/reviewed_render_anchors.batch02.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/segment_qc_sheet.batch02.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02/split_marker_review.batch02.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02_to_batch08_r1_review_summary.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch02_to_batch08_r1_review_summary.json
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/r1_review_archive_manifest.batch03.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/reviewed_render_anchors.batch03.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/segment_qc_sheet.batch03.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch03/split_marker_review.batch03.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/r1_review_archive_manifest.batch04.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/reviewed_render_anchors.batch04.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/segment_qc_sheet.batch04.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch04/split_marker_review.batch04.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/r1_review_archive_manifest.batch05.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/reviewed_render_anchors.batch05.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/segment_qc_sheet.batch05.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch05/split_marker_review.batch05.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/r1_review_archive_manifest.batch06.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/reviewed_render_anchors.batch06.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/segment_qc_sheet.batch06.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch06/split_marker_review.batch06.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/r1_review_archive_manifest.batch07.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/reviewed_render_anchors.batch07.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/segment_qc_sheet.batch07.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch07/split_marker_review.batch07.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/r1_review_archive_manifest.batch08.yaml
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/reviewed_render_anchors.batch08.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/segment_qc_sheet.batch08.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch08/split_marker_review.batch08.csv
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R1_BAIYA_BATCH02_TO_BATCH08_EXPORT_AUDIT_AND_ARCHIVE_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```
