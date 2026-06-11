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
        return (
          <button
            key={`${marker.key}-${marker.time}`}
            className={`marker marker-${marker.color} ${selectedKey === marker.key ? "is-selected" : ""}`}
            style={{ left }}
            onClick={() => onSelect?.(marker.key)}
            title={`${marker.label} ${marker.key}`}
          >
            <span className="marker-tag">{marker.label}<small>{marker.key}</small></span>
          </button>
        );
      })}
    </div>
  );
}
