# Recording Ingest Schema

## Purpose

This document defines the reusable recording asset model for Cyber Guqin v1. It is a schema and provenance guide, not a real recording session and not an ingest record. It prepares the path from raw human recording to reviewed sample assets while keeping score facts, performance realization, recording execution, and audio provenance separate.

## Long-Term Reusable Recording Asset Model

The long-term model has four main layers:

1. `session_manifest`: session-level recording facts such as performer, qin, tuning, room, equipment, audio format, raw audio policy, source script, and linked notes.
2. `take_manifest`: expected and actual take boundaries. It connects a physical take to the script row it was meant to satisfy.
3. `recording_segments`: cut evidence from a take. Segments preserve raw source, time range, attack marker, release tail, QC state, and score/script references.
4. `sample_assets`: renderable samples promoted from reviewed segments. Real samples should coexist with dummy samples through `source_type`, provenance fields, and later sample-set selection.

A future render sample set should choose which dummy and real samples are active for a render. That selection policy is separate from raw ingest.

## Legacy XWC Bridge Note

`RS_XWC_001` for `XWC / 仙翁操` is a legacy recording session source. Its 71 recording tasks were produced in v1.0 Phase 1A as `recording_script.csv`, `recording_script_human.csv`, `recording_script_human.md`, and `recording_batches.md`.

For this one recording session, those files remain the authority for what to play. The bridge maps them to the reusable asset model. Future pieces should use a Dapu Event IR / canon-backed parser to generate standard recording plans and should not depend on `recording_batches.md`.

## Data Layers

### session_manifest

`session_manifest` records facts about one recording session. It records who played, which qin and tuning were used, recording mode, equipment, audio format, room notes, room noise references, raw audio folders, normalized-copy policy, linked script files, and session notes.

It does not record score truth. It should never patch `score_events.csv`.

### take_manifest

`take_manifest` records expected and actual takes. A take may be a single task, a retake, or a context performance that spans multiple events. For XWC, the expected take rows can be previewed from legacy scripts, but the real take manifest should be created only after recording mode and session settings are confirmed.

`recording_take_no` is the stable whole-session take number. `batch_take_no` is the performer-facing order inside the recording-day batches. `script_id` is the semantic recording task ID. `event_id` and `event_range` are score references, not physical take order.

### recording_segments

`recording_segments` is the slicing evidence layer. A segment is cut from a take or raw file and keeps time boundaries, source take, source raw file, score/script references, attack marker, release tail, extraction method, QC status, and quality status.

Do not write `sample_assets` directly from raw audio. Create or review segments first.

Context segments must preserve `event_range`. `straight`, `chuo`, and `zhu` are realization choices, not score facts.

### sample_assets

`sample_assets` is the renderable sample layer. A real row should use `source_type=real_recording`, must include `source_segment_id`, must include `quality_status`, must include `attack_marker_ms`, and should include `release_tail_ms` or the existing tail equivalent. Dummy rows and real rows should coexist.

Segment to sample promotion should require:

- a valid source segment;
- acceptable QC and `quality_status`;
- checked attack marker;
- preserved release tail;
- clear `realization_variant` and `realization_pre_action`;
- source event or event range provenance;
- a later selected sample set / active sample set decision before render selection.

### render sample set

A render sample set is the policy layer that chooses which sample asset is active for a render. This is not created in Phase 1B-1. The later design should allow dummy fallback and real recordings to coexist.

## Separation of Facts

- Score facts: `score_events.csv`, Dapu Event IR, and canon-backed parser output. These define notation facts such as event ID, gesture ID, and score-marked pre-action.
- Performance realization: `realization_variant`, `realization_pre_action`, and performer style decisions such as Sanman default `chuo`.
- Recording execution: batch order, take number, slate, retake status, raw file, and take boundaries.
- Audio provenance: raw file, normalized copy, source take, source segment, start/end time, attack marker, release tail, extraction method, and QC status.
- Canon evidence: canon rules, ontology, aliases, and validation evidence. Recording batches are not canon evidence.

## Field Semantics

- `internal_name`: the standard internal name of the entry itself. For example, a sound-type entry may use `sound_type_an`, `sound_type_san`, or `sound_type_fan` as its own `internal_name`.
- `mapped_component_name`: the ontology component / technique / action that this entry maps to. For example, `sound_type_an` maps to `pressed_pluck`, `sound_type_san` maps to `single_pluck`, and `sound_type_fan` maps to `harmonic_pluck`.

`internal_name` and `mapped_component_name` must not be assumed equal. Validators should compare `manifest.internal_name` with `draft.internal_name`, not with `draft.mapped_component_name`.
- `recording_take_no`: stable whole-session take number.
- `batch_take_no`: performer-facing batch order. It is not event order and not score order.
- `script_id`: semantic recording task ID from a recording plan or legacy script.
- `event_id`: single score event reference.
- `event_range`: multi-event score reference for context takes or context segments. Context rows must keep it before slicing or sample promotion.
- `realization_variant`: sample realization class such as `straight`, `chuo`, `zhu`, `context`, or another later reviewed value.
- `realization_pre_action`: performed pre-action such as `none`, `chuo`, or `zhu`. Sanman default `chuo` belongs here or in sample selection policy, not in score facts.
- `source_take_id`: take-level provenance linking a segment to the take manifest.
- `source_segment_id`: sample-level provenance linking a promoted sample to the reviewed segment.

## Legacy Policy

`recording_batches.md` is an execution view. It is useful on recording day because it answers what to play and in what performer-facing order. It is not a future standard data source and must not reverse-overwrite `score_events.csv`.

XWC `RS_XWC_001` needs a one-time bridge from the old 71 recording tasks to the reusable `session_manifest`, `take_manifest`, and `recording_segments` model. Future pieces should use Dapu Event IR / canon-backed parser output to generate standard recording plans.

## Do-Not-Do List

- Do not treat recording order as score order.
- Do not write Sanman default `chuo` back into score events.
- Do not use a context take as a direct replacement for an atomic sample unless a later selection policy says so.
- Do not write `sample_assets` directly from raw audio.
- Do not overwrite dummy samples.
- Do not delete bad takes.
- Do not cut or rename raw audio masters.
- Do not treat `recording_batches.md` as canon evidence or future source of truth.
