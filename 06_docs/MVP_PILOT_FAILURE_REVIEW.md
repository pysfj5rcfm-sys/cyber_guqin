# MVP Pilot Failure Review

## Closure Statement

RS_XWC_001_MVP_PILOT failed as usable audio-sample MVP.
RS_XWC_001_MVP_PILOT partially succeeded as split workflow discovery.
No experimental clean segment from this pilot may be promoted to sample candidate.
No experimental clean segment from this pilot may be treated as production sample.

Required classification:

- asset_class: mvp_experimental_raw
- production_grade: false
- not_standard_sample_library: true
- not ML training baseline
- not final Sanman standard sample archive

## Pilot Goal

The pilot attempted to prove whether legacy XWC M4A batch recordings by Sanman could be split into clean guqin sample material quickly enough to support the first MVP audio sample library.

## Raw M4A Inputs

- `raw/batch01.m4a`
- `raw/batch02.m4a`
- `raw/batch03.m4a`
- `raw/batch04.m4a`
- `raw/batch05.m4a`
- `raw/batch06.m4a`
- `raw/batch07.m4a`

The raw M4A files remain preserved as evidence. They are not production-grade masters.

## Why The Audio-Sample MVP Failed

The failure was caused by recording structure and source quality, not by the ontology, skills, canon, or V1 runtime direction.

Primary causes:

- Spoken slate and guqin performance were too close together.
- Guqin tail decay often overlapped or touched the next spoken slate.
- M4A/AAC is not an ideal production-like source for sample extraction.
- `recording_take_no` and `batch_take_no` naming created confusion risk.
- Multi-round repair still left spoken residue in clean segments.
- Some cuts removed guqin performance content or created naming mismatch risk.

The slate-ASR idea did not fail as a workflow concept. It helped discover the right split architecture, but the source recording did not contain enough acoustic separation for reliable clean samples.

## Workflow Discoveries That Remain Valid

The reusable process is:

```text
recording plan / take manifest
-> batch range lock
-> ASR slate anchor recognition
-> manual override
-> reviewed anchor manifest
-> anchor-locked unit split
-> unit-internal slate trim
-> human listening QC
-> experimental sample candidate
```

## Deprecated Workflows

- Pure energy sequential alignment.
- Targeted repair based on already-failed clean segments.
- Direct clean split from unreviewed anchors.
- Codex-only automatic QC as a decision that audio is usable.

## Next Plan

- Re-record the MVP pilot.
- Performer: Baiya.
- Use skills to generate a new `recording_batch.md`.
- Add explicit spacing between slate and performance.
- Preserve guqin tail decay before the next slate.
- Prefer raw WAV, 48 kHz / 24-bit.
- Treat sample ingest as a separate future authorization.
