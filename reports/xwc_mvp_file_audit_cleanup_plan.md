# XWC MVP 文件级审计与归档清理 Dry Run 计划

- 生成时间: 2026-06-21 15:50:08 
- 任务: CG-XWC-MVP-P0A_PROJECT_FILE_AUDIT_AND_ARCHIVE_CLEANUP_DRY_RUN
- 模式: dry run only; no move, no delete, no rename, no code edit, no render, no sample ingest, no commit
- 当前 HEAD: `8295651 clean r2_drafts and frontend_config`
- 任务单记录的 latest accepted commit: `4899227 fix(render): regenerate XWC F final with full tail previews`
- 当前状态差异: 当前工作树 HEAD 为 `8295651`，与任务单记录不同；本报告只记录差异，不据此改写任何产物。

## Current State Confirmation

| Item | Value |
| --- | --- |
| Project | Cyber Guqin v1.0 |
| Active Piece | XWC / 仙翁操 |
| Active Session | RS_XWC_002_BAIYA_PILOT |
| Active Phase | Phase 1F-XWC-MVP Passed / Sweep & Review |
| Final Accepted Version | F_FINAL_REVIEWED |
| MVP Status | PASSED_WITH_MINOR_KNOWN_ISSUE |
| Highest Priority | P0-A PROJECT_FILE_AUDIT_AND_ARCHIVE_CLEANUP |
| Blocked Follow-up | P0-B LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED waits for reviewed P0-A plan |
| Dry Run Required | true |

Authority 文件可见性说明: 任务单列出的以下 canonical authority 文件未在当前 repo 文件树中找到；本轮没有到 repo 外查找，也没有用 Downloads/restore/archive 作为 source of truth。
- `Core_Instructions_v1.5.1_MVP_PASSED_SWEEP_GUARD.md`: NOT FOUND in repository inventory
- `NEXT_CHAT_HANDOFF_XWC_MVP_PASSED_v0.1.md`: NOT FOUND in repository inventory

## Scan Policy

- 已执行 repository-wide file inventory，范围为当前 repo，排除 `.git/` 内部对象。
- 收集字段: path, filename/extension, size, modified time, git tracked/untracked/ignored status。
- 未执行 repository-wide content deep scan。
- 未读取 raw master audio、final F wav、图片、render wav、依赖缓存、archive/quarantine 文件正文。
- 受限目录仅按路径/metadata 归类；本轮未提出任何需要 deep-read 的具体文件。
- 未计算新 checksum；仅记录已存在 `.sha256` 文件的路径。

## Git Status Summary

Before dry-run report writes:
```text
?? scripts/generate_baiya_recording_plan.py
```
After dry-run report writes: 见本报告末尾验证区。

## Directory Inventory Summary

- Total files inventoried excluding `.git/`: 11446
- Git status counts: ignored=10427, tracked=1018, untracked=1

### Top-level directories

| Path | Files | Total size |
| --- | ---: | ---: |
| 00_global | 14 | 0.02 MB |
| 01_pieces | 12 | 0.10 MB |
| 02_recordings | 348 | 527.04 MB |
| 03_samples | 86 | 8.93 MB |
| 04_outputs | 318 | 285.83 MB |
| 05_scripts | 7 | 0.04 MB |
| 06_docs | 12 | 0.02 MB |
| README.md | 1 | 0.00 MB |
| canon | 9 | 0.06 MB |
| references | 3 | 0.01 MB |
| reports | 61 | 0.83 MB |
| schemas | 6 | 0.01 MB |
| scripts | 17 | 0.25 MB |
| sources | 29 | 3.43 MB |
| templates | 4 | 0.01 MB |
| tests | 3 | 0.02 MB |
| tools | 2710 | 91.51 MB |
| .DS_Store | 1 | 0.02 MB |
| .agents | 2 | 0.01 MB |
| .gitignore | 1 | 0.00 MB |
| .tools | 1 | 47.08 MB |
| .venv | 2663 | 39.48 MB |
| .venv-asr | 5137 | 203.52 MB |
| .vscode | 1 | 0.00 MB |

### Key scoped directories

| Path | Files | Total size | Git status counts |
| --- | ---: | ---: | --- |
| 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT | 308 | 262.03 MB | ignored=5, tracked=303 |
| 02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT | 324 | 518.06 MB | ignored=8, tracked=316 |
| tools/cg-varw/docs | 27 | 0.18 MB | tracked=27 |
| tools/cg-varw/review_outputs | 66 | 1.00 MB | ignored=64, tracked=2 |
| reports | 61 | 0.83 MB | ignored=1, tracked=60 |
| tools/cg-varw/frontend/node_modules | 2462 | 83.22 MB | ignored=2462 |
| .venv | 2663 | 39.48 MB | ignored=2663 |
| .venv-asr | 5137 | 203.52 MB | ignored=5137 |

