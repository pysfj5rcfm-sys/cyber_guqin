# Reports Cleanup Plan

Phase R2 is a lightweight reports and staging cleanup. It does not modify V1 runtime data, canon data, source evidence, schemas, validator logic, or test fixtures.

## Current Reports Audit

Current status entry reports to keep in `reports/` root:

- `reports/architecture_review.md`
- `reports/architecture_inventory.json`
- `reports/slimming_recommendations.md`
- `reports/validator_parameterization_report.md`
- `reports/canon_seed_report.md`
- `reports/qxby_batch_001_human_review.md`
- `reports/reports_cleanup_plan.md`
- `reports/REPORTS_INDEX.md`

Historical Skills Foundation reports:

- `reports/skills_v1_integration_report.md`
- `reports/v1_compat_audit.md`
- `reports/skill_install_instructions.md`

Regenerable validator JSON:

- `reports/check_v1_compat_report.json`
- `reports/validate_canon_report.json`
- `reports/validate_canon_seed_report.json`
- `reports/validate_dapu_ir_report.json`

Batch-specific QXBY_BATCH_001 reports:

- `reports/qxby_batch_001_report.md`
- `reports/qxby_batch_001_source_audit.md`
- `reports/qxby_batch_001_source_audit.json`
- `reports/validate_qxby_batch_001_report.json`

Completed skill install staging:

- `reports/skill_install_staging/guqin-canon-builder/SKILL.md`
- `reports/skill_install_staging/guqin-dapu-parser/SKILL.md`

## Archive Directories To Create

- `reports/archive/`
- `reports/archive/phase_s0_skills/`
- `reports/archive/phase_2a_canon_seed/`
- `reports/archive/qxby_batch_001/`
- `reports/archive/generated_validation/`
- `reports/archive/staging/`

## Planned Moves

Move historical Skills Foundation reports to `reports/archive/phase_s0_skills/`:

- `reports/skills_v1_integration_report.md`
- `reports/v1_compat_audit.md`
- `reports/skill_install_instructions.md`

Move completed skill install staging to `reports/archive/staging/skill_install_staging/`, because both installed skill files are present under `.agents/skills/`:

- `.agents/skills/guqin-canon-builder/SKILL.md`
- `.agents/skills/guqin-dapu-parser/SKILL.md`

Move QXBY_BATCH_001 batch reports to `reports/archive/qxby_batch_001/`:

- `reports/qxby_batch_001_report.md`
- `reports/qxby_batch_001_source_audit.md`
- `reports/qxby_batch_001_source_audit.json`
- `reports/validate_qxby_batch_001_report.json`

Move regenerable validator JSON to `reports/archive/generated_validation/`:

- `reports/check_v1_compat_report.json`
- `reports/validate_canon_report.json`
- `reports/validate_canon_seed_report.json`
- `reports/validate_dapu_ir_report.json`

## Planned Root Keeps

- `reports/architecture_review.md`
- `reports/architecture_inventory.json`
- `reports/slimming_recommendations.md`
- `reports/validator_parameterization_report.md`
- `reports/canon_seed_report.md`
- `reports/qxby_batch_001_human_review.md`
- `reports/reports_cleanup_plan.md`
- `reports/REPORTS_INDEX.md`
- `reports/reports_cleanup_summary.md`

## Skips And Warnings

- `reports/archive/phase_2a_canon_seed/` will be created for policy consistency, but no files are currently planned for it.
- `reports/canon_seed_report.md` stays in root because it remains the current canon seed entry report.
- Missing candidate files will be skipped without error.
- No file deletion is planned.
