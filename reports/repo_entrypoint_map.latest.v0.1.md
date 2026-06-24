# Repo Entrypoint Map Latest v0.1

Audit date: 2026-06-24

This file maps current entrypoints in HEAD `4a549a33a8c29f627eaebe2856762879465c4e7d`. It is descriptive only. No entrypoint was executed.

## P1-F Self-Contained Reproduction Entrypoints

| Path | Type | Purpose | Current? | Default safety | Canonical/Generated Status | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md` | Skill docs | Workflow gates from dapu intake to F audition and future candidate gates. | yes | stop-rule driven | policy authority | keep |
| `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md` | Markdown | User-facing XWC F dry-run reproduction runbook. | yes | dry-run-first, no accepted F overwrite | docs authority | keep |
| `docs/cyber_guqin/SCRIPT_REGISTRY.md` | Markdown | Script status/safety registry. | yes | classifies dry-run, execute, historical, high-risk | registry authority | keep |
| `examples/cyber_guqin/xwc_recording_plan_config.yaml` | JSON-compatible YAML | Recording plan config example. | yes | dry-run default, not sample/ML | example manifest | keep |
| `examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl` | JSONL | Minimal Dapu IR fixture for reproduction. | yes | fixture only | example/fixture | keep |
| `examples/cyber_guqin/xwc_abcd_render_manifest.yaml` | JSON-compatible YAML | ABCD render planning manifest. | yes | output under reproduction sandbox; derived outputs labeled | example manifest | keep |
| `examples/cyber_guqin/xwc_r2_render_verify_manifest.yaml` | JSON-compatible YAML | R2/final verifier manifest. | yes | rejects derived/forbidden authorities | example manifest | keep |
| `examples/cyber_guqin/xwc_final_render_manifest.yaml` | JSON-compatible YAML | Final reviewed render manifest. | yes | accepted baseline guard, sandbox required for execute | example manifest | keep |
| `scripts/generate_recording_plan_from_dapu_ir.py` | Python CLI | Generic recording plan generator from Dapu IR. | yes | dry-run-first; no raw/sample/review/render outputs by default | source entrypoint | keep |
| `scripts/render_abcd_from_manifest.py` | Python CLI | Generic ABCD manifest planner/materializer for sandbox metadata. | yes | dry-run default; no real audio render in generic tool | source entrypoint | keep |
| `scripts/cyber_guqin_reproduction_lib.py` | Python library | Shared manifest loading, authority guards, sandbox guards, write helpers. | yes | rejects accepted baseline and derived authority misuse | source helper | keep |
| `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py` | Python CLI | Generic final reviewed render planner/materializer. | yes | dry-run default; execute must use `reproduction_runs` sandbox | high-risk source entrypoint | keep |
| `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py` | Python CLI | Read-only verifier for R2/final manifest authority. | yes | read-only validation, no audio write | source entrypoint | keep |
| `tests/test_self_contained_reproduction_toolchain.py` | Python test | Test coverage for reproduction toolchain. | yes | not run in this audit | test source | keep |

## CG-VARW Runtime Entrypoints

| Path | Type | Purpose | Current? | Disposition |
| --- | --- | --- | --- | --- |
| `tools/cg-varw/backend/app/main.py` | FastAPI app | Backend app root. | yes | keep |
| `tools/cg-varw/backend/app/api/health.py` | FastAPI router | Health API. | yes | keep |
| `tools/cg-varw/backend/app/api/r0_raw_files.py` | FastAPI router | R0 raw files/metadata/audio/waveform/asr/review-unit APIs. | yes | keep |
| `tools/cg-varw/backend/app/api/r0_reviews.py` | FastAPI router | R0 review save/export APIs. | yes | keep |
| `tools/cg-varw/backend/app/api/r1_split_review.py` | FastAPI router | R1 split review APIs. | yes | keep |
| `tools/cg-varw/backend/app/api/r2_phrase_review.py` | FastAPI router | R2 render-set/phrase review APIs. | yes | keep |
| `tools/cg-varw/frontend/package.json` | npm config | Frontend `dev`, `build`, `typecheck` scripts. | yes | keep; do not run in R0 |
| `tools/cg-varw/frontend/vite.config.ts` | TS config | Vite config. | yes | keep |
| `tools/cg-varw/frontend/src/main.tsx` | TSX | React mount entry. | yes | keep |
| `tools/cg-varw/frontend/src/App.tsx` | TSX | R0/R1/R2 app mode shell. | yes | keep |
| `tools/cg-varw/frontend/src/pages/R0RawReviewPage.tsx` | TSX | R0 review page. | yes | keep |
| `tools/cg-varw/frontend/src/pages/R1SplitReviewPage.tsx` | TSX | R1 review page. | yes | keep |
| `tools/cg-varw/frontend/src/pages/R2ProjectReviewPage.tsx` | TSX | R2 project review page. | yes | keep |

## Validator / Audit Entrypoints

| Path | Purpose | Current? | Writes? | Disposition |
| --- | --- | --- | --- | --- |
| `scripts/validate_canon.py` | Canon validation. | yes | report/stdout depending script behavior | keep |
| `scripts/validate_canon_seed.py` | Canon seed validation. | yes | report/stdout depending script behavior | keep |
| `scripts/validate_dapu_ir.py` | Dapu IR validation. | yes | report/stdout depending script behavior | keep |
| `scripts/validate_qxby_batch.py` | QXBY draft validation. | yes | report/stdout depending script behavior | keep |
| `scripts/check_v1_compat.py` | V1 compatibility check. | yes | report/stdout depending script behavior | keep |
| `scripts/audit_qxby_batch_sources.py` | Source-image archive audit. | yes | report artifacts | keep |
| `scripts/audit_recording_ingest_readiness.py` | Recording/sample ingest readiness audit. | yes | report artifacts | keep |
| `scripts/audit_v1_to_canon_coverage.py` | V1-to-canon coverage audit. | yes | report artifacts | keep |
| `scripts/build_xwc_legacy_bridge_preview.py` | XWC legacy bridge preview. | historical | preview reports | index-only |

## V1 Runtime / Legacy Entrypoints

| Path | Purpose | Current? | Risk | Disposition |
| --- | --- | --- | --- | --- |
| `05_scripts/smoke_test.py` | V1 dummy pipeline smoke test. | legacy/runtime | writes/runs pipeline scripts | index-only; do not run in R0 |
| `05_scripts/generate_recording_script.py` | Generate XWC recording script. | legacy/runtime | writes runtime docs/csv | index-only |
| `05_scripts/generate_rhythm.py` | Generate rhythm candidates. | legacy/runtime | writes runtime candidates | index-only |
| `05_scripts/make_dummy_samples.py` | Generate dummy sample WAVs. | legacy/runtime | writes WAV/sample data | forbidden in R0 |
| `05_scripts/render_audio.py` | Render dummy/runtime audio. | legacy/runtime | renderer-like writes | forbidden-to-touch in R0 |
| `05_scripts/export_recording_checklist.py` | Export recording checklist. | legacy/runtime | writes checklist | index-only |
| `05_scripts/audio_viability_review.py` | Audio viability report. | legacy/runtime | reads/writes output reports | index-only |

## Historical / High-Risk XWC/Baiya Scripts

| Path | Registry Status | Risk | Disposition |
| --- | --- | --- | --- |
| `scripts/generate_baiya_recording_plan.py` | protected historical template if restored | currently missing; do not process if restored | forbidden-to-touch |
| `scripts/render_xwc_abcd_from_planning.py` | historical-only template | reads/writes audio and render outputs | index-only; do not execute |
| `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py` | historical XWC F generator | reads/writes audio, latest/review entries, F outputs | index-only; do not execute |
| `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py` | historical-only repair/regeneration | rewrites R1/F/latest/derived outputs | index-only; do not execute |
| `tools/cg-varw/backend/scripts/verify_r2_canonical_draft.py` | older R2 verifier | mostly superseded by generic verifier | index-only |
| `scripts/slate_based_experimental_split.py` | historical-only / needs review | may read/write split artifacts | archive-candidate with approval |
| `scripts/slate_number_recognizer.py` | reusable with explicit inputs | may inspect raw metadata/audio depending task | keep / index-only |
| `scripts/trim_clean_experimental_segments.py` | reusable with caution | may read/write preview audio with execute | keep / index-only |
| `scripts/finalize_reviewed_unit_previews.py` | reusable with caution | may read/write preview artifacts with execute | keep / index-only |
| `scripts/register_mvp_pilot_raw_audio.py` | historical MVP pilot helper | raw audio registration | index-only |
| `scripts/split_framework_common.py` | helper library | low direct risk | keep |

## Markdown / YAML / JSON Authority Map

| Path | Authority Status | Disposition |
| --- | --- | --- |
| `README.md` | current project overview, but terminal display shows mojibake | index-only |
| `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md` | current P1-F runbook | keep |
| `docs/cyber_guqin/SCRIPT_REGISTRY.md` | current script safety registry | keep |
| `reports/REPORTS_INDEX.md` | report/archive index, currently too coarse for latest state | index-only |
| `reports/self_contained_reproduction_toolchain_report.md` | P1-F report evidence | index-only |
| `reports/qinist_*`, `reports/*starter*`, `reports/*sidecar*` | Sanman/Qinist starter design reports | index-only |
| `schemas/*starter*`, `schemas/*sidecar*`, `schemas/*prompt*`, `schemas/*profile*` | starter/profile/sidecar schema drafts | keep |
| `examples/cyber_guqin/*.yaml`, `examples/cyber_guqin/*.jsonl` | example manifests/fixtures | keep |
| `canon/*.yaml`, `canon/drafts/*.yaml` | canon seed/draft data | keep |
| `00_global/*.yaml`, `00_global/*.csv` | V1 runtime data | keep |
| `schemas/*.schema.json`, `schemas/*.draft.yaml` | schema authority/drafts | keep |
| `tests/fixtures/*` | test fixtures | keep |
| `sources/qinxue_beiyao/*/manifest.yaml` | source evidence manifests | keep |
| `04_outputs/XWC/.../r2_review_drafts/latest/r2_review_state.latest.json` | canonical R2 latest JSON | keep |
| `04_outputs/XWC/.../r2_review_drafts/latest/*.csv`, `*.yaml` | derived R2 exports | index-only |
| `04_outputs/XWC/.../F_FINAL_REVIEWED/*` | accepted baseline evidence | forbidden-to-touch |
| `reports/archive/**` | historical report evidence | keep historical |
| `archive/**` | historical cleanup snapshot | archive-candidate, no action |

## Old R0 Delta

Obsolete:

- `docs/cyber_guqin/` missing.
- `examples/cyber_guqin/` missing.
- P1-F reproduction toolchain not confirmed.
- Root README only reflected old Phase 0.1/dummy-audio state.

Still valid:

- Accepted `F_FINAL_REVIEWED/` is forbidden-to-touch.
- `r2_review_state.latest.json` is canonical.
- CSV/YAML exports are derived.
- Reports/archive/local artifacts should be classified before cleanup.
- Script-tree overlap needs index/policy documentation.

## R1 Readiness

Status: ready for `CG-REPO-HYGIENE-R1_INDEX_AND_POLICY_DOCS`.

Blocker: none for index/policy-only R1.

R1 should update indexes and policy docs only. It should not move, delete, archive, clean, run tests, build frontend, execute backend scripts, render, ingest, train, or start second-piece production.
