# CG-REPO-HYGIENE-R2B Reference Review and Execution Plan Dry Run v0.1

Task: `CG-REPO-HYGIENE-R2B_REFERENCE_AND_EXECUTION_PLAN_DRY_RUN`

Date: 2026-06-24

Mode: reference review and execution plan only. No move, delete, archive, clean, renderer, ingest, ML, frontend build, backend script, second-piece, G, F2, or accepted F rerun command was run.

## Inputs Read

- `reports/repo_archive_dry_run_proposal.v0.1.md`
- `reports/repo_archive_candidate_manifest.v0.1.csv`
- `reports/repo_delete_candidate_manifest.v0.1.csv`
- `reports/repo_move_candidate_manifest.v0.1.csv`
- `reports/repo_forbidden_touch_manifest.v0.1.csv`
- `reports/repo_archive_risk_matrix.v0.1.json`
- `README.md`
- `06_docs/PROJECT_STRUCTURE.md`
- `reports/REPORTS_INDEX.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `scripts/README.md`
- `tools/cg-varw/backend/scripts/README.md`

## Generated Reports

| File | Purpose |
| --- | --- |
| `reports/repo_archive_r2b_reference_review.v0.1.md` | Human-readable R2B review summary. |
| `reports/repo_archive_r2b_execution_plan.DRY_RUN.v0.1.csv` | Archive/consolidation execution dry-run decisions. |
| `reports/repo_archive_r2b_delete_plan.DRY_RUN.v0.1.csv` | Delete/local-cleanup dry-run decisions. |
| `reports/repo_archive_r2b_defer_manifest.v0.1.csv` | Deferred candidate blockers and next review conditions. |
| `reports/repo_archive_r2b_reference_matrix.v0.1.json` | Machine-readable reference and decision matrix. |

## Archive Candidate Review

| Candidate | Reference status | Decision | Reason |
| --- | --- | --- | --- |
| `04_outputs/xianwengcao/` | `current-doc-reference` | `defer` | Referenced by tracked readiness/provenance artifacts, including `abcd_render_input_manifest.json` and `abcd_render_readiness_report.md`; do not archive separately while readiness provenance remains in place. |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/` | `authority-reference` | `defer` | Referenced by accepted F audit/input snapshot and canonical R2 latest JSON as an `archive_path`; also referenced by historical repair script. |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/` | `current-script-reference` | `defer` | Referenced by `_planning/render_source_map.local.json` and `scripts/render_xwc_abcd_from_planning.py`. |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_intake/` | `current-script-reference` | `defer` | Referenced by current backend discovery, backend tests, README examples, and historical F scripts. |
| `archive/xwc_mvp_file_audit_cleanup_20260621/` | `historical-reference-only` | `cancel` | Already under `archive/`; an in-repo re-archive would churn historical archive references without improving authority hygiene. |
| `archive/xwc_mvp_file_audit_cleanup_20260621/reports/archive/generated_validation/` | `historical-reference-only` | `subsumed-by-parent` | Child path is covered by the parent archive snapshot; do not execute independently. |
| `archive/xwc_mvp_file_audit_cleanup_20260621/reports/archive/staging/skill_install_staging/` | `historical-reference-only` | `subsumed-by-parent` | Child path is covered by the parent archive snapshot; do not execute independently. |

R2C should not perform archive moves from this set unless a later task retires or maps the blocking references.

## Delete Candidate Review

| Candidate | Tracked status | Ignored status | Reference status | Decision |
| --- | --- | --- | --- | --- |
| `tools/cg-varw/backend/.venv/` | `untracked-ignored` | root `.gitignore` | `no-current-reference` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/frontend/node_modules/` | `untracked-ignored` | frontend `.gitignore` | `no-current-reference` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/frontend/dist/` | `untracked-ignored` | frontend `.gitignore` | `historical-reference-only` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/frontend/node_modules/.vite/` | `untracked-ignored` | frontend `node_modules/` rule | `no-current-reference` | `subsumed-by-parent` |
| `tools/cg-varw/backend/app/__pycache__/` | `untracked-ignored` | root `__pycache__/` rule | `no-current-reference` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/backend/app/api/__pycache__/` | `untracked-ignored` | root `__pycache__/` rule | `no-current-reference` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/backend/app/services/__pycache__/` | `untracked-ignored` | root `__pycache__/` rule | `no-current-reference` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/backend/app/tests/__pycache__/` | `untracked-ignored` | root `__pycache__/` rule | `no-current-reference` | `approved-for-future-local-cleanup` |
| `tools/cg-varw/backend/.venv/**/__pycache__/` | `untracked-ignored` | parent `.venv/` | `no-current-reference` | `subsumed-by-parent` |
| `tools/cg-varw/backend/.venv/**/*.pyc` | `untracked-ignored` | parent `.venv/` | `no-current-reference` | `subsumed-by-parent` |
| `tools/cg-varw/review_outputs/r0/` | `untracked-ignored` | `review_outputs/.gitignore` | `authority-reference` | `defer` |
| `tools/cg-varw/review_outputs/r1/` | `untracked-ignored` | `review_outputs/.gitignore` | `authority-reference` | `defer` |

Delete candidates are local cleanup suggestions only. They must not become git commit deletions unless a future scan proves tracked files are involved and the user explicitly authorizes that specific deletion.

## Future R2C Eligibility

Eligible for future R2C local cleanup only, with explicit user approval:

- `tools/cg-varw/backend/.venv/`
- `tools/cg-varw/frontend/node_modules/`
- `tools/cg-varw/frontend/dist/`
- `tools/cg-varw/backend/app/__pycache__/`
- `tools/cg-varw/backend/app/api/__pycache__/`
- `tools/cg-varw/backend/app/services/__pycache__/`
- `tools/cg-varw/backend/app/tests/__pycache__/`

Subsumed local cleanup items:

- `tools/cg-varw/frontend/node_modules/.vite/`
- `tools/cg-varw/backend/.venv/**/__pycache__/`
- `tools/cg-varw/backend/.venv/**/*.pyc`

## Must Defer

- `04_outputs/xianwengcao/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_intake/`
- `tools/cg-varw/review_outputs/r0/`
- `tools/cg-varw/review_outputs/r1/`

## Cancel / Do Not Execute Independently

- `archive/xwc_mvp_file_audit_cleanup_20260621/`: cancel in-repo re-archive; already under archive.
- `archive/xwc_mvp_file_audit_cleanup_20260621/reports/archive/generated_validation/`: subsumed by parent.
- `archive/xwc_mvp_file_audit_cleanup_20260621/reports/archive/staging/skill_install_staging/`: subsumed by parent.

## Non-Actions Confirmed

- No file was moved.
- No file was deleted.
- No file was archived.
- No clean command was run.
- No renderer was run.
- No ingest was run.
- No ML workflow was run.
- No frontend build was run.
- No backend script was run.
- No second-piece, G, F2, or accepted F rerun was started.
- Accepted `F_FINAL_REVIEWED/` was not touched.
- `03_samples/sample_assets.csv`, `03_samples/recording_segments.csv`, and `recording_items_enriched.jsonl` were not written.
- `scripts/generate_baiya_recording_plan.py` is absent in current HEAD and was not processed.
