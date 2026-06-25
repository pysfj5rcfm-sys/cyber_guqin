# QXBY Fingering Chapter Extraction Review v0.1

Task id: `CG-QXBY-FINGERING-LEXICON-AND-VISUAL-ATLAS-DRAFT-v0.1`

Status labels: `QXBY_FINGERING_LEXICON_DRAFT`, `VISUAL_COMPONENT_ATLAS_DRAFT`, `NOT_CANON_AUTHORITY`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.

This task follows jianzipu parser rule baseline v0.3.
This task does not redesign v0.3.
Any conflict is reported as a v0.3.1 patch candidate only.

This extraction does not make any term canonical.
It creates a searchable draft lexicon and visual atlas proposal only.
LXY page01 recognition must still mark NEEDS_HUMAN_REVIEW.

## Preflight Summary

- Local worktree root observed: `D:/AIProjects/cyber_guqin`
- Branch: `master`
- HEAD: `08985b780b96279297c6763d8edb659416f43247`
- Preflight status before report writes: clean.
- Note: the task prompt expected `D:/AIProjects/cyber_guqin/Cyber_Guqin_v1`, but the local git top-level for this execution is `D:/AIProjects/cyber_guqin`. HEAD exactly matches the prompt's observed remote main commit, so the report-only task proceeded.

## Sources Read

- `canon/drafts/qxby_batch_001.yaml`
- `canon/drafts/qxby_batch_002.yaml`
- `reports/qxby_batch_001_human_review.md`
- `reports/qxby_batch_002_report.md`
- `C:/Users/11028/Downloads/qinxue_beiyao_two_pdfs_package.zip::指法篇.pdf`
  - SHA256: `75f65bf8b521416b8c83b1b95e268b03ee772f4c936b2085df5a4b722069b75f`
  - 44 pages, image-only PDF.
- `C:/Users/11028/Downloads/qinxue_beiyao_two_pdfs_package.zip::减字谱组识法.pdf`
  - SHA256: `6f976e3e2f2f647539c7e8a8eac02edcf9bf138164b77c9bcb917d8325b33fd1`
  - 2 pages, image-only PDF.
- `C:/Users/11028/Downloads/codex_qxby_prompt_package_v0.1.zip::jianzipu_decomposition_rules_v0.3_context.md`
  - SHA256: `f35344f25574d98494cf87dd9de1e692704345a151f0b3b9da3621ced10f0869`

No PDF was copied into the git repository. Temporary PDF page images were used only outside the repo for visual inspection.

## 1. Existing QXBY Batch001 Terms Reused

Batch001 status preserved as: human-reviewed draft, not verified.

Reused terms: `擘`, `托`, `抹`, `挑`, `勾`, `剔`, `打`, `摘`, `绰`, `注`, `撞`, `反撞`, `上`, `下`, `掐起/搯起`, `撮`.

These terms remain draft evidence only. They are not canon authority and are not Dapu IR input.

## 2. Existing QXBY Batch002 Terms Reused

Batch002 status preserved as: draft / needs_review.

Reused terms: `按音`, `散音`, `大指`, `食指`, `中指`, `名指`, `跪指`, `泛音`.

These terms remain draft evidence only. They must still be confirmed before use in LXY page01 recognition.

## 3. New Draft-Only Terms Proposed

New draft-only terms from this pass:

- Right-hand sequence or compound: `轮`, `锁`, `背锁`, `长锁`, `短锁`.
- Double-string or multi-string: `反撮`, `打圆`, `全扶`.
- Cross-string sequence: `历`, `滚`, `拂`, `滚拂`, `拨剌/泼剌`.
- Left-hand motion: `进`, `退`, `复`, `进复`, `退复`, `急进复`.
- Ornament or transition: `吟`, `猱`.
- Special technique: `抓起`.
- Non-sounding or timing/context: `少息`, `省`.
- Sound-state boundary: `泛起`, `泛止`.

The visual pass also saw adjacent two-string terms such as `叠`, `夹`, `牵`, and related forms. They were not promoted into the required high-risk sheet because their exact boundaries and normalization need a separate focused pass.

## 4. Terms Requiring User Review Before LXY Recognition

All extracted terms require review before use. Highest priority:

`轮`, `锁`, `背锁`, `长锁`, `短锁`, `历`, `滚`, `拂`, `滚拂`, `拨剌`, `撮`, `反撮`, `打圆`, `全扶`, `绰`, `注`, `上`, `下`, `进`, `退`, `复`, `进复`, `退复`, `急进复`, `吟`, `猱`, `撞`, `反撞`, `掐起`, `搯起`, `抓起`, `少息`, `省`, `泛起`, `泛止`.

The review sheet marks `反撮`, `进复`, `退复`, `急进复`, `猱`, and `抓起` as missing or not confidently found in this pass.

## 5. Terms Affecting Event Granularity

These may change whether one visible jianzipu group contains one sounding unit, multiple sounding units, or a modifier sequence:

`轮`, `锁`, `背锁`, `长锁`, `短锁`, `历`, `滚`, `拂`, `滚拂`, `拨剌`, `撮`, `反撮`, `打圆`, `全扶`, `进`, `退`, `复`, `进复`, `退复`, `急进复`, `撞`, `反撞`, `掐起`, `搯起`, `抓起`.

Per v0.3 R82, none of these event counts may be inferred from jianpu, OCR grouping, old CSV rows, page line layout, or visual spacing alone.

## 6. Terms Affecting Sound State

Sound-state terms and boundaries:

- `散音`: open-string state candidate.
- `按音`: pressed-string state candidate.
- `泛音`: harmonic state candidate.
- `泛起`: harmonic-state entry boundary candidate.
- `泛止`: harmonic-state exit boundary candidate.

