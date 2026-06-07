# RS_XWC_001_MVP_PILOT QC Note

QC classification: MVP experimental only

Production grade: false

Accepted for: MVP pipeline experiment

Rejected for: standard Sanman sample library

## Known Issues

- Source files are M4A/AAC, not WAV.
- Lossy compression may affect guqin tail, harmonic detail, slide detail, and transient fidelity.
- Prior manual review indicated possible hot level / near full-scale peaks in some batches.
- Prior manual review indicated possible stereo imbalance.
- Therefore this batch should not be used as final production sample source.

## Experimental Value

- This batch is not rejected as an experiment.
- This batch is useful for pipeline validation.
- This batch is useful for rough segmentation test.
- This batch is useful for first real-audio render feasibility test.
- Standard sampling should be repeated after MVP success.

## Scope

Asset class: `mvp_experimental_raw`

Not for:

- final production sample library
- long-term Sanman standard sample archive
- ML training baseline
