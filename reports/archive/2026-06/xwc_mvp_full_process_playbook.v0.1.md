# XWC MVP Full Process Playbook v0.1

- Task: `CG-XWC-MVP-P1D_PROCESS_PLAYBOOK_LESSONS_SCRIPT_AUDIT_AND_WORKFLOW_SKILL_DESIGN`
- Phase: `Phase 1F-XWC-MVP Passed / Sweep & Review`
- Mode: documentation-only process freeze.
- Scope: 《仙翁操》白牙 Dapu audition MVP 全流程固化；不是 production sample ingest。

## 0. 本轮执行声明

本轮只写本报告和同批 3 个 `reports/*.md`。未 patch，未改代码，未改真实 R0/R1/R2/F 数据，未移动、删除、归档文件，未跑 render，未生成 G/F2，未重做 F，未进入 sample ingest，未写 `sample_assets.csv`，未写 `recording_segments.csv`，未创建 `recording_items_enriched.jsonl`，未训练 ML，未进入 Arrangement Mode，未生成真正 skill 文件，未处理 `scripts/generate_baiya_recording_plan.py`。

## 1. 项目目标与当前最终状态

本轮固化的是 Dapu audition MVP：目标是把一首古谱从谱面/录音计划/审校/实验渲染推进到一个可供人耳验收的 audition 版本，用来验证打谱、样本选择、录音审校、渲染判断和人耳偏好的闭环。它不是 production sample ingest，不代表样本库入库，不代表 ML training-ready，不代表 Arrangement Mode 已可用。

| Field | Value |
| --- | --- |
| 曲目 | `XWC` / 《仙翁操》 |
| recording_session_id | `RS_XWC_002_BAIYA_PILOT` |
| recording_id | `RS_XWC_002` |
| performer / qinist | `QINIST_002` / 白牙 |
| final version | `F_FINAL_REVIEWED` |
| render_set_id | `R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e` |
| final status | 用户确认“F通过，除了上七九的一点点小瑕疵” |
| MVP grade | `experimental_render=true`, `production_grade=false` |

当前 F metadata：

