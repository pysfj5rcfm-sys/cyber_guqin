# CG-LXY P1/P2 Handoff To P3 v0.1

Task ID: `CG-LXY-136-P1-P2-HANDOFF-TO-P3-v0.1`

Status labels:

- P1_GRAMMAR_PARSER_HANDOFF
- P2_VISUAL_COMPONENT_HANDOFF
- P3_VISUAL_GRAMMAR_FUSION_READY
- COMPONENT_LEVEL_REVIEW_ONLY
- CROSS_VALIDATION_REQUIRED
- GPT_TRANSCRIPTION_DRAFT
- NEEDS_HUMAN_REVIEW
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA

## 1. Scope Boundary

This handoff summarizes the current P1 and P2 state after the CG-LXY-136 reality checks. It is a development handoff, not a phrase-reading report.

Allowed scope:

```text
P1 grammar parser capability
P2G visual decomposition capability
P2B component matcher capability
P2G -> P2B component candidate lattice bridge
component-level visual review evidence
next-stage engineering recommendations
```

Forbidden scope:

```text
phrase reading
surface reading as authority
continuation / inherited phrase relation
Dapu IR
score fact
sample ingest
ML training
piece title / phrase oracle
```

## 2. Current Pipeline Shape

Current intended chain:

```text
notation_unit_crop
  -> P2G Visual Decomposition
  -> segmentation_tree_candidates / component_region_candidates
  -> P2B Component Matcher
  -> component_candidate_lattice
  -> P3 Visual Grammar Fusion
  -> P1 Grammar Parser posterior validation
```

Critical separation:

```text
P2G score = visual decomposition score
P2B score = component visual similarity score
P3/P1 score = grammar validity score
```

P1 grammar validity may be used by P3 as posterior evidence. It must not be used by P2G as the primary reason to cut a notation unit in a particular way.

## 3. P1 Handoff

P1-C is implemented as an executable grammar parser for caller-supplied component token sequences.

Runtime files:

```text
scripts/cyber_guqin_grammar_parser.py
scripts/run_cyber_guqin_grammar_fixtures.py
references/qxby_component_atlas/p1_grammar_runtime_contract.v0.1.json
references/qxby_component_atlas/p1_generation_safe_guards.v0.1.json
```

P1 provides:

```text
component id / alias normalization
grammar production validation
structured parse candidates
deterministic grammar ranking
guard evaluation
unresolved / invalid status reporting
authority flags
```

P1 does not provide:

```text
image segmentation
component visual recognition
notation-unit crop detection
phrase reconstruction
implicit backward context scan
score-event authority
Dapu IR authority
```

P3 should call P1 only after P2 has produced component candidate lattices. P3 should pass explicit context if context is intended; P1 must not infer context from prior calls.

## 4. P2 Handoff

### 4.1 D1 Component Reference Layer

Current D1/P2B visual runtime index is rebuilt from registry authority.

Current index summary:

```text
component_index_count: 186
image_reference_count: 186
source_image_missing_count: 0
```

The following auxiliary components are now matchable:

```text
COMP-081 一
COMP-082 二
COMP-083 三
COMP-084 四
COMP-085 五
COMP-086 六
COMP-087 七
COMP-091 大指
COMP-092 食指
COMP-093 中指
COMP-094 名指
COMP-095 跪指
```

Numeric `一` to `七` are currently provisional equivalence references for the one-to-seven validation phase. The following are explicitly not covered yet:

```text
八
九
十
十一
十二
十三
```

P3 must treat those uncovered numeric gaps as component reference gaps, not as grammar failures.

### 4.2 P2G Visual Decomposition

Implemented runtime:

```text
scripts/visual_decomposition_runtime.py
references/qxby_component_atlas/visual_structure_patterns.v0.1.json
tests/test_visual_decomposition_runtime.py
```

P2G outputs visual-only structures:

```text
layout_candidates
segmentation_tree_candidates
component_region_candidates
quality_metrics
failure_flags
review_packet
```

P2G output must not contain component ids, semantic slots, grammar rules, phrase readings, score facts, or Dapu IR.

Known useful behavior:

```text
red human-review marks are ignored as non-ink
fragmented ink can be grouped before component matching
visual roles remain visual roles, not semantic slots
unknown structures produce human-review packets
```

Known current blocker:

```text
P2G can still over-merge a nested notation unit into one dominant region.
The 2026-07-09 reality-check image should be split into:
  upper_region
  lower_outer_enclosure
  lower_inner_region
but current automatic decomposition can collapse it too early.
```

Component-level review for that image indicates the intended component targets are:

```text
upper_region            -> COMP-705 散
lower_outer_enclosure   -> COMP-116 挑
lower_inner_region      -> COMP-087 七
```

