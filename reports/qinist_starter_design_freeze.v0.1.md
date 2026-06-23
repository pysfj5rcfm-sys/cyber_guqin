# Qinist Starter Design Freeze v0.1

## 1. Task ID

`CG-QINIST-STARTER-KIT-DESIGN-FREEZE-v0.1`

## 2. Freeze Status

Status: `DESIGN_FREEZE_RECORDED`

This is an audit closeout and planning freeze. It does not implement runtime code, production schemas, score import, recording, TTS/audio, R0/R1/R2, render scripts, sample ingest, ML training, or second-piece production.

Current mainline remains:

```text
QINIST_STARTER_COLLECTION_KIT
-> first instance: QINIST_001_SANMAN
```

Baiya / `QINIST_002` remains XWC accepted baseline, workflow regression case, engineering reference, and comparison qinist only. Baiya data must not become Sanman style data or Sanman inventory.

## 3. Authority Documents Used

- `/Users/chenyulin/Downloads/Core_Instructions_v1.6.md`
- `/Users/chenyulin/Downloads/NEXT_CHAT_HANDOFF_SANMAN_DIGITIZATION_STARTUP_v0.2.md`
- `/Users/chenyulin/Downloads/RECD_VARW_Cyber_Guqin_v1.1.md`
- `reports/qinist_starter_field_source_audit.v0.1.md`
- `reports/qinist_starter_field_source_matrix.v0.1.json`
- `reports/qinist_starter_kit_and_sanman_instance_design.v0.1.md`
- `reports/qinist_starter_draft_artifact_review.v0.1.md`
- `reports/qinist_starter_missing_inputs.v0.1.md`

Authority decision:

- `RECD_VARW_Cyber_Guqin_v1.1.md` is current RECD/VARW authority.
- `RECD&VARW · Cyber Guqin v1.0.txt` is historical optional reference only.
- v1.0 absence is not blocking current design freeze or next implementation planning unless the user explicitly asks for historical v1.0/v1.1 delta audit.
- v1.0 contents must not be inferred from v1.1.

## 4. Decisions Frozen

### 4.1 Sanman Inventory Baseline

```yaml
qinist_id: QINIST_001
sanman_inventory_mode: EMPTY_BASELINE
sanman_inventory_status: EMPTY_BASELINE_CONFIRMED
```

There is no existing Sanman inventory to discover. Empty inventory is the intended starting baseline. Coverage diff should treat Sanman inventory as empty until real Sanman collection data exists. Baiya data cannot count as Sanman coverage.

### 4.2 Starter Demand Repertoire

The starter demand repertoire is frozen as five pieces:

| piece_id | title_zh |
| --- | --- |
| `XWC` | 仙翁操 |
| `LXY` | 良宵引 |
| `JK` | 酒狂 |
| `OLWJ` | 鸥鹭忘机 |
| `PSLY` | 平沙落雁 |

Each piece must be processed independently through canon/parser. `guqin-dapu-parser` remains single-piece. Workflow / coverage diff may aggregate resulting single-piece IR outputs later.

### 4.3 Parser and Aggregation Boundary

```text
guqin-dapu-parser = single-piece only
multi-piece aggregation = workflow / coverage diff layer only
```

No multi-piece parser input is approved.

### 4.4 Draft Field Approval Scope

The existing proposed extension fields are approved as draft contract for implementation planning only.

This is not production schema freeze, not runtime wiring approval, not sample ingest approval, and not ML training approval.

### 4.5 Dry-run Fixture Adapter Decision

Existing dry-run fields must be adapter-normalized before future starter execution:

| dry-run field | target concept |
| --- | --- |
| `sound_type` | `primary_sound_type` |
| `string` | `string_no` |
| `hui_position` | `hui` / `hui_target` as appropriate |

Historical dry-run fixtures are not rewritten in this task.

### 4.6 score_event_id Decision

`event_id` remains the repo canonical score event identity. `score_event_id` may be used as a sidecar semantic alias only when explicitly mapped to `event_id`.

This task does not make `score_event_id` a new global first-class score schema key.

### 4.7 Priority Tier Decision

