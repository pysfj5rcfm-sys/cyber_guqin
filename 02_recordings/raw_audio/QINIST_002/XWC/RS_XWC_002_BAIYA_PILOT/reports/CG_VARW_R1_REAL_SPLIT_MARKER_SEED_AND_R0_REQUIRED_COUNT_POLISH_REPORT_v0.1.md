# CG-VARW R1 Real Split Marker Seed and R0 Required Count Polish Report v0.1

Task: `CG-VARW-R1_REAL_SPLIT_MARKER_SEED_AND_R0_REQUIRED_COUNT_POLISH`  
Session: `RS_XWC_002_BAIYA_PILOT`  
Batch: `batch01 / T001-T010`  
Conclusion: `R1_REAL_SPLIT_MARKER_SEED_READY__R1_REVIEW_CAN_CONTINUE`

## Scope

This patch only updates CG-VARW R1 real split marker seeding and R0 left-sidebar progress display.

No split was executed. No unit preview or clean preview was regenerated. No R1 human review was performed. No sample ingest, render, or ML workflow was started.

## Root Cause

`r1_synthetic_split_manifest.json` from RECD-2 contains real clean preview segments with an explicit marker object, but all four R1 marker entries are `null`.

Before this patch, `tools/cg-varw/backend/app/services/r1_split_store.py` converted those manifest rows directly into `SplitSegment` models and returned them unchanged. The R1 frontend can nudge, select, save, and export existing markers, but it does not create the initial marker set when all markers are missing.

## Seed Location

Seed markers are generated in the backend split intake layer:

`tools/cg-varw/backend/app/services/r1_split_store.py`

The loader now fills missing R1 markers before returning real split segments. Existing marker objects are preserved and are not overwritten.

## Seed Priority

Each missing marker is seeded using this priority:

1. `manifest`: derive from `manifests/recd2_split_preview_manifest.csv` when valid `guqin_start_s` or `tail_end_s` exists.
2. `audio_seed`: run a lightweight clean-preview WAV energy scan when manifest marker fields are missing.
3. `fallback_default`: use conservative local-time defaults only if manifest and audio seed are unavailable.

All marker timestamps are clean-segment local time, not raw absolute time. Manifest raw times are converted as:

```text
local_time_s = raw_time_s - clean_start_s
```

All generated times are clamped and ordered:

```text
0 <= pre_idle_end <= gesture_start <= render_anchor <= tail_end <= duration_s
```

## Seed Marker Safety

Generated seed markers use:

```text
review_status=candidate
requires_manual_review=true
review_only=true
production_grade=false
not_sample_assets=true
not_render_executed=true
not_ml_training_data=true
```

Allowed seed `source` values are:

```text
manifest
audio_seed
fallback_default
```

No seed marker is exported or marked as accepted, reviewed, human verified, render usable, production, or sample candidate.

## Batch01 Smoke Result

Real R1 split root:

```text
02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01
```

Smoke result:

```text
batches [('batch01', 10, 'real_split_root')]
segment_count 10
marker_counts [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
statuses {'candidate': 40}
sources {'audio_seed': 40}
render_usable_segments []
T010 T010 2.785 12.475 audio_seed audio_seed
```

For the current RECD-2 manifest, `guqin_start_s` and `tail_end_s` are blank for batch01, so all 40 seed markers are derived from `audio_seed`. If future RECD-2 manifests contain valid `guqin_start_s` or `tail_end_s`, those fields take priority and will produce `source=manifest`.

## R0 Sidebar Polish

R0 left-sidebar completion labels no longer show optional marker counts.

Before:

```text
必填3/3 · 可选2/2
```

After:

```text
必填3/3
必填2/2 · 末条
```

This only changes the left-card summary label. R0 optional markers (`guqin_start`, `tail_end`) remain available in the review UI and are still preserved in draft/export logic.

## Files Modified

```text
tools/cg-varw/backend/app/schemas.py
tools/cg-varw/backend/app/services/r1_split_store.py
tools/cg-varw/backend/app/tests/test_r1_marker_seed.py
tools/cg-varw/frontend/src/mock/rawReviewMock.ts
tools/cg-varw/frontend/src/types/cgVarw.ts
```

## Validation

```text
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_r1_marker_seed
PASS: Ran 3 tests in 0.004s

/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_csv_contracts app.tests.test_r1_marker_seed
PASS: Ran 6 tests in 0.005s

/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m compileall app
PASS

CG_VARW_SPLIT_ROOT=.../split_preview/batch01 python R1 real intake smoke
PASS: 10 segments; 4 candidate markers per segment; no render_usable segment by default.

cd tools/cg-varw/frontend && npm run typecheck
PASS

cd tools/cg-varw/frontend && npm run build
PASS

git diff --check
PASS
```

Forbidden output check:

```text
03_samples/: pre-existing, not touched
04_outputs/: pre-existing, not touched
tools/cg-varw/review_outputs/: pre-existing, not touched
sample_assets.csv: top-level file absent
recording_segments.csv: top-level file absent
recording_items_enriched.jsonl: absent
```

## Git Status

Expected changed files after this patch:

```text
M  tools/cg-varw/backend/app/schemas.py
M  tools/cg-varw/backend/app/services/r1_split_store.py
M  tools/cg-varw/frontend/src/mock/rawReviewMock.ts
M  tools/cg-varw/frontend/src/types/cgVarw.ts
?? tools/cg-varw/backend/app/tests/test_r1_marker_seed.py
?? 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_VARW_R1_REAL_SPLIT_MARKER_SEED_AND_R0_REQUIRED_COUNT_POLISH_REPORT_v0.1.md
```

Pre-existing untracked file, not touched:

```text
?? scripts/generate_baiya_recording_plan.py
```

## Final Confirmation

```text
R1_REAL_SPLIT_MARKER_SEED_READY__R1_REVIEW_CAN_CONTINUE
```
