# Qinist Starter Missing Inputs v0.1

状态：缺失输入报告。缺失内容不推断、不补写。

当前 authority：`/Users/chenyulin/Downloads/RECD_VARW_Cyber_Guqin_v1.1.md` 已可用，作为本设计阶段当前 RECD/VARW 权威。旧版 `RECD&VARW · Cyber Guqin v1.0.txt` 属于 historical reference；除非用户明确要求 historical v1.0/v1.1 delta audit，它不阻塞当前 review，也不阻塞基于 v1.1 当前 authority 的后续实现。缺失时只保持 `MISSING_INPUT / NOT_FOUND / REQUIRED_ONLY_FOR_HISTORICAL_DELTA_AUDIT / NOT_BLOCKING_CURRENT_AUTHORITY`。

| Missing item | Expected path or source | Why needed | Blocking? | Safe fallback | What user should provide next |
| --- | --- | --- | --- | --- | --- |
| `RECD&VARW · Cyber Guqin v1.0.txt` | `/Users/chenyulin/Downloads/RECD&VARW · Cyber Guqin v1.0.txt` or repo same-name equivalent | Historical external project-field design reference named in the earlier design task | Not blocking current review; not blocking implementation based on `RECD_VARW_Cyber_Guqin_v1.1.md` current authority; required only if the user explicitly requests historical v1.0/v1.1 delta audit | Mark `MISSING_INPUT / NOT_FOUND / REQUIRED_ONLY_FOR_HISTORICAL_DELTA_AUDIT / NOT_BLOCKING_CURRENT_AUTHORITY`; do not infer v1.0 contents from v1.1 | Upload or place the exact v1.0 txt only if historical delta audit is requested |
| Sanman starter Dapu IR | future `QINIST_001_SANMAN` single-piece parser output | Needed before real collection demand extraction | Blocking for implementation | Use mock XWC-shaped fixture only as shape example | Provide approved Sanman target piece/source score and single-piece parser output |
| Sanman current collection inventory | future Sanman inventory/sidecar path | Needed to compute `already_covered` truth | Blocking for real coverage diff | Treat inventory as empty in design | Provide current Sanman approved inventory or confirm empty baseline |
| Formal starter-kit schema authority | future approved production schema task | Needed before runtime/schema wiring | Blocking for production | Draft schemas only | Approve or revise proposed fields |
| Prompt timing calibration data | future calibration report from real collection or approved Baiya metadata audit | Needed before hardcoding prompt interval | Non-blocking for design | Default assumption around 10s with warning | Provide calibration evidence or approve calibration task |
| Qinist Profile v0.1 production schema | future profile schema | Needed before profile signal implementation | Blocking for implementation | Draft profile signal extension only | Approve profile signal field set |
| Production sample ingest schema freeze | future sample ingest gate | Needed before sample asset creation | Blocking for sample ingest only | Sidecar-only design | Open separate sample ingest schema task later |
| Rhythm render parameter config | future ABCD render manifest/schema | Needed before rendering | Blocking for render execution | Parameter design only | Provide or approve rhythm parameter schema task |
| R2 profile mapping approval | user decision | Needed before deriving profile signals from R2 evidence | Blocking for implementation | Report-only mapping | Confirm signal families and evidence policy |

Required markers:

```text
MISSING_INPUT
NOT_FOUND
REQUIRED_ONLY_FOR_HISTORICAL_DELTA_AUDIT
NOT_BLOCKING_CURRENT_AUTHORITY
```
