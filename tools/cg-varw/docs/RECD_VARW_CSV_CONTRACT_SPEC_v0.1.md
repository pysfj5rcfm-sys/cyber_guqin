# RECD / VARW CSV Contract Spec v0.1

Task: `CG-RECD_VARW_CSV_CONTRACT_LOCK_SPEC`  
Basis: `tools/cg-varw/docs/RECD_VARW_CSV_CONTRACT_AUDIT.md`  
Project instruction context: `Core_Instructions_v1.3.1.md`  
Session context: `RS_XWC_002_BAIYA_PILOT`, `QINIST_002 = Baiya`  
Spec status: contract freeze for writer patch planning only

This document freezes the v0.1 CSV contract for the six VARW R0/R1 review outputs. It is a documentation-only contract. It does not change writer behavior and does not mark any current export as production-ready.

## 1. Executive summary

The v0.1 contract defines the field names, required/optional status, enum policies, producer/consumer roles, backward-compatible aliases, RECD consumption rules, sample candidate gate safety rules, and migration notes for future writer work.

The contract addresses the audit conclusion `CONTRACT_NOT_READY` at specification level by requiring:

- stable identity fields on all primary CSVs;
- explicit raw vs split audio provenance fields;
- explicit `recording_take_no` separate from `take_id`;
- explicit score/script/gesture keys for R0 split plans and R1 sample candidate gate inputs;
- explicit R0 semantic boundary columns;
- explicit R1 human acceptance and reviewer fields;
- internal enum values instead of Chinese UI labels in contract status fields;
- a locked R1 render anchor type enum policy with active and reserved values;
- safety fields that prevent review exports from being interpreted as sample assets, render output, production data, or ML training data.

Audit findings covered at spec level:

| Finding | Spec-level resolution |
| --- | --- |
| F01 R1 lacks explicit `recording_take_no` | R1 primary and audit CSVs require `recording_take_no`; `take_id` is display-only alias. |
| F02 R1 lacks explicit `source_split_audio` | R1 primary CSVs require `source_split_audio`; `source_audio` is a migration alias only. |
| F03 R1 sample gate lacks `gesture_id` / `script_id` | R1 primary CSVs require `script_id` and `gesture_id`. |
| F04 R1 QC lacks reviewer/human acceptance fields | `segment_qc_sheet.csv` requires `human_accepted`, `reviewed_by`, and `reviewed_at`. |
| F05 Primary outputs lack session/person/piece identity | All primary CSVs require global identity fields. |
| F06 R0 split plan lacks score/gesture keys | R0 split plan requires `event_id`, `event_range`, and `gesture_id`. |
| F07 R0 split boundaries need explicit semantic columns | R0 split plan requires explicit slate, unit, clean, and tail boundary fields. |
| F08 R1 `variant` vs `realization_variant` is ambiguous | `realization_variant` is canonical; `variant` is a verified legacy alias only. |
| F09 R1 anchor type enum not locked | `render_anchor_type` enum is locked with active and reserved values. |
| F10 R1 CSVs lack `not_ml_training_data` | All R1 outputs require `not_ml_training_data=true`. |
| F11 R0 take-number fallbacks need upstream normalization guarantee | `recording_take_no` is the required stable session take number; `take_id` cannot substitute. |

## 2. Scope and non-goals

Scope:

- Define v0.1 contracts for:
  - `reviewed_slate_anchor_manifest.csv`
  - `raw_marker_review.csv`
  - `split_plan_from_raw_markers.csv`
  - `reviewed_render_anchors.csv`
  - `split_marker_review.csv`
  - `segment_qc_sheet.csv`
- Define required and optional fields.
- Define enum policies.
- Define producer and consumer roles.
- Define backward-compatible aliases for migration.
- Define RECD consumption and sample candidate gate safety rules.
- Define future writer patch and validation expectations.

Non-goals:

- No CSV writer change.
- No frontend change.
- No backend logic change.
- No split execution.
- No sample ingest.
- No render execution.
- No ML training.
- No current review output is promoted to production.

All contract CSVs remain governed by these safety defaults unless a later authorized task explicitly changes stage:

```text
review_only=true
production_grade=false
not_sample_assets=true
not_render_executed=true where applicable
not_ml_training_data=true where applicable
```

## 3. Pipeline producer / consumer diagram

