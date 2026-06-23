# XWC Process Script Reuse Audit DRY RUN

- Task: `CG-XWC-MVP-P1D_PROCESS_PLAYBOOK_LESSONS_SCRIPT_AUDIT_AND_WORKFLOW_SKILL_DESIGN`
- Phase: `Phase 1F-XWC-MVP Passed / Sweep & Review`
- Mode: text/metadata-only script audit.

## 0. 本轮执行声明

本轮只审计脚本文本和 metadata。未运行任何脚本，未跑 render，未读取 audio binary，未修改脚本，未参数化脚本，未移动/删除/归档脚本，未处理 `scripts/generate_baiya_recording_plan.py`。当前 `git status --short --untracked-files=all` 在审计前显示：

```text
?? scripts/generate_baiya_recording_plan.py
```

## 1. 分类标签

- `reusable_now`: 当前已参数化或 dry-run 安全，可在明确输入/输出目录下复用。
- `reusable_after_parameterization`: 逻辑有复用价值，但当前 hardcoded 到 XWC/Baiya/session/path/version，第二首前必须参数化。
- `historical_only`: 只作为历史证据或一次性修复记录，不应再作为流程入口。
- `archive_candidate_later`: 后续可归档，但本轮不归档。
- `delete_candidate_later`: 后续可删除，但本轮不删除。
- `unknown_needs_review`: 需要单独审计后才能决定。

## 2. 重点脚本审计

### 2.1 `scripts/generate_baiya_recording_plan.py`

| Field | Audit |
| --- | --- |
| current git state | untracked；本轮未处理。 |
| referenced by repo | 多份既有 reports 提到该脚本为 pre-existing untracked；未发现当前流程代码引用。 |
| hardcoded | 是。`SESSION_ID=RS_XWC_002_BAIYA_PILOT`、`RECORDING_ID=RS_XWC_002`、`PIECE_ID=XWC`、`QINIST_ID=QINIST_002`、`QINIST_NAME=白牙`、T001-T071、T060/T071 context rule、XWC bridge inputs。 |
| inputs | `reports/xwc_legacy_recording_bridge_map.json`、`01_pieces/xianwengcao/recording_script_human.csv`、部分 docs。 |
| outputs | 多个 `reports/rs_xwc_002_baiya_*` 和 `06_docs/RS_XWC_002_BAIYA_RECORDING_PLAN_REVIEW.md` 草稿，需 `--execute` 才写。 |
| parameters | `--input-root`、`--output-root`、`--execute`；但 domain constants hardcoded。 |
| reads audio | 否。 |
| writes audio/render | 否。 |
| modifies review data | 否；写 draft reports/docs。 |
| safe for second piece | 否，不能直接运行。 |
| value | 录音计划生成逻辑、slate variants、tail silence policy、retake/bad take policy 有复用价值。 |
| classification | `reusable_after_parameterization`, `archive_candidate_later` if replaced by generic planner。 |
| next recommendation | keep now；后续参数化为 `generate_recording_plan_from_dapu_ir.py` 或纳入 workflow script registry；本轮不得执行、提交、删除、归档。 |

### 2.2 `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py`

| Field | Audit |
| --- | --- |
| role | 历史修复脚本：刷新 R1 tail policy、重写 preview、复制旧 F、调用 F generator、重写 latest 和 derived exports。 |
| hardcoded | 是。`XWC`、`RS_XWC_002_BAIYA_PILOT`、`QINIST_002`、`F_FINAL_REVIEWED`、render set id、R1/F path 全部 hardcoded。 |
| inputs | R1 archive/workbench、split preview manifests、existing F、latest JSON、raw/split audio。 |
| outputs | 会写 R1 CSV/draft、F archive、F wav/alignment/report/validation、latest JSON、derived CSV/YAML、full_tail audit files。 |
| reads audio | 是，会 open raw/source wav。 |
| writes audio/render | 是，会 slice previews、复生成 F。 |
| modifies review data | 是，会写 R1/F/R2 latest。 |
| safe for second piece | 否，禁止作为默认流程直接运行。 |
| classification | `historical_only`, `archive_candidate_later`。 |
| reuse condition | 必须先拆出只读 audit、tail policy transform、render generation 三个安全参数化模块；并加 dry-run/default no-write。 |

