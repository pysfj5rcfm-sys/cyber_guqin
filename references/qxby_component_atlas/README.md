# QXBY Component Atlas References

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `SOURCE_REFERENCE_IMAGE`, `USER_PROVIDED_QXBY_COMPONENT_SET`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`

This directory contains QXBY component reference registries. The legacy pilot registry remains in `component_registry.v0.1.json`; the new full atlas is registered separately under `component_registry.full.v0.1.json` with IDs starting at `COMP-100`.

## Current Files

- `component_registry.v0.1.json` / `.md`: legacy pilot component reference layer. Do not delete, renumber, or overwrite old IDs.
- `construction_templates.v0.1.json` / `.md`: legacy/reviewed construction-template reference layer for component-guided transcription.
- `component_registry.full.v0.1.json` / `.md`: full QXBY component atlas reference from nine user-provided zips.
- `component_legacy_alias_map.v0.1.json` / `.md`: reviewable mapping from old pilot IDs to full-atlas IDs.
- `component_to_canon_crosswalk.seed.v0.1.json` / `.md`: seed-only canon-builder crosswalk.

## Authority Boundary

The full atlas is authoritative only for source image identity, filename-derived labels, categories from zip/folder names, file hashes, registry IDs, and legacy alias evidence. It is not canon term authority, not phrase score authority, not Dapu IR authority, not sample ingest, not ML training data, and not render output.

Future phrase recognition may read the full atlas as reference evidence, but unknown future glyphs must be marked as `component_gap` instead of force-matched.
