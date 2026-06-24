# LXY Page01 OCR Canon Match Dry Run v0.1

Task id: `CG-LXY-PAGE01-OCR-CANON-MATCH-DRY-RUN-v0.1`

Status labels: `OCR_CANON_MATCH_DRY_RUN`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.

## 1. Preflight Result

Initial workspace root `D:\AIProjects\cyber_guqin` was not itself accepted by `git` as the active worktree for the requested paths. A nested local worktree was present at:

`D:\AIProjects\cyber_guqin\Cyber_Guqin_v1`

All required preflight commands were then run from that local worktree.

- `git status --short --untracked-files=all`: clean before report generation.
- `git branch --show-current`: `main`
- `git rev-parse HEAD`: `b19c273f77a7e65ff0adaa9ce840091e6d45c4e4`
- `git log --oneline -n 5`:
  - `b19c273 chore(reports): add R2B archive reference dry-run review`
  - `0541bbb chore(reports): add R2 archive dry-run proposal`
  - `bbad758 chore(repo): ignore local generated artifacts`
  - `66f2a44 docs(repo): index structure and script safety boundaries`
  - `4f181a4 chore(reports): add latest repo hygiene audit reports`

Required files and directories were present in `Cyber_Guqin_v1`:

- `README.md`
- `06_docs/PROJECT_STRUCTURE.md`
- `reports/REPORTS_INDEX.md`
- `reports/repo_hygiene_inventory.latest.v0.1.json`
- `reports/repo_entrypoint_map.latest.v0.1.md`
- `.agents/skills/`
- `canon/`
- `references/`
- `sources/`
- `schemas/`
- `reports/`

Skill files:

- Present: `.agents/skills/guqin-canon-builder/SKILL.md`
- Present: `.agents/skills/guqin-dapu-parser/SKILL.md`
- Present: `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`

No preflight stop condition was triggered after switching to the nested local worktree.

## 2. Image Input

Image path used:

`C:/Users/11028/Downloads/LXY_良宵引_page01.png`

The image exists locally. Temporary enlarged crops were generated only under the system temp directory for visual inspection. No crop files were written to the repo.

## 3. Sources Read

Skills:

- `.agents/skills/guqin-canon-builder/SKILL.md`
- `.agents/skills/guqin-dapu-parser/SKILL.md`
- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`

Canon and references:

- `canon/component_lexicon.yaml`
- `canon/terms.yaml`
- `canon/alias_rules.yaml`
- `canon/gesture_families.yaml`
- `canon/drafts/qxby_batch_001.yaml`
- `canon/drafts/qxby_batch_002.yaml`
- `references/normalization_rules.md`
- `references/validation_rules.md`

QXBY reports and manifests:

- `sources/qinxue_beiyao/QXBY_BATCH_001/manifest.yaml`
- `sources/qinxue_beiyao/QXBY_BATCH_002/manifest.yaml`
- `reports/qxby_batch_001_human_review.md`
- `reports/qxby_batch_002_report.md`

Note: a broad `rg` discovery command was used early and returned matches from many files. The matching evidence used in this report is limited to the files listed above.

## 4. Phrase Map Used

User-corrected phrase map:

```text
PH01: 56111111
PH02: 650321211——
PH03: 11121｜66661｜653｜3。
PH04: 011｜121｜666｜66｜121｜6765｜33——
PH05: 56｜56｜333｜3332｜166｜661｜2｜03｜53｜21｜1——
PH06: 56｜1｜1｜11｜56｜1｜1——
```

Critical boundary statement: the jianpu strings above were used only as phrase locator and rough visual boundary aids. They were not used to infer event count, pitch, rhythm, string number, hui/fen, right-hand action, left-hand action, Dapu IR fields, or score authority.

## 5. Matching Method

1. Confirmed local worktree and allowed path availability.
2. Read current guqin skills and canon/QXBY context.
3. Inspected the page image directly and used temporary enlarged crops for the visible area from 一段 opening to before the （二段） marker.
4. Grouped visually separable jianzipu glyph blocks by PH01-PH06 using the user phrase map only as a locator.
5. Matched visible candidate terms only against current repo canon and QXBY draft/review evidence.
6. Marked all output as review-only, not score import and not Dapu IR authority.

OCR note: no authoritative OCR engine output was used. `ocr_text_candidate` values in the JSON are manual visual OCR candidates from the image and remain `needs_review=true`.

## 6. Available Relevant Canon Context

Higher-confidence repo entries:

- `勾`: right-hand middle-finger inward pluck, in `canon/component_lexicon.yaml`; QXBY_BATCH_001 reviewed draft item `QXBY_005`.
- `擘`: right-hand thumb inward pluck, in `canon/component_lexicon.yaml`; QXBY_BATCH_001 reviewed draft item `QXBY_001`.
- `上`: left-hand post-attack upward slide, in `canon/component_lexicon.yaml`; QXBY_BATCH_001 reviewed draft item `QXBY_013`.
- `下`: left-hand post-attack downward slide, in `canon/component_lexicon.yaml`; QXBY_BATCH_001 reviewed draft item `QXBY_014`.
- `泛音`: sound type in `canon/terms.yaml`; QXBY_BATCH_002 draft item `QXBY_B002_008`.

Important evidence status:

- QXBY_BATCH_001 is accepted as a human-reviewed draft but not `verified`.
- QXBY_BATCH_002 remains draft / needs review.
- OCR candidates must not be marked verified.

## 7. Candidate Summary by Phrase

Machine-readable details are in `reports/lxy_page01_ocr_canon_match_candidates.v0.1.json`.

| phrase | candidate count | summary |
| --- | ---: | --- |
| PH01 | 4 | Opening clusters include repeated 勾-like forms, one 勾正-like group, and two unresolved complex/仓-like groups. |
| PH02 | 5 | Contains two stronger 勾 matches, several unresolved 仓/省/屈-like forms, and one sustained complex glyph. |
| PH03 | 5 | Contains a strong 泛-like group, possible 上, possible 泛 at right, and two unresolved complex clusters. |
| PH04 | 7 | Contains another strong 泛-like group, possible 上, possible 泛+勾 cluster, and multiple unresolved line-wrap/complex marks. |
| PH05 | 11 | Mostly unresolved dense groups; weak possible 勾, weak possible 擘, possible 下. |
| PH06 | 7 | Contains several clearer 勾-like groups before （二段）, plus unresolved final large glyphs. |

Total candidate glyph groups: 39.

## 8. High-Confidence / Stronger Matches

The following are stronger visual-to-canon matches, but still require human review before any parsing or import:

- `勾`: PH01-G02, PH02-G03, PH02-G04, PH06-G01, PH06-G02, PH06-G05, PH06-G06.
- `泛音` / `泛`: PH03-G03, PH04-G04; weaker partial matches in PH03-G05 and PH04-G06.
- `上`: PH03-G04; weaker in PH04-G05 and PH05-G08.
- `下`: PH05-G10, still mixed with unresolved position/action components.

## 9. Low-Confidence Matches

Low-confidence or uncertain groups include:

- PH01-G03, PH01-G04
- PH02-G01, PH02-G02, PH02-G05
- PH03-G01, PH03-G02, PH03-G05
- PH04-G01, PH04-G02, PH04-G03, PH04-G05, PH04-G06, PH04-G07
- PH05-G01 through PH05-G11
- PH06-G03, PH06-G04, PH06-G07

Common uncertainty causes:

- dense handwritten reduction forms;
- unresolved suffixes such as 正-like, 干-like, 立-like, 省-like, 回-like, 曲-like, 仓/仑-like, 盖/蓝-like;
- QXBY evidence exists for some basic terms but not for many page-specific compound glyphs;
- no safe rule yet for mapping visible small numerals/components into hui/fen/string fields.

## 10. Canon Gaps

Primary canon gaps observed in the image candidate pass:

- No current canon entry for the recurring 正-like suffix after 勾.
- No current canon entry for 省-like marks.
- No current canon entry for 仓/仑-like opening/transition glyphs.
- No current canon entry for 立-like marks.
- No current canon entry for 曲-like mark.
- No current canon entry for several large complex glyph families resembling 蓬/篷/盖/蓝/餐/登.
- No current page-specific rule for small stacked numeric/position marks visible near 上/下 candidates.

## 11. Evidence Gaps

Evidence gaps that block a stronger parse:

- Need human reading of the original 百瓶斋本 glyph groups for PH01-PH06.
- Need supplemental 《琴学备要》 material or other notation explanation for the recurring non-canon reduction forms.
- Need confirmation whether the small suffixes are action marks, position marks, editorial marks, or local reduction components.
- Need confirmation whether weak 擘-like and 勾-like partials in PH05 are real technique glyphs.
- Need line-wrap confirmation for PH04 ending into the next physical line.

## 12. Human Review Checklist

1. Confirm the opening PH01 glyphs, especially the first cluster and the large complex glyph under grouped `111`.
2. Confirm whether `勾正` is a valid reading and what `正` means in this source.
3. Confirm PH02 `省?/屈?` and sustained complex glyph readings.
4. Confirm whether PH03 and PH04 clear 泛-like glyphs are indeed 泛音 components.
5. Confirm whether PH03-G04 is `上` and how the stacked `六三`-like position mark should be read.
6. Confirm whether PH05-G10 contains `下` and whether the right component is `擘` or another mark.
7. Confirm final PH06 groups before （二段）, especially which groups are true 勾 and which are context/position marks.
8. Provide QXBY or source-score evidence for recurring unmatched glyph families.

## 13. Safety Boundary Confirmation

Confirmed:

- No score data imported.
- No `01_pieces/` files written.
- No Dapu IR authority created.
- No recording plan generated.
- No prompt manifest generated.
- No R0/R1/R2 run.
- No audio rendered.
- No sample ingest files written.
- No ML training data generated.
- No runtime/frontend/backend code modified.
- No `canon/`, `sources/`, `references/`, `schemas/`, `examples/`, `templates/`, or `tests/` files modified.
- No accepted F or R2 latest files touched.
- Only the three allowed report paths were written.

