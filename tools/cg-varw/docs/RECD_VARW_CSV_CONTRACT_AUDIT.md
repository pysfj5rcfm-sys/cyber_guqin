# RECD / VARW CSV Contract Audit

Task: `CG-RECD_VARW_CSV_CONTRACT_AUDIT`  
Project instruction context: `Core_Instructions_v1.3.1.md`  
Session context: `RS_XWC_002_BAIYA_PILOT`, `QINIST_002 = 白牙`  
Audit date: 2026-06-12

This is a documentation-only field contract audit. No split, sample ingest, render, or ML action was executed.

## 1. Executive summary

Judgment: `CONTRACT_NOT_READY`

The current CG-VARW R0/R1 CSV writers are usable as review exports, and they preserve important safety flags such as `review_only=true`, `production_grade=false`, `not_sample_assets=true`, and `not_render_executed=true` where applicable. The CSV values inspected in backend writers remain internal enum-like values rather than Chinese UI labels.

The contract is not ready for direct future RECD consumption because several downstream-critical identity and boundary fields are absent or ambiguous:

- R1 exports use `take_id` but do not explicitly export `recording_take_no`, `batch_take_no`, `recording_id`, `recording_session_id`, `script_id`, `gesture_id`, or `source_split_audio`.
- R1 `segment_qc_sheet.csv` can express QC booleans, but it lacks reviewer identity, review timestamp distinct from export `updated_at`, explicit human acceptance, `excluded`, and `not_ml_training_data`.
- R0 `split_plan_from_raw_markers.csv` avoids generic `start_s` / `end_s`, but it does not explicitly distinguish `slate_start_s`, `slate_end_s`, `next_slate_start_s`, `tail_end_s`, or whether the plan is unit preview vs clean preview beyond `planned_*` names.
- The canonical R1 `anchor_type` enum is not locked against possible future values such as `context_first_attack` or `context_second_attack`.

Finding counts:

- `BLOCKER`: 4
- `MAJOR`: 7
- `MINOR`: 5
- `INFO`: 4

## 2. Current pipeline contract diagram

```text
RECD-0 raw archive
  -> session_manifest / raw_audio_inventory / take_manifest
  -> RECD-1 ASR slate anchor recognition
       produces ASR candidate manifest
  -> VARW-R0 raw review
       consumes ASR candidates
       produces reviewed_slate_anchor_manifest.csv
       produces split_plan_from_raw_markers.csv
       produces raw_marker_review.csv as audit/provenance
  -> RECD-2 controlled split preview
       consumes R0 reviewed anchors and split plan
       produces unit preview / clean segment preview
  -> VARW-R1 split review
       consumes clean split preview and segment metadata
       produces reviewed_render_anchors.csv
       produces segment_qc_sheet.csv
       produces split_marker_review.csv as audit/provenance
  -> sample candidate gate
       consumes R1 reviewed_render_anchors.csv and segment_qc_sheet.csv
       must not write sample_assets without later explicit authorization
```

## 3. CSV producer/consumer matrix

| CSV | Producer | Consumer | Contract role | Primary input? | Audit/provenance only? | Affects split? | Affects render alignment? | Affects sample gate? | Must not write sample_assets? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `reviewed_slate_anchor_manifest.csv` | VARW-R0 backend `r0_export_writer.py` | RECD-2 controlled split preview | Trusted reviewed raw slate anchor input | Yes | No | Yes | Indirect | No | Yes |
| `raw_marker_review.csv` | VARW-R0 backend `r0_export_writer.py` | Human/debug/provenance review | Marker-level audit table | No | Yes | No direct effect | No | No | Yes |
| `split_plan_from_raw_markers.csv` | VARW-R0 backend `r0_export_writer.py` | RECD-2 controlled split preview | Planned unit/clean split execution input | Yes | No | Yes | Indirect | No | Yes |
| `reviewed_render_anchors.csv` | VARW-R1 backend `r1_review_store.py` | Render alignment and sample candidate gate | Reviewed segment render anchor input | Yes | No | No | Yes | Yes | Yes |
| `split_marker_review.csv` | VARW-R1 backend `r1_review_store.py` | Human/debug/provenance review | Marker-level R1 audit table | No | Yes | No | Indirect/debug | No | Yes |
| `segment_qc_sheet.csv` | VARW-R1 backend `r1_review_store.py` | Sample candidate gate | Segment QC and usability gate input | Yes | No | No | Indirect | Yes | Yes |

