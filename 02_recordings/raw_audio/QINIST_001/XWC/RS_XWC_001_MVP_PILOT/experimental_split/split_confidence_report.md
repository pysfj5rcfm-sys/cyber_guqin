# Slate-Based Experimental Split Confidence Report

Session: `RS_XWC_001_MVP_PILOT`

## Summary

- Expected takes: 71
- Segment candidates created: 71
- Missing segments: 0
- high: 7
- medium: 58
- low: 0
- forced_review: 6
- Boundary review rows: 64

## Risk Counts

- context takes: 2
- zhu items: 2
- qiaqi items: 3
- RS_XWC_001_060 event_range gap: 1
- retake suspected: 0
- missing gesture_id: 0

## Filename Rule

- All generated segment filenames include gesture_id: true
- UNKNOWN_GESTURE filenames: 0

## Method

- Slate detection method: `energy_sequential_alignment`
- ASR used: false
- Converter status: ffmpeg was used for working WAV conversion with ffmpeg_pcm_s16le_wav. The source files remain M4A/AAC experimental raw material and do not become production sources.

## RS_XWC_001_060 Note

`RS_XWC_001_060` is recognized as a forced-review context take with a missing
`event_range`. The script does not patch legacy source files and does not
auto-write `XWC_P09_N01_to_N02`; that value remains only a human review
possibility if this row is confirmed as 撞到掐起 context.

## Next Step

If coverage is acceptable after audition, proceed to Phase 1B-3E-C Experimental Sample Candidate Set; otherwise run 1B-3E-B boundary repair.