```text
RECD-0 raw archive
  -> session_manifest / raw_audio_inventory / take_manifest
  -> RECD-1 ASR slate anchor recognition
       produces ASR candidate manifest
  -> VARW-R0 raw review
       produces reviewed_slate_anchor_manifest.csv
       produces split_plan_from_raw_markers.csv
       produces raw_marker_review.csv
  -> RECD-2 controlled split preview
       consumes reviewed_slate_anchor_manifest.csv
       consumes split_plan_from_raw_markers.csv
       must not consume raw_marker_review.csv as the primary cutting input
  -> VARW-R1 split review
       produces reviewed_render_anchors.csv
       produces segment_qc_sheet.csv
       produces split_marker_review.csv
  -> sample candidate gate
       consumes reviewed_render_anchors.csv
       consumes segment_qc_sheet.csv
       must not write sample_assets without later explicit authorization
```

| CSV | Producer | Consumer | Contract role | Primary input? | Audit/provenance only? |
| --- | --- | --- | --- | --- | --- |
| `reviewed_slate_anchor_manifest.csv` | VARW-R0 | RECD-2 controlled split preview | Trusted reviewed raw slate anchor input | Yes | No |
| `raw_marker_review.csv` | VARW-R0 | Human/debug/provenance review | Marker-level audit table | No | Yes |
| `split_plan_from_raw_markers.csv` | VARW-R0 | RECD-2 controlled split preview | Planned unit/clean split preview input | Yes | No |
| `reviewed_render_anchors.csv` | VARW-R1 | Render alignment and sample candidate gate | Reviewed segment render anchor input | Yes | No |
| `split_marker_review.csv` | VARW-R1 | Human/debug/provenance review | Marker-level R1 audit table | No | Yes |
| `segment_qc_sheet.csv` | VARW-R1 | Sample candidate gate | Segment QC and candidate gate input | Yes | No |

## 4. Global identity fields

All primary contract CSVs must define the following global identity fields:

| Field | Required in primary CSVs? | Meaning |
| --- | --- | --- |
| `recording_session_id` | Required | Stable recording session identifier, for example `RS_XWC_002_BAIYA_PILOT`. |
| `recording_id` | Required | Stable recording item or raw recording identifier within the session. |
| `piece_id` | Required | Canonical piece identifier. |
| `qinist_id` | Required | Canonical performer identifier, for example `QINIST_002`. |
| `batch_id` | Required | Batch identifier used by recording/review workflow. |
| `recording_take_no` | Required | Stable whole-session take number. |
| `batch_take_no` | Required | Batch-local execution order. |
| `script_id` | Required | Recording script or plan identifier. |

Rules:

- `recording_take_no` is the contract take key for whole-session ordering.
- `batch_take_no` is the performer-facing order inside a batch.
- `take_id` cannot replace `recording_take_no`.
- `take_id` may be retained as a UI/display alias or compatibility field, but it is not a contract primary key.
- R1 primary outputs must include `recording_take_no`, `batch_take_no`, `script_id`, `gesture_id`, and `source_split_audio`.
- R0 primary outputs must include `source_raw_audio`, `batch_id`, and `script_id`.
- Any R0 fallback that derives `recording_take_no` from legacy `takeId` is valid only if an upstream manifest guarantees that `takeId` has already been normalized to the stable whole-session take number.

## 5. Global safety fields

All primary contract CSVs must define:

| Field | Required value for this stage | Meaning |
| --- | --- | --- |
| `review_only` | `true` | Export is for review/control workflow only. |
| `production_grade` | `false` | Export is not production-grade sample data. |
| `not_sample_assets` | `true` | Export did not create and does not represent `sample_assets`. |

R0 split plan must also define:

| Field | Required value | Meaning |
| --- | --- | --- |
| `not_executed` | `true` | The row is a planned split preview instruction, not executed split output. |
| `not_recording_segments` | `true` | The row is not a written `recording_segments.csv` record. |

R1 outputs must also define:

| Field | Required value | Meaning |
| --- | --- | --- |
| `not_render_executed` | `true` | Review/export did not execute render. |
| `not_ml_training_data` | `true` | Review/export is not ML training data. |

Sample candidate gate safety rules:

- `render_usable=true` does not mean a sample asset was created.
- `human_accepted=true` does not mean `sample_assets.csv` was written.
- `segment_status=render_usable` does not mean render was executed.
- Sample ingest must be authorized by a later separate task.
- No R1 CSV may be consumed as production sample data while `review_only=true`, `production_grade=false`, or `not_sample_assets=true`.

