# RS_XWC_002_BAIYA_PILOT Recording Batch Draft

Status: draft pending user review. 生成后等待用户审核；不得自动创建 raw audio folder；不得进入录音登记；不得进入切片。

Performer: `QINIST_002 = 白牙`

Core rule for normal takes: 先报号 -> 停 0.8 秒 -> 再弹 -> 弹完等尾音自然结束 -> 再停 1.2 秒 -> 再进入下一条。

Long-tail rule: 长尾 / 滑音 / 撞 / context / 复合泛音 take 在尾音自然结束后至少停 2.5 秒；若单条 instruction 与通用提醒冲突，以 2.5 秒为准。

Context note: T060/T071 是同一 transition 的两条 context references，event_range 均为 XWC_P09_N01_to_N02；录两遍用于后续择优，不是编号错误，也不要把 context take 当作 atomic sample 的直接替代。

Retake rule: 不停机删除；直接说本条编号加 retake 2 / retake 3；重新弹；坏 take 保留。

Source note: this draft uses the legacy XWC 71-task bridge for Baiya reshoot only. It is not a future source of truth and is not Dapu Event IR ingest.

## batch01 T001-T010

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch01_T001-T010.wav`

### T001 / slate 001

- 指法 / normalized_name: `散挑七`
- gesture_id: `SAN_TIAO_7`
- event: `XWC_P01_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑七弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零幺`
- ASR 兼容读法: `零零幺;零零一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T002 / slate 002

- 指法 / normalized_name: `散勾五`
- gesture_id: `SAN_GOU_5`
- event: `XWC_P01_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音勾五弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零二`
- ASR 兼容读法: `零零二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T003 / slate 003

- 指法 / normalized_name: `散挑七`
- gesture_id: `SAN_TIAO_7`
- event: `XWC_P01_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑七弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零三`
- ASR 兼容读法: `零零三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T004 / slate 004

- 指法 / normalized_name: `名十勾五`
- gesture_id: `AN_RING_10_GOU_5`
- event: `XWC_P01_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指按十徽，勾五弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零四`
- ASR 兼容读法: `零零四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T005 / slate 005

- 指法 / normalized_name: `名十勾五`
- gesture_id: `AN_RING_10_GOU_5`
- event: `XWC_P01_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指十徽勾五弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零零五`
- ASR 兼容读法: `零零五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T006 / slate 006

- 指法 / normalized_name: `散挑七`
- gesture_id: `SAN_TIAO_7`
- event: `XWC_P02_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑七弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零六`
- ASR 兼容读法: `零零六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T007 / slate 007

- 指法 / normalized_name: `散勾五`
- gesture_id: `SAN_GOU_5`
- event: `XWC_P02_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音勾五弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零七`
- ASR 兼容读法: `零零七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T008 / slate 008

- 指法 / normalized_name: `散挑六`
- gesture_id: `SAN_TIAO_6`
- event: `XWC_P02_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑六弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零八`
- ASR 兼容读法: `零零八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T009 / slate 009

- 指法 / normalized_name: `名十勾四`
- gesture_id: `AN_RING_10_GOU_4`
- event: `XWC_P02_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指按十徽，勾四弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零零九`
- ASR 兼容读法: `零零九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T010 / slate 010

- 指法 / normalized_name: `名十勾四`
- gesture_id: `AN_RING_10_GOU_4`
- event: `XWC_P02_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指十徽勾四弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零幺零`
- ASR 兼容读法: `零幺零;零一零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

## batch02 T011-T020

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch02_T011-T020.wav`

### T011 / slate 011

- 指法 / normalized_name: `散挑七`
- gesture_id: `SAN_TIAO_7`
- event: `XWC_P02_N05` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑七弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺幺`
- ASR 兼容读法: `零幺幺;零一一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T012 / slate 012

- 指法 / normalized_name: `大九勾四`
- gesture_id: `AN_THUMB_9_GOU_4`
- event: `XWC_P02_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾四弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺二`
- ASR 兼容读法: `零幺二;零一二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T013 / slate 013

- 指法 / normalized_name: `大九勾四`
- gesture_id: `AN_THUMB_9_GOU_4`
- event: `XWC_P02_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾四弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零幺三`
- ASR 兼容读法: `零幺三;零一三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T014 / slate 014

