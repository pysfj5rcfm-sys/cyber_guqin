import { useEffect, useMemo, useRef, useState } from "react";
import { ABCDEPhrasePlayer } from "../components/ABCDEPhrasePlayer";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { apiBase, loadR2PhraseAlignments, loadR2Phrases, loadR2RenderSets, loadR2Versions } from "../api/cgVarwApi";
import { issueOptions, mockPieces, mockSessions, phraseAlignments as mockAlignments, phrases as mockPhrases, renderSet as mockRenderSet, sections as mockSections, versions as mockVersions } from "../mock/projectReviewMock";
import type { Marker, MarkerReviewStatus, PhraseDefinition, RenderPhraseAlignment, RenderSet, RenderVersion, R2IssueType, Section, Severity } from "../types/cgVarw";

type DataSource = "api" | "mock";
type R2PlaybackRate = 0.5 | 1 | 1.5;
type PlayMode = "idle" | "phrase" | "sequence_abcd" | "preferred";

type ReviewDraft = {
  phrase_id: string;
  event_range: string;
  issue_type: R2IssueType[];
  severity: Severity;
  preferred_version: string;
  comment: string;
  suggested_revision: string;
  reviewer_role: "human";
  gpt_review_pending: true;
  e_revision_plan_generated: false;
};

type DraftByPhrase = Record<string, ReviewDraft>;
type DraftExportReview = Omit<ReviewDraft, "preferred_version"> & {
  phrase_order: number;
  preferred_version: string | null;
};
type DraftExportPayload = {
  render_set_id: string;
  data_source: "real_api" | "mock_fallback";
  reviewer_role: "human";
  gpt_review_pending: true;
  e_revision_plan_generated: false;
  selected_phrase_id: string | null;
  selected_event_range: string | null;
  draft_count: number;
  reviews: DraftExportReview[];
};

type PlaybackState = {
  isPlaying: boolean;
  currentTimeS: number;
  playMode: PlayMode;
  playingVersionId?: string;
  playbackRate: R2PlaybackRate;
};

const VERSION_ORDER = ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC"];
const reviewStatuses: MarkerReviewStatus[] = ["candidate", "accepted", "unclear", "needs_retake", "rejected"];

