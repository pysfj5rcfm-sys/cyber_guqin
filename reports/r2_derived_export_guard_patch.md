# R2 Derived Export Guard Patch

任务：`CG-XWC-MVP-P1B_R2_DERIVED_EXPORT_GUARD_PATCH`

日期：2026-06-21

## 范围结论

本轮只处理 R2 project review 的 latest JSON -> CSV/YAML derived export guard。

未进入 R0/R1 manifest，未做 R012 总重构，未跑 render，未生成 G/F2，未写 sample ingest 文件，未修改真实 Baiya R0/R1/R2 review 数据。

## 修改文件列表

- `tools/cg-varw/backend/app/services/r2_mock_store.py`
- `tools/cg-varw/backend/app/tests/test_r2_review_draft_persistence.py`
- `reports/r2_derived_export_guard_patch.md`

## R2 入口定位

- latest JSON load 入口：`tools/cg-varw/backend/app/services/r2_mock_store.py:261` `load_project_review_draft_latest()`
- latest JSON save 入口：`tools/cg-varw/backend/app/services/r2_mock_store.py:295` `save_project_review_draft()`
- derived export 入口：`tools/cg-varw/backend/app/services/r2_mock_store.py:344` `export_project_review_draft_csv()`
- restore-from-export-dir 入口：`tools/cg-varw/backend/app/services/r2_mock_store.py:390` `restore_project_review_draft_from_export_dir()`
- 8 个 CSV/YAML 写入入口：`tools/cg-varw/backend/app/services/r2_mock_store.py:1882` `write_export_tables()`
- manifest 写入入口：`tools/cg-varw/backend/app/services/r2_mock_store.py:1923` `write_review_state_manifest()`
- API wrapper：
  - `GET /api/r2/render-sets/{render_set_id}/review-draft/latest`
  - `POST /api/r2/render-sets/{render_set_id}/review-draft/save`
  - `POST /api/r2/render-sets/{render_set_id}/review-draft/export-csv`
  - `POST /api/r2/render-sets/{render_set_id}/review-draft/restore-from-export-dir`
- F input snapshot guard：新增只读 metadata helper `tools/cg-varw/backend/app/services/r2_mock_store.py:2019` `r2_f_input_snapshot_guard()`。允许参考报告确认 F 输入应为 latest JSON 或 latest JSON input snapshot，不以 derived CSV/YAML 为 canonical。

## Canonical / Derived 分类

Canonical:

- `r2_review_drafts/latest/r2_review_state.latest.json`

Audit / provenance:

- `r2_review_drafts/latest/r2_review_state_manifest.json`
- latest JSON 内部 `review_history_archived`

Derived-only:

- `issue_list.csv`
- `listening_review.csv`
- `listening_review.yaml`
- `phrase_boundary_decision.csv`
- `phrase_structure_review.yaml`
- `preferred_version_summary.csv`
- `render_phrase_alignment.csv`
- `render_revision_log.yaml`

这些 CSV/YAML 只作为 derived output；普通 latest load 不会从这些文件自动 restore 或 promote。

## Manifest 新字段

`r2_review_state_manifest.json` 现在新增/固化以下语义：

- `manifest_version: varw_export_contract.v0.1`
- `stage: R2`
- `canonical_source: r2_review_state.latest.json`
- `canonical_source_role: primary`
- `derived_export_only: true`
- `derived_outputs: [8 derived files]`
- `input_state_hash: { algorithm, path, value }`
- `output_hashes: [{ path, sha256 }]`
- `row_counts`
- `reload_validation`
- `forbidden_authority: [Downloads, restore_zip, browser_Blob, old_exports]`
- restore 场景额外记录 `restore_provenance` 与 `restore_source`

## Reload Validation 方法

新增 `validate_r2_derived_export_reload()`：

1. 重新读取 `r2_review_state.latest.json`。
2. 重新 parse 8 个 derived CSV/YAML。
3. 校验 8 个文件都存在。
4. 校验 canonical review keys 与 `listening_review.csv` / `listening_review.yaml` keys 一致。
5. 校验 preferred phrase keys 与 `preferred_version_summary.csv` 一致。
6. 校验 counts：`review_count`、`phrase_count`、`preferred_version_count`、`suggested_revision_count`、`issue_count`。
7. 校验 `output_hashes` 覆盖 8 个 derived outputs，且 sha256 与当前文件一致。
8. 将结果写入 manifest 的 `reload_validation.status`，失败时写 `fail` 和 notes，不静默标记成功。

## Restore Provenance

`restore_project_review_draft_from_export_dir()` 仍是显式 restore/promote 路径，不是普通 load。恢复出的 state/manifest 现在记录：

- `restore_provenance: explicit_restore_from_derived_exports`
- `restore_source.path`
- `restore_source.hashes`
- `restore_source.warnings`
- `restore_source.reason: manual restore-from-export-dir request`

普通 latest load 仍只读取 latest JSON，不从 CSV/YAML 自动恢复。

## F Render 影响

本轮未修改 F render 输出，未读取 F wav 内容，未跑 render。

F guard 只确认 metadata 方向：F input authority 应为 `r2_review_state.latest.json` 或 `F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json` 与 `.sha256`，不把 derived CSV/YAML 作为 canonical。

## Tests 结果

Targeted backend tests:

```bash
cd tools/cg-varw/backend
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest app.tests.test_r2_review_draft_persistence
```

结果：`Ran 12 tests in 0.065s`，`OK`

Full backend tests:

```bash
cd tools/cg-varw/backend
/Users/chenyulin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover app/tests
```

结果：`Ran 31 tests in 0.091s`，`OK`

Diff whitespace check:

```bash
git diff --check
```

结果：通过，无输出。

Git status:

```bash
git status --short --untracked-files=all
```

结果：

```text
 M tools/cg-varw/backend/app/services/r2_mock_store.py
 M tools/cg-varw/backend/app/tests/test_r2_review_draft_persistence.py
?? scripts/generate_baiya_recording_plan.py
```

`scripts/generate_baiya_recording_plan.py` 是本轮禁止处理路径，未修改。

## 真实数据与边界

- 是否修改真实 Baiya latest 数据：否。
- 是否修改 R0/R1：否。
- 是否修改 F_FINAL_REVIEWED 输出：否。
- 是否写 sample ingest：否。
- 是否处理 Downloads / restore zip / browser Blob / old exports 作为 current state：否。
- 是否自动 commit：否。

## 风险与回滚

风险：

- Reload validation 目前只校验 R2 guard 所需 counts/keys/hash；不扩展为 R012 通用 contract validator。
- Existing restore 仍可由显式 endpoint 执行，但 manifest/provenance 已标识为 `explicit_restore_from_derived_exports`，不会伪装成 normal load。

回滚：

- 回滚 `tools/cg-varw/backend/app/services/r2_mock_store.py` 中新增 manifest/validator/provenance helper。
- 回滚 `tools/cg-varw/backend/app/tests/test_r2_review_draft_persistence.py` 中新增 guard tests。
- 删除本报告。

## 提交建议

建议提交。建议 commit message：

```text
fix(varw): guard R2 derived exports with canonical latest metadata
```

## 下一步

可以进入下一项：固化 `full_tail` / `natural_decay` 默认策略。该任务应继续保持独立，不并入 R2 derived export guard。