### Extension summary, top 20

| Extension | Files |
| --- | ---: |
| .py | 5239 |
| .js | 1449 |
| .pyc | 1187 |
| [none] | 574 |
| .map | 417 |
| .csv | 323 |
| .json | 262 |
| .pyi | 256 |
| .ts | 254 |
| .wav | 253 |
| .md | 224 |
| .yaml | 126 |
| .txt | 103 |
| .pxd | 89 |
| .so | 80 |
| .typed | 71 |
| .pyx | 61 |
| .c | 53 |
| .f90 | 53 |
| .dylib | 29 |

## KEEP

KEEP 只表示本 dry-run 不建议归档/移动；不代表所有文件都已被正文审阅。
| Reason | Files | Total size | Examples |
| --- | ---: | ---: | --- |
| R0 recovery candidate; P0-B has not been verified | 64 | 0.62 MB | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/batch01/r0_export_archive_manifest.csv`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/batch01/raw_marker_review.batch01.csv`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r0_review/batch01/reviewed_slate_anchor_manifest.batch01.csv` |
| canonical F-final / accepted full-tail output or required F-final audit companion | 19 | 42.67 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/XWC_BAIYA_F_FINAL_REVIEWED.wav`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_final_render_report.md`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_final_validation.json` |
| canonical latest R2 draft/state path | 10 | 0.37 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/issue_list.csv`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/listening_review.csv`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/listening_review.yaml` |
| reports index | 1 | 0.00 MB | `reports/REPORTS_INDEX.md` |

### Must-keep existence check

| Path | Status | Size | Git status |
| --- | --- | ---: | --- |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/XWC_BAIYA_F_FINAL_REVIEWED.wav` | FOUND | 21.38 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/render_event_alignment.F_FINAL_REVIEWED.csv` | FOUND | 0.04 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_revision_plan.yaml` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_final_render_report.md` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_final_validation.json` | FOUND | 0.01 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json` | FOUND | 0.20 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.sha256` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/XWC_BAIYA_F_FINAL_REVIEWED.wav` | FOUND | 20.76 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/archive_metadata.json` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/f_final_render_report.md` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/f_final_validation.json` | FOUND | 0.01 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/f_revision_plan.yaml` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/input_snapshot/r2_review_state.latest.input_for_f.json` | FOUND | 0.18 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/input_snapshot/r2_review_state.latest.input_for_f.sha256` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX/render_event_alignment.F_FINAL_REVIEWED.csv` | FOUND | 0.03 MB | tracked |
| `tools/cg-varw/docs/CG_VARW_R2_F_FINAL_REVIEWED_GENERATION_AND_EXPORT_SYNC_REPORT_v0.1.md` | FOUND | 0.01 MB | tracked |
| `tools/cg-varw/docs/CG_VARW_R1_FULL_TAIL_REFRESH_AND_F_REGEN_REPORT_v0.1.md` | FOUND | 0.00 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/full_tail_preview_refresh_manifest.csv` | FOUND | 0.05 MB | tracked |
| `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/full_tail_refresh_audit.json` | FOUND | 0.01 MB | tracked |

## ARCHIVE Recommendations

这些是 dry-run 的归档建议，不执行移动。每条 ARCHIVE 的逐文件目标路径见 `reports/xwc_mvp_archive_index.DRY_RUN.md`。
| Reason | Risk | Files | Total size | Examples |
| --- | --- | ---: | ---: | --- |
| historical/generated validation or staging report already under archive | low | 13 | 0.04 MB | `reports/archive/generated_validation/check_v1_compat_report.json`<br>`reports/archive/generated_validation/validate_canon_report.json`<br>`reports/archive/generated_validation/validate_canon_seed_report.json` |
| old R2 draft archive path; not current latest state | low | 1 | 0.01 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/archive/.DS_Store` |
| stale R2 source already quarantined; keep out of canonical latest path | low | 232 | 6.62 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/_quarantine/final_canonical_cleanup_20260620_122000/cleanup_manifest.json`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/_quarantine/final_canonical_cleanup_20260620_122000/stale_archive_20260620_120110/issue_list.csv`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/_quarantine/final_canonical_cleanup_20260620_122000/stale_archive_20260620_120110/listening_review.csv` |
| old E_REVIEWED pre-T008-fix variant superseded by E_REVIEWED and F_FINAL_REVIEWED | medium | 5 | 31.22 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED_ORIGINAL_BEFORE_T008_FIX/XWC_BAIYA_E_REVIEWED.wav`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED_ORIGINAL_BEFORE_T008_FIX/e_reviewed_render_report.md`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED_ORIGINAL_BEFORE_T008_FIX/e_reviewed_validation.json` |

