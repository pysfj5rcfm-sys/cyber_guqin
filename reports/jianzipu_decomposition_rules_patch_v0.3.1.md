# Jianzipu Decomposition Rules Patch Candidates v0.3.1

Task id: `CG-QXBY-FINGERING-LEXICON-AND-VISUAL-ATLAS-DRAFT-v0.1`

Status labels: `QXBY_FINGERING_LEXICON_DRAFT`, `VISUAL_COMPONENT_ATLAS_DRAFT`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.

This task follows jianzipu parser rule baseline v0.3.
This task does not redesign v0.3.
Any conflict is reported as a v0.3.1 patch candidate only.

This file is a report-only patch candidate sheet. It does not modify, supersede, or canonize `jianzipu_decomposition_rules_v0.3_context.md`.

## Source Inputs

- `C:/Users/11028/Downloads/qinxue_beiyao_two_pdfs_package.zip::减字谱组识法.pdf`
  - SHA256: `6f976e3e2f2f647539c7e8a8eac02edcf9bf138164b77c9bcb917d8325b33fd1`
  - Extraction note: image-only PDF, visually inspected.
- `C:/Users/11028/Downloads/codex_qxby_prompt_package_v0.1.zip::jianzipu_decomposition_rules_v0.3_context.md`
  - SHA256: `f35344f25574d98494cf87dd9de1e692704345a151f0b3b9da3621ced10f0869`

## R82 event 粒度来源

score_event 粒度只能由减字谱构字、QXBY/canon evidence、人审确认、上下文承前规则决定。不得由 Codex OCR 分组、旧 CSV、简谱音数、简谱连线、页面物理行、视觉排版猜测反推。

## R83 reading_source 分层

每个 candidate 必须标明：

```text
png_visual_only
qxby_lexicon_matched
visual_atlas_matched
context_inherited
human_reviewed
rejected_ocr_surface
```

不得把 human_reviewed 读法说成 png_visual_only；不得把 OCR candidate、旧 CSV、简谱当作 score facts。

## Parser-Relevant Evidence From 《减字谱组识法》

The visual inspection of printed pages 165-166 supports the existing v0.3 direction rather than replacing it:

- `正字`, `旁字`, and `旁注` are distinguished visually and functionally.
- A score glyph may be organized by upper/middle/lower sections and left/right positions.
- Reading order is a rule-bound decomposition problem, not an OCR surface-string problem.
- Examples include state-boundary and timing terms such as `泛起`, `泛止`, and `少息`.
- The examples reinforce that event granularity must come from glyph construction, lexicon evidence, context inheritance, and human review, not from jianpu or page layout.

## v0.3.1 Patch Candidates

These candidates are not applied. They are proposed only as human-review prompts.

### R84 Candidate: visual-slot evidence source

```yaml
patch_candidate:
  id: "R84"
  title: "visual_slot_evidence_from_zushi"
  source_term: "正字 / 旁字 / 旁注 / 上中下截 / 左右位"
  source_page: "减字谱组识法.pdf printed page 165"
  v0_3_rule_supported: "R82, R83"
  evidence_summary: "The source distinguishes primary score glyphs, side glyphs, side notes, and visual positions. This supports slot-aware candidate extraction before semantic parsing."
  proposed_patch: "Add explicit visual_slot_evidence as a candidate evidence field, with allowed slots upper/middle/lower/left/right/side_note and status NEEDS_HUMAN_REVIEW."
  status: "NEEDS_HUMAN_REVIEW"
```

### R85 Candidate: side-note and non-sounding markers

```yaml
patch_candidate:
  id: "R85"
  title: "side_note_and_non_sounding_marker_policy"
  source_term: "旁注 / 少息 / 省"
  source_page: "减字谱组识法.pdf printed pages 165-166"
  v0_3_rule_supported: "R82, R83"
  evidence_summary: "The source shows side-note and timing/context markers that should not automatically become sounding score events."
  proposed_patch: "Require parser candidates for side-note, pause, and omission/context markers to default to non_sounding_or_context_candidate until human reviewed."
  status: "NEEDS_HUMAN_REVIEW"
```

### R86 Candidate: harmonic-state boundary markers

```yaml
patch_candidate:
  id: "R86"
  title: "fan_state_boundary_markers"
  source_term: "泛起 / 泛止"
  source_page: "减字谱组识法.pdf printed page 166"
  v0_3_rule_supported: "R82, R83"
  evidence_summary: "Reading examples include 泛起 and 泛止 as state-boundary terms. They appear to mark entry/exit of harmonic context rather than independent pitch facts."
  proposed_patch: "Represent 泛起/泛止 candidates as state boundary markers with reading_source qxby_lexicon_matched or visual_atlas_matched, not as independent sounding events unless human review confirms otherwise."
  status: "NEEDS_HUMAN_REVIEW"
```

## Conflict Candidates

No direct conflict with v0.3 was confirmed in this pass. The findings above are patch candidates and evidence-strengthening prompts only.

```yaml
conflict_candidates: []
```

If a future review identifies a conflict, it must use this shape and remain `NEEDS_HUMAN_REVIEW`:

```yaml
conflict_candidate:
  source_term:
  source_page:
  v0_3_rule_conflicted:
  evidence_summary:
  proposed_patch:
  status: NEEDS_HUMAN_REVIEW
```

## Safety Boundary

- No parser rule was rewritten.
- No Dapu IR was created.
- No score import was performed.
- No canon authority was created.
- No jianpu was used for event count, fingering inference, rhythm, or pitch authority.
