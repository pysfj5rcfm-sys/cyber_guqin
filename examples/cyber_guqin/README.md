# examples/cyber_guqin

This directory contains example manifests, fixtures, and starter-kit mock examples for P1-F dry-run reproduction and Sanman/QINIST starter design.

## Contents

- `xwc_recording_plan_config.yaml`: example recording-plan config.
- `xwc_dapu_ir_minimal_fixture.jsonl`: minimal Dapu IR fixture.
- `xwc_abcd_render_manifest.yaml`: example ABCD render-planning manifest.
- `xwc_r2_render_verify_manifest.yaml`: example R2/final verifier manifest.
- `xwc_final_render_manifest.yaml`: example final-reviewed render manifest.
- `qinist_starter_kit/`: mock starter-kit examples for candidate sidecar, profile signal extension, prompt manifest, and single-piece Dapu IR input.

## Boundary

These files are:

- example manifests / fixtures;
- dry-run reproduction inputs;
- starter-kit mock examples;
- useful for understanding the manifest shape and workflow gates.

These files are not:

- real production samples;
- accepted baseline authority;
- R2 canonical authority;
- permission to bypass score, canon, R2, or F gates;
- sample ingest, ML training, or Arrangement Mode production inputs.

## Authority Rules

- Accepted baseline / forbidden-to-touch: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
- R2 canonical authority: `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- R2 CSV/YAML exports are derived.
- Any real second-piece or production path needs its own score/canon authority, piece/session/qinist config, Dapu IR, recording config, ABCD manifest, final manifest, dry-run review, and explicit authorization.