## REVIEW

REVIEW 表示仅凭路径/metadata 无法安全判定可归档，需要用户确认或第二阶段窄读。
| Reason | Files | Total size | Examples |
| --- | ---: | ---: | --- |
| ABCD render-readiness artifact; may be provenance but not canonical F output | 5 | 0.15 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/abcd_render_input_manifest.csv`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/abcd_render_input_manifest.json`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_render_readiness/abcd_render_readiness_report.md` |
| ASR/slate candidate artifact; may be historical input/provenance | 26 | 0.18 MB | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_asr_match_report.json`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_asr_transcript_segments.jsonl`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/asr_candidates/batch01_slate_anchor_candidates.csv` |
| Baiya stage report; user confirmation needed before archive | 12 | 0.10 MB | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_HUMAN_LISTENING_GATE_BAIYA_BATCH01_PASS_RECORD_v0.1.md`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_HUMAN_LISTENING_GATE_BAIYA_FULL_T001_TO_T071_PASS_RECORD_v0.1.md`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/reports/CG_RECD0_BAIYA_BATCH01_RAW_ARCHIVE_REPORT_v0.1.md` |
| R1 reviewed output; not R0 recovery, but may support provenance | 66 | 0.88 MB | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/r1_review_archive_manifest.yaml`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/reviewed_render_anchors.batch01.csv`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/r1_review/batch01/segment_qc_sheet.batch01.csv` |
| XWC/Baiya render context; role not safely archiveable from path alone | 5 | 0.07 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/abcd_render_manifest.csv`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/abcd_render_report.md`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/abcd_render_validation.json` |
| active XWC/Baiya render or R2 intake context; may be provenance for final F | 29 | 180.88 MB | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/A_LITERAL/XWC_BAIYA_A_LITERAL.wav`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/A_LITERAL/render_event_alignment.A_LITERAL.csv`<br>`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/B_PHRASE/XWC_BAIYA_B_PHRASE.wav` |
| cg-varw historical/current doc; path alone cannot prove inactive | 25 | 0.17 MB | `tools/cg-varw/docs/CG_VARW_M0_UI_SHELL_NOTES.md`<br>`tools/cg-varw/docs/CG_VARW_M0_VALIDATION.md`<br>`tools/cg-varw/docs/CG_VARW_R0_R1_R2_FINAL_UI_REGRESSION_POLISH_REPORT_v0.1.md` |
| root report or validation output; confirm active vs historical before archive | 46 | 0.78 MB | `reports/XWC_RECORDING_DAY_GUIDE.md`<br>`reports/architecture_inventory.json`<br>`reports/architecture_review.md` |
| split preview / R1 context; may affect provenance or future verification | 184 | 327.84 MB | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/clean_previews/T001_clean_preview.wav`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/clean_previews/T002_clean_preview.wav`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/split_preview/batch01/clean_previews/T003_clean_preview.wav` |
| untracked script present before dry-run; ownership/scope needs user confirmation | 1 | 0.03 MB | `scripts/generate_baiya_recording_plan.py` |

## DELETE_CANDIDATE

DELETE_CANDIDATE 仅表示可重生成/本地缓存类候选；本任务不删除。
| Reason | Files | Total size | Examples |
| --- | ---: | ---: | --- |
| frontend dependency install cache; reproducible from package-lock.json | 2462 | 83.22 MB | `tools/cg-varw/frontend/node_modules/.bin/baseline-browser-mapping`<br>`tools/cg-varw/frontend/node_modules/.bin/browserslist`<br>`tools/cg-varw/frontend/node_modules/.bin/esbuild` |
| local Python environment/cache; reproducible and ignored | 7860 | 243.81 MB | `.venv-asr/bin/Activate.ps1`<br>`.venv-asr/bin/activate`<br>`.venv-asr/bin/activate.csh` |
| macOS metadata file; reproducible/non-project artifact | 30 | 0.27 MB | `.DS_Store`<br>`.venv-asr/.DS_Store`<br>`.venv-asr/lib/.DS_Store` |

## DO_NOT_TOUCH

| Reason | Files | Total size | Examples |
| --- | ---: | ---: | --- |
| raw master audio binary; contents not inspected | 8 | 189.20 MB | `02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav`<br>`02_recordings/raw_audio/QINIST_002/XWC/RS_XWC_002_BAIYA_PILOT/raw/RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav` |
| score/canon/source/schema/sample-ingest boundary; outside cleanup execution scope | 156 | 12.55 MB | `00_global/alias_rules.yaml`<br>`00_global/gesture_component_lexicon.csv`<br>`00_global/gesture_components.csv` |

