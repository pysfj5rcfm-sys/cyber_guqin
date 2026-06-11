import { useEffect, useMemo, useState } from "react";
import { AppShell } from "../components/AppShell";
import { AudioCanvas } from "../components/AudioCanvas";
import { KeyValueList, SearchBox } from "../components/FileNavigator";
import { PlaybackBar } from "../components/ReviewStatusBar";
import {
  buildRawExportPreview,
  completedMarkerCount,
  demoAudioFileName,
  demoAudioUrl,
  demoRawDuration,
  markerLabels,
  rawFiles as fallbackRawFiles,
  rawFlags,
  rawReviewUnits,
  unitStatusLabels,
} from "../mock/rawReviewMock";
import type { Marker, R0MarkerKey, ReviewUnit, ReviewUnitStatus } from "../types/cgVarw";

const apiBase = import.meta.env.VITE_CG_VARW_API_BASE ?? "http://127.0.0.1:8787";
const markerOrder: R0MarkerKey[] = ["slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"];
const markerColors: Record<R0MarkerKey, Marker<R0MarkerKey>["color"]> = {
  slate_start: "green",
  slate_end: "blue",
  guqin_start: "gold",
  tail_end: "purple",
  next_slate_start: "cyan",
};

interface RawFile {
  file_id: string;
  name: string;
  relative_path: string;
  size_bytes: number;
  modified_time: string;
  source_format: string;
}

interface Metadata {
  duration_s: number | null;
  sample_rate: number | null;
  bit_depth: number | null;
  channels: number | null;
  waveform_supported: boolean;
  warning?: string | null;
}

type BackendState =
  | { status: "connecting"; rawRootMode: "demo"; message: string }
  | { status: "offline"; rawRootMode: "demo"; message: string }
  | { status: "online"; rawRootMode: "demo" | "real"; message: string };

