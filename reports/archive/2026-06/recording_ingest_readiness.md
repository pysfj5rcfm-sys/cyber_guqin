# Recording Sample Ingest Readiness Audit

Scope: Phase 1B-R0 read-only audit. This report does not import audio, create slices, alter runtime data, patch V1, or generate enriched recording items.

Validator handling: several existing validators write fixed files under reports/. To keep this audit from rewriting unrelated report artifacts, run those validators in a temporary workspace copy and record their command results in the execution summary.

## 1. Executive Summary

Readiness status: warning. The 71-task recording checklist is usable as the real recording execution source, but the system should not start slicing or sample_assets ingest until session and take manifests are added and the real segment schema is extended.

Direct answers:

- Can start recording now: yes, with a session manifest decision pass before the first take.
- Can start slicing now: no; add take manifest and recording_segments provenance fields first.
- Can write sample_assets now: no; real samples should enter through segments and QC first.
- Need V1 minimal patch now: yes as a recommendation, not in this audit. The patch should target manifests/segment fields/sample-set selection.
- Need recording_items_enriched now: no. Reserve it for a future semantic bridge after the recording archive is stable.
- Prefer session manifest before slicing: yes.
- Prefer manual or semi-auto slicing first: yes.
- Preserve raw audio permanently read-only: yes.
- Keep dummy and real samples together: yes, separated by source_type and sample set.
- Let context samples drive first render: not yet; keep them for training/reference and special left-hand-sound cases until selection policy is explicit.
- Pilot first: yes, ingest a small real batch before processing all 71 tasks.
- Archive all 71 raw takes before slicing: yes, even if slicing starts with a pilot subset.

## 2. Readiness Status

Status: warning. Existing files support recording-day execution, but not lossless real sample ingest. This is a warning state rather than pass because field-level provenance is incomplete for recording sessions, take boundaries, segment QC, and sample-set selection.

## 3. Current V1 Recording / Sample Structure Overview

- score_events.csv: 51 score facts.
- gesture_templates.csv: 29 templates.
- gesture_components.csv: 31 components.
- recording_script.csv: 71 structured recording tasks.
- recording_script_human.csv: 71 human-facing tasks.
- recording_sessions.csv: 0 rows and columns ['recording_id', 'qinist_id', 'piece_id', 'qin_id', 'tuning_id', 'date', 'status', 'notes'].
- recording_segments.csv: 0 rows and columns ['segment_id', 'recording_id', 'event_id', 'start_time', 'end_time', 'status', 'notes'].
- sample_assets.csv: 82 rows, source types {'dummy': 82}, sample types {'atomic': 81, 'context': 1}.
- 02_recordings/raw_audio is absent, which is expected before real recording but means archive layout is not yet materialized.

## 4. 71 Recording Task Check Results

- Total takes: 71.
- Atomic takes: 69.
- Context takes: 2.
- Variants: atomic, chuo, context, straight, zhu.
- script_id, recording_take_no, batch_take_no, event_id, gesture_id, expected_sample_type, realization_variant, and realization_pre_action are present in the human script.
- Key instructions are preserved for 上滑至七徽九分, 大注九勾四撞, 掐起 context, and 撞到掐起 context.
- Context rows missing event_range: 1. This is acceptable for recording-day reading, but not for slicing or ingest.
- recording_take_no should be the stable whole-session take number. batch_take_no should remain the performer-facing order inside grouped batches. Neither should overwrite event_no or score order.
- Main risk: recording_batches.md is an execution order view and must not be treated as score authority.

## 5. Raw Audio Archive Recommendation

Recommended structure, not created in this audit:

```text
02_recordings/
├── recording_sessions.csv
└── raw_audio/
    └── QINIST_001/
        └── XWC/
            └── RS_XWC_001/
                ├── raw/
                ├── normalized/
                ├── session_manifest.yaml
                ├── take_manifest.csv
                └── notes.md
```

- Recommended mode: record either batch-level continuous WAVs or 71 per-take WAVs. Batch-level continuous WAVs are usually safer for performance flow if every take boundary is captured in take_manifest.
- If continuous: preserve take_start_time and take_end_time for each script_id, plus spoken slate policy.
- If 71 files: use names like RS_XWC_001_TK001_RS_XWC_001_001_straight.wav and append _retake02 for retakes.
- Preserve original raw files untouched forever; create normalized copies separately.
- Recommended normalized format: WAV, 48 kHz or 44.1 kHz, 24-bit preferred for capture if available, mono if using one microphone and stereo only if placement is intentional.
- Include recording environment metadata: room, noise note, recorder, microphone, interface, qin condition, tuning note, and reference tone/noise samples.

## 6. Recording Session Manifest Recommendation

Recommended fields:

- recording_session_id
- qinist_id
- qin_id
- tuning_id
- piece_id
- recording_id
- date
- location
- recorder
- microphone
- audio_interface
- sample_rate
- bit_depth
- channel_count
- file_format
- room_noise_note
- qin_condition_note
- recording_mode
- source_raw_files
- linked_recording_script
- notes

Current recording_sessions.csv is only a high-level placeholder. Fields that must be fixed before recording are recording_session_id, recording_mode, sample_rate, bit_depth, channel_count, file_format, source_raw_files, and linked_recording_script. Location/equipment notes can be partly backfilled, but it is safer to capture them at the session.

## 7. Take Manifest Recommendation

A take manifest is needed before slicing. Prefer colocating it with the raw session folder, e.g. 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001/take_manifest.csv, because it travels with the raw archive.

Recommended fields:

- recording_session_id
- recording_id
- recording_take_no
- batch_take_no
- script_id
- event_id
- event_range
- gesture_id
- normalized_name
- expected_sample_type
- realization_variant
- source_raw_file
- take_start_time
- take_end_time
- take_quality
- performer_note
- engineer_note
- needs_reshoot
- selected_for_sample
- notes

- Convert the 71 recording tasks into expected takes before or immediately after recording.
- A take may map to multiple events via event_range, especially context takes.
- Bad takes and retakes should remain in the manifest with take_quality, needs_reshoot, and selected_for_sample.
- Keep take_no and script_id together: take_no tracks physical recording order; script_id tracks intended semantic task.

## 8. recording_segments.csv Field Gaps

Current fields: ['segment_id', 'recording_id', 'event_id', 'start_time', 'end_time', 'status', 'notes']. This is insufficient for real audio slicing.

Recommended fields:

- segment_id
- recording_session_id
- recording_id
- source_raw_file
- source_take_id
- script_id
- event_id
- event_range
- gesture_id
- sample_type
- realization_variant
- start_time_s
- end_time_s
- attack_marker_ms
- release_tail_ms
- file_path
- extraction_method
- qc_status
- notes

- Keep both source_take_id and event_id/event_range so a segment can be traced to raw audio and score semantics.
- Context samples require event_range.
- straight/chuo/zhu belongs in realization_variant or realization_pre_action, not in score facts.
- attack_marker_ms should be manually checked at first; release_tail_ms should be retained for natural decay.
- Distinguish take segments from final samples: recording_segments is source evidence; sample_assets is promoted usable material.

## 9. sample_assets.csv Field Gaps

Current source types: {'dummy': 82}. Current quality statuses: {'good': 82}.

- Dummy and real samples should coexist through source_type=dummy and source_type=real_recording.
- Existing source_recording_id/source_segment_id/source_event_id/source_event_range fields are a good start, but real rows need populated source_segment_id.
- realization_variant and realization_pre_action already exist and should carry straight/chuo/zhu realization facts.
- sample_type covers atomic/context, but context should not automatically enter first-version render without policy.
- Add sample_version and selected_sample_set/active_sample_set concepts before real render selection.
- Preserve multiple takes in sample_assets or a linked segment table; do not overwrite earlier takes when choosing active samples.

## 10. straight / chuo / zhu / context Take Handling

- straight: direct baseline realization, useful as fallback and comparison.
- chuo: Sanman default for unmarked pressed notes; keep as realization_pre_action=chuo, never as score notation unless explicitly marked.
- zhu: use for score-marked 注 and prioritize it when notation_pre_action=zhu.
- context: record as independent evidence, especially for 掐起 and 撞到掐起 transitions. Promote only after event_range and selection policy are explicit.
- default_chuo/no_chuo should remain realization/sample-selection concepts, separated from score_events.

## 11. Split Workflow Recommendation

- 05_scripts/ is appropriate for future V1 runtime pipeline scripts that transform real recording data into V1 sample tables.
- scripts/ should remain for audits, validators, canon utilities, and read-only checks.
- Future split_recording_session.py is useful, but should be created after manifests are agreed.
- Start with manual or semi-auto split using Audacity/Reaper timestamp exports.
- Support both long WAV + take_manifest and per-take WAV registration.
- Suggested future scripts: 05_scripts/split_recording_session.py, 05_scripts/ingest_recording_segments.py, 05_scripts/promote_segments_to_samples.py.

## 12. Dapu Event IR / Skills Bridge Recommendation

- recording ingest should not depend on dapu-parser for raw audio archiving.
- score facts come from score_events.csv and gesture templates/components.
- performance realization comes from realization_variant, realization_pre_action, qinist profile, and sample selection policy.
- recording execution comes from recording_script, human checklist, take manifest, and session manifest.
- canon evidence comes from canon files and validators, not from recording_batches.md.
- Future recording_items_enriched.jsonl can bridge script rows to Dapu Event IR, but should not be created before real archive/segment provenance is stable.

## 13. Real Sample QC Recommendation

- Check WAV exists and is non-empty.
- Check sample_rate, bit_depth, channel count, and file format consistency.
- Check clipping and excessive silence head/tail.
- Require attack_marker_ms for promoted samples.
- Record release_tail_ms and ensure decay is long enough.
- Check duration range by sample_type.
- Ensure context sample covers the full event_range.
- Track repeated takes separately.
- Use quality_status values: good, usable, needs_review, reject.

## 14. Render With Real Samples Recommendation

- render_audio.py currently works against sample_assets and dummy WAV assumptions; it can continue after real rows exist if sample format matches.
- Add source_type preference so real_recording is preferred while dummy remains fallback.
- Rotate among multiple good takes per gesture to avoid immediate repetition.
- Include realization_variant and realization_pre_action in selection.
- Context samples should be excluded from ordinary render until policy specifies when to use them.
- Add a sample_set selector before replacing dummy-first behavior.

## 15. Do Not Immediately Execute

- real audio slices
- recording_items_enriched.jsonl
- recording ingest data rows
- V1 patch scripts
- machine learning training scripts
- OCR pipeline outputs
- new canon drafts
- real sample_assets rows
- real recording_segments rows

## 16. Next Phase 1B Order

1. Phase 1B-1: decide session manifest and recording format.
2. Phase 1B-2: archive raw audio and create take manifest.
3. Phase 1B-3: manually or semi-automatically split a small pilot batch.
4. Phase 1B-4: QC segments, mark attack/tail/quality.
5. Phase 1B-5: promote good segments into real sample_assets and sample set.
6. Phase 1B-6: render with real samples and review by listening.
