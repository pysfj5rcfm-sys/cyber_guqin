# QXBY_BATCH_002 Draft Ingest Report

## Source

- Source title: `琴学备要`
- Batch: `QXBY_BATCH_002`
- Source type: manual image transcription from 8 screenshots
- Draft: `canon/drafts/qxby_batch_002.yaml`
- Source archive: `sources/qinxue_beiyao/QXBY_BATCH_002/`

## Items

| item_id | term | internal_name | status |
|---|---|---|---|
| QXBY_B002_001 | 按音 | `sound_type_an` | draft / needs_review |
| QXBY_B002_002 | 散音 | `sound_type_san` | draft / needs_review |
| QXBY_B002_003 | 大指 | `thumb` | draft / needs_review |
| QXBY_B002_004 | 食指 | `index` | draft / needs_review |
| QXBY_B002_005 | 中指 | `middle` | draft / needs_review |
| QXBY_B002_006 | 名指 | `ring` | draft / needs_review |
| QXBY_B002_007 | 跪指 | `gui_finger` | draft / needs_review |
| QXBY_B002_008 | 泛音 | `sound_type_fan` | draft / needs_review |

## Internal Name Scope

`internal_name` records the standard internal name of the Batch002 entry itself. `mapped_component_name` records the component / technique that the entry maps to in the ontology. For that reason, the three sound-type entries use `sound_type_an`, `sound_type_san`, and `sound_type_fan` as `internal_name`, while their semantic mappings remain in `mapped_component_name`.

## User Clarifications Applied

- Batch002 covers 散音、泛音、按音, plus four left-hand pressing fingers and 跪指.
- The compound 泛音撮 case is treated as left-hand harmonic action plus right-hand 撮; it was not created as an independent special technique entry.
- Batch001 掐起 already covers “名指按下一音位” and same-string predecessor semantics; no new inherited 掐起 rule was added in this batch.

## C1 Coverage

- Covered: 三音型中的 散音、按音、泛音.
- Covered: 指名系统中的 大指、食指、中指、名指, plus 跪指 as a supplemental finger posture / pressed-pluck reference.
- Covered: 泛音取法 and harmonic touch-finger references.
- Explicitly not listed as independent C1 topics: compound 泛音撮, and a new 掐起 inheritance rule.

## Guardrails

- All items remain `source_status=manual_image_transcription`, `review_status=draft`, `needs_review=true`.
- No Batch002 item is marked `verified`.
- No V1 mainline folders were modified.
- No canon seed file in `canon/*.yaml` was modified.
- No recording ingest script, `recording_items_enriched.jsonl`, or V1 patch was created.
