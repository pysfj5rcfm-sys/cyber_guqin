# QXBY Full Component Atlas Registration Report v0.1

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `SOURCE_REFERENCE_IMAGE`, `USER_PROVIDED_QXBY_COMPONENT_SET`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`

## Scope Confirmation

This task is QXBY full component atlas registration only.

It is not score import, LXY phrase transcription, Dapu IR authority, recording plan, R0/R1/R2/E/F, sample ingest, ML training, render, or Sanman collection plan.

## Results

- Input zips found: `9/9`
- Filename encoding clean after `ditto`: `true`
- Source zips processed: `9`
- Images registered: `174`
- Categories: `9`
- ID range: `COMP-100..COMP-273`
- Old `COMP-001..037` preserved: `true`
- Observed `COMP-038` also preserved: `true`
- Legacy aliases resolved: `25`
- Duplicate label groups: `0`
- Duplicate hash groups: `0`
- Excluded non-registered files: `192`

## Category Counts

| Category | Count | ID range |
| --- | --- | --- |
| 节奏谱字 | 22 | COMP-100..COMP-121 |
| 通用谱字 | 15 | COMP-122..COMP-136 |
| 音位谱字 | 8 | COMP-137..COMP-144 |
| 右手指法-两弦双弹 | 17 | COMP-145..COMP-161 |
| 右手指法-数弦连弹 | 9 | COMP-162..COMP-170 |
| 右手指法-一弦单弹 | 23 | COMP-171..COMP-193 |
| 左手指法-本位取音 | 38 | COMP-194..COMP-231 |
| 左手指法-隔位取音 | 33 | COMP-232..COMP-264 |
| 左手指法-散弦取音 | 9 | COMP-265..COMP-273 |

## Source Zip Evidence

| Zip | Category | Registered images | Raw entries | SHA-256 |
| --- | --- | --- | --- | --- |
| 节奏谱字.zip | 节奏谱字 | 22 | 47 | 2b1ce9742950f815f5ee2d36e97c820e36afa8dcdfc30da2425a95f66775c1a4 |
| 通用谱字.zip | 通用谱字 | 15 | 33 | 1c6c0088daa81b03422aa668555abe97019bfc4697084acb914ab9e5d074ecab |
| 音位谱字.zip | 音位谱字 | 8 | 19 | 44a8647f53c66e091ebb2cdd0fc1fde0de3d62b59c92b420a598c6ce2840fd8a |
| 右手指法-两弦双弹.zip | 右手指法-两弦双弹 | 17 | 37 | d4b6c17bd53949bc7313ea54fb7943abdaa52006b3fd7a8ce7cf4f455f0ea667 |
| 右手指法-数弦连弹.zip | 右手指法-数弦连弹 | 9 | 21 | d41f7691a492d348df00b5f4056aba61bfcbc64ffb36d77d42e3daabe8e38ed9 |
| 右手指法-一弦单弹.zip | 右手指法-一弦单弹 | 23 | 49 | d0cf7558651ef7be3ee77cf8488eb5c490fdb4599e2260be139ec34221f0c1fa |
| 左手指法-本位取音.zip | 左手指法-本位取音 | 38 | 79 | b0fd14b9c3fec7f1ebf3fab5aa5081be8f223f9845072e1c621bef3115cde940 |
| 左手指法-隔位取音.zip | 左手指法-隔位取音 | 33 | 69 | 91cf302ec68c71195d6980889016eec233a8f4720390d8ecb6127a37cf3391b2 |
| 左手指法-散弦取音.zip | 左手指法-散弦取音 | 9 | 21 | 37cb77630a2606b578c506de4044266fe6dc931bcee609b0cd68e41683de49de |

## Legacy Alias Summary

Resolved aliases are reviewable evidence only. They do not delete, renumber, or overwrite legacy IDs.

- Resolved aliases: `25`
- Needs-review aliases: `23`
- Unmapped legacy components: `13`

## Duplicate Review

- Duplicate labels: `0`
- Duplicate image hashes: `0`

## Known Caveats

- Direct Python zip listing was mojibake; `ditto` extraction restored Chinese filenames and was used as the registration source.
- Full-atlas categories come from the provided zip/top-level folder names, so old pilot generic categories may differ from new major categories.
- `component_to_canon_crosswalk.seed.v0.1.*` is only a seed for canon-builder review.

## Files Written

- `sources/qxby_component_atlas/README.md`
- `sources/qxby_component_atlas/source_inventory.v0.1.json`
- `sources/qxby_component_atlas/source_inventory.v0.1.csv`
- `sources/qxby_component_atlas/images/`
- `references/qxby_component_atlas/README.md`
- `references/qxby_component_atlas/component_registry.full.v0.1.json`
- `references/qxby_component_atlas/component_registry.full.v0.1.md`
- `references/qxby_component_atlas/component_legacy_alias_map.v0.1.json`
- `references/qxby_component_atlas/component_legacy_alias_map.v0.1.md`
- `references/qxby_component_atlas/component_to_canon_crosswalk.seed.v0.1.json`
- `references/qxby_component_atlas/component_to_canon_crosswalk.seed.v0.1.md`
- `reports/qxby_component_atlas/full_registration_report.v0.1.md`
- `reports/qxby_component_atlas/full_registration_summary.v0.1.json`
- `reports/qxby_component_atlas/full_registration_review_sheet.v0.1.csv`
- `.agents/skills/cyber_guqin_component_guided_transcription/SKILL.md`

## Skill Update

Added a focused `Full QXBY Component Atlas` section requiring phrase recognition to read the full registry, use the legacy alias map for old pilot IDs, treat the canon crosswalk as `seed_pending`, and mark unknown future glyphs as `component_gap` instead of force-matching.
