# Baiya Recording Day Guide Draft

Status: draft pending user review. 本文件不是录音登记，不创建 raw audio folder，不进入切片。

## 1. 录音前准备

- 确认录音人是 `QINIST_002 = 白牙`，不要覆盖 `QINIST_001 = 三曼`。
- 确认本轮是 `RS_XWC_002_BAIYA_PILOT` MVP reshoot pilot，`production_grade=false`。
- 录音前先通读 batch draft，特别确认 T060/T071 这类 context take。

## 2. 设备建议

- 使用稳定录音设备和固定麦克风位置。
- 全 session 期间不要移动麦克风、琴、椅子和主要吸音布置。
- 避免自动增益、强降噪、动态压缩和过度限幅。

## 3. WAV 参数

- 优先 WAV，48kHz / 24-bit。
- 不再使用 M4A/AAC 作为 production-like source。
- 本轮仍是 MVP reshoot raw，非正式 production sample library。

## 4. Room Noise

- 每个 batch 开始前保留数秒房间底噪。
- 避免风扇、键盘、手机震动和椅子声。

## 5. Session 前后调弦参考音

- session 开始前录一段空弦参考音。
- session 结束后再录一段空弦参考音。
- 若中途明显走音，停下重新调弦并口播说明，不删除旧 take。

## 6. 麦克风位置不要中途改变

- 如果必须调整，口播说明并从下一 batch 开始记录为新的设备状态。
- 不要在同一 batch 中途悄悄移动麦克风。

## 7. 每条怎么录

每条 take 固定结构：

```text
spoken slate number
-> at least 0.8 seconds silence
-> guqin performance
-> full natural tail decay
-> at least 1.2 seconds silence
-> next spoken slate
```

中文执行口令：先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。

普通 take：尾音自然结束后至少 1.2 秒再报下一条。

长尾 / 滑音 / 撞 / context / 复合泛音 take：尾音自然结束后至少 2.5 秒再报下一条；T052/T053/T057/T058/T060/T070/T071 必须使用 2.5 秒规则。如果单条 instruction 和通用提醒冲突，以更长的 2.5 秒为准。

T060/T071 是同一 transition 的两条 context references，event_range 均为 `XWC_P09_N01_to_N02`；录两遍用于后续择优，不是编号错误，也不要把 context take 当作 atomic sample 的直接替代。

## 8. Retake 怎么处理

- 不停机删除。
- 直接说“零零幺 retake 2”或“零零幺 retake 3”。
- 重新弹。
- 所有 retake 后续进入 manifest，由用户审核后决定采用。

## 9. Bad Take 怎么处理

- 不删除。
- 可以口播“bad take”或“保留，不采用”。
- 后续 manifest 标记质量，不在录音当天剪掉。

## 10. Batch 文件怎么命名

- `RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`
- `RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav`
- `RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav`
- `RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.wav`
- `RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.wav`
- `RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.wav`
- `RS_XWC_002_BAIYA_PILOT_batch07_T061-T071.wav`

## 11. 录完后怎么交付

- 交付原始 WAV batch 文件。
- 保持文件名和 batch range 一致。
- 同时告知是否有 retake、bad take、设备变化或中途调弦。

## 12. 录完后不要做什么

- 不剪 raw audio。
- 不覆盖 raw audio。
- 不删除 bad take 或 retake。
- 不导出 M4A/AAC 作为 production-like source。
- 不创建 `03_samples`、`sample_assets`、`recording_items_enriched`。
- 不进入录音登记或切片，直到用户审核通过。
