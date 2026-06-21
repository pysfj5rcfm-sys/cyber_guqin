# VARW R0/R1/R2 Export Contract Audit Dry Run

- Task: `CG-XWC-MVP-P1A_VARW_R012_EXPORT_CONTRACT_AUDIT_DRY_RUN`
- Phase: Phase 1F-XWC-MVP Passed / Sweep & Review
- Mode: audit/design only; no patch, no refactor, no export behavior change.
- Generated: 2026-06-21

## Scope

本轮只做 metadata/path 级审计，读取 `tools/cg-varw` 后端/前端入口、允许的 R0/R1/R2/F 元数据目录、以及指定报告。未读取 raw master audio binary、split preview wav、F wav、Downloads、restore zip、browser Blob、node_modules、`.venv`、build caches，也未读取 archived old exports 作为 source of truth。

本轮只允许新增：

- `reports/varw_r012_export_contract_audit.DRY_RUN.md`
- `reports/varw_r012_export_contract_design.v0.1.md`

## Git Status

审计开始时：

```text
?? scripts/generate_baiya_recording_plan.py
```

该脚本是既有未跟踪文件，本轮未读取、未处理、未修改。

## Current Entry Table

| Stage | Entry | Code path | Current behavior |
| --- | --- | --- | --- |
| R0 | raw listing | `tools/cg-varw/backend/app/api/r0_raw_files.py` -> `scan_raw_files()` | `GET /api/r0/raw-files`; `CG_VARW_RAW_INCLUDE_PREFIX` only filters listing. |
| R0 | file_id | `tools/cg-varw/backend/app/services/raw_root.py` | base64-url of POSIX path relative to `CG_VARW_RAW_ROOT`; root depth changes IDs. |
| R0 | review-units load | `load_or_build_review_units(file_id, raw_path)` | priority: draft JSON -> exported `raw_marker_review.csv` -> ASR candidates/manual empty. |
| R0 | draft save | `POST /api/r0/reviews/save` -> `marker_store.save_review_draft()` | writes `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json`. |
| R0 | CSV export | `POST /api/r0/reviews/export` -> `r0_export_writer.export_review_csv()` | writes 3 CSVs under `tools/cg-varw/review_outputs/r0/exports/{file_id}/`. |
| R1 | split listing | `GET /api/r1/batches`, `GET /api/r1/batches/{batch_id}/segments` | `CG_VARW_SPLIT_ROOT` may be parent `split_preview` or one batch root. |
| R1 | split manifest load | `r1_split_store.list_batches/list_segments` | prefers `r1_synthetic_split_manifest.json`; supplements with `recd2_split_preview_manifest.csv`; falls back to files. |
| R1 | draft load/save | `GET /api/r1/reviews/{batch_id}/draft`, `POST /api/r1/reviews/save` | batch draft JSON under `tools/cg-varw/review_outputs/r1/drafts/{batch_id}.split_review.json`. |
| R1 | CSV export | `POST /api/r1/reviews/export` -> `r1_review_store.export_r1_csv()` | writes 3 CSVs under `tools/cg-varw/review_outputs/r1/exports/{batch_id}/`. |
| R2 | latest load | `GET /api/r2/render-sets/{render_set_id}/review-draft/latest` | loads `r2_review_drafts/latest/r2_review_state.latest.json` as engineering-dir latest. |
| R2 | latest save | `POST /api/r2/render-sets/{render_set_id}/review-draft/save` | canonicalizes state, writes latest JSON, 8 derived files, manifest, archive copy. |
| R2 | derived export | `POST /api/r2/render-sets/{render_set_id}/review-draft/export-csv` | reads latest JSON, canonicalizes, rewrites latest JSON and 8 derived CSV/YAML. |
| R2 | restore from export | `POST /api/r2/render-sets/{render_set_id}/review-draft/restore-from-export-dir` | reconstructs latest JSON from CSV/YAML; should be explicit migration only, not normal authority. |
| R2 | legacy mock draft/export | `/api/r2/reviews/draft/save`, `/api/r2/reviews/{render_set_id}/export` | writes `tools/cg-varw/review_outputs/r2/...`; legacy/mock path for current Baiya work. |

## Current Export Files

