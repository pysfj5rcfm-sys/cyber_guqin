import { useMemo } from "react";
import type { Marker } from "../types/cgVarw";
import { MarkerLayer } from "./MarkerLayer";
import { formatAxisTime } from "./reviewUi";

interface AudioMetadata {
  duration_s: number | null;
  sample_rate: number | null;
  bit_depth: number | null;
  channels: number | null;
  waveform_supported: boolean;
  warning?: string | null;
}

export function AudioCanvas({
  markers,
  duration,
  compact = false,
  selectedKey,
  onSelect,
  audioFileName,
  metadata,
  waveformPeaks,
  waveformLoading = false,
  waveformWarning = "",
}: {
  markers: Marker[];
  duration: number;
  compact?: boolean;
  selectedKey?: string;
  onSelect?: (key: string) => void;
  audioFileName?: string;
  metadata?: AudioMetadata;
  waveformPeaks?: number[];
  waveformLoading?: boolean;
  waveformWarning?: string;
}) {
  const barCount = compact ? 80 : 160;
  const fallbackBars = useMemo(
    () =>
      Array.from({ length: barCount }, (_, index) => {
        const wave = Math.sin(index * 0.31) * 0.35 + Math.sin(index * 0.09) * 0.45;
        const noise = ((index * 17) % 11) / 22;
        return Math.max(8, Math.round((Math.abs(wave) + noise) * (compact ? 34 : 74)));
      }),
    [barCount, compact],
  );

  const hasWaveform = Boolean(waveformPeaks?.length);
  const bars = hasWaveform ? peaksToBars(downsamplePeaks(waveformPeaks ?? [], barCount), compact) : fallbackBars;
  const ticks = useMemo(() => makeTicks(duration), [duration]);

  return (
    <div className={`audio-canvas ${compact ? "audio-compact" : ""}`}>
      <div className="axis-label top">波形</div>
      <div className={`waveform ${waveformLoading ? "is-loading" : ""}`} data-source={hasWaveform ? "backend-peaks" : "fallback"}>
        {bars.map((height, index) => <span key={index} style={{ height }} />)}
      </div>
      {waveformLoading && <div className="waveform-loading">正在加载波形...</div>}
      {hasWaveform && (
        <div className="spectrogram" aria-hidden="true">
          {bars.slice(0, 90).map((height, i) => <span key={i} style={{ opacity: 0.22 + Math.min(0.58, height / (compact ? 80 : 150)) }} />)}
        </div>
      )}
      {!waveformLoading && <MarkerLayer markers={markers} duration={duration} selectedKey={selectedKey} onSelect={onSelect} />}
      <div className="audio-meta">
        {waveformLoading
          ? `${audioFileName ?? "音频"} | 波形异步加载中，播放不等待波形`
          : hasWaveform
          ? `${audioFileName ?? "WAV"} | ${formatDurationMeta(duration)} | 后端 WAV 波形无需 ffmpeg`
          : metadata
            ? `${audioFileName ?? "WAV"} | ${metadata.duration_s?.toFixed(3) ?? "未知"}s | ${metadata.sample_rate ?? "未知"} Hz | ${metadata.channels ?? "未知"} ch | ${metadata.bit_depth ?? "未知"} bit`
            : waveformWarning || `${audioFileName ?? "音频"} | 等待波形数据`}
      </div>
      <div className="time-axis">
        {ticks.map((tick) => <span key={tick}>{formatAxisTime(tick, duration)}</span>)}
      </div>
    </div>
  );
}

function peaksToBars(peaks: number[], compact: boolean) {
  const maxHeight = compact ? 42 : 86;
  return peaks.map((peak) => Math.max(6, Math.round(peak * maxHeight)));
}

function downsamplePeaks(peaks: number[], count: number) {
  if (peaks.length <= count) return peaks;
  const bucket = peaks.length / count;
  return Array.from({ length: count }, (_, index) => {
    const start = Math.floor(index * bucket);
    const end = Math.max(start + 1, Math.floor((index + 1) * bucket));
    return Math.max(...peaks.slice(start, end));
  });
}

function makeTicks(duration: number) {
  if (!Number.isFinite(duration) || duration <= 0) return [];
  const count = 6;
  const step = duration / (count - 1);
  if (!Number.isFinite(step) || step <= 0) return [];
  return Array.from({ length: count }, (_, index) => step * index).filter((tick) => Number.isFinite(tick));
}

function formatDurationMeta(duration: number) {
  return Number.isFinite(duration) && duration >= 0 ? `${duration.toFixed(3)}s` : "未知时长";
}
