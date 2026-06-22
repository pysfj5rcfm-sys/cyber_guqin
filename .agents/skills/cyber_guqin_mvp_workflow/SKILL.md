---
name: cyber_guqin_mvp_workflow
description: Use when running or auditing the Cyber Guqin MVP workflow from new dapu score intake through recording plan, R0/R1/R2 review, ABCD/E/F audition render, human acceptance, and future data-candidate gates.
---

# Cyber Guqin MVP Workflow

## Purpose

Use this skill to orchestrate the Cyber Guqin Dapu audition MVP workflow. The goal is to move from a new guqin score or dapu notation source to a human-auditionable `F_FINAL_REVIEWED` render, while preserving enough provenance to later evaluate future digital qinist data candidates.

This is not production sample ingest, not ML training, and not Arrangement Mode production. A passed F render proves an audition loop can be heard and accepted; it does not prove sample assets are ready, model training is allowed, or a modern-song-to-jianzipu arrangement system is production-ready.

The skill coordinates phase boundaries, authority checks, script safety, human review gates, and stop rules. It should not replace engineered safeguards: if a failure can be prevented by schema validation, parameterization, dry-run defaults, or manifest checks, engineer that guard instead of relying on this skill to remember it.

## When To Use

Use this skill when:

- A new guqin score enters Dapu Mode.
- A task spans score intake, canon/parser gates, recording coverage, recording plan generation, R0/R1/R2 review, ABCD/E/F audition renders, or human listening acceptance.
- You need to judge whether an XWC/Baiya lesson can be reused for another piece.
- You need to audit whether a script is reusable now, dry-run only, reusable after parameterization, high-risk, or historical-only.
- You need to decide whether an artifact can enter a future ML-ready candidate pool.
- You need to keep Track A execution, Track B data-candidate accumulation, and Track C Arrangement Mode future design separate.

## When Not To Use

Do not use this workflow skill as the primary tool when:

- The task only extracts canon rules, fingering explanations, aliases, components, gesture families, or source evidence. Use `guqin-canon-builder`.
- The task only parses concrete jianzipu/OCR/manual score tokens into Dapu Event IR. Use `guqin-dapu-parser`.
- The user gives a narrow, already-defined engineering patch task. Follow that task's prompt, tests, and allowed paths.
- The work would enter production sample ingest, ML training, or Arrangement Mode production. Open a separate gate with explicit authority, allowed writes, validation, and human approval.
- The work is cleanup, archive/delete, REVIEW/DELETE_CANDIDATE processing, or second-piece execution without explicit authorization.

## Upstream Skills

### `guqin-canon-builder`

Use `guqin-canon-builder` for the rule layer / canon layer.

Call it when handling terminology, fingering explanations, aliases, component lexicons, gesture families, source evidence, unknown notation, uncertain fingering semantics, missing canon evidence, or parser/canon conflicts.

It answers rule-book questions such as "what does this term mean", "which component or gesture family does this action belong to", and "how should this alias normalize". It must not parse concrete score events, generate recording items, choose a qinist realization, modify V1 runtime data, or generate audio.

### `guqin-dapu-parser`

Use `guqin-dapu-parser` for the parsing layer / score-to-IR layer.

Call it for new score intake, OCR or manual notation structuring, concrete jianzipu token parsing, Dapu Event IR, semantic recording item candidates, score facts vs qinist realization separation, and recording coverage preparation.

It must not extract rule-book canon, decide Sanman/Baiya final performance style, create `recording_items_enriched.jsonl`, modify current recording tasks, execute sample selection, or generate audio.

## Track A: Dapu Mode

Track A is the active MVP path: new dapu score to auditionable F.

