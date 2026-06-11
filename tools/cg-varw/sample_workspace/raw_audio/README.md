# CG-VARW R0B Synthetic Demo Raw Audio

This folder is a local R0B validation fixture only. It contains synthetic demo audio generated from tones, silence, and sine-decay blocks.

It is not a Sanman recording. It is not a Baiya recording. It is not real guqin audio, not a real qinist recording, not a sample source, and not ML training data.

Required flags for every demo artifact in this folder:

```text
synthetic_demo=true
review_only=true
production_grade=false
not_real_qinist_recording=true
not_sample_source=true
not_ml_training_data=true
```

Files:

- `demo_batch01_synthetic.wav`: synthetic batch-style WAV with T001-T010.
- `demo_batch01_synthetic.asr_candidates.json`: synthetic ASR-style marker candidates for T001-T010.

Each T unit contains a short synthetic slate tone/noise block, 0.8 seconds of silence, a synthetic plucked-tone-like sine/decay block, a tail decay, and 1.2 seconds of silence before the next T. T010 ends at a `file_end` boundary.

R0B validation must support WAV metadata and waveform extraction without ffmpeg. ffmpeg is optional for future non-WAV decoding; if ffmpeg or another decoder is unavailable for non-WAV audio, the UI should show a fallback warning instead of treating the file as invalid.
