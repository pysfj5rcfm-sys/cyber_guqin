# QXBY_BATCH_002 Source Audit

- status: `pass`
- passed: `true`
- draft: `canon/drafts/qxby_batch_002.yaml`
- manifest: `sources/qinxue_beiyao/QXBY_BATCH_002/manifest.yaml`
- images: `sources/qinxue_beiyao/QXBY_BATCH_002/images`

## Summary

- draft items: 8
- manifest items: 8
- image files: 8
- expected count: 8
- item ids match: True
- orphan images: []
- manifest missing files: []
- draft missing files: []
- source_image outside source dir: []
- term mismatches: []
- internal_name mismatches: []
- draft items missing internal_name: []
- draft mapped_component_name empty: []
- filename mismatches: []

## Semantic Rules

- `manifest.internal_name` is aligned with draft `internal_name` when that field is present.
- `mapped_component_name` is a semantic mapping field in the draft and is no longer required to equal manifest `internal_name`.
- Source image filenames are human-readable archive aids; filename term mismatches are warnings when referenced files exist.

## Errors

- none

## Warnings

- none
