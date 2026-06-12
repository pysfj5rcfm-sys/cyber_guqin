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
  const safeDuration = Number.isFinite(duration) && duration > 0 ? duration : 0;
  const sortedMarkerIds = markers
    .map((marker) => marker.id ?? marker.key)
    .sort((left, right) => {
      const leftMarker = markers.find((marker) => (marker.id ?? marker.key) === left);
      const rightMarker = markers.find((marker) => (marker.id ?? marker.key) === right);
      return (leftMarker?.time ?? 0) - (rightMarker?.time ?? 0);
    });

  return (
    <div className="marker-layer">
      {markers.map((marker) => {
        const markerId = marker.id ?? marker.key;
        if (!safeDuration || !Number.isFinite(marker.time)) return null;
        const left = `${Math.min(98, Math.max(1, (marker.time / safeDuration) * 100))}%`;
        const sortedIndex = sortedMarkerIds.indexOf(markerId);
        const previousMarkerId = sortedIndex > 0 ? sortedMarkerIds[sortedIndex - 1] : undefined;
        const previousMarker = markers.find((item) => (item.id ?? item.key) === previousMarkerId);
        const isCloseToPrevious = previousMarker ? Math.abs(marker.time - previousMarker.time) / safeDuration < 0.045 : false;
        // Exactly one marker label should be prominent: marker.id === selectedMarkerId.
        const isSelected = selectedKey === markerId;
        const lane = isSelected ? 0 : isCloseToPrevious ? (sortedIndex % 2) + 1 : 0;
        return (
          <button
            key={`${markerId}-${marker.time}`}
            className={`marker marker-${marker.color} marker-lane-${lane} ${isSelected ? "is-selected" : ""} ${marker.weak ? "is-weak" : ""}`}
            style={{ left }}
            onClick={() => onSelect?.(markerId)}
            title={`${marker.unitId ? `${marker.unitId} · ` : ""}${marker.label} ${marker.key}`}
          >
            <span className={`marker-tag ${isSelected ? "marker-label--selected" : "marker-label--compact"}`}>
              {isSelected ? marker.label : compactMarkerLabel(marker.label, marker.key)}
              {isSelected && <small>{marker.key}</small>}
            </span>
          </button>
        );
      })}
    </div>
  );
}

function compactMarkerLabel(label: string, key: string) {
  if (key === "next_slate_start") return "下一口播";
  if (key === "pre_idle_end") return "前置结束";
  return label;
}
