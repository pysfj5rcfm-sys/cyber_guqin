# CG-LXY P2A Review Checklist v0.1

Task ID: `CG-LXY-136-P2A-VISUAL-COMPONENT-CANDIDATE-DESIGN-v0.1`

Status labels:

- P2A_REVIEW_CHECKLIST
- DESIGN_REVIEW_ONLY
- COMPONENT_CANDIDATE_ONLY
- NEEDS_HUMAN_REVIEW
- NOT_PARSER_CODE
- NOT_IMAGE_MODEL_CODE
- NOT_TRAINING_CODE
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY

## 1. Scope Checklist

- [x] Output path limited to `reports/lxy_136_phase_build/`.
- [x] No parser code written.
- [x] No image model code written.
- [x] No training code written.
- [x] No component registry edits.
- [x] No source image edits.
- [x] No sample ingest, recording, render, or ML workflow.
- [x] P2A starts from one component crop and stops at component candidates/top-k lattice.

## 2. Read Boundary Checklist

Allowed context used:

- [x] 1-3-6 phase build docs under `reports/lxy_136_phase_build/`.
- [x] P1-A grammar contract under `reports/lxy_136_phase_build/p1a_grammar_contract/`.
- [x] P1-B fixtures matching `p1b_*`.
- [x] P1-C parser `scripts/cyber_guqin_grammar_parser.py`.
- [x] P1-C implementation report.
- [x] `component_registry.reindexed.v0.2.json`.
- [x] `component_legacy_alias_map.reindexed.v0.2.json`.
- [x] component image inventory under `sources/qxby_component_atlas/images/`.

Forbidden context not used:

- [x] no LXY phrase reports.
- [x] no goldset oracle.
- [x] no `lxy_p1_p6_goldset*`.
- [x] no complete phrase reading.
- [x] no human-corrected answer reports.
- [x] no `01_pieces/`.
- [x] no `04_outputs/`.
- [x] no sample ingest data.
- [x] no recording data.
- [x] no ML data.

## 3. Contract Acceptance Checklist

1. Component registry can cover all candidate output.
   - [x] `ComponentCandidate.component_id_v0_2` must be present in registry `components` or `auxiliary_components`.
   - [x] unknown state is not emitted as a fake `COMP-*` candidate.

2. Unknown component has a clear state.
   - [x] `unknown_component_state.status` includes `UNKNOWN_COMPONENT`.
   - [x] `coverage_ledger.unresolved_reason` records the reason.
   - [x] `needs_human_review=true`.

3. Confidence does not pretend to be probability.
   - [x] `score_type=HEURISTIC_VISUAL_CONFIDENCE`.
   - [x] `calibrated_probability=false`.
   - [x] review language avoids probability claims.

4. Top-k can be sorted.
   - [x] deterministic rank policy is defined.
   - [x] `candidate_rank` is unique and contiguous per crop.
   - [x] tie-break ends on `component_id_v0_2`.

5. Different model outputs can enter the unified candidate contract.
   - [x] template matching, visual embedding, OCR-assisted proposal, and human feedback all normalize to `ComponentCandidateEvidence`.
   - [x] fusion emits only `ComponentCandidate[]`.

6. P2A does not output phrase reading.
   - [x] candidate schema forbids reading fields.
   - [x] examples contain component labels only.

7. P2A does not output score facts.
   - [x] authority flags set `not_score_event_authority=true`.
   - [x] score-event fields are forbidden.

8. P2A does not output Dapu IR.
   - [x] authority flags set `not_dapu_ir_authority=true`.
   - [x] Dapu IR fields are forbidden.

## 4. P2B Implementation Design Handoff

P2B may design implementation details for:

- image preprocessing interface;
- template matching adapter;
- embedding adapter;
- OCR hint adapter;
- candidate fusion;
- JSON validation;
- review UI or review sheet for component candidates only.

P2B must not start:

- phrase reading;
- parser integration beyond contract planning;
- visual model training;
- sample ingest;
- Dapu IR generation;
- score fact promotion.

## 5. Final Readiness Flags

```json
{
  "ready_for_P2B_implementation_design": true,
  "ready_for_visual_model_training": false,
  "ready_for_LXY_phrase_reading": false
}
```

