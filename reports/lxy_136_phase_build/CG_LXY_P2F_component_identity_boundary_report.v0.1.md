# CG-LXY P2F Component Identity Boundary Report v0.1

Task ID: `CG-LXY-136-P2F-COMPONENT-IDENTITY-BOUNDARY-FIX-v0.1`

Status labels:

- P2_COMPONENT_IDENTITY_BOUNDARY_FIXED
- P2_OUTPUT_COMPONENT_CANDIDATE_LATTICE_ONLY
- SEMANTIC_ROLE_DEFERRED_TO_P3
- SURFACE_READING_DEFERRED_TO_P3
- NOT_P3_IMPLEMENTATION
- NOT_SCORE_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA

## Repo Context Gate

Preflight result:

```text
current_branch: main
HEAD: bac3a1c2866c4c347902f877c6c281aeb95ea3cb
main: bac3a1c2866c4c347902f877c6c281aeb95ea3cb
HEAD_matches_main: true
worktree_status_before_p2f: clean
```

Allowed context read:

- `CG_LXY_136_Phase_Build_Requirements_v0.1.md`
- P1-A grammar contract
- P1-B fixture design
- P1-C parser MVP report
- P2-A visual component design
- P2-B component matcher report
- P2-C slot contract/design
- P2-D notation analyzer implementation report and runtime

Forbidden context not used: LXY phrase reports, goldset oracle, old candidate readings, human correction reports, and concrete piece answers.

## Files Modified

- `scripts/notation_unit_analyzer.py`
- `tests/test_notation_unit_analyzer.py`
- `tests/test_component_identity_boundary.py`
- `reports/lxy_136_phase_build/CG_LXY_P2C_visual_slot_lattice_design.v0.1.md`
- `reports/lxy_136_phase_build/CG_LXY_P2C_slot_contract.v0.1.json`
- `reports/lxy_136_phase_build/CG_LXY_P2D_implementation_report.v0.1.md`
- `reports/lxy_136_phase_build/CG_LXY_P2F_component_identity_boundary_report.v0.1.md`

## Boundary Fix

P2D runtime now outputs a Visual Slot Lattice whose slot candidates are component-identity records only:

```json
{
  "component_id": "COMP-091",
  "visual_score": 0.86,
  "confidence": {
    "value": 0.86,
    "bucket": "high",
    "score_type": "HEURISTIC_VISUAL_CONFIDENCE",
    "calibrated_probability": false
  },
  "candidate_rank": 0,
  "source_region_id": "region_001"
}
```

The P3 handoff projection now carries component candidates as:

```json
{
  "slot_id": "slot_001",
  "source_region_id": "region_001",
  "component_id": "COMP-091",
  "confidence": {
    "value": 0.86,
    "bucket": "high",
    "score_type": "HEURISTIC_VISUAL_CONFIDENCE",
    "calibrated_probability": false
  },
  "visual_score": 0.86
}
```

Display/debug fields from P2B such as label/name/category may remain inside the matcher layer for human inspection, but they are not emitted by P2D and are not part of the P3 handoff projection.

## Fields Explicitly Forbidden From P2D Output

- `semantic_role`
- `semantic_role_assigned`
- `reading`
- `surface_reading`
- `surface_reading_candidate`
- `canonical_reading`
- `phrase_reading`
- `complete_reading`
- `slot_meaning`
- `dapu_ir`
- `Dapu_IR`

P2D also no longer emits display/debug fields such as `label` or `lexical_component_type` in slot candidates or P3 handoff candidates.

## D1 Registry Schema Review

Observed registry:

```text
references/qxby_component_atlas/component_registry.reindexed.v0.2.json
```

Current fields include:

- `component_id`
- `label_zh`
- `component_family`
- `category` on auxiliary components
- `source_image_path_v0_1`
- `semantic_alias_refs`
- `legacy_refs`

Target schema mapping for future cleanup:

```text
component_id <- component_id
name <- label_zh
category <- component_family or category
image_ref <- source_image_path_v0_1
aliases <- legacy_refs / semantic_alias_refs after explicit schema migration
```

No new registry fields were added. No `glyph_atom`, `visual_primitive`, or `visual_label_as_intermediate` layer was introduced.

## P2/P3 Boundary

Restored interface:

```text
P2 Output: Component Candidate Lattice
P3 Input: Component Candidate Lattice
P3 responsibility: component_id -> semantic slot -> grammar production -> surface reading
```

Numeric handling is component identity only in P2. For example, `NUM-009` is accepted as a component identity shape in P2D validation; P2 does not decide whether it is hui position, string number, count, or unresolved.

## Validation Evidence

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 -m unittest tests/test_component_identity_boundary.py
Ran 4 tests in 0.018s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 -m unittest tests/test_notation_unit_analyzer.py
Ran 9 tests in 0.034s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 -m unittest tests/test_component_identity_boundary.py tests/test_notation_unit_analyzer.py tests/test_component_visual_layer.py tests/test_component_matcher.py
Ran 31 tests in 0.117s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 -m unittest tests/test_cyber_guqin_grammar_parser.py tests/test_cyber_guqin_grammar_parser_properties.py tests/test_cyber_guqin_grammar_parser_metamorphic.py
Ran 25 tests in 0.143s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 scripts/run_cyber_guqin_grammar_fixtures.py --repo-root /Users/chenyulin/Documents/AIProjects/cyber_guqin --fixture-dir /Users/chenyulin/Documents/AIProjects/cyber_guqin/tests/fixtures/cyber_guqin/component_guided_transcription --output /tmp/cg_lxy_p2f_p1_fixture_results.json
pass_count: 75
fail_count: 0
discovered_case_count: 75
```

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 -m compileall scripts/notation_unit_analyzer.py tests/test_component_identity_boundary.py tests/test_notation_unit_analyzer.py
PASS
```

```text
python3 -m json.tool reports/lxy_136_phase_build/CG_LXY_P2C_slot_contract.v0.1.json
PASS
```

```text
PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2f_pycache python3 -m unittest tests/test_component_identity_boundary.py tests/test_notation_unit_analyzer.py tests/test_component_visual_layer.py tests/test_component_matcher.py tests/test_cyber_guqin_grammar_parser.py tests/test_cyber_guqin_grammar_parser_properties.py tests/test_cyber_guqin_grammar_parser_metamorphic.py
Ran 56 tests in 0.192s
OK
```

```text
git diff --check
PASS
```

## Acceptance Conclusion

1. P2 runtime output no longer contains `semantic_role`.
2. P2 runtime output no longer contains `reading` / `surface_reading`.
3. P2D output is component-id based.
4. P1 parser input remains component sequence based; P1 parser code and grammar rules were not modified.
5. Existing P1/P2 regression checks passed.
6. New `test_component_identity_boundary.py` passed.

```json
{
  "ready_for_P3_visual_grammar_fusion": true
}
```
