# Qinist Starter Kit and Sanman Instance Design v0.1

状态：设计汇总。不是生产就绪，不是 ML 就绪，不是采集执行。

## 1. Current Mainline

当前主线：

```text
QINIST_STARTER_COLLECTION_KIT
-> QINIST_001_SANMAN
```

当前不是 Baiya second piece，不是 sample ingest，不是 ML training，不是 accepted `F_FINAL_REVIEWED` 重跑。

## 2. Starter Kit Concept

Starter kit 是可复用的琴人启动采集设计：

- universal kit 先行
- Sanman 是 first instance
- future qinists 可复用同一 kit 层
- 每个 qinist 拥有自己的 inventory、prompt manifest、candidate sidecar、profile signals

## 3. Sanman Instance Concept

Sanman instance 使用：

```text
qinist_id = QINIST_001
```

已有 `00_global/qinist_profiles/QINIST_001_sanman.yaml` 只是初始占位，不代表训练完成，也不代表已有 Sanman style model。

## 4. Single-Piece Parser Boundary

`guqin-dapu-parser` 保持单曲 parser：

- one piece -> tokens/components/event groups/events/validation
- 不接收 multi-piece aggregate input
- 不决定 Sanman style
- 不写 sample ingest

## 5. Multi-Piece Aggregation Boundary

Workflow/diff layer 可聚合多个 single-piece outputs：

- independently parsed piece outputs
- per-piece demand extraction
- coverage diff against Sanman inventory
- Baiya only as comparison/reference

## 6. Field Audit Conclusions

字段来源矩阵：

```text
reports/qinist_starter_field_source_matrix.v0.1.json
```

关键结论：

- formal Dapu schema 优先于 dry-run fixture shape。
- `primary_sound_type` 是音型字段，只有散/按/泛。
- `take_id/source_audio/variant/anchor_type` 是 legacy aliases。
- `candidate_id/starter_item_id/prompt_manifest_id/profile_signal_id` 等都是 proposed extension。
- `sample_id` 不可作为 sidecar identity。

## 7. Starter Collection Strategy

Priority tiers:

- P0: foundational / high-frequency / clean atomic
- P1: high-frequency pressed sound and common ornaments
- P2: context / transition / yin-nao / complex pressed movement
- P3: long-tail / full-tail / diagnostic
- SKIP: unsafe/unclear/low-value

散音和泛音可以偏 full coverage；按音必须先做结构验证。

## 8. AI Prompted Collection Protocol

Prompt format:

```text
编号 / 给琴人听的指法内容 / 发令枪
```

Example:

```text
T001，散挑七弦，开始。
```

Prompt manifest supports R0 alignment. ASR is auxiliary, not sole authority. Default interval may start around 10 seconds after prior prompt end, but requires calibration.

## 9. Candidate Sidecar

Sidecar only records future candidate evidence:

- score facts
- source take provenance
- R0/R1/R2 labels
- human labels
- qinist realization
- wrong/failed/context-only exclusion

It does not write `sample_assets.csv`, `recording_segments.csv`, or `recording_items_enriched.jsonl`.

## 10. Rhythm-Diverse ABCD

ABCD is parameterized by:

```text
tempo curve
phrase entry delay
intra-phrase variation
cadence hold
tail duration
ornament duration
yin/nao density
silence after phrase
section transition pause
diagnostic intent
```

A/B/C/D are review strategies only, not render authorization.

## 11. VARW R2 Profile Mapping

Profile mapping uses existing VARW R2 outputs:

```text
latest JSON -> listening review -> revision log -> preferred summary -> profile signal extension
```

No disconnected R2 label system.

## 12. Red Lines Preserved

- no audio recording
- no TTS generation
- no sample ingest
- no `sample_assets.csv`
- no `recording_segments.csv`
- no `recording_items_enriched.jsonl`
- no ML training
- no second-piece production
- no accepted F rewrite
- no parser aggregation
- no Baiya-as-Sanman substitution

## 13. Next Recommended Task

Recommended next task:

```text
CG-QINIST-STARTER-KIT-USER-REVIEW-v0.1
```

Scope: user reviews the draft field matrix, priority tiers, prompt protocol, sidecar shape, and proposed extension fields. Implementation should wait for explicit approval.

