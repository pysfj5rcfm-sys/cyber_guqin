# High-Frequency Gesture Array Extraction Design v0.1

状态：设计稿。不是采集清单执行文件。

## 1. Goal

从单曲 Dapu IR 和 canon/gesture tables 中提取 high-frequency fingering / gesture arrays，用于 starter kit priority 设计。

## 2. Sound-Type Principles

硬规则：

- `primary_sound_type` 只允许 `散音` / `按音` / `泛音`。
- 撮、掐起、泼剌、掐撮三声等特殊技法必须保留在 `gesture_family` / `sound_profile` / `components` / `special_technique` 等结构中。
- `绰` / `注` 是 pre-sound actions：score-marked 时进入 `notation_pre_action`，Sanman default 只能进入 realization。
- `上` / `下` 是 post-sound actions：进入 post-motion components。
- Score facts 与 qinist realization 分离。

## 3. 散音 Extraction

散音 comparatively clean，可偏向 full coverage：

- Group by `primary_sound_type=散音`.
- Within each group, count `gesture_family`, `gesture_id`, right-hand `component_name`, `string_no`.
- P0 candidate if:
  - single-pluck/right-hand action is unambiguous
  - no inherited position ambiguity
  - no context dependency
  - no unresolved `needs_review`
- P1/P2 if:
  - phrase transition or long-tail needs are present
  - the event is clean but review confidence is low

## 4. 泛音 Extraction

泛音也 comparatively clean，但需要验证 hui point:

- Group by `primary_sound_type=泛音`.
- Validate `hui` / harmonic role / `gesture_family=harmonic_pluck` or `simultaneous_pluck`.
- P0/P1 candidate if harmonic point and string are explicit.
- P2/P3 if simultaneous harmonic or compound gesture requires component validation.

## 5. 按音 Extraction

按音不能 blindly full-covered。按音必须先做结构验证。

Pressed-sound validation dimensions:

| Dimension | Required source |
| --- | --- |
| base pressed sound | `primary_sound_type=按音`, `gesture_family=pressed_pluck` or related |
| string | `string_no` or mapped `string` |
| hui position | `hui`, `hui_target`, or mapped `hui_position` |
| left finger | `primary_left_finger` or component-level left-hand evidence |
| right action | `primary_right_action` or component-level `component_name` |
| pre-action | `notation_pre_action` for score facts; `realization_pre_action` for qinist realization |
| post-action | post-motion components: `上`, `下`, `进复`, `退复`, `撞`, `反撞` |
| vibrato | `notation_vibrato` vs `realization_vibrato` |
| context | `context_dependency`, `requires_context_sample`, `needs_context_take` |
| tail policy | `needs_long_tail`, `tail_policy=full_tail` |

Validation outcomes:

- `structure_ok_atomic`: can enter P0/P1 atomic candidate.
- `structure_ok_context`: must be context sample.
- `structure_validation_required`: missing position/motion/component evidence.
- `needs_human_decision`: phrase semantics or qinist realization ambiguity.
- `do_not_use_as_atomic`: context-only, phrase transition, or diagnostic sample.

## 6. Priority Guidance

- P0: 散音 high-frequency right-hand plucks; stable 泛音; clean atomic fields.
- P1: common pressed plucks and common score-marked `绰` / `注` / `上` / `下` when structure validates.
- P2: context transitions, left-hand sound, yin/nao, post-motion chains.
- P3: long-tail/full-tail diagnostics, phrase-specific tails, rare compounds.
- SKIP: low-value, ambiguous, unsafe, or only Baiya-reference data.

## 7. Why Existing Fields Are Insufficient Alone

`gesture_id` alone is insufficient because the ontology explicitly avoids storing everything as one gesture string. `primary_sound_type=按音` alone is insufficient because pressed sounds can include position shift, post-motion, virtual/weak pre-action, vibrato, context dependencies, and tail policies. The extraction must preserve the component structure.

