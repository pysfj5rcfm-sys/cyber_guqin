# Qinist Starter Draft Artifact Review v0.1

Task: `CG-QINIST-STARTER-KIT-DRAFT-ARTIFACT-REVIEW-v0.1`

Status: design artifact review only. No production runtime code, audio, sample ingest, ML training, second-piece production, or accepted F output changes.

## 1. Files Reviewed

Field matrix:

- `reports/qinist_starter_field_source_matrix.v0.1.json`

Draft schemas:

- `schemas/qinist_starter_collection_item.schema.draft.yaml`
- `schemas/qinist_candidate_sidecar.schema.draft.yaml`
- `schemas/prompt_manifest.schema.draft.yaml`
- `schemas/profile_signal_extension.schema.draft.yaml`

Mock fixtures:

- `examples/cyber_guqin/qinist_starter_kit/example_single_piece_dapu_ir_input.XWC.mock.yaml`
- `examples/cyber_guqin/qinist_starter_kit/example_prompt_manifest.B01.mock.yaml`
- `examples/cyber_guqin/qinist_starter_kit/example_candidate_sidecar.mock.yaml`
- `examples/cyber_guqin/qinist_starter_kit/example_profile_signal_extension.mock.yaml`

Authority and design reports:

- `/Users/chenyulin/Downloads/RECD_VARW_Cyber_Guqin_v1.1.md`
- `reports/qinist_starter_missing_inputs.v0.1.md`
- `reports/qinist_starter_field_source_audit.v0.1.md`
- `reports/qinist_starter_kit_and_sanman_instance_design.v0.1.md`
- `reports/single_piece_dapu_ir_input_contract.v0.1.md`
- `reports/piece_demand_aggregation_and_coverage_diff_design.v0.1.md`
- `reports/qinist_candidate_sidecar_design.v0.1.md`
- `reports/varw_r2_to_qinist_profile_signal_mapping.v0.1.md`

## 2. RECD_VARW v1.1 Availability

`/Users/chenyulin/Downloads/RECD_VARW_Cyber_Guqin_v1.1.md` is available and was used as current RECD/VARW authority.

Current authority points confirmed:

- RECD/VARW serves Dapu audition and future candidate preparation, not production sample ingest.
- `qinist_id = QINIST_001` is required for the Sanman route.
- Score facts and qinist realization must remain separate.
- R0 active authority is raw marker review JSON; CSV exports are audit/compatibility.
- R1 active authority is split review JSON.
- R2 `r2_review_state.latest.json` is canonical; CSV/YAML are derived-only.
- XWC/Baiya `F_FINAL_REVIEWED` is accepted baseline with `production_grade=false` and `sample_ingest=false`.
- Current work must not write `sample_assets.csv`, `recording_segments.csv`, or `recording_items_enriched.jsonl`.

## 3. RECD&VARW v1.0 Availability

Exact `RECD&VARW · Cyber Guqin v1.0.txt` remains missing. This review keeps it listed as:

```text
MISSING_INPUT
NOT_FOUND
REQUIRED_ONLY_FOR_HISTORICAL_DELTA_AUDIT
NOT_BLOCKING_CURRENT_AUTHORITY
```

Because v1.1 is current authority, v1.0 absence is not blocking for this draft artifact review and is not blocking implementation based on `RECD_VARW_Cyber_Guqin_v1.1.md`. The exact v1.0 file is required only if the user explicitly requests a historical v1.0/v1.1 delta audit.

## 4. Field Matrix Integrity Result

Result: pass.

Checks performed:

- JSON parses.
- `matrix_version` is present.
- Warning states draft / not production / not sample ingest / not ML training.
- Every matrix field has `status`.
- Every matrix field has `canonical_owner`.
- All `proposed_extension_field` entries include approval requirement wording.
- Unsafe identities remain `rejected_or_unsafe_field`.

Attention fields checked and preserved as draft/proposed where required:

- `candidate_id`
- `starter_item_id`
- `kit_id`
- `priority_tier`
- `coverage_status`
- `prompt_manifest_id`
- `prompt_id`
- `prompt_text_zh`
- `trigger_text`
- `prompt_interval_s`
- `profile_signal_id`
- `profile_signal_type`
- `evidence_refs`
- `not_recording_items_enriched`

The proposed fields currently found are:

```text
bad_take_policy
candidate_id
coverage_status
evidence_refs
exclusion_reason
kit_id
not_recording_items_enriched
priority_tier
profile_signal_id
profile_signal_type
prompt_id
prompt_interval_s
prompt_manifest_id
prompt_order
prompt_text_zh
retake_policy
starter_item_id
trigger_text
```

Rejected/unsafe fields remain rejected:

