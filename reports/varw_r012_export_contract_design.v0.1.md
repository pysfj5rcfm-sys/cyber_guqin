# VARW R0/R1/R2 Export Contract Design v0.1

- Task: `CG-XWC-MVP-P1A_VARW_R012_EXPORT_CONTRACT_AUDIT_DRY_RUN`
- Scope: design only. This document does not implement any patch.
- Principle: unify export contract, not business schema.

## Classification Rules

- `primary`: 下游真正读取的权威产物。当前工作状态只允许从 primary 或显式 promoted primary 读取。
- `audit`: 人类审校、追溯、证明用产物；可解释 primary，但不能自动覆盖 primary。
- `derived`: 由 primary 派生的便读导出。可给人读、可给报告引用，但不得隐式反推 primary。
- `legacy`: 历史兼容路径；只为迁移/排障保留，不作为当前权威。
- `archive`: 历史保留；默认只读，不参与当前运行。
- `forbidden authority`: Downloads、restore zip、browser Blob、old exports、quarantine/archive 旧副本；只能作为显式恢复输入或人工证据，不能作为普通 current state。

## Unified Export Contract

R0/R1/R2 的业务 schema 可以不同，但每次导出必须有同形 contract manifest：

```yaml
stage: R0 | R1 | R2
piece_id:
session_id:
qinist_id:
source_root:
include_prefix_or_scope:
file_id_strategy:
canonical_source:
primary_outputs:
audit_outputs:
derived_outputs:
legacy_outputs:
export_manifest_path:
created_at:
tool_version:
input_state_hash:
output_hashes:
row_counts:
reload_validation:
downstream_consumers:
provenance_notes:
compatibility_notes:
```

## Manifest Schema Draft

```yaml
manifest_version: varw_export_contract.v0.1
stage: R0
piece_id: XWC
session_id: RS_XWC_002_BAIYA_PILOT
qinist_id: QINIST_002
source_root: /absolute/path/or/repo-relative/root
include_prefix_or_scope: QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw
file_id_strategy:
  name: raw_root_relative_posix_base64url
  root_is_identity_boundary: true
  scope_changes_file_id: false
canonical_source:
  path: tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json
  role: primary
primary_outputs:
  - path: tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json
    role: primary
audit_outputs:
  - path: tools/cg-varw/review_outputs/r0/exports/{file_id}/raw_marker_review.csv
    role: audit
derived_outputs:
  - path: tools/cg-varw/review_outputs/r0/exports/{file_id}/reviewed_slate_anchor_manifest.csv
    role: derived
  - path: tools/cg-varw/review_outputs/r0/exports/{file_id}/split_plan_from_raw_markers.csv
    role: derived
legacy_outputs: []
export_manifest_path: tools/cg-varw/review_outputs/r0/exports/{file_id}/export_manifest.json
created_at: 2026-06-21T00:00:00Z
tool_version:
  app: cg-varw
  contract: varw_export_contract.v0.1
input_state_hash:
  algorithm: sha256
  path: primary-input-path
  value: hex
output_hashes:
  - path: output-path
    sha256: hex
row_counts:
  raw_marker_review.csv: 29
reload_validation:
  status: pass | fail | skipped
  validator: stage_specific_reload_v0.1
  checked_at: 2026-06-21T00:00:00Z
  notes: parsed outputs match canonical counts and identity keys
downstream_consumers:
  - review_ui
  - report
provenance_notes:
  - review_only=true
  - production_grade=false
compatibility_notes:
  - CSV exports are compatibility/readability outputs, not canonical unless explicitly promoted.
forbidden_authority:
  - Downloads
  - restore_zip
  - browser_Blob
  - old_exports
```

## Source-of-Truth Rules

### R0

- Canonical current state: `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json`.
- CSV compatibility fallback may exist, but must be called `compatibility_restore`, not primary load, unless a manifest explicitly marks it as promoted.
- Project-side `02_recordings/.../r0_review/` remains audit/archive mirror, not a second source of truth.

### R1

- Canonical current state: `tools/cg-varw/review_outputs/r1/drafts/{batch_id}.split_review.json`.
- Split preview manifests are intake metadata and seed identity; they do not replace human review draft.
- Project-side `02_recordings/.../r1_review/` remains audit/archive output, not active save path.

### R2

