import { useMemo, useState } from "react";
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
  rawFiles,
  rawFlags,
  rawReviewUnits,
  unitStatusLabels,
} from "../mock/rawReviewMock";
import type { Marker, R0MarkerKey, ReviewUnit, ReviewUnitStatus } from "../types/cgVarw";

const markerOrder: R0MarkerKey[] = ["slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"];

export function R0RawReviewPage() {
  const [units, setUnits] = useState<ReviewUnit[]>(rawReviewUnits);
  const [selectedUnitId, setSelectedUnitId] = useState("T003");
  const [selectedMarkerKey, setSelectedMarkerKey] = useState<R0MarkerKey>("guqin_start");

  const selectedUnit = units.find((unit) => unit.id === selectedUnitId) ?? units[0];
  const selectedMarker = selectedUnit.markers.find((marker) => marker.key === selectedMarkerKey) ?? selectedUnit.markers[0];
  const selectedIndex = units.findIndex((unit) => unit.id === selectedUnit.id);
  const nextUnit = selectedIndex >= 0 ? units[selectedIndex + 1] : undefined;
  const nextSlateStart = nextUnit?.markers.find((marker) => marker.key === "slate_start");
  const selectedBoundaryMarker = selectedUnit.markers.find((marker) => marker.key === "next_slate_start");
  const isFileEndBoundary = selectedUnit.boundary_type === "file_end";
  const boundaryLinked = Boolean(
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
          weak: unit.id !== selectedUnit.id,
          displayLabel: unit.id === selectedUnit.id,
          color: unit.unit_status === "excluded" ? "red" : marker.color,
        })),
      ) satisfies Marker<R0MarkerKey>[],
    [selectedUnit.id, units],
  );

  function selectMarkerInstance(instanceId: string) {
    const [unitId, markerKey] = instanceId.split(":") as [string, R0MarkerKey];
    if (unitId && markerKey) {
      setSelectedUnitId(unitId);
      setSelectedMarkerKey(markerKey);
    }
  }

  function updateSelectedUnit(updater: (unit: ReviewUnit, index: number) => ReviewUnit) {
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
      color: ({ slate_start: "green", slate_end: "blue", guqin_start: "gold", tail_end: "purple", next_slate_start: "cyan" } as const)[key],
      optional: key === "guqin_start" || key === "tail_end",
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
    const renamedId = selectedUnit.id.endsWith("_R") ? selectedUnit.id : `${selectedUnit.id}_R`;
    setUnits((current) => current.map((unit) => (unit.id === selectedUnit.id ? { ...unit, id: renamedId } : unit)));
    setSelectedUnitId(renamedId);
  }

  return (
    <AppShell
      mode="R0"
      left={
        <LeftPanel
          units={units}
          selectedUnitId={selectedUnit.id}
          onSelectUnit={(id) => {
            setSelectedUnitId(id);
            setSelectedMarkerKey("guqin_start");
          }}
          onAddUnit={addUnit}
          onExclude={excludeSelectedUnit}
          onRestore={restoreExcludedUnit}
          onRename={renameSelectedUnit}
        />
      }
      main={
        <div className="work-area">
          <div className="work-title r0-work-title">
            <div>
              <h1>R0B synthetic raw review: {demoAudioFileName}</h1>
              <p>Selected unit: {selectedUnit.id} / {selectedUnit.sequence} / {selectedUnit.takeId}</p>
              <p>
                Source: {selectedUnit.source} | Status: {unitStatusLabels[selectedUnit.unit_status]} | Markers: {completedMarkerCount(selectedUnit)}/5
              </p>
            </div>
            <span>Duration: {formatTime(demoRawDuration)}</span>
          </div>
          <AudioCanvas
            markers={canvasMarkers}
            duration={demoRawDuration}
            selectedKey={`${selectedUnit.id}:${selectedMarker.key}`}
            onSelect={selectMarkerInstance}
            audioUrl={demoAudioUrl}
            audioFileName={demoAudioFileName}
          />
          <div className={`boundary-note ${boundaryLinked || isFileEndBoundary ? "is-linked" : "is-unlinked"}`}>
            {isFileEndBoundary
              ? `${selectedUnit.id}.next_slate_start is the file_end boundary at ${formatTime(selectedBoundaryMarker?.time ?? demoRawDuration)}`
              : boundaryLinked && nextUnit
                ? `${selectedUnit.id}.next_slate_start is linked to ${nextUnit.id}.slate_start`
                : `Boundary unlinked${nextUnit ? `: ${selectedUnit.id}.next_slate_start differs from ${nextUnit.id}.slate_start` : ""}`}
          </div>
          <PlaybackBar time={formatTime(selectedMarker.time)} total={formatTime(demoRawDuration)} backLabel="Back 300ms" />
        </div>
      }
      right={
        <R0MarkerEditor
          unit={selectedUnit}
          selectedMarkerKey={selectedMarker.key}
          onSelectMarker={setSelectedMarkerKey}
          onNudge={nudge}
          onStatus={setUnitStatus}
        />
      }
      bottom={<RawExportPreviewPanel units={units} />}
    />
  );
}

