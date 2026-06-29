---
name: cyber_guqin_component_guided_transcription
description: Use when converting user-provided guqin jianzipu phrase crop images and optional user-labeled component samples into report-only phrase-level transcription candidates for human review. This skill performs component-guided visual reading, not canon authority, not Dapu IR authority, not sample ingest, not ML training, and not render.
---

# Cyber Guqin Component-Guided Transcription

Revision note: v0.4 adds `就=承前` handling and separates repeated `大指注下七徽` templates by their actual right-hand action, such as `抹七弦` versus `挑七弦`.

## 1. Purpose

Use this skill to convert user-provided guqin jianzipu phrase crop images into phrase-level transcription candidates for human review.

This skill is image-to-reading-candidate only. It produces:

- continuous phrase candidate readings,
- glyph_group candidate tables,
- component-guided visual-slot evidence,
- report-only score_event_candidate drafts,
- human review sheets.

It does not create canon authority, repo contract, Dapu IR authority, sample ingest, ML training data, recording plan, render output, or R0/R1/R2/E/F output.

## 2. When To Use

Use this skill when:

- the user provides a jianzipu phrase crop image,
- the user provides optional named component samples,
- the task asks for component-guided transcription or phrase-level candidate reading,
- the candidate reading must remain `NEEDS_HUMAN_REVIEW`,
- downstream parser work is not yet authorized.

Default status labels for general use:

```text
TRANSCRIPTION_DRAFT
USER_COMPONENT_LABEL_GUIDED
NOT_CANON_AUTHORITY
NOT_REPO_CONTRACT
NOT_DAPU_IR_AUTHORITY
NEEDS_HUMAN_REVIEW
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

When a repo-local QXBY component atlas registry is used, add or prefer this label in LXY outputs:

```text
REFERENCE_COMPONENT_ATLAS_GUIDED
```

The registry label does not remove `NEEDS_HUMAN_REVIEW` and does not create score-event authority.

For LXY reports, use:

```text
LXY_TRANSCRIPTION_DRAFT
USER_COMPONENT_LABEL_GUIDED
NOT_CANON_AUTHORITY
NOT_REPO_CONTRACT
NOT_DAPU_IR_AUTHORITY
NEEDS_HUMAN_REVIEW
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

## 3. When Not To Use

Do not use this skill to:

- create canon authority,
- import score facts into repo runtime data,
- create Dapu Event IR authority,
- write sample ingest files,
- create ML training data,
- generate audio or render outputs,
- generate recording plans,
- run R0/R1/R2/E/F workflows,
- infer score facts from jianpu, OCR surface text, old CSV rows, page layout, or spacing.

If the user asks for final structured Dapu IR after review, hand off to `guqin-dapu-parser`. If the user asks whether a term or component meaning is valid, hand off to `guqin-canon-builder`.

## 4. Skill Architecture Context

This skill sits between the image crop and later parser work:

```text
component-guided transcription skill
→ produces phrase-level reading candidates

guqin-canon-builder
→ resolves rule / terminology / component uncertainty

guqin-dapu-parser
→ structures reviewed readings into Dapu Event IR candidates

cyber_guqin_mvp_workflow
→ controls whether the project may proceed beyond transcription draft
```

The four workflow roles are:

- `cyber_guqin_mvp_workflow`: global workflow orchestrator and phase gate controller. This skill must obey its score, canon, parser, recording, sample-ingest, render, and second-piece gates.
- `cyber_guqin_component_guided_transcription`: this skill. It handles phrase crop images, user-labeled component samples, glyph_group segmentation, component matching, visual slot decomposition, draft lookup, context inheritance, and continuous phrase candidate readings.
- `guqin-canon-builder`: canon / terminology / component / source-evidence layer. This skill may consult canon-builder-style evidence but must not promote draft component matches into canon authority.
- `guqin-dapu-parser`: reviewed-reading-to-structured-score layer. It is used only after the user confirms or corrects the candidate reading.

If `guqin-canon-builder` or `guqin-dapu-parser` are named by project workflow but not physically present in a checkout, do not invent their files. Treat them as architectural roles and preserve the handoff contracts below.

## 5. Handoff Contract

Input from user:

```text
phrase crop image(s)
optional component sample zip
optional human corrections
optional phrase boundary note
optional source page / line note
```

Output to user:

```text
第N句候选读法
glyph_group candidate table
human review sheet
unresolved / low-confidence list
explicit questions for user review
```

