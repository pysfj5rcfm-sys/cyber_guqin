import { useState } from "react";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { ExportPanel } from "../components/ExportPanel";
import { KeyValueList, SearchBox } from "../components/FileNavigator";
import { MarkerEditor } from "../components/MarkerEditor";
import { PlaybackBar } from "../components/ReviewStatusBar";
import { rawExports, rawFiles, rawFlags, rawMarkers } from "../mock/rawReviewMock";
import type { R0MarkerKey, ReviewStatus } from "../types/cgVarw";

export function R0RawReviewPage() {
  const [markers, setMarkers] = useState(rawMarkers);
  const [selectedKey, setSelectedKey] = useState(rawMarkers[2].key);
  const [status, setStatus] = useState<ReviewStatus>("unclear");

  function nudge(deltaMs: number) {
    setMarkers((current) => current.map((marker) => marker.key === selectedKey ? { ...marker, time: Math.max(0, marker.time + deltaMs / 1000) } : marker));
  }

  return (
    <AppShell
      mode="R0"
      left={<LeftPanel />}
      main={
        <div className="work-area">
          <div className="work-title">
            <div><h1>RS_XWC_002_BAIYA_PILOT / batch01_raw.wav</h1><p>44.1kHz · 24bit · 2ch · WAV</p></div>
            <span>时长：02:48.237</span>
          </div>
          <AudioCanvas markers={markers} duration={168.237} selectedKey={selectedKey} onSelect={(key) => setSelectedKey(key as R0MarkerKey)} />
          <PlaybackBar time="01:02.487" total="02:48.237" backLabel="前滚 300ms" />
        </div>
      }
      right={
        <MarkerEditor
          markers={markers}
          selectedKey={selectedKey}
          onSelectMarker={(key) => setSelectedKey(key as R0MarkerKey)}
          onNudge={nudge}
          selectedStatus={status}
          onStatus={(key) => setStatus(key as ReviewStatus)}
          statusLabels={[
            { key: "accepted", label: "通过", tone: "green" },
            { key: "unclear", label: "待复核", tone: "gold" },
            { key: "needs_retake", label: "需重录", tone: "red" },
            { key: "rejected", label: "拒绝", tone: "red" },
          ]}
        />
      }
      bottom={<ExportPanel title="导出" rows={rawExports} />}
    />
  );
}

function LeftPanel() {
  return (
    <div className="panel-stack">
      <h2>原始 Raw 文件</h2>
      <section className="editor-section">
        <h3>已识别 Raw 列表（ASR）</h3>
        <SearchBox placeholder="搜索文件或会话..." />
        <div className="file-list">
          {rawFiles.map((file) => <button key={file.name} className={file.selected ? "selected" : ""}><strong>{file.name}</strong><span>{file.meta}</span></button>)}
        </div>
      </section>
      <KeyValueList rows={[
        ["session_id", "RS_XWC_002_BAIYA_PILOT"],
        ["qinist_id", "QIN_001_BAIYA"],
        ["piece_id", "PIECE_002_XIANGSHUI"],
        ["当前批次 Batch", "batch01_raw.wav"],
        ["当前录次 Take", "TAKE_01"],
        ["review_only", String(rawFlags.review_only)],
        ["production_grade", String(rawFlags.production_grade)],
      ]} />
    </div>
  );
}
