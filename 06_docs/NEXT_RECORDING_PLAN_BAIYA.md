# Next Recording Plan: Baiya MVP Reshoot

## Identity

- 录音人: 白牙
- Suggested performer ID: `QINIST_002 = 白牙`
- Do not overwrite `QINIST_001 = 三曼`
- This is a reshoot MVP pilot
- 三曼后续再进行正式采样

## Recording Hard Rules

1. Prefer WAV, 48 kHz / 24-bit.
2. Do not use M4A/AAC as production-like source.
3. Each take follows:
   - spoken slate number
   - at least 0.8 seconds silence
   - guqin performance
   - natural tail decay
   - at least 1.2 seconds silence
   - next spoken slate
4. Do not start the next spoken slate before guqin tail decay has ended.
5. If recording by batch, every take inside the batch still keeps the same spacing.
6. If acceptable to the user, record one WAV file per take.
7. If recording by batch, keep clear slate numbers.
8. Do not delete retakes; label `retake02`, `retake03`, etc.
9. Do not delete bad takes; include them in the manifest.
10. Every take must trace `recording_take_no`, `script_id`, and `gesture_id`.

## Next Artifact

The next stage should generate a new Baiya-focused `recording_batch.md` through Cyber Guqin skills, not by repairing old RS_XWC_001 clean segments.
