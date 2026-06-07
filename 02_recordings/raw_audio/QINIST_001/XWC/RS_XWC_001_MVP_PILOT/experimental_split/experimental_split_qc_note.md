# Experimental Split QC Note

Session: `RS_XWC_001_MVP_PILOT`

## QC Status

- Segment candidates created: 71
- Missing segments: 0
- Boundary review rows: 64
- Working WAV files generated/reused: 7

## Scope

- This run is experimental auto split only.
- This run did not write `03_samples`.
- This run did not write `sample_assets`.
- This run did not create `recording_items_enriched`.
- This run did not modify raw master audio.
- This run did not modify V1 runtime.
- This run did not modify legacy recording scripts.
- Next step is determined by whether segment candidates exist; this is not production sample ingest.

## Converter

ffmpeg was used for working WAV conversion with ffmpeg_pcm_s16le_wav. The source files remain M4A/AAC experimental raw material and do not become production sources.