`泛起` and `泛止` are especially important as v0.3.1 patch candidates because 《减字谱组识法》 page 166 uses them in reading examples.

## 7. Terms Affecting Sounding Units / Subaction Sequence

Likely sequence or multi-unit candidates:

- `轮`: visually described as sequential `摘` and `剔` in this pass.
- `锁`, `背锁`, `长锁`, `短锁`: right-hand sequence family; subaction count needs review.
- `历`, `滚`, `拂`, `滚拂`: cross-string sequence family; string span and unit count need review.
- `拨剌/泼剌`: compound family; spelling and subaction sequence need review.
- `撮`, `反撮`, `全扶`: multi-string or simultaneous policy needs review.
- `打圆`: compound or circular action; event count and simultaneity need review.
- `进复`, `退复`, `急进复`: compound left-hand motion candidates; not confidently sourced in this pass.

## 8. Non-Sounding Terms

Draft non-sounding or context candidates:

- `少息`: timing/breath marker candidate from 《减字谱组识法》 page 166.
- `省`: omission/context inheritance candidate from 《减字谱组识法》 page 165.
- `泛起`, `泛止`: treated as state-boundary candidates, non-sounding by themselves unless source evidence and human review say otherwise.
- `旁注`: not a sounding event by default; it must remain side-note evidence until reviewed.

## 9. Terms That Should Never Be Inferred From Jianpu

No fingering term, string number, hui position, right-hand action, left-hand action, rhythm, or event count should ever be inferred from jianpu.

This applies to every term in this report, especially:

`轮`, `锁`, `背锁`, `长锁`, `短锁`, `历`, `滚`, `拂`, `滚拂`, `拨剌`, `撮`, `反撮`, `打圆`, `全扶`, `绰`, `注`, `上`, `下`, `进`, `退`, `复`, `进复`, `退复`, `急进复`, `吟`, `猱`, `撞`, `反撞`, `掐起`, `搯起`, `抓起`, `少息`, `省`, `泛起`, `泛止`, `散音`, `按音`, `泛音`.

Jianpu may be used only as rough phrase locator in a separate LXY page01 recognition task, never as score-fact authority.

## 10. LXY Page01 OCR False-Surface Forms To Deprecate

The following LXY page01 OCR or visual-surface forms should be deprecated as authority. They may remain as rejected OCR notes only:

- Generic or layout-like forms: `正`, `立`, `曲`, `干`, `回`, `四`.
- Context-only or ambiguous forms: `省`, `同`, `首`, `蓋/盖`, `仓/仑`.
- Large composite-looking forms that may represent jianzipu blocks, not standalone terms: `蓬`, `篷`, `蓝`, `餐`, `登`, `曷`.
- Any OCR segmentation that splits or merges glyph blocks based on printed spacing, staff-like alignment, or jianpu rhythm.

Deprecated here means rejected as score-fact authority, not deleted from review evidence.

## Human Review Decisions Applied After v0.1

These decisions are written back as `QXBY_HUMAN_REVIEW_DECISION_DRAFT` and do not mark any term verified.

- D11: 锁类序列修正. `轮=[摘,剔,挑]`, `锁=[抹,挑,抹]`, `背锁=[剔,抹,挑]`, `长锁=[抹,挑,抹,勾,剔,抹,挑]`, `短锁=[抹,勾,剔,抹,挑]`. The previous confusion that mapped `锁` to `抹勾剔抹挑` is corrected; that sequence belongs to `短锁`.
- D12: 绰/注成对建模. Both are modeled as `paired_approach_motion`, `timing=pre_attack`, `sound_type=虚声`, `independent_sounding_event=false` when the paired model applies.
- D13: 进复/退复来源补正. User supplied `左下标70页，非 PDF physical page 70`; status is `source_found_by_user_needs_structured_update`, not verified.
- D14: 猱来源补正. User supplied `右下标65页`; model policy is `paired_or_contrasted_with_吟`; status is `source_found_by_user_needs_structured_update`, not verified.
- D15: 撞/反撞成对建模. Both are `position_transition` / `virtual_attack_motion`, not ordinary ornaments.
- D16: 掐起/搯起来源确认. User supplied `左下标74页`; model policy is `special_technique_with_sounding_unit_candidate`; status is `source_confirmed_by_user_needs_structured_update`, not verified.
- D17: 爪起术语修正. Preferred term is `爪起`; `抓起` is retained only as mistaken form / alias. User supplied `左下标76页`; status is `source_found_by_user_needs_structured_update`, not verified.

## Human Review Checklist

- Confirm exact QXBY page references for all Batch001 terms with page-unconfirmed status.
- Confirm `反撮`, `猱`, `爪起/抓起`, `进复`, `退复`, and `急进复` source pages or mark them out of scope.
- Decide preferred normalization for `拨剌` versus `泼剌`.
- Decide preferred normalization for `掐起` versus `搯起`.
- Review whether `泛起` and `泛止` should be represented as non-sounding state boundaries in v0.3.1.
- Review whether `省` maps to context inheritance, omission, or a narrower rule.
- For LXY page01, confirm visual glyph blocks from the PNG before using any atlas match.

## Safety Boundary Confirmation

- No production import was performed.
- No canon authority was created.
- No Dapu IR was created.
- No sample ingest file was written.
- No ML training data was created.
- No audio/render/R0/R1/R2 workflow was executed.
- No files under `01_pieces/`, `canon/`, `sources/`, `references/`, `schemas/`, `03_samples/`, or `04_outputs/` were modified.
