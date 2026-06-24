# 赛博古琴 Cyber Guqin v1.0

当前阶段：`XWC F reproduction ready / Sanman digitization startup`

当前工程基线：`XWC / 《仙翁操》 / QINIST_002 白牙 / RS_XWC_002_BAIYA_PILOT / F_FINAL_REVIEWED`

当前主线：`QINIST_001 = 三曼数字琴人采集协议、controlled fingering samples、ML-ready candidate sidecar`

当前不是：第二首执行、sample ingest、ML training、Arrangement Mode production、accepted F 重跑。

## 当前入口

P1-F self-contained reproduction toolchain 已存在，当前用于 dry-run 复现 XWC F 的工程生成路径。它不是真实 audio renderer，不是 sample ingest，不是 ML 入口，也不是第二首生产入口。

- Workflow skill：`.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- P1-F runbook：`docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- Script registry：`docs/cyber_guqin/SCRIPT_REGISTRY.md`
- Example manifests / fixtures：`examples/cyber_guqin/`
- Runtime / legacy structure：`06_docs/PROJECT_STRUCTURE.md`
- Legacy docs index：`06_docs/INDEX.md`
- Reports index：`reports/REPORTS_INDEX.md`

## Current Authority

- Accepted baseline / forbidden-to-touch：`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- R2 canonical authority：`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML files beside it are derived exports, not canonical authority.
- `reports/` contains audit/status evidence, not runtime output and not canonical authority.

## Latest Repo Hygiene Evidence

Use only the latest R0 reports for current repository hygiene decisions:

- `reports/repo_hygiene_audit.latest.v0.1.md`
- `reports/repo_hygiene_inventory.latest.v0.1.json`
- `reports/repo_cleanup_candidates.latest.v0.1.csv`
- `reports/repo_entrypoint_map.latest.v0.1.md`

Older non-latest R0 reports are historical reference only.

## Current Stop Rules

- Do not move, delete, archive, or clean files as part of index/policy tasks.
- Do not run renderer, ingest, ML, frontend build, backend scripts, second-piece, G, or F2 workflows.
- Do not write `sample_assets.csv`, `recording_segments.csv`, or `recording_items_enriched.jsonl`.
- Do not touch accepted `F_FINAL_REVIEWED`.
- `scripts/generate_baiya_recording_plan.py` is absent in current HEAD; if restored or untracked later, treat it as a protected historical template and forbidden-to-touch.