## 6. Status enum policy

CSV contract status fields must use internal enum values. They must not use Chinese UI labels.

Marker and unit review enum:

```text
candidate
accepted
unclear
needs_retake
rejected
```

If R0 needs a unit-level workflow state, the field must be named:

```text
unit_status
```

`unit_status` is not the same enum family as marker `review_status`. RECD consumers must use `review_status=accepted` for reviewed anchor acceptance, not `unit_status=confirmed`.

R1 segment status enum:

```text
candidate
render_usable
reference_only
unclear
needs_retake
rejected
excluded
```

Chinese text is allowed only in explicit label fields ending in:

```text
*_label_zh
```

Example:

```text
segment_status=render_usable
segment_status_label_zh=渲染可用
```

The following is invalid in a contract status field:

```text
segment_status=渲染可用
```

## 7. Anchor type enum policy

Canonical field name:

```text
render_anchor_type
```

Backward-compatible alias:

```text
anchor_type
```

R1 render anchor type v0.1 active values:

```text
main_attack
gesture_start
context_first_attach
```

R1 render anchor type v0.1 reserved values:

```text
context_first_attack
context_second_attack
```

Rules:

- Writer v0.1 may allow only active values.
- Reserved values are named for future schema evolution, not silently accepted production behavior.
- Downstream consumers must not automatically treat `context_first_attach` as equivalent to `context_first_attack`.
- Supporting `context_first_attack` or `context_second_attack` requires a later schema migration and downstream render logic review.

## 8. R0 CSV contracts

### 8.1 `reviewed_slate_anchor_manifest.csv`

Role:

```text
VARW-R0 reviewed anchor primary output.
Trusted anchor input for RECD-2 controlled split preview.
```

Producer: VARW-R0.  
Consumer: RECD-2 controlled split preview.  
RECD consumption: may be consumed as reviewed anchor input only when required identity, source, boundary, review, and safety fields are present.

Required fields:

| Field | Producer | Consumer | Notes |
| --- | --- | --- | --- |
| `recording_session_id` | VARW-R0 | RECD-2 | Global identity. |
| `recording_id` | VARW-R0 | RECD-2 | Global identity. |
| `piece_id` | VARW-R0 | RECD-2 | Global identity. |
| `qinist_id` | VARW-R0 | RECD-2 | Global identity. |
| `batch_id` | VARW-R0 | RECD-2 | Global identity. |
| `recording_take_no` | VARW-R0 | RECD-2 | Stable session take number. |
| `batch_take_no` | VARW-R0 | RECD-2 | Batch-local take number. |
| `script_id` | VARW-R0 | RECD-2 | Recording script key. |
| `unit_id` | VARW-R0 | RECD-2 | Reviewed unit key. |
| `source_raw_audio` | VARW-R0 | RECD-2 | Canonical raw audio path. |
| `event_id` | VARW-R0 | RECD-2 | Score event key. |
| `event_range` | VARW-R0 | RECD-2 | Score event range. |
| `gesture_id` | VARW-R0 | RECD-2 | Gesture key. |
| `expected_sample_type` | VARW-R0 | RECD-2 | Expected sample class/type. |
| `slate_start_s` | VARW-R0 | RECD-2 | Slate start in raw audio seconds. |
| `slate_end_s` | VARW-R0 | RECD-2 | Slate end in raw audio seconds. |
| `guqin_start_s` | VARW-R0 | RECD-2 | First relevant guqin/audio start in raw audio seconds. |
| `tail_end_s` | VARW-R0 | RECD-2 | Musical tail/end reference in raw audio seconds. |
| `next_slate_start_s` | VARW-R0 | RECD-2 | Next slate boundary in raw audio seconds. |
| `review_status` | VARW-R0 | RECD-2 | Marker/unit review enum. |
| `review_only` | VARW-R0 | RECD-2 | Must be `true`. |
| `production_grade` | VARW-R0 | RECD-2 | Must be `false`. |
| `not_sample_assets` | VARW-R0 | RECD-2 | Must be `true`. |
| `updated_at` | VARW-R0 | RECD-2 | Export/update timestamp, not necessarily human review time. |

Optional fields:

