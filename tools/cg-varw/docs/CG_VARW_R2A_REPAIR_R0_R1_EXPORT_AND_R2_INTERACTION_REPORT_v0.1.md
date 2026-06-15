# CG-VARW R2A Repair R0/R1 Export and R2 Interaction Report v0.1

## 1. Diff Inspection

Initial `git diff --name-only` showed changes in:

- `frontend/src/components/ABCDEPhrasePlayer.tsx`
- `frontend/src/components/ExportPanel.tsx`
- `frontend/src/mock/projectReviewMock.ts`
- `frontend/src/pages/R2ProjectReviewPage.tsx`
- `frontend/src/styles/theme.css`

Direct diffs for `R0RawReviewPage.tsx` and `R1SplitReviewPage.tsx` were empty. The accidental R0/R1 export regression was caused by shared CSS changes to `.export-preview-grid`, not by R0/R1 page logic or backend CSV semantics.

## 2. R0 Export Restoration

R0 keeps its existing inline `RawExportPreviewPanel` and original files:

- `reviewed_slate_anchor_manifest.csv`
- `raw_marker_review.csv`
- `split_plan_from_raw_markers.csv`

The generic `.export-preview-grid` CSS was restored to the three-column field-table preview layout used by R0/R1. R0 does not import or render the R2 export panel.

## 3. R1 Export Restoration

R1 keeps its existing inline `R1ExportPreviewPanel` and original files:

- `reviewed_render_anchors.csv`
- `split_marker_review.csv`
- `segment_qc_sheet.csv`

R1 does not import or render the R2 export panel, category tabs, or phrase export action.

## 4. R2 Export Isolation

R2-specific export UI was moved into `R2ExportPreviewPanel.tsx`. It contains R2 category tabs, phrase export, and field-table previews. The older shared `ExportPanel.tsx` is plain/generic and no longer contains R2 category logic.

## 5. R2 Version Switching

A/B/C/D/E rows remain clickable in `ABCDEPhrasePlayer`. Clicking a row updates:

- active version state,
- highlighted row,
- current phrase markers,
- waveform preview source,
- right-panel active version label,
- bottom action status.

All switching uses `getAlignment(selectedPhraseId, versionId)`, so it remains phrase-aligned and does not reuse absolute time.

## 6. R2 Playback Controls

R2 mock playback now has observable UI state:

- play / pause,
- from phrase start,
- from selected marker,
- 300ms preroll,
- loop current phrase,
- playback rate 0.5x / 1.0x / 1.5x,
- previous / next phrase,
- A→B→C→D→E sequence,
- preferred version playback,
- A/B comparison playback.

These update mock cursor/playback/status state only. No audio file is generated.

## 7. Section Timed Marker Card

The right panel no longer shows timed `section_start` / `section_end` cards or internal section marker keys. `Section 上下文` is now read-only section metadata: section label, section event range, phrase count, and current phrase index within the section.

## 8. Export Action Column

R2 export tables are wrapped in `.export-table-scroll`, and the action column uses a fixed `190px` width through `.export-table-action-column`. This prevents the rightmost action buttons from being clipped.

## 9. Preview Field Tables

R2 category previews now render field tables with:

- 字段
- 示例值
- 来源 / 含义

The preview button focuses the selected file preview rather than being a no-op.

## 10. R0 QA

Source QA confirms:

- R0 has no R2 category tab strings.
- R0 has no `导出当前 phrase`.
- R0 has no Render-root status wording.
- R0 continues using its existing `RawExportPreviewPanel`.

## 11. R1 QA

Source QA confirms:

- R1 has no R2 category tab strings.
- R1 has no `导出当前 phrase`.
- R1 has no Render-root status wording.
- R1 continues using its existing `R1ExportPreviewPanel`.

## 12. R2 QA

Source and build QA confirms:

- R2 imports `R2ExportPreviewPanel`.
- Version switching remains wired through `onSelect={selectVersion}`.
- Playback controls mutate mock playback state and status text.
- Right section context no longer displays timed section marker rows.
- R2 export preview is a field table.

Browser server QA could not be completed because starting the Vite dev server was blocked by Windows access permissions and the escalation review timed out. Build/typecheck/static regression checks passed.

## 13. Validation Results

- `npm run typecheck`: passed.
- `npm run build`: passed; generated `frontend/dist` was removed afterward.
- Backend `compileall app`: passed with bundled Codex Python runtime.
- `git diff --check`: passed.

## 14. Git Status

Final status contains only source/docs changes: R2 frontend interaction/export files, shared CSS repair, the R2-only export component, this repair report, and the earlier R2A polish report. `frontend/dist`, `.vite`, `.env.local`, R2 draft/export artifacts, `03_samples`, `04_outputs`, and sample asset files are absent.

## 15. Boundary Confirmation

This repair did not touch forbidden directories and did not generate real render/sample/ML artifacts:

- No real render connected.
- No ABCDE render generated.
- No `03_samples` writes.
- No `04_outputs` writes.
- No `sample_assets.csv` writes.
- No split/sample ingest.
- No ML training.