1. **Score intake**: Identify the score authority, source evidence, piece/session/qinist scope, OCR/manual input status, and unknown notation. Do not treat recording plans or legacy recording scripts as score authority.
2. **Canon gate**: Route unknown terms, uncertain fingerings, aliases, components, and gesture-family questions to `guqin-canon-builder`. Preserve `needs_review` until human confirmation.
3. **Parser gate**: Route concrete notation tokens through `guqin-dapu-parser`. Produce or audit Dapu Event IR with score facts separate from qinist realization.
4. **Dapu Event IR**: Preserve event source, confidence, validation notes, score-event identity, gesture components, and interpretation boundaries.
5. **Recording coverage / 补录清单**: Diff required events/techniques/context against available reviewed takes. Report missing take coverage, wrong-take risk, context-only candidates, and retake needs.
6. **Recording plan**: Draft take plan, batch ranges, slate rules, context-take policy, tail-silence guidance, and review expectations. Require human approval before recording or downstream processing.
7. **R0 raw review**: Use raw-file identity compatible with active draft/export IDs. Human review accepts slate anchors and raw markers. Do not alter raw audio.
8. **R1 split review**: Review split segments, render anchors, QC, accepted/rejected state, and tail policy. Treat `full_tail` / natural decay as the guqin default unless an explicit human override exists.
9. **R2 render review**: Review phrase/version choices. Confirm latest JSON is canonical before using or exporting R2 state.
10. **ABCD experimental render**: Generate or audit A/B/C/D only with explicit render authorization. Treat outputs as experimental evidence, not production-grade samples.
11. **E_REVIEWED**: Generate or audit E only from canonical R2 latest JSON plus human/GPT co-review. Keep E as reviewed audition evidence, not a sample ingest artifact.
12. **F_FINAL_REVIEWED**: Generate or audit F only from canonical latest JSON or an F input snapshot with hash/provenance. Preserve final-ready/playable/alignment metadata.
13. **Human listening acceptance**: Record pass, conditional pass, residual note, or narrow reopen from explicit user listening feedback. A minor residual note must not automatically trigger G/F2.
14. **Closeout**: Write reports, validation evidence, authority summary, lessons, and script status. Do not clean, archive, delete, or re-run renders unless separately authorized.
15. **Next-piece preparation**: Reuse gates and engineered tools only. Do not run XWC/Baiya hardcoded scripts as default second-piece entry points.

## Track B: Qinist Digitalization

Track B accumulates future ML-ready candidates from each Track A piece. It is not current ML training.

Candidate evidence may include:

- `score_event` alignment and stable event identity.
- `source_take` provenance, recording session, batch/take identity, and replacement provenance.
- R1 labels such as accepted/rejected, render anchor, QC status, tail policy, and context-only status.
- R2 labels such as preferred version, phrase comments, issue type, severity, suggested revision, and human/GPT co-review.
- F-level and phrase-level human preference labels after listening acceptance.
- Realization fields such as qinist timing, light `绰`, `吟猱`, context connection, and tempo preference, kept separate from score facts.

Exclude from candidates:

- Wrong takes and known failed takes.
- Retakes marked bad or unreviewed.
- Context-only takes treated as atomic samples.
- Render-only transition helpers without independent sample authority.
- Any take where score facts and qinist realization are mixed.

Do not start ML training because sample ingest schema, `sample_assets.csv`, `recording_segments.csv`, `recording_items_enriched.jsonl`, cross-piece candidate volume, negative labels, and quality gates are not yet frozen. Sample ingest requires its own gate with schema freeze, source authority freeze, segment-to-score proof, complete human labels, wrong/failed/context-only exclusion checks, and cross-piece validation.

## Track C: Arrangement Mode Future

Track C is future design only. Do not promise production-grade Arrangement Mode from current Track A success.

Future inputs may include 简谱, 五线谱, MIDI, and MusicXML. A future workflow must parse pitch/rhythm/phrase, analyze playable range and phrasing, map melody to guqin feasibility, choose string order / hui position / open-pressed-harmonic options, search left- and right-hand fingering, produce guqinized arrangement candidates, generate jianzipu proposals, and require human review.

Current missing pieces include Arrangement Planner, Fingering Search, Guqinization Review, bidirectional canon/parser validation, and a human audit loop. Keep this as a future track until explicitly authorized and engineered.

## Phase Gates

