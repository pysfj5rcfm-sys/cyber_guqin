# CG-VARW R2 F_FINAL_REVIEWED 生成与导出同步报告 v0.1

任务名称：`CG-VARW_R2_GENERATE_F_FINAL_REVIEWED_FROM_E_REVIEW`

阶段：`Phase 1F-XWC-F_FINAL_REVIEWED`

## 1. 唯一权威输入

本次 F 生成只使用：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`

输入快照已保存到：

- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.json`
- `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/input_snapshot/r2_review_state.latest.input_for_f.sha256`

latest JSON sha256：

`d26eade164c967eb2b053c6a1582d083f2d0d72e4a22fb3852d0781a0aa0670c`

未使用旧 8 个 CSV/YAML、`r2_review_exports/`、Downloads、archive 或 restore zip 作为 F 主输入。

## 2. latest JSON 前置校验

- E_REVIEWED 听评数量：10 条。
- `preferredVersionByPhrase`：P01-P10 均为 `E_REVIEWED`。
- F 前置标志：`f_generation_pending=true`、`f_input_source=E_REVIEWED_USER_REVIEW`、`f_not_generated=true`。
- `phrase_alignments`：生成前为 A/B/C/D/E 共 50 条，E 覆盖 P01-P10。
- E_REVIEWED wav 与 alignment 存在。
- 当前 E_REVIEWED source 不使用 T008；`XWC_P02_N03` 使用 T014。

## 3. 用户 E 听评解释

F 解释为：E_REVIEWED 整体方向可用，但全曲整体略散漫；用户明确要求“全曲建议统一提速，听评1.5倍速正好”。因此 F 基于 E 的 `render_event_alignment` / attack timeline 重新生成，不做整段 wav time-stretch。

- P01 类：P01/P06/P07/P08/P09 收紧 N03 -> N04，不粗暴截断末音。
- P02 类：P02/P03/P04/P05 收紧 N05 -> N06，不粗暴砍尾。
- P09：E 听评“同第1句”解释为 P01 类 timing 修订，不绑定 T008-safe。
- T008-safe：仅作为全局 sample safety guard；F 继承 E 的 `XWC_P02_N03=T014`，不回退 T008，不以散挑七冒充散挑六。

## 4. F 输出

输出目录：

`04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED/`

已生成：

- `XWC_BAIYA_F_FINAL_REVIEWED.wav`
- `render_event_alignment.F_FINAL_REVIEWED.csv`
- `f_revision_plan.yaml`
- `f_final_render_report.md`
- `f_final_validation.json`
- `input_snapshot/r2_review_state.latest.input_for_f.json`
- `input_snapshot/r2_review_state.latest.input_for_f.sha256`

F wav 元数据：

- 时长：82.255011s。
- 采样率：44100 Hz。
- 位深：24 bit。
- 声道：2。
- E 时长：122.857800s。
- 速度比例：122.857800 / 82.255011 = 1.493621，接近 1.5 倍；因保留尾部余量略偏离目标 81.905200s。

F 标志：

- `experimental_render=true`
- `production_grade=false`
- `final_reviewed_for_current_iteration=true`

## 5. R2 接入

F 生成后，R2 后端已从 `F_FINAL_REVIEWED/` 输出目录识别：

- `version_id=F_FINAL_REVIEWED`
- `status=final_ready`
- `playable=true`
- `alignment_available=true`
- audio 指向 `XWC_BAIYA_F_FINAL_REVIEWED.wav`
- phrase alignment 覆盖 P01-P10

R2 版本列表为：

1. `A_LITERAL`
2. `B_PHRASE`
3. `C_QINIST_STYLE`
4. `D_TEACHING_DIAGNOSTIC`
5. `E_REVIEWED`
6. `F_FINAL_REVIEWED`

F 未覆盖 E 的用户听评；latest JSON 保留 E_REVIEWED 10 条用户听评及既有 ABCD 听评。F 已成为新的 preferred version。

## 6. latest JSON 更新

F 生成后 latest JSON 已更新：

