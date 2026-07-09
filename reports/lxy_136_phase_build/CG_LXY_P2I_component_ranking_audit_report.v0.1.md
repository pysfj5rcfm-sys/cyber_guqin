# CG-LXY P2I Component Ranking Audit Report v0.1

Task ID: `CG-LXY-136-P2I-COMPONENT-RANKING-AUDIT-v0.1`

Status labels:

- P2B_COMPONENT_RANKING_AUDIT
- VISUAL_COMPONENT_EVAL_ONLY
- CROSS_VALIDATION_REQUIRED
- NOT_PHRASE_READING_AUTHORITY
- NOT_GRAMMAR_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NEEDS_HUMAN_REVIEW

## Scope

This audit evaluates component-level P2B ranking after P2G visual decomposition.

Allowed evidence:

```text
P2G visual region bbox
P2G visual_role
P2B Top-K component candidates
reviewed_component_id for component-level visual eval only
atlas_status for component reference gaps
```

Forbidden evidence:

```text
phrase reading
surface reading
canonical reading
grammar parse
score fact
Dapu IR
piece title
phrase id
```

## Files

- Runtime: `scripts/component_ranking_audit.py`
- Tests: `tests/test_component_ranking_audit.py`
- Fixture: `reports/lxy_136_phase_build/CG_LXY_P2B_visual_component_eval_fixtures.v0.1.json`
- Machine result: `reports/lxy_136_phase_build/CG_LXY_P2B_visual_component_ranking_audit_result.v0.1.json`

## Fixture Boundary

The fixture is component-level only. It may say:

```text
region V004 visually corresponds to component COMP-418
```

It must not say:

```text
how the notation unit should be read
what grammar parse is valid
what phrase or score event this belongs to
```

Atlas gap statuses are explicit:

```text
HAS_COMPONENT_ID
MATCHABLE_FALSE
NO_INDEPENDENT_COMPONENT_ID
COMPONENT_ATLAS_GAP
```

`MATCHABLE_FALSE` and `NO_INDEPENDENT_COMPONENT_ID` are not counted as P2B matcher misses.

## Real Image Audit

Input:

```text
/Users/chenyulin/Desktop/截屏2026-07-08 11.48.59.png
```

P2G summary:

```text
layout: UPPER_MIDDLE_LOWER
raw_ink_region_count: 34
visual_unit_count: 5
segmentation_confidence: 0.88
```

Component-level audit summary:

```text
reviewed_region_count: 4
observed_region_count: 5
top1_hit_count: 1
top3_hit_count: 2
top5_hit_count: 2
missing_count: 2
atlas_gap_count: 1
failure_flags: P2B_RECALL_MISS, COMPONENT_ATLAS_GAP
```

Region result:

```text
upper_left_region  COMP-091 大指  HAS_COMPONENT_ID             MISS
upper_right_region 九             NO_INDEPENDENT_COMPONENT_ID  ATLAS_GAP
middle_region      COMP-087 七    HAS_COMPONENT_ID             MISS
lower_left_region  COMP-418 注    rank 1                       PASS_TOP1
lower_right_region COMP-116 挑    rank 2                       PASS_TOP3
```

Interpretation:

```text
P2G segmentation: usable for this image
P2B recall for reviewed matchable components: mixed
Current blockers: P2B recall/ranking miss for 大指 and 七; atlas gap for 九
```

## Cross Validation

Cross-validation input:

```text
/Users/chenyulin/Desktop/截屏2026-07-08 10.51.51.png
```

This second image is intentionally unlabeled for component identity. It is used only as visual sanity cross-validation.

P2G/P2B sanity output:

```text
mode: VISUAL_SANITY_ONLY
raw_ink_region_count: 24
visual_unit_count: 6
observed_region_count: 6
bridge_status: MATCHED
failure_flags: none
```

Observed regions:

```text
upper_left_region   [13, 17, 46, 54]
upper_right_region  [58, 16, 60, 46]
middle_region       [51, 58, 41, 22]
lower_left_region   [8, 94, 89, 42]
lower_outer_region  [28, 79, 87, 71]
lower_inner_region  [65, 111, 16, 16]
```

This confirms the chain runs on another notation-unit crop without relying on the first image. It does not provide component recall statistics because no component-level labels were supplied for that image.

## Decision

Do not tune P2B ranking formula from the first image alone.

Reason:

```text
After auxiliary matchability was enabled, the first image now exposes true Top-5 misses for 大指 and 七.
The cross-validation image has no component-level labels, so it cannot safely justify reranking changes.
```

Next safe work:

```text
1. Build or review more component-level visual fixtures from other notation-unit crops.
2. Separate matchable D1 gaps from true P2B misses.
3. Only then tune descriptor/ranking weights against cross-image Top-K metrics.
```

Current readiness:

```text
ready_for_P3_visual_grammar_fusion: true
ready_for_ranking_weight_change: blocked_on_more_labeled_cross_validation
ready_for_final_reading: false
ready_for_score_fact: false
```
