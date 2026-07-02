# QXBY Full Component Atlas Sources

Status labels: `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`, `SOURCE_REFERENCE_IMAGE`, `USER_PROVIDED_QXBY_COMPONENT_SET`, `NOT_SCORE_EVENT_AUTHORITY`, `NOT_DAPU_IR_AUTHORITY`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`, `NOT_RENDER_OUTPUT`, `NEEDS_CANON_BUILDER_CROSSWALK_REVIEW`

This directory stores normalized source/reference images for the full QXBY component atlas. The images are copied from the nine user-provided zip files and registered as `SOURCE_REFERENCE_IMAGE` under `QXBY_FULL_COMPONENT_ATLAS_REFERENCE`.

These files are not score-event authority, not Dapu IR authority, not sample ingest, not ML training data, and not render output.

## Layout

- `source_inventory.v0.1.json`: auditable source zip inventory and per-image registration metadata.
- `source_inventory.v0.1.csv`: flat inventory for review.
- `images/<category_slug>/COMP-100_<label>.png`: normalized source images.

## ID Policy

The full-atlas sequence starts at `COMP-100` and currently covers `COMP-100..COMP-273`. Existing pilot IDs `COMP-001..037` are preserved in the legacy registry and are not overwritten here.

## Filename Encoding

Python `zipfile` direct listing showed mojibake in the source zip internal names. Registration used `ditto -x -k` extraction to `/tmp`, then verified Chinese filenames before writing normalized images.