| tier | frozen meaning |
| --- | --- |
| `P0` | 散音 / 泛音 foundational clean coverage + structure-validated high-frequency pressed sounds only |
| `P1` | common pressed sounds and common score-marked ornaments |
| `P2` | context / transition / yin-nao / complex pressed movement |
| `P3` | long-tail / full-tail / diagnostic cases |
| `SKIP` | unsafe / unclear / low-value / not justified |

Pressed sounds must not be blindly full-covered.

### 4.8 Prompt Manifest Decision

`prompt_manifest` does not pre-allocate real `recording_take_no`. `prompt_id` and `prompt_order` are prompt identities only. Formal `recording_session_id` / `recording_take_no` are created only after recording is authorized.

Prompt format remains concise:

```text
编号 / 给琴人听的指法内容 / 发令枪
```

Example:

```text
T001，散挑七弦，开始。
```

### 4.9 Profile Signal Decision

Qinist Profile signal extraction remains report-only / draft sidecar until real Sanman R2 evidence exists.

Profile signals must map from VARW R2 evidence. Do not create a disconnected R2 label system. Do not claim a Sanman style model exists.

### 4.10 RECD/VARW and Safety Boundary

RECD/VARW serves Dapu audition and future candidate preparation. It does not equal production sample ingest.

## 5. Approved Draft Fields

Approved for draft contract / implementation planning only:

```text
bad_take_policy
candidate_id
coverage_status
evidence_refs
exclusion_reason
kit_id
not_recording_items_enriched
priority_tier
profile_signal_id
profile_signal_type
prompt_id
prompt_interval_s
prompt_manifest_id
prompt_order
prompt_text_zh
retake_policy
starter_item_id
trigger_text
```

These fields remain not approved as production schema, not approved for runtime wiring unless a later implementation task explicitly does so, not approved for sample ingest, and not approved for ML training.

## 6. Decisions Explicitly Not Approved

Not approved:

- production schema freeze
- runtime schema wiring
- modifying draft schemas in this task
- modifying mock fixtures in this task
- score import in this task
- recording start
- TTS/audio generation
- R0/R1/R2 execution
- render/audio script execution
- sample ingest
- writing `sample_assets.csv`
- writing `recording_segments.csv`
- writing `recording_items_enriched.jsonl`
- ML training
- second-piece production
- accepted `F_FINAL_REVIEWED` rewrite
- Baiya-as-Sanman substitution
- score facts / qinist realization mixing
- multi-piece `guqin-dapu-parser` input
- running or modifying `scripts/generate_baiya_recording_plan.py`

## 7. Remaining Blockers Before Real Demand Extraction

Before real demand extraction / coverage diff:

- import the five approved scores
- process each piece independently through canon/parser
- produce auditable single-piece Dapu IR outputs
- normalize dry-run adapter fields into starter contract concepts
- keep Sanman inventory empty until authorized real Sanman collection data exists
- approve implementation task boundaries for coverage diff

Not blockers for design freeze:

- empty Sanman inventory
- missing historical `RECD&VARW · Cyber Guqin v1.0.txt`

## 8. Next Stage: 5-piece Score Import

Next stage: `5-piece score import`.

Scope for the next stage should be limited to preparing/importing:

```text
XWC / 仙翁操
良宵引
酒狂
鸥鹭忘机
平沙落雁
```

Each piece must remain independently parsed. Later aggregation belongs only to workflow / coverage diff.

The next stage still should not start recording, R0/R1/R2, render/audio generation, sample ingest, ML training, or second-piece production.

## 9. Safety Boundaries

Still forbidden:

- `sample_assets.csv`
- `recording_segments.csv`
- `recording_items_enriched.jsonl`
- ML training
- sample ingest
- accepted F rewrite
- audio generation
- TTS generation
- second-piece production
- Baiya-as-Sanman substitution
- score facts / qinist realization mixing

## 10. Commit Recommendation

Safe commit scope, if the user chooses to commit:

```text
reports/qinist_starter_design_freeze.v0.1.md
reports/qinist_starter_design_freeze_decisions.v0.1.json
reports/qinist_starter_missing_inputs.v0.1.md
```

Do not include `scripts/generate_baiya_recording_plan.py`. It remains a protected historical template / pre-existing untracked item and is not part of this design freeze.
