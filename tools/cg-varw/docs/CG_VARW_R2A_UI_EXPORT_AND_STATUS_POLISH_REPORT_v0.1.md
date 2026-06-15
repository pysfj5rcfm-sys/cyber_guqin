# CG-VARW R2A UI Export and Status Polish Report v0.1

## 1. Modified Files

- `tools/cg-varw/frontend/src/pages/R2ProjectReviewPage.tsx`
- `tools/cg-varw/frontend/src/components/ABCDEPhrasePlayer.tsx`
- `tools/cg-varw/frontend/src/components/ExportPanel.tsx`
- `tools/cg-varw/frontend/src/mock/projectReviewMock.ts`
- `tools/cg-varw/frontend/src/styles/theme.css`
- `tools/cg-varw/docs/CG_VARW_R2A_UI_EXPORT_AND_STATUS_POLISH_REPORT_v0.1.md`

## 2. Confirmed Non-Bugs

- The two visible `R2 句读听评` labels are kept: one is the top mode tab, one is the page/mode identity.
- JK / OLWJ / MHSN remain visible as mock-only pieces and are not made real project entries.
- MarkerLayer overlap logic was not rewritten.

## 3. Left Sidebar Cleanup

The duplicated stage buttons were removed from the R2 left sidebar. R0/R1/R2 switching now remains only in the top navigation.

The redundant left-sidebar flags were also removed. Review-only safety remains represented through the top badges and backend/export contracts.

## 4. Center Scrolling

The app root now avoids browser-level scrolling. The main R2 panel scrolls internally with bottom padding, while the bottom export panel and fixed status bar no longer obscure the version list or waveform playback controls.

## 5. Right Panel Localization

The right panel title is now `句读听评编辑`.

Visible version/status text is Chinese-first. Internal keys such as `B_PHRASE` and `candidate` remain only as small supporting text.

## 6. Marker Structure

Phrase marker primary buttons are limited to:

- 句头 / `phrase_start`
- 句尾 / `phrase_end`
- 气口 / `breath_point`
- 收束 / `cadence`

Section markers are shown in a separate `Section 上下文` area when relevant. Boundary unclear is handled as `边界状态`, not as a normal timed marker button.

## 7. Status Staleness

The bottom-right action message is updated from the active selected phrase/version whenever phrase, version, preferred version, draft, export, preview, or playback actions run. Messages such as `已切换到 PHRASE_05 · B 句法呼吸版` are derived from current state.

## 8. Export Preview

`导出与评审历史` now has separate category tabs and action buttons. `全部` shows the file property table. Specific categories show preview cards:

- 1 file: one preview column.
- 2 files: two preview columns.
- 3 files: three preview columns.

The single-file `预览` action focuses that file preview. The invalid `打开导出目录` button was removed.

## 9. Bottom Status Bar

The R2 bottom status bar now matches the R0/R1 style:

- Left: `后端已连接，当前使用合成演示 Render 根目录。`
- Right: latest action message.

It no longer repeats `review_only=true` or `production_grade=false`.

## 10. Boundary Check

This polish did not touch forbidden paths and did not generate real review artifacts:

- Did not write `03_samples/`.
- Did not write `04_outputs/`.
- Did not write `sample_assets.csv`.
- Did not generate render audio.
- Did not train ML.

All R2A mock data remains review-only and non-production.

## 11. Validation Results

- Backend: `compileall app` passed using the bundled Codex Python runtime.
- Frontend: `npm run typecheck` passed.
- Frontend: `npm run build` passed; generated `frontend/dist` was removed after validation.
- `git diff --check` passed.

## 12. Git Status Result

Final expected source changes are limited to R2A frontend polish files and this report. No generated `dist`, `.vite`, `.env.local`, R2 draft/export JSON/YAML/CSV, `03_samples`, `04_outputs`, or sample asset files are present.
