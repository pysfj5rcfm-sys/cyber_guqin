# CG-LXY P2A Visual Confidence Model v0.1

Task ID: `CG-LXY-136-P2A-VISUAL-COMPONENT-CANDIDATE-DESIGN-v0.1`

Status labels:

- P2A_VISUAL_CONFIDENCE_MODEL
- HEURISTIC_VISUAL_CONFIDENCE
- CALIBRATED_PROBABILITY_FALSE
- COMPONENT_CANDIDATE_ONLY
- NEEDS_HUMAN_REVIEW
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_ML_TRAINING_DATA

## 1. Purpose

P2A confidence is a visual ranking signal for component candidates. It is not a probability, not correctness, not a parser score, and not score authority.

Required candidate confidence shape:

```json
{
  "value": 0.82,
  "bucket": "high",
  "score_type": "HEURISTIC_VISUAL_CONFIDENCE",
  "calibrated_probability": false
}
```

## 2. Confidence Inputs

The confidence model may combine multiple evidence families:

| Evidence family | Example signal | Allowed role |
|---|---|---|
| Template match | contour / stroke overlap with registry image | primary visual evidence |
| Visual embedding | nearest-neighbor distance to registry exemplar | primary visual evidence |
| Crop quality | blur, threshold loss, clipped strokes, empty ink | penalty or review trigger |
| Channel agreement | template and embedding propose the same component | confidence support |
| OCR hint | OCR text matches registry label or alias | hint only |
| Human feedback | review correction suppresses or proposes candidate | review evidence only |

No single channel is required by P2A. Every channel must report raw evidence and then normalize through the shared contract.

## 3. Bucket Model

Buckets are ordinal review categories:

| Bucket | Meaning | Required handling |
|---|---|---|
| `high` | strong visual agreement and no major conflict | may rank first, still reviewable |
| `medium` | usable visual evidence but one uncertainty remains | keep in top-k, reviewable |
| `low` | weak or partial match | keep only if useful for review |
| `very_low` | barely supported registry-backed candidate | normally below acceptance threshold |

Thresholds are implementation parameters for P2B. P2A locks only the semantics:

```text
confidence.value is a normalized visual rank score.
confidence.value is not a calibrated probability.
confidence.bucket controls review policy.
```

## 4. OCR Policy

OCR may affect candidate search but cannot produce final component identity by itself.

Valid OCR contributions:

- add `ocr_assisted_candidate_proposal` to `matcher_trace.channels_used`;
- propose labels for registry lookup;
- add a small tie-break support only when visual evidence already exists;
- add a conflict warning if OCR text disagrees with visual evidence.

Invalid OCR contributions:

- copying OCR text into `label` without registry lookup;
- inventing `component_id_v0_2`;
- treating OCR confidence as component confidence;
- producing phrase text or parser slots.

## 5. Fusion Score Sketch

P2B may choose exact weights later, but the fusion model should be monotonic and explainable:

```text
visual_confidence_value
= visual_similarity_support
+ independent_channel_agreement
+ registry_reference_quality
+ optional_hint_support
- crop_quality_penalty
- visual_conflict_penalty
- source_reference_gap_penalty
```

Constraints:

- final value must be clamped to `[0.0, 1.0]`;
- bucket must be derived after penalties;
- `calibrated_probability=false` must remain true for all candidates;
- candidate rank must be deterministic even when values tie.

## 6. Unknown And Review Policy

Unknown state is required when no registry-backed component survives validation:

```text
UNKNOWN_COMPONENT
INSUFFICIENT_VISUAL_EVIDENCE
CONFLICTING_VISUAL_EVIDENCE
CROP_NOT_SINGLE_COMPONENT
SOURCE_REFERENCE_GAP
```

Unknown is not a candidate id. It lives in `unknown_component_state` and `coverage_ledger.unresolved_reason`.

Human review is required for every P2A output because the layer is only candidate generation. Strong confidence reduces review burden; it does not create authority.

## 7. Calibration Boundary

P2A forbids probability language such as:

- "82% correct";
- "probability of 勾 is 0.82";
- "model certainty";
- "final answer".

Allowed language:

- "rank score";
- "visual support";
- "candidate confidence bucket";
- "review priority";
- "evidence agreement".

## 8. P1-C Compatibility

P1-C uses `HEURISTIC_GRAMMAR_SCORE` for parser ranking. P2A uses `HEURISTIC_VISUAL_CONFIDENCE` for visual ranking. These are different score types and must not be merged until a future P3 lattice design defines an integration rule.

P2A confidence must not be written into parser slots, surface readings, score events, or Dapu IR.