```text
take_id
source_audio
unit_source
unit_status
boundary_unlinked
not_sample_ingest
not_recording_segments
notes
*_label_zh
```

Enum fields:

- `review_status`: `candidate`, `accepted`, `unclear`, `needs_retake`, `rejected`.
- `unit_status`, if present, is a separate workflow enum and not the marker review enum.

### 8.2 `raw_marker_review.csv`

Role:

```text
Audit / provenance only.
Must not be used as the RECD-2 primary cutting input.
```

Producer: VARW-R0.  
Consumer: human/debug/provenance review.  
RECD consumption: must not drive cutting directly; may support diagnostics and traceability.

Required fields:

| Field | Producer | Consumer | Notes |
| --- | --- | --- | --- |
| `recording_session_id` | VARW-R0 | Provenance review | Global identity. |
| `recording_id` | VARW-R0 | Provenance review | Global identity. |
| `piece_id` | VARW-R0 | Provenance review | Global identity. |
| `qinist_id` | VARW-R0 | Provenance review | Global identity. |
| `batch_id` | VARW-R0 | Provenance review | Batch identity. |
| `recording_take_no` | VARW-R0 | Provenance review | Stable session take number. |
| `marker_id` | VARW-R0 | Provenance review | Marker key. |
| `marker_type` | VARW-R0 | Provenance review | Marker type enum or known marker category. |
| `time_s` | VARW-R0 | Provenance review | Marker time in raw audio seconds. |
| `source` | VARW-R0 | Provenance review | Marker source, such as ASR/manual; not audio path. |
| `review_status` | VARW-R0 | Provenance review | Marker review enum. |
| `review_only` | VARW-R0 | Provenance review | Must be `true`. |
| `production_grade` | VARW-R0 | Provenance review | Must be `false`. |
| `updated_at` | VARW-R0 | Provenance review | Export/update timestamp. |

Optional fields:

```text
batch_take_no
script_id
unit_id
source_raw_audio
source_audio
confidence
nudge_total_ms
marker_label_zh
unit_status
training_value_class
notes
not_sample_assets
```

Enum fields:

- `review_status`: `candidate`, `accepted`, `unclear`, `needs_retake`, `rejected`.
- `marker_label_zh`, if present, is display-only and not a contract status value.

### 8.3 `split_plan_from_raw_markers.csv`

Role:

```text
RECD-2 controlled split preview execution plan input.
Plan rows are not executed split outputs.
```

Producer: VARW-R0.  
Consumer: RECD-2 controlled split preview.  
RECD consumption: may be consumed as split preview plan only when explicit identity, score/gesture, source, semantic boundary, and safety fields are present.

Required fields:

| Field | Producer | Consumer | Notes |
| --- | --- | --- | --- |
| `recording_session_id` | VARW-R0 | RECD-2 | Global identity. |
| `recording_id` | VARW-R0 | RECD-2 | Global identity. |
| `piece_id` | VARW-R0 | RECD-2 | Global identity. |
| `qinist_id` | VARW-R0 | RECD-2 | Global identity. |
| `batch_id` | VARW-R0 | RECD-2 | Global identity. |
| `recording_take_no` | VARW-R0 | RECD-2 | Stable session take number. |
| `batch_take_no` | VARW-R0 | RECD-2 | Batch-local take number. |
| `script_id` | VARW-R0 | RECD-2 | Recording script key. |
| `unit_id` | VARW-R0 | RECD-2 | Unit key. |
| `source_raw_audio` | VARW-R0 | RECD-2 | Canonical raw audio path. |
| `event_id` | VARW-R0 | RECD-2 | Score event key. |
| `event_range` | VARW-R0 | RECD-2 | Score event range. |
| `gesture_id` | VARW-R0 | RECD-2 | Gesture key. |
| `unit_start_s` | VARW-R0 | RECD-2 | Unit preview start, normally slate start. |
| `unit_end_s` | VARW-R0 | RECD-2 | Unit preview end, normally next slate start or unit boundary. |
| `slate_start_s` | VARW-R0 | RECD-2 | Source slate start. |
| `slate_end_s` | VARW-R0 | RECD-2 | Source slate end. |
| `next_slate_start_s` | VARW-R0 | RECD-2 | Next source slate start. |
| `suggested_clean_start_s` | VARW-R0 | RECD-2 | Suggested clean preview start, normally guqin start or slate end. |
| `suggested_clean_end_s` | VARW-R0 | RECD-2 | Suggested clean preview end. |
| `tail_end_s` | VARW-R0 | RECD-2 | Musical tail/end reference. |
| `split_plan_role` | VARW-R0 | RECD-2 | `unit_preview` or `clean_preview`. |
| `source_boundary_policy` | VARW-R0 | RECD-2 | Boundary derivation policy. |
| `requires_human_confirmation` | VARW-R0 | RECD-2 | Boolean confirmation gate. |
| `not_executed` | VARW-R0 | RECD-2 | Must be `true`. |
| `not_recording_segments` | VARW-R0 | RECD-2 | Must be `true`. |
| `not_sample_assets` | VARW-R0 | RECD-2 | Must be `true`. |
| `review_only` | VARW-R0 | RECD-2 | Must be `true`. |
| `production_grade` | VARW-R0 | RECD-2 | Must be `false`. |