Escalate to `guqin-canon-builder` when:

```text
unknown component appears
term meaning is uncertain
alias normalization is required
QXBY evidence conflicts
gesture-family classification is unclear
state marker / timing marker semantics are uncertain
right-hand or left-hand term cannot be safely classified
```

Escalate to `guqin-dapu-parser` only after:

```text
user confirms or corrects candidate reading
phrase-level reading is stable enough to structure
all unresolved glyph_group boundaries are explicitly marked
score facts remain separate from qinist realization
non-sounding markers are identified
state boundaries are scoped or marked needs_review
```

The parser handoff boundary is mandatory for registry-guided work: a `reference_component_atlas` match may support a draft reading, but only explicit human confirmation or correction can authorize later parser structuring. Even then, this skill must not write Dapu IR itself.

Never bypass:

```text
NEEDS_HUMAN_REVIEW
NOT_CANON_AUTHORITY
NOT_DAPU_IR_AUTHORITY
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

## 6. Required Inputs

At minimum:

- one or more local phrase crop images,
- piece and phrase scope, when known.

Optional:

- user-labeled component sample zip,
- manifest of component labels,
- human corrections from earlier phrases,
- phrase boundary notes,
- source page or line notes.

Represent user-labeled components as:

```yaml
component_id:
filename:
category:
label_zh:
authority_status: USER_PROVIDED_LABEL
```

If a later component manifest uses `USER_CONFIRMED_LABEL`, keep it as user-provided guidance and still set `not_canon_authority=true`, `not_dapu_ir_authority=true`, and `needs_human_review=true` in outputs.

## 7. Required Repo Reports To Read

Before transcription, read the current project boundary files requested by the task, normally:

```text
README.md
06_docs/PROJECT_STRUCTURE.md
reports/REPORTS_INDEX.md
.agents/skills/cyber_guqin_mvp_workflow/SKILL.md
```

For QXBY / v0.3.1 lookup evidence, read only task-approved reports, commonly:

```text
reports/qxby_fingering_chapter_lexicon_draft.v0.1.yaml
reports/qxby_fingering_chapter_visual_atlas_draft.v0.1.json
reports/qxby_fingering_chapter_extraction_review.v0.1.md
reports/qxby_fingering_chapter_high_risk_terms_review_sheet.v0.1.csv
reports/jianzipu_decomposition_rules_patch_v0.3.1.md
```

When a task provides prior phrase reports as seed evidence, read them as transcription drafts only. They are not canon authority and not Dapu IR authority.

## 7a. Reference Component Atlas

For LXY P5 and later component-guided transcription tasks, first read the repo-local reference registry when it exists:

```text
references/qxby_component_atlas/component_registry.v0.1.json
```

Read order:

```text
reference component atlas registry
→ task-approved QXBY / v0.3.1 reports
→ prior LXY phrase reports as transcription-draft template evidence
→ current phrase crop
```

`COMP-001..030` in the registry are reference-level component knowledge after user review. This means the component label, category, visual slot semantics, and construction-template hints may be reused as `QXBY_COMPONENT_ATLAS_REFERENCE`.

This does not mean a new phrase reading is final score authority. A reference component match is not a score event, not Dapu IR authority, not sample ingest, not ML training data, not render output, and not a recording plan.

Required boundary flags for registry-guided phrase outputs:

```text
LXY_TRANSCRIPTION_DRAFT
REFERENCE_COMPONENT_ATLAS_GUIDED
NOT_REPO_CONTRACT
NOT_DAPU_IR_AUTHORITY
NEEDS_HUMAN_REVIEW
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

Preserve the v0.4 correction exactly:

```text
COMP-028 = 撞 / 左手取音
COMP-029 = 轮 / 右手指法
COMP-030 = 急 / 节奏谱字
```

Do not fall back to obsolete raw mappings such as `raw_001=轮` or `raw_003=撞`.

Reusable construction templates from the registry may outrank a generic `unknown_from_crop` fallback, but every reused template remains report-only and `NEEDS_HUMAN_REVIEW`. Template reuse must record the template id or source phrase report and must not be promoted into final phrase score facts.

If a phrase crop is missing or ambiguous, write a missing-input report instead of inventing a candidate reading.

## 8. Core Workflow

Use this workflow:

```text
component_samples
→ phrase_crop
→ glyph_group segmentation
→ component matching
→ visual slot decomposition
→ QXBY / v0.3.1 lookup
→ context inheritance
→ score_event_candidate draft
→ continuous phrase candidate reading
→ human review sheet
```

