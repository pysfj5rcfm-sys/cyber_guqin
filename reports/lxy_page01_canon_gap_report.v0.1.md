# LXY Page01 Canon Gap Report v0.1

Task id: `CG-LXY-PAGE01-OCR-CANON-MATCH-DRY-RUN-v0.1`

Status labels: `OCR_CANON_MATCH_DRY_RUN`, `NOT_REPO_CONTRACT`, `NOT_DAPU_IR_AUTHORITY`, `NEEDS_HUMAN_REVIEW`, `NOT_SAMPLE_INGEST`, `NOT_ML_TRAINING_DATA`.

Image: `C:/Users/11028/Downloads/LXY_良宵引_page01.png`

Scope: `LXY / 良宵引`, 百瓶斋本, page01, 一段起始至（二段）之前.

## 1. Missing or Weak Canon Entries

Missing or weak entries observed during the visual candidate pass:

| suspected visual term/form | current status | notes |
| --- | --- | --- |
| 正-like suffix after 勾 | missing | Appears in `勾正`-like groups. Need source meaning before any parse. |
| 省-like mark | missing | Appears near PH02 and PH05 groups. Must not be treated as rest/omission without evidence. |
| 仓/仑-like mark | missing | Appears near PH01/PH02 opening groups. Function unknown. |
| 立-like mark | missing | Appears in PH04 and near possible 上 grouping. |
| 曲-like mark | missing | Appears at PH05 physical line 5 left. May be non-fingering mark. |
| 干-like suffix after 泛 | weak/missing | 泛 is matched, but the small suffix is unresolved. |
| large 蓬/篷-like glyph family | missing | Recurs in early sustained/slurred groups. |
| large 盖/蓝/餐/登-like glyph family | missing | Several low-confidence phrase groups depend on this family. |
| stacked 六三/七-like position marks | weak | `上六三?`, `下七?` cannot be converted to hui/fen/string fields without rules. |

Existing but incomplete for this page:

- `勾`, `擘`, `上`, `下`, `泛音` exist in repo canon/QXBY evidence.
- The visible page frequently combines known terms with unresolved local components, suffixes, or position marks.
- Current canon can support term matching, but not full event parsing for page01.

## 2. Missing or Weak QXBY Evidence

Current QXBY evidence:

- Batch001 covers `擘`, `托`, `抹`, `挑`, `勾`, `剔`, `打`, `摘`, `绰`, `注`, `撞`, `反撞`, `上`, `下`, `掐起`, `撮`.
- Batch001 has human-reviewed draft confirmation, but remains not `verified`.
- Batch002 covers `按音`, `散音`, `大指`, `食指`, `中指`, `名指`, `跪指`, `泛音`.
- Batch002 remains draft / needs review.

Weak or missing QXBY evidence needed:

- 百瓶斋本 or QXBY explanation for `正` as a suffix or modifier.
- Explanation for `省` or omission-like marks in jianzipu.
- Explanation for `仓/仑`-like and `立`-like forms.
- Explanation for large complex reduction forms seen in PH01-PH06.
- Rules for reading stacked numeric/position components near `上` and `下`.
- Confirmation whether PH05 weak `擘?` and repeated PH06 `勾勾?` visual groups are true right-hand actions.

## 3. Terms Suspected by Image but Not Found in Repo

The following visual candidates are not matched to current repo canon:

- `正?`
- `省?`
- `仓?` / `仑?`
- `立?`
- `曲?`
- `干?` as suffix after `泛`
- `回?` / `四?` as suffix after `勾`
- large complex forms resembling `蓬?`, `篷?`, `盖?`, `蓝?`, `餐?`, `登?`, `曷?`

These are visual OCR candidates only. They should not be normalized until a human confirms the glyph and an authority source explains the term or component.

## 4. Terms Found in Repo but Visually Ambiguous in Image

| repo term | status in repo | visual ambiguity on page01 |
| --- | --- | --- |
| 勾 | strong canon/QXBY evidence | Many page glyphs look like 勾, but several are embedded in larger groups. Confirm which are actions. |
| 擘 | strong canon/QXBY evidence | PH05-G04 and PH05-G10 may resemble 擘/笔, but visual evidence is weak. |
| 上 | strong canon/QXBY evidence | PH03-G04 is plausible; other 上-like marks may be position/context marks. |
| 下 | strong canon/QXBY evidence | PH05-G10 is plausible but mixed with 七/擘-like marks. |
| 泛音 / 泛 | repo term exists; QXBY Batch002 draft | PH03-G03 and PH04-G04 are visually strong; suffix and context remain unresolved. |

## 5. Questions for User

1. Can you confirm the exact glyph reading for PH01 opening: the first `5.6` group and the later large complex group under the slurred `111`?
2. In this 百瓶斋本 page, what does the small `正`-like suffix after `勾` mean?
3. Are the recurring `省`-like marks notation components, omissions, rests, or editorial signs?
4. Are the large `蓬/篷/盖/蓝`-like glyphs named techniques or compact forms for position/action combinations?
5. For the clear `泛` groups, should the small `干`-like suffix be read as a string, right-hand action, finger, or local reduction component?
6. Does PH05-G10 read as `下七擘` or something else?
7. Do the PH06 repeated `勾勾`-like groups represent repeated right-hand 勾 actions, or is one glyph a position/context mark?

## 6. Suggested Supplemental 《琴学备要》 Material Needed

Recommended supplemental evidence for review:

- QXBY or source-score pages explaining reduction forms for suffixes such as `正`, `省`, `干`, `回/四`, and `立`.
- Pages explaining how string number, hui/fen, and finger/action components are stacked in jianzipu forms.
- Pages or examples for `泛` plus suffix/component combinations.
- Pages or examples for `上`/`下` with stacked numeric position marks.
- Any 百瓶斋本 legend, prefatory notation explanation, or parallel clean page that includes the same glyph families from LXY page01.

## 7. Boundary Reminder

This gap report is audit evidence only. It is not a repo contract, not Dapu IR authority, not sample ingest, and not ML training data.

