# XWC R0 Recovery Validation Dry Run

- Task: `CG-XWC-MVP-P0B_R0_RECOVERY_VALIDATION_DRY_RUN`
- Phase: Phase 1F-XWC-MVP Passed / Sweep & Review
- Mode: dry-run audit only; no code changes; no R0 data changes.
- Generated: 2026-06-21

## Scope Guard

This report only validates the legacy R0 draft/load issue. It did not fix F, rerun render, generate G/F2, write sample ingest files, write `sample_assets.csv`, write `recording_segments.csv`, create `recording_items_enriched.jsonl`, process the REVIEW bucket, clean the repository, move/delete/archive files, train ML, enter Arrangement Mode, process `scripts/generate_baiya_recording_plan.py`, or modify score/canon/source/schema files.

Only this dry-run report was written.

## Git Evidence

| Check | Result |
| --- | --- |
| Current `HEAD` | `e6657bc601ab5a75d10de8440046797cd4f697a9` |
| `git merge-base --is-ancestor 4899227 HEAD` | PASS, exit 0 |
| `git status --short` | `?? scripts/generate_baiya_recording_plan.py` |

The current `HEAD` is after the F-final baseline commit `4899227`; equality with `4899227` was not required.

## Candidate Directories

| Directory | Exists | Raw `find -type f` count | Interpreted count |
| --- | ---: | ---: | ---: |
| `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/` | yes | 33 | 32 R0 files plus `.DS_Store` |
| `tools/cg-varw/review_outputs/r0/` | yes | 32 | 8 draft JSON plus 24 export CSV |

Important count note: the project-side `r0_review/.DS_Store` is the only reason the raw command returns 33 instead of the expected 32. Excluding `.DS_Store`, the expected 32 R0 files are present.

## File Correspondence

The two candidate locations are not literal basename mirrors. Their correspondence is by batch and role:

| Batch | Project `r0_review` files | cg-varw `review_outputs/r0` files | Status |
| --- | --- | --- | --- |
| batch01 | `r0_export_archive_manifest.csv`; `raw_marker_review.batch01.csv`; `reviewed_slate_anchor_manifest.batch01.csv`; `split_plan_from_raw_markers.batch01.csv` | one draft JSON for `...batch01_T001-T010.wav`; `raw_marker_review.csv`; `reviewed_slate_anchor_manifest.csv`; `split_plan_from_raw_markers.csv` | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch02 | `r0_review_archive_manifest.batch02.yaml`; `raw_marker_review.batch02.csv`; `reviewed_slate_anchor_manifest.batch02.csv`; `split_plan_from_raw_markers.batch02.csv` | one draft JSON for `...batch02_T011-T020.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch03 | `r0_review_archive_manifest.batch03.yaml`; `raw_marker_review.batch03.csv`; `reviewed_slate_anchor_manifest.batch03.csv`; `split_plan_from_raw_markers.batch03.csv` | one draft JSON for `...batch03_T021-T030.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch04 | `r0_review_archive_manifest.batch04.yaml`; `raw_marker_review.batch04.csv`; `reviewed_slate_anchor_manifest.batch04.csv`; `split_plan_from_raw_markers.batch04.csv` | one draft JSON for `...batch04_T031-T040.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch05 | `r0_review_archive_manifest.batch05.yaml`; `raw_marker_review.batch05.csv`; `reviewed_slate_anchor_manifest.batch05.csv`; `split_plan_from_raw_markers.batch05.csv` | one draft JSON for `...batch05_T041-T050.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch06 | `r0_review_archive_manifest.batch06.yaml`; `raw_marker_review.batch06.csv`; `reviewed_slate_anchor_manifest.batch06.csv`; `split_plan_from_raw_markers.batch06.csv` | one draft JSON for `...batch06_T051-T060.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch07 | `r0_review_archive_manifest.batch07.yaml`; `raw_marker_review.batch07.csv`; `reviewed_slate_anchor_manifest.batch07.csv`; `split_plan_from_raw_markers.batch07.csv` | one draft JSON for `...batch07_T061-T070.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |
| batch08 | `r0_review_archive_manifest.batch08.yaml`; `raw_marker_review.batch08.csv`; `reviewed_slate_anchor_manifest.batch08.csv`; `split_plan_from_raw_markers.batch08.csv` | one draft JSON for `...batch08_T071.wav`; three CSV exports | CSV payload sizes match; manifest vs draft JSON are different roles |

The 24 CSV exports align exactly by batch and file type after normalizing names:

| Batch | `raw_marker_review` size | `reviewed_slate_anchor_manifest` size | `split_plan_from_raw_markers` size | Size status |
| --- | ---: | ---: | ---: | --- |
| batch01 | 18061 | 6401 | 7277 | match |
| batch02 | 18020 | 6400 | 7268 | match |
| batch03 | 18023 | 6400 | 7268 | match |
| batch04 | 18067 | 6396 | 7264 | match |
| batch05 | 18055 | 6396 | 7264 | match |
| batch06 | 18055 | 6397 | 7265 | match |
| batch07 | 18058 | 6394 | 7258 | match |
| batch08 | 1572 | 1152 | 1404 | match |

mtime differences are explainable:

- batch01 CSVs match exactly at `2026-06-19 08:16:25 +0800`.
- batch02-batch08 project-side archived CSVs are all `2026-06-19 19:43:49 +0800`, while cg-varw export mtimes range from `2026-06-19 19:14:01 +0800` to `2026-06-19 19:34:55 +0800`. The size matches indicate copied/archived equivalents, not content divergence.
- cg-varw draft JSON mtimes precede their corresponding exports by seconds or minutes, which is expected for draft-save then export.
- `r0_review/.DS_Store` is an extra Finder metadata file, size 8196, mtime `2026-06-21 17:31:39 +0800`; it is not an R0 recovery artifact.

## R0 Draft/Load Entry Points Found

Backend route:

- `tools/cg-varw/backend/app/api/r0_raw_files.py`
- `GET /api/r0/raw-files/{file_id}/review-units`
- Route implementation resolves the raw file and calls `load_or_build_review_units(file_id, path)`.

Backend loader:

- `tools/cg-varw/backend/app/services/review_unit_builder.py`
- Current load priority is:
  1. `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json`
  2. `tools/cg-varw/review_outputs/r0/exports/{file_id}/raw_marker_review.csv`
  3. fallback through `review_outputs/r0/exports/*/raw_marker_review.csv`
  4. ASR/raw fallback or manual empty state.

Frontend state/load:

- `tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx`
- On page open, frontend calls `/api/health`, then `/api/r0/raw-files`.
- On selecting a raw file, frontend calls `/api/r0/raw-files/{file_id}/metadata` and `/api/r0/raw-files/{file_id}/review-units`.
- There is no separate R0 "load draft" button; loading is implicit when selecting a backend raw file.
- If backend is unavailable, frontend falls back to mock raw review data.

Config/path:

- `tools/cg-varw/backend/app/config.py` hardcodes `REVIEW_OUTPUT_ROOT = TOOL_DIR / "review_outputs"`.
- `CG_VARW_RAW_ROOT` or `tools/cg-varw/backend/config.local.json` controls the raw root.
- In this shell, `CG_VARW_RAW_ROOT` is unset and `tools/cg-varw/backend/config.local.json` is absent, so `load_settings()` falls back to `tools/cg-varw/sample_workspace/raw_audio` with `raw_root_mode=demo`.

## Legacy Problem: Concrete Current Behavior

The previous closeout note in `generate_xwc_f_final_reviewed.py` records:

> `LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED`: `f334880` changed R0 loading priority to draft -> exported CSV -> ASR/raw -> empty, but manual user validation still did not load exported spoken-marker state.

Current dry-run evidence narrows that to two likely mechanisms:

1. Runtime raw root mismatch.
   - Existing cg-varw R0 draft/export IDs decode to paths like `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`.
   - Those IDs match when `CG_VARW_RAW_ROOT` is set to `/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio`.
   - Those IDs do not match when raw root is set to `/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw`.
   - With the narrower raw root, the batch01 ID becomes `UlNfWFdDXzAwMl9CQUlZQV9QSUxPVF9iYXRjaDAxX1QwMDEtVDAxMC53YXY`, while existing draft/export IDs begin with `UUlOSVNU...`.

2. Loader fallback is too broad and not batch-aware.
   - If the direct export path for a `file_id` is absent, `exported_marker_review_path()` returns the first existing `*/raw_marker_review.csv` under `review_outputs/r0/exports`.
   - In the dry-run, for all narrow-root `file_id`s, this fallback returned the batch03 export path even though the requested file was batch01, batch02, etc.
   - `load_units_from_exported_csv()` then filters rows by `row["file_id"] == file_id` or blank `file_id`; for a mismatched file this can produce no rows and then fall through to ASR/manual state.
   - The function does not continue checking other export directories after a candidate CSV has mismatched rows.

## Mismatch Classification

