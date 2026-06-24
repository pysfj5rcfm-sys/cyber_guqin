# CG-REPO-HYGIENE-R2 Archive Dry-Run Proposal v0.1

Task: `CG-REPO-HYGIENE-R2_ARCHIVE_DRY_RUN_PROPOSAL`

Date: 2026-06-24

Mode: dry-run proposal only. No move, delete, archive, clean, renderer, ingest, ML, frontend build, backend script, second-piece, G, F2, or accepted F rerun command was run.

## Scope

This proposal reads the current R1/R0 authority docs and scans the requested areas:

- `reports/`
- `reports/archive/`
- `archive/`
- `04_outputs/xianwengcao/`
- `04_outputs/XWC/`
- `05_scripts/`
- `06_docs/`
- `tools/cg-varw/docs/`
- `tools/cg-varw/review_outputs/`
- `tools/cg-varw/sample_workspace/`
- `scripts/`

Only the six R2 proposal files were added under `reports/`.

## Authority Baseline

Current stage:

`XWC F reproduction ready / Sanman digitization startup`

Current engineering baseline:

`XWC / Xianwengcao / QINIST_002 Baiya / RS_XWC_002_BAIYA_PILOT / F_FINAL_REVIEWED`

Current mainline:

`QINIST_001 = Sanman digitization protocol, controlled fingering samples, ML-ready candidate sidecar`

Canonical R2 authority:

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`

Accepted baseline / forbidden-to-touch:

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`

R2 CSV/YAML exports beside the latest JSON remain derived exports, not canonical authority.

## Generated Manifests

| File | Purpose | Rows |
| --- | --- | ---: |
| `reports/repo_archive_candidate_manifest.v0.1.csv` | Archive candidates only; no action taken. | 7 |
| `reports/repo_delete_candidate_manifest.v0.1.csv` | Delete candidates only; no action taken. | 12 |
| `reports/repo_move_candidate_manifest.v0.1.csv` | Move candidates only; intentionally empty. | 0 |
| `reports/repo_forbidden_touch_manifest.v0.1.csv` | Protected paths/actions. | 6 |
| `reports/repo_archive_risk_matrix.v0.1.json` | Machine-readable risk and guardrail summary. | n/a |

## Disposition Summary

| Disposition | Count or Scope | Notes |
| --- | ---: | --- |
| `keep` | 12 groups | `.agents/skills/**`, `docs/cyber_guqin/**`, `examples/cyber_guqin/**`, `schemas/**`, `canon/**`, `sources/**`, `templates/**`, `tests/**`, root/current index docs, current generic P1-F helpers. |
| `index-only` | 7 groups | `reports/`, `reports/archive/`, `tools/cg-varw/docs/`, `06_docs/`, `05_scripts/`, historical scripts that remain useful evidence, R2 derived CSV/YAML beside latest JSON. |
| `archive-candidate` | 7 rows | Old runtime/dummy outputs, historical pre-fix F snapshot, older readiness/intake artifacts, large historical cleanup snapshot strata. |
| `move-candidate` | 0 rows | No move is recommended in this round. |
| `delete-candidate` | 12 rows | Ignored local generated artifacts only; no deletion performed. |
| `forbidden-to-touch` | 6 rows | Accepted baseline, protected sample indexes, protected future/restored paths. |
| `defer` | 6 groups | Current R2 latest JSON, current accepted baseline, root reports needing policy only, already archived reports, examples/docs/schemas/canon/source/test trees, ambiguous local workbench outputs until user approval. |

## Archive Candidates

The archive manifest proposes candidates only:

- `04_outputs/xianwengcao/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_intake/`
- `archive/xwc_mvp_file_audit_cleanup_20260621/`
- `archive/xwc_mvp_file_audit_cleanup_20260621/reports/archive/generated_validation/`
- `archive/xwc_mvp_file_audit_cleanup_20260621/reports/archive/staging/skill_install_staging/`

These are candidates for R2B review, not approvals to execute. The large `archive/xwc_mvp_file_audit_cleanup_20260621/` snapshot should be reviewed as a whole before any consolidation.

## Delete Candidates

The delete manifest is limited to local generated artifacts and ignored workbench outputs:

- `tools/cg-varw/backend/.venv/`
- `tools/cg-varw/frontend/node_modules/`
- `tools/cg-varw/frontend/dist/`
- `tools/cg-varw/frontend/node_modules/.vite/`
- backend `__pycache__/` groups
- backend `.venv` nested cache patterns
- `tools/cg-varw/review_outputs/r0/`
- `tools/cg-varw/review_outputs/r1/`

Observed ignore evidence:

- `tools/cg-varw/backend/.venv/` is ignored by root `.gitignore`.
- `tools/cg-varw/frontend/node_modules/` and `tools/cg-varw/frontend/dist/` are ignored by `tools/cg-varw/frontend/.gitignore`.
- `tools/cg-varw/review_outputs/**` is ignored except its tracked README and `.gitignore`.

No deletion was performed.

## Move Candidates

No move candidates are recommended. Moving files in this repo could blur authority boundaries unless a future task proves the move does not alter current authority.

Specifically, do not move accepted baseline, R2 latest, examples, docs, schemas, canon, sources, templates, or tests.

## Forbidden-To-Touch

Critical protected paths/actions:

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/`
- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl` if introduced
- `scripts/generate_baiya_recording_plan.py` if restored

The accepted baseline was not touched. The protected sample files were not written. The protected historical template path is absent in current HEAD and was not processed.

## Index-Only / Keep Notes

Keep protected source/evidence trees:

- `.agents/skills/**`
- `docs/cyber_guqin/**`
- `examples/cyber_guqin/**`
- `schemas/**`
- `canon/**`
- `sources/**`
- `templates/**`
- `tests/**`

Index-only evidence strata:

- `reports/*.md`, `reports/*.json`, `reports/*.csv`
- `reports/archive/2026-06/**`
- `tools/cg-varw/docs/*.md`
- `06_docs/*.md`
- historical scripts that remain useful evidence
- R2 derived CSV/YAML beside canonical latest JSON

These should not be treated as current runtime authority.

## Defer

Defer all action on:

- canonical R2 latest JSON and sibling derived exports, except documentation/index labeling
- accepted `F_FINAL_REVIEWED/` and `input_snapshot/`
- `reports/archive/2026-06/**` as already archived historical evidence
- `tools/cg-varw/sample_workspace/**` until demo fixture policy is separately reviewed
- `tools/cg-varw/review_outputs/README.md` and `.gitignore`
- any absent protected path if it appears later

## R2B Candidates

Candidates that can enter R2B human review:

- `04_outputs/xianwengcao/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_intake/`
- `archive/xwc_mvp_file_audit_cleanup_20260621/`
- ignored local generated artifacts listed in the delete manifest

R2B must remain a separate approval step and should first verify references, provenance, and current workflow usage.

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