Optional fields:

```text
take_id
source_audio
guqin_start_s
planned_unit_start_s
planned_unit_end_s
planned_clean_start_s
planned_clean_end_s
notes
updated_at
```

`split_plan_role` enum:

```text
unit_preview
clean_preview
```

Boundary semantics:

- `unit_start_s` and `unit_end_s` describe the full reviewed unit preview window.
- `suggested_clean_start_s` and `suggested_clean_end_s` describe the suggested clean preview window.
- `slate_start_s`, `slate_end_s`, `next_slate_start_s`, and `tail_end_s` preserve the semantic source boundaries used to derive the plan.
- A row may describe both unit and clean windows if all boundary fields are present and `split_plan_role` states which output the row authorizes for preview.
- Generic `start_s` and `end_s` are not valid substitutes for the v0.1 split plan contract.

## 9. R1 CSV contracts

### 9.1 `reviewed_render_anchors.csv`

Role:

```text
Render alignment / sample candidate gate primary input.
Does not execute render and does not create sample assets.
```

Producer: VARW-R1.  
Consumer: render alignment planning and sample candidate gate.  
RECD/sample gate consumption: may be consumed as reviewed render anchor input only when identity, split source, event/gesture, render anchor, status, and safety fields are present.

Required fields:

| Field | Producer | Consumer | Notes |
| --- | --- | --- | --- |
| `recording_session_id` | VARW-R1 | Render/sample gate | Global identity. |
| `recording_id` | VARW-R1 | Render/sample gate | Global identity. |
| `piece_id` | VARW-R1 | Render/sample gate | Global identity. |
| `qinist_id` | VARW-R1 | Render/sample gate | Global identity. |
| `batch_id` | VARW-R1 | Render/sample gate | Global identity. |
| `recording_take_no` | VARW-R1 | Render/sample gate | Stable session take number. |
| `batch_take_no` | VARW-R1 | Render/sample gate | Batch-local take number. |
| `script_id` | VARW-R1 | Render/sample gate | Recording script key. |
| `take_id` | VARW-R1 | UI/debug | UI/display id only; not a primary key. |
| `segment_id` | VARW-R1 | Render/sample gate | Split segment key. |
| `source_split_audio` | VARW-R1 | Render/sample gate | Canonical split audio path. |
| `event_id` | VARW-R1 | Render/sample gate | Score event key. |
| `event_range` | VARW-R1 | Render/sample gate | Score event range. |
| `gesture_id` | VARW-R1 | Render/sample gate | Gesture key. |
| `realization_variant` | VARW-R1 | Render/sample gate | Canonical realization variant. |
| `pre_idle_end_s` | VARW-R1 | Render/sample gate | Segment-local pre-idle end. |
| `gesture_start_s` | VARW-R1 | Render/sample gate | Segment-local gesture start. |
| `render_anchor_s` | VARW-R1 | Render/sample gate | Segment-local render anchor. |
| `tail_end_s` | VARW-R1 | Render/sample gate | Segment-local tail end. |
| `render_anchor_type` | VARW-R1 | Render/sample gate | Locked render anchor type enum. |
| `pre_attack_music_policy` | VARW-R1 | Render/sample gate | Policy for pre-attack musical content. |
| `tail_policy` | VARW-R1 | Render/sample gate | Policy for tail content. |
| `segment_status` | VARW-R1 | Sample gate | R1 segment status enum. |
| `review_status` | VARW-R1 | Render/sample gate | Marker/unit review enum. |
| `review_only` | VARW-R1 | Render/sample gate | Must be `true`. |
| `production_grade` | VARW-R1 | Render/sample gate | Must be `false`. |
| `not_sample_assets` | VARW-R1 | Render/sample gate | Must be `true`. |
| `not_render_executed` | VARW-R1 | Render/sample gate | Must be `true`. |
| `not_ml_training_data` | VARW-R1 | Render/sample gate | Must be `true`. |
| `updated_at` | VARW-R1 | Render/sample gate | Export/update timestamp. |