Candidate reading is not score fact authority. Candidate reading is not Dapu IR. Human correction improves the draft but still does not automatically create canon authority.

## 9. Component Matching Rules

Keep these evidence types separate:

- user-labeled component sample,
- QXBY draft term,
- visual atlas draft match,
- context-inherited value,
- human correction,
- canon authority,
- Dapu IR authority.

User-labeled components may guide visual matching but must not become canon authority automatically.

For every matched component, record:

- component id,
- label,
- category,
- visual slot,
- match confidence,
- evidence note,
- authority status.

When a visual match is partial, write `match_confidence=low` or `medium_low` and add a review reason.

## 9a. Reusable Human-Confirmed Construction Templates

When the user has corrected a construction in an earlier phrase, treat that construction as a reusable visual template for later phrase crops. Template reuse is still report-only and `NEEDS_HUMAN_REVIEW`, but it should outrank a generic `unknown_from_crop` fallback when the same slot structure recurs.

Reusable LXY templates currently include:

- `名指七徽挑六` / `名指七九徽挑六`: upper-left `名指`, right-upper hui number(s), lower/right-hand `COMP-018 挑`, embedded or lower `六` as string.
- `散音，挑五弦`: `COMP-027 散音起始` plus `COMP-018 挑` and `COMP-004 五` as embedded/right-hand string number. Treat `散音` as the sound state and `挑五弦` as the sounding action; `句号` remains punctuation.
- `大指六二徽，轮七弦`: upper-left `大指`, right-upper `六二` as hui, `COMP-029 轮` as right-hand compound action, embedded `七` as string.
- `大指注下七徽，抹七弦` and `大指注下七徽，挑七弦`: both share the same left-hand / hui / `注下` preparation pattern, but the right-hand action must be read from the visible right-hand component. Do not copy `抹` from a neighboring template when the visible action is `COMP-018 挑`.
- `急进复`: adjacent timing/position-transition construction using `COMP-030 急` plus `进复`; allow the phrase crop segmentation to merge neighboring visual pieces when the combined construction is more plausible than two independent events.
- `名指七六徽，掐起`: `名指` holds the target position, `掐起` supplies the sounding special technique; if the hui is supplied by user/theory review, record it as human/theory-assisted evidence.

Do not promote a reusable template into canon authority or Dapu IR authority. Record the source as `human_correction` or `template_reuse_from_prior_phrase`, keep every candidate reviewable, and still report ambiguous boundaries.

When the template source is `references/qxby_component_atlas/component_registry.v0.1.json`, record it as `reference_component_atlas_template_reuse` and keep `score_event_authority=false` and `dapu_ir_authority=false`.

## 10. Slot-Aware Number Semantics

数字在右上槽位优先读作徽位；数字在中下槽位、或嵌入右手指法内部时优先读作弦数；不得仅凭数字形状决定语义，必须结合槽位和构字关系。

Examples:

- 右上“七” -> 七徽 candidate
- 右手动作内部“一 / 二 / 三 / 四 / 五 / 六 / 七” -> 弦数 candidate
- “六二”在右上徽位槽 -> 六二徽 candidate

For left-hand position-transition glyphs, nearby numbers may be hui targets even when they appear under or beside the motion component. Examples include `进五六复` and `上六二`. Treat these as left-hand position/hui candidates rather than string numbers unless right-hand action embedding is visually stronger.

## 11. Context Inheritance Rules

无新左手指法 / 徽位 / 音型状态时，候选读法可承前；承前必须回溯到最近明确的左手指法、徽位、音型状态或 state boundary；承前必须显式标记 context_inherited=true；承前不得静默变成 score fact authority。

Examples:

```text
left_hand_candidate: 名指 (context_inherited)
hui_position_candidate: 七徽 (context_inherited)
sound_type_candidate: 泛音 (context_inherited from 泛起 context)
```

`就` is a context-inheritance candidate when a user-labeled component or strong visual evidence supports it. It is not an independent sounding unit by default.

In continuous phrase reading, `就` should normally be rendered as `承前` behavior rather than spoken as a separate sounding or left-hand action. Keep it in the glyph table and review sheet as a non-sounding context marker, but omit it from the readable phrase line unless the user explicitly asks to surface the marker.

