import { useMemo, useState } from "react";
import { ABCDEPhrasePlayer } from "../components/ABCDEPhrasePlayer";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { ExportPanel } from "../components/ExportPanel";
import { PlaybackBar } from "../components/ReviewStatusBar";
import {
  defaultListeningReview,
  getAlignment,
  getPhrase,
  getSection,
  issueOptions,
  makePhraseMarkers,
  mockPieces,
  mockSessions,
  phraseAlignments,
  phraseExports,
  phrases,
  projectFlags,
  renderSet,
  r2SafetyFlags,
  sections,
  versions,
} from "../mock/projectReviewMock";
import type { ListeningReview, Marker, PhraseMarker, R2DraftPayload, R2IssueType, R2MarkerKey, Severity } from "../types/cgVarw";

const draftKey = `cg-varw:r2:${renderSet.render_set_id}:draft`;

export function R2ProjectReviewPage() {
  const [selectedPhraseId, setSelectedPhraseId] = useState("PHRASE_03");
  const [selectedVersionId, setSelectedVersionId] = useState("B_PHRASE");
  const [preferredVersionId, setPreferredVersionId] = useState("B_PHRASE");
  const [markers, setMarkers] = useState<PhraseMarker[]>(() => makePhraseMarkers("PHRASE_03", "B_PHRASE"));
  const [selectedMarkerId, setSelectedMarkerId] = useState("PHRASE_03_B_PHRASE_cadence");
  const [review, setReview] = useState<ListeningReview>(defaultListeningReview);
  const [exportGroup, setExportGroup] = useState("全部");
  const [status, setStatus] = useState("R2A mock ready · review_only=true · production_grade=false");
  const selectedPhrase = getPhrase(selectedPhraseId);
  const selectedSection = getSection(selectedPhrase.section_id);
  const selectedAlignment = getAlignment(selectedPhraseId, selectedVersionId);
  const activeVersion = versions.find((version) => version.version_id === selectedVersionId) ?? versions[1];
  const alignmentsForPhrase = phraseAlignments.filter((alignment) => alignment.phrase_id === selectedPhraseId);
  const canvasMarkers = useMemo(() => markers.map(toCanvasMarker), [markers]);

  function selectPhrase(phraseId: string) {
    const phrase = getPhrase(phraseId);
    const nextMarkers = makePhraseMarkers(phraseId, selectedVersionId);
    setSelectedPhraseId(phraseId);
    setMarkers(nextMarkers);
    setSelectedMarkerId(nextMarkers[0]?.marker_id ?? "");
    setReview((current) => ({
      ...current,
      review_id: `R2_REVIEW_${phraseId}_${selectedVersionId}`,
      phrase_id: phraseId,
      section_id: phrase.section_id,
      event_range: phrase.event_range,
      active_version_id: selectedVersionId,
      preferred_version_id: preferredVersionId,
    }));
  }

  function selectVersion(versionId: string) {
    const nextMarkers = makePhraseMarkers(selectedPhraseId, versionId);
    setSelectedVersionId(versionId);
    setMarkers(nextMarkers);
    setSelectedMarkerId(nextMarkers[0]?.marker_id ?? "");
    setReview((current) => ({ ...current, active_version_id: versionId }));
    setStatus(`${versionId} 已切换到 ${selectedPhraseId} 的 phrase range；未使用绝对时间复用。`);
  }

  function nudgeMarker(deltaMs: number) {
    setMarkers((current) => current.map((marker) => (
      marker.marker_id === selectedMarkerId
        ? { ...marker, time_s: Math.max(0, Number((marker.time_s + deltaMs / 1000).toFixed(3))), nudge_total_ms: marker.nudge_total_ms + deltaMs }
        : marker
    )));
  }

  function updateMarker(patch: Partial<PhraseMarker>) {
    setMarkers((current) => current.map((marker) => marker.marker_id === selectedMarkerId ? { ...marker, ...patch } : marker));
  }

  function toggleIssue(issue: R2IssueType) {
    setReview((current) => ({
      ...current,
      issue_type: current.issue_type.includes(issue) ? current.issue_type.filter((item) => item !== issue) : [...current.issue_type, issue],
    }));
  }

  function saveDraft() {
    const payload: R2DraftPayload = {
      render_set_id: renderSet.render_set_id,
      selected_phrase_id: selectedPhraseId,
      selected_version_id: selectedVersionId,
      preferred_version_id: preferredVersionId,
      phrase_markers: markers,
      phrase_alignments: phraseAlignments,
      listening_review: { ...review, preferred_version_id: preferredVersionId, reviewed_at: review.reviewed_at || new Date().toISOString() },
      saved_at: new Date().toISOString(),
      ...r2SafetyFlags,
    };
    localStorage.setItem(draftKey, JSON.stringify(payload));
    setStatus("draft 已保存");
  }

  function loadDraft() {
    const raw = localStorage.getItem(draftKey);
    if (!raw) {
      setStatus("未找到 R2 draft；当前仍为内置 mock。");
      return;
    }
    try {
      const payload = JSON.parse(raw) as R2DraftPayload;
      setSelectedPhraseId(payload.selected_phrase_id);
      setSelectedVersionId(payload.selected_version_id);
      setPreferredVersionId(payload.preferred_version_id ?? payload.selected_version_id);
      setMarkers(payload.phrase_markers);
      setSelectedMarkerId(payload.phrase_markers[0]?.marker_id ?? "");
      setReview(payload.listening_review);
      setStatus("已加载 R2 draft");
    } catch (error) {
      setStatus(`R2 draft 加载失败：${error instanceof Error ? error.message : String(error)}`);
    }
  }

  function exportMock(scope: "all" | "phrase") {
    setStatus(`已请求导出${scope === "all" ? "全部" : "当前 phrase"}；后端路径为 review_outputs/r2/exports，保持 review-only。`);
  }

  return (
    <AppShell
      mode="R2"
      left={<LeftPanel selectedPhraseId={selectedPhraseId} onSelectPhrase={selectPhrase} />}
      main={
        <div className="r2-main">
          <div className="work-title tight">
            <div>
              <h1>XWC / 仙翁操 · R2 句读听评</h1>
              <p>当前比较：{selectedSection.section_id} / {selectedPhrase.phrase_id} / {selectedPhrase.event_range}</p>
              <p>按 phrase_id / event_range 对齐，不按绝对时间切换。</p>
            </div>
            <span className="badge badge-blue">active_version={selectedVersionId}</span>
          </div>
          <ABCDEPhrasePlayer versions={versions} alignments={alignmentsForPhrase} selectedVersionId={selectedVersionId} onSelect={selectVersion} />
          <section className="work-area phrase-area">
            <h2>当前 phrase 波形 / 频谱 · {activeVersion.version_code} {activeVersion.version_label_zh}</h2>
            <AudioCanvas
              markers={canvasMarkers}
              duration={activeVersion.duration_s}
              selectedKey={selectedMarkerId}
              onSelect={setSelectedMarkerId}
              audioFileName={`${selectedVersionId} mock waveform · ${selectedPhraseId}`}
              waveformPeaks={activeVersion.waveform_preview}
            />
            <div className="event-strip"><span>{selectedPhrase.start_event_id}</span><span>{selectedPhrase.event_range}</span><span>{selectedPhrase.end_event_id}</span></div>
            <PlaybackBar time={formatTime(selectedAlignment.start_s)} total={formatTime(selectedAlignment.end_s)} backLabel="前滚 300ms" sequenceLabel="从句头播放" />
            <div className="playback-bar r2-playback-bar">
              <button onClick={() => setStatus("顺播 A→B→C→D→E：逐个使用当前 phrase 在各版本的 start_s/end_s。")}>顺播 A→B→C→D→E</button>
              <button onClick={() => setStatus(`播放 preferred version：${preferredVersionId} / ${selectedPhraseId}`)}>播放 preferred version</button>
              <button onClick={() => setStatus(`A/B 对比播放：${selectedPhraseId} 各自 phrase range。`)}>A/B 对比播放</button>
              <strong className="clock">{selectedAlignment.start_s.toFixed(3)}<small>- {selectedAlignment.end_s.toFixed(3)}s</small></strong>
            </div>
          </section>
        </div>
      }
      right={
        <RightPanel
          selectedPhraseId={selectedPhraseId}
          selectedSectionId={selectedSection.section_id}
          eventRange={selectedPhrase.event_range}
          selectedVersionId={selectedVersionId}
          preferredVersionId={preferredVersionId}
          setPreferredVersionId={setPreferredVersionId}
          markers={markers}
          selectedMarkerId={selectedMarkerId}
          setSelectedMarkerId={setSelectedMarkerId}
          updateMarker={updateMarker}
          nudge={nudgeMarker}
          review={review}
          setReview={setReview}
          toggleIssue={toggleIssue}
          saveDraft={saveDraft}
          loadDraft={loadDraft}
        />
      }
      bottom={<ExportPanel title="导出与评审历史" rows={phraseExports} group={exportGroup} onGroupChange={setExportGroup} onSaveDraft={saveDraft} onExportAll={() => exportMock("all")} onExportPhrase={() => exportMock("phrase")} />}
      statusText={status}
    />
  );
}

