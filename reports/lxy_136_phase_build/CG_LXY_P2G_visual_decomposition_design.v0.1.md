# CG-LXY P2G Visual Decomposition Design v0.1

Task ID: `CG-LXY-136-P2G-VISUAL-DECOMPOSITION-v0.1`

Status labels:

- P2G_VISUAL_DECOMPOSITION
- VISUAL_STRUCTURE_PATTERN_REGISTRY
- VISUAL_ONLY_SEGMENTATION_TREE
- HUMAN_REVIEW_EXTENSIBLE
- NOT_COMPONENT_ID_AUTHORITY
- NOT_GRAMMAR_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NEEDS_HUMAN_REVIEW

## Purpose

P2G is a visual decomposition layer for notation-unit crops. It answers:

```text
What visual structure units exist in this crop, and how are they nested, adjacent, or attached?
```

It does not answer:

```text
What component ids are these?
What grammar rule validates them?
What is the surface reading?
What score fact or Dapu IR should be emitted?
```

## Pipeline Boundary

```text
notation_unit_crop
  -> P2G Visual Decomposition
  -> segmentation_tree_candidates
  -> P2B Component Matcher
  -> component_candidate_lattice
  -> P3 Visual Grammar Fusion
  -> grammar validation / review-only reading candidate
```

P2G must not call P2B, P1, or P3 while generating visual decomposition candidates. Grammar can be used only as a later P3 posterior validator, not as the primary cutting criterion.

## Runtime Files

- Runtime: `scripts/visual_decomposition_runtime.py`
- Tests: `tests/test_visual_decomposition_runtime.py`
- Pattern registry: `references/qxby_component_atlas/visual_structure_patterns.v0.1.json`

The first runtime is intentionally independent from the existing P2D `NotationUnitAnalyzer` so current P2C/P2D worktree edits are not overwritten. A later compatibility task can project P2G trees into the old flat P2D slot lattice.

## Output Contract

The runtime returns:

```json
{
  "layout_candidates": [],
  "segmentation_tree_candidates": [],
  "component_region_candidates": [],
  "quality_metrics": {},
  "failure_flags": [],
  "review_packet": {},
  "pattern_registry_trace": {},
  "authority_flags": {}
}
```

Nodes use visual roles only:

```text
root
upper_band
middle_band
lower_band
upper_left_region
upper_right_region
middle_region
lower_left_region
lower_inner_region
lower_outer_region
attached_mark
bridge_or_overlap_region
unknown_visual_region
```

Forbidden in P2G output:

```text
component_id
semantic_role
LEFT_FINGER
HUI_POSITION
RIGHT_HAND_ACTION
STRING_NUMBER
surface_reading
score_fact
Dapu IR
```

## Layout Families

Initial layout families:

```text
UPPER_LOWER
UPPER_MIDDLE_LOWER
LOWER_ONLY
LEFT_RIGHT
ENCLOSURE_WITH_INNER
ATTACHED_MARKS
SCATTERED_OR_AMBIGUOUS
```

The runtime first proposes large visual bands, then recursively parses each band into region nodes. Enclosing shapes must retain parent-child structure instead of being flattened into sibling regions.

## Runtime Decomposition Stages

Current runtime stages:

```text
image crop
-> black/near-black ink extraction
-> raw ink connected components
-> fragment-to-visual-unit grouping
-> layout family detection
-> recursive visual tree proposal
-> component_region_candidates for later P2B calls
```

The ink extractor treats high-chroma pixels as non-ink so human review overlays such as red boxes or circles do not become score strokes. This keeps annotated debug screenshots usable for decomposition sanity checks.

The grouping layer distinguishes:

```text
raw_ink_region_count
visual_unit_count
```

Small disconnected fragments are attached to nearby visual anchors using local distance and overlap only. This is still visual-only: grouping cannot use component ids, construction templates, grammar validity, phrase readings, or any oracle answer.

## Extensibility Model

New structure support is added through `visual_structure_patterns.v0.1.json`, not by changing grammar or construction-template answers.

Lifecycle:

```text
UNKNOWN_STRUCTURE_CANDIDATE
-> HUMAN_BOX_REVIEWED
-> STRUCTURE_PATTERN_DRAFT
-> FIXTURE_VALIDATED
-> HUMAN_REVIEWED_ACTIVE
-> DEPRECATED / SUPERSEDED
```

Every pattern is visual-only. A pattern may define layout family, allowed visual roles, decomposition rules, quality metrics, and forbidden segmentation failures. It must not define component ids, score roles, phrase readings, or grammar productions.

## Failure Flags

Initial flags:

```text
NO_INK_DETECTED
UNKNOWN_STRUCTURE_CANDIDATE
OVER_MERGED_REGION
ENCLOSURE_INNER_NOT_FOUND
```

Planned flags:

```text
UNDER_SPLIT_REGION
INNER_COMPONENT_OUTSIDE_PARENT
ENCLOSURE_LOST
ATTACHED_MARK_DROPPED
BRIDGE_REGION_UNRESOLVED
COVERAGE_GAP
EXCESS_BACKGROUND
```

Current P2D failure on real crops maps to `OVER_MERGED_REGION`: a large region covers the whole notation unit and smaller fragments are treated as inside regions instead of a useful visual tree.

## Validation

Current tests verify:

- nested notation-unit crops produce a visual-only tree;
- lower enclosure / inner regions are represented with parent-child structure;
- unknown scattered structures emit a human review packet;
- fragmented ink regions are grouped into visual units before P2B;
- PNG input is supported without requiring Pillow;
- red human-review marks are ignored as score ink;
- default visual patterns load as visual-only and contain no semantic patterns.

Validation commands:

```bash
python3 -m unittest tests.test_visual_decomposition_runtime -v
python3 -m json.tool references/qxby_component_atlas/visual_structure_patterns.v0.1.json
```

## Next Step

The next integration task should project P2G `component_region_candidates` into P2B crop calls and keep the results in a separate component candidate lattice. That integration must preserve the scoring separation:

```text
P2G visual score
P2B component score
P3 grammar score
```
