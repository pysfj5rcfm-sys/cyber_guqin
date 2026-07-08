# CG-LXY P2D Visual Slot Lattice Implementation Report v0.1

Task ID: `CG-LXY-136-P2D-VISUAL-SLOT-LATTICE-IMPLEMENTATION-v0.1`

Status labels:

- P2D_VISUAL_SLOT_LATTICE_RUNTIME_MVP
- NOTATION_UNIT_ANALYZER_IMPLEMENTED
- COMPONENT_SLOT_SEPARATION_ENFORCED
- SEMANTIC_ROLE_SEPARATION_ENFORCED
- UNKNOWN_COMPONENT_SUPPORTED
- UNKNOWN_SLOT_SUPPORTED
- AMBIGUOUS_SLOT_SUPPORTED
- MISSING_COMPONENT_SUPPORTED
- SPATIAL_RELATION_GRAPH_IMPLEMENTED
- NOT_SCORE_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA

## Repo Context Gate

Preflight commands were run before implementation:

```text
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
git log -5 --oneline
```

Observed context:

```text
current_branch: main
current_head: 1649defb8be163ee4ead749a539ae242b5c6efe8
recent_head_subject: docs(lxy): define phase2 visual slot lattice design
worktree_status_before_p2d: clean
```

Confirmed existing layers:

- P1-C Grammar Parser: `scripts/cyber_guqin_grammar_parser.py`
- P2-B Visual Component Layer: `scripts/component_matcher_runtime.py`, `scripts/component_visual_index.py`, `scripts/component_candidate_lattice.py`
- P2-C Slot Lattice Design: `reports/lxy_136_phase_build/CG_LXY_P2C_visual_slot_lattice_design.v0.1.md`, `CG_LXY_P2C_slot_contract.v0.1.json`, `CG_LXY_P2C_spatial_relation_model.v0.1.json`

## Implementation Summary

Added `scripts/notation_unit_analyzer.py`.

The runtime accepts a notation-unit crop path or a `NotationUnitCrop` object and returns a Visual Slot Lattice. It performs deterministic visual region detection, proposes visual slots from geometry, calls the injected or default P2B `ComponentMatcher` once per detected region, and builds component-level spatial relations.

The runtime does not call P1, does not produce phrase reading, does not inherit context, does not emit Dapu IR, does not ingest samples, and does not train or download a model.

## Boundary Decisions

P2D keeps visual slots separate from semantic roles:

- slot types are loaded from the P2-C slot contract;
- candidates preserve P2B component labels and lexical component types only;
- every component candidate has `semantic_role: "unknown"`;
- every slot has `semantic_role_assigned: false`;
- numeric components such as `九` remain component/lexical candidates, not hui or string assignments.

The analyzer does not hardcode component IDs. New component IDs returned by the registry/image-index-backed matcher pass through the lattice without slot analyzer changes.

## Unknown Policy

The runtime explicitly supports:

- `UNKNOWN_SLOT`
- `UNKNOWN_COMPONENT`
- `AMBIGUOUS_SLOT`
- `MISSING_COMPONENT`
- `EXTRA_INK`

It does not fabricate a component candidate when evidence is missing.

## Spatial Relations

Implemented relation aliases:

- `ABOVE`
- `BELOW`
- `LEFT_OF`
- `RIGHT_OF`
- `INSIDE`
- `ATTACHED`

Each relation also carries P2-C-compatible lowercase `relation_type` and geometry evidence. Relations are deterministic and sorted by source region, target region, and relation priority.

## Tests

Added `tests/test_notation_unit_analyzer.py` with coverage for:

1. single component unit
2. two component unit
3. multi component unit
4. missing component
5. ambiguous slot
6. spatial relation deterministic
7. same image deterministic
8. extension with new component
9. required spatial relation types include `INSIDE` and `ATTACHED`

TDD red state was confirmed before implementation:

```text
ModuleNotFoundError: No module named 'scripts.notation_unit_analyzer'
```

Green target validation:

```text
PYTHONPYCACHEPREFIX=/tmp/cyber_guqin_p2d_pycache python3 -m unittest tests/test_notation_unit_analyzer.py
Ran 9 tests in 0.033s
OK
```

Repository-level unittest observations:

```text
PYTHONPYCACHEPREFIX=/tmp/cyber_guqin_p2d_pycache python3 -m unittest
Ran 0 tests in 0.000s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/cyber_guqin_p2d_pycache python3 -m unittest discover -s tests
Ran 68 tests in 0.592s
FAILED (failures=1)
```

The discover failure is outside the P2D files:

```text
test_self_contained_reproduction_toolchain.DocsExamplesAndLegacySafetyTests
AssertionError: BAIYA_PLAN_SCRIPT.exists() is false
```

This P2D implementation did not modify the Baiya legacy reproduction script or that test.

## Readiness

```json
{
  "ready_for_P3_visual_grammar_fusion": true,
  "ready_for_LXY_phrase_reading": false,
  "ready_for_training_model": false
}
```
