# XWC MVP File Audit Cleanup Closeout

- Task: `CG-XWC-MVP-P0A_ARCHIVE_CLEANUP_FINAL_VALIDATE_AND_COMMIT_PREP`
- Phase: Phase 1F-XWC-MVP Passed / Sweep & Review
- Scope: final validation and commit preparation only.
- Commit policy: no automatic commit.

## Summary

P0-A completed in two bounded steps:

1. Dry-run file-level audit produced a cleanup plan, dry-run archive index, and token-cost retrospective. It did not move, delete, rename, render, regenerate, or deep-scan repository contents.
2. Approved ARCHIVE bucket execution moved only files already classified as `ARCHIVE` into `archive/xwc_mvp_file_audit_cleanup_20260621/`, preserving original relative paths.

No `REVIEW`, `DELETE_CANDIDATE`, `KEEP`, or `DO_NOT_TOUCH` files were processed in the execution step. `scripts/generate_baiya_recording_plan.py` remains untouched because it is a pre-existing untracked file and was explicitly outside this task.

## Archive Execution

- Moved count: 251 files.
- Archive root: `archive/xwc_mvp_file_audit_cleanup_20260621/`.
- Final archive index: `reports/xwc_mvp_archive_index.md`.
- Execution report: `reports/xwc_mvp_archive_execution_report.md`.

`git status` reports `D 250` plus an untracked archive root because 250 moved source files were tracked by git. The approved archive index contains 251 rows; the 251st indexed payload is an ignored `.DS_Store`, so it exists under the archive root but does not appear as a tracked deletion.

The required raw validation command `find archive/xwc_mvp_file_audit_cleanup_20260621 -type f | wc -l` currently returns 259. This is explained by the 251 approved archive-index payloads plus additional ignored `.DS_Store` metadata files under archive parent directories. They were not processed or deleted because this task forbids deletion and forbids handling `DELETE_CANDIDATE` artifacts.

## Final F Validation

The final F canonical outputs remain in place:

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/XWC_BAIYA_F_FINAL_REVIEWED.wav`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/render_event_alignment.F_FINAL_REVIEWED.csv`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_final_validation.json`

The base relationship check is `git merge-base --is-ancestor 4899227 HEAD`, not an equality check against `4899227`.

## Protected State

R0 recovery candidates remain in their original locations:

- `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review`: 32 files.
- `tools/cg-varw/review_outputs/r0`: 32 files.

The canonical R2 latest directory remains in place:

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/`

## Deferred Buckets

`REVIEW` was not processed because those files require user confirmation or a separate narrow review before archive decisions.

`DELETE_CANDIDATE` was not processed because this task was archive-only and explicitly forbade deletion.

`KEEP` and `DO_NOT_TOUCH` were not processed because they include canonical final output, R0 recovery candidates, score/canon/source/sample-ingest boundaries, and other protected project state.

`scripts/generate_baiya_recording_plan.py` was not processed because it is a pre-existing untracked script, outside P0-A archive execution scope, and explicitly excluded from this task and commit preparation.

## P0-A Closeout Decision

P0-A can be treated as complete for the approved archive bucket: the dry-run outputs exist, the approved 251 ARCHIVE files were moved into the archive root, final F outputs still exist, R0 recovery candidates remain in place, and `r2_review_drafts/latest/` remains in place.

Next step: enter P0-B `LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED` / R0 recovery validation as a separate task.

## Final Validation Evidence

| Check | Expected | Result |
| --- | --- | --- |
| `git merge-base --is-ancestor 4899227 HEAD` | exit 0 | PASS |
| `git diff --check` | no output | PASS |
| Final F wav exists | file exists | PASS |
| Final F alignment exists | file exists | PASS |
| Final F validation exists | file exists | PASS |
| R0 project recovery files | 32 | PASS |
| R0 cg-varw recovery files | 32 | PASS |
| `r2_review_drafts/latest/` | directory exists | PASS |
| Final archive index rows | 251 | PASS |
| Archive root raw `find -type f` count | 259 | PASS_WITH_NOTE: includes ignored `.DS_Store` metadata under archive parent directories |

## Commit Preparation

Suggested commit message:

```text
chore(xwc): archive approved MVP cleanup artifacts
```

Suggested staging scope must exclude `scripts/generate_baiya_recording_plan.py`.