function LeftPanel({
  units,
  selectedUnitId,
  onSelectUnit,
  onAddUnit,
  onExclude,
  onRestore,
  onRename,
}: {
  units: ReviewUnit[];
  selectedUnitId: string;
  onSelectUnit: (id: string) => void;
  onAddUnit: () => void;
  onExclude: () => void;
  onRestore: () => void;
  onRename: () => void;
}) {
  return (
    <div className="panel-stack">
      <h2>R0 raw files</h2>
      <section className="editor-section">
        <h3>Demo raw audio</h3>
        <SearchBox placeholder="Search demo files..." />
        <div className="file-list">
          {rawFiles.map((file) => <button key={file.name} className={file.selected ? "selected" : ""}><strong>{file.name}</strong><span>{file.meta}</span></button>)}
        </div>
      </section>
      <section className="editor-section unit-queue-panel">
        <div className="section-title-row">
          <h3>T units in this file</h3>
          <button onClick={onAddUnit}>+ Add T</button>
        </div>
        <div className="unit-actions">
          <button onClick={onExclude}>Exclude current T</button>
          <button onClick={onRestore}>Restore excluded T</button>
          <button onClick={onRename}>Rename current T</button>
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
              <small>{unit.boundary_type ?? "next_slate_start"}</small>
              <code>{unit.takeId}</code>
            </button>
          ))}
        </div>
      </section>
      <KeyValueList rows={[
        ["workspace", "tools/cg-varw/sample_workspace/raw_audio"],
        ["current_raw", demoAudioFileName],
        ["synthetic_demo", String(rawFlags.synthetic_demo)],
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
}: {
  unit: ReviewUnit;
  selectedMarkerKey: R0MarkerKey;
  onSelectMarker: (key: R0MarkerKey) => void;
  onNudge: (delta: number) => void;
  onStatus: (status: ReviewUnitStatus) => void;
}) {
  const selected = unit.markers.find((marker) => marker.key === selectedMarkerKey) ?? unit.markers[0];
  const statuses: { key: ReviewUnitStatus; label: string; tone: string }[] = [
    { key: "confirmed", label: "Confirmed", tone: "green" },
    { key: "needs_review", label: "Needs review", tone: "gold" },
    { key: "needs_retake", label: "Needs retake", tone: "red" },
    { key: "excluded", label: "Excluded", tone: "red" },
  ];

  return (
    <div className="panel-stack">
      <h2>Selected marker</h2>
      <div className="info-card center r0-marker-context">
        <span>Current marker</span>
        <strong>{unit.id} | {selected.label}</strong>
        <code>{selected.key}</code>
        <b>{formatTime(selected.time)}</b>
      </div>
      <section className="editor-section">
        <h3>Marker jump</h3>
        <div className="button-grid">
          {unit.markers.map((marker) => (
            <button key={marker.key} className={selectedMarkerKey === marker.key ? "active" : ""} onClick={() => onSelectMarker(marker.key)}>
              {marker.label}<small>{marker.key}</small>
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>Nudge</h3>
        <div className="nudge-grid">
          {[-50, -10, -5, 5, 10, 50].map((delta) => (
            <button key={delta} onClick={() => onNudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>Review status</h3>
        <div className="status-grid">
          {statuses.map((status) => (
            <button key={status.key} className={`${unit.unit_status === status.key ? "active" : ""} tone-${status.tone}`} onClick={() => onStatus(status.key)}>
              {status.label}
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>Notes</h3>
        <textarea placeholder="Optional review note..." maxLength={500} />
        <span className="char-count">0 / 500</span>
      </section>
    </div>
  );
}

function RawExportPreviewPanel({ units }: { units: ReviewUnit[] }) {
  const preview = buildRawExportPreview(units);
  return (
    <div className="export-panel r0-export-panel">
      <div className="section-title-row">
        <h2>Export preview</h2>
        <span>preview only | synthetic demo | no sample assets</span>
      </div>
      <div className="export-preview-grid">
        <PreviewTable
          title="reviewed_slate_anchor_manifest.csv"
          note="one row per reviewed synthetic ReviewUnit"
          rows={preview.reviewedManifest}
          columns={["unit_id", "unit_status", "take_id", "slate_start", "guqin_start", "synthetic_demo", "review_only"]}
        />
        <PreviewTable
          title="raw_marker_review.csv"
          note="one row per marker instance"
          rows={preview.rawMarkerReview}
          columns={["unit_id", "marker_key", "marker_time", "unit_status", "boundary_type"]}
        />
        <PreviewTable
          title="split_plan_from_raw_markers.csv"
          note="excluded units omitted | not executable from R0B"
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

function formatTime(time: number) {
  const minutes = Math.floor(time / 60);
  const seconds = time - minutes * 60;
  return `${String(minutes).padStart(2, "0")}:${seconds.toFixed(3).padStart(6, "0")}`;
}