- `f_generation_pending=false`
- `f_not_generated=false`
- `f_generation_completed=true`
- `f_input_source=E_REVIEWED_USER_REVIEW`
- `f_generated_from_latest_json_sha256=d26eade164c967eb2b053c6a1582d083f2d0d72e4a22fb3852d0781a0aa0670c`
- `f_version_id=F_FINAL_REVIEWED`
- `preferredVersionByPhrase` 中 P01-P10 全部为 `F_FINAL_REVIEWED`
- `phrase_alignments` 为 A/B/C/D/E/F 共 60 条

## 7. 8 个 CSV/YAML 导出同步

本次修复了 F 后导出会把 state 打回 pending 的问题：

- 后端 `export_project_review_draft_csv()` 现在从 latest JSON / canonical state 重新派生 8 文件。
- F completed 状态会保留，不再被硬编码 pending flags 覆盖。
- R2 前端保存/导出 payload 也改为根据 F 是否 playable 动态写入 F flags。
- 未恢复浏览器 Downloads、Blob 或 `a.download`。
- R2 底部按钮未重构，仍为“保存 draft / 导出 CSV”。

latest 8 文件当前状态：

- `render_phrase_alignment.csv`：60 行。
- `phrase_boundary_decision.csv`：60 行。
- `preferred_version_summary.csv`：10 行，P01-P10 均为 `F_FINAL_REVIEWED`。
- `listening_review.csv` / `listening_review.yaml`：保留 ABCD 与 E 听评，并新增 F 生成记录。
- `render_revision_log.yaml`：包含 E -> F 修订来源。
- `issue_list.csv`：包含全曲略散漫 / 1.5 倍速、P01 类 N03->N04、P02 类 N05->N06、T008 不得回退。
- `phrase_structure_review.yaml`：保留 10 句结构，并带 F 已生成 flags。

## 8. marker / boundary 校验

F 生成以 E 的 `render_event_alignment` 和 `phrase_alignments` 为准，未盲信可能乱序的 `markersByKey`。

`f_final_validation.json` 中 marker order 校验通过：

`section_start <= phrase_start <= breath_point <= cadence <= phrase_end <= section_end`

覆盖 P01-P10，失败列表为空。

## 9. R0 遗留问题

`LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED`

f334880 曾将 R0 加载优先级改为 draft -> exported CSV -> ASR/raw -> empty。用户手动验证后仍未加载出口播标记。

当前不确定原因包括：

- R0 draft/export CSV 本地已丢失；
- 路径不一致；
- `file_id` 不一致；
- CSV fallback 未匹配当前 raw file；
- 前端仍未调用修复后的 API。

该问题不阻塞 F-final；F-final 后应单独开启 R0 recovery/audit 任务。本任务未修改 R0。

## 10. 验证摘要

已完成的关键验证：

- latest JSON parse / E review extraction / input snapshot sha256。
- F revision plan parse。
- F wav 生成与 wav metadata 校验。
- F alignment parse，P01-P10 coverage。
- T008 exclusion：当前 source 不使用 T008；`XWC_P02_N03=T014`。
- P09 不误标 T008-safe。
- tempo ratio：1.493621。
- marker order validation：通过。
- R2 HTTP smoke：versions=6，F playable=true，F alignment_available=true，F audio endpoint 200 `audio/wav`。
- 8 CSV/YAML derive check：通过。
- `render_phrase_alignment.csv=60`，`phrase_boundary_decision.csv=60`。
- preferred summary P01-P10 = F。
- grep 确认未恢复 browser download / Blob / `a.download`。
- A/B/C/D/E wav 与 alignment sha256 复核未变化。
- 禁写路径检查：`03_samples/sample_assets.csv`、`03_samples/recording_segments.csv`、`recording_items_enriched.jsonl` 未改动。
- R0 文件未改。

## 11. 用户验收建议

1. 启动 R2 后端并打开 R2 页面。
2. 确认版本列表显示 A/B/C/D/E/F。
3. 选择 `F_FINAL_REVIEWED`，确认可全曲播放与按 P01-P10 分句播放。
4. 重点验收：全曲是否约 1.5 倍速；P01/P06-P09 的 N03->N04 是否更紧；P02-P05 的 N05->N06 是否更紧；P02_N03 是否未回退 T008；P09 是否没有 context take 重复问题。
