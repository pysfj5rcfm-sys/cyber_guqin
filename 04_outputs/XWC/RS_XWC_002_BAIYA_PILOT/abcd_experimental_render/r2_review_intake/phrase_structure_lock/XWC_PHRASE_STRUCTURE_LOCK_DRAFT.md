# XWC / 仙翁操 R2 谱面句法锁定草案

本文件是正式听评前的谱面句法锁定草案，不是 final / verified dapu interpretation。句法边界来自 `score_events.csv` 的 `phrase_id` 与 `event_role`；ABCD render alignment 只用于列出每句在各版本中的 start/end，sample_selection_decision 只用于列出每个 event 采用的样本。

## 句法概览
- 第1句 / XWC_P01：4 个 score events，event_id = XWC_P01_N01;XWC_P01_N02;XWC_P01_N03;XWC_P01_N04；gesture_id = SAN_TIAO_7;SAN_GOU_5;SAN_TIAO_7;AN_RING_10_GOU_5；指法/归一名 = 散挑七;散勾五;散挑七;名十勾五。
- 第2句 / XWC_P02：6 个 score events，event_id = XWC_P02_N01;XWC_P02_N02;XWC_P02_N03;XWC_P02_N04;XWC_P02_N05;XWC_P02_N06；gesture_id = SAN_TIAO_7;SAN_GOU_5;SAN_TIAO_6;AN_RING_10_GOU_4;SAN_TIAO_7;AN_THUMB_9_GOU_4；指法/归一名 = 散挑七;散勾五;散挑六;名十勾四;散挑七;大九勾四。
- 第3句 / XWC_P03：6 个 score events，event_id = XWC_P03_N01;XWC_P03_N02;XWC_P03_N03;XWC_P03_N04;XWC_P03_N05;XWC_P03_N06；gesture_id = SAN_TIAO_6;SAN_GOU_4;SAN_TIAO_5;AN_RING_10_8_GOU_3;SAN_TIAO_6;AN_THUMB_9_GOU_3；指法/归一名 = 散挑六;散勾四;散挑五;名十徽八勾三;散挑六;大九勾三。
- 第4句 / XWC_P04：6 个 score events，event_id = XWC_P04_N01;XWC_P04_N02;XWC_P04_N03;XWC_P04_N04;XWC_P04_N05;XWC_P04_N06；gesture_id = SAN_TIAO_5;SAN_GOU_3;SAN_TIAO_4;AN_RING_10_GOU_2;SAN_TIAO_5;AN_THUMB_9_GOU_2；指法/归一名 = 散挑五;散勾三;散挑四;名十勾二;散挑五;大九勾二。
- 第5句 / XWC_P05：6 个 score events，event_id = XWC_P05_N01;XWC_P05_N02;XWC_P05_N03;XWC_P05_N04;XWC_P05_N05;XWC_P05_N06；gesture_id = SAN_TIAO_4;SAN_GOU_2;SAN_TIAO_3;AN_RING_10_GOU_1;SAN_TIAO_4;AN_THUMB_9_GOU_1；指法/归一名 = 散挑四;散勾二;散挑三;名十勾一;散挑四;大九勾一。
- 第6句 / XWC_P06：4 个 score events，event_id = XWC_P06_N01;XWC_P06_N02;XWC_P06_N03;XWC_P06_N04；gesture_id = SAN_TIAO_4;AN_THUMB_9_GOU_1;SAN_TIAO_5;AN_THUMB_9_GOU_2；指法/归一名 = 散挑四;大九勾一;散挑五;大九勾二。
- 第7句 / XWC_P07：4 个 score events，event_id = XWC_P07_N01;XWC_P07_N02;XWC_P07_N03;XWC_P07_N04；gesture_id = SAN_TIAO_6;AN_THUMB_9_GOU_3;SAN_TIAO_7;AN_THUMB_9_GOU_4；指法/归一名 = 散挑六;大九勾三;散挑七;大九勾四。
- 第8句 / XWC_P08：4 个 score events，event_id = XWC_P08_N01;XWC_P08_N02;XWC_P08_N03;XWC_P08_N04；gesture_id = AN_THUMB_9_GOU_5;AN_THUMB_9_GOU_6_SHANG_79;SAN_TIAO_7;AN_THUMB_9_GOU_4；指法/归一名 = 大九勾五;大九勾六上七九;散挑七;大九勾四。
- 第9句 / XWC_P09：4 个 score events，event_id = XWC_P09_N01;XWC_P09_N02;XWC_P09_N03;XWC_P09_N04；gesture_id = AN_THUMB_9_GOU_4_ZHUANG;AN_RING_10_QIAQI;SAN_TIAO_6;AN_RING_10_GOU_4；指法/归一名 = 大九勾四撞;名十掐起;散挑六;名十勾四。
- 第10句 / XWC_P10：7 个 score events，event_id = XWC_P10_N01;XWC_P10_N02;XWC_P10_N03;XWC_P10_N04;XWC_P10_N05;XWC_P10_N06;XWC_P10_N07；gesture_id = FAN_SHI_7_GOU_4;FAN_SHI_7_TIAO_7;FAN_SHI_7_TIAO_6;FAN_SHI_7_TIAO_4;FAN_ZHONG_7_GOU_1;FAN_DA_7_BO_6;FAN_DA7_ZHONG7_CUO_6_1；指法/归一名 = 泛食七勾四;泛食七挑七;泛食七挑六;泛食七挑四;泛中七勾一;泛大七擘六;泛大七中七撮六一。

