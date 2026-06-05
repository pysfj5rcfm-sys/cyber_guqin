# Reports Index

`reports/` root keeps current status entry reports only.

`reports/archive/` stores historical audit reports, old batch reports, generated validation outputs, and completed staging artifacts.

## Archive Layout

- `reports/archive/phase_s0_skills/`: Skills Foundation historical reports.
- `reports/archive/qxby_batch_001/`: QXBY_BATCH_001 ingest, source audit, and batch validation reports.
- `reports/archive/generated_validation/`: Regenerable JSON reports produced by validators.
- `reports/archive/staging/`: Completed installation staging artifacts.
- `reports/archive/phase_2a_canon_seed/`: Reserved for future Phase 2A canon seed archive material.

## Operating Rules

- Validator runs may recreate JSON reports in `reports/` root. This is expected behavior for the current validator scripts.
- Regenerated validator JSON can be archived again under `reports/archive/generated_validation/`.
- Do not treat `reports/` as runtime output.
- Audio rendering outputs belong to `04_outputs/`, not `reports/`.
