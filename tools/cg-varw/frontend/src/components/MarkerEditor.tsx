import type { Marker } from "../types/cgVarw";

export function MarkerEditor({
  title = "标记编辑",
  markers,
  selectedKey,
  statusLabels,
  selectedStatus,
  onSelectMarker,
  onNudge,
  onStatus,
  extra,
}: {
  title?: string;
  markers: Marker[];
  selectedKey: string;
  statusLabels: { key: string; label: string; tone?: string }[];
  selectedStatus: string;
  onSelectMarker: (key: string) => void;
  onNudge: (delta: number) => void;
  onStatus: (key: string) => void;
  extra?: React.ReactNode;
}) {
  const selected = markers.find((marker) => marker.key === selectedKey) ?? markers[0];
  return (
    <div className="panel-stack">
      <h2>{title}</h2>
      <div className="info-card center">
        <span>当前选中标记</span>
        <strong>{selected.label}</strong>
        <b>{selected.time.toFixed(3)}s</b>
      </div>
      <section className="editor-section">
        <h3>标记跳转</h3>
        <div className="button-grid">
          {markers.map((marker) => (
            <button key={marker.key} className={selectedKey === marker.key ? "active" : ""} onClick={() => onSelectMarker(marker.key)}>
              {marker.label}<small>{marker.key}</small>
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>微调（相对当前标记）</h3>
        <div className="nudge-grid">
          {[-50, -10, -5, 5, 10, 50].map((delta) => (
            <button key={delta} onClick={() => onNudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>
          ))}
        </div>
      </section>
      {extra}
      <section className="editor-section">
        <h3>审核状态</h3>
        <div className="status-grid">
          {statusLabels.map((status) => (
            <button key={status.key} className={`${selectedStatus === status.key ? "active" : ""} tone-${status.tone ?? "cyan"}`} onClick={() => onStatus(status.key)}>
              {status.label}
            </button>
          ))}
        </div>
      </section>
      <section className="editor-section">
        <h3>备注</h3>
        <textarea placeholder="在此输入备注（可选）..." maxLength={500} />
        <span className="char-count">0 / 500</span>
      </section>
    </div>
  );
}
