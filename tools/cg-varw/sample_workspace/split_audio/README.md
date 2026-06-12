# CG-VARW R1 Synthetic Split Fixture

This is synthetic split demo audio only.
It is not Sanman recording.
It is not Baiya recording.
It is not real guqin audio.
It is not a sample source.
It is not ML training data.
It must not be copied into 03_samples.

Flags:

```text
synthetic_demo=true
review_only=true
production_grade=false
not_real_qinist_recording=true
not_sample_source=true
not_ml_training_data=true
not_render_executed=true
not_sample_assets=true
```

The fixture contains two batches, each with four short mono WAV files:

```text
batch01/T001_clean.wav
batch01/T002_clean.wav
batch01/T003_clean.wav
batch01/T004_clean.wav
batch02/T005_clean.wav
batch02/T006_clean.wav
batch02/T007_clean.wav
batch02/T008_clean.wav
```

Each file is a generated PCM waveform with low-level pre-idle noise, optional weak lead-in content, a pluck-like synthetic sine decay near `render_anchor`, and a natural tail. The files are review-only fixtures for R1 Split 审校 behavior and must not be treated as guqin recordings or sample assets.