export function R2ProjectReviewPage() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const stopTimerRef = useRef<number | null>(null);
  const [dataSource, setDataSource] = useState<DataSource>("mock");
  const [backendMessage, setBackendMessage] = useState("正在尝试读取 R2 render set API...");
  const [renderSet, setRenderSet] = useState<RenderSet>(mockRenderSet);
  const [versions, setVersions] = useState<RenderVersion[]>(abcdVersions(mockVersions));
  const [sections, setSections] = useState<Section[]>(mockSections);
  const [phrases, setPhrases] = useState<PhraseDefinition[]>(mockPhrases);
  const [alignments, setAlignments] = useState<RenderPhraseAlignment[]>(abcdAlignments(mockAlignments));
  const [activePhraseId, setActivePhraseId] = useState(mockPhrases[0]?.phrase_id ?? "");
  const [activeVersionId, setActiveVersionId] = useState("A_LITERAL");
  const [drafts, setDrafts] = useState<DraftByPhrase>({});
  const [boundaryStatus, setBoundaryStatus] = useState<Record<string, MarkerReviewStatus>>({});
  const [lastActionMessage, setLastActionMessage] = useState("R2 模拟数据兜底已就绪");
  const [playback, setPlayback] = useState<PlaybackState>({ isPlaying: false, currentTimeS: 0, playMode: "idle", playbackRate: 1 });

  useEffect(() => {
    let cancelled = false;
    async function loadRealRenderSet() {
      try {
        const renderSets = await loadR2RenderSets();
        const real = renderSets.find(isRealRenderSet);
        if (!real) throw new Error("后端未返回真实 experimental render set");
        const [nextVersions, phraseData, nextAlignments] = await Promise.all([
          loadR2Versions(real.render_set_id),
          loadR2Phrases(real.render_set_id),
          loadR2PhraseAlignments(real.render_set_id),
        ]);
        if (cancelled) return;
        const filteredVersions = abcdVersions(nextVersions);
        const filteredAlignments = abcdAlignments(nextAlignments);
        setDataSource("api");
        setRenderSet(real);
        setVersions(filteredVersions);
        setSections(phraseData.sections);
        setPhrases(phraseData.phrases);
        setAlignments(filteredAlignments);
        setActivePhraseId(phraseData.phrases[0]?.phrase_id ?? "");
        setActiveVersionId(filteredVersions[0]?.version_id ?? "A_LITERAL");
        setBoundaryStatus(makeBoundaryStatusByKey(filteredAlignments));
        setBackendMessage(`后端真实 R2 render set 已加载：${real.render_set_id}`);
        setLastActionMessage("已使用真实 ABCD render set API；模拟数据兜底未启用。");
      } catch (error) {
        if (cancelled) return;
        setDataSource("mock");
        setRenderSet(mockRenderSet);
        setVersions(abcdVersions(mockVersions));
        setSections(mockSections);
        setPhrases(mockPhrases);
        setAlignments(abcdAlignments(mockAlignments));
        setBoundaryStatus(makeBoundaryStatusByKey(abcdAlignments(mockAlignments)));
        setBackendMessage(`后端不可用或未返回真实 render set，已保留模拟数据兜底：${error instanceof Error ? error.message : String(error)}`);
        setLastActionMessage("当前为模拟数据兜底；请启动 backend 后刷新 R2 页面。");
      }
    }
    loadRealRenderSet();
    return () => {
      cancelled = true;
      clearStopTimer();
    };
  }, []);

  const draftKey = `cg-varw:r2:frontend-api-draft:${renderSet.render_set_id}`;
  const activePhrase = getPhrase(phrases, activePhraseId);
  const activeAlignment = getAlignment(alignments, activePhraseId, activeVersionId);
  const activeVersion = versions.find((version) => version.version_id === activeVersionId) ?? versions[0];
  const alignmentsForPhrase = alignments.filter((alignment) => alignment.phrase_id === activePhraseId);
  const activeDraft = drafts[activePhraseId] ?? makeDraft(activePhrase);
  const markers = useMemo(() => makePhraseMarkers(activeAlignment), [activeAlignment]);
  const progress = useMemo(() => deriveProgress(phrases, drafts), [phrases, drafts]);
  const exportPreviewPayload = useMemo(() => buildDraftExportPayload(renderSet, dataSource, phrases, drafts, activePhrase), [renderSet, dataSource, phrases, drafts, activePhrase]);

  useEffect(() => {
    const raw = localStorage.getItem(draftKey);
    if (!raw) {
      setDrafts({});
      return;
    }
    try {
      setDrafts(JSON.parse(raw) as DraftByPhrase);
      setLastActionMessage("已加载本地 R2 review draft JSON。");
    } catch {
      setDrafts({});
    }
  }, [draftKey]);

  function updateDraft(patch: Partial<ReviewDraft>) {
    setDrafts((current) => {
      const next = {
        ...current,
        [activePhraseId]: {
          ...(current[activePhraseId] ?? makeDraft(activePhrase)),
          ...patch,
          phrase_id: activePhraseId,
          event_range: activePhrase.event_range,
          reviewer_role: "human" as const,
          gpt_review_pending: true as const,
          e_revision_plan_generated: false as const,
        },
      };
      localStorage.setItem(draftKey, JSON.stringify(next, null, 2));
      return next;
    });
  }

  function toggleIssue(issue: R2IssueType) {
    const issueType = activeDraft.issue_type.includes(issue)
      ? activeDraft.issue_type.filter((item) => item !== issue)
      : [...activeDraft.issue_type, issue];
    updateDraft({ issue_type: issueType });
  }

  function selectPhrase(phraseId: string) {
    stopPlayback();
    setActivePhraseId(phraseId);
    const nextAlignment = getAlignment(alignments, phraseId, activeVersionId);
    setPlayback((current) => ({ ...current, currentTimeS: phrasePlayStart(nextAlignment), playMode: "idle", isPlaying: false, playingVersionId: undefined }));
    setLastActionMessage(`已切换乐句：${phraseId}`);
  }

  function selectVersion(versionId: string) {
    stopPlayback();
    setActiveVersionId(versionId);
    const nextAlignment = getAlignment(alignments, activePhraseId, versionId);
    setPlayback((current) => ({ ...current, currentTimeS: phrasePlayStart(nextAlignment), playMode: "idle", isPlaying: false, playingVersionId: undefined }));
    setLastActionMessage(`已切换版本：${versionLabel(versions, versionId)}`);
  }

  function setPreferred(versionId: string) {
    updateDraft({ preferred_version: versionId });
    setLastActionMessage(`已设置当前乐句偏好版本：${versionLabel(versions, versionId)}`);
  }

  function playVersion(versionId: string, mode: PlayMode = "phrase", onEnded?: () => void) {
    const version = versions.find((item) => item.version_id === versionId);
    const alignment = getAlignment(alignments, activePhraseId, versionId);
    const playStartS = phrasePlayStart(alignment);
    const playEndS = phrasePlayEnd(alignment);
    setActiveVersionId(versionId);
    setPlayback({ isPlaying: true, currentTimeS: playStartS, playMode: mode, playingVersionId: versionId, playbackRate: playback.playbackRate });
    setLastActionMessage(`播放 ${activePhraseId} · ${versionLabel(versions, versionId)} · ${playStartS.toFixed(3)}-${playEndS.toFixed(3)}s`);
    if (!version?.audio_url || version.mock_render) {
      scheduleMockStop(alignment, onEnded);
      return;
    }
    const audio = audioRef.current;
    if (!audio) return;
    clearStopTimer();
    audio.src = version.audio_url;
    audio.playbackRate = playback.playbackRate;
    audio.currentTime = playStartS;
    audio.play().catch((error) => setLastActionMessage(`浏览器阻止播放：${error instanceof Error ? error.message : String(error)}`));
    stopTimerRef.current = window.setInterval(() => {
      setPlayback((current) => ({ ...current, currentTimeS: audio.currentTime }));
      if (audio.currentTime >= playEndS) {
        audio.pause();
        clearStopTimer();
        setPlayback((current) => ({ ...current, isPlaying: false, currentTimeS: playEndS, playMode: "idle", playingVersionId: undefined }));
        onEnded?.();
      }
    }, 120);
  }

  function playSequenceABCD(index = 0) {
    const queue = versions.map((version) => version.version_id).filter((versionId) => VERSION_ORDER.includes(versionId));
    const versionId = queue[index];
    if (!versionId) {
      stopPlayback();
      return;
    }
    playVersion(versionId, "sequence_abcd", () => playSequenceABCD(index + 1));
  }

  function playPreferredVersion() {
    if (!activeDraft.preferred_version || activeDraft.preferred_version === "none") {
      setLastActionMessage("当前 phrase 尚未设置偏好版本。");
      return;
    }
    playVersion(activeDraft.preferred_version, "preferred");
  }

  function stopPlayback() {
    audioRef.current?.pause();
    clearStopTimer();
    setPlayback((current) => ({ ...current, isPlaying: false, playMode: "idle", playingVersionId: undefined }));
  }

  function scheduleMockStop(alignment: RenderPhraseAlignment, onEnded?: () => void) {
    clearStopTimer();
    const playEndS = phrasePlayEnd(alignment);
    stopTimerRef.current = window.setInterval(() => {
      setPlayback((current) => {
        const nextTime = Number((current.currentTimeS + 0.25 * current.playbackRate).toFixed(3));
        if (nextTime < playEndS) return { ...current, currentTimeS: nextTime };
        clearStopTimer();
        onEnded?.();
        return { ...current, isPlaying: false, currentTimeS: playEndS, playMode: "idle", playingVersionId: undefined };
      });
    }, 250);
  }

  function clearStopTimer() {
    if (stopTimerRef.current !== null) {
      window.clearInterval(stopTimerRef.current);
      stopTimerRef.current = null;
    }
  }

  function saveDraft() {
    localStorage.setItem(draftKey, JSON.stringify(drafts, null, 2));
    setLastActionMessage("R2 review draft 已保存到浏览器 localStorage。");
  }

  function exportDraftJson() {
    const blob = new Blob([JSON.stringify(exportPreviewPayload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${renderSet.render_set_id}.review_draft.json`;
    link.click();
    URL.revokeObjectURL(url);
    setLastActionMessage("已导出听评草稿 JSON；未生成 listening_review.yaml 或 e_revision_plan.yaml。");
  }

  return (
    <AppShell
      mode="R2"
      left={<LeftPanel phrases={phrases} sections={sections} selectedPhraseId={activePhraseId} onSelectPhrase={selectPhrase} progress={progress} dataSource={dataSource} />}
      main={
        <div className="r2-main">
          <audio ref={audioRef} preload="metadata" />
          <div className="work-title tight">
            <div>
              <h1>XWC / 仙翁操 · R2 句读听评</h1>
              <p>渲染集 ID：{renderSet.render_set_id}</p>
              <p>实验渲染 experimental_render=true / 非生产级 production_grade=false / E 未生成 e_generated=false</p>
              <p>按 phrase_id / event_range 对齐，不按同一绝对时间点切换版本。</p>
            </div>
            <span className={`badge ${dataSource === "api" ? "badge-blue" : "badge-gold"}`}>{dataSource === "api" ? "真实 API" : "模拟数据兜底"}</span>
          </div>
          <ABCDEPhrasePlayer
            versions={versions}
            alignments={alignmentsForPhrase}
            selectedVersionId={activeVersionId}
            preferredVersionId={activeDraft.preferred_version === "none" ? undefined : activeDraft.preferred_version}
            onSelect={selectVersion}
            onSetPreferred={setPreferred}
            onPlay={playVersion}
          />
          <section className="work-area phrase-area">
            <h2>当前乐句 · 第{phraseOrder(activePhrase)}句 · {activePhrase.phrase_id}</h2>
            <AudioCanvas
              markers={markers.map(toCanvasMarker)}
              duration={activeVersion?.duration_s ?? activeAlignment.end_s}
              selectedKey={`${activePhraseId}-${activeVersionId}-phrase_start`}
              onSelect={() => undefined}
              audioFileName={`${versionLabel(versions, activeVersionId)} · ${activeVersion?.audio_path ?? "模拟波形"}`}
              waveformPeaks={activeVersion?.waveform_preview}
            />
            <div className="event-strip">
              <span>{activePhrase.start_event_id}</span>
              <span>{activePhrase.event_range}</span>
              <span>{activePhrase.end_event_id}</span>
            </div>
            <div className="playback-bar r2-basic-playback">
              <button className="play-button" onClick={() => playback.isPlaying ? stopPlayback() : playVersion(activeVersionId)}>
                {playback.isPlaying ? "停止" : "播放当前版本"}
                <span>{playModeLabel(playback.playMode)}</span>
              </button>
              <button onClick={() => playVersion(activeVersionId)}>从本版乐句开头播放</button>
              <button onClick={() => playSequenceABCD()}>顺播 A→B→C→D</button>
              <button onClick={playPreferredVersion}>播放偏好版本</button>
              <strong className="clock">{formatTime(playback.currentTimeS)}<small>/ {formatTime(phrasePlayEnd(activeAlignment))} · {playback.playingVersionId ? versionLabel(versions, playback.playingVersionId) : versionLabel(versions, activeVersionId)}</small></strong>
              <span className="speed-label">播放速度</span>
              {([0.5, 1, 1.5] as R2PlaybackRate[]).map((rate) => (
                <button key={rate} className={playback.playbackRate === rate ? "active" : ""} onClick={() => setPlayback((current) => ({ ...current, playbackRate: rate }))}>{rate}x</button>
              ))}
            </div>
            <PhraseAlignmentTable versions={versions} alignments={alignmentsForPhrase} />
          </section>
        </div>
      }
      right={
        <RightPanel
          phrase={activePhrase}
          activeVersionId={activeVersionId}
          versions={versions}
          draft={activeDraft}
          boundaryStatus={boundaryStatus[boundaryKey(activePhraseId, activeVersionId)] ?? "candidate"}
          onBoundaryStatus={(status) => setBoundaryStatus((current) => ({ ...current, [boundaryKey(activePhraseId, activeVersionId)]: status }))}
          onPreferred={setPreferred}
          onToggleIssue={toggleIssue}
          onDraft={updateDraft}
          onSaveDraft={saveDraft}
          onExportDraft={exportDraftJson}
        />
      }
      bottom={<R2BottomPanel renderSet={renderSet} versions={versions} dataSource={dataSource} exportPreviewPayload={exportPreviewPayload} />}
      statusText={backendMessage}
      detailText={lastActionMessage}
    />
  );
}

function LeftPanel({
  phrases,
  sections,
  selectedPhraseId,
  onSelectPhrase,
  progress,
  dataSource,
}: {
  phrases: PhraseDefinition[];
  sections: Section[];
  selectedPhraseId: string;
  onSelectPhrase: (phraseId: string) => void;
  progress: { reviewed: number; total: number };
  dataSource: DataSource;
}) {
  return (
    <div className="panel-stack">
      <h2>项目</h2>
      <div className="tree">
        <strong>Cyber Guqin v1.0 <small>Dapu Mode</small></strong>
        <button className="active">RS_XWC_002_BAIYA_PILOT</button>
      </div>
      <section className="editor-section">
        <h3>当前曲目</h3>
        {mockPieces.map((piece) => <button key={piece.piece_id} className={`wide ${piece.piece_id === "XWC" ? "active" : ""}`}>{piece.piece_id} / {piece.piece_title}<small>{piece.mock_only ? "R2 模拟选项" : "当前 MVP 曲目"}</small></button>)}
      </section>
      <section className="editor-section">
        <h3>当前 session</h3>
        {mockSessions.slice(0, 1).map((session) => <button key={session.recording_session_id} className="wide active">{session.recording_session_id}<small>{dataSource === "api" ? "真实 ABCD render set" : session.label}</small></button>)}
      </section>
      <section className="editor-section">
        <h3>谱面句 / Section</h3>
        {sections.map((section) => (
          <div className="section-tree" key={section.section_id}>
            <strong>{section.section_id} {section.section_label}</strong>
            {section.phrase_ids.map((phraseId) => {
              const phrase = getPhrase(phrases, phraseId);
              return (
                <button key={phraseId} className={`wide ${selectedPhraseId === phraseId ? "active" : ""}`} onClick={() => onSelectPhrase(phraseId)}>
                  第{phraseOrder(phrase)}句 · {phrase.phrase_id}
                  <small>{phrase.event_range} · 事件数 {phrase.event_count ?? "-"} · {phrase.gesture_summary || phrase.gesture_ids || "指法待补"}</small>
                </button>
              );
            })}
          </div>
        ))}
      </section>
      <section className="phrase-rail">
        <h3>草稿进度</h3>
        <div><span>已填 phrase</span><b>{progress.reviewed} / {progress.total}</b><i style={{ width: percentWidth(progress.reviewed, progress.total) }} /></div>
      </section>
    </div>
  );
}

function PhraseAlignmentTable({ versions, alignments }: { versions: RenderVersion[]; alignments: RenderPhraseAlignment[] }) {
  return (
    <section className="editor-section">
      <h3>本 phrase 的 A/B/C/D 独立时间范围</h3>
      <div className="export-table-scroll">
        <table className="export-table">
          <thead>
            <tr><th>版本</th><th>播放开始</th><th>播放结束</th><th>尾音参考</th><th>下一句首音</th><th>事件范围</th><th>wav / audio_url</th></tr>
          </thead>
          <tbody>
            {versions.map((version) => {
              const alignment = alignments.find((item) => item.version_id === version.version_id);
              return (
                <tr key={version.version_id}>
                  <td>{version.version_id}</td>
                  <td>{alignment ? phrasePlayStart(alignment).toFixed(3) : "-"}</td>
                  <td>{alignment ? phrasePlayEnd(alignment).toFixed(3) : "-"}</td>
                  <td>{alignment?.phrase_tail_end_s?.toFixed(3) ?? alignment?.end_s.toFixed(3) ?? "-"}</td>
                  <td>{alignment?.next_phrase_first_attack_s?.toFixed(3) ?? "-"}</td>
                  <td>{alignment?.event_range ?? "-"}</td>
                  <td>{version.audio_url ?? version.audio_path}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function RightPanel({
  phrase,
  activeVersionId,
  versions,
  draft,
  boundaryStatus,
  onBoundaryStatus,
  onPreferred,
  onToggleIssue,
  onDraft,
  onSaveDraft,
  onExportDraft,
}: {
  phrase: PhraseDefinition;
  activeVersionId: string;
  versions: RenderVersion[];
  draft: ReviewDraft;
  boundaryStatus: MarkerReviewStatus;
  onBoundaryStatus: (status: MarkerReviewStatus) => void;
  onPreferred: (versionId: string) => void;
  onToggleIssue: (issue: R2IssueType) => void;
  onDraft: (patch: Partial<ReviewDraft>) => void;
  onSaveDraft: () => void;
  onExportDraft: () => void;
}) {
  return (
    <div className="panel-stack">
      <h2>听评草稿</h2>
      <div className="info-card">
        <span>当前乐句：第{phraseOrder(phrase)}句 · {phrase.phrase_id}</span>
        <code>事件范围：{phrase.event_range}</code>
        <span>事件数：{phrase.event_count ?? "-"}</span>
        <span>当前版本：{versionLabel(versions, activeVersionId)}</span>
        <span>GPT 共评待处理：true</span>
        <span>E 修订计划已生成：false</span>
      </div>
      <section className="editor-section">
        <h3>本句事件明细</h3>
        <PhraseEventDetailList phrase={phrase} />
      </section>
      <section className="editor-section">
        <h3>边界状态</h3>
        <div className="segmented boundary-segmented">
          {reviewStatuses.map((status) => <button key={status} className={boundaryStatus === status ? "active" : ""} onClick={() => onBoundaryStatus(status)}>{boundaryStatusLabel(status)}</button>)}
        </div>
      </section>
      <section className="editor-section">
        <h3>问题类型</h3>
        <div className="issue-grid">
          {issueOptions.filter((issue) => issue.key !== "other").map((issue) => (
            <label key={issue.key} className={draft.issue_type.includes(issue.key) ? "active-check" : ""}>
              <input type="checkbox" checked={draft.issue_type.includes(issue.key)} onChange={() => onToggleIssue(issue.key)} />
              {issue.label}
            </label>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>严重程度</h3>
        <div className="segmented">{(["low", "medium", "high"] as Severity[]).map((item) => <button key={item} className={draft.severity === item ? "active" : ""} onClick={() => onDraft({ severity: item })}>{severityLabel(item)}</button>)}</div>
      </section>
      <section className="editor-section">
        <h3>偏好版本</h3>
        <select className="cg-select" value={draft.preferred_version} onChange={(event) => onPreferred(event.target.value)}>
          <option value="none">none / 未设置</option>
          {versions.map((version) => <option key={version.version_id} value={version.version_id}>{version.version_id}</option>)}
        </select>
      </section>
      <section className="editor-section">
        <h3>评论</h3>
        <textarea value={draft.comment} onChange={(event) => onDraft({ comment: event.target.value })} />
      </section>
      <section className="editor-section">
        <h3>修订建议</h3>
        <textarea value={draft.suggested_revision} onChange={(event) => onDraft({ suggested_revision: event.target.value })} />
      </section>
      <div className="action-row">
        <button className="active" onClick={onSaveDraft}>保存草稿</button>
        <button onClick={onExportDraft}>导出听评草稿 JSON</button>
      </div>
    </div>
  );
}

function PhraseEventDetailList({ phrase }: { phrase: PhraseDefinition }) {
  const rows = phraseEventRows(phrase);
  if (rows.length === 0) return <p>本句事件明细待从 phrase lock 补入。</p>;
  return (
    <div className="export-table-scroll">
      <table className="export-table">
        <thead>
          <tr><th>序号</th><th>event_id</th><th>gesture_id</th><th>指法/归一名</th></tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={`${row.event_id}-${row.index}`}>
              <td>{row.index}</td>
              <td>{row.event_id}</td>
              <td>{row.gesture_id}</td>
              <td>{row.normalized_name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function R2BottomPanel({ renderSet, versions, dataSource, exportPreviewPayload }: { renderSet: RenderSet; versions: RenderVersion[]; dataSource: DataSource; exportPreviewPayload: DraftExportPayload }) {
  return (
    <section className="export-panel">
      <div className="section-title-row">
        <h2>R2 渲染集接入</h2>
        <span>{dataSource === "api" ? "真实 API 数据" : "模拟数据兜底"}</span>
      </div>
      <div className="export-preview-grid">
        <div className="preview-card">
          <h3>渲染集</h3>
          <p>{renderSet.render_set_id}</p>
          <p>实验渲染 experimental_render=true / 非生产级 production_grade=false / E 未生成 e_generated=false</p>
        </div>
        <div className="preview-card">
          <h3>版本</h3>
          <p>{versions.map((version) => version.version_id).join(" / ")}</p>
          <p>不显示 E_REVIEWED；不自动选择最佳版本。</p>
        </div>
        <div className="preview-card">
          <h3>API 地址</h3>
          <p>{apiBase}</p>
          <p>WAV 播放使用后端 audio endpoint，不把本地绝对路径直接塞入浏览器。</p>
        </div>
      </div>
      <section className="editor-section">
        <h3>导出预览</h3>
        <pre className="export-preview-code">{JSON.stringify(exportPreviewPayload, null, 2)}</pre>
      </section>
    </section>
  );
}

function abcdVersions(items: RenderVersion[]) {
  return items.filter((version) => VERSION_ORDER.includes(version.version_id)).sort((a, b) => VERSION_ORDER.indexOf(a.version_id) - VERSION_ORDER.indexOf(b.version_id));
}

function abcdAlignments(items: RenderPhraseAlignment[]) {
  return items.filter((alignment) => VERSION_ORDER.includes(alignment.version_id));
}

function isRealRenderSet(item: RenderSet) {
  return item.render_stage === "experimental_render" && item.review_only === true && item.production_grade === false;
}

function getPhrase(phrases: PhraseDefinition[], phraseId: string) {
  return phrases.find((phrase) => phrase.phrase_id === phraseId) ?? phrases[0] ?? {
    phrase_id: "",
    section_id: "",
    phrase_index: 0,
    phrase_label: "",
    event_range: "",
    start_event_id: "",
    end_event_id: "",
    phrase_order: 0,
    event_count: 0,
    event_ids: "",
    gesture_ids: "",
    normalized_names: "",
    gesture_summary: "",
    lock_status: "",
  };
}

function getSection(sections: Section[], sectionId: string) {
  return sections.find((section) => section.section_id === sectionId) ?? sections[0] ?? { section_id: "", section_label: "", event_range: "", phrase_ids: [] };
}

function getAlignment(alignments: RenderPhraseAlignment[], phraseId: string, versionId: string) {
  return alignments.find((item) => item.phrase_id === phraseId && item.version_id === versionId) ?? alignments.find((item) => item.phrase_id === phraseId) ?? {
    render_set_id: "",
    version_id: versionId,
    phrase_id: phraseId,
    section_id: "",
    event_range: "",
    start_s: 0,
    end_s: 0,
    phrase_play_start_s: null,
    phrase_play_end_s: null,
    phrase_tail_end_s: null,
    next_phrase_first_attack_s: null,
    phrase_end_policy: "",
    breath_points_s: [],
    boundary_source: "mock" as const,
    boundary_confidence: "unclear" as const,
    review_status: "candidate" as const,
  };
}

function makeDraft(phrase: PhraseDefinition): ReviewDraft {
  return {
    phrase_id: phrase.phrase_id,
    event_range: phrase.event_range,
    issue_type: [],
    severity: "low",
    preferred_version: "none",
    comment: "",
    suggested_revision: "",
    reviewer_role: "human",
    gpt_review_pending: true,
    e_revision_plan_generated: false,
  };
}

function buildDraftExportPayload(renderSet: RenderSet, dataSource: DataSource, phrases: PhraseDefinition[], drafts: DraftByPhrase, activePhrase: PhraseDefinition): DraftExportPayload {
  const reviews = phrases
    .map((phrase) => drafts[phrase.phrase_id] ?? makeDraft(phrase))
    .filter(isMeaningfulDraft)
    .map((draft) => {
      const phrase = getPhrase(phrases, draft.phrase_id);
      return {
        ...draft,
        phrase_order: phraseOrder(phrase),
        preferred_version: draft.preferred_version && draft.preferred_version !== "none" ? draft.preferred_version : null,
        reviewer_role: "human" as const,
        gpt_review_pending: true as const,
        e_revision_plan_generated: false as const,
      };
    });
  return {
    render_set_id: renderSet.render_set_id,
    data_source: dataSource === "api" ? "real_api" : "mock_fallback",
    reviewer_role: "human",
    gpt_review_pending: true,
    e_revision_plan_generated: false,
    selected_phrase_id: activePhrase.phrase_id || null,
    selected_event_range: activePhrase.event_range || null,
    draft_count: reviews.length,
    reviews,
  };
}

function isMeaningfulDraft(draft: ReviewDraft) {
  return draft.issue_type.length > 0 || draft.comment.trim().length > 0 || draft.suggested_revision.trim().length > 0 || (draft.preferred_version && draft.preferred_version !== "none");
}

function phraseOrder(phrase: PhraseDefinition) {
  return phrase.phrase_order ?? phrase.phrase_index ?? 0;
}

function phraseEventRows(phrase: PhraseDefinition) {
  const eventIds = splitList(phrase.event_ids);
  const gestureIds = splitList(phrase.gesture_ids);
  const normalizedNames = splitList(phrase.normalized_names || phrase.gesture_summary);
  return eventIds.map((eventId, index) => ({
    index: index + 1,
    event_id: eventId,
    gesture_id: gestureIds[index] ?? "",
    normalized_name: normalizedNames[index] ?? "",
  }));
}

function splitList(value?: string) {
  return (value ?? "").split(";").map((item) => item.trim()).filter(Boolean);
}

function phrasePlayStart(alignment: RenderPhraseAlignment) {
  return alignment.phrase_play_start_s ?? alignment.start_s;
}

function phrasePlayEnd(alignment: RenderPhraseAlignment) {
  return alignment.phrase_play_end_s ?? alignment.end_s;
}

function makeBoundaryStatusByKey(alignments: RenderPhraseAlignment[]) {
  return alignments.reduce<Record<string, MarkerReviewStatus>>((result, alignment) => {
    result[boundaryKey(alignment.phrase_id, alignment.version_id)] = alignment.review_status;
    return result;
  }, {});
}

function makePhraseMarkers(alignment: RenderPhraseAlignment) {
  const markers = [
    marker(`${alignment.phrase_id}-${alignment.version_id}-phrase_start`, "句头", alignment.start_s, "green"),
    marker(`${alignment.phrase_id}-${alignment.version_id}-phrase_end`, "句尾", alignment.end_s, "purple"),
  ];
  alignment.breath_points_s.forEach((time, index) => markers.push(marker(`${alignment.phrase_id}-${alignment.version_id}-breath_${index}`, `气口 ${index + 1}`, time, "blue")));
  if (alignment.cadence_point_s) markers.push(marker(`${alignment.phrase_id}-${alignment.version_id}-cadence`, "收束", alignment.cadence_point_s, "gold"));
  return markers;
}

function marker(id: string, label: string, time: number, color: Marker["color"]): Marker {
  return { id, key: id, label, time, color, displayLabel: true };
}

function toCanvasMarker(item: Marker) {
  return item;
}

function deriveProgress(phrases: PhraseDefinition[], drafts: DraftByPhrase) {
  const reviewed = phrases.filter((phrase) => {
    const draft = drafts[phrase.phrase_id];
    return draft && (draft.issue_type.length > 0 || draft.comment.trim() || draft.suggested_revision.trim() || draft.preferred_version !== "none");
  }).length;
  return { reviewed, total: phrases.length };
}

function boundaryKey(phraseId: string, versionId: string) {
  return `${phraseId}::${versionId}`;
}

function versionLabel(versions: RenderVersion[], versionId: string) {
  const version = versions.find((item) => item.version_id === versionId);
  return version ? `${version.version_code} ${version.version_label_zh}` : versionId;
}

function percentWidth(value: number, total: number) {
  if (total <= 0) return "0%";
  return `${Math.min(100, Math.round((value / total) * 100))}%`;
}

function playModeLabel(mode: PlayMode) {
  return {
    idle: "已停止",
    phrase: "乐句播放",
    sequence_abcd: "A→B→C→D",
    preferred: "偏好版本",
  }[mode];
}

function severityLabel(value: Severity) {
  return {
    low: "低",
    medium: "中",
    high: "高",
  }[value];
}

function boundaryStatusLabel(value: MarkerReviewStatus) {
  return {
    candidate: "候选",
    accepted: "接受",
    unclear: "不清楚",
    needs_retake: "需复核",
    rejected: "拒绝",
  }[value];
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const rest = (seconds % 60).toFixed(3).padStart(6, "0");
  return `${minutes}:${rest}`;
}