```text
baiya_as_sanman_style
multi_piece_parser_input
qid
recording_items_enriched_jsonl
recording_segments_write
sample_asset_created
sample_id
```

## 5. Draft Schema Cross-Reference Result

Result: pass.

All four draft schemas parse with Ruby YAML and carry required warnings:

```text
DRAFT ONLY
NOT PRODUCTION CONTRACT
NOT SAMPLE INGEST
NOT ML TRAINING DATA
REQUIRES USER APPROVAL BEFORE IMPLEMENTATION
```

Every `source_matrix_ref` resolves to an existing key in `reports/qinist_starter_field_source_matrix.v0.1.json`.

No draft schema uses a `rejected_or_unsafe_field` as an active schema identity. No `legacy_alias` appears as a canonical identity field.

`schemas/qinist_candidate_sidecar.schema.draft.yaml` includes `recording_take_no` as an existing RECD/VARW provenance field. This does not authorize prompt pre-allocation or sample ingest.

`schemas/prompt_manifest.schema.draft.yaml` does not include `recording_take_no`; `prompt_id` and `prompt_order` remain prompt identities only.

## 6. Mock Fixture Safety Result

Result: pass.

All four mock fixtures parse with Ruby YAML and include:

```yaml
mock_status: MOCK_ONLY
production_grade: false
not_sample_assets: true
not_recording_segments: true
not_recording_items_enriched: true
not_ml_training_data: true
```

All four fixtures also mark `not_real_sanman_data: true`.

No mock fixture claims real Sanman data, accepted candidate status, sample asset status, sample ingest, or ML training data.

Prompt manifest fixture check:

- `prompt_id` / `prompt_order` are prompt identities only.
- No `recording_take_no` appears in the prompt manifest fixture.
- Prompt text follows the concise shape: prompt number, fingering content, trigger.
- Mock examples include `T001`, `T002`, `T003` and `trigger_text: 开始`.

Candidate sidecar mock note:

- `recording_take_no: ""` is present as empty provenance shape only.
- Because the fixture is `MOCK_ONLY`, `production_grade: false`, and `not_sample_assets: true`, it does not imply real recording authorization or sample ingest.

## 7. RECD/VARW Authority Consistency Result

Result: pass.

The draft artifacts preserve the RECD/VARW v1.1 flow:

```text
score / canon / Dapu Event IR
-> recording plan
-> raw recording
-> R0 raw review
-> R1 split review
-> R2 render review
-> ABCD / E / F audition render
-> human acceptance
-> future ML-ready candidate sidecar
```

The current design keeps:

- `QINIST_001` as Sanman route identity.
- Baiya / `QINIST_002` as accepted XWC baseline, regression case, engineering reference, and comparison qinist only.
- Score facts separated from qinist realization.
- Candidate sidecar separated from sample ingest.
- R2 profile mapping based on VARW R2 evidence instead of a disconnected label system.
- CSV/YAML R2 exports treated as derived when latest JSON exists.
- F pass separated from sample ingest authorization.

## 8. Missing Input Status

`reports/qinist_starter_missing_inputs.v0.1.md` was updated to distinguish:

- `RECD_VARW_Cyber_Guqin_v1.1.md`: available, current authority.
- `RECD&VARW · Cyber Guqin v1.0.txt`: still missing, not inferred from v1.1, historical optional, and required only if historical delta audit is explicitly requested.

Other missing implementation inputs remain:

- real Sanman starter Dapu IR
- Sanman collection inventory
- approved production starter schema
- prompt timing calibration evidence
- Qinist Profile v0.1 production schema
- sample ingest schema freeze
- rhythm render parameter config
- R2 profile mapping approval

## 9. Fixes Made

Small documentation-only fix:

- Clarified `reports/qinist_starter_missing_inputs.v0.1.md` so v1.1 is explicitly current authority and v1.0 remains a separate historical missing input.

New review artifacts:

- `reports/qinist_starter_draft_artifact_review.v0.1.md`
- `reports/qinist_starter_draft_artifact_review_findings.v0.1.json`

No schema or mock fixture edits were required.

## 10. Remaining Approval Decisions

Before implementation, the user still needs to approve or revise:

- proposed extension fields in the field matrix
- draft starter collection item shape
- draft candidate sidecar shape
- prompt manifest identity and timing policy
- profile signal extension families and evidence policy
- whether v1.0 historical delta audit is needed
- real Sanman starter Dapu IR source and first collection inventory baseline

## 11. Final Recommendation

Ready for user review.

This does not mean production readiness, sample ingest readiness, ML training readiness, or existence of a Sanman style model. It means the current draft artifacts are internally consistent enough for human design review and approval decisions.
