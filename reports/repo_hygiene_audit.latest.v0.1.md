# CG-REPO-HYGIENE-R0 Latest Readonly Audit v0.1

Audit date: 2026-06-24

Task: `CG-REPO-HYGIENE-R0_REFRESH_LATEST_STATE`

Mode: readonly audit. No checkout, pull, reset, stash, clean, renderer, ingest, ML, test, frontend build, backend script, second-piece, G, or F2 command was run.

## Git Baseline

| Field | Value |
| --- | --- |
| repo root | `D:/AIProjects/cyber_guqin/Cyber_Guqin_v1` |
| branch | `main` |
| HEAD | `4a549a33a8c29f627eaebe2856762879465c4e7d` |
| HEAD summary | `4a549a3 docs: freeze qinist starter kit design decisions` |
| initial working tree | clean by `git status --short --untracked-files=all` |

Latest five commits observed:

```text
4a549a3 docs: freeze qinist starter kit design decisions
3fabbd7 chore(reports): archive historical project reports
664f1e3 docs(qinist): design starter kit and Sanman instance artifacts
66e3962 fix(varw): harden R0/R1 export manifests and reload guards
a7615f2 docs(project): update current state and engineering backlog
```

## Executive Answer

Current repository **does contain the P1-F self-contained reproduction toolchain**. It is present as a dry-run-first, manifest/config-driven documentation and script set:

- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `examples/cyber_guqin/`
- `scripts/generate_recording_plan_from_dapu_ir.py`
- `scripts/render_abcd_from_manifest.py`
- `scripts/cyber_guqin_reproduction_lib.py`
- `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py`
- `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py`
- `tests/test_self_contained_reproduction_toolchain.py`

`docs/cyber_guqin/` exists. `examples/cyber_guqin/` exists.

The repository can proceed to `CG-REPO-HYGIENE-R1_INDEX_AND_POLICY_DOCS`. No blocker was found for an index/policy-doc-only R1. R1 should not move, delete, archive, or run workflow scripts; it should update documentation/index/policy labels only.

## P1-F Toolchain Verification

| Path | Exists | Status | Notes |
| --- | --- | --- | --- |
| `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md` | yes | keep | Defines Track A/B/C boundaries, R2 canonical authority, sample/ML/Arrangement gates, and stop rules. |
| `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md` | yes | keep | User-facing dry-run runbook; says accepted F must not be overwritten and dry-run does not read/write real audio binary. |
| `docs/cyber_guqin/SCRIPT_REGISTRY.md` | yes | keep | Classifies generic scripts vs historical XWC/Baiya scripts and human approval requirements. |
| `examples/cyber_guqin/` | yes | keep | Contains XWC reproduction manifests and qinist starter kit examples. |
| `scripts/generate_recording_plan_from_dapu_ir.py` | yes | keep | Generic dry-run-first recording plan generator. Docstring says it does not create raw-audio folders, sample ingest files, review data, or render outputs. |
| `scripts/render_abcd_from_manifest.py` | yes | keep | Generic ABCD metadata/sandbox planning tool. Dry-run default and no audio write in dry run. |
| `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py` | yes | keep / high-risk execute | Generic final reviewed render planning tool; protected by sandbox and accepted-baseline checks. |
| `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py` | yes | keep | Read-only manifest verifier; rejects derived CSV/YAML, Downloads, Blob, restore zip, and accepted baseline output root as authority. |
| `scripts/generate_baiya_recording_plan.py` | no | forbidden-to-touch if restored | Current HEAD does not contain it. If restored or untracked later, classify as protected historical template and do not process in hygiene tasks. |

The shared helper `scripts/cyber_guqin_reproduction_lib.py` includes explicit guard functions for derived authority names, forbidden authority markers, accepted-baseline output roots, and reproduction sandbox requirements.

## Authority Rules

Canonical R2 authority:

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`

Accepted baseline / forbidden-to-touch:

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/`

Derived or audit-only:

- R2 CSV/YAML exports such as `listening_review.csv`, `listening_review.yaml`, `issue_list.csv`, `preferred_version_summary.csv`, `phrase_structure_review.yaml`, `render_phrase_alignment.csv`, `phrase_boundary_decision.csv`, `render_revision_log.yaml`
- Reports under `reports/`
- Historical copies under `reports/archive/` and `archive/`

Protected sample/ingest files:

- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl` if introduced later

## Directory Classification

### V1 Runtime / Dapu Mode Spine

| Path | Classification | Notes |
| --- | --- | --- |
| `00_global/` | keep | V1 runtime ontology/config/qinist/piece data. |
| `01_pieces/` | keep | XWC piece data and rhythm candidates. |
| `02_recordings/` | keep | Raw/session recording evidence, including QINIST_001 and QINIST_002 session strata. |
| `03_samples/` | keep / forbidden write in hygiene | Existing sample assets and indexes. Do not write protected CSVs. |
| `04_outputs/` | mixed | Current XWC outputs, accepted F baseline, R2 review state, old xianwengcao outputs, generated render/readiness strata. |
| `05_scripts/` | keep / index-only | Phase 0.1 V1 runtime scripts; `render_audio.py` remains no-run in hygiene tasks. |
| `06_docs/` | index-only | Legacy V1 docs still useful but separate from new `docs/cyber_guqin/`. |

### Canon / Skills / Validator Engineering Tree

| Path | Classification | Notes |
| --- | --- | --- |
| `.agents/` | keep | Now includes `cyber_guqin_mvp_workflow` plus canon/parser skills. |
| `canon/` | keep | Canon seed/draft YAML. |
| `references/` | keep | Mapping/normalization/validation notes. |
| `schemas/` | keep | Expanded to starter/profile/prompt/sidecar schemas plus Dapu/canon schemas. |
| `scripts/` | keep / index-only | Validator, audit, generic P1-F reproduction, and historical helpers coexist; registry mitigates but does not remove overlap. |
| `sources/` | keep | QXBY source evidence. |
| `tests/` | keep | Fixtures plus `test_self_contained_reproduction_toolchain.py`; tests were not run. |
| `reports/` | index-only | Root contains current status reports and many design/toolchain reports; needs R1 index refresh. |

### P1-F Reproduction Toolchain

| Path | Classification | Notes |
| --- | --- | --- |
| `docs/cyber_guqin/` | keep | New runbook and script registry; missing in old R0, now present. |
| `examples/cyber_guqin/` | keep | New example manifests and qinist starter kit examples; missing in old R0, now present. |
| `scripts/generate_recording_plan_from_dapu_ir.py` | keep | Generic recording-plan dry-run/execute entry. |
| `scripts/render_abcd_from_manifest.py` | keep | Generic ABCD manifest planner. |
| `scripts/cyber_guqin_reproduction_lib.py` | keep | Shared authority/sandbox guard helpers. |
| `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py` | keep / high-risk execute | Generic final render planner; execute requires sandbox and human approval. |
| `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py` | keep | Read-only verifier. |

### CG-VARW Tool Tree

| Path | Classification | Notes |
| --- | --- | --- |
| `tools/cg-varw/backend/` | keep | Current FastAPI backend source, tests, scripts, and local `.venv`. |
| `tools/cg-varw/frontend/` | keep | Current Vite/React frontend source plus local `node_modules/` and `dist/`. |
| `tools/cg-varw/docs/` | index-only | Many chronological CG-VARW reports; still needs index/rollup. |
| `tools/cg-varw/review_outputs/` | keep generated ignored area | Local workbench outputs area; not canonical. |
| `tools/cg-varw/sample_workspace/` | keep fixture/demo | Synthetic demo raw/split workspace; non-canonical. |

### Historical / Generated / Derived Strata

| Path or Pattern | Classification | Notes |
| --- | --- | --- |
| `reports/archive/` | keep historical | Now organized under `reports/archive/2026-06/`; do not clean in R0. |
| `archive/` | archive-candidate | Large historical cleanup snapshot; no action without separate authorization. |
| `reports/*validate*.json` and similar generated reports | index-only | Report evidence, not runtime/canonical data. |
| `04_outputs/xianwengcao/` | archive-candidate | Old runtime/dummy render outputs; keep until policy authorizes archival. |
| `04_outputs/XWC/.../F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/` | archive-candidate | Historical pre-fix F snapshot, not accepted baseline. |
| `tools/cg-varw/backend/.venv/` | delete-candidate only under future cleanup | Local environment. Do not clean in this task. |
| `tools/cg-varw/frontend/node_modules/` | delete-candidate only under future cleanup | Local dependency install. Do not clean in this task. |
| `tools/cg-varw/frontend/dist/` | delete-candidate only under future cleanup | Local build artifact. Do not clean in this task. |
| `__pycache__/`, `*.pyc` | delete-candidate only under future cleanup | Local Python cache. Do not clean in this task. |

## Old R0 Judgments Now Outdated

- Old R0 said `docs/cyber_guqin/` was absent. It now exists.
- Old R0 said `examples/cyber_guqin/` was absent. It now exists.
- Old R0 treated the P1-F reproduction toolchain as not yet present or not yet confirmed. It is now present in docs, examples, skill, generic scripts, and test coverage.
- Old R0 said root README was Phase 0.1-only/outdated. It is now updated to current state and lists the P1-F toolchain, though terminal output still shows mojibake/encoding display issues.
- Old R0 counted fewer schemas/scripts/reports/examples. Latest tree has expanded schemas, generic scripts, starter-kit examples, and reports.

## Old R0 Conclusions Still Valid

- Accepted `F_FINAL_REVIEWED/` remains `forbidden-to-touch`.
- `r2_review_state.latest.json` remains the R2 canonical authority.
- CSV/YAML R2 exports remain derived and must not be promoted to canonical.
- `reports/`, `reports/archive/`, `archive/`, local build artifacts, `.venv`, `node_modules`, `dist`, and pycache should not be cleaned in this audit.
- `05_scripts/`, `scripts/`, and `tools/cg-varw/backend/scripts/` remain overlapping script trees and need index labels.
- `REPORTS_INDEX.md` remains too coarse for the current report root and archive layout.
- Root `.gitignore` still has duplicate patterns and does not centrally document all local generated artifact policy.

## Current Hygiene Findings

1. P1-F reproduction toolchain is complete enough for documentation/index policy work.
2. The toolchain is dry-run-first and metadata/sandbox oriented; it is not a real renderer, sample ingest path, ML path, or second-piece execution.
3. `docs/cyber_guqin/SCRIPT_REGISTRY.md` reduces script ambiguity, but R1 should connect it from root docs and reports index.
4. `reports/REPORTS_INDEX.md` has not caught up with `reports/archive/2026-06/`, P1-F reports, starter-kit reports, and toolchain reports.
5. Root `README.md` content is current in substance but still displays as mojibake in PowerShell output, suggesting an encoding/display issue or non-UTF-8 terminal mismatch.
6. Local artifact directories are present: backend `.venv`, frontend `node_modules`, frontend `dist`, and many pycache entries. They are classification evidence only.
7. Duplicate basename hotspots remain high for R2 review exports: `r2_review_state.latest.json` and companion CSV/YAML files appear many times because active and archived snapshots coexist.

## Candidate Actions By Disposition

| Disposition | Paths |
| --- | --- |
| keep | `.agents/skills/cyber_guqin_mvp_workflow/`, `docs/cyber_guqin/`, `examples/cyber_guqin/`, `scripts/generate_recording_plan_from_dapu_ir.py`, `scripts/render_abcd_from_manifest.py`, `scripts/cyber_guqin_reproduction_lib.py`, `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py`, `00_global/`, `01_pieces/`, `canon/`, `schemas/`, `sources/`, `templates/`, `tests/fixtures/` |
| index-only | `README.md`, `06_docs/`, `reports/`, `reports/REPORTS_INDEX.md`, `tools/cg-varw/docs/`, `05_scripts/`, historical scripts in `scripts/` |
| archive-candidate | `04_outputs/xianwengcao/`, `04_outputs/XWC/.../F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/`, `archive/xwc_mvp_file_audit_cleanup_20260621/` |
| move-candidate | none recommended for immediate R1; possible future docs consolidation only after policy |
| delete-candidate | `tools/cg-varw/backend/.venv/`, `tools/cg-varw/frontend/node_modules/`, `tools/cg-varw/frontend/dist/`, pycache; classification only, do not delete now |
| forbidden-to-touch | `04_outputs/XWC/.../F_FINAL_REVIEWED/`, `03_samples/sample_assets.csv`, `03_samples/recording_segments.csv`, `recording_items_enriched.jsonl` if present, `scripts/generate_baiya_recording_plan.py` if restored |

## R1 Recommendation

Proceed to `CG-REPO-HYGIENE-R1_INDEX_AND_POLICY_DOCS` with this scope:

- Refresh `reports/REPORTS_INDEX.md`.
- Add or update index/policy docs for `docs/cyber_guqin/`, `06_docs/`, `tools/cg-varw/docs/`, and script categories.
- Add explicit authority labels: canonical JSON, derived CSV/YAML, generated report, historical archive, accepted baseline.
- Keep R1 read/write limited to docs/index/policy files.
- Do not move/delete/archive files in R1 unless a separate cleanup authorization is opened.

No blocker found for R1 index/policy docs.