## 4. R0 CSV contract audit

### `reviewed_slate_anchor_manifest.csv`

Current writer fields:

```text
file_id, source_audio, unit_id, recording_take_no, batch_take_no, unit_source,
unit_status, review_status, event_id, event_range, gesture_id, expected_sample_type,
slate_start_s, slate_end_s, guqin_start_s, tail_end_s, next_slate_start_s,
boundary_unlinked, review_only, production_grade, not_sample_ingest,
not_recording_segments, not_sample_assets, notes, updated_at
```

Required columns currently present:

```text
source_audio, unit_id, recording_take_no, batch_take_no, unit_status,
review_status, event_id, event_range, gesture_id, slate_start_s, slate_end_s,
guqin_start_s, tail_end_s, next_slate_start_s, review_only, production_grade,
not_sample_assets, updated_at
```

Optional columns currently present:

```text
file_id, unit_source, expected_sample_type, boundary_unlinked, not_sample_ingest,
not_recording_segments, notes
```

Missing columns:

```text
recording_session_id, recording_id, piece_id, qinist_id, batch_id, script_id,
take_id, source_raw_audio, realization_variant
```

Ambiguous columns:

```text
source_audio
```

`source_audio` may be the raw source audio, but future RECD consumers asked for `source_raw_audio` / `source_split_audio` distinction. R0 should document whether `source_audio` is always raw audio.

Extra columns that are okay:

```text
not_sample_ingest, not_recording_segments, boundary_unlinked
```

Extra columns that may confuse consumers:

```text
unit_status
```

`unit_status` uses `confirmed` / `needs_review`, while marker contract expects `accepted` / `unclear` style internal values. It is acceptable if documented as UI-unit state, but consumers should prefer `review_status` for reviewed anchor status.

### `raw_marker_review.csv`

Current writer fields:

```text
file_id, source_audio, unit_id, recording_take_no, unit_status, marker_id,
marker_type, marker_label_zh, time_s, source, confidence, review_status,
nudge_total_ms, notes, review_only, production_grade, training_value_class,
updated_at
```

Required columns currently present:

```text
source_audio, unit_id, recording_take_no, marker_id, marker_type, time_s,
source, confidence, review_status, nudge_total_ms, review_only, production_grade,
updated_at
```

Optional columns currently present:

```text
file_id, unit_status, marker_label_zh, notes, training_value_class
```

Missing columns:

```text
batch_take_no, recording_session_id, recording_id, piece_id, qinist_id,
batch_id, script_id, event_id, event_range, gesture_id, source_raw_audio
```

Ambiguous columns:

```text
source_audio, source
```

`source_audio` is likely raw audio provenance. `source` is marker source such as ASR/manual and must not be interpreted as file provenance.

Extra columns that are okay:

```text
marker_label_zh, training_value_class
```

Extra columns that may confuse consumers:

```text
unit_status
```

This is audit/provenance only and should not be used as the RECD-2 cutting input.

### `split_plan_from_raw_markers.csv`

Current writer fields:

```text
file_id, source_audio, unit_id, recording_take_no, batch_take_no,
planned_unit_start_s, planned_unit_end_s, planned_clean_start_s,
planned_clean_end_s, source_boundary_policy, requires_human_confirmation,
not_executed, not_recording_segments, not_sample_assets, review_only,
production_grade, notes
```

