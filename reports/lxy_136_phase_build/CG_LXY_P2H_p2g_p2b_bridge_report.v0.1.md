# CG-LXY P2H P2G-P2B Bridge Report v0.1

Task ID: `CG-LXY-136-P2H-P2G-P2B-BRIDGE-v0.1`

Status labels:

- P2G_TO_P2B_BRIDGE
- COMPONENT_REGION_CROP_RUNTIME
- COMPONENT_CANDIDATE_LATTICE
- VISUAL_ONLY_SEGMENTATION_SOURCE
- NOT_GRAMMAR_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NEEDS_HUMAN_REVIEW

## Scope

This report documents the bridge from P2G visual decomposition to P2B component matching.

Implemented flow:

```text
notation_unit_crop
-> P2G VisualDecomposer
-> component_region_candidates
-> P2GComponentLatticeRuntime
-> P2B ComponentMatcher per region crop
-> component_candidate_sets
-> component_candidate_lattice
-> P3 handoff projection
```

Out of scope:

```text
phrase reading
surface reading
grammar parse
score fact
Dapu IR
sample ingest
ML training
```

## Files

- Runtime: `scripts/p2g_component_lattice_runtime.py`
- Tests: `tests/test_p2g_component_lattice_runtime.py`
- Related P2G runtime: `scripts/visual_decomposition_runtime.py`
- Related design: `reports/lxy_136_phase_build/CG_LXY_P2G_visual_decomposition_design.v0.1.md`

## Output Contract

The bridge returns:

```json
{
  "contract_id": "CG_LXY_P2G_P2B_component_lattice.v0.1",
  "notation_unit_id": "",
  "status": "MATCHED | PARTIAL | UNRESOLVED",
  "component_candidate_sets": [],
  "component_candidate_lattice": {},
  "p3_handoff_projection": {
    "component_candidates": []
  },
  "failure_flags": [],
  "authority_flags": {},
  "runtime_trace": {}
}
```

`component_candidate_sets` preserves P2B matcher evidence. `p3_handoff_projection` is intentionally narrow:

```text
region_id
node_id
visual_role
bbox
component_id
confidence
visual_score
```

It does not include readings, grammar slots, score facts, or Dapu IR.

## Real Image Sanity Check

Input image:

```text
/Users/chenyulin/Desktop/截屏2026-07-08 11.48.59.png
```

P2G decomposition:

```text
layout: UPPER_MIDDLE_LOWER
raw_ink_region_count: 34
visual_unit_count: 5
```

P2G region candidates:

```text
upper_left_region  [25, 21, 44, 47]
upper_right_region [65, 11, 62, 55]
middle_region      [67, 62, 49, 45]
lower_left_region  [17, 77, 32, 57]
lower_right_region [54, 78, 88, 55]
```

P2B Top-K sanity output:

```text
upper_left_region:
  COMP-802 入慢 0.740
  COMP-501 上 0.698
  COMP-816 蓄 0.683

upper_right_region:
  COMP-503 使 0.618
  COMP-907 就 0.603
  COMP-105 半轮 0.595

middle_region:
  COMP-822 顿 0.677
  COMP-501 上 0.668
  COMP-811 接 0.663

lower_left_region:
  COMP-418 注 0.604
  COMP-818 踢宕 0.586
  COMP-430 缓急吟 0.571

lower_right_region:
  COMP-702 徽 0.592
  COMP-116 挑 0.589
  COMP-516 掩 0.589
```

This verifies that the bridge can generate per-region Top-K component candidates. It does not verify that the correct component is ranked first.

## Current Interpretation

P2G segmentation is now the stronger part of this chain for this test image: it returns five visual units matching the intended decomposition shape.

P2B still needs ranking improvement for fragmented, auxiliary, or non-matchable components. Known boundary examples include auxiliary components that are present in D1 but marked non-matchable, and visual components whose correct identity appears below rank 1.

Therefore:

```text
ready_for_P3_visual_grammar_fusion: true
ready_for_final_reading: false
ready_for_score_fact: false
```

## Validation

Commands used:

```bash
python3 -m unittest tests.test_p2g_component_lattice_runtime -q
python3 -m unittest tests.test_visual_decomposition_runtime -q
```

The bridge test verifies:

- P2G visual region bboxes are cropped into PNG files;
- P2B matcher is called once per region;
- candidate sets are assembled into a component lattice;
- P3 handoff projection remains narrow;
- P1/P3 grammar is not called during bridge generation.