| Gate | Required rule |
| --- | --- |
| score gate | Confirm score authority, source evidence, score facts, scope, and `needs_review`; do not use recording plans as score authority. |
| canon gate | Send unknown notation, aliases, fingering semantics, component mapping, and missing evidence to `guqin-canon-builder`. |
| parser gate | Send concrete tokens/OCR/manual notation to `guqin-dapu-parser`; keep score facts and qinist realization separate. |
| recording plan gate | Require human approval for take plan, batch ranges, context takes, tail rules, retake/bad-take policy, and coverage claims. |
| R0 gate | Confirm raw root/scope/file_id compatibility and human-accepted slate/marker state before split planning. |
| R1 gate | Confirm human-accepted segment/QC/tail review, render anchors, and context-only exclusions before render planning. |
| R2 gate | Confirm `r2_review_state.latest.json` authority, key coverage, derived export guard, and no Downloads/restore/blob authority. |
| E gate | Generate/audit E only from canonical latest JSON plus reviewed revision intent; keep E experimental. |
| F gate | Generate/audit F only from latest JSON or input snapshot hash; require explicit listening acceptance before closeout. |
| sample ingest gate | F pass is insufficient; require schema, labels, exclusion checks, source authority, and human candidate review. |
| second-piece gate | Prepare Track A only; do not run XWC/Baiya hardcoded scripts or enter ML/Arrangement/sample ingest. |

## Authority Gates

Treat these as canonical when in scope:

- Score/canon authority: source score, verified canon evidence, ontology/schema authority, and human-confirmed notation decisions.
- R0 active draft JSON: current raw-marker workbench state, e.g. active `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json`.
- R1 active draft JSON: current split-review workbench state, e.g. active `tools/cg-varw/review_outputs/r1/drafts/{batch_id}.split_review.json`.
- R2 latest JSON canonical: `r2_review_drafts/latest/r2_review_state.latest.json`.
- F input snapshot: `F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json` and its hash/provenance.

Treat these as derived or audit evidence, not current authority:

- R0/R1 CSV exports.
- R2 CSV/YAML exports.
- Reports and validation summaries.
- Archive copies and historical execution evidence.

Never treat these as current authority unless the user explicitly opens a restore/migration task with source path, hash, reason, and warnings:

- Downloads.
- Browser Blob downloads.
- Restore zip.
- Old exports.
- Archived old exports.
- Raw master audio binary contents or split/F WAV contents when the current task forbids audio reads.

## Script Registry

Maintain script status before execution. Do not run scripts blindly. Registry fields must include: script path, phase, status, default mode, input authority, outputs, hardcoded hazards, whether it reads/writes audio, whether it modifies review data, whether it generates render, preflight command, and human approval requirement.

| Script path | Phase | Status | Default mode | Input authority | Outputs | Hardcoded hazards | Reads/writes audio | Modifies review data | Generates render | Preflight command | Human approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `scripts/generate_baiya_recording_plan.py` | recording plan | `reusable_after_parameterization` | no-run template; current untracked | XWC/Baiya legacy bridge and recording plan inputs | reports/docs drafts only with `--execute` | XWC, Baiya, `RS_XWC_002_BAIYA_PILOT`, T001-T071, T060/T071 | no | no | no | none approved for current workflow | Required before any run; do not directly run/commit/delete/archive current untracked file. |
| `scripts/render_xwc_abcd_from_planning.py` | ABCD render | `reusable_after_parameterization` | high-risk render writer; only `--preflight-only` is non-render | XWC/Baiya `_planning` and readiness manifest | ABCD WAV/alignment/manifest/validation/listening guide | XWC/Baiya session, render names, P09/T060/T071 policy | reads and writes audio | no R0/R1/R2 state by default | yes | `python scripts/render_xwc_abcd_from_planning.py --preflight-only` | Required; never run for a second piece directly. |
| `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py` | F render | `reusable_after_parameterization`; current XWC historical | no-run current historical generator | R2 latest JSON, E artifacts, source previews | F WAV/alignment/report/validation/input snapshot/latest exports | XWC, Baiya, E/F names, P01/P02 classes, T008/T014, render set | reads and writes audio | yes, writes latest/review entries | yes | none approved for generic use | Required; never run for a second piece directly. |
| `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py` | full-tail repair / F regeneration | `historical_only` | forbidden as workflow entry | historical XWC/Baiya R1/F/latest state | rewrites R1/F/latest/derived outputs | XWC/Baiya/F paths and render set | reads and writes audio | yes | yes | none | Do not use as default; only separate explicit repair task could inspect it. |
| `tools/cg-varw/backend/scripts/verify_r2_canonical_draft.py` | R2 validation | `reusable_after_parameterization` | read-only verification after root parameterization | R2 latest JSON and derived exports | validation report/stdout | default render root may be XWC/Baiya | no audio writes | no | no | script-specific help or explicit root once parameterized | Approval required if paths are not confirmed read-only. |
| `scripts/slate_number_recognizer.py` | slate planning / R0 support | `reusable_now` | explicit dry-run/input-output workflow | explicit session/raw/take plan/output | slate candidate reports | caller-supplied scope required | may read raw metadata/audio as task allows | no | no | require explicit session/raw/take plan/output arguments | Required before audio reads or writes. |
| `scripts/trim_clean_experimental_segments.py` | R1 preview support | `reusable_now` with caution | dry-run by default; `--execute` writes | explicit reviewed segment/preview authority | clean preview artifacts | caller-supplied roots; risk of wrong output root | may read/write audio previews | may affect preview artifacts, not review truth | no full render | run its dry-run/preflight mode only | Required for `--execute`. |
| `scripts/finalize_reviewed_unit_previews.py` | R1 preview finalization | `reusable_now` with caution | dry-run by default; `--execute` writes | explicit reviewed units and output root | framework/preview artifacts | caller-supplied roots | may read/write audio previews | may affect preview artifacts, not review truth | no full render | run its dry-run/preflight mode only | Required for `--execute`. |
| `scripts/validate_canon.py` | canon validation | `reusable_now` | validation | canon/source/schema authority | validation stdout/report | none known | no | no | no | normal validation command for selected inputs | Not needed for read-only validation; approval for writes. |
| `scripts/validate_dapu_ir.py` | Dapu IR validation | `reusable_now` | validation | Dapu IR/schema authority | validation stdout/report | none known | no | no | no | normal validation command for selected inputs | Not needed for read-only validation; approval for writes. |