Required columns currently present:

```text
source_audio, unit_id, recording_take_no, batch_take_no, planned_unit_start_s,
planned_unit_end_s, planned_clean_start_s, planned_clean_end_s,
source_boundary_policy, requires_human_confirmation, not_executed,
not_recording_segments, not_sample_assets, review_only, production_grade
```

Optional columns currently present:

```text
file_id, notes
```

Missing columns:

```text
recording_session_id, recording_id, piece_id, qinist_id, batch_id, script_id,
event_id, event_range, gesture_id, source_raw_audio, slate_start_s,
slate_end_s, next_slate_start_s, tail_end_s, suggested_clean_start_s,
suggested_clean_end_s
```

Ambiguous columns:

```text
planned_unit_start_s, planned_unit_end_s, planned_clean_start_s,
planned_clean_end_s
```

These are better than generic `start_s` / `end_s`, but the CSV does not explicitly state that `planned_unit_start_s = slate_start`, `planned_unit_end_s = next_slate_start`, `planned_clean_start_s = guqin_start or slate_end`, and `planned_clean_end_s = next_slate_start`.

Extra columns that are okay:

```text
requires_human_confirmation, not_executed, not_recording_segments
```

Extra columns that may confuse consumers:

```text
source_boundary_policy
```

`source_boundary_policy=reviewed_required_markers` is helpful, but the concrete boundary derivation should be documented or split into explicit fields.

## 5. R1 CSV contract audit

### `reviewed_render_anchors.csv`

Current writer fields:

```text
batch_id, take_id, segment_id, source_audio, event_id, event_range, variant,
pre_idle_end_s, gesture_start_s, render_anchor_s, tail_end_s, anchor_type,
pre_attack_music_policy, tail_policy, render_usable, review_status,
review_only, production_grade, not_sample_assets, not_render_executed,
updated_at, notes
```

Required columns currently present:

```text
batch_id, take_id, segment_id, source_audio, event_id, event_range, variant,
pre_idle_end_s, gesture_start_s, render_anchor_s, tail_end_s, anchor_type,
pre_attack_music_policy, tail_policy, render_usable, review_status,
review_only, production_grade, not_sample_assets, not_render_executed,
updated_at
```

Optional columns currently present:

```text
notes
```

Missing columns:

```text
recording_session_id, recording_id, piece_id, qinist_id, recording_take_no,
batch_take_no, script_id, gesture_id, realization_variant, source_split_audio,
not_ml_training_data
```

Ambiguous columns:

```text
take_id, source_audio, variant, render_usable
```

`take_id` may encode `T001`, but the contract requires unambiguous `recording_take_no`. `source_audio` is actually `segment.relative_path`, so it is a split segment path and should be named or duplicated as `source_split_audio`. `variant` appears to be realization/split variant but is not named `realization_variant`. `render_usable` is a boolean, not the segment status enum.

Extra columns that are okay:

```text
pre_attack_music_policy, tail_policy
```

Extra columns that may confuse consumers:

```text
render_usable
```

It is useful, but the sample gate should also receive a single explicit segment status enum or clear QC status.

### `split_marker_review.csv`

Current writer fields:

```text
batch_id, take_id, segment_id, marker_id, marker_type, marker_label_zh,
time_s, source, confidence, review_status, nudge_total_ms, notes,
review_only, production_grade, training_value_class, updated_at
```

Required columns currently present:

```text
batch_id, take_id, segment_id, marker_id, marker_type, time_s, source,
confidence, review_status, nudge_total_ms, review_only, production_grade,
updated_at
```

Optional columns currently present:

```text
marker_label_zh, notes, training_value_class
```

Missing columns:

```text
recording_session_id, recording_id, piece_id, qinist_id, recording_take_no,
batch_take_no, script_id, event_id, event_range, gesture_id, source_split_audio,
not_sample_assets, not_render_executed, not_ml_training_data
```

Ambiguous columns:

```text
take_id, source
```

`source` is marker source, not audio source.

Extra columns that are okay:

```text
marker_label_zh, training_value_class
```

Extra columns that may confuse consumers:

```text
none if treated as audit/provenance only
```

### `segment_qc_sheet.csv`

Current writer fields:

```text
batch_id, take_id, segment_id, source_audio, duration_s, render_usable,
reference_only, unclear, needs_retake, rejected, reject_reason, noise_issue,
click_issue, tail_clipped, attack_clipped, slate_residue, wrong_take, notes,
review_only, production_grade, not_sample_assets, not_render_executed,
updated_at
```

Required columns currently present:

```text
batch_id, take_id, segment_id, source_audio, duration_s, render_usable,
reference_only, unclear, needs_retake, rejected, reject_reason, noise_issue,
click_issue, tail_clipped, attack_clipped, slate_residue, wrong_take,
review_only, production_grade, not_sample_assets, not_render_executed,
updated_at
```

Optional columns currently present:

```text
notes
```

Missing columns:

```text
recording_session_id, recording_id, piece_id, qinist_id, recording_take_no,
batch_take_no, script_id, event_id, event_range, gesture_id,
realization_variant, source_split_audio, excluded, reviewed_by, reviewed_at,
human_accepted, segment_status, not_ml_training_data
```

Ambiguous columns:

```text
take_id, source_audio, updated_at
```

`updated_at` is export time, not necessarily human review time. `source_audio` is a split path but not named as such.

Extra columns that are okay:

```text
noise_issue, click_issue, tail_clipped, attack_clipped, slate_residue,
wrong_take
```

Extra columns that may confuse consumers:

```text
render_usable
```

As a boolean it is safe, but it should not be mistaken for sample creation, production readiness, render execution, or ML readiness.

## 6. Identity key audit

| Key | R0 reviewed manifest | R0 marker review | R0 split plan | R1 render anchors | R1 marker review | R1 segment QC | Audit result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `recording_session_id` | Missing | Missing | Missing | Missing | Missing | Missing | `MAJOR` across all primary outputs |
| `recording_id` | Missing | Missing | Missing | Missing | Missing | Missing | `MAJOR` |
| `piece_id` | Missing | Missing | Missing | Missing | Missing | Missing | `MAJOR` |
| `qinist_id` | Missing | Missing | Missing | Missing | Missing | Missing | `MAJOR` |
| `batch_id` | Missing | Missing | Missing | Present | Present | Present | `MAJOR` for R0 batch trace |
| `recording_take_no` | Present | Present | Present | Missing | Missing | Missing | `BLOCKER` for R1 |
| `batch_take_no` | Present | Missing | Present | Missing | Missing | Missing | `MAJOR` |
| `take_id` | Not explicit; fallback source | Not explicit | Not explicit | Present | Present | Present | `MAJOR`; not equivalent to `recording_take_no` |
| `script_id` | Missing | Missing | Missing | Missing | Missing | Missing | `MAJOR` |
| `segment_id` | N/A | N/A | N/A | Present | Present | Present | OK for R1 |
| `event_id` | Present | Missing | Missing | Present | Missing | Missing | `MAJOR` for split plan/QC |
| `event_range` | Present | Missing | Missing | Present | Missing | Missing | `MAJOR` for context preservation |
| `gesture_id` | Present | Missing | Missing | Missing | Missing | Missing | `BLOCKER` for sample gate |
| `realization_variant` | Missing | Missing | Missing | Ambiguous as `variant` | Missing | Missing | `MAJOR` |
| `source_audio` | Present | Present | Present | Present | Missing | Present | Ambiguous between raw/split |
| `source_raw_audio` | Missing | Missing | Missing | N/A | N/A | N/A | `MAJOR` for R0 clarity |
| `source_split_audio` | N/A | N/A | N/A | Missing; value in `source_audio` | Missing | Missing; value in `source_audio` | `BLOCKER` for R1 path clarity |