- 指法 / normalized_name: `散挑六`
- gesture_id: `SAN_TIAO_6`
- event: `XWC_P03_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑六弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺四`
- ASR 兼容读法: `零幺四;零一四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T015 / slate 015

- 指法 / normalized_name: `散勾四`
- gesture_id: `SAN_GOU_4`
- event: `XWC_P03_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音勾四弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺五`
- ASR 兼容读法: `零幺五;零一五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T016 / slate 016

- 指法 / normalized_name: `散挑五`
- gesture_id: `SAN_TIAO_5`
- event: `XWC_P03_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑五弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺六`
- ASR 兼容读法: `零幺六;零一六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T017 / slate 017

- 指法 / normalized_name: `名十徽八勾三`
- gesture_id: `AN_RING_10_8_GOU_3`
- event: `XWC_P03_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指按十徽八，勾三弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺七`
- ASR 兼容读法: `零幺七;零一七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T018 / slate 018

- 指法 / normalized_name: `名十徽八勾三`
- gesture_id: `AN_RING_10_8_GOU_3`
- event: `XWC_P03_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指十徽八勾三弦，录注按版本，注为谱面明示动作，保留余音
- realization_variant: `zhu`; realization_pre_action: `zhu`; take label: pre=zhu
- 口播: `零幺八`
- ASR 兼容读法: `零幺八;零一八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T019 / slate 019

- 指法 / normalized_name: `散挑六`
- gesture_id: `SAN_TIAO_6`
- event: `XWC_P03_N05` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑六弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零幺九`
- ASR 兼容读法: `零幺九;零一九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T020 / slate 020

- 指法 / normalized_name: `大九勾三`
- gesture_id: `AN_THUMB_9_GOU_3`
- event: `XWC_P03_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾三弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二零`
- ASR 兼容读法: `零二零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

## batch03 T021-T030

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch03_T021-T030.wav`

### T021 / slate 021

- 指法 / normalized_name: `大九勾三`
- gesture_id: `AN_THUMB_9_GOU_3`
- event: `XWC_P03_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾三弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零二幺`
- ASR 兼容读法: `零二幺;零二一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T022 / slate 022

- 指法 / normalized_name: `散挑五`
- gesture_id: `SAN_TIAO_5`
- event: `XWC_P04_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑五弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二二`
- ASR 兼容读法: `零二二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T023 / slate 023

- 指法 / normalized_name: `散勾三`
- gesture_id: `SAN_GOU_3`
- event: `XWC_P04_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音勾三弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二三`
- ASR 兼容读法: `零二三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T024 / slate 024

- 指法 / normalized_name: `散挑四`
- gesture_id: `SAN_TIAO_4`
- event: `XWC_P04_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑四弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二四`
- ASR 兼容读法: `零二四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T025 / slate 025

- 指法 / normalized_name: `名十勾二`
- gesture_id: `AN_RING_10_GOU_2`
- event: `XWC_P04_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指按十徽，勾二弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二五`
- ASR 兼容读法: `零二五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T026 / slate 026

- 指法 / normalized_name: `名十勾二`
- gesture_id: `AN_RING_10_GOU_2`
- event: `XWC_P04_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指十徽勾二弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零二六`
- ASR 兼容读法: `零二六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T027 / slate 027

- 指法 / normalized_name: `散挑五`
- gesture_id: `SAN_TIAO_5`
- event: `XWC_P04_N05` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑五弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二七`
- ASR 兼容读法: `零二七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T028 / slate 028

- 指法 / normalized_name: `大九勾二`
- gesture_id: `AN_THUMB_9_GOU_2`
- event: `XWC_P04_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾二弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零二八`
- ASR 兼容读法: `零二八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T029 / slate 029

- 指法 / normalized_name: `大九勾二`
- gesture_id: `AN_THUMB_9_GOU_2`
- event: `XWC_P04_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾二弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零二九`
- ASR 兼容读法: `零二九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T030 / slate 030

- 指法 / normalized_name: `散挑四`
- gesture_id: `SAN_TIAO_4`
- event: `XWC_P05_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑四弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三零`
- ASR 兼容读法: `零三零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

## batch04 T031-T040

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch04_T031-T040.wav`

### T031 / slate 031

