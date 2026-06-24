# docs/cyber_guqin Index

`docs/cyber_guqin/` contains the current P1-F dry-run reproduction documentation.

## Current Entrypoints

| File | Status | Purpose |
| --- | --- | --- |
| `XWC_F_REPRODUCTION_RUNBOOK.md` | `current` | User-facing dry-run path for understanding how XWC `F_FINAL_REVIEWED` was engineered without rerunning accepted F. |
| `SCRIPT_REGISTRY.md` | `current` | Script safety registry: generic dry-run helpers, read-only verifiers, high-risk execute paths, and historical XWC/Baiya scripts. |
| `INDEX.md` | `index-only` | This directory index. |

## Boundary

These documents are current P1-F dry-run reproduction entrypoints.

They are not:

- a real audio renderer entrypoint;
- sample ingest instructions;
- ML training instructions;
- second-piece execution instructions;
- Arrangement Mode production instructions;
- permission to rerun or overwrite accepted `F_FINAL_REVIEWED`.

## Authority Rules

- Accepted baseline / forbidden-to-touch: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- R2 canonical authority: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML files are derived exports.
- `examples/cyber_guqin/` files are examples/fixtures, not accepted baseline authority.

## Related Entrypoints

- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- `examples/cyber_guqin/README.md`
- `scripts/README.md`
- `tools/cg-varw/backend/scripts/README.md`
- `reports/REPORTS_INDEX.md`
