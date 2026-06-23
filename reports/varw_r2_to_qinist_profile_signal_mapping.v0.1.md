# VARW R2 to Qinist Profile Signal Mapping v0.1

状态：设计稿。Extension/mapping layer only。

## 1. Authority

Current VARW/R2 authority:

```text
r2_review_state.latest.json = canonical
CSV/YAML exports = derived
```

Derived exports may provide readable evidence, but profile mapping should reference the latest JSON and only cite CSV/YAML as derived trace.

## 2. Mapping Flow

```text
R2 phrase/version review
-> listening review
-> revision log
-> preferred version summary
-> profile signal extension
-> Qinist Profile v0.1
```

No new R2 label system is introduced.

## 3. Existing Evidence Fields

Canonical/latest JSON:

- `listeningReviewByKey`
- `preferredVersionByPhrase`
- `phrase_alignments`
- `phrase_markers`
- `review_count`
- `phrase_count`
- `preferred_version_count`
- `suggested_revision_count`

Derived files:

- `listening_review.csv`
- `preferred_version_summary.csv`
- `issue_list.csv`
- `render_phrase_alignment.csv`
- `phrase_boundary_decision.csv`
- `render_revision_log.yaml`

## 4. Signal Families

Draft profile signal families:

- timing preference
- tail preference
- ornament density preference
- phrase motion preference
- breath/cadence preference
- rejection reason pattern

`profile_signal_id` and `profile_signal_type` are proposed extension fields. They identify derived signals only; they do not replace R2 review rows.

## 5. Field Mapping

| Profile signal | Existing VARW evidence |
| --- | --- |
| timing preference | `preferredVersionByPhrase`, `start_s`, `end_s`, `phrase_play_start_s`, `phrase_play_end_s` |
| tail preference | `phrase_tail_end_s`, `tail_policy`, `issue_type=tail_short` |
| ornament density preference | `issue_type`, `comment`, `suggested_revision`, future realization fields |
| phrase motion preference | `preferred_version_id`, `comment`, `suggested_revision` |
| breath/cadence preference | `breath_points_s`, `cadence_point_s`, `phrase_end_policy` |
| rejection reason pattern | `issue_type`, `severity`, rejected/unclear review rows |

## 6. Evidence References

Every profile signal should cite:

- `render_set_id`
- `phrase_id`
- `version_id` or `preferred_version_id`
- review key from `listeningReviewByKey`
- source file/path if derived export is used for audit display
- confidence

`evidence_refs` is proposed because current repo fields are either parser source refs or review row IDs, not a cross-layer profile evidence array.

## 7. Safety

- Do not infer Sanman profile from Baiya as style data.
- Do not write profile signals back into score facts.
- Do not mark profile as trained model.
- Do not treat F pass as sample asset gate.