- Canonical current state: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`.
- The 8 CSV/YAML files in `latest/` are derived from latest JSON.
- `r2_review_state_manifest.json` is audit/provenance for latest JSON and derived files.
- CSV/YAML can only create/replace latest JSON through an explicit `promote` or `restore` operation that records source path, hashes, warnings, reviewer, and reason.
- F render input must be latest JSON or an input snapshot of latest JSON, never old CSV/YAML, Downloads, browser Blob, restore zip, or archive.

## Root / Scope Separation Rules

- `source_root` defines identity boundary.
- `include_prefix_or_scope` filters discovery/export scope but must not change identity.
- R0: `CG_VARW_RAW_ROOT` is `file_id` base. `CG_VARW_RAW_INCLUDE_PREFIX` only filters `/api/r0/raw-files`.
- R1: `CG_VARW_SPLIT_ROOT` may point to parent `split_preview` or a batch root; manifest must record which mode was used and the selected `batch_id` scope.
- R2: `CG_VARW_R2_RENDER_ROOT` defines render/intake root; `r2_review_drafts/latest` defines canonical review-state scope. `r2_review_intake` is intake metadata, not review-state root.

## File-ID Stability Rules

- R0 `file_id_strategy` must be recorded as `raw_root_relative_posix_base64url`.
- Changing `CG_VARW_RAW_ROOT` depth is a breaking identity change and must fail validation unless a migration manifest maps old IDs to new IDs.
- `include_prefix_or_scope` must never participate in `file_id` generation.
- R1 has no R0-style `file_id`; `segment_id`, `batch_id`, `recording_take_no`, `batch_take_no`, and `source_split_audio` must be recorded as identity fields. Fallback filename-derived IDs are compatibility only.
- R2 phrase/version state keys may use backend `phrase_id:version_id` and frontend `phrase_id::version_id`; manifest should record canonical key form and adapter normalization.

## Reload Validation Rules

Each export should validate in the smallest stage-specific way:

- R0: parse all three CSVs after write; verify row counts, required identity fields, `file_id`, `source_raw_audio`, unit IDs, marker types, and safety flags against draft/input units.
- R1: parse all three CSVs after write; verify segment IDs, `source_split_audio`, `tail_policy`, marker counts, QC booleans, `reviewed_at` behavior, and safety flags against derived segment state.
- R2: parse latest JSON and all 8 derived files after write; verify counts (`review_count`, `phrase_count`, `preferred_version_count`, `suggested_revision_count`, `issue_count`), output hashes, expected filenames, and `canonical_source=r2_review_state.latest.json`.
- Validation result must be written to manifest as `reload_validation.status`.
- A failed reload validation must not silently update downstream readiness/provenance reports.

## Stale Export Guard

- Every export manifest must include `input_state_hash` and per-output `output_hashes`.
- Loader must compare current primary hash against manifest `input_state_hash` before treating derived files as current.
- If derived file hash differs from manifest, mark it `stale_derived_export`.
- If manifest references a missing primary, mark export `orphaned_derived_export`.
- Reports must cite canonical source and hash, not only a CSV/YAML path.
- Archive and legacy paths should be discoverable only through audit commands, not normal app load.

## R2 Latest JSON Canonical Guard

Minimum intended guard:

1. `export_project_review_draft_csv()` must read `r2_review_state.latest.json` first.
2. It must write/update manifest fields:
   - `canonical_source: r2_review_state.latest.json`
   - `derived_outputs: [8 files]`
   - `input_state_hash`
   - `output_hashes`
   - `reload_validation.status`
   - `derived_export_only: true`
   - `forbidden_authority: [Downloads, restore_zip, browser_Blob, old_exports]`
3. `restore_project_review_draft_from_export_dir()` must identify itself as `explicit_restore_from_derived_exports`, never as normal load.
4. The frontend status should continue saying `engineering_dir_latest` only when source is latest JSON, not restored exports.
5. F render/report tasks must verify latest JSON hash or `F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.sha256`.

## Backward Compatibility

- Do not remove current CSV/YAML outputs.
- Do not remove R0 CSV fallback immediately; first add manifest/diagnostic guard.
- Do not add project-side R0/R1 archive directories as active loader roots.
- Keep R2 restore endpoint for explicit recovery, but require stronger provenance before using it.
- Legacy/mock R2 `review_outputs/r2` endpoints remain legacy and should be labeled as such in manifest/reporting if encountered.

## Report / Provenance Rules

Every future report that cites VARW exports should include:

- stage and manifest path;
- canonical source path;
- input state hash;
- output file list and row counts;
- reload validation result;
- explicit statement that derived CSV/YAML are not canonical unless promoted;
- forbidden-authority statement for Downloads, restore zip, browser Blob, and old exports.

## Phased Landing Plan

### P1-A audit/design

This round:

- audit R0/R1/R2 current entry points and artifacts;
- define primary/audit/derived/legacy classification;
- write this design;
- no code or data patch.

### P1-B minimal guard patch

Recommended one-patch scope:

`R2 latest JSON -> CSV/YAML derived export guard`

Implementation should be narrow:

- update R2 manifest writer to include `input_state_hash`, `output_hashes`, `derived_outputs`, `reload_validation`, and `derived_export_only`;
- add parse/count validation for the 8 latest derived files after export;
- label restore endpoint output provenance as explicit restore from derived exports;
- add focused tests around R2 export manifest/hash/reload validation.

Do not modify F/R1/R0 data, render outputs, sample ingest, file-id rules, or legacy archives.

### P1-C manifest/reload validation

After R2 guard lands:

- add R0 active export manifest and reload validation;
- add R1 active export manifest and reload validation;
- optionally extract a shared manifest utility only after R2/R0/R1 needs are proven by tests;
- keep schema differences stage-specific.

## Next Minimal Patch Proposal

Choose exactly one next patch:

`R2 latest JSON -> CSV/YAML derived export guard`

Priority rationale:

1. It most directly prevents F render from being affected by stale or mistaken canonical state.
2. It fits current code shape because R2 already has `r2_review_state_manifest.json`.
3. It avoids a larger R0/R1 loader refactor and does not change `file_id` behavior.
4. It creates a concrete manifest/reload pattern that R0/R1 can copy later without forcing a shared abstraction too early.
