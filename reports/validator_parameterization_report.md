# Validator Parameterization Report

## Scope

Phase R1 parameterized the QXBY batch validator scripts for future OCR import batches while preserving QXBY_BATCH_001 defaults.

Modified scripts:

- `scripts/validate_qxby_batch.py`
- `scripts/audit_qxby_batch_sources.py`

Added report:

- `reports/validator_parameterization_report.md`

## CLI Parameters

`scripts/validate_qxby_batch.py` now supports:

- `--batch-id`
- `--draft`
- `--expected-count`
- `--report`
- `--strict`
- `--allow-warnings`

`scripts/audit_qxby_batch_sources.py` now supports:

- `--batch-id`
- `--draft`
- `--source-dir`
- `--manifest`
- `--expected-count`
- `--report-md`
- `--report-json`

## Default Compatibility

No-argument `validate_qxby_batch.py` remains equivalent to:

```powershell
python scripts/validate_qxby_batch.py --batch-id QXBY_BATCH_001 --draft canon/drafts/qxby_batch_001.yaml --expected-count 16 --report reports/validate_qxby_batch_001_report.json
```

No-argument `audit_qxby_batch_sources.py` remains equivalent to:

```powershell
python scripts/audit_qxby_batch_sources.py --batch-id QXBY_BATCH_001 --draft canon/drafts/qxby_batch_001.yaml --source-dir sources/qinxue_beiyao/QXBY_BATCH_001 --manifest sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml --expected-count 16 --report-md reports/qxby_batch_001_source_audit.md --report-json reports/qxby_batch_001_source_audit.json
```

QXBY_BATCH_001 keeps its 16 required-term regression checks. Future batches without a predefined required item list use generic item count, required field, review-status, OCR/manual-transcription, conflict-field, and complex-technique sound-type guardrails.

## Verification

Verification was run in temporary copy:

- `D:\AIProjects\cyber_guqin\Cyber_Guqin_v1_R1_verify_tmp_20260605140800`

QXBY validators:

- `python scripts/validate_qxby_batch.py`: pass
- `python scripts/audit_qxby_batch_sources.py`: pass
- `python scripts/validate_qxby_batch.py --batch-id QXBY_BATCH_001 --draft canon/drafts/qxby_batch_001.yaml --expected-count 16 --report reports/validate_qxby_batch_001_report.json`: pass
- `python scripts/audit_qxby_batch_sources.py --batch-id QXBY_BATCH_001 --draft canon/drafts/qxby_batch_001.yaml --source-dir sources/qinxue_beiyao/QXBY_BATCH_001 --manifest sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml --expected-count 16 --report-md reports/qxby_batch_001_source_audit.md --report-json reports/qxby_batch_001_source_audit.json`: pass

Mainline validation:

- `python scripts/validate_canon.py`: pass
- `python scripts/validate_dapu_ir.py`: pass
- `python scripts/check_v1_compat.py`: passed with existing recommendation warning
- `python scripts/validate_canon_seed.py`: pass

The validation used Codex bundled Python 3.12.13 because the local user Python executable was intermittently denied by the sandbox.

## Files Not Modified

This round did not modify:

- `00_global/`
- `01_pieces/`
- `02_recordings/`
- `03_samples/`
- `04_outputs/`
- `05_scripts/`
- `.agents/`
- `canon/*.yaml`
- `canon/drafts/qxby_batch_001.yaml`
- `sources/qinxue_beiyao/QXBY_BATCH_001/`
- `references/`
- `schemas/`
- `tests/fixtures/`
- existing QXBY_BATCH_001 data files

This round did not create QXBY_BATCH_002, recording ingest files, recording item enrichment files, V1 patch scripts, ML training scripts, or real recording split scripts.

## Future QXBY_BATCH_002 Invocation

Example validator call:

```powershell
python scripts/validate_qxby_batch.py --batch-id QXBY_BATCH_002 --draft canon/drafts/qxby_batch_002.yaml --expected-count <count> --report reports/validate_qxby_batch_002_report.json
```

Example source audit call:

```powershell
python scripts/audit_qxby_batch_sources.py --batch-id QXBY_BATCH_002 --draft canon/drafts/qxby_batch_002.yaml --source-dir sources/qinxue_beiyao/QXBY_BATCH_002 --manifest sources/qinxue_beiyao/QXBY_BATCH_002/manifest.yaml --expected-count <count> --report-md reports/qxby_batch_002_source_audit.md --report-json reports/qxby_batch_002_source_audit.json
```
