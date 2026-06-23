# Project Report Archive Inventory v0.1

- Task id: `CG-PROJECT-REPORTS-ARCHIVE-CLEANUP-v0.1`
- Date: 2026-06-23
- Scope: documentation/archive cleanup only.
- Archive spelling check: existing repo convention uses `archive`; no `achieve/` directory convention was found.
- Primary archive target: `reports/archive/2026-06/`

## Safety Boundaries

No runtime code, tests, schemas, mock fixtures, sample ingest files, audio files, accepted `F_FINAL_REVIEWED` outputs, ML/training files, or production render/sample workflows are in the move set.

Explicit red-line file kept untouched:

- `scripts/generate_baiya_recording_plan.py`

## Files Scanned

Scanned report/documentation-like paths by metadata/path:

| Area | Result |
| --- | --- |
| `reports/` | Primary target. Root report-like files classified one by one below. Existing `reports/archive/` convention observed. |
| `docs/cyber_guqin/` | Active runbook/script-registry entrypoints; keep in place. |
| `06_docs/` | Project documentation and historical stage notes; keep in place for this task because several files remain project structure/status references. |
| `tools/cg-varw/docs/` | Tool-local reports/specs; keep in place for this task because several are current VARW/RECD contract or repair evidence. |
| `tools/cg-varw/reports/` | Directory does not exist. |
| `examples/cyber_guqin/` | Current reusable example manifests and current `qinist_starter_kit/*.mock.yaml`; keep in place. |
| `00_global/`, `01_pieces/`, `02_recordings/`, `04_outputs/` | Data/runtime/output areas scanned only for report-like path context; no moves proposed from these areas. |

## Classification Table

### `reports/`

