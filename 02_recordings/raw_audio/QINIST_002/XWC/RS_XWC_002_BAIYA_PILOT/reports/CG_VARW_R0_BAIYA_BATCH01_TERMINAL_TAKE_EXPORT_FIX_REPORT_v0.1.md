# CG-VARW R0 Baiya Batch01 Terminal Take Export Fix Report v0.1

Task: `CG-VARW-R0_BAIYA_BATCH01_TERMINAL_TAKE_EXPORT_FIX`

## Summary

- Final conclusion: `R0_TERMINAL_EXPORT_READY__RECD2_CAN_RETRY`
- Recording session: `RS_XWC_002_BAIYA_PILOT`
- Performer: `QINIST_002` / 白牙
- Batch scope: `batch01` / `T001-T010`
- Terminal take: `T010`
- Split executed: `false`
- R1 started: `false`

## Root Cause

RECD-2 was blocked because current R0 export logic treated every R0 unit as requiring these three required markers:

```text
slate_start
slate_end
next_slate_start
```

That rule is correct for non-terminal takes `T001-T009`, but wrong for terminal take `T010`, which has no next slate in `batch01`.

The R0 draft showed that `T010` was already reviewed at marker level:

```text
boundary_type=file_end
slate_start review_status=accepted time=100.060
slate_end review_status=accepted time=102.060
next_slate_start absent
tail_end absent
```

But because exporter status derivation required `next_slate_start`, it produced:

```text
review_status=candidate
unit_status=needs_review
```

and skipped `T010` in `split_plan_from_raw_markers.csv`.

Classification:

```text
B. User had confirmed terminal slate markers, but exporter did not support terminal take.
C. R0 UI derived terminal take as needs_review because next_slate_start was fixed-required.
D. split_plan writer skipped terminal take because next_slate_start was fixed-required.
```

## Files Modified

- `tools/cg-varw/backend/app/services/r0_export_writer.py`
- `tools/cg-varw/backend/app/tests/test_csv_contracts.py`
- `tools/cg-varw/frontend/src/mock/rawReviewMock.ts`
- `tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx`

## Logic Changed

Backend exporter:

- Detects terminal units with `boundary_type=file_end` and no `next_slate_start` marker.
- Allows terminal R0 acceptance when `slate_start` and `slate_end` are accepted.
- Uses raw WAV duration as terminal unit end.
- Writes explicit terminal fields:
  - `is_terminal_take=true`
  - `terminal_boundary_policy=raw_end`
  - `terminal_unit_end_s=115.170476`
  - `terminal_reason=no_next_slate_in_batch`
  - `next_slate_marker_source=terminal_raw_end`
- Does not create a fake real next slate marker.

Frontend R0 derived state:

- Terminal take required markers are now `slate_start` and `slate_end`.
- Non-terminal take required markers remain `slate_start`, `slate_end`, and `next_slate_start`.
- Boundary note now states that terminal take has no next slate and uses raw file end.

Regression test added:

```text
test_r0_terminal_take_uses_file_end_boundary_without_next_slate
```

The test failed before the exporter fix because `_is_plannable(unit)` returned `false`; it passes after the fix.

## Re-Exported R0 Outputs

R0 export directory:

```text
tools/cg-varw/review_outputs/r0/exports/UUlOSVNUXzAwMi9YV0MvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVC9yYXcvUlNfWFdDXzAwMl9CQUlZQV9QSUxPVF9iYXRjaDAxX1QwMDEtVDAxMC53YXY/
```

Files:

- `reviewed_slate_anchor_manifest.csv`
- `raw_marker_review.csv`
- `split_plan_from_raw_markers.csv`

These files remain under `tools/cg-varw/review_outputs/`; they were not force-added to git. RECD-2 should archive them in its own task.

## Export Validation

Validated after re-export:

```text
reviewed_rows=10
split_rows=10
marker_rows=29
recording_take_no=T001,T002,T003,T004,T005,T006,T007,T008,T009,T010
errors=[]
```

T010 in `reviewed_slate_anchor_manifest.csv`:

```text
review_status=accepted
unit_status=confirmed
is_terminal_take=true
terminal_boundary_policy=raw_end
terminal_unit_end_s=115.170476
terminal_reason=no_next_slate_in_batch
next_slate_start_s=115.170476
next_slate_marker_source=terminal_raw_end
```

T010 in `split_plan_from_raw_markers.csv`:

```text
unit_start_s=100.060
unit_end_s=115.170476
suggested_clean_start_s=102.060
suggested_clean_end_s=115.170476
is_terminal_take=true
terminal_boundary_policy=raw_end
terminal_unit_end_s=115.170476
terminal_reason=no_next_slate_in_batch
next_slate_marker_source=terminal_raw_end
not_executed=true
not_recording_segments=true
not_sample_assets=true
```

Contract validator warnings remain for upstream provenance blanks such as `event_id`, `event_range`, `gesture_id`, `expected_sample_type`, `guqin_start_s`, and `tail_end_s`. These are warnings, not blockers, and were pre-existing relative to this terminal export rule.

## Non-Actions

- split executed: `false`
- unit preview generated: `false`
- clean preview generated: `false`
- R1 review started: `false`
- `03_samples/` written: `false`
- root `sample_assets.csv` written: `false`
- root `recording_segments.csv` written: `false`
- `recording_items_enriched.jsonl` written: `false`
- `04_outputs/` written: `false`
- render executed: `false`
- ML training data generated: `false`
- raw master modified: `false`
- score events / gesture templates / canon / sources modified: `false`

## Validation Commands

Regression test, red state before fix:

```text
FAIL: test_r0_terminal_take_uses_file_end_boundary_without_next_slate
AssertionError: False is not true
```

Regression test after fix:

```text
Ran 1 test in 0.001s
OK
```

Backend contract tests:

```text
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_csv_contracts
Ran 3 tests in 0.001s
OK
```

Backend compile:

```text
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m compileall app
PASS
```

Frontend typecheck:

```text
npm run typecheck
PASS
```

Frontend build:

```text
npm run build
PASS
```

Final validation commands were run after this report was created:

```text
git diff --check
PASS
```

```text
R0 export validation
PASS
```

```text
forbidden output check
PASS
```

Final git status:

```text
M tools/cg-varw/backend/app/services/r0_export_writer.py
M tools/cg-varw/backend/app/tests/test_csv_contracts.py
M tools/cg-varw/frontend/src/mock/rawReviewMock.ts
M tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R0_BAIYA_BATCH01_TERMINAL_TAKE_EXPORT_FIX_REPORT_v0.1.md
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/reports/CG_RECD2_BAIYA_BATCH01_CONTROLLED_SPLIT_PREVIEW_REPORT_v0.1.md
?? scripts/generate_baiya_recording_plan.py
```

`scripts/generate_baiya_recording_plan.py` was pre-existing and was not modified by this task. The RECD-2 blocked report is present as an untracked report artifact and was not modified by the terminal export fix.

## Next Action

R0 terminal export is ready. RECD-2 can be retried and should consume the re-exported R0 three-file set. The next RECD-2 task should archive the R0 reviewed outputs into the session `r0_review/batch01/` directory before generating split previews.

