# Phase R0 Architecture Review

Date: 2026-06-05

Scope: Cyber Guqin v1 architecture review and slimming audit only. No files were deleted, moved, renamed, or modified outside the three Phase R0 report outputs. Validation commands were run in a temporary copy because the validator scripts write report files and `05_scripts/smoke_test.py` regenerates V1 mainline outputs.

## Executive Summary

The current project is structurally coherent enough to enter the next OCR and recording phases, but it has accumulated three kinds of historical weight:

1. Runtime generation scripts and persistent runtime scripts are both in `05_scripts/`.
2. Batch-specific QXBY validators are in `scripts/` and should become parameterized long-term tools before `QXBY_BATCH_002`.
3. `reports/` mixes current status, historical audits, regenerable validator output, and skill install staging.

No immediate rename is recommended. The safer next move is to keep the existing paths stable and document boundaries in `06_docs/PROJECT_STRUCTURE.md` before any archive or rename pass.

## Counts

| Item | Count |
| --- | ---: |
| Python scripts total | 13 |
| `05_scripts/*.py` | 7 |
| `scripts/*.py` | 6 |
| `tests/fixtures` files | 3 |
| pre-R0 report files under `reports/` | 15 |
| `QXBY_BATCH_001` source images | 16 |
| untracked nonignored files | 0 |
| cache/disposable findings | 1 ignored `.DS_Store` |

`.gitignore` already contains `.DS_Store`, `__pycache__/`, `*.pyc`, and `.pytest_cache/`. No `.gitignore` edit is needed in Phase R0.

## Directory Classification

### A. Core Runtime

These files support the V1 Dapu Mode runtime and should stay in place:

- `00_global/`: global ontology, lexicon, parsing, sample policy, qin/qinist/tuning registries.
- `01_pieces/`: `xianwengcao` score events, phrase structure, rhythm candidates, recording scripts.
- `02_recordings/`: recording session metadata.
- `03_samples/`: sample assets, recording segments, and current WAV sample library.
- `04_outputs/`: rendered audio and audio viability outputs.
- `05_scripts/`: V1 runtime and regeneration scripts.
- `06_docs/`: baseline docs and structure documentation.

### B. Core Skills Infrastructure

These are the skills/canon/validator support layer:

- `.agents/skills/guqin-canon-builder/SKILL.md`
- `.agents/skills/guqin-dapu-parser/SKILL.md`
- `schemas/*.schema.json`
- `references/*.md`
- `tests/fixtures/*`
- `scripts/validate_canon.py`
- `scripts/validate_dapu_ir.py`
- `scripts/check_v1_compat.py`
- `scripts/validate_canon_seed.py`

### C. Canon Data

Canon seed files are clearly separated from draft ingest:

- Seed: `canon/alias_rules.yaml`, `canon/component_lexicon.yaml`, `canon/gesture_families.yaml`, `canon/sources.yaml`, `canon/technique_rules.yaml`, `canon/terms.yaml`, `canon/validation_rules.yaml`
- Draft: `canon/drafts/qxby_batch_001.yaml`

This split is healthy. `qxby_batch_001.yaml` should remain a draft until human review and OCR/transcription uncertainty are resolved.

### D. Source Evidence

`sources/qinxue_beiyao/QXBY_BATCH_001/` contains:

- `manifest.yaml`
- `README.md`
- 16 source images under `images/`

Temporary-copy validation found draft, manifest, and image linkage passing with no orphan images, missing files, or filename mismatches.

### E. Reports / Audit Trail

`reports/` currently contains current status reports, historical audit reports, regenerable validator JSON/MD outputs, and skill install staging. This is the main directory needing slimming after confirmation.

### F. Disposable / Generated / Cache

Found one ignored `.DS_Store` at project root. No `__pycache__`, `.pytest_cache`, or `*.pyc` files were found in the live project scan.

### G. Candidate for Parameterization

The following are batch-specific today and should be parameterized before the next OCR batch:

- `scripts/validate_qxby_batch.py`
- `scripts/audit_qxby_batch_sources.py`