| File | Classification | Proposed action | Rationale |
| --- | --- | --- | --- |
| `reports/REPORTS_INDEX.md` | `KEEP_IN_PLACE_ENTRYPOINT` | Keep | Active report directory index. |
| `reports/qinist_starter_field_source_audit.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current Qinist starter/Sanman design-review artifact. |
| `reports/qinist_starter_field_source_matrix.v0.1.json` | `ACTIVE_CURRENT` | Keep | Current Qinist starter/Sanman design-review artifact. |
| `reports/qinist_starter_kit_and_sanman_instance_design.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current mainline design artifact. |
| `reports/single_piece_dapu_ir_input_contract.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current input contract design artifact. |
| `reports/piece_demand_aggregation_and_coverage_diff_design.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current design artifact. |
| `reports/high_frequency_gesture_array_extraction_design.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current design artifact. |
| `reports/universal_qinist_starter_collection_kit.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current starter collection kit artifact. |
| `reports/ai_prompted_collection_protocol.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current collection protocol artifact. |
| `reports/qinist_candidate_sidecar_design.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current candidate sidecar design artifact. |
| `reports/rhythm_diverse_abcd_strategy_design.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current strategy design artifact. |
| `reports/varw_r2_to_qinist_profile_signal_mapping.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current VARW-to-Qinist profile signal mapping artifact. |
| `reports/qinist_starter_missing_inputs.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current missing-inputs review artifact. |
| `reports/qinist_starter_draft_artifact_review.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current user-review artifact. |
| `reports/qinist_starter_draft_artifact_review_findings.v0.1.json` | `ACTIVE_CURRENT` | Keep | Current user-review artifact. |
| `reports/engineering_tail_backlog.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current engineering closeout/backlog artifact. |
| `reports/self_contained_reproduction_toolchain_report.md` | `ACTIVE_CURRENT` | Keep | Current XWC F reproduction-ready status evidence. |
| `reports/varw_r012_export_contract_design.v0.1.md` | `ACTIVE_CURRENT` | Keep | Current RECD/VARW authority design. |
| `reports/varw_r012_export_contract_audit.DRY_RUN.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Related to current VARW export contract; keep until contract docs are explicitly reviewed. |
| `reports/r0r1_export_manifest_reload_identity_guard_report.md` | `ACTIVE_CURRENT` | Keep | Referenced by current starter field-source audit; current guard evidence. |
| `reports/r2_derived_export_guard_patch.md` | `ACTIVE_CURRENT` | Keep | Current R2 derived-export guard evidence. |
| `reports/full_tail_natural_decay_default_patch.md` | `ACTIVE_CURRENT` | Keep | Current guqin tail-policy guard evidence. |
| `reports/validator_parameterization_report.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Contains active command examples and output-path contracts; do not move without link/update pass. |
| `reports/canon_seed_report.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Canon seed provenance may still be useful as an active reference. |
| `reports/c1_candidate_normalization_report.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | QXBY Batch002 candidate normalization may still be useful for source/canon review. |
| `reports/qxby_batch_002_candidate_list.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Source/canon review evidence; not clearly superseded by current starter artifacts. |
| `reports/qxby_batch_002_collection_plan.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Source/canon review evidence; referenced by ingest readiness tooling. |
| `reports/qxby_batch_002_collection_plan.json` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Data-like source/canon planning evidence. |
| `reports/qxby_batch_002_report.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Source/canon review evidence. |
| `reports/qxby_batch_002_source_audit.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Source/canon review evidence. |
| `reports/qxby_batch_002_source_audit.json` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Source/canon review evidence. |
| `reports/qxby_batch_001_human_review.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Referenced as input evidence by `scripts/audit_recording_ingest_readiness.py`; do not move in this cleanup. |
| `reports/v1_to_canon_coverage.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Large canon/source coverage audit; may remain useful as active evidence. |
| `reports/v1_to_canon_coverage.json` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Data-like paired output for coverage audit; leave for user review. |
| `reports/xwc_legacy_recording_bridge_plan.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Referenced by session manifests as bridge-plan evidence. |
| `reports/xwc_legacy_recording_bridge_map.json` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Data-like bridge artifact; keep with bridge plan. |
| `reports/xwc_legacy_take_manifest_preview.csv` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Data-like bridge artifact; keep with bridge plan. |
| `reports/rs_xwc_002_baiya_recording_take_plan.csv` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Referenced by Baiya session manifest; do not move. |
| `reports/rs_xwc_002_baiya_recording_batch.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Baiya recording-plan evidence; keep with take plan. |
| `reports/rs_xwc_002_baiya_batch_ranges.csv` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Data-like Baiya recording-plan evidence. |
| `reports/rs_xwc_002_baiya_session_manifest_draft.yaml` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Manifest-like Baiya recording artifact. |
| `reports/rs_xwc_002_baiya_generation_report.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Baiya plan generation evidence; keep with related plan files. |
| `reports/rs_xwc_002_baiya_recording_day_guide.md` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Baiya recording guide; not moved while related plan files remain active/uncertain. |
| `reports/rs_xwc_002_baiya_validation_report.json` | `KEEP_IN_PLACE_UNCERTAIN` | Keep | Data-like validation evidence for Baiya plan. |
| `reports/xwc_r0_raw_file_scope_filter_patch.md` | `ACTIVE_CURRENT` | Keep | Current R0 raw scope guard evidence. |
| `reports/XWC_RECORDING_DAY_GUIDE.md` | `HISTORICAL_REFERENCE` | Move | Older RS_XWC_001 recording-day guide, superseded by current Baiya/XWC and starter-kit direction. References found only in historical reports selected for archive. |
| `reports/architecture_inventory.json` | `HISTORICAL_SUPERSEDED` | Move | Old Phase R0/reports cleanup inventory; superseded by current structure and this inventory. |
| `reports/architecture_review.md` | `HISTORICAL_SUPERSEDED` | Move | Old Phase R0 architecture review; superseded by current status and later artifacts. |
| `reports/check_v1_compat_report.json` | `HISTORICAL_REFERENCE` | Move | Generated validation output; `REPORTS_INDEX.md` allows generated validation reports to be archived and regenerated. |
| `reports/cyber_guqin_mvp_workflow_skill_design_and_three_target_coverage.v0.1.md` | `HISTORICAL_REFERENCE` | Move | Historical skill-design evidence; current entrypoint is `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`. |
| `reports/cyber_guqin_mvp_workflow_skill_generation_report.md` | `HISTORICAL_REFERENCE` | Move | Historical skill-generation report; current entrypoint is the installed skill. |
| `reports/mvp_pilot_cleanup_inventory.csv` | `HISTORICAL_SUPERSEDED` | Move | Old cleanup inventory; superseded by later cleanup closeout and current inventory. |
| `reports/mvp_pilot_cleanup_summary.md` | `HISTORICAL_SUPERSEDED` | Move | Old cleanup summary. |
| `reports/mvp_pilot_reusable_framework_report.md` | `HISTORICAL_REFERENCE` | Move | Old MVP reusable-framework report; current reusable status is documented in README/runbook/toolchain report. |
| `reports/next_recording_batch_generation_plan.md` | `HISTORICAL_SUPERSEDED` | Move | Old next-recording planning report; current mainline is Qinist starter/Sanman. |
| `reports/phase_1b1_manifest_template_report.md` | `HISTORICAL_REFERENCE` | Move | Historical manifest-template report. |
| `reports/project_instruction_rollback_recommendation.md` | `HISTORICAL_SUPERSEDED` | Move | Old one-off recommendation report. |
| `reports/qxby_batch_001_source_audit.md` | `HISTORICAL_REFERENCE` | Move | Regenerable/source-audit report; not current mainline, and existing report index already treats QXBY Batch001 reports as archive material. |
| `reports/qxby_batch_001_source_audit.json` | `HISTORICAL_REFERENCE` | Move | JSON pair for archived source-audit report. |
| `reports/recording_ingest_decisions_needed.md` | `HISTORICAL_SUPERSEDED` | Move | Historical sample-ingest planning report; sample ingest is explicitly not current. |
| `reports/recording_ingest_field_gap.json` | `HISTORICAL_SUPERSEDED` | Move | Historical sample-ingest audit output; sample ingest is explicitly not current. |
| `reports/recording_ingest_next_steps.md` | `HISTORICAL_SUPERSEDED` | Move | Historical sample-ingest planning report; sample ingest is explicitly not current. |
| `reports/recording_ingest_readiness.md` | `HISTORICAL_SUPERSEDED` | Move | Historical sample-ingest readiness audit; sample ingest is explicitly not current. |
| `reports/reports_cleanup_plan.md` | `HISTORICAL_SUPERSEDED` | Move | Prior cleanup plan; superseded by this task inventory and manifest. |
| `reports/reports_cleanup_summary.md` | `HISTORICAL_SUPERSEDED` | Move | Prior cleanup summary. |
| `reports/slimming_recommendations.md` | `HISTORICAL_SUPERSEDED` | Move | Old Phase R0 slimming recommendations. |
| `reports/validate_canon_report.json` | `HISTORICAL_REFERENCE` | Move | Generated validation output; can be regenerated in root if needed. |
| `reports/validate_canon_seed_report.json` | `HISTORICAL_REFERENCE` | Move | Generated validation output; can be regenerated in root if needed. |
| `reports/validate_dapu_ir_report.json` | `HISTORICAL_REFERENCE` | Move | Generated validation output; can be regenerated in root if needed. |
| `reports/validate_qxby_batch_001_report.json` | `HISTORICAL_REFERENCE` | Move | Generated validation output; can be regenerated in root if needed. |
| `reports/validate_qxby_batch_002_report.json` | `HISTORICAL_REFERENCE` | Move | Generated validation output; can be regenerated in root if needed. |
| `reports/xwc_f_final_token_cost_retrospective.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Move | Historical dry-run retrospective draft. |
| `reports/xwc_f_final_token_cost_retrospective.md` | `HISTORICAL_REFERENCE` | Move | Historical finalized retrospective; useful for traceability but not an active entrypoint. |
| `reports/xwc_mvp_archive_execution_report.md` | `HISTORICAL_REFERENCE` | Move | Historical archive execution report from prior cleanup. |
| `reports/xwc_mvp_archive_index.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Move | Historical dry-run archive index. |
| `reports/xwc_mvp_archive_index.md` | `HISTORICAL_REFERENCE` | Move | Historical final archive index. |
| `reports/xwc_mvp_file_audit_cleanup_closeout.md` | `HISTORICAL_REFERENCE` | Move | Historical cleanup closeout. |
| `reports/xwc_mvp_file_audit_cleanup_plan.md` | `HISTORICAL_REFERENCE` | Move | Historical cleanup plan. |
| `reports/xwc_mvp_full_process_playbook.v0.1.md` | `HISTORICAL_REFERENCE` | Move | Historical XWC MVP playbook; current user-facing entrypoints are README, workflow skill, script registry, and reproduction runbook. |
| `reports/xwc_mvp_lessons_learned_and_pitfalls.v0.1.md` | `HISTORICAL_REFERENCE` | Move | Historical lessons report; useful traceability but not active entrypoint. |
| `reports/xwc_process_script_reuse_audit.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Move | Historical dry-run audit report; current entrypoint is script registry. |
| `reports/xwc_r0_recovery_validation.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Move | Historical dry-run validation report; current R0 guard report stays in root. |

