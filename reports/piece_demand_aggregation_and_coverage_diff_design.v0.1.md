# Piece Demand Aggregation and Coverage Diff Design v0.1

状态：设计稿。Aggregation 不属于 `guqin-dapu-parser`。

## 1. Boundary

多曲目 starter analysis 是 workflow/diff-layer 特例：

```text
single piece -> Dapu IR -> per-piece demand extraction
multiple per-piece demand sets -> coverage diff engine
```

`guqin-dapu-parser` 只处理一首曲子的 tokens/components/events/validation。它不接受 multi-piece corpus 输入，不负责跨曲统计，也不决定 Sanman collection priority。

## 2. Inputs

Allowed inputs:

- one or more independently parsed single-piece Dapu IR outputs
- `00_global/gesture_templates.csv`
- `00_global/gesture_components.csv`
- `00_global/sample_selection_policy.yaml`
- existing Sanman starter inventory, initially empty or mock-only
- Baiya/XWC baseline as comparison/reference only
- human-approved collection constraints

Disallowed inputs as authority:

- Baiya sample data as Sanman style data
- R2 CSV/YAML as canonical when latest JSON exists
- recording plans as score authority
- Downloads / Blob / restore zip / old exports

## 3. Per-Piece Demand Extraction

For each single-piece output, derive a demand row per event or component group:

| Concept | Field source |
| --- | --- |
| event identity | `event_id` / mapped `score_event_id` |
| phrase identity | `phrase_id` |
| sound class | `primary_sound_type` |
| gesture family | `gesture_family` |
| components | `components`, `component_name`, `component_category` |
| string/hui | `string_no`, `hui`, `hui_target` |
| pre/post/vibrato | `notation_pre_action`, `notation_vibrato`, post-motion components |
| context | `context_dependency`, `requires_context_sample`, `needs_context_take` |
| tail | `needs_long_tail`, `tail_policy` |
| confidence | `certainty` / `source_confidence` |

If any field is absent, classify demand as `structure_validation_required` or `needs_human_decision` rather than inventing data.

## 4. Coverage Diff Statuses

Design statuses:

- `already_covered`: Sanman inventory has an approved matching item.
- `missing`: no Sanman coverage.
- `must_record_atomic`: clean atomic collection is needed.
- `must_record_context`: context sample is needed and must not be used as atomic.
- `must_record_long_tail`: full-tail / natural-decay behavior must be captured.
- `structure_validation_required`: pressed-sound or complex technique structure is insufficient.
- `do_not_use_as_atomic`: context-only or diagnostic item.
- `needs_human_decision`: canon/parser/realization ambiguity.
- `baiya_comparison_only`: available only as Baiya reference.
- `qinist_must_record`: Sanman must record because Baiya cannot substitute.

These are proposed diff-layer statuses, not existing runtime enums. They should remain report/draft-schema only until user approval.

## 5. Diff Logic Sketch

1. Validate each piece independently against Dapu/canon fields.
2. Expand event demand into atomic/component/context/tail dimensions.
3. Normalize aliases:
   - `sound_type` -> `primary_sound_type`
   - `string` -> `string_no`
   - `hui_position` -> `hui`
4. Match against Sanman inventory only.
5. Mark Baiya matches as `baiya_comparison_only`, never `already_covered`.
6. Promote to `must_record_atomic/context/long_tail` only after structure validation passes.
7. Emit `needs_human_decision` for ambiguous phrase semantics or score/realization boundary risk.

## 6. Output Shape

The diff engine should produce a report-first table:

```text
piece_id
event_id
phrase_id
primary_sound_type
gesture_family
gesture_id
component_summary
coverage_status
reason
sanman_inventory_ref
baiya_reference_ref
requires_human_confirmation
```

The field `coverage_status` is `proposed_extension_field` in the matrix and must not become production behavior without approval.

