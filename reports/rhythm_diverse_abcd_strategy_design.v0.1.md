# Rhythm-Diverse ABCD Strategy Design v0.1

状态：parameter design only。不实现 audio rendering。

## 1. Goal

Design rhythm-diverse ABCD versions for future review without vague labels such as "more natural" unless translated into parameters.

## 2. Parameter Families

Every ABCD strategy should specify:

- tempo curve
- phrase entry delay
- intra-phrase variation
- cadence hold
- tail duration
- ornament duration
- yin/nao density
- silence after phrase
- section transition pause
- diagnostic intent

## 3. A_BASELINE_LITERAL_LIGHT_VARIATION

Intent: literal baseline with light rhythmic variation; low freedom.

Parameters:

- tempo curve: near-flat; max local deviation small.
- phrase entry delay: fixed or minimal.
- intra-phrase variation: low; preserve score order timing.
- cadence hold: short-to-medium, only at explicit cadence.
- tail duration: `full_tail` when required; otherwise controlled natural decay.
- ornament duration: score-marked only.
- yin/nao density: none unless score/profile says explicit.
- silence after phrase: consistent small gap.
- section transition pause: modest fixed pause.
- diagnostic intent: baseline reference, not style proof.

## 4. B_INTRA_PHRASE_RHYTHM_EXPLORATION

Intent: experiments with multiple rhythm shapes inside phrase boundaries.

Parameters:

- tempo curve: phrase-internal accelerando/ritardando candidates.
- phrase entry delay: mild variation by phrase role.
- intra-phrase variation: medium; test alternative grouping.
- cadence hold: medium; compare phrase-end breathing.
- tail duration: preserve `full_tail` where musically required.
- ornament duration: score-marked ornaments may vary within bounded ranges.
- yin/nao density: low-to-medium if explicitly represented.
- silence after phrase: phrase-specific.
- section transition pause: adjusted by section boundary.
- diagnostic intent: expose timing preference within same phrase boundary.

## 5. C_HUMAN_INITIALIZED_QINIST_PRIOR

Intent: before Sanman profile exists, allow human-initialized prior.

Example priors:

- faster tempo tendency
- fewer yin/nao
- restrained ornament
- natural but not excessive tail

Parameters:

- tempo curve: human prior sets base tempo and allowed curvature.
- phrase entry delay: prior-driven, not auto-learned.
- intra-phrase variation: medium-low unless human prior says otherwise.
- cadence hold: prior-defined.
- tail duration: natural decay but capped by explicit profile/human prior.
- ornament duration: restrained by prior.
- yin/nao density: low unless explicit.
- silence after phrase: prior-defined breathing.
- section transition pause: human prior can lengthen/shorten.
- diagnostic intent: test provisional qinist prior, not claim trained profile.

## 6. D_OUT_OF_DISTRIBUTION_DIAGNOSTIC

Intent: tries rhythm/style choices not covered by A/B/C to expose preference boundaries.

Parameters:

- tempo curve: intentionally wider range.
- phrase entry delay: diagnostic extremes within safe review bounds.
- intra-phrase variation: high but auditable.
- cadence hold: extended or compressed variants.
- tail duration: test tail boundary, still respecting no destructive trim unless explicitly marked.
- ornament duration: diagnostic over/under variants.
- yin/nao density: diagnostic density changes.
- silence after phrase: variable extremes.
- section transition pause: diagnostic contrast.
- diagnostic intent: reveal rejection patterns and boundary conditions.

## 7. Safety

ABCD strategy fields are planning parameters only. They do not authorize rendering, sample ingest, F rerun, or profile model creation.

