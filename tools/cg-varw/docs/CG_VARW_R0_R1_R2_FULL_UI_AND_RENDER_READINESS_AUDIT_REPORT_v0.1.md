# CG-VARW R0/R1/R2 Full UI and Render Readiness Audit Report v0.1

Task: `CG-VARW-R0_R1_R2_FULL_UI_AND_RENDER_READINESS_AUDIT`
Date: 2026-06-15
Mode: read-only audit / QA
Project phase: Phase 1B-3A-BY Recording Reshoot Preparation
Active session: `RS_XWC_002_BAIYA_PILOT`
Performer: `QINIST_002` / Baiya

## 1. Browser UI QA

Result: **not completed**

The audit attempted to use the configured Browser plugin / in-app browser as required. Browser bootstrap failed after reset with:

```text
node_repl kernel exited unexpectedly
windows sandbox failed: runner error: CreateProcessAsUserW failed: 5
```

Local dev services were also tested. The backend and frontend can start in foreground commands, but this shell environment terminates foreground servers at command timeout and does not preserve ordinary background processes across tool calls. A persistent Node runtime attempt to spawn local services failed with the same Windows sandbox process-creation error.

Therefore, no browser click regression is claimed in this report. All R0/R1/R2 UI click checks below are marked **UNVERIFIED_BROWSER_BLOCKED** unless explicitly supported by source-level inspection.

## 2. Service Startup Attempts

- Backend intended command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8787`
- Frontend intended command: `npm run dev -- --port 5173`
- Backend foreground smoke: Uvicorn reached `Application startup complete` and `http://127.0.0.1:8787` before timeout cleanup.
- Frontend foreground smoke: Vite can run through project Node/npm, but persistent browser-accessible service could not be held open in this sandbox.
- Temporary backend Python deps were installed under `%TEMP%\cg_varw_pydeps_audit`, outside the repository, because the bundled Python lacked `fastapi` / `uvicorn`.

## 3. R0 UI QA Result

Result: **UNVERIFIED_BROWSER_BLOCKED**

Source-supported observations:

- R0 uses `AppShell mode="R0"` and local R0 preview code, not `R2ExportPreviewPanel`.
- R0 preview lists only:
  - `reviewed_slate_anchor_manifest.csv`
  - `raw_marker_review.csv`
  - `split_plan_from_raw_markers.csv`
- R0 source contains raw file selection, waveform canvas, marker jump, play/pause, 300ms preroll, loop audition, 0.5x/1x/1.5x rate controls, marker nudge/status, save draft, and export CSV handlers.
- R0 bottom status/detail text is supplied by backend/raw-review state, not Render-root wording.

Not verified by browser: actual visual navigation, waveform rendering, audio playback behavior, loop behavior, draft/export feedback, and absence of visible R2 tabs/buttons in a rendered page.

## 4. R1 UI QA Result

Result: **UNVERIFIED_BROWSER_BLOCKED**

Source-supported observations:

- R1 uses `AppShell mode="R1"` and local R1 preview code, not `R2ExportPreviewPanel`.
- R1 preview lists only:
  - `reviewed_render_anchors.csv`
  - `split_marker_review.csv`
  - `segment_qc_sheet.csv`
- R1 source contains batch/segment selection, waveform canvas, marker jump, play/pause, 100ms/300ms preroll, loop audition, 0.5x/1x/1.5x rate controls, marker nudge/status, anchor/policy/tail selects, segment status/QC controls, save draft reload, and export CSV handlers.
- R1 bottom status/detail text is split-review wording, not Render-root wording.

Not verified by browser: actual rendered layout, audio playback, persistence after page switch, dropdown behavior, draft/export feedback, and absence of visible R2 tabs/buttons in a rendered page.

## 5. R2 UI QA Result

Result: **UNVERIFIED_BROWSER_BLOCKED**

Source-supported observations:

- R2 imports and uses `ABCDEPhrasePlayer` and `R2ExportPreviewPanel`.
- R2 mock pieces include `XWC`, `JK`, `OLWJ`, `MHSN`; non-XWC pieces are marked `mock_only`.
- R2 session data includes `RS_XWC_002_BAIYA_PILOT` and demo sessions.
- Section > phrase hierarchy is modeled by `sections` and `phrases`.
- A/B/C/D/E versions are modeled as `A_LITERAL`, `B_PHRASE`, `C_QINIST_STYLE`, `D_TEACHING`, `E_REVIEWED`.
- `preferredVersionByPhrase` is phrase-level.
- `listeningReviewByKey` uses `phrase_id::version_id`, so it is phrase+version-level.
- `boundaryStatusByKey` uses `phrase_id::version_id`, so it is phrase+version-level.
- Save/load draft uses `localStorage` and includes preferred, boundary, marker, and listening review state.
- R2 export preview builds actual live preview rows for non-`全部` categories from current props/state.
- R2 frontend does not call real render, sample ingest, ML training, `03_samples`, `04_outputs`, or `sample_assets`.

Not verified by browser: actual click behavior for A/B/C/D/E, playback state changes, phrase navigation, A/B compare sequence, preferred-version warning, visible absence of naked internal keys, live progress visual updates, and preview button interaction.

## 6. R0/R1/R2 Contract Audit

Result: **PASS_WITH_BROWSER_GAP**

R0 contract role:

- `reviewed_slate_anchor_manifest.csv`: primary reviewed raw slate anchor input for RECD-2.
- `raw_marker_review.csv`: marker audit / provenance only.
- `split_plan_from_raw_markers.csv`: controlled split preview input for RECD-2.
- Backend contract validator requires upstream IDs and safety fields including `review_only`, `production_grade`, and `not_sample_assets`.

