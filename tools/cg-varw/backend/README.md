# CG-VARW FastAPI Backend

This backend serves the R0B raw review workflow. It is review-only and never creates split audio, sample assets, render output, or ML training data.

## Raw Root

Raw root priority:

1. `CG_VARW_RAW_ROOT`
2. `backend/config.local.json`
3. `tools/cg-varw/sample_workspace/raw_audio`

If no real raw root is configured, the backend falls back to the synthetic demo workspace and reports demo mode.

Example `config.local.json`:

```json
{
  "raw_root": "D:\\path\\to\\your\\raw_audio",
  "split_root": "D:\\path\\to\\your\\split_preview"
}
```

Do not commit `.env.local` or `config.local.json`.

## Local Startup

The backend uses modern Python typing syntax and should run with Python 3.11 or newer. In VSCode, select the same Python 3.11 interpreter that has `fastapi`, `pydantic`, and `uvicorn` installed.

macOS:

```bash
cd tools/cg-varw/backend
/opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
CG_VARW_RAW_ROOT="/path/to/your/raw_audio" /opt/homebrew/bin/python3.11 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

Windows:

Backend:

```powershell
cd tools\cg-varw\backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:CG_VARW_RAW_ROOT="D:\path\to\your\raw_audio"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

Frontend:

```powershell
cd tools\cg-varw\frontend
npm install
$env:VITE_CG_VARW_API_BASE="http://127.0.0.1:8787"
npm run dev -- --host 127.0.0.1 --port 5173
```

Browser:

```text
http://127.0.0.1:5173/
```

## Implemented APIs

- `GET /api/health`
- `GET /api/r0/raw-files`
- `GET /api/r0/raw-files/{file_id}/metadata`
- `GET /api/r0/raw-files/{file_id}/audio`
- `GET /api/r0/raw-files/{file_id}/waveform?points=1600`
- `GET /api/r0/raw-files/{file_id}/asr-candidates`
- `GET /api/r0/raw-files/{file_id}/review-units`
- `POST /api/r0/reviews/save`
- `POST /api/r0/reviews/export`
- `GET /api/r1/batches`
- `GET /api/r1/batches/{batch_id}/segments`
- `GET /api/r1/segments/{segment_id}/metadata`
- `GET /api/r1/segments/{segment_id}/audio`
- `GET /api/r1/segments/{segment_id}/waveform?points=1600`
- `POST /api/r1/reviews/save`
- `POST /api/r1/reviews/export`

R1 `CG_VARW_SPLIT_ROOT` supports both a single batch root and a parent `split_preview` root. Parent mode discovers child `batchXX` folders that contain `r1_synthetic_split_manifest.json`, `manifests/recd2_split_preview_manifest.csv`, `manifests/r1_intake_pointer.yaml`, or `clean_previews/`.

R0 and R1 waveform endpoints share the same downsample/cache service. The cache is in-process only and is not written to recording, sample, render, or repo asset directories.

Drafts are saved under:

```text
tools/cg-varw/review_outputs/r0/drafts/
```

CSV exports are saved under:

```text
tools/cg-varw/review_outputs/r0/exports/{file_id}/
```

Generated drafts and CSV exports are ignored by git.

## Validation

```powershell
cd tools\cg-varw\backend
python -m compileall app
python -m unittest app.tests.test_csv_contracts app.tests.test_r1_marker_seed app.tests.test_waveform_service
```
