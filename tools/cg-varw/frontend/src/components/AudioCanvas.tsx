import type { Marker } from "../types/cgVarw";
import { MarkerLayer } from "./MarkerLayer";

export function AudioCanvas({
  markers,
  duration,
  compact = false,
  selectedKey,
  onSelect,
}: {
  markers: Marker[];
  duration: number;
  compact?: boolean;
  selectedKey?: string;
  onSelect?: (key: string) => void;
}) {
  const bars = Array.from({ length: compact ? 80 : 160 }, (_, index) => {
    const wave = Math.sin(index * 0.31) * 0.35 + Math.sin(index * 0.09) * 0.45;
    const noise = ((index * 17) % 11) / 22;
    return Math.max(8, Math.round((Math.abs(wave) + noise) * (compact ? 34 : 74)));
  });

  return (
    <div className={`audio-canvas ${compact ? "audio-compact" : ""}`}>
      <div className="axis-label top">波形</div>
      <div className="waveform">
        {bars.map((height, index) => <span key={index} style={{ height }} />)}
      </div>
      <div className="spectrogram">
        {Array.from({ length: 90 }, (_, i) => <span key={i} style={{ opacity: 0.35 + ((i * 7) % 10) / 16 }} />)}
      </div>
      <MarkerLayer markers={markers} duration={duration} selectedKey={selectedKey} onSelect={onSelect} />
      <div className="time-axis">
        <span>0:00</span><span>0:30</span><span>1:00</span><span>1:30</span><span>2:00</span><span>2:30</span>
      </div>
    </div>
  );
}
