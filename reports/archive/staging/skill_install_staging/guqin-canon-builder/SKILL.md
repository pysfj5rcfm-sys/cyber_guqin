---
name: guqin-canon-builder
description: Use when processing guqin rule-book text, fingering explanations, aliases, gesture families, component lexicons, or canon validation for Cyber Guqin without parsing concrete score events or modifying V1 runtime data.
---

# Guqin Canon Builder

## Position

`guqin-canon-builder` is the rule-book processing skill for Cyber Guqin. It converts guqin rule-book material, fingering explanations, jianzipu notation explanations, gesture descriptions, and terminology notes into canon-ready knowledge structures.

It is a canon rule builder. It is not a concrete score-event parser.

## Inputs

Accept:

- Rule-book OCR text
- Manual excerpts
- Single fingering explanations
- Page and source references
- Human descriptions of image pages
- Glossaries
- Traditional notation explanations
- Left-hand and right-hand technique descriptions
- Dapu rule descriptions

## Outputs

Future traditional-textbook view:

- `canon/sources.yaml`
- `canon/terms.yaml`
- `canon/right_hand_techniques.yaml`
- `canon/left_hand_techniques.yaml`
- `canon/special_techniques.yaml`
- `canon/gesture_templates.yaml`
- `canon/dapu_rules.yaml`
- `references/normalization_rules.md`
- `references/validation_rules.md`

Future Cyber Guqin ontology view:

- `canon/component_lexicon.yaml`
- `canon/gesture_families.yaml`
- `canon/alias_rules.yaml`
- `canon/technique_rules.yaml`
- `canon/validation_rules.yaml`

Phase S0 creates only minimal fixtures and validation scaffolding. Do not import formal `琴学备要` or other full canon data in this phase.

## Strict Boundaries

Do not:

- Parse concrete score events
- Generate Xianwengcao events
- Generate `score_events`
- Modify `recording_batches.md`
- Generate Sanman performance candidates
- Generate audio
- Modify V1 runtime
- Modify V1 running tables
- Overwrite `00_global/guqin_fingering_ontology.yaml`
- Modify ontology, score events, gesture templates, gesture components, sample assets, recording scripts, renderer, smoke tests, or recording task files
- Create recording script ingest
- Create `recording_items_enriched.jsonl`

This skill only answers:

- What does this term mean in principle?
- Which action component does this fingering belong to?
- Which `gesture_family` does this action belong to?
- How should this alias normalize?
- How does this rule map to Cyber Guqin fields?

## Authority

Read existing V1 authority files first when available:

- `00_global/guqin_fingering_ontology.yaml`
- `00_global/gesture_component_lexicon.csv`
- `00_global/gesture_family_catalog.csv`
- `00_global/alias_rules.yaml`
- `00_global/schema_contract.yaml`
- `00_global/sample_selection_policy.yaml`
- `06_docs/GESTURE_ONTOLOGY.md`

Gesture Ontology v1.1 is the final field authority. If older framework notes conflict with V1.1, follow V1.1.

## Core Ontology Rules

- `primary_sound_type` is only `散音`, `按音`, or `泛音`; canon techniques that do not directly sound may use `none`.
- `component_sound_type` is only `散音`, `按音`, `泛音`, or `none`.
- Do not create a fourth sound type.
- Express complex techniques through `sound_profile`, `gesture_family`, and `gesture_components`.
- Score facts and Sanman realization must remain separate.
- Sanman default `绰` and default light `吟猱` belong to `qinist_profile`, `interpretations`, `realization`, `sample_selection_policy`, or review layers.
- Score-unmarked `绰` must not be auto-filled as `notation_pre_action=chuo`.
- Score-marked `绰` maps to `notation_pre_action=chuo`.
- Score-marked `注` maps to `notation_pre_action=zhu`.
- Score-marked `吟`/`猱` maps to `notation_vibrato=yin`, `nao`, or `yin_nao`.

## Post-Attack Motion Rules

The following score-marked post-attack actions enter `gesture_components`:

- `上`
- `下`
- `进复`
- `退复`
- `撞`
- `反撞`
- `引上`
- `淌下`
- `往来`

Categories:

- `上`, `下`: `component_category=single_slide`
- `进复`, `退复`: `component_category=returning_slide`
- `撞`, `反撞`: `component_category=micro_returning_slide`

Hard rules:

- `进复` and `退复` are atomic; do not split them into `进+复` or `退+复`.
- `撞` and `反撞` are not `percussive`.
- Do not use a `percussive` field for `撞`, `反撞`, `吟`, or `猱`.

## Complex Technique Rules

- `撮`: `gesture_family=simultaneous_pluck`
- `掐起`: `gesture_family=left_hand_sound`
- `罨`: `gesture_family=left_hand_sound`
- `带起`: `gesture_family=left_hand_sound`
- `泼`: `gesture_family=right_hand_sequence`
- `剌`: `gesture_family=right_hand_sequence`
- `滚`: `gesture_family=right_hand_sequence`
- `拂`: `gesture_family=right_hand_sequence`
- `泼剌`: combination name with components `po + la`
- `滚拂`: combination name with components `gun + fu`
- `放合`: `gesture_family=open_pressed_harmony`
- `应合`: `gesture_family=open_pressed_harmony`
- `分开`: `gesture_family=compound_both_hands`, `sound_profile=compound_pressed_motion`
- `掐撮三声`: `gesture_family=compound_both_hands`

`分开` hard rules:

- `分开` is not `open_pressed_harmony`.
- `分开` is `compound_both_hands`.
- `分开` uses `sound_profile=compound_pressed_motion`.
- Components are `抹`, `上`, and `注挑回原音位`.
- `注挑回原音位` already contains the return-to-origin direction; do not add a separate `下`.

## Internal Naming Rules

- `bo = 擘`
- `pi` and `劈` are aliases of `bo`, not standard internal enum values.
- `po = 泼`
- `la = 剌`
- `po_la = 泼剌`
- `gun = 滚`
- `fu = 拂`
- `gun_fu = 滚拂`
- `yan = 罨`
- `掩` is an alias of `yan`.

Never create `拨` as an internal standard basic fingering. External `拨`, `撥`, `拨剌`, and `撥剌` map only to `泼` and `泼剌`.

## OCR And Review Status

OCR candidates are not `verified`.

- Default `source_status=ocr_candidate`
- Default `needs_review=true`
- Mark `verified` only after human confirmation
- Preserve ambiguous candidates
- Emit validation warnings for tokens or rules that cannot be uniquely normalized

## Workflow

1. Read V1 authority files.
2. Normalize aliases.
3. Assign `component_category`, `gesture_family`, and `sound_profile` according to V1.1.
4. Preserve source references, confidence, and review status.
5. Keep score facts separate from Sanman realization.
6. Validate against `references/normalization_rules.md`, `references/validation_rules.md`, and `scripts/validate_canon.py`.
