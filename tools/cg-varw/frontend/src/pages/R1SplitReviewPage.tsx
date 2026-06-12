import { useEffect, useMemo, useRef, useState } from "react";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { KeyValueList, SearchBox } from "../components/FileNavigator";
import type {
  Marker,
  MarkerReviewStatus,
  R1AnchorType,
  R1Marker,
  R1MarkerKey,
  R1PreAttackMusicPolicy,
  R1SegmentQC,
  R1SegmentStatus,
  R1TailPolicy,
  ReviewStatus,
  SplitBatch,
  SplitSegment,
} from "../types/cgVarw";

const apiBase = import.meta.env.VITE_CG_VARW_API_BASE ?? "http://127.0.0.1:8787";
const markerOrder: R1MarkerKey[] = ["pre_idle_end", "gesture_start", "render_anchor", "tail_end"];
const coreMarkerKeys: R1MarkerKey[] = ["render_anchor", "tail_end"];
const markerColors: Record<R1MarkerKey, Marker<R1MarkerKey>["color"]> = {
  pre_idle_end: "blue",
  gesture_start: "gold",
  render_anchor: "cyan",
  tail_end: "purple",
};
const markerLabels: Record<R1MarkerKey, string> = {
  pre_idle_end: "前置空白结束",
  gesture_start: "前导起势",
  render_anchor: "渲染锚点",
  tail_end: "尾音结束",
};
const reviewStatusLabels: Record<ReviewStatus, string> = {
  not_started: "待审",
  in_progress: "审校中",
  accepted: "已审",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已排除",
};
const markerStatusLabels: Record<MarkerReviewStatus, string> = {
  candidate: "待确认",
  accepted: "已确认",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已排除",
};
const markerStatusTone: Record<MarkerReviewStatus, string> = {
  candidate: "not_started",
  accepted: "confirmed",
  unclear: "needs_review",
  needs_retake: "needs_retake",
  rejected: "excluded",
};
const segmentStatusLabels: Record<R1SegmentStatus, string> = {
  candidate: "待审",
  render_usable: "可用于后续渲染评估",
  reference_only: "仅供参考",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已拒绝",
  excluded: "排除单元",
};

type BackendState =
  | { status: "connecting"; splitRootMode: "demo"; message: string }
  | { status: "offline"; splitRootMode: "demo"; message: string }
  | { status: "online"; splitRootMode: "demo" | "real"; message: string };

interface R1Metadata {
  duration_s: number;
  sample_rate: number | null;
  bit_depth: number | null;
  channels: number | null;
  waveform_supported: boolean;
}

interface R1Waveform {
  segment_id: string;
  duration_s: number;
  peaks: number[];
  waveform_supported: boolean;
}

interface R1DraftResponse {
  batch_id: string;
  exists: boolean;
  saved_at?: string | null;
  segments?: SplitSegment[];
}

