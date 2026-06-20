# XWC 白牙 F_FINAL_REVIEWED 生成报告

- 唯一权威输入：`/Users/chenyulin/Documents/AIProjects/cyber_guqin/04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json`
- latest JSON sha256：`94b1a58ef43eeb9864671bd2bf6457d65a26298f87a29014bfbfca30499ea885`
- E_REVIEWED 用户听评数量：10
- F 解释：E_REVIEWED 整体方向可用；全曲略散漫，因此基于 E 的 attack timeline 约 1.5 倍提速，不做整段 wav time-stretch；本次使用 full_tail source preview，不再以 smart fade 作为主要尾音策略。
- P01 类：P01/P06/P07/P08/P09 收紧 N03 -> N04。
- P02 类：P02/P03/P04/P05 收紧 N05 -> N06。
- P09：仅继承 P01 类 timing 修订，不绑定 T008。
- T008-safe：继承 E 的 XWC_P02_N03=T014 exact SAN_TIAO_6，F 不使用 T008。
- F wav：84.708005s，44100 Hz，24 bit。
- 尾音策略：source_tail_policy=full_tail，smart_fade_applied=false，tail_trimmed_event_count=0。
- 速度比例：E 122.857800s / F 84.708005s = 1.450368，接近 1.5 倍。
- R2 接入：F_FINAL_REVIEWED 已由后端从 F 输出目录识别为 playable/final_ready/alignment_available。
- preferredVersionByPhrase：P01-P10 已切换为 F_FINAL_REVIEWED。
- 8 个 CSV/YAML：已从 latest JSON/canonical state 重新派生，不使用旧 exports。
- render_phrase_alignment.csv：60 行；phrase_boundary_decision.csv：60 行。
- Downloads：未触发；未使用 Blob / a.download。
- R2 按钮：未重构，仍为保存 draft / 导出 CSV。
- R0：未修复、未改代码。

## R0 遗留问题

`LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED`

f334880 曾将 R0 加载优先级改为 draft -> exported CSV -> ASR/raw -> empty；用户手动验证后仍未加载出口播标记。当前不确定原因包括：R0 draft/export CSV 本地已丢失、路径不一致、file_id 不一致、CSV fallback 未匹配当前 raw file、前端仍未调用修复后的 API。该问题不阻塞 F-final，F-final 后应单独开启 R0 recovery/audit 任务；本任务不得修改 R0。

## 用户验收

1. 启动 R2 后端并打开 R2 页面。
2. 确认版本列表为 A/B/C/D/E/F。
3. 选择 F_FINAL_REVIEWED，确认可播放并可按 P01-P10 分句播放。
4. 重点听 P01/P06-P09 的 N03->N04、P02-P05 的 N05->N06、全曲约 1.5 倍速，以及 P02_N03 未回退 T008。