### 2.3 `scripts/render_xwc_abcd_from_planning.py`

| Field | Audit |
| --- | --- |
| role | 从本地 planning 生成 XWC/Baiya ABCD experimental render。 |
| hardcoded | 是。`SESSION_DIR=04_outputs/XWC/RS_XWC_002_BAIYA_PILOT`、ABCD wav names、P09 context policy、`XWC_P09_N02`、`T060/T071`、render settings。 |
| inputs | `_planning` source map / phrase plan / version policy / E schema / readiness manifest；clean preview wav。 |
| outputs | ABCD wav、alignment CSV、selection decision、render manifest、validation、listening guide。 |
| parameters | 只有 `--preflight-only`；没有 piece/session/config 参数。 |
| reads audio | 是，读取 clean preview wav metadata 和 PCM。 |
| writes audio/render | 是，除非 `--preflight-only`。 |
| modifies review data | 不改 R0/R1/R2 review state，但写 render outputs。 |
| safe for second piece | 默认不安全；可作为 ABCD render 模板。 |
| classification | `reusable_after_parameterization` with high risk；current file also `historical_only` for XWC run evidence。 |
| parameterization needs | session root、piece id、render_set_id、version definitions、phrase/event parser、context take policy、output names、input manifest contract、dry-run default。 |

### 2.4 `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py`

| Field | Audit |
| --- | --- |
| role | 从 E_REVIEWED 和 canonical latest 生成同名 `F_FINAL_REVIEWED` 并同步 R2 latest exports。 |
| hardcoded | 是。`XWC`、`RS_XWC_002_BAIYA_PILOT`、`E_REVIEWED`、`F_FINAL_REVIEWED`、P01/P02 phrase classes、T008 guard、T014 replacement、render set id。 |
| inputs | latest JSON、E wav、E alignment、source wav previews。 |
| outputs | F wav、F alignment、F plan/report/validation、input snapshot、latest JSON、derived CSV/YAML。 |
| reads audio | 是。 |
| writes audio/render | 是。 |
| modifies review data | 是，会写 latest JSON 和 review entries。 |
| safe for second piece | 否。 |
| classification | `reusable_after_parameterization` for algorithm ideas; current script `historical_only` for XWC F generation。 |
| parameterization target | `generate_final_reviewed_render.py`，由 manifest 提供 source version、target version、phrase classes、tempo/tail policy、sample safety rules、output root。 |

## 3. 全脚本粗分类

| Script | Classification | Second-piece note |
| --- | --- | --- |
| `scripts/generate_baiya_recording_plan.py` | `reusable_after_parameterization` | 录音计划逻辑可用，但 Baiya/XWC/T001-T071 hardcoded。 |
| `scripts/render_xwc_abcd_from_planning.py` | `reusable_after_parameterization` | 可作为 ABCD render 模板，但当前会读写 audio/render，默认不可跑。 |
| `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py` | `reusable_after_parameterization`, `historical_only` | 需改为 manifest-driven final render generator。 |
| `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py` | `historical_only`, `archive_candidate_later` | 历史修复脚本，第二首不得默认运行。 |
| `tools/cg-varw/backend/scripts/verify_r2_canonical_draft.py` | `reusable_after_parameterization` | 只读验证逻辑有价值，但 default render root hardcoded XWC/Baiya。 |
| `scripts/slate_number_recognizer.py` | `reusable_now` | 参数显式，默认 dry-run，适合录音计划之后复用。 |
| `scripts/trim_clean_experimental_segments.py` | `reusable_now` with caution | 参数显式，默认 dry-run；写 preview artifacts，需授权。 |
| `scripts/finalize_reviewed_unit_previews.py` | `reusable_now` with caution | 参数显式，默认 dry-run；写 framework artifacts，需授权。 |
| `scripts/split_framework_common.py` | `reusable_now` | helper module。 |
| `scripts/validate_canon.py` | `reusable_now` | canon validation。 |
| `scripts/validate_dapu_ir.py` | `reusable_now` | Dapu IR validation。 |
| `scripts/validate_canon_seed.py` | `reusable_now` | seed validation。 |
| `scripts/check_v1_compat.py` | `historical_only` or `unknown_needs_review` | V1 compatibility audit，可能仍有用，需按任务确认。 |
| `scripts/audit_v1_to_canon_coverage.py` | `historical_only` | XWC/canon transition audit evidence。 |
| `scripts/build_xwc_legacy_bridge_preview.py` | `historical_only` | XWC legacy bridge only；第二首不应使用。 |
| `scripts/register_mvp_pilot_raw_audio.py` | `historical_only`, `delete_candidate_later` after replacement | 固定 `RS_XWC_001/QINIST_001`，不适合第二首。 |
| `scripts/audit_recording_ingest_readiness.py` | `historical_only` | 早期 ingest readiness，不等于当前 sample ingest plan。 |
| `scripts/audit_qxby_batch_sources.py` | `unknown_needs_review` | QXBY specific，非 XWC 第二首流程核心。 |
| `scripts/validate_qxby_batch.py` | `unknown_needs_review` | QXBY specific。 |
| `scripts/slate_based_experimental_split.py` | `historical_only` | 自述为替代/解释流程，需另审。 |