| Category | Found? | Evidence |
| --- | --- | --- |
| Missing candidate directories | no | both directories exist |
| Missing R0 files | no, with note | project side has 32 R0 files plus `.DS_Store`; cg-varw side has 32 files |
| CSV size mismatch | no | all 24 normalized CSV pairs match by size |
| mtime anomaly | no blocker | project archive mtimes differ from cg-varw export mtimes but sizes match |
| hardcoded path | yes | `REVIEW_OUTPUT_ROOT` is fixed to `tools/cg-varw/review_outputs`; project `r0_review/` is not a runtime load source |
| stale path/config risk | yes | no current `CG_VARW_RAW_ROOT`/config; default is demo root |
| frontend state mismatch | not primary | frontend calls the review-units API on file selection; offline/demo fallback can mask real data |
| backend route mismatch | route exists, loader fragile | route is present; fallback path selection can pick an unrelated export when `file_id` direct path misses |
| raw root / `file_id` mismatch | yes | existing IDs only match raw root at `02_recordings/raw_audio` level |

## Initial Root Cause Judgment

The R0 data candidates are intact. The most likely root cause is not missing data; it is a contract mismatch between runtime raw-root selection and the file-id scheme used when the R0 drafts/exports were saved.

The current code can load the existing cg-varw candidates if the backend raw root is exactly `/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio`. In that configuration, all 8 Baiya raw WAV file IDs have both `draft=True` and `export=True`.

If the backend raw root is unset, the app uses demo data and cannot load Baiya R0 candidates. If the backend raw root points directly at the session `raw/` folder, the displayed files are the 8 Baiya raw WAVs but their generated `file_id`s do not match the existing draft/export directories. In that case the broad export fallback can choose an unrelated CSV, fail the row filter, and fall through to ASR/manual state.

The project-side `02_recordings/.../r0_review/` directory is an archive/candidate location, not currently a loader input. It is useful as an audit mirror and recovery source, but the active loader reads `tools/cg-varw/review_outputs/r0/`.

## Minimal Fix Plan, No Code Changes First

1. Start the backend with the exact raw root used by the existing R0 file IDs:

```bash
cd tools/cg-varw/backend
CG_VARW_RAW_ROOT="/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio" \
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

2. Open R0 and select only the 8 raw files under:

```text
QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/
```

3. Confirm the operation message shows draft/export recovery rather than demo/offline/manual empty state.

4. If the UI still does not show reviewed spoken-marker state, capture the selected raw file's `file_id`, `reviewData.source`, `reviewData.message`, and `units.length` from the `review-units` response before patching.

No data movement, no re-export, and no code change are required for this first confirmation pass.

## Patch Assessment

Patch is probably needed for durable behavior, but should wait for user confirmation after the no-code startup/config validation.

Low-risk patch candidates, if approved:

1. Add a diagnostic response field in R0 review-units showing `file_id`, direct draft path existence, direct export path existence, selected fallback path, and final source.
2. Make `exported_marker_review_path()` batch/file-id aware:
   - first check direct `{file_id}/raw_marker_review.csv`;
   - then decode each export directory and compare to the requested raw file name or relative path;
   - only return a fallback CSV if its rows match the requested file;
   - continue scanning candidates when a candidate CSV has only mismatched `file_id` rows.
3. Add regression coverage for raw-root mismatch:
   - wide root `02_recordings/raw_audio` should hit existing full-path IDs;
   - narrow root `.../RS_XWC_002_BAIYA_PILOT/raw` should not silently load an unrelated export.
4. Optionally make the required R0 raw root explicit in documentation or a non-secret local config template.

Patch risks:

- Changing `file_id` normalization can affect existing saved draft/export paths.
- Supporting multiple raw-root depths can accidentally merge unrelated recordings if matching is only by basename.
- Reading project-side `r0_review/` directly would introduce a second source of truth and should not be added without a clear migration rule.
- Frontend changes are unnecessary unless API diagnostics prove the frontend is discarding valid loaded units.

## Questions Requiring User Confirmation

1. Should the next validation run use `CG_VARW_RAW_ROOT=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio` as the canonical R0 root for this recovery?
2. If the no-code run succeeds, should P0-B close as config/documentation-only, with no patch?
3. If the no-code run still fails, do you approve a narrow backend-only diagnostic/loader patch limited to R0 `review_unit_builder.py` and tests?
4. Should `.DS_Store` remain ignored as non-R0 metadata in this P0-B scope, with no cleanup action?

## Next Step Recommendation

Do not patch immediately. First run a user-confirmed no-code UI/API validation with `CG_VARW_RAW_ROOT` set to the wide root `/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio`. If that loads the 8 draft JSON files and shows reviewed R0 markers, close P0-B without code changes. If it still fails, open a narrow R0 backend patch to add diagnostics and make export fallback file-id aware.

