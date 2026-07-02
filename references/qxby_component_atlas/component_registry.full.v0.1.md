# QXBY Full Component Atlas Registry v0.1

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `SOURCE_REFERENCE_IMAGE`, `USER_PROVIDED_QXBY_COMPONENT_SET`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`

This is `QXBY_FULL_COMPONENT_ATLAS_REFERENCE` for user-provided QXBY component images. It is source/reference knowledge only: `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, and `NOT_RENDER_OUTPUT`.

## Summary

- Registry ID: `QXBY_FULL_COMPONENT_ATLAS_v0.1`
- Source set: `USER_PROVIDED_QXBY_COMPONENT_SET`
- Total components: `174`
- Total categories: `9`
- ID range: `COMP-100..COMP-273`
- Legacy range preserved: `COMP-001..037`
- Observed `COMP-038` in current legacy registry: `true`; it was also left untouched.
- Duplicate label groups: `0`
- Duplicate hash groups: `0`
- Legacy aliases resolved: `25`
- Excluded non-registered files: `192`

## Category Counts And ID Ranges

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

## Source Zips

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

## Duplicate Labels

No duplicate labels were found in the full atlas.

## Duplicate Image Hashes

No duplicate image hashes were found in the full atlas.

## Legacy Aliases

Resolved aliases are stored in `component_legacy_alias_map.v0.1.json`. Category-taxonomy differences remain reviewable and do not become canon authority.

| Legacy ID | Legacy label | Legacy category | Full ID | Full category | Basis | Confidence | Needs review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| COMP-001 | 托 | 右手指法 | COMP-182 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-002 | 泛起 | 泛音起始 | COMP-144 | 音位谱字 | label_match | medium | true |
| COMP-003 | 少息 | 节奏谱字 | COMP-105 | 节奏谱字 | label_match+category_match | high | false |
| COMP-010 | 吟 | 左手指法 | COMP-198 | 左手指法-本位取音 | label_match | medium | true |
| COMP-014 | 历 | 右手指法 | COMP-163 | 右手指法-数弦连弹 | label_match | medium | true |
| COMP-017 | 泛止 | 泛音停止 | COMP-143 | 音位谱字 | label_match | medium | true |
| COMP-018 | 挑 | 右手指法 | COMP-186 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-019 | 爪起 | 左手指法 | COMP-273 | 左手指法-散弦取音 | label_match | medium | true |
| COMP-020 | 勾 | 右手指法 | COMP-173 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-021 | 背锁 | 右手指法 | COMP-190 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-022 | 掐起 | 左手指法 | COMP-246 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-023 | 就 | 左手承前 | COMP-128 | 通用谱字 | label_match | medium | true |
| COMP-024 | 进复 | 左手取音 | COMP-258 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-025 | 注 | 左手取音 | COMP-211 | 左手指法-本位取音 | label_match | medium | true |
| COMP-026 | 上 | 左手取音 | COMP-232 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-028 | 撞 | 左手取音 | COMP-209 | 左手指法-本位取音 | label_match | medium | true |
| COMP-029 | 轮 | 右手指法 | COMP-191 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-030 | 急 | 节奏谱字 | COMP-106 | 节奏谱字 | label_match+category_match | high | false |
| COMP-031 | 抹挑 | 右手指法 | COMP-185 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-033 | 绰 | 左手取音 | COMP-219 | 左手指法-本位取音 | label_match | medium | true |
| COMP-034 | 双吟 | 左手取音 | COMP-194 | 左手指法-本位取音 | label_match | medium | true |
| COMP-035 | 落指猱 | 左手取音 | COMP-227 | 左手指法-本位取音 | label_match | medium | true |
| COMP-036 | 掩 | 左手指法 | COMP-247 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-037 | 剔 | 右手指法 | COMP-172 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-038 | 双弹 | 右手指法 | COMP-150 | 右手指法-两弦双弹 | label_match | medium | true |

## Excluded Files

Ignored entries are recorded in `sources/qxby_component_atlas/source_inventory.v0.1.json`. Ignored categories include `__MACOSX/`, `.DS_Store`, `._*`, hidden files, and non-image files.

## Known Caveats

- Python `zipfile` direct listing showed mojibake for internal paths, so registration used `ditto -x -k` extraction to `/tmp` and verified restored Chinese filenames before assigning IDs.
- The full atlas uses the nine user-provided major categories from zip/top-level folder names. Older pilot categories are sometimes broader, so label-only aliases are marked reviewable.
- `component_to_canon_crosswalk.seed.v0.1.*` is seed-only and `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`.
- No phrase reading, Dapu IR, recording plan, sample ingest, ML training data, or render output is created by this registry.

## Next Canon-Builder Crosswalk Step

A future canon-builder review should inspect each `seed_pending` entry, confirm or revise canonical term keys, decide gesture/sound policies, and keep score-event promotion behind explicit human/parser gates.
