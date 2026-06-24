# Cyber Guqin v1 Project Structure

Cyber Guqin v1 intentionally keeps two main tracks side by side: the V1 runtime / Dapu Mode spine, and the canon / skills / validator engineering tree. P1-F reproduction docs and CG-VARW live near those tracks but have their own safety boundaries.

Current stage: `XWC F reproduction ready / Sanman digitization startup`.

Current engineering baseline: `XWC / 《仙翁操》 / QINIST_002 白牙 / RS_XWC_002_BAIYA_PILOT / F_FINAL_REVIEWED`.

Current mainline: `QINIST_001` Sanman digitization protocol, controlled fingering samples, and ML-ready candidate sidecar design. This is not second-piece execution, sample ingest, ML training, Arrangement Mode production, or accepted F rerun.

## 1. V1 Runtime / Dapu Mode Spine

- `00_global/`: V1 runtime global ontology, qinist, piece, tuning, schema contract, parse rules, gesture templates, and components.
- `01_pieces/`: Piece data. Current baseline piece is XWC / 《仙翁操》.
- `02_recordings/`: Recording sessions and raw/review evidence, including QINIST_001 and QINIST_002 strata.
- `03_samples/`: Sample assets and indexes. Hygiene tasks must not write `sample_assets.csv`, `recording_segments.csv`, or future `recording_items_enriched.jsonl`.
- `04_outputs/`: Runtime/render/review outputs. This is a mixed-risk area, not a generic reports folder.
- `05_scripts/`: V1 runtime scripts for old recording, sampling, rhythm, render, smoke-test, and related workflows.
- `06_docs/`: Legacy V1 documentation and project-structure/index docs.

These folders are the runtime-facing spine. Canon drafts and report evidence must not quietly redefine their data contracts.

## 2. Canon / Skills / Validator Engineering Tree

- `.agents/`: Codex agent assets and workflow skills, including `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`.
- `canon/`: Canon seed files and draft YAML.
- `references/`: Mapping, normalization, and validation notes.
- `schemas/`: Dapu, canon, starter/profile/prompt/sidecar schemas.
- `scripts/`: Validator, audit, generic P1-F reproduction helpers, split/recording helpers, and historical scripts.
- `sources/`: Source evidence such as archived QXBY material.
- `tests/`: Fixtures and toolchain tests.
- `reports/`: Audit, status, design, validation, and reproduction evidence. `reports/` is not runtime output and not canonical authority.

This tree supports canon engineering and non-invasive validation. It can inform future verified canon work, but it does not directly patch V1 runtime files.

## 3. P1-F Reproduction Toolchain

- `docs/cyber_guqin/`: Current P1-F runbook and script registry.
- `examples/cyber_guqin/`: Example manifests, fixtures, and starter-kit mock examples.
- `scripts/generate_recording_plan_from_dapu_ir.py`: Generic dry-run-first recording plan helper.
- `scripts/render_abcd_from_manifest.py`: Generic dry-run-first ABCD metadata/sandbox planner.
- `scripts/cyber_guqin_reproduction_lib.py`: Shared authority and sandbox guard helpers.
- `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py`: Generic final reviewed render planner; execute is high-risk and must use sandbox plus explicit approval.
- `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py`: Read-only R2/final manifest verifier.

This toolchain reproduces the engineering path by dry-run/default metadata planning. It is not a true audio renderer, not sample ingest, not ML, and not second-piece production.

## 4. CG-VARW Tool Tree

- `tools/cg-varw/backend/`: FastAPI backend, tests, scripts, and local backend workspace.
- `tools/cg-varw/frontend/`: Vite/React frontend. Frontend build artifacts such as `dist/` are local generated artifacts, not canonical data.
- `tools/cg-varw/docs/`: Chronological CG-VARW design, contract, patch, and implementation reports. Use `tools/cg-varw/docs/INDEX.md` for current rollup.
- `tools/cg-varw/review_outputs/`: Generated non-canonical local workbench outputs. Do not treat these as R2 authority.
- `tools/cg-varw/sample_workspace/`: Synthetic demo workspace and fixtures, not production authority.

## 5. Authority and Derived Data

- Accepted baseline / forbidden-to-touch: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- R2 canonical authority: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML files beside the latest JSON are derived exports. Do not promote `listening_review.csv`, `listening_review.yaml`, `issue_list.csv`, `preferred_version_summary.csv`, `phrase_structure_review.yaml`, `render_phrase_alignment.csv`, `phrase_boundary_decision.csv`, or `render_revision_log.yaml` to canonical authority.
- `reports/` and `reports/archive/` are audit/status evidence, not runtime output and not canonical authority.
- `archive/` is historical cleanup evidence. Do not clean, move, delete, or re-archive it without a separate task.

## 6. Script Tree Boundary

`05_scripts/` is the legacy V1 runtime script tree.

`scripts/` is the engineering/helper script tree for validators, audits, generic P1-F reproduction helpers, split/recording helpers, and historical templates.

`tools/cg-varw/backend/scripts/` sits closest to R2/F/final-reviewed render behavior and carries higher risk. Use `tools/cg-varw/backend/scripts/README.md` before treating any file there as an entry point.

## 7. Current Hygiene Rules

- Do not rename the `00_*` directories.
- Do not mix canon drafts into `00_global/`.
- Do not place source screenshots in `canon/`.
- Do not treat `reports/` as runtime output.
- Do not treat generated reports, archive snapshots, CSV/YAML exports, or CG-VARW workbench outputs as canonical authority.
- Do not touch accepted `F_FINAL_REVIEWED/` without a separate accepted-baseline task.
- Do not run renderer, ingest, ML, frontend build, backend scripts, second-piece, G, or F2 workflows during repo hygiene index/policy tasks.
- Do not process `scripts/generate_baiya_recording_plan.py`; it is absent in current HEAD, and if restored it is a protected historical template / forbidden-to-touch.
