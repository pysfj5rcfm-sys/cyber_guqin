import { useEffect, useMemo, useState } from "react";
import { ABCDEPhrasePlayer } from "../components/ABCDEPhrasePlayer";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { R2ExportPreviewPanel } from "../components/R2ExportPreviewPanel";
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
  renderSet,
  r2SafetyFlags,
  sections,
  versions,
} from "../mock/projectReviewMock";
import type { ListeningReview, Marker, MarkerReviewStatus, PhraseMarker, R2DraftPayload, R2IssueType, R2MarkerKey, RenderPhraseAlignment, Severity } from "../types/cgVarw";

type R2PlaybackRate = 0.5 | 1 | 1.5;
type R2PlayMode = "idle" | "phrase" | "marker" | "preroll" | "sequence_abcde" | "preferred" | "ab_compare";

type R2PlaybackState = {
  isPlaying: boolean;
  currentTimeS: number;
  playbackRate: R2PlaybackRate;
  loopPhrase: boolean;
  playMode: R2PlayMode;
  sequenceQueue?: string[];
  currentQueueIndex?: number;
  playingVersionId?: string;
};

type BoundaryStatusByKey = Record<string, MarkerReviewStatus>;
type PreferredVersionByPhrase = Record<string, string>;
type QuickJudgement = "good" | "usable" | "needs_revision" | "bad";

type R2ListeningReviewDraft = {
  phrase_id: string;
  version_id: string;
  issue_type: R2IssueType[];
  severity: Severity;
  quick_judgement?: QuickJudgement;
  comment: string;
  suggested_revision: string;
  reviewer: string;
  reviewed_at: string;
  updated_at?: string;
};

type ListeningReviewByKey = Record<string, R2ListeningReviewDraft>;

type R2DraftPayloadWithReviewState = R2DraftPayload & {
  preferred_version_by_phrase?: PreferredVersionByPhrase;
  listening_review_by_key?: ListeningReviewByKey;
};

type ProgressOverview = {
  totalPhraseCount: number;
  reviewedPhraseCount: number;
  pendingPhraseCount: number;
  unclearBoundaryCount: number;
  needsRetakeCount: number;
  preferredVersionCount: number;
};

const draftKey = `cg-varw:r2:${renderSet.render_set_id}:draft`;
const backendStatus = "后端已连接，当前使用合成演示 Render 根目录。";

