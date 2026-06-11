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
  "raw_root": "D:\\path\\to\\your\\raw_audio"
}
```

Do not commit `.env.local` or `config.local.json`.

## Windows Startup

Backend:

```powershell
cd tools\cg-varw\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:CG_VARW_RAW_ROOT="D:\path\to\your\raw_audio"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
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
```