At a phrase opening, context inheritance may cross the phrase boundary. If the first glyph_group has no new left-hand finger, hui position, or sound-state marker, look back to the nearest explicit state in the previous reviewed/candidate phrase. Record the inherited source phrase and glyph_group when known, and keep `context_inherited=true`. Do not silently inherit string number, rhythm, or event count unless the visible construction or user review explicitly supports it.

## 12. State Boundary / Non-Sounding Markers

Use these defaults:

```text
泛起 = enter harmonic state boundary candidate
泛止 = exit harmonic state boundary candidate
泛起 / 泛止 默认非独立发声音
其作用域必须进入 needs_review，直到用户确认
```

```text
少息、句号、旁注、状态边界默认不生成 sounding_unit；
只能作为 timing_marker / punctuation / state_boundary candidate；
不得自动变成发声音。
```

`散音起始` is an open-string state marker candidate when user-provided component evidence supports it. It should not automatically generate a sounding_unit without a visible right-hand action or human confirmation.

Do not confuse `COMP-027 散音起始` with separate left-hand or hui components. The `散音起始` grass-head-like component has a connected middle in the user-provided sample. If the top area instead separates into a left-hand finger plus right-upper number, read it as left-hand / hui evidence, not as `散音起始`.

## 13. Right-Hand Action Rules

Use these draft rules:

```text
勾：右手动作，可含内嵌弦数。
托：右手动作，可含内嵌弦数。
挑：右手动作，COMP-018 的乙形下承结构必须识别为挑，不得漏读为裸弦数。
历：连挑；读作 sequential cross-string action candidate。若用户确认“历五四”，按五弦到四弦生成两个 sounding_unit candidates。
```

Do not infer `历` string span from jianpu or spacing. Use visible embedded string numbers or user correction.

For compound right-hand actions such as `背锁`, keep sequence and sounding-unit expansion as draft candidate logic. If the exact sequence or host context is uncertain, mark it `NEEDS_HUMAN_REVIEW` and escalate to canon-builder-style evidence before parser promotion.

For v0.4 component samples:

- `COMP-028 撞` is a left-hand position-transition / virtual-attack candidate, not the obsolete raw_001=轮 mapping.
- `COMP-029 轮` is a right-hand compound action candidate. QXBY/v0.3.1 draft evidence models it as `摘-剔-挑`, but expansion and string targets remain `NEEDS_HUMAN_REVIEW`.
- `COMP-030 急` is a timing/urgency marker candidate and non-sounding by default unless human review says otherwise.

## 14. Left-Hand / Hui / Sound-Type Rules

Use these draft rules:

```text
处于泛起—泛止之间的明确发声动作候选，默认 primary_sound_type_candidate=泛音，除非另有更强证据。
泛止之后出现大指 + 徽位 + 右手动作，默认 primary_sound_type_candidate=按音候选。
吟默认是 ornament / left-hand motion candidate，通常附着于承前按音位置，不独立生成发声音，除非用户确认。
爪起是 special_technique candidate，需人工确认是否带发声、是否附着承前位置。
```

For left-hand position-taking motions such as `进复`, `上`, `下`, `注`, and `退复`:

- read nearby numbers as hui-position or position-transition candidates when the construction supports it,
- examples include `进五六复` and `上六二`,
- assume the motion generally continues toward or through the next note position,
- do not generate an independent sounding_unit by default unless there is visible attack evidence or user confirmation,
- mark the host event / attachment scope as `NEEDS_HUMAN_REVIEW`.

`注下` is a left-hand attack-preparation / downward approach candidate. It means the attack has a lead-in or advance motion before arriving at the target hui; do not read it as the finger directly pressing the hui with no preparation. A reading such as `大指注下七徽，抹七弦` should keep `注下` attached to the host pluck and mark the advance/attachment scope for review.

`吟` is usually an ornament / left-hand motion candidate attached to the preceding or host position. A standalone-looking `吟` glyph should not be confused with `上 + number` just because the strokes are compact.

`掐起` / `搯起` / `爪起` are special-technique candidates. They require human review for whether they create sounding units and how they attach to inherited left-hand position. In common candidate readings, `掐起` may be produced after 名指 or 跪指 holds the prior/target position and 大指 follows through to pluck or raise the sound. If the user provides 三分损益法 or other theory-assisted reasoning for a hui target, record it as `human_correction` / `theory_assisted_review_evidence`, not as crop-only evidence or canon authority.

Project boundary:

```text
primary_sound_type must remain one of 散 / 按 / 泛 when promoted to structured score facts later.
At this transcription stage, unknown_from_crop is allowed as a draft candidate value.
```

## 15. Phrase-Level Candidate Reading Format

Always give a readable phrase candidate first:

```text
第N句候选：……
```

Then provide structured tables for glyph_group, component matches, candidate readings, score_event_candidate drafts, and review questions.

Prefer guqin reading language in the phrase candidate, but mark uncertain terms with `？` or a review note instead of silently normalizing them.

## 16. Human Review Loop

Every candidate must remain `NEEDS_HUMAN_REVIEW`.

When the user corrects a reading:

- record the correction in the next draft report,
- update the relevant skill rule only if it generalizes safely,
- keep the correction as human review evidence, not canon authority,
- do not automatically structure it into Dapu IR.

Ask explicit review questions for:

- uncertain boundaries,
- unknown components,
- inherited left-hand / hui / sound-state scope,
- special technique sounding policy,
- compound right-hand sequence expansion,
- state boundary scope.

## 17. Safety Boundaries

Forbidden in this skill:

- jianpu as score authority,
- OCR surface text as score facts,
- old CSV rows as score facts,
- page layout as event count,
- final readings inferred from spacing,
- Dapu IR import,
- canon authority creation,
- sample ingest,
- ML training data,
- render output,
- recording plan or R0/R1/R2/E/F output.

Jianpu may be used only as a rough phrase locator if visible. It must not determine event count, rhythm, pitch, string number, hui position, right-hand action, left-hand action, sound type, or score_event granularity.

## 18. Allowed Outputs

Allowed report-only outputs are:

- JSON transcription candidate report,
- Markdown transcription candidate report,
- CSV human review sheet,
- optional segmentation review Markdown,
- missing-input report when phrase crop is absent or ambiguous.

Do not write source images or temporary crops into the repo. Temporary crops, if made, must stay outside the repo and be deleted before final status when practical.

## 19. Validation Checklist

Before final response:

- verify the skill/report files are under allowed paths,
- validate JSON with `python -m json.tool` or the available bundled Python,
- run `git diff --check`,
- run `git diff --name-status`,
- run `git status --short --untracked-files=all`,
- if CSV is produced, check headers and row count,
- report any missing inputs or skipped validation honestly.

## 20. Common Failure Modes

Watch for:

- treating user component labels as canon,
- treating QXBY draft reports as canon,
- treating the reference component atlas as final phrase score authority,
- treating a reference component match as Dapu IR authority,
- treating a score_event_candidate as Dapu IR,
- reading right-upper numbers as strings without slot evidence,
- reading embedded right-hand numbers as hui positions,
- missing `COMP-018 挑` and calling the embedded number a bare string,
- turning `少息`, `句号`, `就`, `泛起`, `泛止`, or `散音起始` into sounding units,
- forgetting context inheritance flags,
- expanding `历`, `背锁`, or special techniques without visible evidence or human confirmation,
- missing hui targets on `进复`, `上`, `下`, `注`, or related left-hand position-transition glyphs,
- stopping context inheritance at the current phrase when the phrase opening requires looking back to the previous phrase,
- confusing connected `COMP-027 散音起始` with separate 大指 + hui-number construction,
- flattening `注下` into direct pressing with no attack lead-in,
- using theory-assisted hui calculation without marking it as human review evidence,
- using page layout, old OCR, old CSV, or jianpu to decide score facts.

## 21. Seed Examples From LXY Phrase 1 / Phrase 2

These are seed examples only:

```text
seed examples
LXY_TRANSCRIPTION_DRAFT
NEEDS_HUMAN_REVIEW
NOT_CANON_AUTHORITY
NOT_DAPU_IR_AUTHORITY
```

第一句候选：泛起：中指七徽勾一，名指七徽勾二，承前勾三，泛止；大指按六二徽，托七弦。

第二句候选：承前大指六二徽吟，爪起；名指泛七徽挑六，少息，承前历五四，承前勾三，承前挑四，承前勾三，泛止；大指按六二徽，托七弦。

Rules learned from these seed examples:

- slot-aware numbers are required,
- `挑` must be recognized from the `COMP-018` lower support shape,
- `历五四` is a sequential cross-string action when confirmed,
- `泛起` / `泛止` are state boundaries,
- no-new-left-hand groups may inherit prior left hand and hui context,
- phrase-line continuation must come from user/source note, not layout guesswork.
