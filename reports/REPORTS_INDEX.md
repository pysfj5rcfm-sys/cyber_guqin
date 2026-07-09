# Reports Index

`reports/` contains audit/status evidence, design notes, generated validation reports, and latest repo hygiene reports. It is not runtime output and not canonical authority.

Audio/runtime outputs belong under `04_outputs/`. R2 canonical authority remains:

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`

Accepted baseline / forbidden-to-touch:

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`

## Latest Repo Hygiene Reports

Use these latest R0 files as the current basis for repo hygiene decisions:

| File | Role |
| --- | --- |
| `repo_hygiene_audit.latest.v0.1.md` | Latest readonly audit and R1 readiness conclusion. |
| `repo_hygiene_inventory.latest.v0.1.json` | Latest inventory, guardrails, directory classification, authority map, and duplicate hotspots. |
| `repo_cleanup_candidates.latest.v0.1.csv` | Latest cleanup/index-only/forbidden-to-touch candidate table. |
| `repo_entrypoint_map.latest.v0.1.md` | Latest entrypoint and authority map. |

Older non-latest R0 reports are historical reference only.

## P1-F Reproduction Reports

| File | Role |
| --- | --- |
| `self_contained_reproduction_toolchain_report.md` | Evidence that the P1-F dry-run reproduction toolchain exists. |
| `rs_xwc_002_baiya_generation_report.md` | XWC/Baiya generation evidence. |
| `rs_xwc_002_baiya_recording_batch.md` | Recording batch evidence. |
| `rs_xwc_002_baiya_recording_day_guide.md` | Recording-day guide evidence. |
| `rs_xwc_002_baiya_recording_take_plan.csv` | Take-plan evidence; report artifact, not canonical R2 authority. |
| `rs_xwc_002_baiya_session_manifest_draft.yaml` | Draft session manifest evidence. |
| `rs_xwc_002_baiya_validation_report.json` | Generated validation evidence. |
| `rs_xwc_002_baiya_batch_ranges.csv` | Batch range evidence. |

Current P1-F docs live in `docs/cyber_guqin/`; example manifests live in `examples/cyber_guqin/`.

## QINIST Starter Kit / Sanman Reports

| File or Pattern | Role |
| --- | --- |
| `qinist_starter_kit_and_sanman_instance_design.v0.1.md` | Starter-kit and Sanman instance design. |
| `qinist_starter_design_freeze.v0.1.md` | Design-freeze narrative. |
| `qinist_starter_design_freeze_decisions.v0.1.json` | Design-freeze decision evidence. |
| `qinist_starter_field_source_audit.v0.1.md` | Field/source audit. |
| `qinist_starter_field_source_matrix.v0.1.json` | Field/source matrix evidence. |
| `qinist_starter_draft_artifact_review.v0.1.md` | Draft artifact review. |
| `qinist_starter_draft_artifact_review_findings.v0.1.json` | Draft artifact review findings. |
| `qinist_starter_missing_inputs.v0.1.md` | Missing-inputs report. |
| `qinist_candidate_sidecar_design.v0.1.md` | Candidate sidecar design. |
| `ai_prompted_collection_protocol.v0.1.md` | AI-prompted collection protocol. |
| `universal_qinist_starter_collection_kit.v0.1.md` | Universal QINIST starter collection kit. |
| `single_piece_dapu_ir_input_contract.v0.1.md` | Single-piece Dapu IR input contract. |
| `varw_r2_to_qinist_profile_signal_mapping.v0.1.md` | VARW R2 to qinist profile-signal mapping. |

These reports support the current QINIST_001 Sanman digitization startup work, but they do not start sample ingest or ML training.

## VARW / Contract / Patch Reports

| File or Pattern | Role |
| --- | --- |
| `varw_r012_export_contract_design.v0.1.md` | R0/R1/R2 export contract design. |
| `varw_r012_export_contract_audit.DRY_RUN.md` | Dry-run export contract audit. |
| `r0r1_export_manifest_reload_identity_guard_report.md` | R0/R1 export reload identity guard report. |
| `r2_derived_export_guard_patch.md` | Derived export guard patch report. |
| `xwc_r0_raw_file_scope_filter_patch.md` | XWC R0 raw-file scope filter patch. |
| `full_tail_natural_decay_default_patch.md` | Full-tail natural-decay default patch report. |
| `rhythm_diverse_abcd_strategy_design.v0.1.md` | Rhythm-diverse ABCD strategy design. |
| `engineering_tail_backlog.v0.1.md` | Engineering tail backlog. |

CG-VARW chronological docs are indexed separately in `tools/cg-varw/docs/INDEX.md`.

## Generated Validation / Audit Reports

| File or Pattern | Role |
| --- | --- |
| `canon_seed_report.md` | Canon seed report evidence. |
| `c1_candidate_normalization_report.md` | Candidate normalization report. |
| `validator_parameterization_report.md` | Validator parameterization report. |
| `v1_to_canon_coverage.md` | V1-to-canon coverage report. |
| `v1_to_canon_coverage.json` | Generated coverage data. |
| `qxby_batch_*.md`, `qxby_batch_*.json` | QXBY batch planning, audit, and evidence. |
| `xwc_legacy_recording_bridge_plan.md` | Legacy bridge plan. |
| `xwc_legacy_recording_bridge_map.json` | Legacy bridge generated map. |
| `xwc_legacy_take_manifest_preview.csv` | Legacy preview CSV; report evidence only. |

Validator runs may recreate JSON reports in `reports/` root. Generated validator reports can be archived again under `reports/archive/` in a separate cleanup/archive task.

## CG-LXY-136 Phase Build Reports

| File or Pattern | Role |
| --- | --- |
| `lxy_136_phase_build/CG_LXY_P1_P2_handoff_to_P3.v0.1.md` | Current P1/P2 handoff and P3 visual-grammar fusion recommendations. |
| `lxy_136_phase_build/CG_LXY_P2G_visual_decomposition_design.v0.1.md` | P2G visual-only decomposition design and runtime boundary. |
| `lxy_136_phase_build/CG_LXY_P2H_p2g_p2b_bridge_report.v0.1.md` | P2G-to-P2B component candidate lattice bridge evidence. |
| `lxy_136_phase_build/CG_LXY_P2I_component_ranking_audit_report.v0.1.md` | Component-level P2B ranking audit and cross-validation boundary. |
| `lxy_136_phase_build/CG_LXY_P2J_auxiliary_matchability_update_report.v0.1.md` | Auxiliary component matchability update and numeric one-to-seven provisional coverage. |

These reports are review and implementation evidence only. They do not authorize phrase reading, score facts, Dapu IR, sample ingest, or ML training.

## Archive Layout

- `reports/archive/2026-06/`: Historical audit reports, old batch reports, generated validation outputs, cleanup plans, retrospective reports, and completed staging artifacts from June 2026.

Do not clean `reports/archive/` in index/policy tasks. Archived reports are historical evidence, not current workflow authority.

## Operating Rules

- Do not treat `reports/` as runtime output.
- Do not treat `reports/` or `reports/archive/` as canonical authority.
- Do not promote R2 CSV/YAML exports to canonical authority.
- Do not move, delete, archive, or clean reports without a separate authorized cleanup/archive task.
- Do not use reports to bypass score, canon, R2, or F gates.
