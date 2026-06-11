import { useState } from "react";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { ExportPanel } from "../components/ExportPanel";
import { KeyValueList, SearchBox } from "../components/FileNavigator";
import { MarkerEditor } from "../components/MarkerEditor";
import { PlaybackBar } from "../components/ReviewStatusBar";
import { splitExports, splitFlags, splitMarkers, splitSegments } from "../mock/splitReviewMock";
import type { R1MarkerKey, RenderStatus } from "../types/cgVarw";

export function R1SplitReviewPage() {
  const [markers, setMarkers] = useState(splitMarkers);
  const [selectedKey, setSelectedKey] = useState(splitMarkers[2].key);
  const [status, setStatus] = useState<RenderStatus>("render_usable");

  function nudge(deltaMs: number) {
    setMarkers((current) => current.map((marker) => marker.key === selectedKey ? { ...marker, time: Math.max(0, marker.time + deltaMs / 1000) } : marker));
  }

  return (
    <AppShell
      mode="R1"
      left={<LeftPanel />}
      main={
        <div className="work-area">
          <div className="work-title">
            <div><h1>当前选择　batch01 / T003_clean.wav</h1><p>Event: E_20250506_142500　Segment ID: seg_000127　Variant: clean</p></div>
          </div>
          <AudioCanvas markers={markers} duration={2.9} selectedKey={selectedKey} onSelect={(key) => setSelectedKey(key as R1MarkerKey)} />
          <PlaybackBar time="0.410s" total="02:45.093" backLabel="前滚 100ms" />
        </div>
      }
      right={
        <MarkerEditor
          markers={markers}
          selectedKey={selectedKey}
          onSelectMarker={(key) => setSelectedKey(key as R1MarkerKey)}
          onNudge={nudge}
          selectedStatus={status}
          onStatus={(key) => setStatus(key as RenderStatus)}
          statusLabels={[
            { key: "render_usable", label: "可渲染", tone: "green" },
            { key: "reference_only", label: "仅参考", tone: "blue" },
            { key: "unclear", label: "不明确", tone: "gold" },
            { key: "needs_retake", label: "需重录", tone: "red" },
            { key: "rejected", label: "拒绝", tone: "red" },
          ]}
          extra={
            <>
              <section className="editor-section">
                <h3>Anchor type</h3>
                <div className="pill-row"><button className="active">main_attack</button><button>gesture_start</button><button>context_first_attack</button></div>
              </section>
              <section className="editor-section">
                <h3>审核策略</h3>
                <label>pre_attack_music<select><option>keep_silence</option><option>preserve</option></select></label>
                <label>tail_policy<select><option>smart_fade_100ms</option><option>full_tail</option></select></label>
              </section>
            </>
          }
        />
      }
      bottom={<ExportPanel title="导出" rows={splitExports} />}
    />
  );
}

function LeftPanel() {
  return (
    <div className="panel-stack">
      <h2>Split 文件审校</h2>
      <section className="editor-section"><h3>一级筛选 / 批次 batch</h3><select><option>batch01</option></select></section>
      <section className="editor-section">
        <h3>二级筛选 / Take / Segment</h3>
        <SearchBox placeholder="搜索 take / segment..." />
        <div className="file-list compact-list">
          {splitSegments.map((segment) => <button key={segment.name} className={segment.selected ? "selected" : ""}><strong>{segment.name}<em>{segment.status}</em></strong><span>{segment.duration}　{segment.time}</span></button>)}
        </div>
      </section>
      <KeyValueList rows={[
        ["session_id", "RS_XWC_002_BAIYA_PILOT"],
        ["qinist_id", "QIN_001_BAIYA"],
        ["piece_id", "PIECE_002_XIANGSHUI"],
        ["当前批次 batch", "batch01"],
        ["当前文件 segment", "T003_clean.wav"],
        ["文件时长", "02:45.093"],
        ["采样率 / 位深", "44.1kHz / 24bit"],
        ["声道", "Mono"],
        ["review_only", String(splitFlags.review_only)],
        ["production_grade", String(splitFlags.production_grade)],
      ]} />
    </div>
  );
}