export function R1SplitReviewPage() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [backend, setBackend] = useState<BackendState>({
    status: "connecting",
    splitRootMode: "demo",
    message: "正在连接 R1 后端...",
  });
  const [operationMessage, setOperationMessage] = useState("R1 不执行 render，不写 sample_assets。");
  const [batches, setBatches] = useState<SplitBatch[]>([]);
  const [selectedBatchId, setSelectedBatchId] = useState("");
  const [segments, setSegments] = useState<SplitSegment[]>([]);
  const [selectedSegmentId, setSelectedSegmentId] = useState("");
  const [selectedMarkerType, setSelectedMarkerType] = useState<R1MarkerKey>("render_anchor");
  const [metadata, setMetadata] = useState<R1Metadata | null>(null);
  const [waveformPeaks, setWaveformPeaks] = useState<number[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [loopAuditionEnabled, setLoopAuditionEnabled] = useState(false);
  const [loopStartS, setLoopStartS] = useState(0);
  const [loopEndS, setLoopEndS] = useState(0);

  useEffect(() => {
    let cancelled = false;
    async function loadBatches() {
      try {
        const response = await fetch(`${apiBase}/api/r1/batches`);
        if (!response.ok) throw new Error(`batches ${response.status}`);
        const data = await response.json() as { split_root_mode: "demo" | "real"; message: string; batches: SplitBatch[] };
        if (cancelled) return;
        setBatches(data.batches);
        setBackend({ status: "online", splitRootMode: data.split_root_mode, message: data.message });
        const rememberedBatch = window.localStorage.getItem("cg-varw:r1:selectedBatchId");
        const initialBatch = data.batches.find((batch) => batch.batch_id === rememberedBatch) ?? data.batches[0];
        if (initialBatch) await loadBatchReviewState(initialBatch.batch_id);
      } catch {
        if (cancelled) return;
        setBackend({ status: "offline", splitRootMode: "demo", message: "R1 后端未连接，无法加载 Split 审校数据。" });
        setOperationMessage("请启动 CG-VARW backend 后刷新 R1 Split 审校。");
      }
    }
    loadBatches();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (audioRef.current) audioRef.current.playbackRate = playbackRate;
  }, [playbackRate]);

  const selectedSegment = segments.find((segment) => segment.segment_id === selectedSegmentId) ?? segments[0];
  const selectedMarker = selectedSegment?.markers[selectedMarkerType] ?? selectedSegment?.markers.render_anchor ?? selectedSegment?.markers.tail_end;
  const audioUrl = selectedSegment ? `${apiBase}/api/r1/segments/${selectedSegment.segment_id}/audio` : "";
  const duration = metadata?.duration_s ?? selectedSegment?.duration_s ?? 0;

  const canvasMarkers = useMemo(
    () =>
      markerOrder
        .map((key) => selectedSegment?.markers[key])
        .filter(Boolean)
        .map((marker) => ({
          id: marker!.marker_type,
          key: marker!.marker_type,
          label: marker!.marker_label_zh,
          time: marker!.time_s,
          color: markerColors[marker!.marker_type],
          source: marker!.source,
          confidence: marker!.confidence,
          review_status: marker!.review_status,
          nudge_total_ms: marker!.nudge_total_ms,
          notes: marker!.notes,
        })) satisfies Marker<R1MarkerKey>[],
    [selectedSegment],
  );

  async function loadBatchReviewState(batchId: string, preferredSegmentId?: string) {
    setSelectedBatchId(batchId);
    window.localStorage.setItem("cg-varw:r1:selectedBatchId", batchId);
    setOperationMessage("正在加载当前批次 Segment...");
    const response = await fetch(`${apiBase}/api/r1/batches/${batchId}/segments`);
    if (!response.ok) throw new Error(`segments ${response.status}`);
    const data = await response.json() as { segments: SplitSegment[] };
    let nextSegments = data.segments.map(withDerivedSegmentState);
    let draftMessage = "已加载 R1 Split 合成演示数据。";
    try {
      const draftResponse = await fetch(`${apiBase}/api/r1/reviews/${batchId}/draft`);
      if (draftResponse.ok) {
        const draft = await draftResponse.json() as R1DraftResponse;
        if (draft.exists && draft.segments?.length) {
          nextSegments = mergeDraftSegments(nextSegments, draft.segments);
          draftMessage = `已加载 ${batchId} draft`;
        }
      } else {
        draftMessage = `${batchId} draft 加载失败：HTTP ${draftResponse.status}`;
      }
    } catch {
      draftMessage = `${batchId} draft 加载失败`;
    }
    setSegments(nextSegments);
    const nextSelected = nextSegments.find((segment) => segment.segment_id === preferredSegmentId) ?? nextSegments[0];
    if (nextSelected) {
      setSelectedSegmentId(nextSelected.segment_id);
      setSelectedMarkerType("render_anchor");
      await loadSegmentAssets(nextSelected);
    }
    setOperationMessage(draftMessage);
  }

  async function selectBatch(batchId: string) {
    await loadBatchReviewState(batchId);
  }

  async function selectSegment(segmentId: string) {
    const segment = segments.find((item) => item.segment_id === segmentId);
    if (!segment) return;
    setSelectedSegmentId(segment.segment_id);
    setSelectedMarkerType("render_anchor");
    setCurrentTime(0);
    setLoopAuditionEnabled(false);
    await loadSegmentAssets(segment);
  }

  async function loadSegmentAssets(segment: SplitSegment) {
    try {
      const [metadataResponse, waveformResponse] = await Promise.all([
        fetch(`${apiBase}/api/r1/segments/${segment.segment_id}/metadata`),
        fetch(`${apiBase}/api/r1/segments/${segment.segment_id}/waveform?points=1600`),
      ]);
      if (metadataResponse.ok) setMetadata(await metadataResponse.json() as R1Metadata);
      if (waveformResponse.ok) {
        const waveform = await waveformResponse.json() as R1Waveform;
        setWaveformPeaks(waveform.waveform_supported ? waveform.peaks : []);
      }
    } catch {
      setWaveformPeaks([]);
    }
  }

  function jumpToMarker(markerType: R1MarkerKey, shouldPlay = false) {
    const marker = selectedSegment?.markers[markerType];
    if (!marker) return;
    setSelectedMarkerType(markerType);
    if (audioRef.current) {
      audioRef.current.currentTime = marker.time_s;
      setCurrentTime(marker.time_s);
      if (shouldPlay) {
        audioRef.current.playbackRate = playbackRate;
        void audioRef.current.play();
      }
    }
  }

  function updateSelectedSegment(updater: (segment: SplitSegment) => SplitSegment) {
    if (!selectedSegment) return;
    setSegments((current) =>
      current.map((segment) => segment.segment_id === selectedSegment.segment_id ? withDerivedSegmentState(updater(segment)) : segment),
    );
  }

  function updateSelectedMarker(updater: (marker: R1Marker) => R1Marker) {
    updateSelectedSegment((segment) => {
      const marker = segment.markers[selectedMarkerType];
      if (!marker) return segment;
      return {
        ...segment,
        markers: {
          ...segment.markers,
          [selectedMarkerType]: updater(marker),
        },
      };
    });
  }

  function nudge(deltaMs: number) {
    updateSelectedMarker((marker) => ({
      ...marker,
      time_s: Math.max(0, Number((marker.time_s + deltaMs / 1000).toFixed(3))),
      source: "human_adjusted",
      nudge_total_ms: (marker.nudge_total_ms ?? 0) + deltaMs,
    }));
  }

  function setMarkerStatus(review_status: MarkerReviewStatus) {
    updateSelectedMarker((marker) => ({ ...marker, review_status }));
  }

  function setPolicy<Key extends "anchor_type" | "pre_attack_music_policy" | "tail_policy">(key: Key, value: SplitSegment[Key]) {
    updateSelectedSegment((segment) => ({ ...segment, [key]: value }));
  }

  function updateQc(key: keyof R1SegmentQC, value: boolean | string) {
    updateSelectedSegment((segment) => ({ ...segment, qc: { ...segment.qc, [key]: value } }));
  }

  function setSegmentConclusion(status: R1SegmentStatus) {
    updateSelectedSegment((segment) => ({
      ...segment,
      segment_status: status,
      qc: {
        ...segment.qc,
        render_usable: status === "render_usable",
        reference_only: status === "reference_only",
        unclear: status === "unclear",
        needs_retake: status === "needs_retake",
        rejected: status === "rejected" || status === "excluded",
      },
    }));
  }

  function updateNotes(notes: string) {
    updateSelectedSegment((segment) => ({ ...segment, notes }));
  }

  function playPause() {
    const audio = audioRef.current;
    if (!audio) return;
    if (!audio.paused) {
      audio.pause();
      return;
    }
    if (selectedMarker) audio.currentTime = selectedMarker.time_s;
    audio.playbackRate = playbackRate;
    void audio.play();
  }

  function playBefore(deltaS: number) {
    const audio = audioRef.current;
    if (!audio) return;
    const start = Math.max(0, selectedMarker ? selectedMarker.time_s - deltaS : audio.currentTime - deltaS);
    audio.currentTime = start;
    audio.playbackRate = playbackRate;
    void audio.play();
  }

  function toggleLoopAudition() {
    const audio = audioRef.current;
    if (!audio || !selectedSegment || !selectedMarker) return;
    if (loopAuditionEnabled) {
      setLoopAuditionEnabled(false);
      return;
    }
    const window = loopWindowForMarker(selectedSegment, selectedMarker.marker_type, duration);
    setLoopStartS(window.start);
    setLoopEndS(window.end);
    setLoopAuditionEnabled(true);
    audio.currentTime = window.start;
    audio.playbackRate = playbackRate;
    void audio.play();
  }

  function changePlaybackRate(rate: number) {
    setPlaybackRate(rate);
    if (audioRef.current) audioRef.current.playbackRate = rate;
  }

  function handleTimeUpdate() {
    const audio = audioRef.current;
    if (!audio) return;
    if (loopAuditionEnabled && loopEndS > loopStartS && audio.currentTime >= loopEndS) {
      audio.currentTime = loopStartS;
      void audio.play();
    }
    setCurrentTime(audio.currentTime);
  }

  async function saveDraft() {
    if (backend.status !== "online" || !selectedBatchId) {
      setOperationMessage("R1 后端未连接，无法保存 draft。");
      return;
    }
    const response = await postReview("save");
    if (response.ok) {
      setOperationMessage("draft 已保存");
      await loadBatchReviewState(selectedBatchId, selectedSegment?.segment_id);
    } else {
      setOperationMessage("draft 保存失败。");
    }
  }

  async function exportCsv() {
    if (backend.status !== "online" || !selectedBatchId) {
      setOperationMessage("R1 后端未连接，无法导出 CSV。");
      return;
    }
    const response = await postReview("export");
    setOperationMessage(response.ok ? "三个 review-only CSV 已导出到 review_outputs/r1/exports/{batch_id}。" : "CSV 导出失败。");
  }

  async function postReview(action: "save" | "export") {
    const response = await fetch(`${apiBase}/api/r1/reviews/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        batch_id: selectedBatchId,
        segments: segments.map(withDerivedSegmentState),
        notes: "R1 review-only split marker draft",
      }),
    });
    return response.json() as Promise<{ ok: boolean }>;
  }

  return (
    <AppShell mode="R1" statusText={backend.message} detailText={operationMessage}>
      {{
        left: (
          <LeftPanel
            batches={batches}
            selectedBatchId={selectedBatchId}
            segments={segments}
            selectedSegmentId={selectedSegment?.segment_id ?? ""}
            onSelectBatch={(batchId) => void selectBatch(batchId)}
            onSelectSegment={(segmentId) => void selectSegment(segmentId)}
          />
        ),
        main: (
          <div className="work-area">
            <audio
              ref={audioRef}
              src={audioUrl}
              preload="auto"
              onTimeUpdate={handleTimeUpdate}
              onPlay={() => setIsPlaying(true)}
              onPause={() => setIsPlaying(false)}
              onEnded={() => setIsPlaying(false)}
              onLoadedMetadata={(event) => {
                if (!metadata) setMetadata({ duration_s: event.currentTarget.duration, sample_rate: null, bit_depth: null, channels: null, waveform_supported: true });
              }}
            />
            <div className="work-title r0-work-title">
              <div>
                <h1>当前选择：{selectedSegment ? `${selectedSegment.batch_id} / ${selectedSegment.file_name}` : "未选择 Segment"}</h1>
                {selectedSegment && (
                  <>
                    <p>事件：{selectedSegment.event_id} · Segment ID：{selectedSegment.segment_id} · 版本：{selectedSegment.variant}</p>
                    <p>
                      时长：{formatTime(duration)} · 状态：{reviewStatusLabels[selectedSegment.review_status]} ·
                      核心{acceptedCount(selectedSegment, coreMarkerKeys)}/2 · 标记{acceptedCount(selectedSegment, markerOrder)}/4
                    </p>
                  </>
                )}
              </div>
            </div>
            <AudioCanvas
              markers={canvasMarkers}
              duration={Math.max(duration, 0.1)}
              selectedKey={selectedMarkerType}
              onSelect={(key) => jumpToMarker(key as R1MarkerKey, false)}
              audioUrl={audioUrl}
              audioFileName={selectedSegment?.file_name}
              metadata={metadata ?? undefined}
              waveformPeaks={waveformPeaks}
            />
            <R1PlaybackBar
              time={formatTime(currentTime)}
              total={formatTime(duration)}
              isPlaying={isPlaying}
              playbackRate={playbackRate}
              loopAuditionEnabled={loopAuditionEnabled}
              onPlayPause={playPause}
              onBack100={() => playBefore(0.1)}
              onBack300={() => playBefore(0.3)}
              onToggleLoop={toggleLoopAudition}
              onRateChange={changePlaybackRate}
            />
          </div>
        ),
        right: selectedSegment && selectedMarker ? (
          <R1MarkerEditor
            segment={selectedSegment}
            marker={selectedMarker}
            selectedMarkerType={selectedMarkerType}
            onSelectMarker={(key) => jumpToMarker(key, false)}
            onNudge={nudge}
            onMarkerStatus={setMarkerStatus}
            onPolicy={setPolicy}
            onQc={updateQc}
            onSegmentConclusion={setSegmentConclusion}
            onNotes={updateNotes}
            onSave={saveDraft}
            onExport={exportCsv}
          />
        ) : (
          <div className="panel-stack">
            <h2>标记编辑</h2>
            <section className="editor-section">请选择 Split Segment。</section>
          </div>
        ),
        bottom: <R1ExportPreviewPanel segments={segments} onSave={saveDraft} onExport={exportCsv} />,
      }}
    </AppShell>
  );
}

function LeftPanel({
  batches,
  selectedBatchId,
  segments,
  selectedSegmentId,
  onSelectBatch,
  onSelectSegment,
}: {
  batches: SplitBatch[];
  selectedBatchId: string;
  segments: SplitSegment[];
  selectedSegmentId: string;
  onSelectBatch: (batchId: string) => void;
  onSelectSegment: (segmentId: string) => void;
}) {
  const selectedBatch = batches.find((batch) => batch.batch_id === selectedBatchId);
  return (
    <div className="panel-stack">
      <h2>Split 文件审校</h2>
      <section className="editor-section">
        <h3>批次筛选</h3>
        <select value={selectedBatchId} onChange={(event) => onSelectBatch(event.target.value)}>
          {batches.map((batch) => <option key={batch.batch_id} value={batch.batch_id}>{batch.display_name}</option>)}
        </select>
      </section>
      <section className="editor-section unit-queue-panel">
        <div className="section-title-row">
          <h3>录音单元 / Segment</h3>
          <span>当前批次：{selectedBatchId || "未加载"}</span>
        </div>
        <SearchBox placeholder="搜索 T / segment..." />
        <div className="unit-queue">
          {segments.map((segment) => (
            <button
              key={segment.segment_id}
              className={`unit-row r1-unit-row ${selectedSegmentId === segment.segment_id ? "selected" : ""} ${segment.segment_status === "excluded" ? "is-excluded" : ""}`}
              onClick={() => onSelectSegment(segment.segment_id)}
            >
              <strong>{segment.file_name}</strong>
              <span className={`unit-status status-${segmentStatusClass(segment.segment_status)}`}>{segmentStatusLabels[segment.segment_status]}</span>
              <span className="progress-chip">核心{acceptedCount(segment, coreMarkerKeys)}/2</span>
              <small>标记{acceptedCount(segment, markerOrder)}/4</small>
              <code>{segment.take_id} · {formatTime(segment.duration_s)} · {segment.segment_id}</code>
            </button>
          ))}
        </div>
      </section>
      <KeyValueList rows={[
        ["batch_id", selectedBatch?.batch_id ?? selectedBatchId],
        ["display_name", selectedBatch?.display_name ?? ""],
        ["segment_count", String(selectedBatch?.segment_count ?? segments.length)],
        ["source", selectedBatch?.source ?? ""],
      ]} />
    </div>
  );
}

function R1MarkerEditor({
  segment,
  marker,
  selectedMarkerType,
  onSelectMarker,
  onNudge,
  onMarkerStatus,
  onPolicy,
  onQc,
  onSegmentConclusion,
  onNotes,
  onSave,
  onExport,
}: {
  segment: SplitSegment;
  marker: R1Marker;
  selectedMarkerType: R1MarkerKey;
  onSelectMarker: (key: R1MarkerKey) => void;
  onNudge: (delta: number) => void;
  onMarkerStatus: (status: MarkerReviewStatus) => void;
  onPolicy: <Key extends "anchor_type" | "pre_attack_music_policy" | "tail_policy">(key: Key, value: SplitSegment[Key]) => void;
  onQc: (key: keyof R1SegmentQC, value: boolean | string) => void;
  onSegmentConclusion: (status: R1SegmentStatus) => void;
  onNotes: (notes: string) => void;
  onSave: () => void;
  onExport: () => void;
}) {
  const statusButtons: { key: MarkerReviewStatus; label: string; tone: string }[] = [
    { key: "accepted", label: "标记确认", tone: "green" },
    { key: "unclear", label: "待复核", tone: "gold" },
    { key: "needs_retake", label: "需重录", tone: "red" },
    { key: "rejected", label: "排除此标记", tone: "red" },
  ];

  return (
    <div className="panel-stack">
      <h2>标记级审校</h2>
      <div className="info-card center">
        <span>当前选中标记</span>
        <strong>{segment.take_id} · {marker.marker_label_zh} {marker.marker_type}</strong>
        <b>{marker.time_s.toFixed(3)}s</b>
        <span className={`unit-status status-${markerStatusTone[marker.review_status]}`}>状态：{markerStatusLabels[marker.review_status]}</span>
      </div>
      <section className="editor-section">
        <h3>标记跳转</h3>
        <div className="button-grid">
          {markerOrder.map((key) => (
            <button key={key} className={selectedMarkerType === key ? "active" : ""} onClick={() => onSelectMarker(key)}>
              {markerLabels[key]}<small>{key}</small>
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>微调</h3>
        <div className="nudge-grid">
          {[-50, -10, -5, 5, 10, 50].map((delta) => (
            <button key={delta} onClick={() => onNudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>标记审核状态</h3>
        <div className="status-grid">
          {statusButtons.map((status) => (
            <button key={status.key} className={`${marker.review_status === status.key ? "active" : ""} tone-${status.tone}`} onClick={() => onMarkerStatus(status.key)}>
              {status.label}
            </button>
          ))}
        </div>
      </section>
      <h2>Segment 级审校</h2>
      <section className="editor-section">
        <h3>锚点类型</h3>
        <SelectField
          value={segment.anchor_type}
          options={[
            ["main_attack", "主发声点 main_attack"],
            ["gesture_start", "前导起势点 gesture_start"],
            ["context_first_attach", "上下文首触点 context_first_attach"],
          ]}
          onChange={(value) => onPolicy("anchor_type", value as R1AnchorType)}
          help="锚点类型说明 render_anchor 代表什么。普通古琴单音默认使用“主发声点”。"
        />
      </section>
      <section className="editor-section">
        <h3>前置内容策略</h3>
        <SelectField
          value={segment.pre_attack_music_policy}
          options={[
            ["keep_silence", "保留静音缓冲 keep_silence"],
            ["preserve", "保留前导音乐 preserve"],
          ]}
          onChange={(value) => onPolicy("pre_attack_music_policy", value as R1PreAttackMusicPolicy)}
          help="render_anchor 前只是静音或安全余量时选“保留静音缓冲”；存在绰注、滑入、连接声等音乐性内容时选“保留前导音乐”。"
        />
      </section>
      <section className="editor-section">
        <h3>尾音策略</h3>
        <SelectField
          value={segment.tail_policy}
          options={[
            ["smart_fade_100ms", "智能淡出 100ms smart_fade_100ms"],
            ["full_tail", "保留完整尾音 full_tail"],
          ]}
          onChange={(value) => onPolicy("tail_policy", value as R1TailPolicy)}
          help="R1A 只记录策略，不执行实际 fade，不生成 render audio。"
        />
      </section>
      <section className="editor-section">
        <h3>Segment 审核状态</h3>
        <div className="status-grid">
          {[
            ["render_usable", "可用于后续渲染评估"],
            ["reference_only", "仅供参考"],
            ["unclear", "待复核"],
            ["needs_retake", "需重录"],
            ["rejected", "已拒绝"],
            ["excluded", "排除单元"],
          ].map(([key, label]) => (
            <button key={key} className={segment.segment_status === key ? "active" : ""} onClick={() => onSegmentConclusion(key as R1SegmentStatus)}>
              {label}
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>QC 标记</h3>
        <div className="issue-grid">
          {[
            ["noise_issue", "噪声问题"],
            ["click_issue", "click 问题"],
            ["tail_clipped", "尾音被切"],
            ["attack_clipped", "起声被切"],
            ["slate_residue", "口播残留"],
            ["wrong_take", "错误 take"],
          ].map(([key, label]) => (
            <label key={key}><input type="checkbox" checked={Boolean(segment.qc[key as keyof R1SegmentQC])} onChange={(event) => onQc(key as keyof R1SegmentQC, event.target.checked)} /> {label}</label>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>Segment 备注</h3>
        <textarea value={segment.notes ?? ""} onChange={(event) => onNotes(event.target.value)} placeholder="输入备注（可选）..." maxLength={500} />
        <span className="char-count">{(segment.notes ?? "").length} / 500</span>
      </section>
      <section className="editor-section">
        <h3>保存与导出</h3>
        <div className="action-row">
          <button onClick={onSave}>保存 draft</button>
          <button onClick={onExport}>导出 CSV</button>
        </div>
      </section>
    </div>
  );
}

function R1PlaybackBar({
  time,
  total,
  isPlaying,
  playbackRate,
  loopAuditionEnabled,
  onPlayPause,
  onBack100,
  onBack300,
  onToggleLoop,
  onRateChange,
}: {
  time: string;
  total: string;
  isPlaying: boolean;
  playbackRate: number;
  loopAuditionEnabled: boolean;
  onPlayPause: () => void;
  onBack100: () => void;
  onBack300: () => void;
  onToggleLoop: () => void;
  onRateChange: (rate: number) => void;
}) {
  return (
    <div className="playback-bar">
      <button className="play-button" onClick={onPlayPause}>{isPlaying ? "暂停" : "播放"}<span>{isPlaying ? "播放" : "暂停"}</span></button>
      <button onClick={onBack100}>前滚 100ms</button>
      <button onClick={onBack300}>前滚 300ms</button>
      <button className={loopAuditionEnabled ? "active" : ""} onClick={onToggleLoop}>循环试听</button>
      <strong className="clock">{time}<small>/ {total}</small></strong>
      <span className="speed-label">播放速度</span>
      {[0.5, 1, 1.5].map((rate) => (
        <button key={rate} className={playbackRate === rate ? "active" : ""} onClick={() => onRateChange(rate)}>
          {rate}x
        </button>
      ))}
    </div>
  );
}

function SelectField({
  value,
  options,
  onChange,
  help,
}: {
  value: string;
  options: [string, string][];
  onChange: (value: string) => void;
  help: string;
}) {
  return (
    <div className="cg-select-row">
      <select className="cg-select" value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map(([key, label]) => <option key={key} value={key}>{label}</option>)}
      </select>
      <small className="cg-select-help">{help}</small>
    </div>
  );
}

function R1ExportPreviewPanel({ segments, onSave, onExport }: { segments: SplitSegment[]; onSave: () => void; onExport: () => void }) {
  const preview = buildR1ExportPreview(segments.map(withDerivedSegmentState));
  return (
    <div className="export-panel r0-export-panel">
      <div className="section-title-row">
        <h2>导出预览</h2>
        <span>仅预览 | review_only=true | production_grade=false | 不写 sample_assets | R1 不执行 render</span>
        <div className="row-actions">
          <button onClick={onSave} title="保存 draft">存</button>
          <button onClick={onExport} title="导出三个 CSV">导</button>
        </div>
      </div>
      <div className="export-preview-grid">
        <PreviewTable
          title="reviewed_render_anchors.csv"
          note="一行一个 segment / clean wav"
          rows={preview.renderAnchors}
          columns={["take_id", "render_anchor_s", "tail_end_s", "anchor_type", "render_usable", "review_status"]}
        />
        <PreviewTable
          title="split_marker_review.csv"
          note="一行一个标记实例"
          rows={preview.markerReview}
          columns={["take_id", "marker_type", "marker_label_zh", "time_s", "review_status", "nudge_total_ms"]}
        />
        <PreviewTable
          title="segment_qc_sheet.csv"
          note="一行一个 segment QC 结论"
          rows={preview.qcRows}
          columns={["take_id", "render_usable", "reference_only", "unclear", "needs_retake", "rejected"]}
        />
      </div>
    </div>
  );
}

function PreviewTable({ title, note, rows, columns }: { title: string; note: string; rows: Record<string, string>[]; columns: string[] }) {
  return (
    <section className="preview-card">
      <h3><span className="file-icon">CSV</span>{title}</h3>
      <small>{note}</small>
      <table>
        <thead>
          <tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${title}-${index}`}>
              {columns.map((column) => <td key={column}>{row[column]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

function withDerivedSegmentState(segment: SplitSegment): SplitSegment {
  const review_status = deriveReviewStatus(segment);
  const render_usable = deriveRenderUsable(segment);
  const qc = {
    ...segment.qc,
    render_usable,
    reference_only: segment.segment_status === "reference_only" || segment.qc.reference_only,
    unclear: review_status === "unclear" || segment.segment_status === "unclear" || segment.qc.unclear,
    needs_retake: review_status === "needs_retake" || segment.segment_status === "needs_retake" || segment.qc.needs_retake,
    rejected: review_status === "rejected" || segment.segment_status === "rejected" || segment.segment_status === "excluded" || segment.qc.rejected,
  };
  const segment_status = segment.segment_status === "excluded"
    ? "excluded"
    : render_usable
      ? "render_usable"
      : qc.reference_only
        ? "reference_only"
        : qc.needs_retake
          ? "needs_retake"
          : qc.rejected
            ? "rejected"
            : qc.unclear
              ? "unclear"
              : "candidate";
  return { ...segment, review_status, segment_status, qc };
}

function mergeDraftSegments(defaultSegments: SplitSegment[], draftSegments: SplitSegment[]) {
  const draftsBySegmentId = new Map(draftSegments.map((segment) => [segment.segment_id, segment]));
  return defaultSegments.map((segment) => {
    const draft = draftsBySegmentId.get(segment.segment_id);
    if (!draft) return segment;
    return withDerivedSegmentState({
      ...segment,
      ...draft,
      batch_id: segment.batch_id,
      take_id: segment.take_id,
      file_name: segment.file_name,
      relative_path: segment.relative_path,
      duration_s: segment.duration_s,
      sample_rate: segment.sample_rate,
      bit_depth: segment.bit_depth,
      channels: segment.channels,
      markers: {
        ...segment.markers,
        ...draft.markers,
      },
      qc: {
        ...segment.qc,
        ...draft.qc,
      },
      review_only: true,
      production_grade: false,
      not_sample_assets: true,
      not_render_executed: true,
      not_ml_training_data: true,
    });
  });
}

function deriveReviewStatus(segment: SplitSegment): ReviewStatus {
  const markers = markerOrder.map((key) => segment.markers[key]).filter(Boolean) as R1Marker[];
  const core = coreMarkerKeys.map((key) => segment.markers[key]).filter(Boolean) as R1Marker[];
  const renderAnchor = segment.markers.render_anchor;
  const tailEnd = segment.markers.tail_end;
  if (segment.segment_status === "excluded") return "rejected";
  if (core.some((marker) => marker.review_status === "needs_retake")) return "needs_retake";
  if (core.some((marker) => marker.review_status === "rejected")) return "rejected";
  if (renderAnchor?.review_status === "accepted" && tailEnd?.review_status === "accepted") return "accepted";
  if (markers.some((marker) => marker.review_status === "unclear")) return "unclear";
  if (markers.some((marker) => marker.review_status !== "candidate" || (marker.nudge_total_ms ?? 0) !== 0)) return "in_progress";
  return "not_started";
}

function deriveRenderUsable(segment: SplitSegment) {
  const renderAnchor = segment.markers.render_anchor;
  const tailEnd = segment.markers.tail_end;
  if (segment.segment_status === "excluded") return false;
  if (renderAnchor?.review_status !== "accepted" || tailEnd?.review_status !== "accepted") return false;
  if (segment.qc.attack_clipped || segment.qc.tail_clipped || segment.qc.wrong_take) return false;
  return true;
}

function loopWindowForMarker(segment: SplitSegment, markerType: R1MarkerKey, duration: number) {
  const marker = segment.markers[markerType] ?? segment.markers.render_anchor ?? segment.markers.tail_end;
  if (!marker) return { start: 0, end: Math.min(duration, 1) };
  const tailEnd = segment.markers.tail_end;
  if (marker.marker_type === "render_anchor" && tailEnd) {
    return { start: Math.max(0, marker.time_s - 0.2), end: Math.min(duration, tailEnd.time_s + 0.2) };
  }
  return { start: Math.max(0, marker.time_s - 0.2), end: Math.min(duration, marker.time_s + 0.8) };
}

function acceptedCount(segment: SplitSegment, keys: R1MarkerKey[]) {
  return keys.filter((key) => segment.markers[key]?.review_status === "accepted").length;
}

function buildR1ExportPreview(segments: SplitSegment[]) {
  return {
    renderAnchors: segments.map((segment) => ({
      take_id: segment.take_id,
      render_anchor_s: timeField(segment.markers.render_anchor),
      tail_end_s: timeField(segment.markers.tail_end),
      anchor_type: segment.anchor_type,
      render_usable: String(segment.qc.render_usable),
      review_status: segment.review_status,
    })),
    markerReview: segments.flatMap((segment) =>
      markerOrder.map((key) => {
        const marker = segment.markers[key];
        return {
          take_id: segment.take_id,
          marker_type: key,
          marker_label_zh: marker?.marker_label_zh ?? markerLabels[key],
          time_s: timeField(marker),
          review_status: marker?.review_status ?? "candidate",
          nudge_total_ms: String(marker?.nudge_total_ms ?? 0),
        };
      }),
    ),
    qcRows: segments.map((segment) => ({
      take_id: segment.take_id,
      render_usable: String(segment.qc.render_usable),
      reference_only: String(segment.qc.reference_only),
      unclear: String(segment.qc.unclear),
      needs_retake: String(segment.qc.needs_retake),
      rejected: String(segment.qc.rejected),
    })),
  };
}

function timeField(marker?: R1Marker) {
  return marker ? marker.time_s.toFixed(3) : "";
}

function statusClass(status: ReviewStatus) {
  if (status === "accepted") return "confirmed";
  if (status === "needs_retake" || status === "rejected") return "needs_retake";
  if (status === "not_started") return "not_started";
  return "needs_review";
}

function segmentStatusClass(status: R1SegmentStatus) {
  if (status === "render_usable") return "confirmed";
  if (status === "reference_only" || status === "unclear") return "needs_review";
  if (status === "needs_retake" || status === "rejected") return "needs_retake";
  if (status === "excluded") return "excluded";
  return "not_started";
}

function formatTime(time: number) {
  const minutes = Math.floor(time / 60);
  const seconds = time - minutes * 60;
  return `${String(minutes).padStart(2, "0")}:${seconds.toFixed(3).padStart(6, "0")}`;
}