Optional fields:

```text
source_audio
variant
anchor_type
render_usable
notes
*_label_zh
```

Compatibility aliases:

- `source_audio` -> `source_split_audio`
- `variant` -> `realization_variant`, only if verified by manifest
- `anchor_type` -> `render_anchor_type`

Enum fields:

- `render_anchor_type` active values: `main_attack`, `gesture_start`, `context_first_attach`.
- `render_anchor_type` reserved values: `context_first_attack`, `context_second_attack`.
- `segment_status`: `candidate`, `render_usable`, `reference_only`, `unclear`, `needs_retake`, `rejected`, `excluded`.
- `review_status`: `candidate`, `accepted`, `unclear`, `needs_retake`, `rejected`.

### 9.2 `split_marker_review.csv`

Role:

```text
Audit / provenance only.
Must not be used as the sample gate primary input.
```

Producer: VARW-R1.  
Consumer: human/debug/provenance review.  
RECD/sample gate consumption: must not drive sample candidacy directly; may support diagnostics and traceability.

Required fields:

| Field | Producer | Consumer | Notes |
| --- | --- | --- | --- |
| `recording_session_id` | VARW-R1 | Provenance review | Global identity. |
| `recording_id` | VARW-R1 | Provenance review | Global identity. |
| `piece_id` | VARW-R1 | Provenance review | Global identity. |
| `qinist_id` | VARW-R1 | Provenance review | Global identity. |
| `batch_id` | VARW-R1 | Provenance review | Global identity. |
| `recording_take_no` | VARW-R1 | Provenance review | Stable session take number. |
| `batch_take_no` | VARW-R1 | Provenance review | Batch-local take number. |
| `script_id` | VARW-R1 | Provenance review | Recording script key. |
| `segment_id` | VARW-R1 | Provenance review | Split segment key. |
| `marker_id` | VARW-R1 | Provenance review | Marker key. |
| `marker_type` | VARW-R1 | Provenance review | Marker type enum or known marker category. |
| `time_s` | VARW-R1 | Provenance review | Marker time in split audio seconds. |
| `source` | VARW-R1 | Provenance review | Marker source, not audio path. |
| `review_status` | VARW-R1 | Provenance review | Marker review enum. |
| `nudge_total_ms` | VARW-R1 | Provenance review | Total marker adjustment in milliseconds. |
| `review_only` | VARW-R1 | Provenance review | Must be `true`. |
| `production_grade` | VARW-R1 | Provenance review | Must be `false`. |
| `not_sample_assets` | VARW-R1 | Provenance review | Must be `true`. |
| `not_render_executed` | VARW-R1 | Provenance review | Must be `true`. |
| `not_ml_training_data` | VARW-R1 | Provenance review | Must be `true`. |
| `updated_at` | VARW-R1 | Provenance review | Export/update timestamp. |

Optional fields:

```text
take_id
source_split_audio
source_audio
event_id
event_range
gesture_id
confidence
marker_label_zh
training_value_class
notes
```

Enum fields:

- `review_status`: `candidate`, `accepted`, `unclear`, `needs_retake`, `rejected`.
- Chinese marker labels may appear only in `marker_label_zh`.

### 9.3 `segment_qc_sheet.csv`

Role:

```text
Sample candidate gate primary input.
Must not directly write sample_assets.
```

Producer: VARW-R1.  
Consumer: sample candidate gate.  
Sample gate consumption: may identify candidate eligibility only; cannot create `sample_assets.csv` or `recording_segments.csv`.

Required fields:

