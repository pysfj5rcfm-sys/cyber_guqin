# QXBY Component Atlas Reference v0.1

Status labels: `QXBY_COMPONENT_ATLAS_REFERENCE`, `USER_REVIEWED_COMPONENT_LABELS`, `SOURCE_REFERENCE_KNOWLEDGE`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.

This directory stores repo-local reference knowledge for the user-reviewed QXBY / 《琴学备要》 component set used across LXY P1-P4.

It is a component atlas reference only. It is not a score import, not canon authority, not Dapu IR authority, not sample ingest, not ML training data, not render output, and not a recording plan.

## Files

- `component_registry.v0.1.json`: structured registry for `COMP-001..030` and reusable construction templates.
- `component_registry.v0.1.md`: human-readable summary of the same registry.

No PNG or ZIP binary assets are copied into this repository by this task.

## Authority Boundary

The registry may be used as reference authority for:

- component labels,
- component categories,
- visual slot semantics,
- construction-template hints,
- QXBY / user-review provenance.

The registry must not be used as authority for:

- final phrase score facts,
- Dapu Event IR,
- sample ingest,
- ML training data,
- render or recording-plan outputs,
- R0/R1/R2/E/F workflow state.

New LXY phrase readings remain `LXY_TRANSCRIPTION_DRAFT` and `NEEDS_HUMAN_REVIEW`.

## Source Provenance

- `/Users/chenyulin/Downloads/basic_components_named_v0.2.zip`
  - SHA-256: `ac4330df2c5d8b234d6cdb16ab9141692faf7553ab599391047b7a6a4a9817ac`
  - Components: `COMP-001..020`
- `/Users/chenyulin/Downloads/basic_components_named_v0.3.zip`
  - SHA-256: `77bf5daaffeb9a1c7b0dab6241a2d89ca0bd20cff0c0e73c9070fbaac34c50b5`
  - Components: `COMP-021..027`
- `/Users/chenyulin/Downloads/basic_components_named_v0.4.zip`
  - SHA-256: `569a74b0d644be8c4bef0a90c44dec19fed9f9073de2c0d8524afb76f4e1cc31`
  - Components: `COMP-028..030`

The v0.4 correction is preserved:

- `COMP-028 = 撞 / 左手取音`
- `COMP-029 = 轮 / 右手指法`
- `COMP-030 = 急 / 节奏谱字`

Do not use earlier wrong raw mappings such as `raw_001=轮` or `raw_003=撞`.

## Read Order For Component-Guided Transcription

For P5 and later LXY phrase crops, the component-guided transcription skill should read:

1. `references/qxby_component_atlas/component_registry.v0.1.json`
2. approved QXBY / v0.3.1 reports
3. prior LXY phrase reports as transcription-draft template evidence

Any candidate phrase reading produced from this atlas must remain report-only and human-reviewable.