- 指法 / normalized_name: `散勾二`
- gesture_id: `SAN_GOU_2`
- event: `XWC_P05_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音勾二弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三幺`
- ASR 兼容读法: `零三幺;零三一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T032 / slate 032

- 指法 / normalized_name: `散挑三`
- gesture_id: `SAN_TIAO_3`
- event: `XWC_P05_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑三弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三二`
- ASR 兼容读法: `零三二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T033 / slate 033

- 指法 / normalized_name: `名十勾一`
- gesture_id: `AN_RING_10_GOU_1`
- event: `XWC_P05_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指按十徽，勾一弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三三`
- ASR 兼容读法: `零三三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T034 / slate 034

- 指法 / normalized_name: `名十勾一`
- gesture_id: `AN_RING_10_GOU_1`
- event: `XWC_P05_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指十徽勾一弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零三四`
- ASR 兼容读法: `零三四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T035 / slate 035

- 指法 / normalized_name: `散挑四`
- gesture_id: `SAN_TIAO_4`
- event: `XWC_P05_N05` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑四弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三五`
- ASR 兼容读法: `零三五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T036 / slate 036

- 指法 / normalized_name: `大九勾一`
- gesture_id: `AN_THUMB_9_GOU_1`
- event: `XWC_P05_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾一弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三六`
- ASR 兼容读法: `零三六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T037 / slate 037

- 指法 / normalized_name: `大九勾一`
- gesture_id: `AN_THUMB_9_GOU_1`
- event: `XWC_P05_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾一弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零三七`
- ASR 兼容读法: `零三七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T038 / slate 038

- 指法 / normalized_name: `散挑四`
- gesture_id: `SAN_TIAO_4`
- event: `XWC_P06_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑四弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三八`
- ASR 兼容读法: `零三八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T039 / slate 039

- 指法 / normalized_name: `大九勾一`
- gesture_id: `AN_THUMB_9_GOU_1`
- event: `XWC_P06_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾一弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零三九`
- ASR 兼容读法: `零三九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T040 / slate 040

- 指法 / normalized_name: `大九勾一`
- gesture_id: `AN_THUMB_9_GOU_1`
- event: `XWC_P06_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾一弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零四零`
- ASR 兼容读法: `零四零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

## batch05 T041-T050

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch05_T041-T050.wav`

### T041 / slate 041

- 指法 / normalized_name: `散挑五`
- gesture_id: `SAN_TIAO_5`
- event: `XWC_P06_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑五弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零四幺`
- ASR 兼容读法: `零四幺;零四一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T042 / slate 042

- 指法 / normalized_name: `大九勾二`
- gesture_id: `AN_THUMB_9_GOU_2`
- event: `XWC_P06_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾二弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零四二`
- ASR 兼容读法: `零四二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T043 / slate 043

- 指法 / normalized_name: `大九勾二`
- gesture_id: `AN_THUMB_9_GOU_2`
- event: `XWC_P06_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾二弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零四三`
- ASR 兼容读法: `零四三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T044 / slate 044

- 指法 / normalized_name: `散挑六`
- gesture_id: `SAN_TIAO_6`
- event: `XWC_P07_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑六弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零四四`
- ASR 兼容读法: `零四四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T045 / slate 045

- 指法 / normalized_name: `大九勾三`
- gesture_id: `AN_THUMB_9_GOU_3`
- event: `XWC_P07_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾三弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零四五`
- ASR 兼容读法: `零四五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T046 / slate 046

- 指法 / normalized_name: `大九勾三`
- gesture_id: `AN_THUMB_9_GOU_3`
- event: `XWC_P07_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾三弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零四六`
- ASR 兼容读法: `零四六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T047 / slate 047

- 指法 / normalized_name: `散挑七`
- gesture_id: `SAN_TIAO_7`
- event: `XWC_P07_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑七弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零四七`
- ASR 兼容读法: `零四七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T048 / slate 048

- 指法 / normalized_name: `大九勾四`
- gesture_id: `AN_THUMB_9_GOU_4`
- event: `XWC_P07_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾四弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零四八`
- ASR 兼容读法: `零四八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T049 / slate 049

- 指法 / normalized_name: `大九勾四`
- gesture_id: `AN_THUMB_9_GOU_4`
- event: `XWC_P07_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾四弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零四九`
- ASR 兼容读法: `零四九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T050 / slate 050

- 指法 / normalized_name: `大九勾五`
- gesture_id: `AN_THUMB_9_GOU_5`
- event: `XWC_P08_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾五弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零五零`
- ASR 兼容读法: `零五零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