## Human Review Gates

Require human review for:

- Unknown notation review.
- Recording plan review.
- R0 marker acceptance.
- R1 segment/QC/tail review.
- R2 phrase/version review.
- ABCD listening review.
- E listening review.
- F acceptance.
- Sample ingest candidate review.
- Arrangement proposal review.

## Stop Rules

Stop and ask, or write a dry-run audit report instead of changing state, when:

- A script is hardcoded to a different piece, session, qinist, render set, version, or output root.
- Current state could be Downloads, restore zip, browser Blob, old exports, or archive copies.
- The task would write audio, render, review, sample, archive, cleanup, or second-piece files outside explicit allowed paths.
- A minor listening issue could trigger G/F2, F redo, full R012 governance, or render regeneration without explicit approval.
- Work drifts into sample ingest, ML training, Arrangement Mode, cleanup, archive/delete, REVIEW/DELETE_CANDIDATE handling, or second-piece execution without authorization.
- Score facts and qinist realization are being mixed.
- Root/scope/file_id ambiguity exists.
- R2 latest JSON authority is not confirmed.
- The user says "不要猜" and metadata identity, scope, source authority, or coverage is ambiguous.

## Engineer Instead Of Remembering

These must be solved by code, schemas, tests, manifests, or dry-run tooling rather than by relying on this skill:

- R0 root/scope/file_id compatibility.
- R2 canonical/derived guard.
- `full_tail` / natural decay default.
- Script parameterization and dry-run default.
- Coverage diff.
- Sample ingest schema.
- Wrong-take exclusion checks.

## Future Work

- Parameterize XWC/Baiya scripts.
- Build a generic recording plan generator from Dapu Event IR.
- Build a generic ABCD render template.
- Build a generic final reviewed render generator.
- Define sample ingest gate/schema.
- Build a cross-piece candidate database.
- Build Arrangement Planner, Fingering Search, and Guqinization Review.

## Case Study: XWC / Baiya

Use XWC/Baiya as a learned guard, not a hardcoded workflow.

- `F_FINAL_REVIEWED` passed by human listening: "F通过，除了上七九的一点点小瑕疵".
- The 上七九 note is a low-severity residual issue; do not auto-generate G/F2 or redo F.
- T008 was a wrong take for `XWC_P02_N03`; accepted E/F used replacement provenance such as T014 for exact `SAN_TIAO_6`.
- P02/P09 showed that human phrase semantics and context-take identity cannot be guessed from code alone.
- R0 root/scope/file_id compatibility requires wide raw root plus include-prefix filtering, not a narrow root that changes IDs.
- R2 latest JSON is canonical; CSV/YAML are derived outputs.
- Guqin default tail policy is `full_tail` / natural decay; smart fade is only an explicit override.
