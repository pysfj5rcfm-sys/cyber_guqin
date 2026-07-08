# CG-LXY P2A Visual Component Candidate Design v0.1

Task ID: `CG-LXY-136-P2A-VISUAL-COMPONENT-CANDIDATE-DESIGN-v0.1`

Status labels:

- P2A_VISUAL_COMPONENT_CANDIDATE_DESIGN
- REFERENCE_COMPONENT_ATLAS_GUIDED
- COMPONENT_CANDIDATE_ONLY
- TOP_K_LATTICE_DESIGN
- NEEDS_HUMAN_REVIEW
- NOT_REPO_CONTRACT
- NOT_CANON_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA
- NOT_RENDER_OUTPUT

## 1. Scope

P2A designs the Visual Component Candidate Layer that sits after image cropping and before grammar parsing.

```text
image crop
-> VisualComponentMatcher
-> component candidates
-> top-k component lattice
```

P2A does not read a whole score line, reconstruct a phrase, call P1-C grammar parsing, create Dapu IR, create score facts, train a visual model, or update component registry assets. It only defines the contract and review model for a future P2B implementation design.

## 2. Confirmed Baseline

Preflight evidence:

```text
current_branch: main
current_head: 51598da04434749630c135548b4be854d948dac3
recent_head_subject: feat(lxy): implement phase1 grammar parser mvp
git_status_before_p2a: clean
```

P1-C exists and is explicitly bounded: it starts from caller-provided component tokens and does not detect glyphs, segment lines, build a lattice, reconstruct phrases, infer historical context, or create score authority. P2A therefore fills only the missing visual component candidate layer.

## 3. Authority Sources

The component registry is the only component authority for registry-backed candidates:

```text
references/qxby_component_atlas/component_registry.reindexed.v0.2.json
references/qxby_component_atlas/component_legacy_alias_map.reindexed.v0.2.json
sources/qxby_component_atlas/images/
```

Observed registry shape:

- `components`: 174 full-atlas primary v0.2 components.
- `auxiliary_components`: 12 registry auxiliary components for numerals and left-finger names.
- `total_primary_components`: 186.
- `sources/qxby_component_atlas/images/`: 174 source PNGs for full-atlas components.
- auxiliary numerals and left-finger names are registry-backed, but not all have a copied repo source image path.

P2A may use alias normalization as identity support, but candidate output must use the primary v0.2 component id.

## 4. VisualComponentMatcher

`VisualComponentMatcher` is a model-agnostic adapter boundary. It accepts one crop and returns a registry-backed top-k component lattice plus coverage ledger.

### Input

`SingleComponentCrop`:

- `crop_id`
- `crop_image_reference`
- optional `bbox_in_parent_image`
- optional `preprocessing_trace`
- optional `ocr_hint`
- optional `human_feedback_hint`
- optional `matcher_options`

The crop is treated as one component crop or a suspected component sub-region. If the crop appears to contain multiple components or a whole notation unit, P2A must mark `crop_scope_status=REJECTED_NOT_SINGLE_COMPONENT_SCOPE` or `NEEDS_COMPONENT_SEGMENTATION` instead of silently reading it.

### Output

`ComponentCandidateLattice`:

- `crop_id`
- `crop_scope_status`
- `top_k`
- `component_candidates`
- `unknown_component_state`
- `coverage_ledger`
- `matcher_trace`
- `authority_flags`

Each registry-backed `ComponentCandidate` contains:

- `component_id_v0_2`
- `label`
- `category`
- `confidence`
- `visual_match_reason`
- `source_image_reference`
- `candidate_rank`

`component_candidates` may contain multiple candidates for one crop. It may also be empty when the crop is unknown or insufficiently supported.

## 5. Candidate Proposal Channels

P2A does not assume a single visual algorithm. P2B may combine any of these channels, as long as each channel outputs the same evidence shape before fusion.

### A. Template Matching

Compares normalized crop shapes against registry source images or auxiliary reference evidence.

Allowed output:

- visual similarity evidence;
- source image or auxiliary registry reference;
- candidate component id from registry only.

Forbidden output:

- final reading;
- score event;
- grammar slot resolution.

### B. Visual Embedding

Looks up nearest components in an embedding index built from registry images and permitted auxiliary reference evidence.

