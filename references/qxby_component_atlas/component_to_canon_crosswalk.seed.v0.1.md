# QXBY Component To Canon Crosswalk Seed v0.1

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `SOURCE_REFERENCE_IMAGE`, `USER_PROVIDED_QXBY_COMPONENT_SET`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`

This file is a seed crosswalk only. Every entry is `seed_pending`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, and `NOT_RENDER_OUTPUT`.

## Summary

- Entries: `174`
- Canon authority: `false`
- Score-event authority: `false`
- Dapu IR authority: `false`

## Coarse Role Guesses

| Category | Semantic role guess | Sound policy guess |
| --- | --- | --- |
| 节奏谱字 | timing_or_punctuation_marker_candidate | timing_or_punctuation_policy_needs_canon_builder_review |
| 通用谱字 | generic_score_marker_candidate | generic_marker_policy_needs_canon_builder_review |
| 音位谱字 | sound_position_or_state_marker_candidate | sound_position_or_state_policy_needs_canon_builder_review |
| 右手指法-两弦双弹 | right_hand_action_candidate | right_hand_action_sound_policy_needs_canon_builder_review |
| 右手指法-数弦连弹 | right_hand_action_candidate | right_hand_action_sound_policy_needs_canon_builder_review |
| 右手指法-一弦单弹 | right_hand_action_candidate | right_hand_action_sound_policy_needs_canon_builder_review |
| 左手指法-本位取音 | left_hand_action_or_position_candidate | left_hand_action_or_position_sound_policy_needs_canon_builder_review |
| 左手指法-隔位取音 | left_hand_action_or_position_candidate | left_hand_action_or_position_sound_policy_needs_canon_builder_review |
| 左手指法-散弦取音 | left_hand_action_or_position_candidate | left_hand_action_or_position_sound_policy_needs_canon_builder_review |

## Review Rule

Do not over-infer gesture family, sound policy, event semantics, or parser fields from this seed. Canon-builder review must approve any final canon linkage.
