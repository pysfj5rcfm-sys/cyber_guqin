# QXBY_BATCH_001 Draft Ingest Report

## Scope

- Batch: `QXBY_BATCH_001`
- Source title: `琴学备要`
- Source status: `manual_image_transcription`
- Draft path: `canon/drafts/qxby_batch_001.yaml`
- Validator report: `reports/validate_qxby_batch_001_report.json`

This batch records a small manual transcription draft from user-provided `琴学备要` screenshot/image material. It is not a verified canon ingest.

## Imported Items

The draft contains the requested 16 items:

| normalized_term | mapped_component_name | category | gesture_family | sound_profile | confidence |
| --- | --- | --- | --- | --- | --- |
| `bo` | `bo` | `pluck` | `single_pluck` | `single` | high |
| `tuo` | `tuo` | `pluck` | `single_pluck` | `single` | medium |
| `mo` | `mo` | `pluck` | `single_pluck` | `single` | high |
| `tiao` | `tiao` | `pluck` | `single_pluck` | `single` | medium |
| `gou` | `gou` | `pluck` | `single_pluck` | `single` | medium |
| `ti` | `ti` | `pluck` | `single_pluck` | `single` | high |
| `da` | `da` | `pluck` | `single_pluck` | `single` | high |
| `zhai` | `zhai` | `pluck` | `single_pluck` | `single` | medium |
| `chuo` | `chuo` | `pre_slide` | `component_only` | `none` | high |
| `zhu` | `zhu` | `pre_slide` | `component_only` | `none` | high |
| `zhuang` | `zhuang` | `micro_returning_slide` | `post_motion` | `post_motion` | medium |
| `fan_zhuang` | `fan_zhuang` | `micro_returning_slide` | `post_motion` | `post_motion` | high |
| `shang` | `shang` | `single_slide` | `post_motion` | `post_motion` | high |
| `xia` | `xia` | `single_slide` | `post_motion` | `post_motion` | high |
| `qiaqi` | `qiaqi` | `left_sound` | `left_hand_sound` | `left_hand_sound` | medium |
| `cuo` | `cuo` | `simultaneous_pluck` | `simultaneous_pluck` | `simultaneous_strings` | high |

## Review Status

Every item remains:

- `source_status=manual_image_transcription`
- `review_status=draft`
- `needs_review=true`

No item is marked `verified`. Confidence is a transcription/mapping confidence only; it is not verification.

## Confidence Summary

- high: `bo`, `mo`, `ti`, `da`, `chuo`, `zhu`, `fan_zhuang`, `shang`, `xia`, `cuo`
- medium: `tuo`, `tiao`, `gou`, `zhai`, `zhuang`, `qiaqi`
- low: none

## OCR / Transcription Uncertainty

The batch comes from screenshot/image transcription and is therefore review-bound. Items with explicit uncertainty markers,待补 page/section data, or medium confidence are tracked by the validator in `ocr_or_transcription_uncertainty_terms`.

## Ontology Conflicts

No item in this batch is marked as conflicting with `PROJECT_ONTOLOGY_V1_1`:

- `conflict_with_project_ontology=false` for all 16 items.

The batch-specific validator checks the present 16 mappings against Gesture Ontology v1.1 rules. Global guardrails for absent terms such as `po`, `la`, `yan`, `fanghe`, `yinghe`, `fenkai`, `jinfu`, and `tuifu` are conditional only and are not reported as missing.

`chuo` and `zhu` are `pre_slide` components: they are pre-sound approach actions, not `post_motion`. Their `component_only` marker is draft-local and is not treated as a canonical `gesture_family`.

## Validation Result

`scripts/validate_qxby_batch.py` result:

- status: `pass`
- passed: `true`
- errors: none
- warnings: none

The validator can use PyYAML when available and includes a built-in simple YAML fallback so missing third-party YAML support does not directly fail the validation path.

## Boundary Confirmation

This round did not modify V1 mainline files such as:

- `00_global/`
- `01_pieces/`
- `03_samples/`
- `render_audio.py`
- `smoke_test.py`
- `recording_batches.md`
- `recording_script_human.csv`
- `recording_script_human.md`

This round did not create `recording_items_enriched.jsonl`, did not run recording ingest, and did not make V1 repair edits.

## Human Review Update

The user manually reviewed all 16 QXBY_BATCH_001 items and confirmed image-to-item mapping, raw excerpt, normalized term, and ontology mapping are correct. The batch remains non-verified and is recorded as reviewed draft in `reports/qxby_batch_001_human_review.md`.