This is component-level visual review only. It is not a phrase reading and not grammar authority.

### 4.3 P2G -> P2B Bridge

Implemented runtime:

```text
scripts/p2g_component_lattice_runtime.py
tests/test_p2g_component_lattice_runtime.py
```

Bridge output contract:

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

The bridge is downstream of P2G. It must not alter segmentation using component or grammar success.

### 4.4 P2B Component Matcher

Implemented runtime:

```text
scripts/component_matcher_runtime.py
scripts/component_visual_index.py
scripts/component_candidate_lattice.py
scripts/component_ranking_audit.py
```

P2B returns Top-K component candidates. It does not force a unique answer.

Current reality-check findings:

```text
First image, five reviewed visual parts:
  COMP-091 大指  HAS_COMPONENT_ID             MISS
  九             NO_INDEPENDENT_COMPONENT_ID  ATLAS_GAP
  COMP-087 七    HAS_COMPONENT_ID             MISS
  COMP-418 注    PASS_TOP1
  COMP-116 挑    PASS_TOP3

Second image, manually reviewed three-block structure:
  segmentation blocker: P2G over-merge
  lower_outer_enclosure can recall COMP-116 挑 when correctly cropped
  upper_region and lower_inner_region still need better automatic masking/ranking validation
```

Do not tune P2B ranking weights from one image alone. More component-level, cross-image visual fixtures are required before changing ranking policy.

## 5. Handoff Contract To P3

P3 should consume:

```text
notation_unit_id
segmentation_candidate_id
region_id
node_id
visual_role
bbox
Top-K component candidates per region
visual_score
component_similarity_score
failure_flags
authority_flags
```

P3 may produce:

```text
grammar_candidate structures
grammar validity / invalidity
ambiguity-preserving candidate ranking
review packets for unresolved visual/component/grammar conflicts
```

P3 must not produce as authority in this phase:

```text
final phrase reading
score fact
Dapu IR
sample ingest candidate
ML training label
```

P3 failure typing should distinguish:

```text
SEGMENTATION_FAILURE
COMPONENT_RECALL_GAP
COMPONENT_ATLAS_GAP
GRAMMAR_FAILURE
AMBIGUOUS_BUT_VALID
NEEDS_HUMAN_REVIEW
```

Suggested P3 parser handoff shape:

```json
{
  "notation_unit_id": "",
  "segmentation_candidate_id": "",
  "component_candidate_lattice": {},
  "grammar_candidates": [],
  "fusion_scores": {
    "visual_confidence": "",
    "component_confidence": "",
    "grammar_confidence": ""
  },
  "failure_analysis": {},
  "authority_flags": {
    "GPT_TRANSCRIPTION_DRAFT": true,
    "NEEDS_HUMAN_REVIEW": true,
    "NOT_DAPU_IR_AUTHORITY": true,
    "NOT_SCORE_EVENT_AUTHORITY": true
  }
}
```

## 6. Next-Stage Recommendations

Recommended next tasks, in order:

1. Build a P3 Visual Grammar Fusion skeleton that accepts P2G/P2B lattices and calls P1 as posterior grammar validation only.
2. Add a visual-only component-level fixture for the three-block `散 / 七 / 挑` image: bbox, visual_role, reviewed_component_id, and no phrase-reading fields.
3. Improve P2G nested-region splitting for `ENCLOSURE_WITH_INNER`: outer mask, inner mask, upper attached band, and over-merge detection.
4. Add cross-validation images before changing P2B ranking. Each fixture may contain component-level visual review labels, but must not contain phrase reading, grammar parse, score fact, or Dapu IR.
5. Keep the current one-to-seven validation policy. Avoid test images requiring `八` to `十三` until those components are explicitly registered.
6. After segmentation stabilizes, run P2B ranking audit by component category: auxiliary numeric, auxiliary left-finger name, right-hand action, sound-position marker, and enclosure/compound-like shapes.

## 7. Readiness

```json
{
  "ready_for_P3_visual_grammar_fusion": true,
  "ready_for_P2G_block_point_attack": true,
  "ready_for_P2B_ranking_weight_change": "blocked_on_more_labeled_cross_validation",
  "ready_for_final_reading": false,
  "ready_for_score_fact": false,
  "ready_for_Dapu_IR": false,
  "ready_for_sample_ingest": false,
  "ready_for_ML_training": false
}
```

## 8. Engineering Notes

The current block point is segmentation, not grammar.

For the latest reality-check failure, the safest engineering move is:

```text
define the correct visual structure as a reviewed component-level fixture
-> teach P2G to propose that structure visually
-> rerun P2B on each region
-> let P3/P1 validate grammar only after Top-K component candidates exist
```

This keeps the project from circularly using a plausible reading to justify a visual cut.