function LeftPanel({ selectedPhraseId, onSelectPhrase }: { selectedPhraseId: string; onSelectPhrase: (phraseId: string) => void }) {
  return (
    <div className="panel-stack">
      <h2>项目</h2>
      <div className="tree">
        <strong>Cyber Guqin v1.0 <small>Dapu Mode</small></strong>
        <button className="active">RS_XWC_002_BAIYA_PILOT</button>
        <button>R0 Raw 审校</button><button>R1 Split 审校</button><button className="active">R2 句读听评</button>
      </div>
      <section className="editor-section">
        <h3>曲目</h3>
        {mockPieces.map((piece) => <button key={piece.piece_id} className={`wide ${piece.piece_id === "XWC" ? "active" : ""}`}>{piece.piece_id} / {piece.piece_title}<small>{piece.mock_only ? "R2A UI mock only" : "active MVP piece"}</small></button>)}
      </section>
      <section className="editor-section">
        <h3>Session</h3>
        {mockSessions.map((session) => <button key={session.recording_session_id} className={`wide ${session.current_project_session ? "active" : ""}`}>{session.recording_session_id}<small>{session.label}</small></button>)}
      </section>
      <section className="editor-section">
        <h3>Section / Phrase</h3>
        {sections.map((section) => (
          <div className="section-tree" key={section.section_id}>
            <strong>{section.section_id} {section.section_label}</strong>
            {section.phrase_ids.map((phraseId) => {
              const phrase = getPhrase(phraseId);
              return <button key={phraseId} className={`wide ${selectedPhraseId === phraseId ? "active" : ""}`} onClick={() => onSelectPhrase(phraseId)}>{phrase.phrase_id}<small>{phrase.event_range}</small></button>;
            })}
          </div>
        ))}
      </section>
      <p className="flags">review_only={String(projectFlags.review_only)} · production_grade={String(projectFlags.production_grade)} · not_render_executed=true</p>
    </div>
  );
}

