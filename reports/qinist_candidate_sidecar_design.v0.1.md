# Qinist Candidate Sidecar Design v0.1

状态：sidecar design only。不是 sample ingest。

## 1. Boundary

Hard separation:

```text
score facts != qinist realization
candidate sidecar != sample ingest
ML-ready != ML training
human accepted != sample asset created
```

This task does not write:

```text
sample_assets.csv
recording_segments.csv
recording_items_enriched.jsonl
```

## 2. Purpose

The sidecar records candidate evidence for future digital qinist learning without promoting any row into production sample data.

It should link:

- score/Dapu event identity
- source take provenance
- R0/R1/R2 review evidence
- human listening labels
- qinist realization fields
- exclusion flags

## 3. Field Groups

### Identity

- `candidate_id`: proposed extension, because `sample_id` belongs to sample ingest.
- `qinist_id`: existing.
- `piece_id` / `work_id`: existing.
- `score_event_id` mapped to `event_id`: documented.
- `gesture_event_id`: documented, not repo-frozen.

### Provenance

- `recording_session_id` / `session_id`
- `recording_id`
- `recording_take_no`
- `source_take_id`
- `segment_id`
- `source_raw_audio`
- `source_split_audio`
- `audio_segment_ref`

### Score Facts

- `primary_sound_type`
- `gesture_family`
- `gesture_id`
- `components`
- `notation_pre_action`
- `notation_vibrato`
- `context_dependency`

### Qinist Realization

- `realization_variant`
- `realization_pre_action`
- `realization_vibrato`
- `tail_policy`
- future tempo/dynamic fields only as proposed extensions if needed

### Review Labels

- R0: marker/review status and source_raw provenance
- R1: `segment_status`, `human_accepted`, `wrong_take`, `reviewed_by`, `reviewed_at`
- R2: `preferred_version_id`, `issue_type`, `severity`, `comment`, `suggested_revision`

### Exclusion

- `is_wrong_take`
- `is_failed_take`
- `is_context_only`
- `exclusion_reason`

No exclusion field may be silently inferred from Baiya/Sanman identity.

## 4. Candidate Status

Suggested draft values:

```text
candidate
hold
reject
```

`candidate_status` is documented in the ML roadmap, but implementation still requires a future schema gate.

## 5. Safety Flags

Every sidecar row must carry:

```text
review_only=true
production_grade=false
not_sample_assets=true
not_recording_segments=true
not_recording_items_enriched=true
not_ml_training_data=true
```

`not_recording_items_enriched` is a proposed extension safety flag because the hard red line names that file explicitly.

