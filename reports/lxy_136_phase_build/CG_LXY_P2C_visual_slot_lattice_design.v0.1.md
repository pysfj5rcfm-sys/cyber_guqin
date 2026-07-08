# CG-LXY P2C Visual Slot Lattice Design v0.1

Task ID: `CG-LXY-136-P2C-VISUAL-SLOT-LATTICE-DESIGN-v0.1`

Status labels:

- P2C_VISUAL_SLOT_LATTICE_DESIGN
- NOTATION_UNIT_ANALYZER_DESIGN
- COMPONENT_SLOT_LATTICE_ONLY
- TOP_K_SLOT_CANDIDATES
- SPATIAL_RELATION_GRAPH
- UNKNOWN_COMPONENT_SUPPORTED
- UNKNOWN_SLOT_SUPPORTED
- AMBIGUOUS_SLOT_SUPPORTED
- NEEDS_HUMAN_REVIEW
- NOT_RUNTIME_CODE
- NOT_PARSER_CODE
- NOT_TEST_CODE
- NOT_SCORE_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA

## 1. Scope

P2C designs the Visual Slot Lattice Layer between whole notation-unit images and later grammar parsing.

```text
notation unit crop
-> NotationUnitAnalyzer
-> visual region hypotheses
-> visual slot candidates
-> P2B ComponentMatcher calls on component crop hypotheses
-> VisualSlotLattice
```

P2C is not a reading layer. It does not output a complete jianzipu reading, phrase, Dapu IR, score fact, sample, render artifact, or ML training row.

The only intended P2C output is an internal visual lattice:

- visual slot candidates;
- component candidates returned by P2B;
- spatial relations between region hypotheses;
- non-probabilistic visual confidence;
- unresolved states for missing, unknown, ambiguous, or extra-ink evidence.

## 2. Repo Context Gate

Preflight commands were checked before writing this design:

```text
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
git log -5
```

Observed context:

```text
current_branch: main
current_head: ccc5377c75d56e9f8f013bf0c1cd1a914fb3f9c5
recent_head_subject: feat(lxy): implement phase2 component matcher mvp
```

The worktree already contained untracked P2 artifacts before P2C started. They were treated as existing user or prior-step output and were not modified by this P2C design task.

Confirmed existing layers:

- P1-A Grammar Contract: `reports/lxy_136_phase_build/p1a_grammar_contract/`.
- P1-B Fixture System: present in the current LXY 1-3-6 phase-build baseline and prior fixture gate.
- P1-C Grammar Parser MVP: `scripts/cyber_guqin_grammar_parser.py`, with recent commit `feat(lxy): implement phase1 grammar parser mvp`.
- P2-A Visual Component Design: `CG_LXY_P2A_visual_component_design.v0.1.md` and companion P2A contract files.
- P2-B Component Matcher MVP: current HEAD commit `feat(lxy): implement phase2 component matcher mvp` and P2 runtime files.

## 3. Core Concepts

### Component

A `Component` is one registry-backed visual unit, such as a literal label component. P2B accepts one suspected component crop and returns top-k component candidates.

Allowed component-level evidence:

- `component_id`;
- literal `label`;
- visual similarity evidence;
- confidence bucket;
- registry source trace;
- unknown component state.

Forbidden component-level promotion:

- assigning a final semantic role;
- constructing a notation-unit reading;
- constructing phrase text;
- creating score or Dapu authority.

### NotationUnit

A `NotationUnit` is a whole visual crop that may contain one or more components arranged spatially. It is not a phrase and not a grammar parse.

Example, as literal visual labels only:

```text
NotationUnit = 大 + 九 + 绰 + 勾 + 六
```

The example above means only "these visible component labels may be present in one unit." It does not say what the unit reads as.

### VisualSlot

A `VisualSlot` is a position or attachment bucket inside one notation-unit crop. It is not a P1/P3 semantic slot.

P2C visual slot examples:

- `LEFT_UPPER`
- `RIGHT_UPPER`
- `MIDDLE`
- `LOWER_OUTER`
- `LOWER_INNER`
- `ATTACHED_MARK`

Semantic slot examples that P2C must not assign:

- `LEFT_FINGER`
- `HUI_POSITION`
- `PRE_SOUND_MOTION`
- `RIGHT_HAND_ACTION`
- `STRING_NUMBER`

Strict separation:

| Visible label | P2C may say | P2C must not say |
|---|---|---|
| `大` | visual component candidate label `大` in a visual slot | final left-finger role |
| `九` | visual component candidate label `九` in a visual slot | final hui or string role |
| `绰` | visual component candidate label `绰` in a visual slot | final motion reading with target |
| `勾` | visual component candidate label `勾` in a visual slot | final attack reading |
| `六` | visual component candidate label `六` in a visual slot | final string role |

P3 decides legal grammar parse from the P2C candidate lattice.

## 4. NotationUnitAnalyzer

`NotationUnitAnalyzer` is a future implementation boundary. It decomposes a whole notation-unit crop without producing grammar output.

Input:

```json
{
  "notation_unit_id": "unit_001",
  "crop_image_reference": {
    "path_or_uri": "path/to/unit_crop.png",
    "reference_type": "notation_unit_crop"
  },
  "analyzer_options": {
    "top_k_regions": 8,
    "top_k_components_per_region": 5
  }
}
```

Steps:

1. Detect visual regions.
   - Estimate ink bounding boxes, connected components, projection cuts, nested regions, and attached marks.
   - Preserve multiple hypotheses when segmentation is uncertain.

2. Assign slot candidates.
   - Map region hypotheses to visual slot candidates such as `LEFT_UPPER` or `LOWER_INNER`.
   - Allow top-k slot hypotheses for one region.
   - Record `AMBIGUOUS_SLOT` when geometry supports more than one slot.

3. Call P2B ComponentMatcher.
   - Crop each region hypothesis.
   - Call P2B on each component crop hypothesis.
   - Keep P2B output as component candidates only.
   - Do not pass phrase, score context, or P1 grammar parse output into P2B.

4. Construct slot lattice.
   - Combine slot candidates, P2B component candidates, region confidence, and spatial relations.
   - Keep unresolved slots explicit.
   - Return `VisualSlotLattice`.

Output:

```text
VisualSlotLattice
```

Explicit non-calls:

- no `GrammarParser.parse()`;
- no phrase reconstruction;
- no context inheritance;
- no "carry previous unit" handling;
- no sample or training export.

## 5. Slot Model

P2C uses visual slot types only.

| Slot type | Visual meaning | Semantic boundary |
|---|---|---|
| `LEFT_UPPER` | upper-left visible region in the unit crop | not automatically left finger |
| `RIGHT_UPPER` | upper-right visible region in the unit crop | not automatically hui, motion, or action |
| `MIDDLE` | central visible region or host region | not automatically host semantic role |
| `LOWER_OUTER` | lower exterior visible region | not automatically action or string |
| `LOWER_INNER` | lower nested or embedded visible region | not automatically string |
| `ATTACHED_MARK` | small attached visual mark tied to a host region | not automatically pre/post motion or state marker |

Required unresolved states:

- `UNKNOWN_SLOT`: a region exists, but no visual slot assignment is safe.
- `UNKNOWN_COMPONENT`: P2B cannot return a registry-backed component candidate.
- `AMBIGUOUS_SLOT`: the same region has multiple plausible visual slot assignments.
- `MISSING_COMPONENT`: a slot rule expects visual evidence, but the crop has no supported component region.
- `EXTRA_INK`: ink exists outside supported region or slot hypotheses.

P2C must not fill missing visual evidence by guessing.

## 6. VisualSlotLattice Shape

Minimum shape:

```json
{
  "notation_unit_id": "unit_001",
  "slots": [
    {
      "slot_id": "slot_001",
      "slot_type": "LEFT_UPPER",
      "slot_status": "PRESENT",
      "region_candidate_ids": ["region_001"],
      "candidates": [
        {
          "component_id": "COMP-091",
          "visual_score": 0.82,
          "confidence": {
            "value": 0.82,
            "bucket": "high",
            "score_type": "HEURISTIC_VISUAL_CONFIDENCE",
            "calibrated_probability": false
          },
          "candidate_rank": 0,
          "source_region_id": "region_001"
        }
      ]
    }
  ],
  "unresolved_slots": [],
  "authority_flags": {
    "NOT_SCORE_AUTHORITY": true,
    "NOT_DAPU_IR_AUTHORITY": true
  }
}
```