They should accept batch id, draft path, source directory, manifest path, expected image/item count, and report prefix. Keep them in `scripts/`; do not merge `05_scripts/` and `scripts/`.

## Script Audit

| Path | Purpose | Category | Recommendation | One-off? | Writes files? | V1 runtime? | Canon/skills validator? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `05_scripts/audio_viability_review.py` | Review rendered audio and write audio viability reports. | Core Runtime | keep | no | yes | yes | no |
| `05_scripts/export_recording_checklist.py` | Export human recording checklist and recording batch docs. | Core Runtime | keep | no | yes | yes | no |
| `05_scripts/generate_recording_script.py` | Generate `recording_script.csv` from score events. | Core Runtime | review | likely | yes | yes | no |
| `05_scripts/generate_rhythm.py` | Generate rhythm candidate CSVs. | Core Runtime | review | likely | yes | yes | no |
| `05_scripts/make_dummy_samples.py` | Generate dummy WAVs and `sample_assets.csv`. | Core Runtime | review | likely | yes | yes | no |
| `05_scripts/render_audio.py` | Render candidate audio and render event report. | Core Runtime | keep | no | yes | yes | no |
| `05_scripts/smoke_test.py` | Run regenerating V1 smoke pipeline. | Core Runtime | keep | no | yes | yes | no |
| `scripts/audit_qxby_batch_sources.py` | Audit QXBY batch source/draft linkage. | Candidate for Parameterization | parameterize | no | yes | no | yes |
| `scripts/check_v1_compat.py` | Check skills/canon against V1 compatibility. | Core Skills Infrastructure | keep | no | yes | no | yes |
| `scripts/validate_canon.py` | Validate Phase S0 minimal canon fixture. | Core Skills Infrastructure | keep | no | yes | no | yes |
| `scripts/validate_canon_seed.py` | Validate canon seed YAML files. | Core Skills Infrastructure | keep | no | yes | no | yes |
| `scripts/validate_dapu_ir.py` | Validate minimal Dapu Event IR fixture. | Core Skills Infrastructure | keep | no | yes | no | yes |
| `scripts/validate_qxby_batch.py` | Validate QXBY_BATCH_001 draft ingest. | Candidate for Parameterization | parameterize | no | yes | no | yes |

Recommended boundary: `05_scripts/` remains V1 runtime scripts; `scripts/` remains skills/canon/validator scripts. Do not merge them in this phase.

`05_scripts/smoke_test.py` is important but should be documented as a regenerating pipeline, not as a harmless read-only test. It rewrites or regenerates `recording_script.csv`, `sample_assets.csv`, dummy WAV samples, rhythm candidates, rendered WAVs, and audio reports.

## Fixtures Audit

| Path | Still valuable? | Phase S0 minimal? | Long-term smoke fixture? | Needs doc note? |
| --- | --- | --- | --- | --- |
| `tests/fixtures/canon_minimal.yaml` | yes | yes | yes | yes |
| `tests/fixtures/xianwengcao_events_minimal.jsonl` | yes | yes | yes | yes |
| `tests/fixtures/xianwengcao_tokens_minimal.jsonl` | yes | yes | yes | yes |

Recommendation: keep all three. Add a note in `README.md` or `06_docs/PROJECT_STRUCTURE.md` that these are intentionally small smoke fixtures, not complete canon or complete `xianwengcao` data.

## Reports Audit

### Current Status Reports

Keep in `reports/` root for now:

- `reports/canon_seed_report.md`
- `reports/qxby_batch_001_human_review.md`

### Historical Audit Reports

Candidates to archive under `reports/archive/` after confirmation:

- `reports/skills_v1_integration_report.md`
- `reports/v1_compat_audit.md`
- `reports/qxby_batch_001_report.md`

### Regenerable Reports

Candidates to regenerate on demand, or move under batch/run-specific report paths after confirmation:

- `reports/check_v1_compat_report.json`
- `reports/validate_canon_report.json`
- `reports/validate_canon_seed_report.json`
- `reports/validate_dapu_ir_report.json`
- `reports/validate_qxby_batch_001_report.json`
- `reports/qxby_batch_001_source_audit.json`
- `reports/qxby_batch_001_source_audit.md`

