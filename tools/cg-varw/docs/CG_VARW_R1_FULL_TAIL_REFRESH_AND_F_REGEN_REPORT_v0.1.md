# CG-VARW R1 full_tail 刷新与 F_FINAL_REVIEWED 复生成报告 v0.1

## 结论

本任务将白牙 `RS_XWC_002_BAIYA_PILOT` 的 R1 注册 tail policy 从 `smart_fade_100ms` 刷新为 `full_tail`，从 raw/split manifest 重新写出 T-previewer 音频，并在不新增 G/F2 的前提下复生成同名 `F_FINAL_REVIEWED`。

## 为什么改为 full_tail

用户验收指出旧 F 基本通过，但尾音存在截断感。古琴尾音轻、长，和下一个音自然叠合时不一定造成明显堆叠，因此本轮不再以 smart fade 作为主要尾音策略；只保留自然衰减，允许轻尾自然混合。

## R1 刷新范围

- R1 注册范围：T001-T071。
- 刷新前 R1 registry `smart_fade_100ms` 行数：71。
- 刷新后目标 tail_policy：`full_tail`。
- R1 changed_rows：71（以 git HEAD / 初始刷新前状态计；后续复跑时脚本复用归档，因此运行态计数可能为 0）。
- T008：F source 仍不使用 T008；`XWC_P02_N03` 继续使用 T014。
- full_tail preview：71 个 preview 从 raw/split manifest 重新写出。
- preview hash 结果：clean/unit preview 重写后 hash 未变化，说明现有 T-previewer 音频本身已等同 raw full_tail slice；旧 F 尾音截断来自 F 混音阶段的 `safe_trim_smart_fade`，不是继续复用 destructive smart-faded preview。
- 无法恢复完整 tail：0。

## 旧 F 归档

- 归档路径：`/Users/chenyulin/Documents/AIProjects/cyber_guqin/04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX`
- 旧 F sha256：`88096718ffaca3b6a1ec6a54e0a113f220118551c0819987d2f58b4d6a1b1ee1`
- 旧 F 时长：82.255011s
- 旧 F tempo ratio：1.4936208561064728

## 新 F

- 新 F sha256：`cc522c94f4e1db2ca23a07c85a1f4c25f72112a2a51379a0506754ce091a8aa8`
- 新 F wav：84.708005s，44100 Hz，24 bit。
- 新 F tempo ratio：1.4503682518284098
- 新 F 仍保持原 F attack timeline 与约 1.5 倍速策略，只将 source preview / tail policy 切换为 full_tail。
- P01/P06-P09 仍为 N03->N04；P02-P05 仍为 N05->N06。
- P02_N03：T014。
- source_take_id 不含 T008：True.
- smart_fade_applied：False.
- tail_trimmed_event_count：0.

## R2 与导出同步

- R2 版本仍为 A/B/C/D/E/F，不新增 G/F2。
- `preferredVersionByPhrase` 仍为 F。
- `render_phrase_alignment.csv`：60 行。
- `phrase_boundary_decision.csv`：60 行。
- 8 个 CSV/YAML 从 canonical latest state 重新派生。
- 未恢复 Downloads、Blob 或 `a.download`。
- 未修改 R2 按钮。
- 未重做 A/B/C/D/E。

## R0 遗留问题

`LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED`：用户已验证 R0 仍未加载出口播标记。本任务不处理 R0；F full_tail 修复后再单独开 R0 recovery/audit。

## 用户验收

请打开 R2，选择 `F_FINAL_REVIEWED`，重点听 P01/P06-P09 的 N03->N04、P02-P05 的 N05->N06，以及每句 cadence/final note 的自然尾音。预期是节奏与旧 F 一致，但尾音不再有明显截断。