| Field | Producer | Consumer | Notes |
| --- | --- | --- | --- |
| `recording_session_id` | VARW-R1 | Sample gate | Global identity. |
| `recording_id` | VARW-R1 | Sample gate | Global identity. |
| `piece_id` | VARW-R1 | Sample gate | Global identity. |
| `qinist_id` | VARW-R1 | Sample gate | Global identity. |
| `batch_id` | VARW-R1 | Sample gate | Global identity. |
| `recording_take_no` | VARW-R1 | Sample gate | Stable session take number. |
| `batch_take_no` | VARW-R1 | Sample gate | Batch-local take number. |
| `script_id` | VARW-R1 | Sample gate | Recording script key. |
| `segment_id` | VARW-R1 | Sample gate | Split segment key. |
| `source_split_audio` | VARW-R1 | Sample gate | Canonical split audio path. |
| `event_id` | VARW-R1 | Sample gate | Score event key. |
| `event_range` | VARW-R1 | Sample gate | Score event range. |
| `gesture_id` | VARW-R1 | Sample gate | Gesture key. |
| `realization_variant` | VARW-R1 | Sample gate | Canonical realization variant. |
| `duration_s` | VARW-R1 | Sample gate | Segment duration. |
| `segment_status` | VARW-R1 | Sample gate | R1 segment status enum. |
| `render_usable` | VARW-R1 | Sample gate | Boolean convenience field, not sample creation. |
| `reference_only` | VARW-R1 | Sample gate | Boolean QC class. |
| `unclear` | VARW-R1 | Sample gate | Boolean QC class. |
| `needs_retake` | VARW-R1 | Sample gate | Boolean QC class. |
| `rejected` | VARW-R1 | Sample gate | Boolean QC class. |
| `excluded` | VARW-R1 | Sample gate | Boolean QC class. |
| `human_accepted` | VARW-R1 | Sample gate | Human review accepted the segment for gate consideration only. |
| `reviewed_by` | VARW-R1 | Sample gate | Reviewer identifier. |
| `reviewed_at` | VARW-R1 | Sample gate | Human review timestamp. |
| `reject_reason` | VARW-R1 | Sample gate | Rejection or exclusion reason. |
| `noise_issue` | VARW-R1 | Sample gate | Boolean QC issue. |
| `click_issue` | VARW-R1 | Sample gate | Boolean QC issue. |
| `tail_clipped` | VARW-R1 | Sample gate | Boolean QC issue. |
| `attack_clipped` | VARW-R1 | Sample gate | Boolean QC issue. |
| `slate_residue` | VARW-R1 | Sample gate | Boolean QC issue. |
| `wrong_take` | VARW-R1 | Sample gate | Boolean QC issue. |
| `review_only` | VARW-R1 | Sample gate | Must be `true`. |
| `production_grade` | VARW-R1 | Sample gate | Must be `false`. |
| `not_sample_assets` | VARW-R1 | Sample gate | Must be `true`. |
| `not_render_executed` | VARW-R1 | Sample gate | Must be `true`. |
| `not_ml_training_data` | VARW-R1 | Sample gate | Must be `true`. |
| `updated_at` | VARW-R1 | Sample gate | Export/update timestamp, not a substitute for `reviewed_at`. |

Optional fields:

```text
take_id
source_audio
variant
notes
segment_status_label_zh
```

Rules:

- `human_accepted=true` only means human aural/review acceptance for gate consideration.
- `render_usable=true` only means render alignment appears usable.
- Both booleans together still do not mean a sample asset was created.
- Sample ingest must be authorized by a later separate task.
- `updated_at` is export/update time and does not replace `reviewed_at`.
- `render_usable` is a boolean convenience field and is not sufficient as a replacement for `segment_status`.

Enum fields:

- `segment_status`: `candidate`, `render_usable`, `reference_only`, `unclear`, `needs_retake`, `rejected`, `excluded`.
- `segment_status_label_zh`, if present, is display-only.

## 10. Backward-compatible aliases

Migration aliases are allowed only to help current readers and writers transition to this v0.1 contract.

| Legacy field | Canonical v0.1 meaning | Rules |
| --- | --- | --- |
| `source_audio` in R0 | `source_raw_audio` | R0 legacy `source_audio` means raw audio only. New writers should emit `source_raw_audio`; migration writers may emit both. |
| `source_audio` in R1 | `source_split_audio` | R1 legacy `source_audio` means split audio only. New writers should emit `source_split_audio`; migration writers may emit both. |
| `take_id` | UI/display id | `take_id` is not equivalent to `recording_take_no` and cannot serve as a contract key. |
| `variant` | `realization_variant` | Valid only if verified by manifest or source segment metadata. |
| `anchor_type` | `render_anchor_type` | Migration writers may emit both; consumers should prefer `render_anchor_type`. |
| `render_usable` | Boolean convenience field | Useful for filtering, but not sufficient as a `segment_status` replacement and not evidence of sample asset creation. |