function RightPanel({
  selectedPhraseId,
  selectedSectionId,
  eventRange,
  selectedVersionId,
  preferredVersionId,
  setPreferredVersionId,
  markers,
  selectedMarkerId,
  setSelectedMarkerId,
  updateMarker,
  nudge,
  review,
  setReview,
  toggleIssue,
  saveDraft,
  loadDraft,
}: {
  selectedPhraseId: string;
  selectedSectionId: string;
  eventRange: string;
  selectedVersionId: string;
  preferredVersionId: string;
  setPreferredVersionId: (versionId: string) => void;
  markers: PhraseMarker[];
  selectedMarkerId: string;
  setSelectedMarkerId: (markerId: string) => void;
  updateMarker: (patch: Partial<PhraseMarker>) => void;
  nudge: (delta: number) => void;
  review: ListeningReview;
  setReview: (review: ListeningReview) => void;
  toggleIssue: (issue: R2IssueType) => void;
  saveDraft: () => void;
  loadDraft: () => void;
}) {
  const selectedMarker = markers.find((marker) => marker.marker_id === selectedMarkerId) ?? markers[0];
  const markerLabels: { key: R2MarkerKey; label: string }[] = [
    { key: "phrase_start", label: "句头" },
    { key: "phrase_end", label: "句尾" },
    { key: "breath_point", label: "气口" },
    { key: "cadence", label: "收束" },
    { key: "section_start", label: "段落起" },
    { key: "unclear_boundary", label: "边界不明" },
  ];
  return (
    <div className="panel-stack">
      <h2>Phrase Review Editor</h2>
      <div className="info-card">
        <span>当前句读对象：{selectedPhraseId}</span>
        <code>所属 section：{selectedSectionId}</code>
        <code>event_range：{eventRange}</code>
        <code>active_version：{selectedVersionId}</code>
        <code>preferred_version：{preferredVersionId}</code>
      </div>
      <section className="editor-section">
        <h3>A. 句读标记</h3>
        <div className="button-grid">
          {markerLabels.map((item) => {
            const marker = markers.find((candidate) => candidate.marker_type === item.key);
            return <button key={item.key} className={selectedMarker?.marker_type === item.key ? "active" : ""} onClick={() => marker ? setSelectedMarkerId(marker.marker_id) : updateMarker({ marker_type: item.key, marker_label_zh: item.label })}>{item.label}<small>{item.key}</small></button>;
          })}
        </div>
        <div className="nudge-grid">{[-50, -10, -5, 5, 10, 50].map((delta) => <button key={delta} onClick={() => nudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>)}</div>
        <div className="cg-select-row">
          <select className="cg-select" value={selectedMarker?.review_status ?? "candidate"} onChange={(event) => updateMarker({ review_status: event.target.value as PhraseMarker["review_status"] })}>
            {["candidate", "accepted", "unclear", "needs_retake", "rejected"].map((status) => <option key={status} value={status}>{status}</option>)}
          </select>
          <textarea value={selectedMarker?.notes ?? ""} onChange={(event) => updateMarker({ notes: event.target.value })} />
        </div>
      </section>
      <section className="editor-section">
        <h3>B. 听评批注</h3>
        <div className="issue-grid">
          {issueOptions.map((issue) => <label key={issue.key} className={review.issue_type.includes(issue.key) ? "active-check" : ""}><input type="checkbox" checked={review.issue_type.includes(issue.key)} onChange={() => toggleIssue(issue.key)} />{issue.label}</label>)}
        </div>
        <div className="segmented">{(["low", "medium", "high"] as Severity[]).map((item) => <button key={item} className={review.severity === item ? "active" : ""} onClick={() => setReview({ ...review, severity: item })}>{item}</button>)}</div>
        <div className="cg-select-row">
          <select className="cg-select" value={preferredVersionId} onChange={(event) => { setPreferredVersionId(event.target.value); setReview({ ...review, preferred_version_id: event.target.value }); }}>
            {versions.map((version) => <option key={version.version_id} value={version.version_id}>{version.version_code} / {version.version_label_zh}</option>)}
          </select>
          <textarea value={review.comment} onChange={(event) => setReview({ ...review, comment: event.target.value })} />
          <textarea value={review.suggested_revision ?? ""} onChange={(event) => setReview({ ...review, suggested_revision: event.target.value })} />
          <input value={review.reviewer} onChange={(event) => setReview({ ...review, reviewer: event.target.value })} />
          <input value={review.reviewed_at} onChange={(event) => setReview({ ...review, reviewed_at: event.target.value })} />
        </div>
        <div className="action-row"><button className="active" onClick={saveDraft}>保存 draft</button><button onClick={loadDraft}>加载 draft</button></div>
      </section>
    </div>
  );
}

function toCanvasMarker(marker: PhraseMarker): Marker {
  return {
    id: marker.marker_id,
    key: marker.marker_id,
    label: marker.marker_label_zh,
    time: marker.time_s,
    color: markerColor(marker.marker_type),
    source: marker.source,
    review_status: marker.review_status,
    nudge_total_ms: marker.nudge_total_ms,
    notes: marker.notes,
    displayLabel: true,
    weak: marker.marker_type === "section_start" || marker.marker_type === "section_end",
  };
}

function markerColor(markerType: R2MarkerKey): Marker["color"] {
  if (markerType === "phrase_start") return "green";
  if (markerType === "phrase_end") return "purple";
  if (markerType === "breath_point") return "blue";
  if (markerType === "cadence") return "gold";
  if (markerType === "unclear_boundary") return "red";
  return "cyan";
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const rest = (seconds % 60).toFixed(3).padStart(6, "0");
  return `${minutes}:${rest}`;
}
