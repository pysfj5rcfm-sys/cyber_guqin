# CG-LXY P2C Review Checklist v0.1

Task ID: `CG-LXY-136-P2C-VISUAL-SLOT-LATTICE-DESIGN-v0.1`

Status labels:

- P2C_REVIEW_CHECKLIST
- DESIGN_REVIEW_ONLY
- COMPONENT_SLOT_LATTICE_ONLY
- NOT_RUNTIME_CODE
- NOT_PARSER_CODE
- NOT_TEST_CODE
- NOT_SCORE_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA

## 1. Scope Checklist

- [x] Output path limited to `reports/lxy_136_phase_build/`.
- [x] Only the four requested P2C files are written.
- [x] No runtime code written.
- [x] No parser code written.
- [x] No tests written.
- [x] No component registry edits.
- [x] No P2B matcher edits.
- [x] No P3 parser edits.
- [x] No sample ingest, render, recording, or ML workflow.
- [x] P2C starts from a whole notation-unit crop and stops at `VisualSlotLattice`.

## 2. Repo Context Gate Checklist

- [x] Ran `git status --short --untracked-files=all`.
- [x] Ran `git branch --show-current`.
- [x] Ran `git rev-parse HEAD`.
- [x] Ran `git log -5`.
- [x] Current branch is `main`.
- [x] Current HEAD is `ccc5377c75d56e9f8f013bf0c1cd1a914fb3f9c5`.
- [x] Recent commits include P1-A, P1-B, P1-C, P2-A, and P2-B milestones.
- [x] Pre-existing untracked P2 artifacts were left untouched.

## 3. Read Boundary Checklist

Allowed context used:

- [x] P1-A grammar contract under `reports/lxy_136_phase_build/p1a_grammar_contract/`.
- [x] P1-C parser `scripts/cyber_guqin_grammar_parser.py`.
- [x] P2-A design files under `reports/lxy_136_phase_build/`.
- [x] P2-B matcher runtime files under `scripts/`.
- [x] `component_registry.reindexed.v0.2.json`.
- [x] `component_legacy_alias_map.reindexed.v0.2.json`.
- [x] `component_visual_index.v0.1.json`.
- [x] `construction_templates.reindexed.v0.2.json`.

Forbidden context not used:

- [x] no goldset.
- [x] no phrase reports.
- [x] no old candidate reports.
- [x] no human correction data.
- [x] no LXY answer data.
- [x] no piece score facts.
- [x] no sample ingest data.
- [x] no ML training data.

## 4. Contract Acceptance Checklist

1. JSON schema PASS.
   - [x] `CG_LXY_P2C_slot_contract.v0.1.json` is valid JSON.
   - [x] `CG_LXY_P2C_spatial_relation_model.v0.1.json` is valid JSON.
   - [x] `VisualSlotLattice` schema is included in the slot contract.

2. Slot taxonomy PASS.
   - [x] Required visual slot types are present: `LEFT_UPPER`, `RIGHT_UPPER`, `MIDDLE`, `LOWER_OUTER`, `LOWER_INNER`, `ATTACHED_MARK`.
   - [x] Unknown states are present: `UNKNOWN_SLOT`, `UNKNOWN_COMPONENT`, `AMBIGUOUS_SLOT`.
   - [x] Missing and extra-ink states are present: `MISSING_COMPONENT`, `EXTRA_INK`.

3. Component/slot boundary PASS.
   - [x] Component candidates remain registry-backed P2B outputs.
   - [x] Visual slots are layout buckets, not component identities.
   - [x] Same component candidate may appear in different visual slots without role collapse.

4. Semantic role separation PASS.
   - [x] P2C visual slot types are not P1/P3 semantic slots.
   - [x] Visual labels remain literal component candidates.
   - [x] Numeric labels are not assigned hui or string roles in P2C.
   - [x] Motion and action labels are not assigned final grammar roles in P2C.

5. No concrete phrase reading PASS.
   - [x] P2C design contains no complete notation-unit reading output.
   - [x] P2C output examples are component labels, slots, and relations only.
   - [x] P3 remains the first layer allowed to decide legal grammar parse.

6. No oracle leakage PASS.
   - [x] Fixture contract is oracle-free.
   - [x] Forbidden sources are listed and excluded.
   - [x] Human correction and answer data are forbidden input fields.
   - [x] Gold answer references are forbidden input fields.

7. P2B interface PASS.
   - [x] P2C calls P2B only with component crop hypotheses.
   - [x] P2C does not require P2B matcher modification.
   - [x] P2C preserves P2B `UNKNOWN_COMPONENT` instead of forcing identity.

8. P3 interface PASS.
   - [x] P2C handoff contains `slot_candidates`, `component_candidates`, `spatial_relations`, and `confidence`.
   - [x] P2C does not call `GrammarParser.parse()`.
   - [x] P2C does not output accepted parser candidates.

9. Spatial relation PASS.
   - [x] Required relations are present: `above`, `below`, `left_of`, `right_of`, `inside`, `attached`.
   - [x] Spatial relations are visual evidence only.
   - [x] Non-linear notation layout is preserved.

10. Fixture coverage design PASS.
    - [x] Single component unit.
    - [x] Two component unit.
    - [x] Multi component notation unit.
    - [x] Ambiguous visual slot.
    - [x] Missing component.
    - [x] Extra ink.
    - [x] Component order variation.
    - [x] Same component different slot.

## 5. Final Readiness Flags

```json
{
  "ready_for_P2C_implementation_design": true,
  "ready_for_LXY_phrase_reading": false,
  "ready_for_training_model": false
}
```
