# tools/cg-varw/backend/scripts

This directory sits close to R2/F/final-reviewed render behavior and is higher risk than root `scripts/`. Do not treat files here as routine entrypoints without checking `docs/cyber_guqin/SCRIPT_REGISTRY.md`.

## Current / Read-Only

| Script | Status | Rule |
| --- | --- | --- |
| `verify_r2_render_manifest.py` | read-only verifier | Verifies R2/final manifest authority and rejects derived CSV/YAML, Downloads, Blob, restore zip, and accepted-baseline output roots as authority. |

## Generic Final Reviewed Planner

| Script | Status | Rule |
| --- | --- | --- |
| `generate_final_reviewed_render.py` | generic final reviewed render planner | Dry-run/default metadata planning. `--execute` must use a sandbox such as `reproduction_runs/<RUN_ID>/` and requires explicit authorization. It must not write accepted `F_FINAL_REVIEWED/`. |

## Historical XWC / F Scripts

| Script | Status | Rule |
| --- | --- | --- |
| `generate_xwc_f_final_reviewed.py` | historical XWC F generator | Do not run routinely. Historical XWC/Baiya script that can read/write audio, review data, latest exports, and F outputs. |
| `refresh_xwc_r1_full_tail_and_regenerate_f.py` | historical repair/regeneration | Do not use as a workflow entrypoint. Historical repair script that can rewrite R1/F/latest/derived outputs. |
| `verify_r2_canonical_draft.py` | older verifier | Mostly superseded by `verify_r2_render_manifest.py`; only use with explicit path scope and authorization. |

## Accepted Baseline Rule

Accepted baseline / forbidden-to-touch:

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`

Any accepted-baseline write requires a separate task and explicit authorization. Repo hygiene/index tasks must not touch it.

## Authority Boundary

- R2 canonical authority: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML exports are derived, not canonical.
- `tools/cg-varw/review_outputs/` is generated non-canonical local workbench output.
- Do not run renderer, ingest, ML, frontend build, backend scripts, second-piece, G, or F2 workflows during hygiene/index tasks.