| Item | Value |
| --- | --- |
| authority input | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json` |
| F input snapshot | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json` |
| input sha256 | `94b1a58ef43eeb9864671bd2bf6457d65a26298f87a29014bfbfca30499ea885` |
| F wav | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/XWC_BAIYA_F_FINAL_REVIEWED.wav` |
| duration | `84.7080045351474s` |
| audio format | 44100 Hz, 24 bit, stereo |
| tempo ratio | `1.4503682518284098` against E |
| event coverage | 51 events, P01-P10 |
| T008 guard | true; `XWC_P02_N03` uses `T014` |
| tail policy | `full_tail`; `smart_fade_applied=false`; `tail_trimmed_event_count=0` |
| latest export rows | `render_phrase_alignment.csv=60`, `phrase_boundary_decision.csv=60` |

“上七九” minor issue 的处理原则：记录为当前 F 人耳验收的 low-severity residual note；不重开 G，不生成 F2，不重做 F，不回退到 E，不触发 full R012 governance。只有当用户明确把它升级为独立修复任务时，才另开窄任务，并重新声明 canonical input 和禁写范围。

## 2. 全流程阶段图

```text
1. Score / Dapu planning
-> 2. Recording plan
-> 3. R0 raw review
-> 4. R1 split review
-> 5. R2 render review
-> 6. ABCD experimental render
-> 7. E_REVIEWED
-> 8. F_FINAL_REVIEWED
-> 9. human listening acceptance
-> 10. sweep & guard
-> 11. next-piece preparation
```

## 3. Phase 1: Score / Dapu Planning

| Field | 内容 |
| --- | --- |
| 输入 | 古谱谱面、人工谱字、OCR candidates、已有 V1 authority files、历史 XWC bridge 仅可作只读背景。 |
| 输出 | Dapu Event IR / score events / semantic recording items 的草案；缺失指法、缺失上下文、缺失录音清单。XWC 本轮早期使用 legacy bridge，后续第二首应转向正式 Dapu Event IR。 |
| canonical authority | score facts 与 canon layer。`recording_batches.md` 或录音计划不是 score authority。 |
| human decision point | 未知谱字、指法语义、P02/P09 这类解释分歧必须人工确认。 |
| Codex task boundary | 只做解析、比对和缺口报告；不要直接决定三曼/白牙最终演奏风格。 |
| 允许读写路径 | 可读 score/canon/source 文本和 docs；本轮不写这些路径。未来写入必须另开任务。 |
| 不得混入 | sample ingest、render、ML、Arrangement Mode、把 qinist realization 写回 score facts。 |
| 验收标准 | 每个 score event 有来源、置信度、needs_review 状态；score facts 与 qinist realization 分离。 |

## 4. Phase 2: Recording Plan

| Field | 内容 |
| --- | --- |
| 输入 | Dapu Event IR / legacy bridge map、take manifest draft、batch range draft、录音规则。 |
| 输出 | recording take plan、batch ranges、recording day guide、session manifest draft。XWC 产物包括 `reports/rs_xwc_002_baiya_recording_take_plan.csv` 等。 |
| canonical authority | 经人工确认的 recording plan。计划仍不是 sample asset，也不是 render input 的最终证明。 |
| human decision point | take 数量、batch 边界、context take 是否录两遍、长尾规则、retake/bad take policy。 |
| Codex task boundary | 可生成 draft 和 validation report；不得自动创建 raw audio folder、不得登记、不得切片。 |
| 允许读写路径 | `reports/*recording*` 草稿；未来生成需明确授权。 |
| 不得混入 | raw audio 处理、R0/R1 审校、sample ingest、ML。 |
| 验收标准 | 覆盖 T001-T071；`T071` 属于 `batch08 / batch_take_no=001`；T060/T071 是 context candidates，不是 atomic sample。 |

## 5. Phase 3: R0 Raw Review

| Field | 内容 |
| --- | --- |
| 输入 | raw batch WAV metadata、ASR/slate candidates、R0 draft/export candidates。 |
| 输出 | `raw_marker_review.csv`、`reviewed_slate_anchor_manifest.csv`、`split_plan_from_raw_markers.csv`，以及 active workbench draft JSON。 |
| canonical authority | active UI state: `tools/cg-varw/review_outputs/r0/drafts/{file_id}.raw_marker_review.json`。CSV 是 audit/compatibility fallback。project-side `r0_review/` 是 audit/archive mirror。 |
| human decision point | marker 是否 accepted、slate 是否匹配、wrong take 是否排除、是否进入 split planning。 |
| Codex task boundary | 修复 discovery/load 只限 R0 review usability；不得改原始音频，不得改 R1/R2/F。 |
| 允许读写路径 | R0 active workbench 和 R0 reports；本轮只读。 |
| 不得混入 | render、sample ingest、ML、把 raw root 深度改变当作无害配置。 |
| 验收标准 | `CG_VARW_RAW_ROOT` 保持 wide root `02_recordings/raw_audio`；`CG_VARW_RAW_INCLUDE_PREFIX` 仅过滤 discovery；8 个 Baiya raw WAV file_id 直连 existing draft/export。 |

## 6. Phase 4: R1 Split Review

| Field | 内容 |
| --- | --- |
| 输入 | R0 split plan、split preview manifest、clean preview metadata、R1 draft/export。 |
| 输出 | `reviewed_render_anchors.csv`、`split_marker_review.csv`、`segment_qc_sheet.csv`、R1 draft JSON。 |
| canonical authority | active UI state: `tools/cg-varw/review_outputs/r1/drafts/{batch_id}.split_review.json`。project-side `r1_review/batchXX/*` 是 validated historical reviewed outputs，不是 active save path。 |
| human decision point | segment accepted/rejected、render anchor、tail policy、context-only 标记。 |
| Codex task boundary | 可修复 review UI / CSV contract；不得把 `render_usable` 等同 sample asset。 |
| 允许读写路径 | R1 active outputs 和 reports；本轮只读。 |
| 不得混入 | 生产级 sample ingest、render、ML、重写 source raw audio。 |
| 验收标准 | batch01-batch07 各 10 takes，batch08 为 T071；`tail_policy=full_tail` 是古琴默认；显式人工 override 需保留。 |

## 7. Phase 5: R2 Render Review

| Field | 内容 |
| --- | --- |
| 输入 | ABCD render outputs、R2 latest review draft、phrase alignment、human/GPT co-review。 |
| 输出 | `r2_review_state.latest.json`、8 个 derived CSV/YAML、manifest。 |
| canonical authority | `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`。8 个 CSV/YAML 只作为 derived output。 |
| human decision point | preferred version、comment、issue_type、severity、suggested_revision、phrase boundary acceptance。 |
| Codex task boundary | audit latest first；不得用 Downloads、old exports、restore zip、browser Blob 作为 current state。 |
| 允许读写路径 | R2 latest engineering dir；本轮只读。 |
| 不得混入 | restore-from-export 作为普通 load、F/G render、R012 总重构。 |
| 验收标准 | manifest 标明 `canonical_source=r2_review_state.latest.json`、`current_page_load_source=engineering_dir_latest`、`no_downloads_policy=true`；derived export 有 guard。 |

## 8. Phase 6: ABCD Experimental Render

| Field | 内容 |
| --- | --- |
| 输入 | ABCD planning `_planning/*`、render readiness manifest、51 个 event 的 source map、version policy。 |
| 输出 | A/B/C/D wav、alignment CSV、selection decision、ABCD render report/validation。 |
| canonical authority | ABCD planning files + readiness manifest for that run；输出是 experimental render evidence。 |
| human decision point | 四版分别作为 literal/phrase/qinist_style/diagnostic 的听评候选，不自动生成 E。 |
| Codex task boundary | 只能在明确授权时执行 render；不能把 ABCD 产物变成 sample ingest。 |
| 允许读写路径 | `04_outputs/XWC/.../abcd_experimental_render/` 的 ABCD 输出；本轮只读。 |
| 不得混入 | E/F 生成、sample assets、ML、production render。 |
| 验收标准 | `experimental_render=true`、`production_grade=false`、T071 仍属于 batch08，T060/T071 context identity 正确。 |

## 9. Phase 7: E_REVIEWED

| Field | 内容 |
| --- | --- |
| 输入 | canonical latest R2 JSON、ABCD听评、suggested revisions。 |
| 输出 | `E_REVIEWED` wav/alignment/report/validation；R2 version 可接入为 playable/review_ready。 |
| canonical authority | 生成 E 时只读 engineering dir latest；E 本身是 experimental reviewed render。 |
| human decision point | E 听评是否足以进入 F；P02/P09/P10 的语义解释需保留。 |
| Codex task boundary | 不读 Downloads/old exports；不把 E 直接变 sample asset。 |
| 允许读写路径 | `E_REVIEWED/` 输出和 R2 latest future-F 元数据；本轮只读。 |
| 不得混入 | F 生成、1.5x 直接 time-stretch、sample ingest。 |
| 验收标准 | E T008-safe；`XWC_P02_N03` 不使用 `T008`，替换为 `T014`；P09 避免 context take overuse。 |

## 10. Phase 8: F_FINAL_REVIEWED

| Field | 内容 |
| --- | --- |
| 输入 | `r2_review_state.latest.json` 或其 F input snapshot；E review 中的 user preference。 |
| 输出 | `F_FINAL_REVIEWED` wav、alignment、revision plan、validation、render report、input snapshot。 |
| canonical authority | latest JSON / input snapshot sha256。 |
| human decision point | 用户人耳确认是否通过。当前结论：F 通过，记录上七九 minor issue，不生成 G/F2。 |
| Codex task boundary | 不做 production sample ingest，不触发后续训练，不改变 score facts。 |
| 允许读写路径 | `F_FINAL_REVIEWED/`；本轮只读 metadata。 |
| 不得混入 | 重做 F、G/F2、sample_assets、recording_segments、ML。 |
| 验收标准 | F playable/final_ready/alignment_available；P01-P10 coverage；`tail_policy=full_tail`；`production_grade=false`。 |

## 11. Phase 9: Human Listening Acceptance

| Field | 内容 |
| --- | --- |
| 输入 | F wav/alignment、用户听评。 |
| 输出 | 人耳验收结论和 residual issue 记录。 |
| canonical authority | 用户明确确认。 |
| human decision point | pass / conditional pass / reopen narrow issue。 |
| Codex task boundary | 记录结论，不替用户重新听、不擅自改音频。 |
| 允许读写路径 | pass record / reports；本轮只写 reports。 |
| 不得混入 | 自动 quality replay、sample ingest、production approval。 |
| 验收标准 | 明确“F通过，除了上七九的一点点小瑕疵”；minor issue 不升级为默认修复。 |

## 12. Phase 10: Sweep & Guard

| Field | 内容 |
| --- | --- |
| 输入 | 已完成任务报告、git status、diff check、script inventory。 |
| 输出 | cleanup closeout、lessons learned、script reuse audit、workflow skill design。 |
| canonical authority | 当前 HEAD + repo reports + metadata-only evidence。 |
| human decision point | 是否进入真正 skill 生成、脚本工程化、第二首小曲。 |
| Codex task boundary | 只做文档固化；不清理仓库、不处理 REVIEW/DELETE_CANDIDATE。 |
| 允许读写路径 | 本轮 4 个 `reports/*.md`。 |
| 不得混入 | archive/delete、commit、code patch、render。 |
| 验收标准 | 只新增 4 个 report；不新增真实 skill；不处理 untracked `generate_baiya_recording_plan.py`。 |

## 13. Phase 11: Next-Piece Preparation

| Field | 内容 |
| --- | --- |
| 输入 | 本 playbook、lessons、script audit、workflow skill 草案。 |
| 输出 | 第二首小曲的最小准备清单和 stop rules。 |
| canonical authority | 新曲谱面、人工确认的 score/canon/recording plan；不得复用 XWC/Baiya hardcode。 |
| human decision point | 选曲、谱面 authority、录音人、是否启用 workflow skill。 |
| Codex task boundary | 先准备，不进入第二首执行；不要一口气做完整 R012 治理。 |
| 允许读写路径 | 后续另开任务。 |
| 不得混入 | 直接跑 XWC 脚本、直接生成 render、直接 sample ingest。 |
| 验收标准 | 新曲有谱面输入、canon/parser gate、recording plan gate、script parameterization plan。 |

## 14. 第二首复用与必须重新人工确认

可复用：

- 阶段边界：Score/Dapu -> Recording Plan -> R0 -> R1 -> R2 -> ABCD -> E -> F -> listening acceptance -> sweep。
- authority gate：R2 latest JSON canonical，CSV/YAML derived；Downloads/restore zip/browser Blob forbidden。
- R0 root/scope rule：identity root 与 discovery prefix 分离。
- tail policy guard：古琴默认 `full_tail` / natural decay，smart fade 只能显式 override。
- T008 类事故处理方法：wrong take 标记、replacement provenance、validation guard。
- reports 结构：每个阶段保留输入、输出、authority、人审点、禁写声明。

必须重新人工确认：

- 曲目、session、performer、recording_id、piece_id。
- 新谱面的 score facts、未知谱字、指法语义和 canon evidence。
- Dapu parser 输出与 recording items 覆盖。
- recording plan 的 take 数量、batch range、context takes、long-tail rules。
- R0/R1 的 accepted/rejected 人审结论。
- R2 preferred versions 和每句听评。
- ABCD/E/F 的实际听感，不得套用 XWC 的 P01/P02/P09 timing 语义。
- 是否允许生成 E/F、是否允许后续 sample ingest。

## 15. 下一步建议

建议下一步可以进入真正 `cyber_guqin_mvp_workflow` skill 文件生成，但仍应只生成 skill 文档，不运行第二首。再下一步才进入脚本工程化，把 XWC/Baiya hardcode 拆出参数化配置。最后再进入第二首小曲验证，并以 Track A 的最小闭环验证为主。
