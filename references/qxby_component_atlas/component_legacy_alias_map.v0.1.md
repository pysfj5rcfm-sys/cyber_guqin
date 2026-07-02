# QXBY Full Component Atlas Legacy Alias Map v0.1

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `SOURCE_REFERENCE_IMAGE`, `USER_PROVIDED_QXBY_COMPONENT_SET`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`

This alias map preserves old pilot IDs and maps them to `COMP-100+` full-atlas IDs only when there is a unique exact label match. It is `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, and `NOT_RENDER_OUTPUT`.

## Summary

- Legacy components observed: `38`
- Prompt legacy range preserved: `COMP-001..037`
- Resolved aliases: `25`
- Review-needed aliases: `23`
- Unmapped legacy components: `13`

## Resolved Aliases

| Legacy ID | Legacy label | Legacy category | Full ID | Full label | Full category | Basis | Confidence | Needs review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COMP-001 | 托 | 右手指法 | COMP-182 | 托 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-002 | 泛起 | 泛音起始 | COMP-144 | 泛起 | 音位谱字 | label_match | medium | true |
| COMP-003 | 少息 | 节奏谱字 | COMP-105 | 少息 | 节奏谱字 | label_match+category_match | high | false |
| COMP-010 | 吟 | 左手指法 | COMP-198 | 吟 | 左手指法-本位取音 | label_match | medium | true |
| COMP-014 | 历 | 右手指法 | COMP-163 | 历 | 右手指法-数弦连弹 | label_match | medium | true |
| COMP-017 | 泛止 | 泛音停止 | COMP-143 | 泛止 | 音位谱字 | label_match | medium | true |
| COMP-018 | 挑 | 右手指法 | COMP-186 | 挑 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-019 | 爪起 | 左手指法 | COMP-273 | 爪起 | 左手指法-散弦取音 | label_match | medium | true |
| COMP-020 | 勾 | 右手指法 | COMP-173 | 勾 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-021 | 背锁 | 右手指法 | COMP-190 | 背锁 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-022 | 掐起 | 左手指法 | COMP-246 | 掐起 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-023 | 就 | 左手承前 | COMP-128 | 就 | 通用谱字 | label_match | medium | true |
| COMP-024 | 进复 | 左手取音 | COMP-258 | 进复 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-025 | 注 | 左手取音 | COMP-211 | 注 | 左手指法-本位取音 | label_match | medium | true |
| COMP-026 | 上 | 左手取音 | COMP-232 | 上 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-028 | 撞 | 左手取音 | COMP-209 | 撞 | 左手指法-本位取音 | label_match | medium | true |
| COMP-029 | 轮 | 右手指法 | COMP-191 | 轮 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-030 | 急 | 节奏谱字 | COMP-106 | 急 | 节奏谱字 | label_match+category_match | high | false |
| COMP-031 | 抹挑 | 右手指法 | COMP-185 | 抹挑 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-033 | 绰 | 左手取音 | COMP-219 | 绰 | 左手指法-本位取音 | label_match | medium | true |
| COMP-034 | 双吟 | 左手取音 | COMP-194 | 双吟 | 左手指法-本位取音 | label_match | medium | true |
| COMP-035 | 落指猱 | 左手取音 | COMP-227 | 落指猱 | 左手指法-本位取音 | label_match | medium | true |
| COMP-036 | 掩 | 左手指法 | COMP-247 | 掩 | 左手指法-隔位取音 | label_match | medium | true |
| COMP-037 | 剔 | 右手指法 | COMP-172 | 剔 | 右手指法-一弦单弹 | label_match | medium | true |
| COMP-038 | 双弹 | 右手指法 | COMP-150 | 双弹 | 右手指法-两弦双弹 | label_match | medium | true |

## Unmapped Legacy Components

| Legacy ID | Label | Category | Reason |
| --- | --- | --- | --- |
| COMP-004 | 五 | 弦数 | no_exact_full_atlas_label_match |
| COMP-005 | 句号 | 节奏谱字 | no_exact_full_atlas_label_match |
| COMP-006 | 六 | 弦数 | no_exact_full_atlas_label_match |
| COMP-007 | 七 | 弦数 | no_exact_full_atlas_label_match |
| COMP-008 | 名指 | 左手指法 | no_exact_full_atlas_label_match |
| COMP-009 | 一 | 弦数 | no_exact_full_atlas_label_match |
| COMP-011 | 四 | 弦数 | no_exact_full_atlas_label_match |
| COMP-012 | 大指 | 左手指法 | no_exact_full_atlas_label_match |
| COMP-013 | 中指 | 左手指法 | no_exact_full_atlas_label_match |
| COMP-015 | 二 | 弦数 | no_exact_full_atlas_label_match |
| COMP-016 | 三 | 弦数 | no_exact_full_atlas_label_match |
| COMP-027 | 散音起始 | 散音起始 | no_exact_full_atlas_label_match |
| COMP-032 | 如一声 | 两弦双弹 | no_exact_full_atlas_label_match |

## Caveat

A legacy alias is not canon authority. Category-different matches stay `needs_review=true` unless canon-builder review later confirms a stable equivalence.
