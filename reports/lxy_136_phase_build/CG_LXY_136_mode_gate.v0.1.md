# CG-LXY-136 Mode Gate v0.1

Task ID: `CG-LXY-136-DOC-REGISTRATION-AND-GATE-v0.1`

Status: `MODE_GATE_DESIGN_BASELINE`

This document defines the repo-local gate for `cyber_guqin_component_guided_transcription` under the LXY 1-3-6 phase build design. It is a design and safety boundary report. It is not parser code, not a skill patch, not Dapu IR authority, not sample ingest, not ML training data, and not render output.

## Purpose

The component-guided transcription workflow must be split into three modes before Phase 1 implementation:

1. Generation Mode
2. Evaluation Mode
3. Learning Mode

The split prevents the generation prediction side from reading phrase-level oracle answers or old reports while still allowing it to use reusable skills, component references, construction grammar, and generation-safe guardrails.

## Mode 1: Generation Mode

Generation Mode creates candidate readings. It must remain answer-blind.

### Allowed Reads

- D1 Component Reference Layer
  - `component_registry`
  - component images
  - alias map
  - component-to-canon seed or crosswalk material when used as reference evidence only
- D2 Construction Grammar Layer
  - construction templates
  - grammar productions
  - legal slot patterns
  - illegal parse patterns that do not reveal phrase-level answers
- D3A Generation-safe Guards
  - `component_match_cases`
  - `construction_template_cases`
  - forbidden scoped guards
  - `must_not_read_as`
  - illegal parse rejection cases
  - component-level known failure guards
  - construction-level known failure guards

### Forbidden Reads

- phrase-level oracle answers
- raw goldset expected readings
- `expected_continuous_reading`
- phrase-level `must_include`
- phrase integration oracle cases
- old `reports/lxy_*`
- old phrase candidate reports
- old human-corrected candidates
- evaluation or triage oracle material

### Allowed Writes

Generation Mode may write only draft candidate artifacts in an explicitly authorized output path for the active task.

### Required Output Labels

Every Generation Mode output must keep these labels:

```text
GPT_TRANSCRIPTION_DRAFT
REFERENCE_COMPONENT_ATLAS_GUIDED
NEEDS_HUMAN_REVIEW
NOT_DAPU_IR_AUTHORITY
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

### Forbidden Writes

Generation Mode must not write:

- Dapu IR authority
- `01_pieces/` production facts
- canon authority
- sample ingest files
- ML training files
- render outputs
- R0/R1/R2/E/F artifacts
- accepted XWC F state

## Mode 2: Evaluation Mode

Evaluation Mode evaluates a frozen prediction. It may read oracle only after the prediction is frozen.

### Required Input

- frozen prediction artifact

The prediction must be treated as immutable during the evaluation run.

### Allowed Reads

- frozen prediction
- D3B Oracle Answers
  - `expected_continuous_reading`
  - phrase-level `must_include`
  - `phrase_integration_cases`
  - source report references when needed for evaluation context
- forbidden fixtures
- scoped equivalence rules

### Forbidden Actions

Evaluation Mode must not:

- modify prediction;
- patch or backfill candidates;
- use oracle to repair candidate output;
- turn evaluation evidence into generation evidence;
- write authority facts;
- write sample, ML, render, R0/R1/R2/E/F, or accepted F artifacts.

### Allowed Output

Evaluation Mode may output only evaluation evidence such as:

- `exact`
- `equivalent`
- `partial`
- `fail`
- diff
- failure category
- guard violation summary
- coverage or unresolved-slot summary

## Mode 3: Learning Mode

Learning Mode receives human review and proposes updates to the three deposits. It is proposal-only until the user explicitly authorizes a follow-up write task.

### Allowed Input

- human review
- low-confidence system output
- disagreement cases
- unresolved slots
- forbidden violations
- unread ink
- boundary disputes
- Evaluation Mode failure categories

### Allowed Proposal Output

Learning Mode may propose:

- new component exemplar
- corrected component exemplar
- new component alias
- corrected component alias
- new construction grammar rule
- corrected construction grammar rule
- new forbidden parse
- new regression case
- new boundary rule

### Approval Gate

No Learning Mode proposal may be promoted before explicit user approval.

Correct sequence:

```text
system output
→ human review
→ proposal report
→ user approval
→ references / tests / fixtures update
```

### Forbidden Actions

Learning Mode must not automatically write:

- Dapu IR authority
- canon authority
- score facts
- qinist realization facts
- sample ingest files
- ML training data
- render output
- R0/R1/R2/E/F artifacts
- accepted XWC F state

## D3 Split Principle

D3 must not be treated as one monolithic file set.

### D3A: Generation-safe Guards

D3A may be read by Generation Mode if it is sanitized and does not reveal phrase-level expected answers.

Allowed D3A content:

- component match cases
- construction template cases
- scoped forbidden outputs
- `must_not_read_as`
- illegal parse rejection
- component-level known failure guards
- construction-level known failure guards

### D3B: Oracle Answers

D3B may be read only by Evaluation Mode after prediction freeze.

D3B content:

- `expected_continuous_reading`
- phrase-level `must_include`
- `phrase_integration_cases`
- `source_report`
- old phrase report references used for evaluation or failure analysis

### Raw Goldset Rule

Raw goldset must not be read directly by the generation prediction side. If a goldset file contains phrase-level expected readings, the generation side needs a sanitized D3A view rather than direct file access.

## Old Reports Rule

Generation Mode must not read `old reports/lxy_*`.

Old reports may be read only when the task explicitly opens one of these modes:

- failure analysis
- historical audit
- regression audit

Even then, old reports remain historical evidence and must not become authority.

## Phase 1 Entry Gate

Do not start Phase 1 Grammar Parser MVP until all of the following are true:

1. The requirements document and flow diagram are repo-local under `reports/lxy_136_phase_build/`.
2. The mode gate is repo-local and accepted as the active boundary.
3. D3A/D3B split is respected in implementation design.
4. Generation Mode has no path to phrase-level oracle answers.
5. Evaluation Mode requires frozen prediction.
6. Learning Mode is proposal-only before explicit approval.

## Forbidden Path Boundary

This mode gate does not authorize writes to:

- `.agents/`
- `references/`
- `tests/`
- `sources/`
- `00_global/`
- `01_pieces/`
- `02_recordings/`
- `03_samples/`
- `04_outputs/`
- `05_scripts/`
- `scripts/`
- `tools/`
- `archive/`
- `reports/archive/`

It also does not authorize writes to:

- `scripts/generate_baiya_recording_plan.py`
- `03_samples/sample_assets.csv`
- `03_samples/recording_segments.csv`
- `recording_items_enriched.jsonl`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`
