# CG-LXY P2J Auxiliary Matchability Update Report v0.1

Task ID: `CG-LXY-136-P2J-AUXILIARY-MATCHABILITY-v0.1`

Status labels:

- D1_COMPONENT_REFERENCE_LAYER_UPDATE
- P2B_RUNTIME_INDEX_UPDATE
- AUXILIARY_COMPONENT_MATCHABLE
- PROVISIONAL_NUMERIC_EQUIVALENCE_REFERENCE
- NOT_PHRASE_READING_AUTHORITY
- NOT_GRAMMAR_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NEEDS_HUMAN_REVIEW

## Scope

This update changes the twelve auxiliary components that were previously `matchable=false` in the P2B runtime visual index.

Out of scope:

```text
phrase reading
surface reading
grammar parse
score fact
Dapu IR
sample ingest
ML training
八～十三 component minting
```

## Updated Components

Numeric auxiliary components:

```text
COMP-081 一  matchable=true  provisional_numeric_equivalence_reference
COMP-082 二  matchable=true  provisional_numeric_equivalence_reference
COMP-083 三  matchable=true  provisional_numeric_equivalence_reference
COMP-084 四  matchable=true  provisional_numeric_equivalence_reference
COMP-085 五  matchable=true  provisional_numeric_equivalence_reference
COMP-086 六  matchable=true  provisional_numeric_equivalence_reference
COMP-087 七  matchable=true  provisional_numeric_equivalence_reference
```

Left-finger-name auxiliary components:

```text
COMP-091 大指  matchable=true  registry_auxiliary_reference
COMP-092 食指  matchable=true  registry_auxiliary_reference
COMP-093 中指  matchable=true  registry_auxiliary_reference
COMP-094 名指  matchable=true  registry_auxiliary_reference
COMP-095 跪指  matchable=true  registry_auxiliary_reference
```

## Reference Images

Generated or bound files:

```text
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-081_一_provisional_equivalence.png
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-082_二_provisional_equivalence.png
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-083_三_provisional_equivalence.png
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-084_四_provisional_equivalence.png
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-085_五_provisional_equivalence.png
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-086_六_provisional_equivalence.png
sources/qxby_component_atlas/images/auxiliary_numeric/COMP-087_七_provisional_equivalence.png

sources/qxby_component_atlas/images/auxiliary_left_finger_names/COMP-091_大指.png
sources/qxby_component_atlas/images/auxiliary_left_finger_names/COMP-092_食指.png
sources/qxby_component_atlas/images/auxiliary_left_finger_names/COMP-093_中指.png
sources/qxby_component_atlas/images/auxiliary_left_finger_names/COMP-094_名指.png
sources/qxby_component_atlas/images/auxiliary_left_finger_names/COMP-095_跪指.png
```

Left-finger-name PNGs were converted from the repo-local `QXBY_BATCH_002` reference JPEGs.

Numeric one-to-seven PNGs are provisional equivalence references. They are only for component-level visual matching during the current one-to-seven validation phase.

## Explicit Non-Coverage

The following labels are not minted as primary components in this update:

```text
八
九
十
十一
十二
十三
```

Runtime metadata for `COMP-081..087` records:

```text
reference_type: provisional_numeric_equivalence_reference
equivalence_scope: ONE_TO_SEVEN_ONLY
not_covered: 八, 九, 十, 十一, 十二, 十三
```

This implements the current validation policy: avoid low-register hui-position images for now, stabilize one-to-seven hui/string validation first, and register eight-to-thirteen references later.

## Index Summary

After rebuild:

```text
component_index_count: 186
image_reference_count: 186
source_image_missing_count: 0
```

## Real-Image Impact

After enabling auxiliary matchability, the first reality-check image changes from atlas-gap-dominated to mixed P2B recall:

```text
COMP-091 大指  MISS
九             ATLAS_GAP
COMP-087 七    MISS
COMP-418 注    PASS_TOP1
COMP-116 挑    PASS_TOP3
```

Interpretation:

```text
P2G segmentation remains usable.
P2B now has enough reference coverage to expose true misses for 大指 and 七.
九 remains a deliberate no-independent-component-id gap.
```
