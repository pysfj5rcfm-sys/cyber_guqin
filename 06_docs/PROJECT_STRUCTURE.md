# Cyber Guqin v1 Project Structure

Cyber Guqin v1 currently uses two directory styles. This is intentional project structure, not an error: the V1 runtime/Dapu Mode tree preserves the working performance pipeline, while the Skills/Canon/Validator tree supports rule-book canon work, audits, and non-invasive validation.

## 1. V1 Runtime / Dapu Mode Mainline

- `00_global/`: Global data and ontology files for the V1 runtime mainline.
- `01_pieces/`: Piece data; the current focus is `xianwengcao`.
- `02_recordings/`: Real recording sessions and raw audio locations.
- `03_samples/`: Cut sample assets derived from recordings.
- `04_outputs/`: Rendered outputs and runtime reports.
- `05_scripts/`: V1 runtime scripts for recording script generation, dummy samples, rhythm, rendering, smoke tests, and related runtime work.
- `06_docs/`: V1 project documentation.

These folders are the runtime-facing project spine. Canon draft work must not overwrite them or quietly redefine their data contracts.

## 2. Skills / Canon / Validator Engineering Tree

- `.agents/`: Codex agent assets; `.agents/skills/` stores Codex skills.
- `canon/`: Canon seed files, drafts, and future verified rule data.
- `canon/drafts/`: Unverified rule batches such as `qxby_batch_001.yaml`.
- `sources/`: External source evidence, such as archived `琴学备要` screenshots.
- `references/`: Normalization, validation, and V1 mapping notes.
- `reports/`: Audit, validation, and review reports.
- `schemas/`: Skills, Canon, and Dapu IR schemas.
- `scripts/`: Canon, skills, validator, compatibility, and source-audit helper scripts.
- `tests/`: Test fixtures; `tests/fixtures/` stores minimal fixtures.

This tree is for canon engineering and review. Drafts here can inform future verified canon work, but they do not directly patch V1 runtime files.

## 3. `05_scripts/` vs `scripts/`

`05_scripts/` = V1 runtime scripts, serving recording, sampling, rhythm, render, and smoke-test workflows.

`scripts/` = Skills/Canon/Validator scripts, serving canon seed checks, QXBY drafts, compatibility checks, and source audits.

The two script trees must not be mixed. Runtime scripts should not absorb canon draft logic, and validator scripts should not perform recording ingest or audio rendering.

## 4. Current Recommended Principles

- Do not rename the `00_*` directories.
- Do not mix canon drafts into `00_global/`.
- Do not place source screenshots in `canon/`.
- Do not treat `reports/` as runtime output.
- Do not let Step 2B drafts overwrite Gesture Ontology v1.1.
- Do not treat `recording_batches.md` as a source of score facts.