## batch06 T051-T060

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch06_T051-T060.wav`

### T051 / slate 051

- 指法 / normalized_name: `大九勾五`
- gesture_id: `AN_THUMB_9_GOU_5`
- event: `XWC_P08_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾五弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零五幺`
- ASR 兼容读法: `零五幺;零五一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T052 / slate 052

- 指法 / normalized_name: `大九勾六上七九`
- gesture_id: `AN_THUMB_9_GOU_6_SHANG_79`
- event: `XWC_P08_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾六弦出声后上滑至七徽九分；直按版本，不主动加绰。上滑要拖开，保留滑音过程和余音，结束后停 2.5 秒
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零五二`
- ASR 兼容读法: `零五二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T053 / slate 053

- 指法 / normalized_name: `大九勾六上七九`
- gesture_id: `AN_THUMB_9_GOU_6_SHANG_79`
- event: `XWC_P08_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾六弦，按 realization_variant=chuo 加入自然绰音；勾六出声后上滑至七徽九分。绰不要夸张，上滑要拖开，保留滑音过程和余音，结束后停 2.5 秒
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零五三`
- ASR 兼容读法: `零五三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T054 / slate 054

- 指法 / normalized_name: `散挑七`
- gesture_id: `SAN_TIAO_7`
- event: `XWC_P08_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑七弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零五四`
- ASR 兼容读法: `零五四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T055 / slate 055

- 指法 / normalized_name: `大九勾四`
- gesture_id: `AN_THUMB_9_GOU_4`
- event: `XWC_P08_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指按九徽，勾四弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零五五`
- ASR 兼容读法: `零五五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T056 / slate 056

- 指法 / normalized_name: `大九勾四`
- gesture_id: `AN_THUMB_9_GOU_4`
- event: `XWC_P08_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾四弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零五六`
- ASR 兼容读法: `零五六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T057 / slate 057

- 指法 / normalized_name: `大九勾四撞`
- gesture_id: `AN_THUMB_9_GOU_4_ZHUANG`
- event: `XWC_P09_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾四弦，带撞动作，撞幅度小，不要压重，保留余音，结束后停 2.5 秒
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零五七`
- ASR 兼容读法: `零五七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T058 / slate 058

- 指法 / normalized_name: `大九勾四撞`
- gesture_id: `AN_THUMB_9_GOU_4_ZHUANG`
- event: `XWC_P09_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 大指九徽勾四弦，录注按并带撞版本；撞为小幅回返，落点偏虚，保留余音，结束后停 2.5 秒
- realization_variant: `zhu`; realization_pre_action: `zhu`; take label: pre=zhu
- 口播: `零五八`
- ASR 兼容读法: `零五八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T059 / slate 059

- 指法 / normalized_name: `名十掐起`
- gesture_id: `AN_RING_10_QIAQI`
- event: `XWC_P09_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 单独录名十掐起，动作放清楚，保留左手发音的自然起点，保留余音，结束后停 2.5 秒
- realization_variant: `atomic`; realization_pre_action: `none`; take label: straight
- 口播: `零五九`
- ASR 兼容读法: `零五九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T060 / slate 060

- 指法 / normalized_name: `名十掐起`
- gesture_id: `AN_RING_10_QIAQI`
- event: `XWC_P09_N02` event_range: `XWC_P09_N01_to_N02`
- 弦位 / 徽位 / 动作说明: 录上下文版本：从 XWC_P09_N01 大注九勾四撞 接到 XWC_P09_N02 名十掐起，重点保持‘注—勾四—撞—掐起’的承接自然。撞要小幅、落点偏虚；掐起不要像孤立插入音。保留余音；context take，需录清前后动作；T060/T071 是同一 transition 的两条 context references，录两遍用于后续择优，不是编号错误，不作为 atomic sample 的直接替代
- realization_variant: `context`; realization_pre_action: `none`; take label: context
- 口播: `零六零`
- ASR 兼容读法: `零六零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

## batch07 T061-T071

Recommended raw filename after user-approved recording: `RS_XWC_002_BAIYA_PILOT_batch07_T061-T071.wav`

### T061 / slate 061

- 指法 / normalized_name: `散挑六`
- gesture_id: `SAN_TIAO_6`
- event: `XWC_P09_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 弹散音挑六弦，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六幺`
- ASR 兼容读法: `零六幺;零六一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T062 / slate 062