export function R0RawReviewPage() {
  const [units, setUnits] = useState<ReviewUnit[]>(rawReviewUnits);
  const [selectedUnitId, setSelectedUnitId] = useState("T003");
  const [selectedMarkerKey, setSelectedMarkerKey] = useState<R0MarkerKey>("guqin_start");
  const [rawFiles, setRawFiles] = useState<RawFile[]>([]);
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [sourceAudio, setSourceAudio] = useState(demoAudioFileName);
  const [audioUrl, setAudioUrl] = useState(demoAudioUrl);
  const [duration, setDuration] = useState(demoRawDuration);
  const [metadata, setMetadata] = useState<Metadata | null>(null);
  const [backend, setBackend] = useState<BackendState>({
    status: "connecting",
    rawRootMode: "demo",
    message: "正在连接后端...",
  });
  const [operationMessage, setOperationMessage] = useState("尚未保存 draft");

  useEffect(() => {
    let cancelled = false;

    async function loadBackend() {
      try {
        const health = await fetch(`${apiBase}/api/health`);
        if (!health.ok) throw new Error(`health ${health.status}`);

        const rawResponse = await fetch(`${apiBase}/api/r0/raw-files`);
        if (!rawResponse.ok) throw new Error(`raw-files ${rawResponse.status}`);
        const rawData = await rawResponse.json() as { raw_root_mode: "demo" | "real"; files: RawFile[] };
        if (cancelled) return;

        const firstFile = rawData.files[0];
        setRawFiles(rawData.files);
        setBackend({
          status: "online",
          rawRootMode: rawData.raw_root_mode,
          message:
            rawData.raw_root_mode === "demo"
              ? "后端已连接，当前使用合成演示 Raw 根目录。"
              : "后端已连接，当前使用真实 Raw 根目录。",
        });

        if (firstFile) {
          await selectBackendFile(firstFile);
        }
      } catch {
        if (cancelled) return;
        setBackend({
          status: "offline",
          rawRootMode: "demo",
          message: "后端未连接，当前仅显示前端演示数据。",
        });
        setRawFiles([]);
        setSelectedFileId(null);
        setSourceAudio(demoAudioFileName);
        setAudioUrl(demoAudioUrl);
        setDuration(demoRawDuration);
        setMetadata(null);
        setUnits(rawReviewUnits);
        setSelectedUnitId("T003");
        setSelectedMarkerKey("guqin_start");
      }
    }

    loadBackend();
    return () => {
      cancelled = true;
    };
  }, []);

  async function selectBackendFile(file: RawFile) {
    setSelectedFileId(file.file_id);
    setSourceAudio(file.name);
    setAudioUrl(`${apiBase}/api/r0/raw-files/${file.file_id}/audio`);

    const [metadataResponse, reviewUnitsResponse] = await Promise.all([
      fetch(`${apiBase}/api/r0/raw-files/${file.file_id}/metadata`),
      fetch(`${apiBase}/api/r0/raw-files/${file.file_id}/review-units`),
    ]);
    const nextMetadata = await metadataResponse.json() as Metadata;
    const reviewData = await reviewUnitsResponse.json() as { units: ReviewUnit[]; message?: string };
    setMetadata(nextMetadata);
    setDuration(nextMetadata.duration_s ?? demoRawDuration);
    const nextUnits = reviewData.units.length ? normalizeUnits(reviewData.units) : [];
    setUnits(nextUnits);
    if (nextUnits[0]) {
      setSelectedUnitId(nextUnits[0].id);
      setSelectedMarkerKey("guqin_start");
    }
    if (reviewData.message) setOperationMessage(reviewData.message);
  }

  const selectedUnit = units.find((unit) => unit.id === selectedUnitId) ?? units[0];
  const selectedMarker = selectedUnit?.markers.find((marker) => marker.key === selectedMarkerKey) ?? selectedUnit?.markers[0];
  const selectedIndex = selectedUnit ? units.findIndex((unit) => unit.id === selectedUnit.id) : -1;
  const nextUnit = selectedIndex >= 0 ? units[selectedIndex + 1] : undefined;
  const nextSlateStart = nextUnit?.markers.find((marker) => marker.key === "slate_start");
  const selectedBoundaryMarker = selectedUnit?.markers.find((marker) => marker.key === "next_slate_start");
  const isFileEndBoundary = selectedUnit?.boundary_type === "file_end";
  const boundaryLinked = Boolean(
    selectedUnit &&
      nextUnit &&
      nextSlateStart &&
      !selectedUnit.boundary_unlinked &&
      selectedBoundaryMarker?.time === nextSlateStart.time,
  );

  const canvasMarkers = useMemo(
    () =>
      units.flatMap((unit) =>
        unit.markers.map((marker) => ({
          ...marker,
          id: `${unit.id}:${marker.key}`,
          unitId: unit.id,
          weak: selectedUnit ? unit.id !== selectedUnit.id : false,
          displayLabel: selectedUnit ? unit.id === selectedUnit.id : true,
          color: unit.unit_status === "excluded" ? "red" : marker.color,
        })),
      ) satisfies Marker<R0MarkerKey>[],
    [selectedUnit?.id, units],
  );

  function selectMarkerInstance(instanceId: string) {
    const [unitId, markerKey] = instanceId.split(":") as [string, R0MarkerKey];
    if (unitId && markerKey) {
      setSelectedUnitId(unitId);
      setSelectedMarkerKey(markerKey);
    }
  }

  function updateSelectedUnit(updater: (unit: ReviewUnit, index: number) => ReviewUnit) {
    if (!selectedUnit) return;
    setUnits((current) => current.map((unit, index) => (unit.id === selectedUnit.id ? updater(unit, index) : unit)));
  }

  function nudge(deltaMs: number) {
    updateSelectedUnit((unit, index) => {
      const next = units[index + 1];
      const nextSlate = next?.markers.find((marker) => marker.key === "slate_start");
      return {
        ...unit,
        boundary_unlinked: selectedMarkerKey === "next_slate_start" && nextSlate ? true : unit.boundary_unlinked,
        markers: unit.markers.map((marker) =>
          marker.key === selectedMarkerKey ? { ...marker, time: Math.max(0, marker.time + deltaMs / 1000) } : marker,
        ),
      };
    });
  }

  function setUnitStatus(unit_status: ReviewUnitStatus) {
    updateSelectedUnit((unit) => ({ ...unit, unit_status }));
  }

  function addUnit() {
    const last = units.at(-1);
    const sequence = (last?.sequence ?? 0) + 1;
    const base = (last?.markers.find((marker) => marker.key === "next_slate_start")?.time ?? 0) + 4.52;
    const id = `T${String(sequence).padStart(3, "0")}`;
    const markers = markerOrder.map((key, index) => ({
      key,
      label: markerLabels[key],
      time: base + [0, 0.32, 1.12, 3.32, 4.52][index],
      color: markerColors[key],
      optional: key === "guqin_start" || key === "tail_end",
      source: "manual",
    }));
    setUnits((current) => [...current, { id, sequence, unit_status: "not_started", source: "manual", takeId: `DEMO_BATCH01_${id}`, markers }]);
    setSelectedUnitId(id);
    setSelectedMarkerKey("slate_start");
  }

  function excludeSelectedUnit() {
    setUnitStatus("excluded");
  }

  function restoreExcludedUnit() {
    updateSelectedUnit((unit) => ({ ...unit, unit_status: unit.unit_status === "excluded" ? "needs_review" : unit.unit_status }));
  }

  function renameSelectedUnit() {
    if (!selectedUnit) return;
    const renamedId = selectedUnit.id.endsWith("_R") ? selectedUnit.id : `${selectedUnit.id}_R`;
    setUnits((current) => current.map((unit) => (unit.id === selectedUnit.id ? { ...unit, id: renamedId } : unit)));
    setSelectedUnitId(renamedId);
  }

  async function saveDraft() {
    if (backend.status !== "online" || !selectedFileId) {
      setOperationMessage("后端未连接，无法保存 draft。");
      return;
    }
    const response = await postReview("save");
    setOperationMessage(response.ok ? "draft 已保存到 review_outputs/r0/drafts。" : "draft 保存失败。");
  }

  async function exportCsv() {
    if (backend.status !== "online" || !selectedFileId) {
      setOperationMessage("后端未连接，无法导出 CSV。");
      return;
    }
    const response = await postReview("export");
    setOperationMessage(response.ok ? "三个 review-only CSV 已导出到 review_outputs/r0/exports。" : "CSV 导出失败。");
  }

  async function postReview(action: "save" | "export") {
    const response = await fetch(`${apiBase}/api/r0/reviews/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file_id: selectedFileId,
        source_audio: sourceAudio,
        units,
      }),
    });
    return response.json() as Promise<{ ok: boolean }>;
  }

  return (
    <AppShell mode="R0" statusText={backend.message} detailText={operationMessage}>
      {{
        left: (
          <LeftPanel
            backend={backend}
            rawFiles={rawFiles}
            selectedFileId={selectedFileId}
            units={units}
            selectedUnitId={selectedUnit?.id ?? ""}
            onSelectBackendFile={selectBackendFile}
            onSelectUnit={(id) => {
              setSelectedUnitId(id);
              setSelectedMarkerKey("guqin_start");
            }}
            onAddUnit={addUnit}
            onExclude={excludeSelectedUnit}
            onRestore={restoreExcludedUnit}
            onRename={renameSelectedUnit}
          />
        ),
        main: (
          <div className="work-area">
            <div className="work-title r0-work-title">
              <div>
                <h1>R0B 合成 Raw 校验：{sourceAudio}</h1>
                {selectedUnit ? (
                  <>
                    <p>当前校验单元：{selectedUnit.id} / {selectedUnit.sequence} / {selectedUnit.takeId}</p>
                    <p>
                      来源：{sourceLabel(selectedUnit.source)} {selectedUnit.source} | 状态：{unitStatusLabels[selectedUnit.unit_status]} {selectedUnit.unit_status} | 标记：{completedMarkerCount(selectedUnit)}/5
                    </p>
                  </>
                ) : (
                  <p>未找到 ASR 候选，可手动新增 T</p>
                )}
              </div>
              <span>时长：{formatTime(duration)}</span>
            </div>
            <AudioCanvas
              markers={canvasMarkers}
              duration={duration}
              selectedKey={selectedUnit && selectedMarker ? `${selectedUnit.id}:${selectedMarker.key}` : undefined}
              onSelect={selectMarkerInstance}
              audioUrl={audioUrl}
              audioFileName={sourceAudio}
              metadata={metadata ?? undefined}
            />
            <div className={`boundary-note ${boundaryLinked || isFileEndBoundary ? "is-linked" : "is-unlinked"}`}>
              {selectedUnit && isFileEndBoundary
                ? `${selectedUnit.id}.next_slate_start 为文件结束边界：${formatTime(selectedBoundaryMarker?.time ?? duration)}`
                : selectedUnit && boundaryLinked && nextUnit
                  ? `${selectedUnit.id}.next_slate_start 已联动到 ${nextUnit.id}.slate_start`
                  : selectedUnit
                    ? `边界已解除联动${nextUnit ? `：${selectedUnit.id}.next_slate_start 与 ${nextUnit.id}.slate_start 不同` : ""}`
                    : "暂无边界可校验"}
            </div>
            <PlaybackBar time={formatTime(selectedMarker?.time ?? 0)} total={formatTime(duration)} backLabel="前滚 300ms" />
          </div>
        ),
        right: selectedUnit && selectedMarker ? (
          <R0MarkerEditor
            unit={selectedUnit}
            selectedMarkerKey={selectedMarker.key}
            onSelectMarker={setSelectedMarkerKey}
            onNudge={nudge}
            onStatus={setUnitStatus}
            onSave={saveDraft}
            onExport={exportCsv}
          />
        ) : (
          <div className="panel-stack">
            <h2>当前选中标记</h2>
            <section className="editor-section">请先新增或选择 T 单元。</section>
          </div>
        ),
        bottom: <RawExportPreviewPanel units={units} onSave={saveDraft} onExport={exportCsv} />,
      }}
    </AppShell>
  );
}

function LeftPanel({
  backend,
  rawFiles,
  selectedFileId,
  units,
  selectedUnitId,
  onSelectBackendFile,
  onSelectUnit,
  onAddUnit,
  onExclude,
  onRestore,
  onRename,
}: {
  backend: BackendState;
  rawFiles: RawFile[];
  selectedFileId: string | null;
  units: ReviewUnit[];
  selectedUnitId: string;
  onSelectBackendFile: (file: RawFile) => void;
  onSelectUnit: (id: string) => void;
  onAddUnit: () => void;
  onExclude: () => void;
  onRestore: () => void;
  onRename: () => void;
}) {
  return (
    <div className="panel-stack">
      <h2>R0 原始 Raw 文件</h2>
      <section className="editor-section">
        <h3>{backend.status === "online" ? "Raw 根目录文件" : "合成演示音频"}</h3>
        <SearchBox placeholder="搜索演示文件..." />
        <div className="file-list">
          {backend.status === "online"
            ? rawFiles.map((file) => (
                <button key={file.file_id} className={selectedFileId === file.file_id ? "selected" : ""} onClick={() => onSelectBackendFile(file)}>
                  <strong>{file.name}</strong>
                  <span>{file.source_format.toUpperCase()} | {formatBytes(file.size_bytes)} | review_only</span>
                </button>
              ))
            : fallbackRawFiles.map((file) => <button key={file.name} className={file.selected ? "selected" : ""}><strong>{file.name}</strong><span>{file.meta}</span></button>)}
        </div>
      </section>
      <section className="editor-section unit-queue-panel">
        <div className="section-title-row">
          <h3>本文件内录音单元</h3>
          <button onClick={onAddUnit}>+ 新增 T</button>
        </div>
        <div className="unit-actions">
          <button onClick={onExclude}>排除当前 T</button>
          <button onClick={onRestore}>恢复已排除 T</button>
          <button onClick={onRename}>重命名当前 T</button>
        </div>
        <div className="unit-queue">
          {units.map((unit) => (
            <button
              key={unit.id}
              className={`unit-row ${selectedUnitId === unit.id ? "selected" : ""} ${unit.unit_status === "excluded" ? "is-excluded" : ""}`}
              onClick={() => onSelectUnit(unit.id)}
            >
              <strong>{unit.id}</strong>
              <span className={`unit-status status-${unit.unit_status}`}>{unitStatusLabels[unit.unit_status]}</span>
              <span className="progress-chip">{completedMarkerCount(unit)}/5</span>
              <small>{boundaryLabel(unit.boundary_type)}</small>
              <code>{unit.takeId}</code>
            </button>
          ))}
        </div>
      </section>
      <KeyValueList rows={[
        ["当前使用", backend.rawRootMode === "real" ? "真实 Raw 根目录" : "合成演示 Raw 根目录"],
        ["连接状态", backend.status === "online" ? "后端已连接" : "未连接真实 Raw 根目录"],
        ["合成演示", String(rawFlags.synthetic_demo)],
        ["review_only", String(rawFlags.review_only)],
        ["production_grade", String(rawFlags.production_grade)],
        ["not_real_qinist_recording", String(rawFlags.not_real_qinist_recording)],
        ["not_sample_source", String(rawFlags.not_sample_source)],
        ["not_ml_training_data", String(rawFlags.not_ml_training_data)],
      ]} />
    </div>
  );
}

function R0MarkerEditor({
  unit,
  selectedMarkerKey,
  onSelectMarker,
  onNudge,
  onStatus,
  onSave,
  onExport,
}: {
  unit: ReviewUnit;
  selectedMarkerKey: R0MarkerKey;
  onSelectMarker: (key: R0MarkerKey) => void;
  onNudge: (delta: number) => void;
  onStatus: (status: ReviewUnitStatus) => void;
  onSave: () => void;
  onExport: () => void;
}) {
  const selected = unit.markers.find((marker) => marker.key === selectedMarkerKey) ?? unit.markers[0];
  const statuses: { key: ReviewUnitStatus; label: string; tone: string }[] = [
    { key: "confirmed", label: "已确认", tone: "green" },
    { key: "needs_review", label: "待复核", tone: "gold" },
    { key: "needs_retake", label: "需重录", tone: "red" },
    { key: "excluded", label: "已排除", tone: "red" },
  ];

  return (
    <div className="panel-stack">
      <h2>当前选中标记</h2>
      <div className="info-card center r0-marker-context">
        <span>当前选中标记</span>
        <strong>{unit.id} · {selected.label} {selected.key}</strong>
        <b>{formatTime(selected.time)}</b>
      </div>
      <section className="editor-section">
        <h3>标记跳转</h3>
        <div className="button-grid">
          {unit.markers.map((marker) => (
            <button key={marker.key} className={selectedMarkerKey === marker.key ? "active" : ""} onClick={() => onSelectMarker(marker.key)}>
              {marker.label}<small>{marker.key}</small>
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
        <h3>审核状态</h3>
        <div className="status-grid">
          {statuses.map((status) => (
            <button key={status.key} className={`${unit.unit_status === status.key ? "active" : ""} tone-${status.tone}`} onClick={() => onStatus(status.key)}>
              {status.label}
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>备注</h3>
        <textarea placeholder="输入备注（可选）..." maxLength={500} />
        <span className="char-count">0 / 500</span>
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

function RawExportPreviewPanel({ units, onSave, onExport }: { units: ReviewUnit[]; onSave: () => void; onExport: () => void }) {
  const preview = buildRawExportPreview(units);
  return (
    <div className="export-panel r0-export-panel">
      <div className="section-title-row">
        <h2>导出预览</h2>
        <span>仅预览 | 合成演示 | 不生成 sample_assets</span>
        <div className="row-actions">
          <button onClick={onSave} title="保存 draft">存</button>
          <button onClick={onExport} title="导出三个 CSV">导</button>
        </div>
      </div>
      <div className="export-preview-grid">
        <PreviewTable
          title="reviewed_slate_anchor_manifest.csv"
          note="按 ReviewUnit 粒度预览"
          rows={preview.reviewedManifest}
          columns={["unit_id", "unit_status", "take_id", "slate_start", "guqin_start", "synthetic_demo", "review_only"]}
        />
        <PreviewTable
          title="raw_marker_review.csv"
          note="每个标记实例一行"
          rows={preview.rawMarkerReview}
          columns={["unit_id", "marker_key", "marker_time", "unit_status", "boundary_type"]}
        />
        <PreviewTable
          title="split_plan_from_raw_markers.csv"
          note="已排除单元不导出，R0B 不执行切片"
          rows={preview.splitPlan}
          columns={["unit_id", "take_id", "not_executed", "not_sample_source", "not_ml_training_data"]}
        />
      </div>
    </div>
  );
}

function PreviewTable({
  title,
  note,
  rows,
  columns,
}: {
  title: string;
  note: string;
  rows: Record<string, string>[];
  columns: string[];
}) {
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

function normalizeUnits(units: ReviewUnit[]): ReviewUnit[] {
  return units.map((unit) => ({
    ...unit,
    takeId: unit.takeId || `TAKE_${unit.id}`,
    markers: unit.markers.map((marker) => ({
      ...marker,
      label: marker.label || markerLabels[marker.key],
      color: marker.color || markerColors[marker.key],
    })),
  }));
}

function sourceLabel(source: string) {
  return source === "asr_candidate" ? "ASR 候选" : "手动新增";
}

function boundaryLabel(boundary?: string) {
  return boundary === "file_end" ? "文件结束" : "下一口播";
}

function formatBytes(value: number) {
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
  return `${(value / 1024 / 1024).toFixed(1)} MB`;
}

function formatTime(time: number) {
  const minutes = Math.floor(time / 60);
  const seconds = time - minutes * 60;
  return `${String(minutes).padStart(2, "0")}:${seconds.toFixed(3).padStart(6, "0")}`;
}
