# Guqin Slate-Based Split Pipeline

This document captures the reusable split pipeline discovered during the failed RS_XWC_001_MVP_PILOT.

## Stable Pipeline

1. Raw master is permanently read-only.
2. Batch range lock maps each batch to explicit `recording_take_no` ranges.
3. Spoken slate numbers are recognized as ASR anchors.
4. Slate recognition must support both `yao` and `yi` for digit 1.
5. Manual override resolves missing, ambiguous, repeated, or wrong ASR anchors.
6. Reviewed anchors become the only trusted split boundary input.
7. Unit preview includes spoken slate plus guqin performance, ending before the next spoken slate.
8. Clean segment is the suffix of a reviewed unit after removing the front spoken slate.
9. Clean segment must receive human listening QC.
10. Sample candidate can only come from a human-accepted clean segment.

## Non-Production Rule

Until human listening QC explicitly accepts a clean segment, every split artifact remains:

- experimental_only: true
- production_grade: false
- not_standard_sample_library: true

## Recording Implication

The pipeline depends on recording discipline. A slate that touches performance, or performance tail that touches the next slate, can make clean splitting impossible even when anchor detection is correct.
