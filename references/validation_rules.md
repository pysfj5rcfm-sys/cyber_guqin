# Validation Rules

These rules are hard checks for Phase S0 validators and future skill users.

1. `primary_sound_type` may only be `散音`, `按音`, `泛音`, or `none` for canon techniques. Dapu event IR uses only `散音`, `按音`, or `泛音`.
2. `component_sound_type` may only be `散音`, `按音`, `泛音`, or `none`.
3. Complex techniques must not be encoded as a fourth `sound_type`; use `sound_profile`, `gesture_family`, and `gesture_components`.
4. `撞` must be `micro_returning_slide`.
5. `反撞` must be `micro_returning_slide`.
6. `进复` and `退复` must not be split into `进+复` or `退+复`.
7. `掐起` must be `left_hand_sound`.
8. `撮` must be `simultaneous_pluck`.
9. `放合` and `应合` must be `open_pressed_harmony`.
10. `分开` must not be `open_pressed_harmony`.
11. `分开` must be `compound_both_hands` with `sound_profile=compound_pressed_motion`.
12. If the score does not explicitly show `绰`, do not auto-fill `notation_pre_action=chuo`; Sanman default `绰` belongs to realization.
13. OCR candidates must not be `verified`.
14. Omitted tokens that depend on missing inherited string, position, or right-hand sources must set `needs_review=true`.

Additional V1.1 checks:

- `吟` and `猱` belong to vibrato. Explicit notation maps to `notation_vibrato=yin`, `nao`, or `yin_nao`; default vibrato belongs to realization.
- `撞` and `反撞` must not use a `percussive` field.
- `分开` components are `mo_attack`, `shang_motion`, and `zhu_tiao_return_attack`; `zhu_tiao_return_attack` already includes return direction, so no extra `下` component is added.
