import { useState } from "react";
import { ABCDEPhrasePlayer } from "../components/ABCDEPhrasePlayer";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { ExportPanel } from "../components/ExportPanel";
import { PhraseStructurePanel } from "../components/PhraseStructurePanel";
import { PlaybackBar } from "../components/ReviewStatusBar";
import { phraseExports, phraseMarkers, projectFlags, versions } from "../mock/projectReviewMock";
import type { R2MarkerKey, Severity } from "../types/cgVarw";

export function R2ProjectReviewPage() {
  const [markers, setMarkers] = useState(phraseMarkers);
  const [selectedKey, setSelectedKey] = useState<R2MarkerKey>("cadence");
  const [preferred, setPreferred] = useState("B_PHRASE");
  const [severity, setSeverity] = useState<Severity>("medium");

  function nudgePhrase(delta: number) {
    setMarkers((current) => current.map((marker) => marker.key === selectedKey ? { ...marker, time: Math.max(0, marker.time + delta / 1000) } : marker));
  }

  return (
    <AppShell
      mode="R2"
      left={<LeftPanel />}
      main={
        <div className="r2-main">
          <div className="work-title tight">
            <div>
              <h1>XWC / 仙翁操 · ABCDE 句读对齐听评</h1>
              <p>当前比较：PHRASE_03 / XWC_P03_N02_to_N04 · 不按绝对时间切换，只按句读结构对齐</p>
            </div>
            <span>自动滚动 <input type="checkbox" defaultChecked /></span>
          </div>
          <ABCDEPhrasePlayer versions={versions.map((item) => ({ ...item, selected: item.key === preferred }))} onSelect={setPreferred} />
          <section className="work-area phrase-area">
            <h2>当前句读波形工作区（B 句法呼吸版 / B Phrase Dapu）</h2>
            <AudioCanvas markers={markers} duration={106.262} selectedKey={selectedKey} onSelect={(key) => setSelectedKey(key as R2MarkerKey)} />
            <div className="event-strip"><span>XWC_P03_N02</span><span>XWC_P03_N03</span><span>XWC_P03_N04</span></div>
            <PlaybackBar time="01:03.842" total="01:46.262" backLabel="前后 5s" sequenceLabel="A→E 顺序播放" />
          </section>
        </div>
      }
      right={<RightPanel selectedKey={selectedKey} setSelectedKey={setSelectedKey} severity={severity} setSeverity={setSeverity} nudge={nudgePhrase} />}
      bottom={<ExportPanel title="导出与评审历史" rows={phraseExports} />}
    />
  );
}

function LeftPanel() {
  return (
    <div className="panel-stack">
      <h2>项目</h2>
      <div className="tree">
        <strong>⌬ Cyber Guqin v1.0 <small>进行中</small></strong>
        <button className="active">RS_XWC_002_BAIYA_PILOT</button>
        <button>Raw 文件</button><button>Split 标记</button><button>Render 输出</button>
      </div>
      <section className="editor-section"><h3>曲目</h3><button className="wide active">♫ XWC / 仙翁操</button><button className="wide">♫ LDJ / 流水</button><button className="wide">♫ GYQ / 广陵散</button><button className="wide">♫ ZJ / 梅花三弄</button></section>
      <section className="editor-section"><h3>会话</h3><button className="wide">session_01</button><button className="wide active">session_02</button><button className="wide">session_03</button></section>
      <section className="editor-section"><h3>评审看板</h3><button className="wide">Project Dashboard</button><button className="wide">Samples Review</button><button className="wide active">ABCDE 句读对齐听评</button></section>
      <PhraseStructurePanel />
      <p className="flags">review_only={String(projectFlags.review_only)} · production_grade={String(projectFlags.production_grade)}</p>
    </div>
  );
}

function RightPanel({
  selectedKey,
  setSelectedKey,
  severity,
  setSeverity,
  nudge,
}: {
  selectedKey: R2MarkerKey;
  setSelectedKey: (key: R2MarkerKey) => void;
  severity: Severity;
  setSeverity: (key: Severity) => void;
  nudge: (delta: number) => void;
}) {
  const labels: { key: R2MarkerKey; label: string }[] = [
    { key: "phrase_start", label: "句头" },
    { key: "phrase_end", label: "句尾" },
    { key: "breath_point", label: "气口" },
    { key: "cadence", label: "收束" },
    { key: "section_start", label: "段落起" },
    { key: "unclear_boundary", label: "边界不明" },
  ];
  const issues = ["太快", "太拖", "尾音短", "气口错", "像拼接", "音头突兀", "句读不清", "很好"];
  return (
    <div className="panel-stack">
      <h2>句读与听评编辑</h2>
      <div className="info-card">
        <span>当前比较对象</span>
        <strong>PHRASE_03 · 第3句</strong>
        <code>event_range: XWC_P03_N02_to_N04</code>
        <code>preferred_version: B_PHRASE</code>
      </div>
      <section className="editor-section">
        <h3>句读标记（当前句）</h3>
        <div className="button-grid">
          {labels.map((item) => <button key={item.key} className={selectedKey === item.key ? "active" : ""} onClick={() => setSelectedKey(item.key)}>{item.label}<small>{item.key}</small></button>)}
        </div>
      </section>
      <section className="editor-section"><h3>微调</h3><div className="nudge-grid">{[-50, -10, -5, 5, 10, 50].map((delta) => <button key={delta} onClick={() => nudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>)}</div></section>
      <section className="editor-section"><h3>问题类型（单选）</h3><div className="issue-grid">{issues.map((issue) => <button key={issue} className={issue === "尾音短" ? "active tone-red" : issue === "很好" ? "tone-green" : ""}>{issue}</button>)}</div></section>
      <section className="editor-section"><h3>严重程度</h3><div className="segmented">{(["low", "medium", "high"] as Severity[]).map((item) => <button key={item} className={severity === item ? "active" : ""} onClick={() => setSeverity(item)}>{item === "low" ? "低" : item === "medium" ? "中" : "高"}</button>)}</div></section>
      <section className="editor-section"><h3>批注与修订建议</h3><textarea defaultValue={"气口出现偏晚，影响后段呼吸连贯性。\n建议在 00:21.824 附近提前收气，增强短承转合。"} /><span className="char-count">78 / 500</span><div className="action-row"><button className="active">保存当前批注</button><button>导出听评 YAML</button></div></section>
      <section className="editor-section"><h3>快速统计（本会话）</h3><div className="quick-stats"><b>已标注句 8</b><b>问题数 13</b><b>优秀句 3</b></div></section>
    </div>
  );
}