export function R2ProjectReviewPage() {
  const [activePhraseId, setActivePhraseId] = useState("PHRASE_03");
  const [activeVersionId, setActiveVersionId] = useState("B_PHRASE");
  const [preferredVersionByPhrase, setPreferredVersionByPhrase] = useState<PreferredVersionByPhrase>(() => ({ PHRASE_03: "B_PHRASE" }));
  const [markers, setMarkers] = useState<PhraseMarker[]>(() => makePhraseMarkers("PHRASE_03", "B_PHRASE"));
  const [selectedMarkerId, setSelectedMarkerId] = useState("PHRASE_03_B_PHRASE_cadence");
  const [boundaryStatusByKey, setBoundaryStatusByKey] = useState<BoundaryStatusByKey>(() => makeInitialBoundaryStatusByKey());
  const [listeningReviewByKey, setListeningReviewByKey] = useState<ListeningReviewByKey>(() => ({
    [phraseVersionKey("PHRASE_03", "B_PHRASE")]: draftFromListeningReview(defaultListeningReview),
  }));
  const [exportGroup, setExportGroup] = useState("全部");
  const [lastActionMessage, setLastActionMessage] = useState(`已切换到 PHRASE_03 · ${versionLabel("B_PHRASE")}`);
  const [playback, setPlayback] = useState<R2PlaybackState>({
    isPlaying: false,
    currentTimeS: getAlignment("PHRASE_03", "B_PHRASE").start_s,
    playbackRate: 1,
    loopPhrase: false,
    playMode: "idle",
  });

  const activePhrase = getPhrase(activePhraseId);
  const activeSection = getSection(activePhrase.section_id);
  const reviewedAlignments = useMemo(() => phraseAlignments.map((alignment) => ({
    ...alignment,
    review_status: boundaryStatusByKey[boundaryKey(alignment.phrase_id, alignment.version_id)] ?? alignment.review_status,
  })), [boundaryStatusByKey]);
  const activeAlignment = reviewedAlignments.find((alignment) => alignment.phrase_id === activePhraseId && alignment.version_id === activeVersionId) ?? getAlignment(activePhraseId, activeVersionId);
  const boundaryStatus = activeAlignment.review_status;
  const activeVersion = versions.find((version) => version.version_id === activeVersionId) ?? versions[1];
  const alignmentsForPhrase = reviewedAlignments.filter((alignment) => alignment.phrase_id === activePhraseId);
  const preferredVersionId = preferredVersionByPhrase[activePhraseId];
  const activeReviewDraft = listeningReviewByKey[phraseVersionKey(activePhraseId, activeVersionId)] ?? makeReviewDraft(activePhraseId, activeVersionId);
  const activeListeningReview = toListeningReview(activeReviewDraft, activeSection.section_id, activePhrase.event_range, preferredVersionId);
  const progress = useMemo(
    () => deriveProgressOverview(reviewedAlignments, preferredVersionByPhrase, listeningReviewByKey),
    [reviewedAlignments, preferredVersionByPhrase, listeningReviewByKey],
  );
  const selectedMarker = markers.find((marker) => marker.marker_id === selectedMarkerId) ?? markers[0];
  const playbackRange = getAlignment(activePhraseId, playback.playingVersionId ?? activeVersionId);
  const canvasMarkers = useMemo(() => markers.map(toCanvasMarker), [markers]);

  useEffect(() => {
    if (!playback.isPlaying) return;
    const timer = window.setInterval(() => {
      setPlayback((current) => {
        const currentIndex = current.currentQueueIndex ?? 0;
        const currentVersionId = current.playingVersionId ?? current.sequenceQueue?.[currentIndex] ?? activeVersionId;
        const range = getAlignment(activePhraseId, currentVersionId);
        const nextTime = Number((current.currentTimeS + 0.25 * current.playbackRate).toFixed(3));
        if (nextTime < range.end_s) return { ...current, currentTimeS: nextTime };
        if (current.loopPhrase && (!current.sequenceQueue || current.sequenceQueue.length <= 1)) {
          return { ...current, currentTimeS: range.start_s };
        }
        if (current.sequenceQueue && currentIndex < current.sequenceQueue.length - 1) {
          const nextIndex = currentIndex + 1;
          const nextVersionId = current.sequenceQueue[nextIndex];
          const nextRange = getAlignment(activePhraseId, nextVersionId);
          return { ...current, currentQueueIndex: nextIndex, playingVersionId: nextVersionId, currentTimeS: nextRange.start_s };
        }
        return { ...current, isPlaying: false, currentTimeS: range.end_s, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined };
      });
    }, 250);
    return () => window.clearInterval(timer);
  }, [activePhraseId, activeVersionId, playback.isPlaying]);

  function ensureReviewDraft(phraseId: string, versionId: string) {
    const key = phraseVersionKey(phraseId, versionId);
    setListeningReviewByKey((current) => current[key] ? current : {
      ...current,
      [key]: makeReviewDraft(phraseId, versionId),
    });
  }

  function selectPhrase(phraseId: string) {
    const nextMarkers = makePhraseMarkers(phraseId, activeVersionId);
    const alignment = getAlignment(phraseId, activeVersionId);
    setActivePhraseId(phraseId);
    setMarkers(nextMarkers);
    setSelectedMarkerId(defaultMarkerId(nextMarkers));
    setPlayback((current) => ({ ...current, isPlaying: false, currentTimeS: alignment.start_s, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
    ensureReviewDraft(phraseId, activeVersionId);
    setLastActionMessage(`已切换到 ${phraseId} · ${versionLabel(activeVersionId)}`);
  }

  function selectVersion(versionId: string) {
    const nextMarkers = makePhraseMarkers(activePhraseId, versionId);
    const alignment = getAlignment(activePhraseId, versionId);
    setActiveVersionId(versionId);
    setMarkers(nextMarkers);
    setSelectedMarkerId(defaultMarkerId(nextMarkers));
    setPlayback((current) => ({ ...current, isPlaying: false, currentTimeS: alignment.start_s, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
    ensureReviewDraft(activePhraseId, versionId);
    setLastActionMessage(`已切换到 ${activePhraseId} · ${versionLabel(versionId)}`);
  }

  function setPreferred(versionId: string) {
    setPreferredVersionByPhrase((current) => ({ ...current, [activePhraseId]: versionId }));
    setLastActionMessage(`已选择偏好版本 · ${activePhraseId} · ${versionLabel(versionId)}`);
  }

  function playVersion(versionId: string) {
    const alignment = getAlignment(activePhraseId, versionId);
    if (versionId !== activeVersionId) {
      setActiveVersionId(versionId);
      setMarkers(makePhraseMarkers(activePhraseId, versionId));
      setSelectedMarkerId(defaultMarkerId(makePhraseMarkers(activePhraseId, versionId)));
      ensureReviewDraft(activePhraseId, versionId);
    }
    setPlayback((current) => ({ ...current, isPlaying: true, currentTimeS: alignment.start_s, playMode: "phrase", sequenceQueue: [versionId], currentQueueIndex: 0, playingVersionId: versionId }));
    setLastActionMessage(`播放 ${activePhraseId} · ${versionLabel(versionId)}`);
  }

  function updateMarker(patch: Partial<PhraseMarker>) {
    setMarkers((current) => current.map((marker) => marker.marker_id === selectedMarkerId ? { ...marker, ...patch } : marker));
    if (patch.review_status) setLastActionMessage(`已更新标记状态 · ${statusLabel(patch.review_status)}`);
  }

  function nudgeMarker(deltaMs: number) {
    setMarkers((current) => current.map((marker) => marker.marker_id === selectedMarkerId ? {
      ...marker,
      time_s: Math.max(0, Number((marker.time_s + deltaMs / 1000).toFixed(3))),
      nudge_total_ms: marker.nudge_total_ms + deltaMs,
    } : marker));
    setLastActionMessage(`已微调 ${selectedMarker?.marker_label_zh ?? "标记"} ${deltaMs > 0 ? "+" : ""}${deltaMs}ms`);
  }

  function updateBoundaryStatus(status: MarkerReviewStatus) {
    setBoundaryStatusByKey((current) => ({
      ...current,
      [boundaryKey(activePhraseId, activeVersionId)]: status,
    }));
    setLastActionMessage(`${activePhraseId} · ${versionLabel(activeVersionId)} 边界状态已更新为${statusLabel(status)}`);
  }

  function updateReviewDraft(patch: Partial<R2ListeningReviewDraft>) {
    const key = phraseVersionKey(activePhraseId, activeVersionId);
    setListeningReviewByKey((current) => {
      const base = current[key] ?? makeReviewDraft(activePhraseId, activeVersionId);
      return {
        ...current,
        [key]: {
          ...base,
          ...patch,
          phrase_id: activePhraseId,
          version_id: activeVersionId,
          updated_at: new Date().toISOString(),
        },
      };
    });
  }

  function toggleIssue(issue: R2IssueType) {
    const issueType = activeReviewDraft.issue_type.includes(issue)
      ? activeReviewDraft.issue_type.filter((item) => item !== issue)
      : [...activeReviewDraft.issue_type, issue];
    updateReviewDraft({ issue_type: issueType });
  }

  function saveDraft() {
    const payload: R2DraftPayloadWithReviewState = {
      render_set_id: renderSet.render_set_id,
      selected_phrase_id: activePhraseId,
      selected_version_id: activeVersionId,
      preferred_version_id: preferredVersionId,
      phrase_markers: markers,
      phrase_alignments: reviewedAlignments,
      listening_review: { ...activeListeningReview, reviewed_at: activeListeningReview.reviewed_at || new Date().toISOString() },
      preferred_version_by_phrase: preferredVersionByPhrase,
      listening_review_by_key: listeningReviewByKey,
      saved_at: new Date().toISOString(),
      ...r2SafetyFlags,
    };
    localStorage.setItem(draftKey, JSON.stringify(payload));
    setLastActionMessage("draft 已保存");
  }

  function loadDraft() {
    const raw = localStorage.getItem(draftKey);
    if (!raw) {
      setLastActionMessage("未找到 R2 draft");
      return;
    }
    try {
      const payload = JSON.parse(raw) as R2DraftPayloadWithReviewState;
      const versionId = payload.selected_version_id;
      const phraseId = payload.selected_phrase_id;
      const alignment = getAlignment(phraseId, versionId);
      setActivePhraseId(phraseId);
      setActiveVersionId(versionId);
      setPreferredVersionByPhrase(payload.preferred_version_by_phrase ?? (payload.preferred_version_id ? { [phraseId]: payload.preferred_version_id } : {}));
      setMarkers(payload.phrase_markers);
      setSelectedMarkerId(defaultMarkerId(payload.phrase_markers));
      setBoundaryStatusByKey(makeBoundaryStatusByKey(payload.phrase_alignments));
      setListeningReviewByKey(payload.listening_review_by_key ?? {
        [phraseVersionKey(payload.listening_review.phrase_id, payload.listening_review.active_version_id)]: draftFromListeningReview(payload.listening_review),
      });
      setPlayback((current) => ({ ...current, isPlaying: false, currentTimeS: alignment.start_s, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
      setLastActionMessage("已加载 R2 draft");
    } catch (error) {
      setLastActionMessage(`R2 draft 加载失败：${error instanceof Error ? error.message : String(error)}`);
    }
  }

  function seekMock(time: number, playMode: R2PlayMode, message: string, queue?: string[]) {
    setPlayback((current) => ({
      ...current,
      isPlaying: true,
      currentTimeS: Number(time.toFixed(3)),
      playMode,
      sequenceQueue: queue,
      currentQueueIndex: queue ? 0 : undefined,
      playingVersionId: queue?.[0],
    }));
    setLastActionMessage(message);
  }

  function togglePlayPause() {
    setPlayback((current) => ({ ...current, isPlaying: !current.isPlaying, playMode: current.isPlaying ? "idle" : "phrase" }));
    setLastActionMessage(playback.isPlaying ? `已暂停 · ${activePhraseId}` : `播放中 · ${activePhraseId} · ${versionLabel(activeVersionId)}`);
  }

  function playFromPhraseStart() {
    seekMock(activeAlignment.start_s, "phrase", `从句头播放 · ${activePhraseId} · ${versionLabel(activeVersionId)}`, [activeVersionId]);
  }

  function playFromSelectedMarker() {
    seekMock(selectedMarker?.time_s ?? activeAlignment.start_s, "marker", `从当前标记播放 · ${selectedMarker?.marker_label_zh ?? "句头"}`, [activeVersionId]);
  }

  function playPreroll300ms() {
    const markerTime = selectedMarker?.time_s ?? activeAlignment.start_s;
    seekMock(Math.max(activeAlignment.start_s, markerTime - 0.3), "preroll", `前滚 300ms · ${activePhraseId}`, [activeVersionId]);
  }

  function toggleLoopPhrase() {
    setPlayback((current) => ({ ...current, loopPhrase: !current.loopPhrase }));
    setLastActionMessage(playback.loopPhrase ? `已关闭循环 · ${activePhraseId}` : `循环当前 phrase · ${activePhraseId}`);
  }

  function changeRate(rate: R2PlaybackRate) {
    setPlayback((current) => ({ ...current, playbackRate: rate }));
    setLastActionMessage(`播放速度 ${rate}x · ${activePhraseId}`);
  }

  function jumpPhrase(direction: -1 | 1) {
    const currentIndex = phrases.findIndex((phrase) => phrase.phrase_id === activePhraseId);
    const nextPhrase = phrases[Math.min(phrases.length - 1, Math.max(0, currentIndex + direction))];
    if (nextPhrase && nextPhrase.phrase_id !== activePhraseId) selectPhrase(nextPhrase.phrase_id);
  }

  function playSequenceABCDE() {
    const queue = versions.map((version) => version.version_id);
    const first = getAlignment(activePhraseId, queue[0]);
    seekMock(first.start_s, "sequence_abcde", `顺播 A→B→C→D→E：${activePhraseId}`, queue);
  }

  function playPreferredVersion() {
    if (!preferredVersionId) {
      setLastActionMessage(`当前 phrase 尚未设置偏好版本：${activePhraseId}`);
      setPlayback((current) => ({ ...current, isPlaying: false, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
      return;
    }
    const alignment = getAlignment(activePhraseId, preferredVersionId);
    seekMock(alignment.start_s, "preferred", `正在播放偏好版本：${versionLabel(preferredVersionId)}`, [preferredVersionId]);
  }

  function playABCompare() {
    const queue = ["A_LITERAL", "B_PHRASE"];
    const first = getAlignment(activePhraseId, queue[0]);
    seekMock(first.start_s, "ab_compare", `A/B 对比播放：A 直译谱面版 → B 句法呼吸版`, queue);
  }

  return (
    <AppShell
      mode="R2"
      left={<LeftPanel selectedPhraseId={activePhraseId} onSelectPhrase={selectPhrase} progress={progress} />}
      main={
        <div className="r2-main">
          <div className="work-title tight">
            <div>
              <h1>XWC / 仙翁操 · R2 句读听评</h1>
              <p>当前比较：{activeSection.section_id} / {activePhrase.phrase_id} / {activePhrase.event_range}</p>
              <p>按 phrase_id / event_range 对齐，不按绝对时间切换。</p>
            </div>
            <span className="badge badge-blue" title={activeVersionId}>{versionLabel(activeVersionId)}</span>
          </div>
          <ABCDEPhrasePlayer
            versions={versions}
            alignments={alignmentsForPhrase}
            selectedVersionId={activeVersionId}
            preferredVersionId={preferredVersionId}
            onSelect={selectVersion}
            onSetPreferred={setPreferred}
            onPlay={playVersion}
          />
          <section className="work-area phrase-area">
            <h2>当前 phrase 波形 / 频谱 · {activeVersion.version_code} {activeVersion.version_label_zh}</h2>
            <AudioCanvas
              markers={canvasMarkers}
              duration={activeVersion.duration_s}
              selectedKey={selectedMarkerId}
              onSelect={setSelectedMarkerId}
              audioFileName={`${versionLabel(activeVersionId)} mock waveform · ${activePhraseId}`}
              waveformPeaks={activeVersion.waveform_preview}
            />
            <div className="event-strip"><span>{activePhrase.start_event_id}</span><span>{activePhrase.event_range}</span><span>{activePhrase.end_event_id}</span></div>
            <R2PlaybackControls
              playback={playback}
              phraseEndS={playbackRange.end_s}
              onPlayPause={togglePlayPause}
              onPhraseStart={playFromPhraseStart}
              onMarkerStart={playFromSelectedMarker}
              onPreroll={playPreroll300ms}
              onToggleLoop={toggleLoopPhrase}
              onRateChange={changeRate}
              onPrevPhrase={() => jumpPhrase(-1)}
              onNextPhrase={() => jumpPhrase(1)}
            />
            <div className="playback-bar r2-playback-bar">
              <button onClick={playSequenceABCDE}>顺播 A→B→C→D→E</button>
              <button onClick={playPreferredVersion}>播放偏好版本</button>
              <button onClick={playABCompare}>A/B 对比播放</button>
              <strong className="clock">{activeAlignment.start_s.toFixed(3)}<small>- {activeAlignment.end_s.toFixed(3)}s</small></strong>
            </div>
          </section>
        </div>
      }
      right={
        <RightPanel
          activePhraseId={activePhraseId}
          activeSection={activeSection}
          eventRange={activePhrase.event_range}
          activeVersionId={activeVersionId}
          preferredVersionId={preferredVersionId}
          setPreferredVersionId={setPreferred}
          markers={markers}
          selectedMarkerId={selectedMarkerId}
          setSelectedMarkerId={setSelectedMarkerId}
          updateMarker={updateMarker}
          nudge={nudgeMarker}
          review={activeReviewDraft}
          updateReview={updateReviewDraft}
          toggleIssue={toggleIssue}
          saveDraft={saveDraft}
          loadDraft={loadDraft}
          boundaryStatus={boundaryStatus}
          setBoundaryStatus={updateBoundaryStatus}
        />
      }
      bottom={
        <R2ExportPreviewPanel
          title="导出与评审历史"
          rows={phraseExports}
          group={exportGroup}
          sections={sections}
          phrases={phrases}
          alignments={reviewedAlignments}
          markers={markers}
          review={activeListeningReview}
          preferredVersionByPhrase={preferredVersionByPhrase}
          listeningReviewByKey={listeningReviewByKey}
          activePhraseId={activePhraseId}
          activeVersionId={activeVersionId}
          preferredVersionId={preferredVersionId}
          boundaryStatus={boundaryStatus}
          onGroupChange={setExportGroup}
          onSaveDraft={saveDraft}
          onExportAll={() => setLastActionMessage("已导出全部")}
          onExportPhrase={() => setLastActionMessage("已导出当前 phrase")}
          onPreview={(file) => setLastActionMessage(`已预览 ${file}`)}
        />
      }
      statusText={backendStatus}
      detailText={lastActionMessage}
    />
  );
}

function LeftPanel({
  selectedPhraseId,
  onSelectPhrase,
  progress,
}: {
  selectedPhraseId: string;
  onSelectPhrase: (phraseId: string) => void;
  progress: ProgressOverview;
}) {
  return (
    <div className="panel-stack">
      <h2>项目</h2>
      <div className="tree">
        <strong>Cyber Guqin v1.0 <small>Dapu Mode</small></strong>
        <button className="active">RS_XWC_002_BAIYA_PILOT</button>
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
      <section className="phrase-rail">
        <h3>本曲进度概览</h3>
        <div><span>已审 phrase</span><b>{progress.reviewedPhraseCount} / {progress.totalPhraseCount}</b><i style={{ width: percentWidth(progress.reviewedPhraseCount, progress.totalPhraseCount) }} /></div>
        <div><span>待审 phrase</span><b>{progress.pendingPhraseCount} / {progress.totalPhraseCount}</b><i className="gold-line" style={{ width: percentWidth(progress.pendingPhraseCount, progress.totalPhraseCount) }} /></div>
        <div><span>边界不明</span><b>{progress.unclearBoundaryCount}</b><i className="gold-line" style={{ width: percentWidth(progress.unclearBoundaryCount, phraseAlignments.length) }} /></div>
        <div><span>需重录</span><b>{progress.needsRetakeCount}</b><i className="gold-line" style={{ width: percentWidth(progress.needsRetakeCount, phraseAlignments.length) }} /></div>
        <div><span>偏好已设</span><b>{progress.preferredVersionCount} / {progress.totalPhraseCount}</b><i style={{ width: percentWidth(progress.preferredVersionCount, progress.totalPhraseCount) }} /></div>
      </section>
    </div>
  );
}

function RightPanel({
  activePhraseId,
  activeSection,
  eventRange,
  activeVersionId,
  preferredVersionId,
  setPreferredVersionId,
  markers,
  selectedMarkerId,
  setSelectedMarkerId,
  updateMarker,
  nudge,
  review,
  updateReview,
  toggleIssue,
  saveDraft,
  loadDraft,
  boundaryStatus,
  setBoundaryStatus,
}: {
  activePhraseId: string;
  activeSection: ReturnType<typeof getSection>;
  eventRange: string;
  activeVersionId: string;
  preferredVersionId?: string;
  setPreferredVersionId: (versionId: string) => void;
  markers: PhraseMarker[];
  selectedMarkerId: string;
  setSelectedMarkerId: (markerId: string) => void;
  updateMarker: (patch: Partial<PhraseMarker>) => void;
  nudge: (delta: number) => void;
  review: R2ListeningReviewDraft;
  updateReview: (patch: Partial<R2ListeningReviewDraft>) => void;
  toggleIssue: (issue: R2IssueType) => void;
  saveDraft: () => void;
  loadDraft: () => void;
  boundaryStatus: MarkerReviewStatus;
  setBoundaryStatus: (status: MarkerReviewStatus) => void;
}) {
  const phraseMarkers = markers.filter((marker) => ["phrase_start", "phrase_end", "breath_point", "cadence"].includes(marker.marker_type));
  const selectedMarker = phraseMarkers.find((marker) => marker.marker_id === selectedMarkerId) ?? phraseMarkers[0];
  const markerLabels: { key: R2MarkerKey; label: string }[] = [
    { key: "phrase_start", label: "句头" },
    { key: "phrase_end", label: "句尾" },
    { key: "breath_point", label: "气口" },
    { key: "cadence", label: "收束" },
  ];
  return (
    <div className="panel-stack">
      <h2>句读听评编辑</h2>
      <div className="info-card">
        <span>当前句读对象：{activePhraseId}</span>
        <span>所属 section：{activeSection.section_id} {activeSection.section_label}</span>
        <code>event_range：{eventRange}</code>
        <span>当前版本：{versionLabel(activeVersionId)}</span>
        <span>偏好版本：{preferredVersionId ? versionLabel(preferredVersionId) : "未设置偏好"}</span>
      </div>
      <section className="editor-section">
        <h3>A. 句读标记</h3>
        <div className="button-grid">
          {markerLabels.map((item) => {
            const marker = phraseMarkers.find((candidate) => candidate.marker_type === item.key);
            return <button key={item.key} className={selectedMarker?.marker_type === item.key ? "active" : ""} title={item.key} onClick={() => marker && setSelectedMarkerId(marker.marker_id)}>{item.label}</button>;
          })}
        </div>
        <div className="info-card marker-info-card">
          <span>当前标记：{selectedMarker?.marker_label_zh ?? "未选择"}</span>
          <b>{(selectedMarker?.time_s ?? 0).toFixed(3)}s</b>
          <span>状态：{statusLabel(selectedMarker?.review_status ?? "candidate")}</span>
        </div>
        <div className="nudge-grid">{[-50, -10, -5, 5, 10, 50].map((delta) => <button key={delta} onClick={() => nudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>)}</div>
        <div className="cg-select-row">
          <select className="cg-select" value={selectedMarker?.review_status ?? "candidate"} onChange={(event) => updateMarker({ review_status: event.target.value as PhraseMarker["review_status"] })}>
            {(["candidate", "accepted", "unclear", "needs_retake", "rejected"] as MarkerReviewStatus[]).map((status) => <option key={status} value={status}>{statusLabel(status)}</option>)}
          </select>
          <textarea value={selectedMarker?.notes ?? ""} onChange={(event) => updateMarker({ notes: event.target.value })} />
        </div>
      </section>
      <section className="editor-section">
        <h3>Section 上下文</h3>
        <div className="context-summary">
          <span>所属 section：<b>{activeSection.section_id} {activeSection.section_label}</b></span>
          <span>section event_range：<b>{activeSection.event_range}</b></span>
          <span>本 section phrase 数：<b>{activeSection.phrase_ids.length}</b></span>
          <span>当前 phrase 序号：<b>{activeSection.phrase_ids.indexOf(activePhraseId) + 1} / {activeSection.phrase_ids.length}</b></span>
        </div>
      </section>
      <section className="editor-section">
        <h3>边界状态</h3>
        <div className="segmented boundary-segmented">
          {(["candidate", "accepted", "unclear", "needs_retake", "rejected"] as MarkerReviewStatus[]).map((status) => <button key={status} className={boundaryStatus === status ? "active" : ""} onClick={() => setBoundaryStatus(status)}>{statusLabel(status)}</button>)}
        </div>
      </section>
      <section className="editor-section">
        <h3>B. 当前版本听评批注</h3>
        <div className="review-subsection">
          <h4>当前评审对象</h4>
          <span>当前 phrase：<b>{activePhraseId}</b></span>
          <span>当前 version：<b>{versionLabel(activeVersionId)}</b></span>
          <span>当前 preferred：<b>{preferredVersionId ? versionLabel(preferredVersionId) : "未设置偏好"}</b></span>
          <select className="cg-select" value={preferredVersionId ?? ""} onChange={(event) => event.target.value && setPreferredVersionId(event.target.value)}>
            <option value="">未设置偏好</option>
            {versions.map((version) => <option key={version.version_id} value={version.version_id}>{version.version_code} {version.version_label_zh}</option>)}
          </select>
        </div>
        <div className="review-subsection">
          <h4>快速评价</h4>
          <div className="segmented">
            {([
              ["good", "很好"],
              ["usable", "可用"],
              ["needs_revision", "需修"],
              ["bad", "不可用"],
            ] as [QuickJudgement, string][]).map(([value, label]) => <button key={value} className={review.quick_judgement === value ? "active" : ""} onClick={() => updateReview({ quick_judgement: value })}>{label}</button>)}
          </div>
        </div>
        <div className="review-subsection">
          <h4>问题类型</h4>
          <div className="issue-grid">
            {issueOptions.map((issue) => <label key={issue.key} className={review.issue_type.includes(issue.key) ? "active-check" : ""}><input type="checkbox" checked={review.issue_type.includes(issue.key)} onChange={() => toggleIssue(issue.key)} />{issue.label}</label>)}
          </div>
        </div>
        <div className="review-subsection">
          <h4>严重程度</h4>
          <div className="segmented">{(["low", "medium", "high"] as Severity[]).map((item) => <button key={item} className={review.severity === item ? "active" : ""} onClick={() => updateReview({ severity: item })}>{severityLabel(item)}</button>)}</div>
        </div>
        <div className="review-subsection">
          <h4>文字批注</h4>
          <textarea value={review.comment} onChange={(event) => updateReview({ comment: event.target.value })} />
        </div>
        <div className="review-subsection">
          <h4>修订建议</h4>
          <textarea value={review.suggested_revision} onChange={(event) => updateReview({ suggested_revision: event.target.value })} />
        </div>
        <div className="action-row"><button className="active" onClick={saveDraft}>保存 draft</button><button onClick={loadDraft}>加载 draft</button></div>
      </section>
    </div>
  );
}

function R2PlaybackControls({
  playback,
  phraseEndS,
  onPlayPause,
  onPhraseStart,
  onMarkerStart,
  onPreroll,
  onToggleLoop,
  onRateChange,
  onPrevPhrase,
  onNextPhrase,
}: {
  playback: R2PlaybackState;
  phraseEndS: number;
  onPlayPause: () => void;
  onPhraseStart: () => void;
  onMarkerStart: () => void;
  onPreroll: () => void;
  onToggleLoop: () => void;
  onRateChange: (rate: R2PlaybackRate) => void;
  onPrevPhrase: () => void;
  onNextPhrase: () => void;
}) {
  return (
    <div className="playback-bar r2-basic-playback">
      <button className="play-button" onClick={onPlayPause}>{playback.isPlaying ? "暂停" : "播放"}<span>{playModeLabel(playback.playMode)}</span></button>
      <button onClick={onPhraseStart}>从句头播放</button>
      <button onClick={onMarkerStart}>从当前标记播放</button>
      <button onClick={onPreroll}>前滚 300ms</button>
      <button className={playback.loopPhrase ? "active" : ""} onClick={onToggleLoop}>循环当前 phrase</button>
      <button onClick={onPrevPhrase}>上一 phrase</button>
      <button onClick={onNextPhrase}>下一 phrase</button>
      <strong className="clock">{formatTime(playback.currentTimeS)}<small>/ {formatTime(phraseEndS)} · {playback.playingVersionId ? versionLabel(playback.playingVersionId) : "当前版本"}</small></strong>
      <span className="speed-label">播放速度</span>
      {([0.5, 1, 1.5] as R2PlaybackRate[]).map((rate) => (
        <button key={rate} className={playback.playbackRate === rate ? "active" : ""} onClick={() => onRateChange(rate)}>
          {rate}x
        </button>
      ))}
    </div>
  );
}

function toCanvasMarker(marker: PhraseMarker): Marker {
  return {
    id: marker.marker_id,
    key: marker.marker_id,
    label: `${marker.marker_label_zh} · ${statusLabel(marker.review_status)}`,
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

function boundaryKey(phraseId: string, versionId: string) {
  return `${phraseId}::${versionId}`;
}

function phraseVersionKey(phraseId: string, versionId: string) {
  return `${phraseId}::${versionId}`;
}

function makeInitialBoundaryStatusByKey() {
  return makeBoundaryStatusByKey(phraseAlignments);
}

function makeBoundaryStatusByKey(alignments: RenderPhraseAlignment[]) {
  return alignments.reduce<BoundaryStatusByKey>((result, alignment) => {
    result[boundaryKey(alignment.phrase_id, alignment.version_id)] = alignment.review_status;
    return result;
  }, {});
}

function makeReviewDraft(phraseId: string, versionId: string): R2ListeningReviewDraft {
  return {
    phrase_id: phraseId,
    version_id: versionId,
    issue_type: [],
    severity: "low",
    comment: "",
    suggested_revision: "",
    reviewer: defaultListeningReview.reviewer,
    reviewed_at: "",
  };
}

function draftFromListeningReview(review: ListeningReview): R2ListeningReviewDraft {
  return {
    phrase_id: review.phrase_id,
    version_id: review.active_version_id,
    issue_type: review.issue_type,
    severity: review.severity,
    quick_judgement: review.issue_type.includes("good") ? "good" : undefined,
    comment: review.comment,
    suggested_revision: review.suggested_revision ?? "",
    reviewer: review.reviewer,
    reviewed_at: review.reviewed_at,
    updated_at: review.reviewed_at,
  };
}

function toListeningReview(review: R2ListeningReviewDraft, sectionId: string, eventRange: string, preferredVersionId?: string): ListeningReview {
  return {
    ...defaultListeningReview,
    review_id: `R2_REVIEW_${review.phrase_id}_${review.version_id}`,
    phrase_id: review.phrase_id,
    section_id: sectionId,
    event_range: eventRange,
    active_version_id: review.version_id,
    preferred_version_id: preferredVersionId,
    issue_type: review.issue_type,
    severity: review.severity,
    comment: review.comment,
    suggested_revision: review.suggested_revision,
    reviewer: review.reviewer,
    reviewed_at: review.reviewed_at,
  };
}

function deriveProgressOverview(
  alignments: RenderPhraseAlignment[],
  preferredVersionByPhrase: PreferredVersionByPhrase,
  listeningReviewByKey: ListeningReviewByKey,
): ProgressOverview {
  const phraseIds = phrases.map((phrase) => phrase.phrase_id);
  const reviewedPhraseCount = phraseIds.filter((phraseId) => (
    alignments.some((alignment) => alignment.phrase_id === phraseId && alignment.review_status === "accepted")
    || Object.values(listeningReviewByKey).some((review) => review.phrase_id === phraseId && (
      review.issue_type.length > 0
      || Boolean(review.quick_judgement)
      || review.comment.trim().length > 0
      || review.suggested_revision.trim().length > 0
    ))
  )).length;
  return {
    totalPhraseCount: phraseIds.length,
    reviewedPhraseCount,
    pendingPhraseCount: phraseIds.length - reviewedPhraseCount,
    unclearBoundaryCount: alignments.filter((alignment) => alignment.review_status === "unclear").length,
    needsRetakeCount: alignments.filter((alignment) => alignment.review_status === "needs_retake").length,
    preferredVersionCount: phraseIds.filter((phraseId) => Boolean(preferredVersionByPhrase[phraseId])).length,
  };
}

function percentWidth(value: number, total: number) {
  if (total <= 0) return "0%";
  return `${Math.min(100, Math.round((value / total) * 100))}%`;
}

function defaultMarkerId(nextMarkers: PhraseMarker[]) {
  return nextMarkers.find((marker) => marker.marker_type === "cadence")?.marker_id ?? nextMarkers[0]?.marker_id ?? "";
}

function versionLabel(versionId: string) {
  const version = versions.find((item) => item.version_id === versionId);
  return version ? `${version.version_code} ${version.version_label_zh}` : versionId;
}

function statusLabel(status: MarkerReviewStatus) {
  return {
    candidate: "待确认",
    accepted: "已确认",
    unclear: "待复核",
    needs_retake: "需重录",
    rejected: "已排除",
  }[status];
}

function severityLabel(severity: Severity) {
  return { low: "低", medium: "中", high: "高" }[severity];
}

function playModeLabel(mode: R2PlayMode) {
  return {
    idle: "mock 已暂停",
    phrase: "phrase 播放",
    marker: "marker 播放",
    preroll: "前滚播放",
    sequence_abcde: "A→B→C→D→E",
    preferred: "偏好版本",
    ab_compare: "A/B 对比",
  }[mode];
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const rest = (seconds % 60).toFixed(3).padStart(6, "0");
  return `${minutes}:${rest}`;
}