`recording_take_no` vs `batch_take_no`:

- Project documentation states `recording_take_no` is the stable whole-session take number and `batch_take_no` is performer-facing batch order only.
- R0 exports both values in primary files, but when absent the writer falls back to `unit.takeId` for `recording_take_no` and `unit.sequence` for `batch_take_no`. That fallback can be unsafe if `takeId` is not normalized as a whole-session take number.
- R1 exports do not carry either `recording_take_no` or `batch_take_no`. R1 `take_id` must not be treated as automatically equivalent to `recording_take_no`.

## 7. Status enum audit

Expected marker/unit internal marker enum:

```text
candidate, accepted, unclear, needs_retake, rejected
```

Current R0/R1 marker `review_status` values are internal values and not Chinese labels. UI labels such as `待确认`, `已确认`, `待复核`, `需重录`, and `已排除` live in frontend label maps and `marker_label_zh`, not in contract status fields.

Observed R0 derived unit states:

```text
unit_status: candidate, confirmed, needs_review, needs_retake, excluded, rejected
review_status: not_started, in_progress, accepted, unclear, needs_retake, rejected
```

Risk: `unit_status` is not the same enum as marker review status. RECD consumers should use `review_status=accepted` for reviewed anchor acceptance rather than `unit_status=confirmed`.

Expected R1 segment internal enum:

```text
render_usable, reference_only, unclear, needs_retake, rejected, excluded
```

Current R1 schema contains:

```text
candidate, render_usable, reference_only, unclear, needs_retake, rejected, excluded
```

`candidate` is an additional pre-review state and should be explicitly allowed for in-progress exports, or filtered out of final contract exports.

`render_usable` vs `渲染可用`:

- UI label map renders `render_usable` as `渲染可用`.
- CSV writer exports internal booleans/values, not the Chinese label.
- There is no observed silent switch from `render_usable` to `渲染可用` in CSV contract fields.

## 8. Anchor type enum audit

Current backend/frontend schema allows:

```text
main_attack, gesture_start, context_first_attach
```

Current synthetic manifest uses:

```text
main_attack, context_first_attach
```

Potential expected or disputed values called out for review:

```text
main_attack, gesture_start, context_first_attach, context_first_attack,
context_second_attack
```

Recommendation: lock the canonical enum to:

```text
main_attack, gesture_start, context_first_attach, context_first_attack,
context_second_attack
```

If `context_first_attack` / `context_second_attack` are out of scope for R1A, document them as reserved values and keep the current parser strict. Do not rely on `context_first_attach` to mean attack unless downstream render logic explicitly supports that interpretation.

## 9. Split boundary audit

`split_plan_from_raw_markers.csv` does not use generic `start_s` / `end_s`; it uses:

```text
planned_unit_start_s, planned_unit_end_s, planned_clean_start_s,
planned_clean_end_s
```

Current derivation:

```text
planned_unit_start_s = slate_start
planned_unit_end_s = next_slate_start
planned_clean_start_s = guqin_start if present else slate_end
planned_clean_end_s = next_slate_start
```

Requested equivalent fields:

```text
unit_start_s, unit_end_s, slate_start_s, slate_end_s, next_slate_start_s,
suggested_clean_start_s, suggested_clean_end_s, tail_end_s
```

Current gap:

- It does not explicitly carry `slate_start_s`, `slate_end_s`, `next_slate_start_s`, or `tail_end_s` in the split plan.
- It does not explicitly identify `unit preview`, `clean preview`, or `slate trim` as separate plan roles.
- It lacks a clear `tail_end_s`; clean end currently uses `next_slate_start`, which may preserve gap/slate context but is not the same as musical tail end.

## 10. Render anchor audit

`reviewed_render_anchors.csv` contains:

```text
segment_id, take_id, source_audio, render_anchor_s, anchor_type,
pre_idle_end_s, gesture_start_s, tail_end_s, tail_policy,
pre_attack_music_policy, review_status, review_only, production_grade
```

Missing or ambiguous for downstream render alignment:

```text
recording_take_no, source_split_audio, render_anchor_type,
not_ml_training_data
```

Notes:

- `anchor_type` currently serves as the render anchor type field, but the requested field name is `render_anchor_type`.
- `source_audio` contains `segment.relative_path`, so it is operationally the split audio path. The contract should either rename it to `source_split_audio` or include both.
- `take_id` should not be the only take identity for render alignment.

## 11. Segment QC / sample candidate gate audit

`segment_qc_sheet.csv` can answer:

```text
whether render_usable/reference_only/unclear/needs_retake/rejected
why via reject_reason and issue booleans
whether still review_only
whether production_grade=false
whether not_sample_assets=true
whether not_render_executed=true
```

It cannot fully answer:

```text
who reviewed
when human review occurred
whether human accepted
whether excluded
whether not_ml_training_data=true in CSV
```

The sheet does not imply:

```text
sample asset created
production sample
render executed
ML-ready
```

because it explicitly carries `review_only=true`, `production_grade=false`, `not_sample_assets=true`, and `not_render_executed=true`.

Risk remains that a downstream consumer may treat `render_usable=true` as sample-ready without later authorization. The sample candidate gate must require `not_sample_assets=true` and an explicit later promotion task.

## 12. Blocking mismatches

1. `BLOCKER`: R1 primary outputs do not export `recording_take_no`; they only export `take_id`. This can confuse stable whole-session take identity with file or display IDs.
2. `BLOCKER`: R1 primary outputs do not export `source_split_audio`; `source_audio` is populated with `segment.relative_path`, but the raw/split path role is not explicit.
3. `BLOCKER`: R1 sample-gate outputs do not export `gesture_id` or `script_id`, so promoted candidates cannot safely map back to recording plan / gesture contract without external joins.
4. `BLOCKER`: `segment_qc_sheet.csv` lacks explicit human acceptance and reviewer fields, so it cannot independently prove a segment is accepted for a gate.

## 13. Non-blocking mismatches

1. `MAJOR`: All six CSVs lack `recording_session_id`, `recording_id`, `piece_id`, and `qinist_id`.
2. `MAJOR`: R0 split plan lacks explicit `event_id`, `event_range`, and `gesture_id`, even though R0 manifest carries them.
3. `MAJOR`: R0 split plan lacks explicit slate/tail boundary source columns needed to audit unit vs clean preview decisions.
4. `MAJOR`: R1 `variant` is not named `realization_variant`, and may not be semantically equivalent.
5. `MAJOR`: R1 `anchor_type` enum is narrower than the candidate canonical set discussed for future context anchors.
6. `MAJOR`: R1 CSVs lack `not_ml_training_data`, although draft JSON carries it.
7. `MAJOR`: R0 writer fallbacks may populate `recording_take_no` from `takeId` and `batch_take_no` from `sequence`; safe only if upstream data is normalized.
8. `MINOR`: R0 `unit_status` and `review_status` use different enum families and need contract notes.
9. `MINOR`: R0/R1 marker review files include Chinese label columns, which are safe as label columns but should remain non-contractual.
10. `MINOR`: `updated_at` is export time, not necessarily human review time.
11. `MINOR`: R1 `render_usable` appears as boolean columns, not a single `segment_status` export.
12. `MINOR`: `raw_marker_review.csv` does not include `batch_take_no`; acceptable as audit-only, but inconvenient for provenance joins.

## 14. Recommended contract lock decisions

1. Lock primary contract inputs:
   - RECD-2 consumes `reviewed_slate_anchor_manifest.csv` and `split_plan_from_raw_markers.csv`.
   - RECD-2 must not consume `raw_marker_review.csv` as the main cutting input.
   - Render/sample gate consumes `reviewed_render_anchors.csv` and `segment_qc_sheet.csv`.
   - `split_marker_review.csv` remains audit/provenance only.
