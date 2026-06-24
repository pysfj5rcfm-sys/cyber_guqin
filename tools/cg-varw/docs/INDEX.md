# tools/cg-varw/docs Index

This directory contains chronological CG-VARW design, contract, patch, repair, and implementation reports. It is a documentation rollup only; no file is moved or superseded by deletion.

## Current Design / Spec References

| File | Status | Role |
| --- | --- | --- |
| `RECD_VARW_CSV_CONTRACT_SPEC_v0.1.md` | `current` | CSV contract spec reference. |
| `RECD_VARW_CSV_CONTRACT_AUDIT.md` | `partially-current` | CSV contract audit evidence. |
| `CG_VARW_R0_R1_R2_FULL_UI_AND_RENDER_READINESS_AUDIT_REPORT_v0.1.md` | `partially-current` | Full UI/render readiness audit evidence. |
| `CG_VARW_R0_R1_R2_FINAL_UI_REGRESSION_POLISH_REPORT_v0.1.md` | `partially-current` | Final UI regression polish evidence. |

## R0 / R1 / R2 Contract and Closure Reports

| File | Status | Role |
| --- | --- | --- |
| `CG_VARW_R2A_PHRASE_REVIEW_REPORT_v0.1.md` | `partially-current` | R2A phrase review report. |
| `CG_VARW_R2A_REPAIR_R0_R1_EXPORT_AND_R2_INTERACTION_REPORT_v0.1.md` | `partially-current` | R0/R1 export and R2 interaction repair evidence. |
| `CG_VARW_R2A_PHRASE_VERSION_REVIEW_STATE_FIX_REPORT_v0.1.md` | `partially-current` | Phrase-version review-state fix report. |
| `CG_VARW_R2A_VISIBLE_VERSION_SWITCHER_AND_BOUNDARY_STATE_FIX_REPORT_v0.1.md` | `partially-current` | Version switcher and boundary-state fix report. |
| `CG_VARW_R2A_UI_EXPORT_AND_STATUS_POLISH_REPORT_v0.1.md` | `partially-current` | R2A UI/export/status polish evidence. |
| `CG_VARW_R2A_FUNCTIONAL_CLOSURE_AND_VERSION_SWITCHER_REPAIR_REPORT_v0.1.md` | `partially-current` | R2A functional closure and version-switcher repair report. |
| `CG_VARW_R2_CANONICAL_DRAFT_CLEANUP_REPORT_v0.1.md` | `partially-current` | R2 canonical draft cleanup report. |
| `CG_VARW_R2_E_INTAKE_T008_SAFE_R0_LOAD_AND_F_SLOT_REPORT_v0.1.md` | `partially-current` | Safe R0 load and F-slot intake report. |

## Patch / Repair Reports

| File | Status | Role |
| --- | --- | --- |
| `RECD_VARW_CSV_WRITER_PATCH_REPORT_v0.1.md` | `historical` | CSV writer patch evidence. |
| `CG_VARW_R2_FULL_EXPORT_PAYLOAD_FIX_REPORT_v0.1.md` | `historical` | Full export payload fix report. |
| `CG_VARW_R2_FINAL_CANONICAL_EXPORT_FIX_REPORT_v0.1.md` | `historical` | Final canonical export fix report. |
| `CG_VARW_R2_FRONTEND_RESTORE_FROM_4A26CB5_REPORT_v0.1.md` | `historical` | Frontend restore evidence. |
| `CG_VARW_R2_PERSISTENCE_FAILURE_FIX_REPORT_v0.1.md` | `historical` | Persistence failure fix evidence. |
| `CG_VARW_R2_PERSISTENT_REVIEW_DRAFT_AND_RESTORE_REPORT_v0.1.md` | `historical` | Persistent review draft and restore report. |
| `CG_VARW_R2_RECENT_CHANGE_AUDIT_AND_SAFE_REPAIR_REPORT_v0.1.md` | `historical` | Recent-change audit and safe repair report. |
| `CG_VARW_R2_REVIEW_STATE_RESTORE_AFTER_DEDUPE_REPORT_v0.1.md` | `historical` | Restore-after-dedupe report. |
| `CG_VARW_R2_STABILIZATION_AUDIT_AND_REPAIR_REPORT_v0.1.md` | `historical` | R2 stabilization audit and repair report. |
| `CG_VARW_R2_XWC_ABCD_FRONTEND_API_WIRING_REPORT_v0.1.md` | `historical` | XWC ABCD frontend/API wiring report. |
| `CG_VARW_R2_E_REVIEWED_GENERATION_REPORT_v0.1.md` | `historical` | E-reviewed generation report. |
| `CG_VARW_R2_F_FINAL_REVIEWED_GENERATION_AND_EXPORT_SYNC_REPORT_v0.1.md` | `historical` | F final-reviewed generation and export-sync evidence. |
| `CG_VARW_R1_FULL_TAIL_REFRESH_AND_F_REGEN_REPORT_v0.1.md` | `historical` | Historical full-tail refresh and F regeneration evidence. |

## Historical Implementation Notes

| File | Status | Role |
| --- | --- | --- |
| `CG_VARW_M0_UI_SHELL_NOTES.md` | `historical` | M0 UI shell notes. |
| `CG_VARW_M0_VALIDATION.md` | `historical` | M0 validation note. |

## Obsolete / Superseded Notes

These files remain as historical evidence. For current script safety, use:

- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `tools/cg-varw/backend/scripts/README.md`
- `reports/repo_entrypoint_map.latest.v0.1.md`

## Authority Boundary

- CG-VARW docs are report evidence, not canonical authority.
- `tools/cg-varw/review_outputs/` is generated non-canonical local workbench output.
- R2 canonical authority is `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`.
- R2 CSV/YAML exports are derived.
- Accepted `F_FINAL_REVIEWED/` is forbidden-to-touch.
