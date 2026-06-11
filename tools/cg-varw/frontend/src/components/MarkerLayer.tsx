import type { Marker } from "../types/cgVarw";

export function MarkerLayer({
  markers,
  duration,
  selectedKey,
  onSelect,
}: {
  markers: Marker[];
  duration: number;
  selectedKey?: string;
  onSelect?: (key: string) => void;
}) {
  return (
    <div className="marker-layer">
      {markers.map((marker) => {
        const left = `${Math.min(98, Math.max(1, (marker.time / duration) * 100))}%`;
        const markerId = marker.id ?? marker.key;
        const showLabel = marker.displayLabel ?? !marker.weak;
        return (
          <button
            key={`${markerId}-${marker.time}`}
            className={`marker marker-${marker.color} ${selectedKey === markerId ? "is-selected" : ""} ${marker.weak ? "is-weak" : ""}`}
            style={{ left }}
            onClick={() => onSelect?.(markerId)}
            title={`${marker.unitId ? `${marker.unitId} · ` : ""}${marker.label} ${marker.key}`}
          >
            {showLabel && <span className="marker-tag">{marker.label}<small>{marker.key}</small></span>}
          </button>
        );
      })}
    </div>
  );
}