### Secondary Areas Kept In Place

| Area | Classification | Rationale |
| --- | --- | --- |
| `docs/cyber_guqin/SCRIPT_REGISTRY.md` | `KEEP_IN_PLACE_ENTRYPOINT` | Active safety registry. |
| `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md` | `KEEP_IN_PLACE_ENTRYPOINT` | Active reproduction runbook. |
| `06_docs/*.md` | `KEEP_IN_PLACE_UNCERTAIN` | Stage/project docs may still be entrypoints; no secondary moves without narrower approval. |
| `tools/cg-varw/docs/*.md` | `KEEP_IN_PLACE_UNCERTAIN` | Tool-local docs/specs include current RECD/VARW contract material and recent repair evidence. |
| `examples/cyber_guqin/*.yaml` | `ACTIVE_CURRENT` | Current reusable examples. |
| `examples/cyber_guqin/qinist_starter_kit/*.mock.yaml` | `ACTIVE_CURRENT` | Current starter-kit mock fixtures. |

## Proposed Moves

Move these files to `reports/archive/2026-06/` with filenames preserved:

| Original path | Archive path | Classification | Reference note |
| --- | --- | --- | --- |
| `reports/XWC_RECORDING_DAY_GUIDE.md` | `reports/archive/2026-06/XWC_RECORDING_DAY_GUIDE.md` | `HISTORICAL_REFERENCE` | Referenced only by historical reports in this move set. |
| `reports/architecture_inventory.json` | `reports/archive/2026-06/architecture_inventory.json` | `HISTORICAL_SUPERSEDED` | Referenced by prior cleanup reports in this move set. |
| `reports/architecture_review.md` | `reports/archive/2026-06/architecture_review.md` | `HISTORICAL_SUPERSEDED` | Referenced by prior cleanup reports in this move set. |
| `reports/check_v1_compat_report.json` | `reports/archive/2026-06/check_v1_compat_report.json` | `HISTORICAL_REFERENCE` | Generated validation output; historical references noted. |
| `reports/cyber_guqin_mvp_workflow_skill_design_and_three_target_coverage.v0.1.md` | `reports/archive/2026-06/cyber_guqin_mvp_workflow_skill_design_and_three_target_coverage.v0.1.md` | `HISTORICAL_REFERENCE` | Referenced by skill-generation report in this move set. |
| `reports/cyber_guqin_mvp_workflow_skill_generation_report.md` | `reports/archive/2026-06/cyber_guqin_mvp_workflow_skill_generation_report.md` | `HISTORICAL_REFERENCE` | No active external references found. |
| `reports/mvp_pilot_cleanup_inventory.csv` | `reports/archive/2026-06/mvp_pilot_cleanup_inventory.csv` | `HISTORICAL_SUPERSEDED` | No active external references found. |
| `reports/mvp_pilot_cleanup_summary.md` | `reports/archive/2026-06/mvp_pilot_cleanup_summary.md` | `HISTORICAL_SUPERSEDED` | No active external references found. |
| `reports/mvp_pilot_reusable_framework_report.md` | `reports/archive/2026-06/mvp_pilot_reusable_framework_report.md` | `HISTORICAL_REFERENCE` | No active external references found. |
| `reports/next_recording_batch_generation_plan.md` | `reports/archive/2026-06/next_recording_batch_generation_plan.md` | `HISTORICAL_SUPERSEDED` | No active external references found. |
| `reports/phase_1b1_manifest_template_report.md` | `reports/archive/2026-06/phase_1b1_manifest_template_report.md` | `HISTORICAL_REFERENCE` | No active external references found. |
| `reports/project_instruction_rollback_recommendation.md` | `reports/archive/2026-06/project_instruction_rollback_recommendation.md` | `HISTORICAL_SUPERSEDED` | No active external references found. |
| `reports/qxby_batch_001_source_audit.md` | `reports/archive/2026-06/qxby_batch_001_source_audit.md` | `HISTORICAL_REFERENCE` | Referenced as regenerable/historical output path, not active source authority. |
| `reports/qxby_batch_001_source_audit.json` | `reports/archive/2026-06/qxby_batch_001_source_audit.json` | `HISTORICAL_REFERENCE` | Referenced as regenerable/historical output path, not active source authority. |
| `reports/recording_ingest_decisions_needed.md` | `reports/archive/2026-06/recording_ingest_decisions_needed.md` | `HISTORICAL_SUPERSEDED` | Referenced only as script output path. |
| `reports/recording_ingest_field_gap.json` | `reports/archive/2026-06/recording_ingest_field_gap.json` | `HISTORICAL_SUPERSEDED` | Referenced only as script output path. |
| `reports/recording_ingest_next_steps.md` | `reports/archive/2026-06/recording_ingest_next_steps.md` | `HISTORICAL_SUPERSEDED` | Referenced only as script output path. |
| `reports/recording_ingest_readiness.md` | `reports/archive/2026-06/recording_ingest_readiness.md` | `HISTORICAL_SUPERSEDED` | Referenced only as script output path. |
| `reports/reports_cleanup_plan.md` | `reports/archive/2026-06/reports_cleanup_plan.md` | `HISTORICAL_SUPERSEDED` | Superseded by this inventory. |
| `reports/reports_cleanup_summary.md` | `reports/archive/2026-06/reports_cleanup_summary.md` | `HISTORICAL_SUPERSEDED` | Superseded by this inventory. |
| `reports/slimming_recommendations.md` | `reports/archive/2026-06/slimming_recommendations.md` | `HISTORICAL_SUPERSEDED` | Referenced only by historical cleanup reports in this move set. |
| `reports/validate_canon_report.json` | `reports/archive/2026-06/validate_canon_report.json` | `HISTORICAL_REFERENCE` | Generated validation output. |
| `reports/validate_canon_seed_report.json` | `reports/archive/2026-06/validate_canon_seed_report.json` | `HISTORICAL_REFERENCE` | Generated validation output. |
| `reports/validate_dapu_ir_report.json` | `reports/archive/2026-06/validate_dapu_ir_report.json` | `HISTORICAL_REFERENCE` | Generated validation output. |
| `reports/validate_qxby_batch_001_report.json` | `reports/archive/2026-06/validate_qxby_batch_001_report.json` | `HISTORICAL_REFERENCE` | Generated validation output. |
| `reports/validate_qxby_batch_002_report.json` | `reports/archive/2026-06/validate_qxby_batch_002_report.json` | `HISTORICAL_REFERENCE` | Generated validation output. |
| `reports/xwc_f_final_token_cost_retrospective.DRY_RUN.md` | `reports/archive/2026-06/xwc_f_final_token_cost_retrospective.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Historical dry-run draft. |
| `reports/xwc_f_final_token_cost_retrospective.md` | `reports/archive/2026-06/xwc_f_final_token_cost_retrospective.md` | `HISTORICAL_REFERENCE` | Historical finalized retrospective. |
| `reports/xwc_mvp_archive_execution_report.md` | `reports/archive/2026-06/xwc_mvp_archive_execution_report.md` | `HISTORICAL_REFERENCE` | Historical cleanup execution report. |
| `reports/xwc_mvp_archive_index.DRY_RUN.md` | `reports/archive/2026-06/xwc_mvp_archive_index.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Historical cleanup dry-run index. |
| `reports/xwc_mvp_archive_index.md` | `reports/archive/2026-06/xwc_mvp_archive_index.md` | `HISTORICAL_REFERENCE` | Historical cleanup final index. |
| `reports/xwc_mvp_file_audit_cleanup_closeout.md` | `reports/archive/2026-06/xwc_mvp_file_audit_cleanup_closeout.md` | `HISTORICAL_REFERENCE` | Historical cleanup closeout. |
| `reports/xwc_mvp_file_audit_cleanup_plan.md` | `reports/archive/2026-06/xwc_mvp_file_audit_cleanup_plan.md` | `HISTORICAL_REFERENCE` | Historical cleanup plan. |
| `reports/xwc_mvp_full_process_playbook.v0.1.md` | `reports/archive/2026-06/xwc_mvp_full_process_playbook.v0.1.md` | `HISTORICAL_REFERENCE` | Superseded as active entrypoint by README, workflow skill, script registry, and reproduction runbook. |
| `reports/xwc_mvp_lessons_learned_and_pitfalls.v0.1.md` | `reports/archive/2026-06/xwc_mvp_lessons_learned_and_pitfalls.v0.1.md` | `HISTORICAL_REFERENCE` | Historical lessons report. |
| `reports/xwc_process_script_reuse_audit.DRY_RUN.md` | `reports/archive/2026-06/xwc_process_script_reuse_audit.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Superseded as active safety entrypoint by script registry. |
| `reports/xwc_r0_recovery_validation.DRY_RUN.md` | `reports/archive/2026-06/xwc_r0_recovery_validation.DRY_RUN.md` | `HISTORICAL_REFERENCE` | Historical R0 recovery validation dry-run. |

## Files Explicitly Kept In Place

- Current Qinist starter/Sanman design-review artifacts listed in the task prompt.
- Current schema drafts in `schemas/`.
- Current mock fixtures under `examples/cyber_guqin/qinist_starter_kit/`.
- Active docs: `README.md`, `docs/cyber_guqin/SCRIPT_REGISTRY.md`, `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`, and `reports/REPORTS_INDEX.md`.
- Current guard/authority evidence: `reports/varw_r012_export_contract_design.v0.1.md`, `reports/r0r1_export_manifest_reload_identity_guard_report.md`, `reports/r2_derived_export_guard_patch.md`, `reports/full_tail_natural_decay_default_patch.md`, `reports/xwc_r0_raw_file_scope_filter_patch.md`.

## Uncertain Files Left For User Review

These are not moved because they may still be used as source/canon/manifest evidence or because moving them would require a doc-link/update pass:

- `reports/c1_candidate_normalization_report.md`
- `reports/canon_seed_report.md`
- `reports/qxby_batch_001_human_review.md`
- `reports/qxby_batch_002_candidate_list.md`
- `reports/qxby_batch_002_collection_plan.md`
- `reports/qxby_batch_002_collection_plan.json`
- `reports/qxby_batch_002_report.md`
- `reports/qxby_batch_002_source_audit.md`
- `reports/qxby_batch_002_source_audit.json`
- `reports/rs_xwc_002_baiya_batch_ranges.csv`
- `reports/rs_xwc_002_baiya_generation_report.md`
- `reports/rs_xwc_002_baiya_recording_batch.md`
- `reports/rs_xwc_002_baiya_recording_day_guide.md`
- `reports/rs_xwc_002_baiya_recording_take_plan.csv`
- `reports/rs_xwc_002_baiya_session_manifest_draft.yaml`
- `reports/rs_xwc_002_baiya_validation_report.json`
- `reports/validator_parameterization_report.md`
- `reports/varw_r012_export_contract_audit.DRY_RUN.md`
- `reports/v1_to_canon_coverage.md`
- `reports/v1_to_canon_coverage.json`
- `reports/xwc_legacy_recording_bridge_map.json`
- `reports/xwc_legacy_recording_bridge_plan.md`
- `reports/xwc_legacy_take_manifest_preview.csv`
- all `06_docs/*.md`
- all `tools/cg-varw/docs/*.md`

## Red-Line Files Not Touched

- `scripts/generate_baiya_recording_plan.py`
- `sample_assets.csv`
- `recording_segments.csv`
- `recording_items_enriched.jsonl`
- accepted `F_FINAL_REVIEWED` outputs
- audio files
- ML/training files
- production runtime code
- `guqin-dapu-parser`, `guqin-canon-builder`, and `cyber_guqin_mvp_workflow` behavior

