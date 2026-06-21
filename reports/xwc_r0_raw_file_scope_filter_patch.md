# XWC R0 Raw File Scope Filter Patch

- Task: `CG-XWC-MVP-P0B_R0_RAW_FILE_SCOPE_FILTER_PATCH`
- Phase: Phase 1F-XWC-MVP Passed / Sweep & Review
- Generated: 2026-06-21
- Commit policy: no automatic commit

## 修改文件

| File | Change |
| --- | --- |
| `tools/cg-varw/backend/app/config.py` | Added `raw_include_prefix` to settings; reads `CG_VARW_RAW_INCLUDE_PREFIX`; normalizes and ignores unsafe prefixes. |
| `tools/cg-varw/backend/app/services/raw_file_scanner.py` | Filters only `/api/r0/raw-files` discovery by POSIX relative prefix under `CG_VARW_RAW_ROOT`. |
| `tools/cg-varw/backend/app/tests/test_r0_raw_file_scope_filter.py` | Added regression tests for default behavior, prefix filtering, wide-root file IDs, unsafe prefixes, and review-units compatibility. |
| `tools/cg-varw/backend/README.md` | Documented the new environment variable and the split between raw root and discovery scope. |
| `reports/xwc_r0_raw_file_scope_filter_patch.md` | This report. |

No R0 data files, `review_outputs/r0` files, recording audio, F/R1/R2/render/sample outputs, score/canon/source/schema files, or `scripts/generate_baiya_recording_plan.py` were modified.

## 新增 Env

```bash
export CG_VARW_RAW_ROOT="/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio"
export CG_VARW_RAW_INCLUDE_PREFIX="QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw"
```

`CG_VARW_RAW_INCLUDE_PREFIX` is optional. If unset or unsafe, current raw file discovery behavior remains compatible with the previous behavior.

The prefix is normalized by:

- trimming leading/trailing whitespace;
- converting `\` to POSIX `/`;
- removing empty path segments;
- supporting no trailing slash;
- ignoring absolute paths;
- ignoring any prefix containing `..`.

## Root 与 Prefix 的职责区分

`CG_VARW_RAW_ROOT` remains the file-id base. R0 file IDs are still generated from `path.relative_to(CG_VARW_RAW_ROOT).as_posix()`, then base64-url encoded. This preserves compatibility with existing R0 draft/export directories.

`CG_VARW_RAW_INCLUDE_PREFIX` only limits `/api/r0/raw-files` discovery/listing. It does not change `file_id`, direct audio/metadata/waveform lookup, or `review-units` draft/export lookup.

## 为什么不能改回窄 Root

Existing Baiya R0 draft/export IDs decode to paths such as:

```text
QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav
```

These IDs only match when `CG_VARW_RAW_ROOT` is the wide root:

```text
/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio
```

If `CG_VARW_RAW_ROOT` is changed to the narrow session `raw/` directory, the relative path becomes only:

```text
RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav
```

That produces a different short `file_id`, so existing `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json` and `exports/{file_id}/raw_marker_review.csv` no longer match.

## `/api/r0/raw-files` 行为变化

Before patch:

- with the wide raw root, `/api/r0/raw-files` listed every supported audio file under `02_recordings/raw_audio`;
- this included other sessions and Baiya split preview / T-preview WAVs;
- file IDs were correct for existing R0 draft/export, but the UI list was too broad.

After patch:

- with the wide raw root and `CG_VARW_RAW_INCLUDE_PREFIX=QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw`, `/api/r0/raw-files` lists only Baiya's 8 raw WAV files;
- file IDs still use the wide-root relative path;
- if the include prefix is unset, listing behavior remains unchanged.

## API Smoke Evidence

Port `8788` was already occupied by existing Python processes, so the same backend configuration was started temporarily on `127.0.0.1:8790` to avoid interrupting the existing server.

Health:

```text
GET /api/health -> 200 OK
{"ok": true, "service": "cg-varw-backend", "review_only": true, "production_grade": false}
```

Raw files:

```text
GET /api/r0/raw-files -> file_count=8
raw_root_mode=real
raw_root=/Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio
```

Returned Baiya raw WAVs:

| Batch | Relative path | Direct draft | Direct export | Units | First unit |
| --- | --- | ---: | ---: | ---: | --- |
| batch01 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav` | yes | yes | 10 | `T001 confirmed/accepted` |
| batch02 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav` | yes | yes | 10 | `T011 confirmed/accepted` |
| batch03 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav` | yes | yes | 10 | `T021 confirmed/accepted` |
| batch04 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.wav` | yes | yes | 10 | `T031 confirmed/accepted` |
| batch05 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.wav` | yes | yes | 10 | `T041 confirmed/accepted` |
| batch06 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.wav` | yes | yes | 10 | `T051 confirmed/accepted` |
| batch07 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch07_T061-T070.wav` | yes | yes | 10 | `T061 confirmed/accepted` |
| batch08 | `QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch08_T071.wav` | yes | yes | 1 | `T071 confirmed/accepted` |

Other same-root audio, including split preview / T-preview WAVs and other sessions, was not returned by the filtered `/api/r0/raw-files` result.

All 8 returned `file_id`s matched the existing wide-root draft/export directories. `review-units` returned non-empty reviewed units and did not fall back to demo/offline/manual empty.

## Tests

Red step:

```text
python -m unittest app.tests.test_r0_raw_file_scope_filter
FAILED (failures=2)
```

The failing tests showed that unfiltered discovery still returned split preview / other session files and matched `raw_extra` when no safe boundary existed.

Green step:

```text
python -m unittest app.tests.test_r0_raw_file_scope_filter
Ran 5 tests in 0.011s
OK
```

Targeted R0 regression:

```text
python -m unittest app.tests.test_r0_raw_file_scope_filter app.tests.test_r0_review_unit_loading
Ran 6 tests in 0.011s
OK
```

Full backend tests:

```text
python -m unittest discover -s app/tests
Ran 28 tests in 0.071s
OK
```

## Git Status

Expected status after patch:

```text
M  tools/cg-varw/backend/README.md
M  tools/cg-varw/backend/app/config.py
M  tools/cg-varw/backend/app/services/raw_file_scanner.py
?? reports/xwc_r0_raw_file_scope_filter_patch.md
?? reports/xwc_r0_recovery_validation.DRY_RUN.md
?? tools/cg-varw/backend/app/tests/test_r0_raw_file_scope_filter.py
?? scripts/generate_baiya_recording_plan.py
```

`reports/xwc_r0_recovery_validation.DRY_RUN.md` is the prior P0-B dry-run report. `scripts/generate_baiya_recording_plan.py` remains untouched and outside this task.

## Risk 与回滚

Risk is low because the patch changes only raw file listing. It does not change:

- R0 `file_id` encoding;
- raw file resolution for direct API calls;
- `review-units` load order;
- draft/export storage;
- any R0/R1/R2/F/render/sample data.

Main operational risk: a wrongly typed include prefix may return zero raw files. In that case unset `CG_VARW_RAW_INCLUDE_PREFIX` to restore previous listing behavior.

Rollback:

- remove `CG_VARW_RAW_INCLUDE_PREFIX` from the environment; or
- revert the small backend patch in `config.py`, `raw_file_scanner.py`, test file, and README.

## Recommendation

Recommended commit message:

```text
fix(varw): scope R0 raw file discovery without changing file ids
```

This patch should be committed after final user review. With the API smoke passing, P0-B's raw discovery/file-id mismatch can be considered resolved at the discovery-scope layer. No R0 loader fallback patch is required for the confirmed Baiya 8-file path, because all 8 returned file IDs directly hit existing draft/export artifacts.