2. Add or require explicit identity fields in all primary outputs:
   - `recording_session_id`, `recording_id`, `piece_id`, `qinist_id`, `batch_id`, `recording_take_no`, `batch_take_no`, `script_id`.
3. Lock path role fields:
   - R0 primary outputs should carry `source_raw_audio`.
   - R1 primary outputs should carry `source_split_audio`.
   - Keep `source_audio` only as a backward-compatible alias if needed.
4. Lock R0 split boundary names:
   - Include explicit `unit_start_s`, `unit_end_s`, `slate_start_s`, `slate_end_s`, `next_slate_start_s`, `suggested_clean_start_s`, `suggested_clean_end_s`, and `tail_end_s`.
5. Lock R1 anchor enum:
   - Current active: `main_attack`, `gesture_start`, `context_first_attach`.
   - Reserved or canonical extension: `context_first_attack`, `context_second_attack`.
6. Lock status policy:
   - CSV contract values must remain internal values.
   - Chinese labels may appear only in explicit `*_label_zh` columns.
7. Lock sample gate safety:
   - `render_usable=true` is necessary but not sufficient for sample asset creation.
   - Require `review_only=true`, `production_grade=false`, `not_sample_assets=true`, `not_render_executed=true`, and explicit later authorization before sample ingest.

## 15. Recommended next Codex task

Suggested task:

```text
CG-RECD_VARW_CSV_CONTRACT_LOCK_SPEC
```

Scope:

- Write a versioned CSV contract spec for the six VARW outputs.
- Do not change writers yet.
- Define canonical field names, required/optional columns, enum sets, and backward-compatible aliases.
- Include migration notes for `source_audio -> source_raw_audio/source_split_audio`, `take_id -> recording_take_no`, and `variant -> realization_variant`.

Only after that spec is accepted should a separate implementation task update CSV writers and tests.

## 16. Explicit no-execution statement

No split audio was created.  
No `03_samples/` file was written.  
No `sample_assets.csv` was written.  
No `recording_segments.csv` was written.  
No render was executed.  
No ML training data was created.  
No source code was modified for this audit.

## Findings index

| ID | Severity | Summary |
| --- | --- | --- |
| F01 | BLOCKER | R1 lacks explicit `recording_take_no` |
| F02 | BLOCKER | R1 lacks explicit `source_split_audio` |
| F03 | BLOCKER | R1 sample gate lacks `gesture_id` / `script_id` |
| F04 | BLOCKER | R1 QC lacks reviewer/human acceptance fields |
| F05 | MAJOR | Primary outputs lack session/person/piece identity |
| F06 | MAJOR | R0 split plan lacks score/gesture keys |
| F07 | MAJOR | R0 split boundaries need explicit semantic columns |
| F08 | MAJOR | R1 `variant` vs `realization_variant` is ambiguous |
| F09 | MAJOR | R1 anchor type enum not locked for future context values |
| F10 | MAJOR | R1 CSVs lack `not_ml_training_data` |
| F11 | MAJOR | R0 take-number fallbacks need upstream normalization guarantee |
| F12 | MINOR | R0 `unit_status` / `review_status` enum families differ |
| F13 | MINOR | Chinese labels are safe only in label columns |
| F14 | MINOR | `updated_at` is export time, not human review time |
| F15 | MINOR | R1 exports booleans but no explicit `segment_status` CSV column |
| F16 | MINOR | R0 marker audit lacks `batch_take_no` |
| F17 | INFO | R0/R1 preview panels show subsets, backend writers define actual CSVs |
| F18 | INFO | `raw_marker_review.csv` should remain provenance-only |
| F19 | INFO | `split_marker_review.csv` should remain provenance-only |
| F20 | INFO | Current CSV status values are internal values, not UI Chinese labels |