### Skill Install Staging

`.agents/skills` is present in the project and appears to contain the installed skill files. Therefore:

- `reports/skill_install_staging/` likely no longer needs to remain active in `reports/`.
- `reports/skill_install_instructions.md` can be archived after confirmation.
- Do not delete them in Phase R0.

## Canon And Sources

`canon seed` and `canon draft` are clearly separated. `QXBY_BATCH_001` remains draft/manual image transcription evidence, not verified canon. The source-image linkage is currently healthy: temporary validation found 16 draft items, 16 manifest items, 16 images, matching item ids, and no orphan/missing image files.

Risk to watch: source image and draft linkage is encoded across filename conventions, manifest entries, and `source_image` paths. This works for Batch 001, but scaling to OCR batches needs a uniform batch contract before Batch 002.

Recommended future batch pattern:

- `sources/qinxue_beiyao/QXBY_BATCH_002/`
- `sources/qinxue_beiyao/QXBY_BATCH_002/images/`
- `sources/qinxue_beiyao/QXBY_BATCH_002/transcriptions/`
- `sources/qinxue_beiyao/QXBY_BATCH_002/manifest.yaml`
- `canon/drafts/qxby_batch_002.yaml`
- `reports/qxby_batch_002_report.md`
- `reports/qxby_batch_002_source_audit.md`

## Naming Findings

There is naming-style inconsistency, but it is manageable:

- Runtime directories use numeric prefixes: `00_global` through `06_docs`.
- Skills/canon directories use semantic names: `canon`, `sources`, `schemas`, `scripts`, `tests`.
- Source batch names use uppercase `QXBY_BATCH_001`; draft/report filenames use lowercase `qxby_batch_001`.
- `05_scripts/` mixes persistent runtime tools with regeneration/bootstrap utilities.

Recommendation: do not immediately rename. First document boundaries in `06_docs/PROJECT_STRUCTURE.md`, then consider any archive or naming changes as a separate confirmed phase.

## Next-Phase Structure

1. OCR batch should live under `sources/<source_slug>/<BATCH_ID>/`, for example `sources/qinxue_beiyao/QXBY_BATCH_002/`.
2. OCR original images should live under `sources/qinxue_beiyao/QXBY_BATCH_002/images/`.
3. OCR transcription text should live under `sources/qinxue_beiyao/QXBY_BATCH_002/transcriptions/`, with stable names matching manifest item ids.
4. Canon draft should live under `canon/drafts/qxby_batch_002.yaml`.
5. Batch validators should be parameterized around `--batch-id`, `--draft`, `--source-dir`, `--manifest`, `--expected-count`, and `--report-prefix`.
6. Real recording raw audio should live under `02_recordings/<piece_id>/<session_id>/raw/`.
7. Real recording session manifest should live under `02_recordings/<piece_id>/<session_id>/session_manifest.yaml` or a CSV equivalent that can map takes to `recording_sessions.csv`.
8. Sliced samples should enter `03_samples` only through a manifest-backed ingest step that updates `03_samples/sample_assets.csv` and places WAVs under the existing qin/tuning/gesture directory convention.
9. Phase-result reports should be stable human/audit summaries; validator JSON, source-audit JSON, render event CSV, and smoke outputs are regenerable unless explicitly frozen as evidence.

## Validation

Commands were run in temporary copy `D:/AIProjects/cyber_guqin/Cyber_Guqin_v1_R0_verify_tmp_20260605131203`.

| Command | Result |
| --- | --- |
| `scripts/validate_canon.py` | pass |
| `scripts/validate_dapu_ir.py` | pass |
| `scripts/check_v1_compat.py` | pass, with warning: minimal patch recommended for first-class Dapu Event IR fields |
| `scripts/validate_canon_seed.py` | pass |
| `scripts/validate_qxby_batch.py` | pass |
| `scripts/audit_qxby_batch_sources.py` | pass |
| `05_scripts/smoke_test.py` | pass |

The commands were not run against the live project because doing so would overwrite existing reports and, for smoke test, regenerate mainline runtime data.