R1 contract role:

- `reviewed_render_anchors.csv`: reviewed segment render anchor input.
- `split_marker_review.csv`: marker audit / provenance only.
- `segment_qc_sheet.csv`: primary sample candidate gate input.
- Backend contract validator requires `source_split_audio`, `segment_id`, `render_anchor_s`, `segment_status`, QC flags, reviewer fields, and safety fields including `not_render_executed` / `not_ml_training_data`.

R2 contract role:

- `phrase_structure_review.yaml`
- `render_phrase_alignment.csv`
- `phrase_boundary_decision.csv`
- `listening_review.yaml`
- `render_revision_log.yaml`
- `preferred_version_summary.csv`
- `issue_list.csv`

R2 is review-only/mock. It records phrase/version alignment and review evidence, but it must not be treated as production render output.

## 7. Sampling-to-Render Readiness

Conclusion: **READY_WITH_MINOR_ISSUES**

Field chain coverage:

- Present for raw/archive and R0/R1 contracts: `recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `batch_id`, `recording_take_no`, `batch_take_no`, `script_id`, `event_id`, `event_range`, `gesture_id`, `source_raw_audio`, `source_split_audio`, `segment_id`, `render_anchor_s`, `review_status`.
- Present for R1 gate: `realization_variant`, `segment_status`, QC booleans, `human_accepted`, `reviewed_by`, `reviewed_at`.
- Present for future R2 render-set review: `render_set_id`, `version_id`, `phrase_id`, `section_id`, `start_s`, `end_s`, `boundary_status`/`review_status`, `preferred_version_id`, `issue_type`, `severity`, `comment`, `suggested_revision`.
- Safety flags are present in the modeled contracts: `review_only`, `production_grade=false`, `not_render_executed`, `not_sample_assets`, `not_ml_training_data`.

Minor readiness gaps:

- R2 backend export endpoint writes default mock export rows from `r2_mock_store`, not the frontend live localStorage state. The frontend preview is live, but a future real export writer should consume the saved live review payload.
- Browser click regression could not be completed in this environment, so UI readiness remains source-supported rather than interaction-proven.

## 8. Blockers

- Browser / UI automation was blocked by Windows sandbox process creation failure: `CreateProcessAsUserW failed: 5`. Required click QA for R0/R1/R2 was not completed.

## 9. Major Issues

- The repository already contains `03_samples/` and `04_outputs/` before this audit. Existing files observed include `03_samples/recording_segments.csv`, `03_samples/sample_assets.csv`, and `04_outputs/xianwengcao`. This audit did not create or modify them, but the strict "confirm absent" check is false for the current repository state.

## 10. Minor Issues

- R2 real backend export is still mock/default-state oriented; it is suitable for review-only mock evidence, but not yet a live-state production export path.
- R2 UI browser behavior remains unverified due environment blocker.

## 11. Info / Observations

- `npm run typecheck` passed.
- `npm run build` passed. It generated `frontend/dist`; that temporary build output was moved out of the repository after validation.
- `python -m compileall app` passed.
- `tools/cg-varw/review_outputs/r2/drafts` and `tools/cg-varw/review_outputs/r2/exports` did not exist after the audit.
- `frontend/.vite` and `frontend/.env.local` did not exist after the audit.
- `tsconfig.tsbuildinfo` was restored to its pre-validation hash.

## 12. R0/R1 R2-Pollution Check

Result: **not detected at source level**

- R0/R1 do not import `R2ExportPreviewPanel`.
- `ExportPanel` contains no R2 grouping/category logic.
- R0/R1 preview panels are locally scoped and list only their original three files.

## 13. R2 State Closure Check

Result: **source-level pass**

- Preferred version state is phrase-level.
- Listening review state is phrase+version-level.
- Boundary status state is phrase+version-level.
- R2 export preview reads live props/state from current R2 UI state.
- Writing comments updates listening review state and does not call `setPreferredVersionByPhrase`.

## 14. Forbidden Output / Directory Touch Check

This audit did not write:

- `03_samples/`
- `04_outputs/`
- `sample_assets.csv`
- `recording_segments.csv`
- `recording_items_enriched.jsonl`
- `tools/cg-varw/review_outputs/r2/drafts/`
- `tools/cg-varw/review_outputs/r2/exports/`
- real render output
- sample ingest output
- ML training data

Existing pre-audit repository content includes `03_samples/` and `04_outputs/`; these were not touched.

## 15. Validation Commands

Frontend:

```text
cd tools/cg-varw/frontend
npm run typecheck
=> PASS

npm run build
=> PASS
```

Backend:

```text
cd tools/cg-varw/backend
python -m compileall app
=> PASS
```

Repository:

```text
git status --short --untracked-files=all
=> clean before report creation

git diff --check
=> PASS

git status --short --untracked-files=all
=> ?? tools/cg-varw/docs/CG_VARW_R0_R1_R2_FULL_UI_AND_RENDER_READINESS_AUDIT_REPORT_v0.1.md
```

Final generated-output check:

```text
tools/cg-varw/frontend/dist => absent
tools/cg-varw/frontend/.vite => absent
tools/cg-varw/frontend/.env.local => absent
tools/cg-varw/review_outputs/r2/drafts => absent
tools/cg-varw/review_outputs/r2/exports => absent
recording_items_enriched.jsonl => absent
```

## 16. Final Conclusion

Overall conclusion: **READY_WITH_MINOR_ISSUES**

Tooling appears source-ready for fast transition from Baiya sample completion into sample candidate gate / render-set review preparation, with the caveat that browser UI regression could not be executed in this sandbox and R2 backend export remains mock/default-state rather than live-state production export.
