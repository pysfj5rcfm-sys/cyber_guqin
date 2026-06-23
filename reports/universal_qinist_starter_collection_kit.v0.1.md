# Universal Qinist Starter Collection Kit v0.1

状态：设计稿。Universal kit first; Sanman is first instance.

## 1. Concept

The kit is a reusable collection design for future qinists:

```text
QINIST_STARTER_COLLECTION_KIT
-> instance: QINIST_001_SANMAN
-> future instances: QINIST_003, QINIST_004, ...
```

It must not be permanently bound to Sanman, but this first design uses Sanman as the active instance.

## 2. Kit Layers

1. Universal taxonomy layer:
   - sound type
   - gesture family
   - components
   - context/tail policies
   - priority tiers
2. Qinist instance layer:
   - `qinist_id`
   - optional profile priors
   - current inventory
   - collection constraints
3. Piece demand layer:
   - single-piece Dapu IR demand
   - workflow aggregation output
4. Prompt and review layer:
   - prompt manifest
   - R0/R1/R2 compatibility
   - candidate sidecar

## 3. Priority Tiers

| Tier | Meaning | Examples |
| --- | --- | --- |
| P0 | foundational / high-frequency / clean atomic | 散挑七、散勾五、stable 泛音, clean right-hand plucks |
| P1 | high-frequency pressed sound and common ornaments | clean 按音, explicit 绰/注, simple 上/下 |
| P2 | context / transition / yin-nao / complex pressed movement | 掐起 context, 吟/猱, phrase transition |
| P3 | long-tail / full-tail / diagnostic cases | 上七九 tail, rare compounds, diagnostic phrase boundary |
| SKIP | low-value, unsafe, unclear, not justified | ambiguous OCR, Baiya-only substitution, context-only-as-atomic |

`priority_tier` is a proposed extension field and requires approval before implementation.

## 4. Sanman Instance

Sanman instance rules:

- `qinist_id=QINIST_001`
- Baiya rows never count as Sanman coverage.
- Existing `00_global/qinist_profiles/QINIST_001_sanman.yaml` is a profile placeholder, not trained model proof.
- Sanman realization preferences may influence collection design, but must not be written into score facts.
- Real collection batch data is not created in this task.

## 5. Future Qinist Support

Future qinists should inherit the universal kit and have separate:

- qinist profile file
- collection inventory
- prompt manifests
- candidate sidecars
- profile signal extensions

No universal item should contain a hardcoded qinist-specific style claim.

## 6. Minimal Starter Item Shape

Draft starter item fields:

```text
kit_id
starter_item_id
priority_tier
qinist_id
piece_id / source_score_id
event_id / score_event_id
primary_sound_type
gesture_family
gesture_id
components
string_no / hui
context policy
tail policy
coverage_status
evidence_refs
safety flags
```

All new fields are draft-only and referenced in the field matrix.

