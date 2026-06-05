# Canon Seed Report - Step 2A

## Scope

This Step 2A run created a minimal canon seed for Cyber Guqin v1. It is a project-defined seed derived from `PROJECT_ONTOLOGY_V1_1`, not a formal ingestion of 《琴学备要》.

## Created Files

- `canon/sources.yaml`
- `canon/terms.yaml`
- `canon/component_lexicon.yaml`
- `canon/gesture_families.yaml`
- `canon/alias_rules.yaml`
- `canon/technique_rules.yaml`
- `canon/validation_rules.yaml`
- `scripts/validate_canon_seed.py`
- `reports/validate_canon_seed_report.json`

## Source

The seed source is `PROJECT_ONTOLOGY_V1_1`: Cyber Guqin Gesture Ontology v1.1, marked as `project_internal` and `verified`.

## Rules Written

- `primary_sound_type` and `component_sound_type` stay limited to `散音`, `按音`, `泛音`, or `none` for canon seed validation.
- Complex techniques are represented through `sound_profile`, `gesture_family`, and component rules, not new sound types.
- `bo=擘`, `po=泼`, `la=剌`, and `yan=罨`.
- `pi/劈` remain aliases of `bo/擘`.
- `拨/撥` and `拨剌/撥剌` remain aliases of `泼` and `泼剌`.
- `撞/反撞` are `micro_returning_slide` and are not percussive.
- `进复/退复` are atomic `returning_slide` components.
- `掐起/罨/带起` are `left_sound`.
- `撮` is `simultaneous_pluck`.
- `放合/应合` are `open_pressed_harmony`.
- `分开` is `compound_both_hands` with `sound_profile=compound_pressed_motion`.
- `分开` uses `mo_attack`, `shang_motion`, and `zhu_tiao_return_attack`; it does not add a separate `下`.
- Score-unmarked `绰` must not become `notation_pre_action=chuo`.

## Validation

The new `scripts/validate_canon_seed.py` reads `canon/*.yaml` and writes `reports/validate_canon_seed_report.json`. It uses Python standard-library JSON parsing for the JSON-compatible YAML seed files, with optional PyYAML fallback if future files use broader YAML syntax.

The full validation run should include:

- `scripts/validate_canon.py`
- `scripts/validate_dapu_ir.py`
- `scripts/check_v1_compat.py`
- `scripts/validate_canon_seed.py`

## Future Ingestion Path

Future 《琴学备要》 ingestion should proceed in small reviewed batches. Each batch should add source records, preserve OCR candidates as unverified, normalize aliases against `canon/alias_rules.yaml`, map techniques into `component_lexicon`, `gesture_families`, and `technique_rules`, and then run the canon seed validator before any V1 runtime integration.

## Non-Invasive Confirmation

This run did not modify V1 mainline authority files under `00_global`, piece data under `01_pieces`, sample data under `03_samples`, `05_scripts/render_audio.py`, or `05_scripts/smoke_test.py`. It did not create `recording_items_enriched.jsonl` or recording batch ingest artifacts.
