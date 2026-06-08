# Formal Recording Split Reuse Plan

## Inputs

Pilot input:

- Legacy XWC take plan.
- M4A/AAC batch recordings.
- Manual salvage after recording constraints were already fixed in audio.

Formal input:

- Skills or Dapu Event IR generated recording plan.
- WAV raw masters, preferably 48 kHz / 24-bit.
- Complete session manifest.
- Clear slate and performance spacing.

## Shared Pipeline

Both pilot and formal recordings use the same split pipeline:

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

## Formal Differences

- Stricter slate/performance spacing.
- Higher quality source format.
- More complete session manifest.
- Clearer `recording_take_no`, `script_id`, and `gesture_id` traceability.
- More rigorous QC before any sample candidate step.

## Reuse Boundary

Reusable scripts may prepare experimental manifests and framework reports. Production ingest and `03_samples` writes require a separate explicit authorization.
