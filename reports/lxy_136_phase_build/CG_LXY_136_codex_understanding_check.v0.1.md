# CG-LXY-136 Codex Understanding Check v0.1

Task ID: `CG-LXY-136-DOC-REGISTRATION-AND-GATE-v0.1`

Status: `REPORT_REGISTRATION_ONLY`

This report records the repo-local understanding baseline for the Cyber Guqin / LXY 1-3-6 phase build design. It is design and validation evidence under `reports/`; it is not runtime output, not Dapu IR authority, not sample ingest, not ML training data, and not render output.

## Source Documents

- `reports/lxy_136_phase_build/CG_LXY_136_Phase_Build_Requirements_v0.1.md`
- `reports/lxy_136_phase_build/CG_LXY_136_Flow_Design_v0.1.svg`
- `reports/lxy_136_phase_build/CG_LXY_136_Flow_Design_v0.1.png`

The PNG is a generated preview derived from the SVG for easier review. The SVG remains the registered source diagram.

## Core Understanding

The LXY 1-3-6 design is a pre-Phase-1 architecture baseline. It does not authorize parser implementation, visual reading execution, score-fact promotion, sample ingest, render, ML training, or any R0/R1/R2/E/F workflow.

The system shape is:

- `1 Skill`: `cyber_guqin_component_guided_transcription`
- `3 Deposits`: D1 Component Reference Layer, D2 Construction Grammar Layer, D3 Regression Guard & Oracle Layer
- `6 Phases`: P1 Grammar Parser MVP, P2 Visual Component Candidate Layer, P3 Parser + Lattice, P4 Line-level Context, P5 Phrase-level Reconstruction, P6 Human Review as Active Learning

The skill is a runtime orchestrator for auditable draft transcription workflow, not a single prompt and not a final answer generator.

## Three Hard Boundaries

1. `禁止答案，不禁止技能。`
2. `禁止旧 reports，不禁止三层沉淀。`
3. Generation can read component references, construction grammar, and generation-safe guards; it must not read phrase-level oracle answers.

## Authority Boundary

All current LXY transcription outputs must remain:

- `GPT_TRANSCRIPTION_DRAFT`
- `REFERENCE_COMPONENT_ATLAS_GUIDED`
- `NOT_REPO_CONTRACT`
- `NEEDS_HUMAN_REVIEW`
- `NOT_DAPU_IR_AUTHORITY`
- `NOT_SAMPLE_INGEST`
- `NOT_ML_TRAINING_DATA`
- `NOT_RENDER_OUTPUT`

The registered reports do not change `01_pieces/`, Dapu Event IR, canon authority, sample assets, recording segments, ML candidate pools, render outputs, or accepted XWC F state.

## Deposit Understanding

### D1 Component Reference Layer

D1 answers local component identity questions:

- possible `component_id`
- `label_zh`
- component family or category
- source image evidence
- visual similarity and confidence

D1 does not answer phrase reading, score-event authority, final score facts, Dapu IR, sample ingest, ML, or render questions.

### D2 Construction Grammar Layer

D2 upgrades construction templates into grammar productions. It answers whether a component sequence or lattice can form a legal jianzipu construction.

D2 is not an answer bank. It must not encode phrase-level expected readings as reusable grammar.

### D3 Regression Guard & Oracle Layer

D3 must be split before Phase 1 execution:

- D3A generation-safe guards may be used by Generation Mode.
- D3B oracle answers may only be used by Evaluation Mode.

Raw goldset must not be read directly by the generation prediction side because it contains phrase-level expected readings.

## Phase Understanding

### P1 Grammar Parser MVP

P1 does not touch images. It starts from known component sequences and checks whether the system can produce legal parse candidates with slots, reasons, confidence, and illegal-parse rejection.

P1 comes first because it isolates construction grammar from visual detection and phrase reconstruction.

### P2 Visual Component Candidate Layer

P2 begins local image handling, but only maps visual crops or glyph subregions to component top-k candidate lattices. It must not hard-pick a final reading.

### P3 Parser + Lattice

P3 connects visual top-k candidates to grammar parsing. It outputs n-best legal readings and rejected candidates with reasons.

### P4 Line-level Context

P4 handles a line image as units, per-unit component lattices, per-unit parse candidates, and coverage ledger. It does not output phrase authority.

### P5 Phrase-level Reconstruction

P5 may combine unit streams into phrase candidates after unit-level behavior is stable. It handles boundaries, inherited context, `就`, `泛起/泛止`, `少息/急`, repeated structures, and state continuation. Phrase output remains draft.

### P6 Human Review as Active Learning

P6 turns human review into structured proposal material. It is not long-term human dictation and not automatic authority writing.

Correct order:

```text
system output
→ human review
→ proposal report
→ user approval
→ references / tests / fixtures update
```

Forbidden shortcut:

```text
Codex sees a correction
→ automatically writes canon / Dapu IR / sample / ML / render authority
```

## Old Reports Boundary

`old reports/lxy_*` are forbidden for Generation Mode. They may only be read under explicit failure-analysis or historical-audit authorization, and even then they remain historical evidence rather than authority.

This prevents a false success pattern where the system appears to read the score but is actually replaying old candidates or human corrections.

## Mode Gate Summary

Generation Mode:

- can read D1, D2, and D3 generation-safe guards;
- cannot read oracle, old reports, old candidates, or phrase-level expected answers;
- outputs draft candidates only.

Evaluation Mode:

- reads frozen prediction plus oracle;
- evaluates exact, equivalent, partial, or fail;
- cannot mutate prediction or use oracle to backfill candidate output.

Learning Mode:

- receives human corrections;
- writes proposal reports only unless a later task explicitly authorizes deposit updates;
- must not automatically write authority.

The full mode gate is registered in `CG_LXY_136_mode_gate.v0.1.md`.

## Current Task Boundary

This task only registers design documents and mode gates under `reports/lxy_136_phase_build/`.

It does not:

- implement Phase 1 parser;
- modify `.agents/`;
- modify `references/`;
- modify `tests/`;
- modify `sources/`;
- modify runtime or production folders;
- run parser, tests, sample ingest, render, ML, R0/R1/R2/E/F, or backend/frontend workflows.
