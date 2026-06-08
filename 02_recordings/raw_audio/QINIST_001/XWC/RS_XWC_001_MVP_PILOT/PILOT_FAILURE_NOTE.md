# RS_XWC_001_MVP_PILOT Failure Note

RS_XWC_001_MVP_PILOT failed as usable audio-sample MVP.
RS_XWC_001_MVP_PILOT partially succeeded as split workflow discovery.
No experimental clean segment from this pilot may be promoted to sample candidate.
No experimental clean segment from this pilot may be treated as production sample.

## Required Classification

- asset_class: mvp_experimental_raw
- production_grade: false
- not_standard_sample_library: true
- not ML training baseline
- not final Sanman standard sample archive

## Human Review Decision

The user manually listened to the MVP audio samples and confirmed:

```text
本次 MVP 音频样本失败。
```

## Failure Reasons

1. Recording quality and recording structure were not suitable for reliable clean splitting.
2. Spoken slate audio and guqin performance were often too close together.
3. Guqin tail decay often touched the next spoken slate.
4. `recording_take_no` and `batch_take_no` naming created confusion risk.
5. Clean segments still contained spoken slate residue.
6. Some slices cut guqin performance or carried incorrect naming.

## Policy

The raw M4A files remain preserved as evidence only. Generated experimental split artifacts from this pilot must not be used as future sample input, production input, ML training baseline, or final Sanman standard sample archive.
