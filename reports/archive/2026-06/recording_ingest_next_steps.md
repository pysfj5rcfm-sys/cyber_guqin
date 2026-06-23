# Recording Ingest Next Steps

Scope: Phase 1B route after the read-only readiness audit. Do not treat this file as recording ingest data.

## Phase 1B-1: Recording Session Metadata

Goal: establish session_manifest template and lock the recording mode before audio enters the repository.

- Inputs: recording_script_human.csv, recording_batches.md, qinist/qin/tuning IDs, chosen recorder settings.
- Outputs: approved session_manifest template and agreed file naming policy.
- Modifies data: yes, future manifest only; no audio slicing.
- Human confirmation: required for recording_mode, sample_rate, bit_depth, channel count, room, qin, and tuning.

## Phase 1B-2: Raw Audio Archive

Goal: put true recordings into raw audio storage while preserving originals.

- Inputs: raw WAV files, session_manifest, 71-task checklist.
- Outputs: raw/ originals, normalized/ copies if needed, take_manifest.csv.
- Modifies data: yes, raw archive and take manifest; no sample_assets rows.
- Human confirmation: required for take boundary policy, slate policy, retake naming, and selected recording session ID.

## Phase 1B-3: Manual / Semi-auto Split

Goal: cut source audio into recording_segments using take_manifest and recording_script references.

- Inputs: raw or normalized WAV, take_manifest, recording_script.csv, optional Audacity/Reaper timestamp export.
- Outputs: candidate segment files and recording_segments rows.
- Modifies data: yes, future segment files/table only after schema patch.
- Human confirmation: required for context event_range and ambiguous take boundaries.

## Phase 1B-4: Segment QC

Goal: verify each segment before it becomes a renderable sample.

- Inputs: recording_segments, segment audio, session manifest.
- Outputs: qc_status, attack_marker_ms, release_tail_ms, quality_status, selected_for_sample decisions.
- Modifies data: yes, segment QC metadata.
- Human confirmation: required for borderline tone quality, clipping, noisy room, wrong attack, and reshoot decisions.

## Phase 1B-5: Promote to Sample Assets

Goal: generate real sample_assets rows from good segments while keeping dummy fallback.

- Inputs: good/usable recording_segments, sample selection policy, existing sample_assets schema.
- Outputs: real_recording sample_assets rows and a selected sample set.
- Modifies data: yes, sample_assets and possibly sample set metadata after a V1 minimal patch.
- Human confirmation: required for active sample set and multiple-take choice.

## Phase 1B-6: Render With Real Samples

Goal: render the first real-sample Sanman Xianwengcao candidate.

- Inputs: active real sample set, dummy fallback, rhythm candidates, render_audio.py selection rules.
- Outputs: first real-sample render and listening review notes.
- Modifies data: yes, render outputs only.
- Human confirmation: required for whether context samples participate and whether dummy fallback remains audible.

Recommended first pilot: choose a small subset that includes one straight, one chuo, one zhu, and one context transition before processing all 71 tasks.