Allowed output:

- nearest registry component ids;
- embedding distance or similarity as raw evidence;
- top-k proposal list.

Embedding distance is not a calibrated probability and must be mapped through the shared confidence model.

### C. OCR-Assisted Candidate Proposal

OCR may provide only a hint. It cannot be the final answer.

Valid uses:

- propose registry labels or aliases to inspect;
- break ties when visual evidence is already present;
- mark text-shape disagreement for review.

Invalid uses:

- emitting OCR text directly as `label`;
- creating a component id from OCR text;
- overriding visual conflict;
- producing phrase text.

### D. Human Feedback Correction

Human feedback may suppress a known bad visual candidate or propose a registry-backed candidate for review.

It remains review evidence. It is not canon authority, not Dapu IR authority, and not model training data in P2A. Any future learning deposit update requires a separate authorized Learning Mode task.

## 6. Candidate Fusion

All proposal channels must first normalize to `ComponentCandidateEvidence`:

```text
crop_id
component_id_v0_2
label
category
evidence_channel
raw_score
raw_score_type
source_image_reference
visual_match_reason
evidence_quality_flags
```

Fusion then:

1. removes any proposal whose `component_id_v0_2` is not present in the registry;
2. merges evidence for the same registry component;
3. assigns a non-probabilistic confidence bucket;
4. applies low-confidence and conflict penalties;
5. sorts into deterministic top-k order;
6. records unresolved state when evidence is missing, conflicting, or below threshold.

## 7. Top-K Lattice

Sorting order:

1. higher confidence bucket;
2. higher visual confidence value inside the same bucket;
3. more independent visual channels agreeing;
4. direct registry source image match before OCR-only hint;
5. fewer evidence quality warnings;
6. stable `component_id_v0_2` tie-break.

`candidate_rank` is assigned after sorting and must be unique within a crop. The rank is an ordering statement only.

The lattice is component-only. It is not a parser lattice and must not contain slot bindings, unit readings, phrase readings, score events, or Dapu IR nodes.

## 8. Unknown And Low Confidence

Unknown is not represented by a fake component id. If no registry-backed component passes the minimum evidence gate:

```json
{
  "component_candidates": [],
  "unknown_component_state": {
    "status": "UNKNOWN_COMPONENT",
    "unresolved_reason": "no registry-backed candidate passed minimum visual evidence gate",
    "needs_human_review": true
  }
}
```

Low confidence is allowed and must be explicit. A low-confidence registry candidate may appear in top-k, but it must carry:

- `confidence.bucket=low` or `very_low`;
- `confidence.calibrated_probability=false`;
- a concrete review reason;
- `needs_human_review=true`.

## 9. Coverage Ledger

Every crop output must include a coverage ledger:

```json
{
  "crop_id": "crop_001",
  "matched_components": ["COMP-103", "COMP-116"],
  "unresolved_reason": null,
  "needs_human_review": true
}
```

For unknown:

```json
{
  "crop_id": "crop_002",
  "matched_components": [],
  "unresolved_reason": "UNKNOWN_COMPONENT",
  "needs_human_review": true
}
```

The ledger is crop coverage only. Line coverage, notation-unit coverage, and phrase coverage are later phases.

## 10. P1-C Handoff Boundary

P2A output can later be transformed into P3/P1-C token candidates only after a separate P3 integration design. P2A itself does not call:

```text
GrammarParser.parse()
load_default_parser()
scripts/run_cyber_guqin_grammar_fixtures.py
```

P2A output may include the fields needed by a future tokenization adapter:

- `component_id_v0_2`
- `label`
- `category`
- `candidate_rank`
- `confidence`
- `source_image_reference`

It must not include parser slots or surface readings.

## 11. Explicit Non-Outputs

P2A must not output:

- phrase reading;
- continuous reading;
- notation-unit reading;
- score event;
- Dapu IR;
- parser accepted candidate;
- grammar slot binding;
- line-level context;
- phrase boundary;
- sample ingest row;
- ML training example;
- render artifact.

## 12. Readiness

```json
{
  "ready_for_P2B_implementation_design": true,
  "ready_for_visual_model_training": false,
  "ready_for_LXY_phrase_reading": false
}
```