## 4. 按流程阶段的脚本候选

| Phase | Candidate | Use now? | Risk |
| --- | --- | --- | --- |
| Score / Dapu planning | `validate_canon.py`, `validate_dapu_ir.py` | 可只读/验证时使用 | 不生成新曲 formal outputs，除非授权。 |
| Recording plan | `generate_baiya_recording_plan.py` | 否 | Baiya/XWC hardcoded；仅作为模板。 |
| Slate planning | `slate_number_recognizer.py` | 可在授权后 dry-run | 需显式 session/raw/take plan/output。 |
| R0 raw review | cg-varw backend APIs, not standalone script | 否 | 需 UI/API 人审。 |
| R1 split review | `trim_clean_experimental_segments.py`, `finalize_reviewed_unit_previews.py` | 可在授权后 dry-run | 会写 preview/framework artifacts with `--execute`。 |
| R2 canonical check | `verify_r2_canonical_draft.py` | 当前 XWC 可只读；第二首需参数化 | Default root hardcoded。 |
| ABCD render | `render_xwc_abcd_from_planning.py` | 否 | 会读写 wav/render；hardcoded。 |
| E/F render | `generate_xwc_f_final_reviewed.py` | 否 | 会写 F/latest；hardcoded。 |
| full_tail repair | `refresh_xwc_r1_full_tail_and_regenerate_f.py` | 否 | 历史修复，重写 R1/F。 |
| sample ingest | none approved | 否 | 当前 gate 未通过。 |
| ML | none approved | 否 | 当前不是 training。 |

## 5. 后续归档/删除建议，本轮不执行

Archive candidates later:

- `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py`
- XWC-specific one-off reports/scripts once generic replacements exist。
- `scripts/build_xwc_legacy_bridge_preview.py` after XWC migration evidence is indexed。

Delete candidates later:

- `scripts/register_mvp_pilot_raw_audio.py` if superseded by a generic raw registration workflow and historical reports remain sufficient。
- Any stale one-off script only after user approves and a report maps replacement/retention reason。

Keep for now:

- `scripts/generate_baiya_recording_plan.py` because it is untracked, historically referenced, and not yet replaced。
- reusable parameterized helpers under split/slate/validation。

## 6. Script Registry 草案

后续 workflow skill 不应记住所有脚本细节，而应维护一个 script registry：

| Registry field | Required |
| --- | --- |
| script path | exact path |
| phase | Track A/B/C phase |
| status | reusable_now / after_parameterization / historical_only / blocked |
| default mode | read-only / dry-run / writes reports / writes audio |
| input manifest | required config and authority file |
| output paths | exact allowed outputs |
| hardcoded hazards | piece/session/qinist/render_set/version |
| forbidden side effects | audio/render/review/sample/ML |
| preflight | command that does not write, if any |
| human gate | required approval before execute |

## 7. Next Recommendation

下一步可以生成真正 workflow skill 文件，但不要直接工程化脚本。脚本工程化应作为再下一步：先把 `generate_baiya_recording_plan.py`、`render_xwc_abcd_from_planning.py`、`generate_xwc_f_final_reviewed.py` 拆成 manifest/config-driven dry-run-first tools，再用第二首小曲验证。`refresh_xwc_r1_full_tail_and_regenerate_f.py` 只保留为历史修复证据，不进入默认 workflow。
