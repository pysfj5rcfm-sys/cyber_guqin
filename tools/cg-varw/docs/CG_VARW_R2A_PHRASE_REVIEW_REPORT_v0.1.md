# CG-VARW R2A Phrase Review Mock Report v0.1

## 1. Modified Files

- Frontend: `src/App.tsx`, `src/types/cgVarw.ts`, `src/mock/projectReviewMock.ts`, `src/pages/R2ProjectReviewPage.tsx`, `src/components/ABCDEPhrasePlayer.tsx`, `src/components/ExportPanel.tsx`, `src/styles/theme.css`.
- Backend: `app/main.py`, `app/schemas.py`, `app/api/r2_phrase_review.py`, `app/services/r2_mock_store.py`.
- Docs: `docs/CG_VARW_R2A_PHRASE_REVIEW_REPORT_v0.1.md`.

## 2. R2 Naming

The R2 navigation and page title are unified as `R2 句读听评`. The removed UI wording includes `R2 Project Review`, `ABCDE 句读对齐听评`, and standalone `句读听评` navigation text.

## 3. Mock Pieces

R2A mock pieces are fixed as:

- `XWC / 仙翁操`: active MVP piece.
- `JK / 酒狂`: R2A UI mock only.
- `OLWJ / 鸥鹭忘机`: R2A UI mock only.
- `MHSN / 梅花三弄`: R2A UI mock only.

The UI labels the non-XWC pieces as mock-only and does not imply sampling, rendering, or project-mainline status.

## 4. Mock Sessions

R2A sessions are fixed as:

- `RS_XWC_002_BAIYA_PILOT`: current project session.
- `DEMO_SESSION_001`: UI mock only.
- `DEMO_SESSION_002`: UI mock only.

The old `session_01/session_02/session_03` placeholders were removed from the R2 UI.

## 5. Section / Phrase Hierarchy

The R2 mock contract implements `section_id > phrase_id > event_range > version_id/start_s/end_s`.

`Section` owns `phrase_ids`, each `PhraseDefinition` belongs to exactly one section, and the left rail displays sections as phrase groups. The center work area only renders the selected phrase, while section markers are context markers.

## 6. Primary Review Unit

The primary review unit is `phrase` because listening comments, marker nudges, preferred version selection, and draft rehydration all bind to `phrase_id`. Sections are used only for grouping, context, and progress.

## 7. No Absolute-Time Switching

Each A/B/C/D/E version has its own `RenderPhraseAlignment` row for every phrase. The R2 version table displays `PHRASE_xx: start_s-end_s` per version, and playback status messages state that sequence and A/B playback use each version's phrase range.

## 8. Playback Controls

The waveform area keeps the existing R0/R1 `PlaybackBar` style for play/pause, phrase-start playback, 300ms preroll, loop, and speed controls. R2-specific controls are a second row below it: A→B→C→D→E sequence, preferred-version playback, and A/B comparison.

## 9. R2-Specific Playback

R2 sequence playback is represented as phrase-aligned mock control state. It does not generate audio cuts and does not reuse a shared absolute time span across versions.

## 10. Export Area

The bottom area is `导出与评审历史`, implemented as a semantic grouped table rather than dense multi-column cards. Groups are `全部`, `句读结构`, `版本对齐`, `听评记录`, `修订依据`, and `汇总`.

## 11. Export Files

Core default files:

- `phrase_structure_review.yaml`
- `render_phrase_alignment.csv`
- `phrase_boundary_decision.csv`
- `listening_review.yaml`
- `render_revision_log.yaml`

Summary files:

- `preferred_version_summary.csv`
- `issue_list.csv`

## 12. Draft Save / Rehydration

Frontend draft save/load uses a render-set-scoped localStorage payload with selected phrase, selected version, phrase markers, phrase alignments, issue_type array, severity, comment, suggested_revision, preferred_version, reviewer, and reviewed_at.

Backend draft save/load is exposed through `/api/r2/reviews/draft/save` and `/api/r2/render-sets/{render_set_id}/reviews/draft`, writing to `tools/cg-varw/review_outputs/r2/drafts/{render_set_id}.r2_review_draft.json`.

## 13. Render / Output / Sample / ML Safety

- Real render generated: no.
- `04_outputs/` written: no.
- `03_samples/` written: no.
- `sample_assets.csv` written: no.
- ML trained or training data produced: no.

Every R2 mock contract object carries or writes:

- `review_only=true`
- `production_grade=false`
- `not_render_executed=true`
- `not_sample_assets=true`
- `not_ml_training_data=true`

## 14. Backend API Contract

Added `/api/r2` endpoints for projects, sessions, pieces, render sets, versions, phrases, phrase alignments, event timeline, mock waveform/spectrogram/audio, draft save/load, save actions, export list, and export generation.

Generated draft/export files are under `tools/cg-varw/review_outputs/r2/...`, which is covered by `tools/cg-varw/review_outputs/.gitignore`.

## 15. Validation Results

- Backend compile: passed with `C:\Users\11028\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m compileall app`.
- Backend mock store smoke test: passed; `list_alignments()` returns 25 rows and version data starts with `A_LITERAL`.
- Frontend typecheck: passed with `npm run typecheck`.
- Frontend build: passed with `npm run build`; generated `frontend/dist` files were removed afterward.
- FastAPI import smoke test: not run because the bundled validation Python does not include `fastapi`, and the project `.venv` launcher is not usable in this shell.

## 16. Git Status Snapshot

Expected source changes are limited to `tools/cg-varw/backend/app/**`, `tools/cg-varw/frontend/src/**`, and this report. No `03_samples`, `04_outputs`, sample assets, real render audio, ML data, `node_modules`, `dist`, `.vite`, or `.env.local` files are part of the source diff.
