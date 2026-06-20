# CG-VARW R2 E Intake / T008-safe / R0 Load / F Slot 报告 v0.1

## 1. 任务边界

本次任务只做 `E_REVIEWED` 的 T008 安全修复与 R2 接入、`F_FINAL_REVIEWED` pending 槽位预留、R0 初始状态恢复链路修复。

未生成 `F_FINAL_REVIEWED.wav`，未生成 `E2_FAST_1P5`，未根据“1.5 倍速”直接重渲染 E，未恢复浏览器 Downloads，未增加 R2 底部按钮，未写 sample ingest 文件。

## 2. T008 审计结论

当前原始 E 审计发现：`E_REVIEWED/render_event_alignment.E_REVIEWED.csv` 曾在 `XWC_P02_N03` 使用 `T008`。

T008 的原始标注目标为“散挑六” / `SAN_TIAO_6`，但实际白牙演奏为“散挑七”。用户已将 T008 置为排除单元，因此不能继续作为 E 的听评音频来源。

处理结果：

- 原始 E 已归档到 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/E_REVIEWED_ORIGINAL_BEFORE_T008_FIX/`。
- 当前 `E_REVIEWED` 已将 `XWC_P02_N03` 从 `T008` 替换为 `T014`。
- `T014` 来源为白牙 `batch02` exact `SAN_TIAO_6` / “散挑六”，符合替代优先级 a：白牙其它 exact “散 + 挑 + 六弦”。
- 当前 E alignment 中没有 `source_take_id=T008`，也没有 `T008_clean_preview.wav` 作为 source audio。
- alignment flags 已写入 `t008_excluded=true`、`t008_safe_replacement=T014`、`replacement_priority=exact_baiya_san_tiao_6`。

E wav hash：

- 原始归档 E：`2e5b2b545e0b54e3d5a937a6e7bef45f4b20ad2d7dc2882a7dde1280f0bd3d6c`
- 当前 T008-safe E：`2b0e4271928e4af71c57df2f70efb8300f42caf9e93797cdfbb6868b2fce752a`

当前 E wav：

- duration：`122.857800s`
- sample rate：`44100`
- channels：`2`
- bit depth：`24-bit`

## 3. E 接入 R2

R2 render set API 的版本列表现在包含：

- `A_LITERAL`
- `B_PHRASE`
- `C_QINIST_STYLE`
- `D_TEACHING_DIAGNOSTIC`
- `E_REVIEWED`
- `F_FINAL_REVIEWED`

其中 `E_REVIEWED`：

- `status=review_ready`
- `playable=true`
- `alignment_available=true`
- audio 指向当前 T008-safe `XWC_BAIYA_E_REVIEWED.wav`
- phrase alignment 从 `render_event_alignment.E_REVIEWED.csv` 聚合为 P01-P10 共 10 行
- 可填写 comment / issue_type / severity / suggested_revision
- 可保存到 R2 latest draft
- 不覆盖 A/B/C/D 旧听评

R2 导出的 `render_phrase_alignment.csv` 与 `phrase_boundary_decision.csv` 现在预期为 50 行：A/B/C/D 共 40 行，E 共 10 行，F 无 alignment。

## 4. F pending slot

`F_FINAL_REVIEWED` 当前只作为 R2 UI/API 槽位显示：

- `status=pending`
- `playable=false`
- `audio_path=""`
- `audio_url` 不生成
- `alignment_available=false`
- `source=future_from_e_review`
- `generation_allowed=false`

用户点击 F 时，页面提示：

`F_FINAL_REVIEWED 尚未生成，请先完成 E_REVIEWED 听评。`

F 不参与播放队列，不参与 preferred 默认选择，不生成 review draft，不生成 wav，不生成 alignment。

## 5. E 听评进入未来 F

R2 latest draft / export 兼容 E 的听评记录。未来 F 的输入来源为：

- `E_REVIEWED` 的 user comment
- `E_REVIEWED` 的 issue_type
- `E_REVIEWED` 的 severity
- `E_REVIEWED` 的 suggested_revision
- `E_REVIEWED` 的 preferred / rejected 评价

本次新增 future-F 元数据：

- `f_generation_pending=true`
- `f_input_source=E_REVIEWED_USER_REVIEW`
- `f_not_generated=true`

例如用户在 E 听评中写入“整体建议调整为 1.5 倍速”，本任务只会保存为未来 F 的 `tempo_policy` 输入依据，不会直接生成 E2 或 F。

## 6. R0 初始状态加载根因与修复

根因：

R0 页面通过 `/api/r0/raw-files/{file_id}/review-units` 调用 `load_or_build_review_units()`。原逻辑只有：

1. project draft
2. ASR candidates / raw manifest
3. manual empty

缺失“没有 draft 但已有 exported CSV / saved annotations”时的恢复层。因此一旦 draft 缺失，页面会退回 raw/ASR 初始态，导致追溯复盘不方便。

修复后加载优先级：

1. project draft：`review_outputs/r0/drafts/{file_id}.raw_marker_review.json`
2. exported CSV：`review_outputs/r0/exports/{file_id}/raw_marker_review.csv`
3. raw manifest / ASR candidates
4. manual empty

CSV 恢复会重建 `ReviewUnit`、markers、marker source、review_status、unit_status、nudge、notes 与 provenance 字段。该修复只读，不覆盖已有 draft，不清空 R0 标注，不写 Downloads，不改 R1/R2 保存导出逻辑。

## 7. 未改范围确认

- 未修改 R2 保存 draft / 导出 CSV 的按钮数量和底部按钮结构。
- 未恢复浏览器下载逻辑。
- 未生成 F wav / F alignment。
- 未重渲染 A/B/C/D。
- 未写 `03_samples/sample_assets.csv`。
- 未写 `03_samples/recording_segments.csv`。
- 未创建 `recording_items_enriched.jsonl`。
- 未训练 ML。
- 未修改 score_events / gesture_templates / canon / sources。
- 未修改 raw master / R0/R1 archive。
- 未清空 R2 latest draft。

## 8. 验证摘要

已执行并通过：

- backend targeted tests：R2 E intake、F pending slot、R2 draft/export、R0 CSV fallback。
- backend full unittest：20 tests passed。
- backend compileall。
- frontend `npm run typecheck`。
- frontend `npm run build`。
- 当前 E T008 source 审计：`source_take_id=T008` 数量为 0。
- 当前 E wav：存在，`44100Hz` / `24-bit` / stereo，时长 `122.857800s`。
- A/B/C/D wav hash 已记录，未被本次重写。
- R2 API smoke：versions=6，alignments=50，E playable，F pending / no audio / no alignment。
- 浏览器交互烟测限制：本地 Vite 服务可启动并返回页面 HTML，但 in-app browser 控制工具在当前环境返回 sandbox metadata 错误，未能执行真实点击；F 点击提示由组件逻辑和 API 状态覆盖，仍需用户在浏览器中做最终可视验收。

完整最终验证见本任务提交前命令输出。

## 9. 用户下一步验收

1. 启动 cg-varw backend/frontend。
2. 打开 R2 页面。
3. 在版本列表中确认可见 A/B/C/D/E/F。
4. 播放 `E_REVIEWED`，重点复听 P02 的 `XWC_P02_N03` 是否已避开错误 T008。
5. 点击 `F_FINAL_REVIEWED`，确认只提示待生成，不播放、不报错。
6. 在 E 上填写听评，例如“整体建议调整为 1.5 倍速”，保存 draft。
7. 导出 CSV，确认不触发 Downloads，工程目录 latest 中保留 E 听评与 future-F pending 元数据。
8. 打开 R0，确认如存在 draft 或 exported CSV，页面不是空白初始态，刷新后仍可恢复。
