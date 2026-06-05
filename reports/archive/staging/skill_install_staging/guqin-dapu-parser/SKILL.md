---
name: guqin-dapu-parser
description: Use when parsing guqin jianzipu tokens, OCR candidates, manual score tokens, score-event projections, or read-only legacy recording scripts into Dapu Event IR while preserving Cyber Guqin V1 score facts.
---

# Guqin Dapu Parser

## Position

`guqin-dapu-parser` is the jianzipu parsing skill for Cyber Guqin. It parses concrete score tokens, OCR candidates, manually entered notation, existing score-event projections, and read-only legacy recording script projections into Dapu Event IR.

It is a score parser. It is not a rule-book extractor and not a Sanman realization engine.

## Inputs

Accept:

- Manually entered notation tokens
- OCR token candidates
- Dapu token sequences
- Known work, phrase, and position context
- Existing `score_events`
- Read-only `recording_batches.md`
- Read-only `recording_script_human.csv`
- Read-only legacy V1 recording scripts

## Parsing Chain

Use this chain:

```text
token
-> components
-> event_group
-> events
-> validation_report
```

Definitions:

- `token`: raw score input or OCR candidate
- `components`: internal action components inside a notation token
- `event_group`: the event group represented by one token or compound token
- `events`: structured facts mappable to V1 / Digital Qinist Core
- `validation_report`: parser and validator result

## Outputs

Future outputs may include:

- `corpus/<work>/tokens.jsonl`
- `corpus/<work>/components.jsonl`
- `corpus/<work>/events.jsonl`
- `corpus/<work>/recording_items_enriched.jsonl`
- `corpus/<work>/validation_report.json`

Phase S0 creates only minimal fixtures. Do not create formal corpus outputs and do not generate `recording_items_enriched.jsonl` in this phase.

## Strict Boundaries

Do not:

- Extract `琴学备要` rules
- Modify canon rule libraries
- Decide Sanman final performance style
- Generate audio
- Execute sample selection
- Modify current 71 recording tasks
- Refactor V1 runtime
- Reverse-overwrite `score_events.csv`
- Treat `recording_batches.md` as score authority
- Modify ontology, score events, gesture templates, gesture components, sample assets, recording scripts, renderer, smoke tests, or recording task files
- Create recording script ingest
- Create `recording_items_enriched.jsonl`

## Legacy Recording Script Rule

`recording_batches.md` is a recording execution file, not a score authority.

Future `recording_script_ingest` mode may read legacy recording files only for semantic enrichment, but must not:

- Modify `recording_batches.md`
- Reorder `recording_batches.md`
- Delete or merge recording tasks
- Reverse-overwrite `score_events.csv`
- Treat `recording_batches.md` as the original score source

Phase S0 only reserves this mode in documentation. Do not implement the ingest script.

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

- `primary_sound_type` is only `散音`, `按音`, or `泛音`.
- `component_sound_type` is only `散音`, `按音`, `泛音`, or `none`.
- Do not create a fourth sound type.
- Express complex techniques through `sound_profile`, `gesture_family`, and `gesture_components`.
- `events` are original score facts and parse facts.
- `interpretations` are dapu interpretations.
- `qinist_profile` is Sanman style preference.
- Do not write Sanman performance preferences into raw events.

Score and realization separation:

- Score-unmarked `绰` must not be auto-filled as `notation_pre_action=chuo`.
- Score-marked `绰` maps to `notation_pre_action=chuo`.
- Score-marked `注` maps to `notation_pre_action=zhu`.
- Sanman default `绰` belongs to `realization_pre_action=chuo` or `sample_selection_policy`.
- Score-marked `吟`/`猱` maps to `notation_vibrato=yin`, `nao`, or `yin_nao`.
- Sanman default `吟猱` belongs to `realization_vibrato`.

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
- Emit validation warnings for tokens that cannot be uniquely parsed

## Workflow

1. Read V1 authority files.
2. Normalize token aliases.
3. Parse token internals into components.
4. Build event groups and events without adding realization defaults.
5. Preserve source references, confidence, and review status.
6. Validate against `references/normalization_rules.md`, `references/validation_rules.md`, and `scripts/validate_dapu_ir.py`.
