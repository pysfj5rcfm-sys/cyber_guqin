# Normalization Rules

These rules follow Gesture Ontology v1.1 and are intended for Phase S0 fixtures and validators only.

1. `bo=擘`; `pi` and `劈` are aliases to `bo`, not standard internal names.
2. `po=泼`, `la=剌`, `po_la=泼剌`.
3. `拨` and `撥` are aliases to `泼`.
4. `拨剌` and `撥剌` are aliases to `泼剌`.
5. `yan=罨`; `掩` is an alias to `罨`.
6. Score facts and realization must remain separate: explicit `绰` maps to `notation_pre_action=chuo`; explicit `注` maps to `notation_pre_action=zhu`; Sanman defaults belong to realization or sample selection.
7. `上`, `下`, `进复`, `退复`, `撞`, and `反撞` enter `components`; `进复` and `退复` remain atomic.
8. `分开` does not belong to `open_pressed_harmony`.
9. `放合` and `应合` belong to `open_pressed_harmony`.
10. OCR candidates must not be marked `verified`; they require `source_status=ocr_candidate` and `needs_review=true`.