## ABCD 各句时间范围
- 第1句 `XWC_P01_LOCAL_PHRASE` / `XWC_P01_N01_to_XWC_P01_N04`：A_LITERAL: 1.284-20.877s；B_PHRASE: 1.284-20.324s；C_QINIST_STYLE: 1.284-20.051s；D_TEACHING_DIAGNOSTIC: 1.284-21.702s
- 第2句 `XWC_P02_LOCAL_PHRASE` / `XWC_P02_N01_to_XWC_P02_N06`：A_LITERAL: 16.392-35.239s；B_PHRASE: 17.179-37.434s；C_QINIST_STYLE: 16.362-35.709s；D_TEACHING_DIAGNOSTIC: 18.167-39.064s
- 第3句 `XWC_P03_LOCAL_PHRASE` / `XWC_P03_N01_to_XWC_P03_N06`：A_LITERAL: 30.836-51.542s；B_PHRASE: 32.494-52.352s；C_QINIST_STYLE: 30.415-49.077s；D_TEACHING_DIAGNOSTIC: 35.467-58.223s
- 第4句 `XWC_P04_LOCAL_PHRASE` / `XWC_P04_N01_to_XWC_P04_N06`：A_LITERAL: 46.502-67.317s；B_PHRASE: 48.723-68.756s；C_QINIST_STYLE: 45.293-63.779s；D_TEACHING_DIAGNOSTIC: 54.095-77.023s
- 第5句 `XWC_P05_LOCAL_PHRASE` / `XWC_P05_N01_to_XWC_P05_N06`：A_LITERAL: 62.056-81.132s；B_PHRASE: 65.084-85.225s；C_QINIST_STYLE: 59.733-78.721s；D_TEACHING_DIAGNOSTIC: 72.712-94.063s
- 第6句 `XWC_P06_LOCAL_PHRASE` / `XWC_P06_N01_to_XWC_P06_N04`：A_LITERAL: 77.290-91.380s；B_PHRASE: 80.701-93.908s；C_QINIST_STYLE: 73.673-86.317s；D_TEACHING_DIAGNOSTIC: 91.048-106.603s
- 第7句 `XWC_P07_LOCAL_PHRASE` / `XWC_P07_N01_to_XWC_P07_N04`：A_LITERAL: 87.060-101.429s；B_PHRASE: 91.153-105.236s；C_QINIST_STYLE: 83.034-96.324s；D_TEACHING_DIAGNOSTIC: 103.233-118.948s
- 第8句 `XWC_P08_LOCAL_PHRASE` / `XWC_P08_N01_to_XWC_P08_N04`：A_LITERAL: 95.732-110.575s；B_PHRASE: 100.168-117.927s；C_QINIST_STYLE: 92.258-107.926s；D_TEACHING_DIAGNOSTIC: 114.201-130.004s
- 第9句 `XWC_P09_LOCAL_PHRASE` / `XWC_P09_N01_to_XWC_P09_N04`：A_LITERAL: 104.697-120.539s；B_PHRASE: 109.851-125.918s；C_QINIST_STYLE: 101.833-115.735s；D_TEACHING_DIAGNOSTIC: 125.496-142.838s
- 第10句 `XWC_P10_LOCAL_PHRASE` / `XWC_P10_N01_to_XWC_P10_N07`：A_LITERAL: 116.371-140.721s；B_PHRASE: 121.976-146.805s；C_QINIST_STYLE: 111.460-134.605s；D_TEACHING_DIAGNOSTIC: 139.720-166.573s

## R2 seed 审计
- 当前 `r2_phrase_alignment_seed.csv` 与谱面句法一致：10 个 unique phrase，每句恰好 A/B/C/D 四行，总计 40 行。
- R2 前端应按 unique phrase 展示左侧列表，不应把 40 条 version row 显示成 40 个 phrase，也不应把 51 个 event 显示成 51 个 phrase。

## 需要人工确认
- 10 句均为 draft 状态：谱面句法事实已从 `score_events.csv` 锁定为草案，但正式进入 E_REVIEWED 前仍需要用户确认。
- 未发现 blocked 句；若听评时认为某句应跨 Pxx 合并或拆分，不得直接修改 score_events，应先形成 Human+GPT 共评记录。

## 禁止边界
- 本草案不生成 E，不生成 wav，不训练 ML，不写 sample_assets.csv / recording_segments.csv / recording_items_enriched.jsonl。
- 不把 realization_variant、白牙样本选择或 render 对齐反写成谱面事实。
