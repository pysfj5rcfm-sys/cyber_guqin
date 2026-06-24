# 06_docs Index

This index labels legacy V1 project documentation without moving or deleting any file.

Status values:

- `current`: safe current reference for the stated scope.
- `partially-current`: still useful, but must be read with newer P1-F / Sanman / R2 authority docs.
- `historical`: historical evidence or retrospective; not a current workflow entry.
- `superseded-by`: replaced for current workflow decisions by another document.
- `index-only`: an index or directory boundary document.

## Current / Index Documents

| File | Status | Role |
| --- | --- | --- |
| `PROJECT_STRUCTURE.md` | `current` | Current directory boundary and authority policy. |
| `INDEX.md` | `index-only` | This status index for `06_docs/`. |
| `GESTURE_ONTOLOGY.md` | `partially-current` | V1 gesture ontology reference; do not let draft canon work silently overwrite it. |
| `RECORDING_INGEST_SCHEMA.md` | `partially-current` | Recording ingest schema notes; current work is not sample ingest. |

## Legacy Runtime / Pilot Documents

| File | Status | Role |
| --- | --- | --- |
| `PHASE_0_1_BASELINE.md` | `historical` | Phase 0.1 baseline reference. |
| `PROJECT_STATUS_RECORDING_SAMPLE_STAGE.md` | `historical` | Earlier recording/sample-stage status. |
| `NEXT_RECORDING_PLAN_BAIYA.md` | `historical` | Earlier Baiya recording planning note. |
| `RS_XWC_002_BAIYA_RECORDING_PLAN_REVIEW.md` | `historical` | Baiya recording-plan review evidence. |
| `MVP_PILOT_FAILURE_REVIEW.md` | `historical` | Pilot failure review / lessons evidence. |
| `CYBER_GUQIN_V1_EVOLUTION_REVIEW.md` | `historical` | Evolution review. |
| `NOTES.md` | `historical` | General notes; verify against current entrypoints before use. |

## Split / Recording Helper References

| File | Status | Role |
| --- | --- | --- |
| `FORMAL_RECORDING_SPLIT_REUSE_PLAN.md` | `partially-current` | Split/reuse planning reference; not a hygiene-task command entry. |
| `GUQIN_SLATE_BASED_SPLIT_PIPELINE.md` | `partially-current` | Slate split pipeline reference; any audio/split execution needs separate authorization. |

## Current External Entrypoints

For current P1-F dry-run reproduction, use:

- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- `docs/cyber_guqin/INDEX.md`
- `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `examples/cyber_guqin/README.md`

For reports and latest R0 evidence, use `reports/REPORTS_INDEX.md`.

## Authority Notes

- Accepted baseline / forbidden-to-touch: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- R2 canonical authority: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML exports are derived, not canonical.
- `reports/` is audit/status evidence, not runtime output.
