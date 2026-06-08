# RS_XWC_001_MVP_PILOT

Session ID: `RS_XWC_001_MVP_PILOT`

Asset class: `mvp_experimental_raw`

Production grade: `false`

This folder preserves the first MVP pilot raw audio batch for 《仙翁操》 by 三曼. The original M4A files are stored in `raw/` with filenames unchanged from `batch01.m4a` through `batch07.m4a`.

This session is registered only as MVP experimental raw audio.

Guardrails:

- Do not continue repairing the failed experimental clean segments.
- Do not promote any experimental split output from this pilot to sample candidate.
- Do not write `sample_assets` rows from this batch.
- Do not write `03_samples` rows from this batch.
- Do not treat this batch as the final Sanman standard sample library.
- Do not use this batch as an ML training baseline.

Closure decision:

- `RS_XWC_001_MVP_PILOT` failed as usable audio-sample MVP.
- `RS_XWC_001_MVP_PILOT` partially succeeded as split workflow discovery.
- No experimental clean segment from this pilot may be promoted to sample candidate.
- No experimental clean segment from this pilot may be treated as production sample.

The next allowed phase is recording reshoot preparation. The next MVP pilot should use a new Baiya performer ID and WAV-first recording rules; Sanman remains `QINIST_001` for later formal sampling.