## Files Not Deeply Inspected

| Group | Files | Total size | Reason |
| --- | ---: | ---: | --- |
| raw master audio | 157 | 525.75 MB | binary raw audio; metadata only |
| final F wav | 1 | 21.38 MB | canonical final wav binary; metadata/existence only |
| render/intermediate wav | 12 | 277.61 MB | audio binary; metadata only |
| split preview wav | 142 | 327.64 MB | audio binary; metadata only |
| image source files | 24 | 3.42 MB | image/source boundary; metadata only |
| archive/quarantine contents | 246 | 6.67 MB | restricted path; listed by path only |
| dependency/env cache files | 10262 | 326.22 MB | ignored local dependency/cache tree; metadata only |

## Specific Files / Groups Needing User Confirmation

- `scripts/generate_baiya_recording_plan.py`: untracked before this dry-run; confirm whether it is user work, planned script, or should be archived separately.
- `04_outputs/.../A_LITERAL`, `B_PHRASE`, `C_QINIST_STYLE`, `D_TEACHING_DIAGNOSTIC`, `E_REVIEWED`: large render variants; likely provenance, but not canonical F-final. Confirm KEEP vs ARCHIVE.
- `04_outputs/.../r2_review_intake/` and `_planning/`: R2/F provenance candidates. Confirm whether needed for future traceability.
- `02_recordings/.../split_preview/` and `r1_review/`: R1 provenance and preview assets. Confirm before archive/delete decisions.
- `tools/cg-varw/docs/CG_VARW_R2*.md`: many R2 historical reports; only two docs were explicit must_keep. Confirm which older reports should remain active.
- `reports/*.json` validation outputs in root: likely reproducible, but some may be current index evidence. Confirm active vs historical.

## Risk Notes

- R0 recovery is not verified; all visible R0 draft/export/review files were classified KEEP, not ARCHIVE.
- Final F canonical files exist and were classified KEEP/DO_NOT_TOUCH; final wav contents were not read.
- Current HEAD differs from task sheet accepted commit; cleanup execution should verify intended base before moving anything.
- Already-archived or quarantined files are still represented in ARCHIVE recommendations because they are non-canonical historical material; second-stage execution may decide to leave them in place if consolidation is unnecessary.
- Ignored `.venv*` and `node_modules` dominate file count and size; deleting them is outside this dry-run and may affect local convenience, though they are reproducible.

## Proposed Second-stage Archive Execution Plan

1. Require explicit user approval and freeze the exact reviewed archive index.
2. Re-run the same inventory commands and compare counts against this dry-run.
3. For each REVIEW group, either move it to KEEP/ARCHIVE/DO_NOT_TOUCH or record a user decision.
4. Archive only with `mkdir -p` + `git mv`/`mv` after approval; preserve relative paths under the proposed archive root.
5. Do not delete in the execution step; archive first, validate, then consider deletion in a separate task if ever needed.
6. Re-run final F existence checks and ensure no source code/sample ingest/final F files changed unexpectedly.

## Future Execute-step Validation Commands

- `git status --short`
- `find reports -maxdepth 3 -type f | sort`
- `find tools/cg-varw/docs -maxdepth 3 -type f | sort`
- `find 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT -maxdepth 5 -type f | sort`
- `test -f 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/XWC_BAIYA_F_FINAL_REVIEWED.wav`
- `test -f 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/render_event_alignment.F_FINAL_REVIEWED.csv`
- `test -f 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/f_final_validation.json`

## Dry-run Classification Counts

| Bucket | Files | Total size |
| --- | ---: | ---: |
| KEEP | 94 | 43.66 MB |
| ARCHIVE | 251 | 37.88 MB |
| REVIEW | 399 | 511.08 MB |
| DELETE_CANDIDATE | 10352 | 327.30 MB |
| DO_NOT_TOUCH | 164 | 201.75 MB |

## Final Git Status After Dry-run

```text
?? reports/xwc_f_final_token_cost_retrospective.DRY_RUN.md
?? reports/xwc_mvp_archive_index.DRY_RUN.md
?? reports/xwc_mvp_file_audit_cleanup_plan.md
?? scripts/generate_baiya_recording_plan.py
```

Acceptance note: `scripts/generate_baiya_recording_plan.py` was already untracked before this dry-run and was not modified or classified as an execution target. Because it remains in `git status`, the strict acceptance criterion "only the three expected report files changed/created" is not fully satisfied until the user separately decides how to handle that pre-existing untracked script.
