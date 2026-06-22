# XWC F Reproduction Runbook

本文面向用户脱离 Codex 独立操作。目标是 dry-run 复现《仙翁操》`F_FINAL_REVIEWED` 的工程生成路径：确认权威输入、理解录音计划、理解 ABCD 渲染计划、理解 final reviewed render 计划，并且不覆盖 accepted F baseline。

## 0. 目标与边界

本 runbook 复现的是工程路径，不重跑 accepted F。

- 默认全部使用 `--dry-run`。
- 不覆盖 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`。
- 不生成 G/F2。
- 不进入 sample ingest、ML training 或 Arrangement Mode。
- 不读取真实 audio binary；本轮 dry-run 只读 JSON/CSV/YAML/Markdown/text metadata。
- `scripts/generate_baiya_recording_plan.py` 是 historical template，不直接运行。

## 1. 前置条件

- repo 位于本工程根目录。
- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md` 已存在。
- XWC accepted F baseline 已存在，但本 runbook 不读取 F wav binary。
- R2 latest JSON authority:
  `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- F input snapshot metadata:
  `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json`
- 使用 Python 3.9+ 即可；示例 manifest 是 JSON-compatible YAML，不需要 `PyYAML`。

## 2. Authority Rule

Canonical authority:

- `r2_review_drafts/latest/r2_review_state.latest.json`
- 或 `F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json` 与对应 hash/provenance

Derived / audit only:

- `listening_review.csv`
- `listening_review.yaml`
- `issue_list.csv`
- `preferred_version_summary.csv`
- `phrase_structure_review.yaml`
- `render_phrase_alignment.csv`
- `phrase_boundary_decision.csv`
- `render_revision_log.yaml`

Forbidden as current authority:

- Downloads
- browser Blob downloads
- restore zip
- old exports
- archived old exports
- raw/split/F audio binary contents

## 3. Step-by-Step Dry Run

### Step 0: Git Status

```bash
git status --short --untracked-files=all
```

Expected known caveat: `scripts/generate_baiya_recording_plan.py` may appear as untracked historical template. Do not run, stage, delete, move, or archive it in this workflow.

### Step 1: Read Workflow Skill

```bash
sed -n '1,260p' .agents/skills/cyber_guqin_mvp_workflow/SKILL.md
```

Confirm the phase gates: R2 latest JSON canonical, CSV/YAML derived, F pass does not imply sample ingest or ML.

### Step 2: Confirm Authority Metadata

```bash
python3 tools/cg-varw/backend/scripts/verify_r2_render_manifest.py \
  --review-state 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json \
  --render-manifest examples/cyber_guqin/xwc_r2_render_verify_manifest.yaml \
  --dry-run
```

This verifier is read-only. It fails if the manifest tries to use derived CSV/YAML, Downloads, Blob, restore zip, or an accepted baseline output root as authority.

### Step 3: Recording Plan Dry Run

```bash
python3 scripts/generate_recording_plan_from_dapu_ir.py \
  --piece-id XWC \
  --session-id RS_XWC_002_BAIYA_PILOT \
  --recording-id RS_XWC_002 \
  --qinist-id QINIST_002 \
  --qinist-name Baiya \
  --dapu-ir examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl \
  --recording-config examples/cyber_guqin/xwc_recording_plan_config.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY/recording_plan \
  --dry-run
```

Expected: stdout contains `DRY_RUN`, expected output paths, warnings, and no files are written.

### Step 4: ABCD Render Dry Run

```bash
python3 scripts/render_abcd_from_manifest.py \
  --render-manifest examples/cyber_guqin/xwc_abcd_render_manifest.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY/abcd \
  --dry-run
```

Expected: planned A/B/C/D paths and alignment row counts. No WAV is read or written.

### Step 5: Final Reviewed Render Dry Run

```bash
python3 tools/cg-varw/backend/scripts/generate_final_reviewed_render.py \
  --final-render-manifest examples/cyber_guqin/xwc_final_render_manifest.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY/final \
  --dry-run
```

Expected: authority summary, source review hash, phrase/event counts, planned target files, sample safety checks, and no writes.

### Step 6: Script Help Check

```bash
python3 scripts/generate_recording_plan_from_dapu_ir.py --help
python3 scripts/render_abcd_from_manifest.py --help
python3 tools/cg-varw/backend/scripts/generate_final_reviewed_render.py --help
python3 tools/cg-varw/backend/scripts/verify_r2_render_manifest.py --help
```

Each help page should show dry-run-first behavior and the manifest/config entry point.

## 4. Optional Sandbox Execute

Only run these after explicit user authorization. They must write under `reproduction_runs/<RUN_ID>/` and must never write into accepted `F_FINAL_REVIEWED`.

```bash
RUN_ID=manual_reproduction_$(date +%Y%m%d_%H%M%S)
```

```bash
python3 scripts/generate_recording_plan_from_dapu_ir.py \
  --piece-id XWC \
  --session-id RS_XWC_002_BAIYA_PILOT \
  --recording-id RS_XWC_002 \
  --qinist-id QINIST_002 \
  --qinist-name Baiya \
  --dapu-ir examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl \
  --recording-config examples/cyber_guqin/xwc_recording_plan_config.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/$RUN_ID/recording_plan \
  --execute
```

```bash
python3 scripts/render_abcd_from_manifest.py \
  --render-manifest examples/cyber_guqin/xwc_abcd_render_manifest.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/$RUN_ID/abcd \
  --execute
```

```bash
python3 tools/cg-varw/backend/scripts/generate_final_reviewed_render.py \
  --final-render-manifest examples/cyber_guqin/xwc_final_render_manifest.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/$RUN_ID/final \
  --execute
```

Current generic render execute materializes sandbox metadata, alignment planning, validation, reports, and input snapshots. It does not run a real audio renderer.

## 5. Output Verification Checklist

- Verifier reports `PASS`.
- Dry-run commands report planned paths only.
- No command writes under accepted `F_FINAL_REVIEWED`.
- No command creates G/F2.
- No command creates `sample_assets.csv`, `recording_segments.csv`, or `recording_items_enriched.jsonl`.
- No command reads or writes real audio binary.
- Any sandbox execute output lives under `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/<RUN_ID>/`.
- Human listening gate remains required before any future accepted render claim.

## 6. Stop Rules

Stop immediately if:

- A command prepares to write into `F_FINAL_REVIEWED`.
- A command prepares to generate G or F2.
- A command tries to read real audio binary.
- A command tries to write sample ingest files.
- A command treats CSV/YAML derived outputs as source authority.
- A command references Downloads, browser Blob, restore zip, or old exports as current authority.
- The authority path is unclear.

## 7. No Cleanup Rule

Do not clean, delete, archive, move, or stage historical files during this reproduction pass. In particular, do not process `scripts/generate_baiya_recording_plan.py`. Cleanup requires a separate task and explicit approval.