| Stage | Current files observed | Counts / notes |
| --- | --- | --- |
| R0 active workbench | `tools/cg-varw/review_outputs/r0/drafts/*.json`; `tools/cg-varw/review_outputs/r0/exports/{file_id}/{reviewed_slate_anchor_manifest.csv,raw_marker_review.csv,split_plan_from_raw_markers.csv}` | 8 draft JSON + 24 export CSV. Drafts have `units` and `unit_change_log`; no stage export manifest. |
| R0 project-side archive/audit | `02_recordings/.../r0_review/batchXX/*` | 32 R0 artifacts plus `.DS_Store`; batch CSV row counts match active exports from previous P0-B evidence. Not current loader authority. |
| R1 active workbench | `tools/cg-varw/review_outputs/r1/drafts/{batch_id}.split_review.json`; `tools/cg-varw/review_outputs/r1/exports/{batch_id}/...` | Code paths exist; active export manifest absent. |
| R1 project-side archive/audit | `02_recordings/.../r1_review/batchXX/{reviewed_render_anchors,split_marker_review,segment_qc_sheet,manifest}` | batch01 has 10/40/10 rows; batch02-batch07 10/40/10; batch08 1/4/1. Historical audited outputs, not current save path. |
| R1 split metadata | `split_preview/batchXX/r1_synthetic_split_manifest.json`, `manifests/recd2_split_preview_manifest.csv`, `r1_intake_pointer.yaml` | batch01-batch07 each 10 segments; batch08 1 segment. Audio files were not read. |
| R2 canonical latest | `r2_review_drafts/latest/r2_review_state.latest.json` | Current canonical. Observed counts: review=49, phrase=10, preferred=10, suggested_revision=33, issue=53. |
| R2 latest manifest | `r2_review_drafts/latest/r2_review_state_manifest.json` | Records `canonical_source=r2_review_state.latest.json`, `current_page_load_source=engineering_dir_latest`, `no_downloads_policy=true`; lacks full output hashes/reload validation. |
| R2 derived latest files | 8 files: `issue_list.csv`, `listening_review.csv`, `listening_review.yaml`, `phrase_boundary_decision.csv`, `phrase_structure_review.yaml`, `preferred_version_summary.csv`, `render_phrase_alignment.csv`, `render_revision_log.yaml` | Derived from latest JSON. Observed rows: issue 53, listening 49, boundary/alignment 60, preferred 10, structure 10, revision 33. |
| R2 intake | `r2_review_intake/r2_render_set_index.json`, alignment seeds, phrase lock files, validation/report metadata | Intake authority for render-set metadata, not review-state authority. |
| F final metadata | `F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json`, `.sha256`, `f_final_validation.json`, alignment/report metadata | F input snapshot confirms F was generated from latest JSON snapshot, not Downloads/old CSV/YAML. F wav was not read. |

## Primary / Audit / Derived / Legacy Classification

### R0

| Class | Files / paths | Reason |
| --- | --- | --- |
| primary | `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json` for active UI state | First loader source and draft save target. |
| audit | `raw_marker_review.csv` | Human marker review trace; can reconstruct rows but should not outrank draft when draft exists. |
| derived | `reviewed_slate_anchor_manifest.csv`, `split_plan_from_raw_markers.csv` | Generated from review units for downstream planning/review; not sample ingest. |
| legacy/audit mirror | `02_recordings/.../r0_review/batchXX/*` | Project-side archive/candidate mirror; explicitly not a second runtime source of truth. |

R0 current manifest is not sufficient. `reviewed_slate_anchor_manifest.csv` is a domain CSV, not an export manifest. Project-side `r0_review_archive_manifest.*` is archive metadata, not active export metadata. Missing: stage manifest, source root/scope, file-id strategy, input state hash, output hashes, reload validation result, downstream-consumer declaration.

### R1

| Class | Files / paths | Reason |
| --- | --- | --- |
| primary | `tools/cg-varw/review_outputs/r1/drafts/{batch_id}.split_review.json` for active UI state | First-class save/load endpoint. |
| audit | `split_marker_review.csv`, `segment_qc_sheet.csv` | Human marker/QC trace and review status. |
| derived | `reviewed_render_anchors.csv` | Render-anchor table derived from reviewed split markers/QC. |
| intake metadata | `split_preview/batchXX/r1_synthetic_split_manifest.json`, `recd2_split_preview_manifest.csv` | Source listing/seed metadata, not human review result. |
| legacy/audit archive | `02_recordings/.../r1_review/batchXX/*` | Validated historical reviewed outputs; not current save path. |

R1 current manifest is not sufficient. Project-side `r1_review_archive_manifest*.yaml` exists for archive/audit, but active export path has no manifest, no source root/scope hash, no input-state hash, no output hashes, no reload validation.

`tail_policy` and `full_tail`: `SplitSegment.tail_policy` is part of R1 schema and exported in `reviewed_render_anchors.csv`. `full_tail` is not an R1 schema enum; it appears as the `tail_policy` value `full_tail` when present. R1 export keeps `tail_policy` as review metadata; it does not execute render or sample ingest.

### R2

