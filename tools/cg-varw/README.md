# CG-VARW

Cyber Guqin Visual Anchor Review Workbench.

R0B now includes a review-only FastAPI backend for raw root scanning, WAV metadata/waveform extraction without ffmpeg, draft save, and three review-only CSV exports. It does not execute split, create sample assets, render audio, or create ML data.

## Backend

The backend should run with Python 3.11 or newer.

macOS:

```bash
cd tools/cg-varw/backend
/opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
CG_VARW_RAW_ROOT="/path/to/your/raw_audio" /opt/homebrew/bin/python3.11 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

Windows:

```powershell
cd tools\cg-varw\backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:CG_VARW_RAW_ROOT="D:\path\to\your\raw_audio"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

If `CG_VARW_RAW_ROOT` is not set, the backend falls back to `tools/cg-varw/sample_workspace/raw_audio` and the UI reports that it is using the synthetic demo root.

R1 split review can point either to a single batch root or to a parent `split_preview` root:

```bash
CG_VARW_SPLIT_ROOT="/path/to/split_preview" /opt/homebrew/bin/python3.11 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
CG_VARW_SPLIT_ROOT="/path/to/split_preview/batch02" /opt/homebrew/bin/python3.11 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8787
```

When the split root is the parent directory, the backend discovers child `batchXX` directories with R1 intake files and keeps each batch separate in the R1 UI.

## R2 ABCD render-set intake

When the XWC Baiya ABCD intake package exists at:

```text
04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_intake/
```

the R2 backend prefers that real experimental render set over the built-in mock store. Start the backend as usual, then inspect:

```text
GET /api/r2/render-sets
GET /api/r2/render-sets/R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e/versions
GET /api/r2/render-sets/R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e/phrase-alignments
```

This intake is review-only. It does not generate E, choose a best version, write sample assets, or start ML training.

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
python -m unittest app.tests.test_csv_contracts app.tests.test_r1_marker_seed app.tests.test_waveform_service

cd ..\frontend
npm run build
npm run typecheck
```
