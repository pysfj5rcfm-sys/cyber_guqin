# P1-P6 Reindexed Regression Report v0.2

Status labels: `LXY_TRANSCRIPTION_DRAFT`, `REGRESSION_GOLDSET_FOR_DRAFT_REPLAY`, `CATEGORY_REINDEXED_COMPONENT_IDS`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`

## Result

- P1-P6 reindexed regression prevalidation: `PASS`
- Component match cases: `4`
- Construction template cases: `21`
- Phrase integration cases: `6`
- Forbidden output cases: `23`
- Forbidden evaluation mode: `scoped_component_or_template_context`
- Global literal forbidden scan: `false`

These fixtures are replay guardrails only. They are not canon authority, not score-event authority, and not Dapu IR authority.

Forbidden-output checks are evaluated only when the matched component, template, or phrase context intersects the case scope. A `forbidden_output` literal is not a global banned string.

In particular:

- `FORBID-JIU-AS-SHAOXI` applies to `COMP-907` / `就` and forbids outputting `少息` only under that scoped context.
- `FORBID-SHAOXI-AS-JIU` applies to `COMP-806` / `少息` and forbids outputting `就` only under that scoped context.
- Legal `少息` remains legal when the matched component is `COMP-806` / `少息`.
- Legal `就` remains legal when the matched component is `COMP-907` / `就`.
- If a forbidden output appears outside its scoped component/template/phrase context, it is not a regression failure.

## Validation

- JSON validation: `PASS`
- Reindexed fixture sanity: `PASS`
- Scoped forbidden semantics: `PASS`
- Primary fixture IDs use `category_based_v0_2`; legacy and v0.1 source IDs remain traceability-only.
