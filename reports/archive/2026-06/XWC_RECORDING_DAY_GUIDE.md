# 《仙翁操》RS_XWC_001 录音日执行手册

这份手册只回答录音当天怎么录、怎么报号、错了怎么办、文件怎么保存、录完后不要做什么。

它不替代 `recording_batches.md`、`recording_script_human.csv`、`recording_script_human.md`。那三份旧任务文件仍然负责回答弹什么、按什么顺序弹、每条是什么指法、`straight` / `chuo` / `zhu` / `context` 怎么执行。

本次 `RS_XWC_001` 仍使用旧 71 条 recording tasks 作为演奏执行源。新的 `session_manifest`、`take_manifest`、`recording_segments` 是未来可复用录音资产模型；本次 legacy bridge 是把旧任务映射到新模型，不是推翻旧任务。

## 1. 本次录音目标

本次录的是《仙翁操》`RS_XWC_001` 的 71 条录音任务。录音内容以现有 `recording_batches.md` 为准。

录音当天不要临场改指法、改顺序、删任务。遇到 `straight`、`chuo`、`zhu`、`context`，按旧任务文字执行。

本次录音是为了后续切片、`sample_assets` 入库和真实三曼音频渲染。今天的任务是把可追溯、可切片、可复核的原始录音录好。

## 2. 录音前准备

使用 `QIN_A`，调弦使用 `ZHENG_DIAO`。

录 WAV。优先 48kHz / 24-bit；如果设备不方便，44.1kHz / 24-bit 也可以接受。一支麦就录 mono，只有在双麦摆位稳定、相位关系可控时才录 stereo。

开录前先录 10 秒 room noise。正式任务前录一次调弦参考音，录完整个 session 后再录一次调弦参考音。

尽量保证环境安静。开会话后不要反复移动麦克风；如果必须移动，在 notes 里记录移动发生在哪个 batch 之前。

## 3. 推荐录音方式

推荐按 batch 连续录。每个 batch 可以录成一个 WAV。

不建议一口气把 71 条全部录成一个大文件，也不建议每条都频繁开关录音。按 batch 录能保留演奏流动，也方便后面定位。

raw audio 原始文件不剪、不覆盖、不删除。后续切片发生在 normalized copy / `recording_segments` 层，不在 raw 文件上直接剪。

“raw 不剪”不是说未来不切片，而是说原始母带永久保存。后续拼曲使用的是 `recording_segments` / `sample_assets`，不是直接拼 raw audio。

## 4. 每条怎么录

每条开始前读或轻敲 `batch_take_no`，例如：“001”，然后弹奏。

弹完保留 2-3 秒自然尾音。不要刚出声结束就立刻说话，也不要马上停止录音。

遇到上滑、撞、掐起、泛音等特殊动作，按 `recording_batches.md` 的文字执行。尤其是上滑和撞，不要为了单个样本而把动作做成机械短音；要让动作过程和余音自然留下来。

## 5. 弹错怎么办

不要停机删除。

直接说或敲：“001 retake 2”，然后重新弹。坏 take 保留在 raw audio 里。

后续会在 `take_manifest` / QC 阶段标记 reject 或 needs_reshoot。不要覆盖旧 take，不要把坏 take 剪掉。

## 6. context take 怎么录

context take 也要按编号录，特别是撞到掐起这类上下文。

context take 暂时作为参考 / 特殊样本候选。第一版 render 不一定直接使用 context sample。

录的时候仍需保留完整前后动作和尾音。不要只录孤立的掐起；要让前一个动作、连接、掐起、尾音都在录音里。

## 7. 录完后怎么交付

保留原始 WAV。不要剪，不要转 MP3，不要重命名成看不出 batch 的名字。

将每个 batch 的 WAV 放入待归档目录。如果有 retake，保留在同一个 batch 文件里，或按后续确认的 retake 规则命名。

录完后只做文件备份，不做 `sample_assets` 入库。

## 8. 录完后不要做什么

- 不要直接切片。
- 不要直接写 `03_samples/sample_assets.csv`。
- 不要删除 raw audio。
- 不要把口播编号从 raw 中剪掉。
- 不要把 bad take 删除。
- 不要把 `recording_batches.md` 当作未来标准数据源。
- 不要把三曼默认绰写回 `score_events`。

## 9. 录音当天最小清单

- [ ] `QIN_A`
- [ ] `ZHENG_DIAO`
- [ ] WAV
- [ ] 48kHz / 24-bit 或 44.1kHz / 24-bit
- [ ] 10 秒 room noise
- [ ] session 前调弦参考音
- [ ] 按 batch 录
- [ ] 每条读/敲编号
- [ ] 每条后留 2-3 秒尾音
- [ ] retake 不删除
- [ ] session 后调弦参考音
- [ ] raw 文件备份
- [ ] 不切片
- [ ] 不写 `sample_assets`

## 10. 和 legacy bridge 的关系

本次 71 条任务来自旧 v1.0 Phase 1A 结构。它仍然是本次“弹什么”的权威执行源。

`session_manifest` / `take_manifest` / `recording_segments` 是未来可复用资产模型。legacy bridge 用来把本次旧任务映射到未来资产模型。

Future pieces should use Dapu Event IR / canon-backed parser to generate standard recording plans.
