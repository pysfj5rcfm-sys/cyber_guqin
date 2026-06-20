import { useEffect, useMemo, useRef, useState } from "react";
import { ABCDEPhrasePlayer } from "../components/ABCDEPhrasePlayer";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { R2ExportPreviewPanel } from "../components/R2ExportPreviewPanel";
import { markerReviewStatusLabels, markerReviewStatusTone } from "../components/reviewUi";
import {
  apiBase,
  loadR2LatestReviewDraft,
  loadR2PhraseAlignments,
  loadR2Phrases,
  loadR2RenderSets,
  loadR2Versions,
  restoreR2ReviewDraftFromExportDir,
  saveR2ReviewDraftToProject,
} from "../api/cgVarwApi";
import { buildR2PreviewTables, type R2PreviewTable } from "../utils/r2ExportPayload";
import {
  defaultListeningReview,
  issueOptions,
  mockPieces,
  mockSessions,
  phraseAlignments as mockAlignments,
  phraseExports,
  phrases as mockPhrases,
  renderSet as mockRenderSet,
  r2SafetyFlags,
  sections as mockSections,
  versions as mockVersions,
} from "../mock/projectReviewMock";
import type {
  ListeningReview,
  Marker,
  MarkerReviewStatus,
  PhraseDefinition,
  PhraseMarker,
  R2IssueType,
  R2MarkerKey,
  RenderPhraseAlignment,
  RenderSet,
  RenderVersion,
  Section,
  Severity,
} from "../types/cgVarw";

type DataSource = "api" | "mock";
type R2PlaybackRate = 0.5 | 1 | 1.5;
type R2PlayMode = "idle" | "phrase" | "marker" | "preroll" | "sequence_abcd" | "preferred" | "ab_compare";

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
type MarkersByKey = Record<string, PhraseMarker[]>;
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

type R2DraftPayloadWithReviewState = {
  render_set_id: string;
  selected_phrase_id: string;
  selected_version_id: string;
  preferred_version_id?: string;
  phrase_markers: PhraseMarker[];
  phrase_alignments: RenderPhraseAlignment[];
  listening_review: ListeningReview;
  preferred_version_by_phrase?: PreferredVersionByPhrase;
  listening_review_by_key?: ListeningReviewByKey;
  boundary_status_by_key?: BoundaryStatusByKey;
  markers_by_key?: MarkersByKey;
  playback_rate?: R2PlaybackRate;
  loop_phrase?: boolean;
  saved_at: string;
};

type ProgressOverview = {
  totalPhraseCount: number;
  reviewedPhraseCount: number;
  pendingPhraseCount: number;
  unclearBoundaryCount: number;
  needsRetakeCount: number;
  preferredVersionCount: number;
};

const VERSION_ORDER = ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC", "D_TEACHING"];
const reviewStatuses: MarkerReviewStatus[] = ["candidate", "accepted", "unclear", "needs_retake", "rejected"];

