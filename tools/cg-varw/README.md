# CG-VARW

Cyber Guqin Visual Anchor Review Workbench.

R0B now includes a review-only FastAPI backend for raw root scanning, WAV metadata/waveform extraction without ffmpeg, draft save, and three review-only CSV exports. It does not execute split, create sample assets, render audio, or create ML data.

## Windows Backend

```powershell
cd tools\cg-varw\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:CG_VARW_RAW_ROOT="D:\path\to\your\raw_audio"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

If `CG_VARW_RAW_ROOT` is not set, the backend falls back to `tools/cg-varw/sample_workspace/raw_audio` and the UI reports that it is using the synthetic demo root.

## Windows Frontend

```powershell
cd tools/cg-varw/frontend
npm install
$env:VITE_CG_VARW_API_BASE="http://127.0.0.1:8787"
npm run dev -- --host 127.0.0.1 --port 5173
```

Open `http://127.0.0.1:5173/`.

## Validate

```powershell
cd tools\cg-varw\backend
python -m compileall app

cd ..\frontend
npm run build
npm run typecheck
```