- 指法 / normalized_name: `名十勾四`
- gesture_id: `AN_RING_10_GOU_4`
- event: `XWC_P09_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指按十徽，勾四弦，直按版本，不主动加绰，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六二`
- ASR 兼容读法: `零六二`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T063 / slate 063

- 指法 / normalized_name: `名十勾四`
- gesture_id: `AN_RING_10_GOU_4`
- event: `XWC_P09_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 名指十徽勾四弦，按 realization_variant=chuo 加入自然绰音，注意绰不要夸张，保留余音
- realization_variant: `chuo`; realization_pre_action: `chuo`; take label: pre=chuo
- 口播: `零六三`
- ASR 兼容读法: `零六三`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T064 / slate 064

- 指法 / normalized_name: `泛食七勾四`
- gesture_id: `FAN_SHI_7_GOU_4`
- event: `XWC_P10_N01` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录泛音泛食七勾四，泛音点轻触清楚，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六四`
- ASR 兼容读法: `零六四`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T065 / slate 065

- 指法 / normalized_name: `泛食七挑七`
- gesture_id: `FAN_SHI_7_TIAO_7`
- event: `XWC_P10_N02` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录泛音泛食七挑七，泛音点轻触清楚，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六五`
- ASR 兼容读法: `零六五`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T066 / slate 066

- 指法 / normalized_name: `泛食七挑六`
- gesture_id: `FAN_SHI_7_TIAO_6`
- event: `XWC_P10_N03` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录泛音泛食七挑六，泛音点轻触清楚，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六六`
- ASR 兼容读法: `零六六`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T067 / slate 067

- 指法 / normalized_name: `泛食七挑四`
- gesture_id: `FAN_SHI_7_TIAO_4`
- event: `XWC_P10_N04` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录泛音泛食七挑四，泛音点轻触清楚，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六七`
- ASR 兼容读法: `零六七`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T068 / slate 068

- 指法 / normalized_name: `泛中七勾一`
- gesture_id: `FAN_ZHONG_7_GOU_1`
- event: `XWC_P10_N05` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录泛音泛中七勾一，泛音点轻触清楚，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六八`
- ASR 兼容读法: `零六八`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T069 / slate 069

- 指法 / normalized_name: `泛大七擘六`
- gesture_id: `FAN_DA_7_BO_6`
- event: `XWC_P10_N06` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录泛音泛大七擘六，泛音点轻触清楚，保留余音
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零六九`
- ASR 兼容读法: `零六九`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 1.2 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T070 / slate 070

- 指法 / normalized_name: `泛大七中七撮六一`
- gesture_id: `FAN_DA7_ZHONG7_CUO_6_1`
- event: `XWC_P10_N07` event_range: `none`
- 弦位 / 徽位 / 动作说明: 录复合泛音泛大七中七撮六一，两声同时起，手法保持干净，保留余音，结束后停 2.5 秒
- realization_variant: `straight`; realization_pre_action: `none`; take label: straight
- 口播: `零七零`
- ASR 兼容读法: `零七零`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。

### T071 / slate 071

- 指法 / normalized_name: `名十掐起`
- gesture_id: `AN_RING_10_QIAQI`
- event: `XWC_P09_N02` event_range: `XWC_P09_N01_to_N02`
- 弦位 / 徽位 / 动作说明: 录上下文版本：从 XWC_P09_N01 大注九勾四撞 接到 XWC_P09_N02 名十掐起，重点保持‘注—勾四—撞—掐起’的承接自然。撞要小幅、落点偏虚；掐起不要像孤立插入音。保留余音；context take，需录清前后动作；T060/T071 是同一 transition 的两条 context references，录两遍用于后续择优，不是编号错误，不作为 atomic sample 的直接替代
- realization_variant: `context`; realization_pre_action: `none`; take label: context
- 口播: `零七幺`
- ASR 兼容读法: `零七幺;零七一`
- 录音提醒: 先报号；停 0.8 秒；再弹；弹完等尾音自然结束；再停 2.5 秒；再进入下一条。
- Retake: 不停机删除；直接说本条编号 retake 2 / retake 3；重新弹；坏 take 保留。