| Class | Files / paths | Reason |
| --- | --- | --- |
| primary | `r2_review_drafts/latest/r2_review_state.latest.json` | Current canonical review state and F input authority. |
| audit | `r2_review_state_manifest.json`, `review_history_archived` inside latest JSON, archive copies | Provenance/history, not normal load authority. |
| derived | latest 8 CSV/YAML files | Rebuilt from canonical latest JSON for human inspection/downstream review. |
| intake metadata | `r2_review_intake/*` | Render-set/phrase/alignment seed metadata, not review-state authority. |
| legacy | `tools/cg-varw/review_outputs/r2/drafts`, `tools/cg-varw/review_outputs/r2/exports`, old mock `/reviews/...` endpoints | Old/mock R2 path; not canonical for Baiya F-final state. |
| forbidden authority | Downloads, restore zip, browser Blob, old exports/archive | May be historical evidence only; never implicit current source of truth. |

R2 manifest is partially sufficient: it records canonical source, latest path, files, counts, F flags, `no_downloads_policy`. It lacks `input_state_hash`, `output_hashes`, explicit `derived_outputs` classification, reload-validation status, and a guard that forbids normal promotion from CSV/YAML back to latest JSON.

## Risks Found

| Risk | Stage | Current evidence | Severity |
| --- | --- | --- | --- |
| Root/scope confusion | R0 | `file_id` is relative to `CG_VARW_RAW_ROOT`; include prefix only filters listing. A narrow root produces incompatible IDs. | High if env/config changes. |
| Broad fallback may select unrelated export | R0 | `exported_marker_review_path()` falls back to first `*/raw_marker_review.csv` if direct file-id path misses. | Medium; current Baiya 8 files direct-hit after P0-B. |
| No active export manifest | R0/R1 | Writers return file paths and contract warnings only. | Medium. |
| No reload validation | R0/R1/R2 | CSV writers validate rows before writing but do not re-open and compare exported state to input state. | Medium. |
| R1 parent/single root ambiguity | R1 | `CG_VARW_SPLIT_ROOT` supports both parent and batch root; fallback file-derived `segment_id` is weaker than manifest identity. | Medium. |
| Derived export can be mistaken for authority | R2 | Latest CSV/YAML sit beside canonical JSON; old restore endpoint can reconstruct JSON from exports. | High because F render depends on canonical review state. |
| Latest JSON vs CSV/YAML drift | R2 | Current export writes both, but manifest has no output hashes or reload-equality proof. Manual edits to CSV/YAML would not be detected by loader. | High for human handoff confusion. |
| Legacy/mock R2 endpoints remain callable | R2 | `/api/r2/reviews/{render_set_id}/export` writes mock/default `review_outputs/r2` exports. | Medium; not used by current page flow. |
| Restore/export authority leak | R2 | `restore_project_review_draft_from_export_dir()` reads CSV/YAML or zip and writes latest JSON. | High unless restricted to explicit migration. |

## Derived-As-Canonical Code Paths

- R0: `load_units_from_exported_csv()` can rebuild review units from `raw_marker_review.csv` after missing draft. This is a compatibility fallback and should be manifest-guarded.
- R2: `restore_project_review_draft_from_export_dir()` can rebuild latest JSON from `listening_review.csv`, `preferred_version_summary.csv`, `issue_list.csv`, boundary/alignment files, or zip contents. This must remain explicit promote/restore, not normal load.
- R2: legacy mock export path `export_reviews()` writes default mock exports under `review_outputs/r2`; these are legacy, not current Baiya authority.
- Frontend: current `R2ProjectReviewPage` loads `loadR2LatestReviewDraft()` and exports via project API. `R2ExportPreviewPanel` previews tables only; current source search found no active Blob/download path in `frontend/src`.

## Reload Validation Gaps

- R0 export: no read-back parse of the three CSVs, no comparison to draft/input `units`, no manifest row-count/hash proof.
- R1 export: no read-back parse of the three CSVs, no comparison to derived segment state, no manifest row-count/hash proof.
- R2 latest export: reads latest JSON and writes derived files, but does not prove each derived file parses back to the same counts/keys, and manifest lacks output hashes.
- R2 latest load: returns counts from JSON and manifest, but does not assert manifest/files match current JSON hash.

## Dry-Run Non-Patch Statement

本轮未修改任何 code、R0/R1/R2 数据、render output、sample ingest、score/canon/source/schema、archive 文件；未移动/删除/归档文件；未运行 render；未生成 G/F2；未写 `sample_assets.csv`、`recording_segments.csv`、`recording_items_enriched.jsonl`；未训练 ML；未进入 Arrangement Mode；未处理 `scripts/generate_baiya_recording_plan.py`。

## Next Recommendation

下一轮只选一个最小 patch，推荐：

`R2 latest JSON -> CSV/YAML derived export guard`

理由：优先防止再次影响 F render 的 canonical state。R0/R1 当前主要风险是 manifest/reload validation 不足；R2 风险直接关系 `F_FINAL_REVIEWED` 输入权威性，并且已有 canonical latest 方向，适合加小 guard：manifest/hash/reload proof + 明确 CSV/YAML derived-only + 禁止普通路径从 derived 反推 latest。