Alias precedence:

1. Prefer canonical v0.1 fields when present.
2. Use aliases only during migration.
3. Reject ambiguous alias values if the source stage cannot prove whether the value refers to raw audio, split audio, display take id, or realization variant.

## 11. Migration notes for writer patch

Future writer patch should be a separate authorized task. That task should:

1. Add global identity fields to all primary CSVs.
2. Add `source_raw_audio` to R0 primary CSVs.
3. Add `source_split_audio` to R1 primary CSVs.
4. Add `recording_take_no`, `batch_take_no`, `script_id`, and `gesture_id` to R1 primary CSVs.
5. Add explicit score/gesture keys and semantic boundary fields to `split_plan_from_raw_markers.csv`.
6. Add `segment_status`, `human_accepted`, `reviewed_by`, `reviewed_at`, `excluded`, and `not_ml_training_data` to `segment_qc_sheet.csv`.
7. Rename or duplicate `variant` as `realization_variant`.
8. Rename or duplicate `anchor_type` as `render_anchor_type`.
9. Keep migration aliases for one compatibility window, then remove only after downstream readers are updated.
10. Keep all safety flags at the review-stage values listed in this spec.

The writer patch must not change semantic stage. A CSV row that passes this contract is still review/sample-candidate data, not a rendered sample, sample asset, production asset, or ML training item.

## 12. Validation rules for future tests

This task does not implement tests. Future tests should validate:

1. All primary CSVs contain global identity fields.
2. R1 primary CSVs contain `recording_take_no`.
3. R1 primary CSVs contain `source_split_audio`.
4. R0 primary CSVs contain `source_raw_audio`.
5. Contract status fields use internal enums.
6. Chinese labels only appear in `*_label_zh`.
7. R0 split plan contains explicit slate/tail/unit/clean boundaries.
8. R1 `segment_qc_sheet.csv` contains `human_accepted`, `reviewed_by`, and `reviewed_at`.
9. No primary CSV implies `sample_assets` were written.
10. `review_only=true` and `production_grade=false` are present.
11. `not_sample_assets=true` is present.
12. R1 outputs include `not_render_executed=true` and `not_ml_training_data=true`.
13. `take_id` is not accepted as a substitute for `recording_take_no`.
14. `source_audio` alias use is stage-specific and cannot be ambiguous.
15. `segment_status` never contains Chinese UI labels such as `渲染可用`.
16. `render_anchor_type` values are either active v0.1 values or explicitly rejected reserved values until a later migration authorizes them.
17. `raw_marker_review.csv` and `split_marker_review.csv` are not accepted as primary split/sample gate inputs.

## 13. Open decisions

The following decisions remain open for later implementation or schema migration tasks:

1. Whether writer v0.1 emits both legacy aliases and canonical fields in the same CSV, or emits canonical fields only after a compatibility reader update.
2. Whether `context_first_attack` and `context_second_attack` should become active `render_anchor_type` values in a future schema version.
3. Whether `raw_marker_review.csv` should include optional `batch_take_no`, `script_id`, `event_id`, `event_range`, `gesture_id`, and `source_raw_audio` for easier provenance joins.
4. Whether `split_marker_review.csv` should include optional `source_split_audio`, `event_id`, `event_range`, and `gesture_id` for easier provenance joins.
5. Whether `reviewed_at` should be human-entered, system-captured at reviewer action time, or both with separate fields.
6. Whether `segment_status` should be derived from booleans or stored as the canonical review decision in the VARW-R1 data model.

None of these open decisions blocks the v0.1 contract freeze because the required safety and identity rules are explicit here.

## 14. Explicit no-execution statement

This specification is documentation-only.

No split audio was created.  
No clean preview was generated.  
No `02_recordings/` file was written.  
No `03_samples/` file was written.  
No `03_samples/sample_assets.csv` was written.  
No `03_samples/recording_segments.csv` was written.  
No `recording_items_enriched.jsonl` was written.  
No `04_outputs/` file was written.  
No render was executed.  
No sample ingest was executed.  
No ML training was executed.  
No source code was modified by this contract spec.
