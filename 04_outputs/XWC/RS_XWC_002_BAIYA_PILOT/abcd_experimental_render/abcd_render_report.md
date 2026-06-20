# 《仙翁操》白牙 ABCD Experimental Render 报告

任务名称：`CG-XWC_BAIYA_ABCD_EXPERIMENTAL_RENDER_FROM_PLANNING`

## 1. 本次输出性质

本次生成的是 `RS_XWC_002_BAIYA_PILOT` 的 A/B/C/D experimental render，不是 production render，不是 sample ingest 成功，也不是最终打谱成功。白牙仍为 `QINIST_002`，`QINIST_001 三曼` 身份未被覆盖。

## 2. 四版如何使用 abcd_version_policy.local.yaml

四版共享同一 `render_source_map.local.json` 与 51 个唯一 event order，但分别读取 `abcd_version_policy.local.yaml` 的版本意图、phrase/timing/context/tail/crossfade 策略：

- `A_LITERAL`：尽量少加修饰，节奏克制，保留谱面骨架。 输出 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/A_LITERAL/XWC_BAIYA_A_LITERAL.wav`，duration=141.721s，event_count=51。
- `B_PHRASE`：强调句读、气口、段落呼吸，但不添加新的谱面事实。 输出 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/B_PHRASE/XWC_BAIYA_B_PHRASE.wav`，duration=147.805s，event_count=51。
- `C_QINIST_STYLE`：在不改谱面事实的前提下，更自然地处理白牙样本衔接、尾音与呼吸。 输出 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/C_QINIST_STYLE/XWC_BAIYA_C_QINIST_STYLE.wav`，duration=135.605s，event_count=51。
- `D_TEACHING_DIAGNOSTIC`：结构更清楚，动作与音位更分明，方便听评和定位问题。 输出 `04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/D_TEACHING_DIAGNOSTIC/XWC_BAIYA_D_TEACHING_DIAGNOSTIC.wav`，duration=167.573s，event_count=51。

## 3. render_anchor_s 对齐

本次所有 segment 均使用 `segment_insert_time_s = target_attack_time_s - render_anchor_s`。未按 clean wav 文件开头直接对齐，validation 中 `render_anchor_alignment_used=true`、`file_start_alignment_used=false`。

## 4. dummy fallback

未使用 dummy fallback。若 source map 或 clean preview 缺失，本脚本会停止生成 wav 并写 blocked validation。

## 5. E_REVIEWED

未生成 E。`e_co_review_schema.local.yaml` 只用于确认 E 是后续 Human+GPT Co-Created Reviewed Dapu，当前 `e_generated=false`。

## 6. 禁写资产

未写 `03_samples/sample_assets.csv`，未写 `03_samples/recording_segments.csv`，未创建 `recording_items_enriched.jsonl`，未训练 ML，未修改 score/canon/sources/raw/R0/R1 archive。

## 7. T060/T071 context take

`T060=context_take_1`，`T071=context_take_2`，二者均属于 `XWC_P09_N01_to_N02`。本次将它们作为 P09 transition context references：A 保持更直译的 `T059`，B/D 使用 `T060`，C 使用 `T071`。它们没有被反写为普通 atomic sample 或 score fact。`T071` 保持 `batch08 / T071 / 001`，不是 `batch07_take_011`，不是 retake。

## 8. 每版听评目标

- `A_LITERAL`：听谱面骨架、anchor 是否稳、是否过于机械。
- `B_PHRASE`：听句读、气口、phrase boundary 与呼吸是否自然。
- `C_QINIST_STYLE`：听白牙样本衔接、自然尾音、context take 的演奏连续性。
- `D_TEACHING_DIAGNOSTIC`：听结构、动作与音位边界是否清楚，方便定位问题。

## 9. 下一步

下一步应进入 Human+GPT co-review：用户先听四个 wav，GPT 再结合 wav、alignment 与 `sample_selection_decision.csv` 做结构分析、工程诊断与打谱解释诊断，共创 `E_REVIEWED` 的 revision plan。不得自动生成 E。
