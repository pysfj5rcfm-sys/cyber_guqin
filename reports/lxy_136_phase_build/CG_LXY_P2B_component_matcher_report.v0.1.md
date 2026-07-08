# CG-LXY P2B Component Matcher MVP Report v0.1

Task ID: `CG-LXY-136-P2B-COMPONENT-MATCHER-MVP-v0.1`

Status labels:

- P2B_COMPONENT_MATCHER_MVP
- COMPONENT_CANDIDATE_ONLY
- VISUAL_RETRIEVAL_LAYER
- TEMPLATE_BACKEND_MVP
- MODEL_AGNOSTIC_BACKEND_INTERFACE
- UNKNOWN_COMPONENT_SUPPORTED
- UNLABELED_EVAL
- NOT_SCORE_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING

## 1. Scope

P2-B implements a single-crop visual component candidate layer:

```text
single component crop image
-> ComponentMatcher
-> top-k ComponentCandidateSet
```

It does not read phrases, lines, score context, Dapu IR, score facts, samples, recordings, model training data, or goldset/oracle answers.

## 2. Implemented Files

- `scripts/component_matcher.py`
  - `ComponentMatcher`
  - `ComponentImageIndex`
  - `TemplateMatcherBackend`
  - `EmbeddingMatcherBackend` interface slot
  - `VisionModelMatcherBackend` interface slot
- `scripts/build_component_visual_index.py`
  - builds `component_visual_index.v0.1.json` from registry image references
- `scripts/run_component_matcher_eval.py`
  - evaluates crop directories without fabricating accuracy when labels are absent
- `tests/test_component_matcher.py`
  - covers index loading, image references, deterministic matching, top-k ordering, unknown policy, empty/invalid inputs, and registry extension
- `references/qxby_component_atlas/component_visual_index.v0.1.json`
  - registry-backed visual index
- `reports/lxy_136_phase_build/CG_LXY_P2B_eval_result.v0.1.json`
  - unlabeled smoke eval over permitted source images

## 3. Component Visual Index

Index source:

```text
references/qxby_component_atlas/component_registry.reindexed.v0.2.json
sources/qxby_component_atlas/images/
```

Index summary:

```text
component_index_count: 186
image_reference_count: 174
source_image_missing_count: 0
auxiliary_component_count: 12
```

The 174 full-atlas registry components have repo source PNG references. The 12 auxiliary components are indexable registry identities, but are marked `matchable=false` when no repo source image exists. No source image was copied or modified.

## 4. Matcher Contract

`ComponentMatcher.match(image_crop, top_k=5)` returns:

```text
crop_id
status: MATCHED | AMBIGUOUS | UNKNOWN_COMPONENT
candidates[]
authority_flags
matcher_trace
```

Each candidate contains:

```text
component_id
label
category
rank
confidence_level: HIGH | MEDIUM | LOW
evidence.visual_similarity
evidence.source_image_reference
evidence.notes
```

Confidence is a non-probabilistic bucket. Raw visual similarity is reported only as heuristic evidence and is marked `calibrated_probability=false`.

## 5. Backend Boundary

The MVP binds only the stdlib template backend:

```text
TemplateMatcherBackend
```

It also defines replaceable adapter slots:

```text
EmbeddingMatcherBackend
VisionModelMatcherBackend
```

Those slots intentionally do not bind models, download dependencies, train models, or expose model-specific output to P3.

## 6. Unknown Strategy

Unknown is supported. If the top candidate does not meet `unknown_threshold`, the matcher returns:

```text
status: UNKNOWN_COMPONENT
candidates: []
failure_classification: UNKNOWN_THRESHOLD_ERROR
```

Empty and invalid crop images also return `UNKNOWN_COMPONENT` with explicit input warnings instead of forcing a component choice.

## 7. Evaluation

Eval command used the permitted source image directory as an unlabeled smoke set:

```text
python3 scripts/run_component_matcher_eval.py sources/qxby_component_atlas/images --index references/qxby_component_atlas/component_visual_index.v0.1.json --output reports/lxy_136_phase_build/CG_LXY_P2B_eval_result.v0.1.json
```

Eval summary:

```text
evaluation_status: UNLABELED_EVAL
total_crops: 174
matched: 174
ambiguous: 0
unknown: 0
top1_accuracy: null
topk_recall: null
```

No accuracy or recall was computed because no explicit human label file was supplied.

## 8. Validation Evidence

Executed validation:

```text
python3 -m unittest tests.test_component_matcher
8 tests OK

PYTHONPYCACHEPREFIX=/tmp/cg_lxy_p2b_pycache python3 -m compileall scripts/component_matcher.py scripts/build_component_visual_index.py scripts/run_component_matcher_eval.py tests/test_component_matcher.py
compile OK

python3 -m unittest
0 tests discovered, OK
```

Direct verification summary:

```text
component_index_count: 186
image_reference_count: 174
missing_image_path_count: 0
hash_mismatch_count: 0
determinism_status: true
unknown_policy_status: UNKNOWN_COMPONENT
extension_test_status: PASS
```

## 9. Readiness

```text
ready_for_P2C_visual_lattice_design: true
ready_for_LXY_phrase_reading: false
ready_for_training_model: false
```