export function R2ProjectReviewPage() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const stopTimerRef = useRef<number | null>(null);
  const [dataSource, setDataSource] = useState<DataSource>("mock");
  const [backendStatus, setBackendStatus] = useState("正在尝试读取 R2 真实 render set API...");
  const [renderSet, setRenderSet] = useState<RenderSet>(mockRenderSet);
  const [versions, setVersions] = useState<RenderVersion[]>(abcdVersions(mockVersions));
  const [sections, setSections] = useState<Section[]>(mockSections);
  const [phrases, setPhrases] = useState<PhraseDefinition[]>(mockPhrases);
  const [alignments, setAlignments] = useState<RenderPhraseAlignment[]>(abcdAlignments(mockAlignments));
  const [activePhraseId, setActivePhraseId] = useState(mockPhrases[2]?.phrase_id ?? mockPhrases[0]?.phrase_id ?? "");
  const [activeVersionId, setActiveVersionId] = useState("B_PHRASE");
  const [preferredVersionByPhrase, setPreferredVersionByPhrase] = useState<PreferredVersionByPhrase>(() => {
    const phraseId = mockPhrases[2]?.phrase_id ?? mockPhrases[0]?.phrase_id ?? "";
    return phraseId ? { [phraseId]: "B_PHRASE" } : {};
  });
  const [markersByKey, setMarkersByKey] = useState<MarkersByKey>({});
  const [selectedMarkerId, setSelectedMarkerId] = useState("");
  const [boundaryStatusByKey, setBoundaryStatusByKey] = useState<BoundaryStatusByKey>(() => makeBoundaryStatusByKey(abcdAlignments(mockAlignments)));
  const [listeningReviewByKey, setListeningReviewByKey] = useState<ListeningReviewByKey>({});
  const [exportGroup, setExportGroup] = useState("全部");
  const [lastActionMessage, setLastActionMessage] = useState("R2 模拟数据兜底已就绪");
  const [projectDraftStatus, setProjectDraftStatus] = useState("工程目录 draft 尚未加载");
  const [playback, setPlayback] = useState<R2PlaybackState>({
    isPlaying: false,
    currentTimeS: phrasePlayStart(getAlignmentFromList(abcdAlignments(mockAlignments), mockPhrases[2]?.phrase_id ?? mockPhrases[0]?.phrase_id ?? "", "B_PHRASE")),
    playbackRate: 1,
    loopPhrase: false,
    playMode: "idle",
  });

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
        const latestDraft = await loadR2LatestReviewDraft(real.render_set_id).catch((error) => {
          setProjectDraftStatus(`工程目录 draft 查询失败：${error instanceof Error ? error.message : String(error)}`);
          return undefined;
        });
        if (cancelled) return;
        const filteredVersions = abcdVersions(nextVersions);
        const filteredAlignments = abcdAlignments(nextAlignments);
        const firstPhrase = phraseData.phrases[0]?.phrase_id ?? "";
        const firstVersion = filteredVersions[0]?.version_id ?? "A_LITERAL";
        const nextMarkers = makeMarkersForAlignment(getAlignmentFromList(filteredAlignments, firstPhrase, firstVersion), phraseData.sections);
        setDataSource("api");
        setRenderSet(real);
        setVersions(filteredVersions);
        setSections(phraseData.sections);
        setPhrases(phraseData.phrases);
        setAlignments(filteredAlignments);
        setActivePhraseId(firstPhrase);
        setActiveVersionId(firstVersion);
        setPreferredVersionByPhrase({});
        setMarkersByKey({ [phraseVersionKey(firstPhrase, firstVersion)]: nextMarkers });
        setSelectedMarkerId(defaultMarkerId(nextMarkers));
        setBoundaryStatusByKey(makeBoundaryStatusByKey(filteredAlignments));
        setListeningReviewByKey({});
        setPlayback((current) => ({
          ...current,
          isPlaying: false,
          currentTimeS: phrasePlayStart(getAlignmentFromList(filteredAlignments, firstPhrase, firstVersion)),
          playMode: "idle",
          sequenceQueue: undefined,
          currentQueueIndex: undefined,
          playingVersionId: undefined,
        }));
        setBackendStatus(`后端真实 R2 render set 已加载：${real.render_set_id}`);
        setLastActionMessage("已接入真实 ABCD render set；E_REVIEWED 未启用。");
        if (latestDraft?.has_draft && latestDraft.draft) {
          applyProjectDraft(latestDraft.draft, {
            versions: filteredVersions,
            phrases: phraseData.phrases,
            alignments: filteredAlignments,
            sections: phraseData.sections,
            sourceLabel: "已加载工程内 draft",
            path: latestDraft.path,
            savedAt: latestDraft.saved_at,
          });
        } else if (latestDraft && !latestDraft.has_draft) {
          setProjectDraftStatus("工程目录暂无 latest draft");
        }
      } catch (error) {
        if (cancelled) return;
        const fallbackVersions = abcdVersions(mockVersions);
        const fallbackAlignments = abcdAlignments(mockAlignments);
        const fallbackPhraseId = mockPhrases[2]?.phrase_id ?? mockPhrases[0]?.phrase_id ?? "";
        const fallbackVersionId = fallbackVersions.find((version) => version.version_id === "B_PHRASE")?.version_id ?? fallbackVersions[0]?.version_id ?? "";
        const nextMarkers = makeMarkersForAlignment(getAlignmentFromList(fallbackAlignments, fallbackPhraseId, fallbackVersionId), mockSections);
        setDataSource("mock");
        setRenderSet(mockRenderSet);
        setVersions(fallbackVersions);
        setSections(mockSections);
        setPhrases(mockPhrases);
        setAlignments(fallbackAlignments);
        setActivePhraseId(fallbackPhraseId);
        setActiveVersionId(fallbackVersionId);
        setPreferredVersionByPhrase(fallbackPhraseId ? { [fallbackPhraseId]: fallbackVersionId } : {});
        setMarkersByKey({ [phraseVersionKey(fallbackPhraseId, fallbackVersionId)]: nextMarkers });
        setSelectedMarkerId(defaultMarkerId(nextMarkers));
        setBoundaryStatusByKey(makeBoundaryStatusByKey(fallbackAlignments));
        setBackendStatus(`后端不可用或无真实 render set，已保留模拟数据兜底：${error instanceof Error ? error.message : String(error)}`);
        setLastActionMessage("当前为模拟数据兜底；请启动 backend 后刷新 R2 页面。");
      }
    }
    loadRealRenderSet();
    return () => {
      cancelled = true;
      clearStopTimer();
    };
  }, []);

  const draftKey = `cg-varw:r2:draft:${renderSet.recording_session_id}:${renderSet.piece_id}:${renderSet.render_set_id}`;
  const legacyDraftKey = `cg-varw:r2:${renderSet.render_set_id}:draft`;
  const activeMarkerStateKey = phraseVersionKey(activePhraseId, activeVersionId);
  const activePhrase = getPhraseFromList(phrases, activePhraseId);
  const activeSection = getSectionFromList(sections, activePhrase.section_id);
  const reviewedAlignments = useMemo(() => alignments.map((alignment) => ({
    ...alignment,
    review_status: boundaryStatusByKey[boundaryKey(alignment.phrase_id, alignment.version_id)] ?? alignment.review_status,
  })), [alignments, boundaryStatusByKey]);
  const activeAlignment = getAlignmentFromList(reviewedAlignments, activePhraseId, activeVersionId);
  const boundaryStatus = activeAlignment.review_status;
  const activeVersion = versions.find((version) => version.version_id === activeVersionId) ?? versions[0];
  const alignmentsForPhrase = reviewedAlignments.filter((alignment) => alignment.phrase_id === activePhraseId);
  const preferredVersionId = preferredVersionByPhrase[activePhraseId];
  const activeReviewDraft = listeningReviewByKey[phraseVersionKey(activePhraseId, activeVersionId)] ?? makeReviewDraft(activePhraseId, activeVersionId);
  const activeListeningReview = toListeningReview(activeReviewDraft, renderSet, activeSection.section_id, activePhrase.event_range, preferredVersionId);
  const progress = useMemo(
    () => deriveProgressOverview(phrases, reviewedAlignments, preferredVersionByPhrase, listeningReviewByKey),
    [phrases, reviewedAlignments, preferredVersionByPhrase, listeningReviewByKey],
  );
  const markers = useMemo(
    () => markersByKey[activeMarkerStateKey] ?? makeMarkersForAlignment(activeAlignment, sections),
    [activeMarkerStateKey, activeAlignment, markersByKey, sections],
  );
  const selectedMarker = markers.find((marker) => marker.marker_id === selectedMarkerId) ?? markers[0];
  const playbackRange = getAlignmentFromList(reviewedAlignments, activePhraseId, playback.playingVersionId ?? activeVersionId);
  const canvasMarkers = useMemo(() => markers.map(toCanvasMarker), [markers]);

  function ensureReviewDraft(phraseId: string, versionId: string) {
    const key = phraseVersionKey(phraseId, versionId);
    setListeningReviewByKey((current) => current[key] ? current : {
      ...current,
      [key]: makeReviewDraft(phraseId, versionId),
    });
  }

  function ensureMarkerState(phraseId: string, versionId: string) {
    const key = phraseVersionKey(phraseId, versionId);
    const nextMarkers = markersByKey[key] ?? makeMarkersForAlignment(getAlignmentFromList(reviewedAlignments, phraseId, versionId), sections);
    setMarkersByKey((current) => current[key] ? current : { ...current, [key]: nextMarkers });
    return nextMarkers;
  }

  function setActiveMarkers(updater: (current: PhraseMarker[]) => PhraseMarker[]) {
    setMarkersByKey((current) => {
      const currentMarkers = current[activeMarkerStateKey] ?? makeMarkersForAlignment(activeAlignment, sections);
      return {
        ...current,
        [activeMarkerStateKey]: updater(currentMarkers),
      };
    });
  }

  function selectPhrase(phraseId: string) {
    stopPlayback();
    const nextMarkers = ensureMarkerState(phraseId, activeVersionId);
    const alignment = getAlignmentFromList(reviewedAlignments, phraseId, activeVersionId);
    setActivePhraseId(phraseId);
    setSelectedMarkerId(defaultMarkerId(nextMarkers));
    setPlayback((current) => ({ ...current, isPlaying: false, currentTimeS: phrasePlayStart(alignment), playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
    ensureReviewDraft(phraseId, activeVersionId);
    setLastActionMessage(`已切换到 ${phraseId} · ${versionLabel(versions, activeVersionId)}`);
  }

  function selectVersion(versionId: string) {
    stopPlayback();
    const nextMarkers = ensureMarkerState(activePhraseId, versionId);
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, versionId);
    setActiveVersionId(versionId);
    setSelectedMarkerId(defaultMarkerId(nextMarkers));
    setPlayback((current) => ({ ...current, isPlaying: false, currentTimeS: phrasePlayStart(alignment), playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
    ensureReviewDraft(activePhraseId, versionId);
    setLastActionMessage(`已切换到 ${activePhraseId} · ${versionLabel(versions, versionId)}`);
  }

  function setPreferred(versionId: string) {
    setPreferredVersionByPhrase((current) => ({ ...current, [activePhraseId]: versionId }));
    setLastActionMessage(`已选择偏好版本 · ${activePhraseId} · ${versionLabel(versions, versionId)}`);
  }

  function playVersion(versionId: string) {
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, versionId);
    if (versionId !== activeVersionId) {
      const nextMarkers = ensureMarkerState(activePhraseId, versionId);
      setActiveVersionId(versionId);
      setSelectedMarkerId(defaultMarkerId(nextMarkers));
      ensureReviewDraft(activePhraseId, versionId);
    }
    startPlayback([versionId], "phrase", phrasePlayStart(alignment), `播放 ${activePhraseId} · ${versionLabel(versions, versionId)}`);
  }

  function updateMarker(patch: Partial<PhraseMarker>) {
    setActiveMarkers((current) => current.map((marker) => marker.marker_id === selectedMarkerId ? { ...marker, ...patch } : marker));
    if (patch.review_status) setLastActionMessage(`已更新标记状态 · ${statusLabel(patch.review_status)}`);
  }

  function nudgeMarker(deltaMs: number) {
    setActiveMarkers((current) => current.map((marker) => marker.marker_id === selectedMarkerId ? {
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
    setLastActionMessage(`${activePhraseId} · ${versionLabel(versions, activeVersionId)} 边界状态已更新为${statusLabel(status)}`);
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
    const nextMarkersByKey = { ...markersByKey, [activeMarkerStateKey]: markers };
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
      boundary_status_by_key: boundaryStatusByKey,
      markers_by_key: nextMarkersByKey,
      playback_rate: playback.playbackRate,
      loop_phrase: playback.loopPhrase,
      saved_at: new Date().toISOString(),
      ...r2SafetyFlags,
    };
    localStorage.setItem(draftKey, JSON.stringify(payload));
    setLastActionMessage("draft 已保存到浏览器；未生成 E 或 e_revision_plan。");
  }

  function loadDraft(options: { silentMissing?: boolean; source?: "auto" | "manual" } = {}) {
    const raw = localStorage.getItem(draftKey) ?? localStorage.getItem(legacyDraftKey);
    if (!raw) {
      if (!options.silentMissing) setLastActionMessage("未找到 R2 draft");
      return;
    }
    try {
      const payload = JSON.parse(raw) as R2DraftPayloadWithReviewState;
      const versionId = abcdVersionId(payload.selected_version_id, versions) ?? versions[0]?.version_id ?? "";
      const phraseId = phrases.some((phrase) => phrase.phrase_id === payload.selected_phrase_id) ? payload.selected_phrase_id : phrases[0]?.phrase_id ?? "";
      const alignment = getAlignmentFromList(reviewedAlignments, phraseId, versionId);
      const nextMarkersByKey = payload.markers_by_key ?? {
        [phraseVersionKey(phraseId, versionId)]: payload.phrase_markers?.length ? payload.phrase_markers : makeMarkersForAlignment(alignment, sections),
      };
      const nextMarkers = nextMarkersByKey[phraseVersionKey(phraseId, versionId)] ?? makeMarkersForAlignment(alignment, sections);
      setActivePhraseId(phraseId);
      setActiveVersionId(versionId);
      setPreferredVersionByPhrase(filterPreferredVersions(payload.preferred_version_by_phrase ?? (payload.preferred_version_id ? { [phraseId]: payload.preferred_version_id } : {}), versions));
      setMarkersByKey(nextMarkersByKey);
      setSelectedMarkerId(defaultMarkerId(nextMarkers));
      setBoundaryStatusByKey(payload.boundary_status_by_key ?? makeBoundaryStatusByKey(payload.phrase_alignments));
      setListeningReviewByKey(filterReviewDrafts(payload.listening_review_by_key ?? {
        [phraseVersionKey(payload.listening_review.phrase_id, payload.listening_review.active_version_id)]: draftFromListeningReview(payload.listening_review),
      }, versions));
      setPlayback((current) => ({
        ...current,
        isPlaying: false,
        currentTimeS: phrasePlayStart(alignment),
        playbackRate: payload.playback_rate ?? current.playbackRate,
        loopPhrase: payload.loop_phrase ?? current.loopPhrase,
        playMode: "idle",
        sequenceQueue: undefined,
        currentQueueIndex: undefined,
        playingVersionId: undefined,
      }));
      setLastActionMessage(options.source === "auto" ? "已自动加载 R2 draft" : "已加载 R2 draft");
    } catch (error) {
      setLastActionMessage(`R2 draft 加载失败：${error instanceof Error ? error.message : String(error)}`);
    }
  }

  function applyProjectDraft(rawDraft: Record<string, unknown>, context: {
    versions: RenderVersion[];
    phrases: PhraseDefinition[];
    alignments: RenderPhraseAlignment[];
    sections: Section[];
    sourceLabel: string;
    path?: string;
    savedAt?: string;
  }) {
    const preferred = readRecord(rawDraft.preferredVersionByPhrase) ?? readRecord(rawDraft.preferred_version_by_phrase) ?? {};
    const reviews = readRecord(rawDraft.listeningReviewByKey) ?? readRecord(rawDraft.listening_review_by_key) ?? {};
    const boundary = readRecord(rawDraft.boundaryStatusByKey) ?? readRecord(rawDraft.boundary_status_by_key) ?? {};
    const markerState = readRecord(rawDraft.markersByKey) ?? readRecord(rawDraft.markers_by_key) ?? {};
    const phraseId = phraseIdInList(readString(rawDraft.active_phrase_id) || readString(rawDraft.selected_phrase_id), context.phrases);
    const versionId = versionIdInList(readString(rawDraft.active_version_id) || readString(rawDraft.selected_version_id), context.versions);
    const alignment = getAlignmentFromList(context.alignments, phraseId, versionId);
    const key = phraseVersionKey(phraseId, versionId);
    const restoredMarkers = (markerState[key] as PhraseMarker[] | undefined) ?? makeMarkersForAlignment(alignment, context.sections);
    const selectedMarker = readString(rawDraft.selected_marker_id);
    setActivePhraseId(phraseId);
    setActiveVersionId(versionId);
    setPreferredVersionByPhrase(filterPreferredVersions(preferred as PreferredVersionByPhrase, context.versions));
    setListeningReviewByKey(filterReviewDrafts(reviews as ListeningReviewByKey, context.versions));
    setBoundaryStatusByKey(Object.keys(boundary).length ? boundary as BoundaryStatusByKey : makeBoundaryStatusByKey(context.alignments));
    setMarkersByKey(Object.keys(markerState).length ? markerState as MarkersByKey : { [key]: restoredMarkers });
    setSelectedMarkerId(selectedMarker && restoredMarkers.some((marker) => marker.marker_id === selectedMarker) ? selectedMarker : defaultMarkerId(restoredMarkers));
    setPlayback((current) => ({
      ...current,
      isPlaying: false,
      currentTimeS: phrasePlayStart(alignment),
      playMode: "idle",
      sequenceQueue: undefined,
      currentQueueIndex: undefined,
      playingVersionId: undefined,
    }));
    setProjectDraftStatus(`${context.sourceLabel}${context.path ? `：${context.path}` : ""}${context.savedAt ? ` · ${context.savedAt}` : ""}`);
    setLastActionMessage(`${context.sourceLabel}；未生成 E。`);
  }

  async function saveProjectDraft() {
    if (dataSource !== "api") {
      setLastActionMessage("当前为模拟数据兜底，未写工程目录 draft。");
      return;
    }
    try {
      const response = await saveR2ReviewDraftToProject(renderSet.render_set_id, buildProjectReviewStatePayload());
      const data = response.data ?? {};
      const latestDir = readString(data.latest_dir) || response.path || "";
      setProjectDraftStatus(`已保存工程目录 draft：${latestDir}`);
      setLastActionMessage("已保存听评草稿到工程目录 latest/archive；未生成 E。");
    } catch (error) {
      setLastActionMessage(`工程目录 draft 保存失败：${error instanceof Error ? error.message : String(error)}`);
    }
  }

  async function loadProjectDraftLatest() {
    try {
      const response = await loadR2LatestReviewDraft(renderSet.render_set_id);
      if (!response.has_draft || !response.draft) {
        setProjectDraftStatus("工程目录暂无 latest draft");
        setLastActionMessage("工程目录暂无 latest draft。");
        return;
      }
      applyProjectDraft(response.draft, {
        versions,
        phrases,
        alignments: reviewedAlignments,
        sections,
        sourceLabel: "已从工程目录重新加载 draft",
        path: response.path,
        savedAt: response.saved_at,
      });
    } catch (error) {
      setLastActionMessage(`工程目录 draft 加载失败：${error instanceof Error ? error.message : String(error)}`);
    }
  }

  async function restoreProjectDraftFromExports() {
    if (dataSource !== "api") {
      setLastActionMessage("当前为模拟数据兜底，未从导出文件恢复工程 draft。");
      return;
    }
    try {
      const response = await restoreR2ReviewDraftFromExportDir(renderSet.render_set_id);
      const data = response.data ?? {};
      const warningCount = Number(data.warning_count ?? 0);
      setProjectDraftStatus(`已从导出文件恢复 latest draft：${readString(data.latest_dir) || response.path || ""}`);
      setLastActionMessage(`已从 8 个导出文件恢复工程 draft；warnings=${warningCount}；未生成 E。`);
      await loadProjectDraftLatest();
    } catch (error) {
      setLastActionMessage(`从导出文件恢复工程 draft 失败：${error instanceof Error ? error.message : String(error)}`);
    }
  }

  function buildProjectReviewStatePayload(): Record<string, unknown> {
    return {
      render_set_id: renderSet.render_set_id,
      data_source: dataSource === "api" ? "api" : "mock_fallback",
      review_status: "draft",
      active_phrase_id: activePhraseId,
      active_version_id: activeVersionId,
      selected_marker_id: selectedMarkerId,
      boundaryStatusByKey,
      listeningReviewByKey,
      preferredVersionByPhrase,
      markersByKey: { ...markersByKey, [activeMarkerStateKey]: markers },
      phrase_markers: markers,
      phrase_alignments: reviewedAlignments,
      listening_review: activeListeningReview,
      export_tables: previewTables,
      review_count: Object.keys(listeningReviewByKey).length,
      preferred_version_count: Object.keys(preferredVersionByPhrase).length,
      gpt_review_pending: true,
      e_revision_plan_generated: false,
      e_generated: false,
      experimental_render: true,
      provenance: {
        saved_from_frontend: true,
        saved_at: new Date().toISOString(),
      },
      ...r2SafetyFlags,
    };
  }

  function startPlayback(queue: string[], playMode: R2PlayMode, startTime: number, message: string) {
    const firstVersionId = queue[0] ?? activeVersionId;
    clearStopTimer();
    setPlayback((current) => ({
      ...current,
      isPlaying: true,
      currentTimeS: Number(startTime.toFixed(3)),
      playMode,
      sequenceQueue: queue,
      currentQueueIndex: 0,
      playingVersionId: firstVersionId,
    }));
    startAudioIfAvailable(firstVersionId, startTime);
    setLastActionMessage(message);
  }

  function startAudioIfAvailable(versionId: string, startTime: number) {
    const version = versions.find((item) => item.version_id === versionId);
    const audio = audioRef.current;
    if (!audio || !version?.audio_url || version.mock_render) return;
    audio.src = version.audio_url;
    audio.playbackRate = playback.playbackRate;
    audio.currentTime = startTime;
    audio.play().catch((error) => setLastActionMessage(`浏览器阻止播放：${error instanceof Error ? error.message : String(error)}`));
  }

  function togglePlayPause() {
    if (playback.isPlaying) {
      stopPlayback();
      setLastActionMessage(`已暂停 · ${activePhraseId}`);
      return;
    }
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, activeVersionId);
    startPlayback([activeVersionId], "phrase", Math.max(playback.currentTimeS, phrasePlayStart(alignment)), `播放中 · ${activePhraseId} · ${versionLabel(versions, activeVersionId)}`);
  }

  function playFromPhraseStart() {
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, activeVersionId);
    startPlayback([activeVersionId], "phrase", phrasePlayStart(alignment), `从句头播放 · ${activePhraseId} · ${versionLabel(versions, activeVersionId)}`);
  }

  function playFromSelectedMarker() {
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, activeVersionId);
    const markerTime = selectedMarker?.time_s ?? phrasePlayStart(alignment);
    startPlayback([activeVersionId], "marker", Math.min(markerTime, phrasePlayEnd(alignment)), `从当前标记播放 · ${selectedMarker?.marker_label_zh ?? "句头"}`);
  }

  function playPreroll300ms() {
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, activeVersionId);
    const markerTime = selectedMarker?.time_s ?? phrasePlayStart(alignment);
    startPlayback([activeVersionId], "preroll", Math.max(phrasePlayStart(alignment), markerTime - 0.3), `前滚 300ms · ${activePhraseId}`);
  }

  function toggleLoopPhrase() {
    setPlayback((current) => ({ ...current, loopPhrase: !current.loopPhrase }));
    setLastActionMessage(playback.loopPhrase ? `已关闭循环 · ${activePhraseId}` : `循环当前 phrase · ${activePhraseId}`);
  }

  function changeRate(rate: R2PlaybackRate) {
    if (audioRef.current) audioRef.current.playbackRate = rate;
    setPlayback((current) => ({ ...current, playbackRate: rate }));
    setLastActionMessage(`播放速度 ${rate}x · ${activePhraseId}`);
  }

  function jumpPhrase(direction: -1 | 1) {
    const currentIndex = phrases.findIndex((phrase) => phrase.phrase_id === activePhraseId);
    const nextPhrase = phrases[Math.min(phrases.length - 1, Math.max(0, currentIndex + direction))];
    if (nextPhrase && nextPhrase.phrase_id !== activePhraseId) selectPhrase(nextPhrase.phrase_id);
  }

  function playSequenceABCD() {
    const queue = versions.map((version) => version.version_id);
    const first = getAlignmentFromList(reviewedAlignments, activePhraseId, queue[0]);
    startPlayback(queue, "sequence_abcd", phrasePlayStart(first), `顺播 A→B→C→D：${activePhraseId}`);
  }

  function playPreferredVersion() {
    if (!preferredVersionId) {
      setLastActionMessage(`当前 phrase 尚未设置偏好版本：${activePhraseId}`);
      stopPlayback();
      return;
    }
    const alignment = getAlignmentFromList(reviewedAlignments, activePhraseId, preferredVersionId);
    startPlayback([preferredVersionId], "preferred", phrasePlayStart(alignment), `正在播放偏好版本：${versionLabel(versions, preferredVersionId)}`);
  }

  function playABCompare() {
    const a = versions.find((version) => version.version_code === "A")?.version_id;
    const b = versions.find((version) => version.version_code === "B")?.version_id;
    const queue = [a, b].filter(Boolean) as string[];
    const first = getAlignmentFromList(reviewedAlignments, activePhraseId, queue[0]);
    startPlayback(queue, "ab_compare", phrasePlayStart(first), "A/B 对比播放：A 直译谱面版 → B 句法呼吸版");
  }

  function stopPlayback() {
    audioRef.current?.pause();
    clearStopTimer();
    setPlayback((current) => ({ ...current, isPlaying: false, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined }));
  }

  function clearStopTimer() {
    if (stopTimerRef.current !== null) {
      window.clearInterval(stopTimerRef.current);
      stopTimerRef.current = null;
    }
  }

  useEffect(() => {
    if (!playback.isPlaying) return;
    clearStopTimer();
    stopTimerRef.current = window.setInterval(() => {
      setPlayback((current) => {
        const currentIndex = current.currentQueueIndex ?? 0;
        const currentVersionId = current.playingVersionId ?? current.sequenceQueue?.[currentIndex] ?? activeVersionId;
        const range = getAlignmentFromList(reviewedAlignments, activePhraseId, currentVersionId);
        const endS = phrasePlayEnd(range);
        const audio = audioRef.current;
        const liveTime = audio && !versions.find((version) => version.version_id === currentVersionId)?.mock_render ? audio.currentTime : current.currentTimeS + 0.25 * current.playbackRate;
        const nextTime = Number(liveTime.toFixed(3));
        if (nextTime < endS) return { ...current, currentTimeS: nextTime };
        audio?.pause();
        if (current.loopPhrase && (!current.sequenceQueue || current.sequenceQueue.length <= 1)) {
          startAudioIfAvailable(currentVersionId, phrasePlayStart(range));
          return { ...current, currentTimeS: phrasePlayStart(range) };
        }
        if (current.sequenceQueue && currentIndex < current.sequenceQueue.length - 1) {
          const nextIndex = currentIndex + 1;
          const nextVersionId = current.sequenceQueue[nextIndex];
          const nextRange = getAlignmentFromList(reviewedAlignments, activePhraseId, nextVersionId);
          startAudioIfAvailable(nextVersionId, phrasePlayStart(nextRange));
          return { ...current, currentQueueIndex: nextIndex, playingVersionId: nextVersionId, currentTimeS: phrasePlayStart(nextRange) };
        }
        clearStopTimer();
        return { ...current, isPlaying: false, currentTimeS: endS, playMode: "idle", sequenceQueue: undefined, currentQueueIndex: undefined, playingVersionId: undefined };
      });
    }, 120);
    return clearStopTimer;
  }, [activePhraseId, activeVersionId, playback.isPlaying, reviewedAlignments, versions]);

  const previewTables = useMemo(
    () => buildR2PreviewTables({ sections, phrases, alignments: reviewedAlignments, markers, review: activeListeningReview, preferredVersionByPhrase, listeningReviewByKey, activePhraseId, activeVersionId, preferredVersionId, boundaryStatus }),
    [sections, phrases, reviewedAlignments, markers, activeListeningReview, preferredVersionByPhrase, listeningReviewByKey, activePhraseId, activeVersionId, preferredVersionId, boundaryStatus],
  );

  function exportFiles(scope: "all" | "phrase") {
    const files = Object.keys(previewTables);
    const selectedFiles = scope === "all" ? files : files.filter((file) => ["phrase_boundary_decision.csv", "render_phrase_alignment.csv", "listening_review.csv", "listening_review.yaml", "render_revision_log.yaml"].includes(file));
    selectedFiles.forEach((file) => downloadPreviewFile(file, previewTables[file]));
    setLastActionMessage(scope === "all" ? "已导出全部 R2 draft 文件；未生成 E。" : "已导出当前 phrase draft 文件；未生成 E。");
  }

  function downloadPreviewFile(file: string, table?: R2PreviewTable) {
    if (!table) return;
    const text = file.endsWith(".yaml") ? tableToYaml(table) : tableToCsv(table);
    const blob = new Blob([text], { type: file.endsWith(".yaml") ? "text/yaml;charset=utf-8" : "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = file;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <AppShell
      mode="R2"
      left={<LeftPanel renderSet={renderSet} phrases={phrases} sections={sections} selectedPhraseId={activePhraseId} onSelectPhrase={selectPhrase} progress={progress} dataSource={dataSource} />}
      main={
        <div className="r2-main">
          <audio ref={audioRef} preload="metadata" />
          <div className="work-title tight">
            <div>
              <h1>{renderSet.piece_id} / {renderSet.piece_title} · R2 句读听评</h1>
              <p>当前比较：{activeSection.section_id} / {activePhrase.phrase_id} / {activePhrase.event_range}</p>
              <p>按 phrase_id / event_range 对齐；播放使用 playback-safe 边界，不按绝对时间切换。</p>
            </div>
            <span className={`badge ${dataSource === "api" ? "badge-blue" : "badge-gold"}`} title={activeVersionId}>{dataSource === "api" ? "真实 API" : "模拟数据兜底"} · {versionLabel(versions, activeVersionId)}</span>
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
            <h2>当前 phrase 波形 / 频谱 · {activeVersion?.version_code} {activeVersion?.version_label_zh}</h2>
            <AudioCanvas
              markers={canvasMarkers}
              duration={activeVersion?.duration_s ?? phrasePlayEnd(activeAlignment)}
              selectedKey={selectedMarkerId}
              onSelect={setSelectedMarkerId}
              audioFileName={`${versionLabel(versions, activeVersionId)} · ${activeVersion?.audio_path ?? "模拟波形"}`}
              waveformPeaks={activeVersion?.waveform_preview}
            />
            <div className="event-strip"><span>{activePhrase.start_event_id}</span><span>{activePhrase.event_range}</span><span>{activePhrase.end_event_id}</span></div>
            <R2PlaybackControls
              playback={playback}
              phraseEndS={phrasePlayEnd(playbackRange)}
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
              <button onClick={playSequenceABCD}>顺播 A→B→C→D</button>
              <button onClick={playPreferredVersion}>播放偏好版本</button>
              <button onClick={playABCompare}>A/B 对比播放</button>
              <strong className="clock">{phrasePlayStart(activeAlignment).toFixed(3)}<small>- {phrasePlayEnd(activeAlignment).toFixed(3)}s · 尾音参考 {phraseTailEnd(activeAlignment).toFixed(3)}s</small></strong>
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
          versions={versions}
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
          rows={r2ExportRows()}
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
          onSaveProjectDraft={saveProjectDraft}
          onLoadProjectDraft={loadProjectDraftLatest}
          onRestoreProjectDraft={restoreProjectDraftFromExports}
          onExportAll={() => exportFiles("all")}
          onExportPhrase={() => exportFiles("phrase")}
          onPreview={(file) => setLastActionMessage(`已预览 ${file}`)}
          onDownloadFile={(file) => downloadPreviewFile(file, previewTables[file])}
        />
      }
      statusText={backendStatus}
      detailText={`${lastActionMessage} · ${projectDraftStatus} · API base: ${apiBase} · E 未生成`}
    />
  );
}

function LeftPanel({
  renderSet,
  phrases,
  sections,
  selectedPhraseId,
  onSelectPhrase,
  progress,
  dataSource,
}: {
  renderSet: RenderSet;
  phrases: PhraseDefinition[];
  sections: Section[];
  selectedPhraseId: string;
  onSelectPhrase: (phraseId: string) => void;
  progress: ProgressOverview;
  dataSource: DataSource;
}) {
  return (
    <div className="panel-stack">
      <h2>项目</h2>
      <div className="tree">
        <strong>Cyber Guqin v1.0 <small>Dapu Mode</small></strong>
        <button className="active">{renderSet.recording_session_id}</button>
      </div>
      <section className="editor-section">
        <h3>曲目</h3>
        {mockPieces.map((piece) => <button key={piece.piece_id} className={`wide ${piece.piece_id === renderSet.piece_id ? "active" : ""}`}>{piece.piece_id} / {piece.piece_title}<small>{piece.piece_id === renderSet.piece_id ? "当前曲目" : "R2 模拟选项"}</small></button>)}
      </section>
      <section className="editor-section">
        <h3>Session</h3>
        {mockSessions.slice(0, 1).map((session) => <button key={session.recording_session_id} className="wide active">{renderSet.recording_session_id}<small>{dataSource === "api" ? "真实 ABCD render set" : session.label}</small></button>)}
      </section>
      <section className="editor-section">
        <h3>Section / Phrase</h3>
        {sections.map((section) => (
          <div className="section-tree" key={section.section_id}>
            <strong>{section.section_id} {section.section_label}</strong>
            {section.phrase_ids.map((phraseId) => {
              const phrase = getPhraseFromList(phrases, phraseId);
              return <button key={phraseId} className={`wide ${selectedPhraseId === phraseId ? "active" : ""}`} onClick={() => onSelectPhrase(phraseId)}>{phrase.phrase_id}<small>{phrase.event_range} · 事件数 {phrase.event_count ?? "-"}</small></button>;
            })}
          </div>
        ))}
      </section>
      <section className="phrase-rail">
        <h3>本曲进度概览</h3>
        <div><span>已审 phrase</span><b>{progress.reviewedPhraseCount} / {progress.totalPhraseCount}</b><i style={{ width: percentWidth(progress.reviewedPhraseCount, progress.totalPhraseCount) }} /></div>
        <div><span>待审 phrase</span><b>{progress.pendingPhraseCount} / {progress.totalPhraseCount}</b><i className="gold-line" style={{ width: percentWidth(progress.pendingPhraseCount, progress.totalPhraseCount) }} /></div>
        <div><span>待复核边界</span><b>{progress.unclearBoundaryCount}</b><i className="gold-line" style={{ width: percentWidth(progress.unclearBoundaryCount, Math.max(1, progress.totalPhraseCount * 4)) }} /></div>
        <div><span>需重录</span><b>{progress.needsRetakeCount}</b><i className="gold-line" style={{ width: percentWidth(progress.needsRetakeCount, Math.max(1, progress.totalPhraseCount * 4)) }} /></div>
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
  versions,
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
  activeSection: Section;
  eventRange: string;
  activeVersionId: string;
  versions: RenderVersion[];
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
        <span>当前版本：{versionLabel(versions, activeVersionId)}</span>
        <span>偏好版本：{preferredVersionId ? versionLabel(versions, preferredVersionId) : "未设置偏好"}</span>
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
          <span className={`unit-status status-${statusToneClass(selectedMarker?.review_status ?? "candidate")}`}>状态：{statusLabel(selectedMarker?.review_status ?? "candidate")}</span>
        </div>
        <div className="nudge-grid">{[-50, -10, -5, 5, 10, 50].map((delta) => <button key={delta} onClick={() => nudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>)}</div>
        <div className="status-grid marker-status-grid">
          {reviewStatuses.map((status) => (
            <button
              key={status}
              className={`status-option status-${statusToneClass(status)} ${selectedMarker?.review_status === status ? "active" : ""}`}
              onClick={() => updateMarker({ review_status: status })}
            >
              {statusLabel(status)}
            </button>
          ))}
        </div>
        <div className="cg-select-row">
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
          {reviewStatuses.map((status) => (
            <button
              key={status}
              className={`status-option status-${statusToneClass(status)} ${boundaryStatus === status ? "active" : ""}`}
              onClick={() => setBoundaryStatus(status)}
            >
              {statusLabel(status)}
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>B. 当前版本听评批注</h3>
        <div className="review-subsection">
          <h4>当前评审对象</h4>
          <span>当前 phrase：<b>{activePhraseId}</b></span>
          <span>当前 version：<b>{versionLabel(versions, activeVersionId)}</b></span>
          <span>当前 preferred：<b>{preferredVersionId ? versionLabel(versions, preferredVersionId) : "未设置偏好"}</b></span>
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
            {issueOptions.filter((issue) => issue.key !== "other").map((issue) => <label key={issue.key} className={review.issue_type.includes(issue.key) ? "active-check" : ""}><input type="checkbox" checked={review.issue_type.includes(issue.key)} onChange={() => toggleIssue(issue.key)} />{issue.label}</label>)}
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
        <div className="action-row"><button className="active" onClick={saveDraft}>保存 draft</button><button onClick={() => loadDraft()}>加载 draft</button></div>
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
      <strong className="clock">{formatTime(playback.currentTimeS)}<small>/ {formatTime(phraseEndS)} · {playback.playingVersionId ?? "当前版本"}</small></strong>
      <span className="speed-label">播放速度</span>
      {([0.5, 1, 1.5] as R2PlaybackRate[]).map((rate) => (
        <button key={rate} className={playback.playbackRate === rate ? "active" : ""} onClick={() => onRateChange(rate)}>
          {rate}x
        </button>
      ))}
    </div>
  );
}

function abcdVersions(items: RenderVersion[]) {
  const filtered = items.filter((version) => version.version_code !== "E" && version.version_id !== "E_REVIEWED");
  return filtered.sort((a, b) => VERSION_ORDER.indexOf(a.version_id) - VERSION_ORDER.indexOf(b.version_id));
}

function abcdAlignments(items: RenderPhraseAlignment[]) {
  const allowedVersions = new Set(VERSION_ORDER);
  return items.filter((alignment) => allowedVersions.has(alignment.version_id));
}

function isRealRenderSet(item: RenderSet) {
  return item.render_stage === "experimental_render" && item.review_only === true && item.production_grade === false;
}

function getPhraseFromList(phrases: PhraseDefinition[], phraseId: string) {
  return phrases.find((phrase) => phrase.phrase_id === phraseId) ?? phrases[0] ?? {
    phrase_id: "",
    section_id: "",
    phrase_index: 0,
    phrase_label: "",
    event_range: "",
    start_event_id: "",
    end_event_id: "",
  };
}

function getSectionFromList(sections: Section[], sectionId: string) {
  return sections.find((section) => section.section_id === sectionId) ?? sections[0] ?? { section_id: "", section_label: "", event_range: "", phrase_ids: [] };
}

function getAlignmentFromList(alignments: RenderPhraseAlignment[], phraseId: string, versionId: string) {
  return alignments.find((item) => item.phrase_id === phraseId && item.version_id === versionId) ?? alignments.find((item) => item.phrase_id === phraseId) ?? alignments[0] ?? {
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

function phrasePlayStart(alignment: RenderPhraseAlignment) {
  return alignment.phrase_play_start_s ?? alignment.start_s;
}

function phrasePlayEnd(alignment: RenderPhraseAlignment) {
  return alignment.phrase_play_end_s ?? alignment.end_s;
}

function phraseTailEnd(alignment: RenderPhraseAlignment) {
  return alignment.phrase_tail_end_s ?? alignment.end_s;
}

function makeMarkersForAlignment(alignment: RenderPhraseAlignment, sections: Section[]): PhraseMarker[] {
  const markers = [
    marker("phrase_start", "句头", phrasePlayStart(alignment), alignment),
    ...alignment.breath_points_s.map((time, index) => marker("breath_point", `气口 ${index + 1}`, Math.min(time, phrasePlayEnd(alignment)), alignment)),
    marker("cadence", "收束", Math.min(alignment.cadence_point_s ?? phrasePlayEnd(alignment) - 0.8, phrasePlayEnd(alignment)), alignment),
    marker("phrase_end", "句尾", phrasePlayEnd(alignment), alignment),
  ];
  const section = getSectionFromList(sections, alignment.section_id);
  if (section.phrase_ids[0] === alignment.phrase_id) markers.unshift(marker("section_start", "段落起", phrasePlayStart(alignment), alignment));
  if (section.phrase_ids[section.phrase_ids.length - 1] === alignment.phrase_id) markers.push(marker("section_end", "段落止", phrasePlayEnd(alignment), alignment));
  return markers;
}

function marker(marker_type: PhraseMarker["marker_type"], marker_label_zh: string, time_s: number, alignment: RenderPhraseAlignment, review_status: PhraseMarker["review_status"] = "candidate"): PhraseMarker {
  return {
    marker_id: `${alignment.phrase_id}_${alignment.version_id}_${marker_type}`,
    render_set_id: alignment.render_set_id,
    version_id: alignment.version_id,
    phrase_id: alignment.phrase_id,
    marker_type,
    marker_label_zh,
    time_s: Number(Math.max(0, time_s).toFixed(3)),
    source: alignment.boundary_source,
    review_status,
    nudge_total_ms: 0,
    notes: alignment.phrase_end_policy ? `playback-safe: ${alignment.phrase_end_policy}` : "R2 marker; review-only.",
  };
}

function toCanvasMarker(item: PhraseMarker): Marker {
  return {
    id: item.marker_id,
    key: item.marker_id,
    label: `${item.marker_label_zh} · ${statusLabel(item.review_status)}`,
    time: item.time_s,
    color: markerColor(item.marker_type),
    source: item.source,
    review_status: item.review_status,
    nudge_total_ms: item.nudge_total_ms,
    notes: item.notes,
    displayLabel: true,
    weak: item.marker_type === "section_start" || item.marker_type === "section_end",
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
    reviewer: "human",
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

function toListeningReview(review: R2ListeningReviewDraft, renderSet: RenderSet, sectionId: string, eventRange: string, preferredVersionId?: string): ListeningReview {
  return {
    ...defaultListeningReview,
    review_id: `R2_REVIEW_${review.phrase_id}_${review.version_id}`,
    render_set_id: renderSet.render_set_id,
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
    training_usable: false,
    ...r2SafetyFlags,
  };
}

function deriveProgressOverview(
  phrases: PhraseDefinition[],
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

function filterPreferredVersions(preferred: PreferredVersionByPhrase, versions: RenderVersion[]) {
  const allowed = new Set(versions.map((version) => version.version_id));
  return Object.fromEntries(Object.entries(preferred).filter(([, versionId]) => allowed.has(versionId)));
}

function filterReviewDrafts(drafts: ListeningReviewByKey, versions: RenderVersion[]) {
  const allowed = new Set(versions.map((version) => version.version_id));
  return Object.fromEntries(Object.entries(drafts).filter(([, draft]) => allowed.has(draft.version_id)));
}

function abcdVersionId(versionId: string, versions: RenderVersion[]) {
  return versions.some((version) => version.version_id === versionId) ? versionId : undefined;
}

function r2ExportRows() {
  const now = new Date().toLocaleString("zh-CN", { hour12: false });
  const baseRows = phraseExports.filter((row) => row.file !== "listening_review.yaml");
  return [
    ...baseRows.slice(0, 3),
    { file: "listening_review.csv", group: "听评记录", description: "浏览器导出的当前 draft 听评表。", rule: "draft review only", scope: "all reviewed phrases", actor: "human", updatedAt: now },
    { file: "listening_review.yaml", group: "听评记录", description: "浏览器导出的当前 draft 听评 YAML。", rule: "draft review only; no e_revision_plan", scope: "all reviewed phrases", actor: "human", updatedAt: now },
    ...baseRows.slice(3),
  ];
}

function tableToCsv(table: R2PreviewTable) {
  const lines = [table.columns.join(",")];
  table.rows.forEach((row) => lines.push(table.columns.map((column) => csvCell(row[column] ?? "")).join(",")));
  return `${lines.join("\n")}\n`;
}

function tableToYaml(table: R2PreviewTable) {
  const lines = [`file: ${JSON.stringify(table.file)}`, "rows:"];
  table.rows.forEach((row) => {
    lines.push("  -");
    table.columns.forEach((column) => lines.push(`      ${column}: ${JSON.stringify(row[column] ?? "")}`));
  });
  return `${lines.join("\n")}\n`;
}

function csvCell(value: string) {
  if (!/[",\n]/.test(value)) return value;
  return `"${value.replace(/"/g, '""')}"`;
}

function readString(value: unknown) {
  return typeof value === "string" ? value : "";
}

function readRecord(value: unknown) {
  return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : undefined;
}

function phraseIdInList(value: string, phrases: PhraseDefinition[]) {
  return phrases.some((phrase) => phrase.phrase_id === value) ? value : phrases[0]?.phrase_id ?? "";
}

function versionIdInList(value: string, versions: RenderVersion[]) {
  return versions.some((version) => version.version_id === value) ? value : versions[0]?.version_id ?? "";
}

function percentWidth(value: number, total: number) {
  if (total <= 0) return "0%";
  return `${Math.min(100, Math.round((value / total) * 100))}%`;
}

function defaultMarkerId(nextMarkers: PhraseMarker[]) {
  return nextMarkers.find((item) => item.marker_type === "cadence")?.marker_id ?? nextMarkers[0]?.marker_id ?? "";
}

function versionLabel(versions: RenderVersion[], versionId: string) {
  const version = versions.find((item) => item.version_id === versionId);
  return version ? `${version.version_code} ${version.version_label_zh}` : versionId;
}

function statusLabel(status: MarkerReviewStatus) {
  return markerReviewStatusLabels[status];
}

function statusToneClass(status: MarkerReviewStatus) {
  return markerReviewStatusTone[status];
}

function severityLabel(severity: Severity) {
  return { low: "低", medium: "中", high: "高" }[severity];
}

function playModeLabel(mode: R2PlayMode) {
  return {
    idle: "已暂停",
    phrase: "phrase 播放",
    marker: "marker 播放",
    preroll: "前滚播放",
    sequence_abcd: "A→B→C→D",
    preferred: "偏好版本",
    ab_compare: "A/B 对比",
  }[mode];
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const rest = (seconds % 60).toFixed(3).padStart(6, "0");
  return `${minutes}:${rest}`;
}