`visual_score` is a ranking signal only. It is not correctness probability.

## 7. Spatial Relations

P2C must represent spatial structure because jianzipu notation units are not linear text.

Required relation types:

- `above`
- `below`
- `left_of`
- `right_of`
- `inside`
- `attached`

Spatial relations are visual evidence for grouping. They are not semantic readings.

Examples of allowed relation statements:

```text
region_001 above region_003
region_004 inside region_002
region_005 attached region_002
```

Examples of forbidden promotion:

```text
region_001 above region_003, therefore region_001 is a fixed semantic role
region_004 inside region_002, therefore the whole unit has a final reading
```

## 8. P2B Interface

P2B remains the single-component matcher:

```text
component crop hypothesis
-> ComponentMatcher.match(...)
-> ComponentCandidateSet
```

P2C wraps P2B outputs into notation-unit slots:

```text
whole notation unit crop
-> region hypotheses
-> component crop hypotheses
-> P2B ComponentMatcher
-> slot/component lattice
```

Interface rules:

- P2C must not modify P2B matcher logic.
- P2C must not require P2B to understand notation-unit layout.
- P2C may pass `crop_id`, `top_k`, and crop image path to P2B.
- P2C must not pass phrase id, gold answer, human correction, or score context to P2B.
- P2C may record P2B `UNKNOWN_COMPONENT` as a slot unresolved state.

## 9. P3 Interface

P2C produces a visual handoff projection:

```json
{
  "slot_candidates": [],
  "component_candidates": [],
  "spatial_relations": [],
  "confidence": {
    "score_type": "HEURISTIC_VISUAL_CONFIDENCE",
    "calibrated_probability": false
  }
}
```

P3 may then decide:

- which component candidate belongs to which grammar token;
- whether a visible numeric component is hui, string, count, or unresolved;
- whether a visible motion label attaches before or after another unit;
- whether a candidate parse is valid, incomplete, ambiguous, or rejected.

P2C itself must not make those decisions.

## 10. P2C Fixture Contract Design

P2C implementation should later add fixtures for these cases:

| Fixture id | Case | Required assertion |
|---|---|---|
| `P2C-FIX-001` | single component unit | one region can map to one visual slot and one top-k P2B candidate set |
| `P2C-FIX-002` | two component unit | two region hypotheses preserve spatial relation and independent component candidates |
| `P2C-FIX-003` | multi component notation unit | three or more regions can form one lattice without linearizing into a reading |
| `P2C-FIX-004` | ambiguous visual slot | one region may carry multiple slot candidates and `AMBIGUOUS_SLOT` |
| `P2C-FIX-005` | missing component | expected region absence records `MISSING_COMPONENT`, not a fabricated candidate |
| `P2C-FIX-006` | extra ink | unsupported ink records `EXTRA_INK` without forcing registry identity |
| `P2C-FIX-007` | component order variation | spatial graph preserves non-linear order and avoids sequence-only assumptions |
| `P2C-FIX-008` | same component different slot | same component label can appear in different visual slots without semantic role collapse |

Fixture assertions must be oracle-free. They may assert contract shape, slot taxonomy, unknown behavior, and relation graph integrity. They must not assert LXY phrase facts or final readings.

## 11. Extensibility Policy

Adding a new notation unit type must require only:

1. a new P2C fixture; and
2. a new visual slot rule.

It must not require:

- changing P2B matcher;
- changing P3 parser;
- adding phrase-specific branches;
- adding goldset or answer-data dependencies;
- adding ML training data.

## 12. Validation Contract

This design is ready only if these checks pass:

- JSON schema PASS;
- slot taxonomy PASS;
- component/slot boundary PASS;
- semantic role separation PASS;
- no concrete phrase reading PASS;
- no oracle leakage PASS.

Final readiness:

```json
{
  "ready_for_P2C_implementation_design": true,
  "ready_for_LXY_phrase_reading": false,
  "ready_for_training_model": false
}
```
