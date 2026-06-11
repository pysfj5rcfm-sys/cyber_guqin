import { useEffect, useMemo, useState } from "react";
import type { Marker } from "../types/cgVarw";
import { MarkerLayer } from "./MarkerLayer";

interface WavInfo {
  duration: number;
  sampleRate: number;
  channels: number;
  bitDepth: number;
  peaks: number[];
}

const nonWavWarning = "Waveform fallback: non-WAV audio needs ffmpeg or another decoder for local waveform extraction.";

export function AudioCanvas({
  markers,
  duration,
  compact = false,
  selectedKey,
  onSelect,
  audioUrl,
  audioFileName,
}: {
  markers: Marker[];
  duration: number;
  compact?: boolean;
  selectedKey?: string;
  onSelect?: (key: string) => void;
  audioUrl?: string;
  audioFileName?: string;
}) {
  const barCount = compact ? 80 : 160;
  const [wavInfo, setWavInfo] = useState<WavInfo | null>(null);
  const [warning, setWarning] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setWavInfo(null);
    setWarning(null);

    if (!audioUrl) return;
    if (!audioUrl.toLowerCase().split("?")[0].endsWith(".wav")) {
      setWarning(nonWavWarning);
      return;
    }

    fetch(audioUrl)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.arrayBuffer();
      })
      .then((buffer) => parseWav(buffer, barCount))
      .then((info) => {
        if (!cancelled) setWavInfo(info);
      })
      .catch((error: unknown) => {
        if (!cancelled) setWarning(`WAV metadata fallback failed: ${error instanceof Error ? error.message : String(error)}`);
      });

    return () => {
      cancelled = true;
    };
  }, [audioUrl, barCount]);

  const fallbackBars = useMemo(
    () =>
      Array.from({ length: barCount }, (_, index) => {
        const wave = Math.sin(index * 0.31) * 0.35 + Math.sin(index * 0.09) * 0.45;
        const noise = ((index * 17) % 11) / 22;
        return Math.max(8, Math.round((Math.abs(wave) + noise) * (compact ? 34 : 74)));
      }),
    [barCount, compact],
  );

  const bars = wavInfo ? peaksToBars(wavInfo.peaks, compact) : fallbackBars;
  const ticks = useMemo(() => makeTicks(duration), [duration]);

  return (
    <div className={`audio-canvas ${compact ? "audio-compact" : ""}`}>
      <div className="axis-label top">waveform</div>
      <div className="waveform" data-source={wavInfo ? "wav-native" : "fallback"}>
        {bars.map((height, index) => <span key={index} style={{ height }} />)}
      </div>
      <div className="spectrogram">
        {bars.slice(0, 90).map((height, i) => <span key={i} style={{ opacity: 0.22 + Math.min(0.58, height / (compact ? 80 : 150)) }} />)}
      </div>
      <MarkerLayer markers={markers} duration={duration} selectedKey={selectedKey} onSelect={onSelect} />
      <div className="audio-meta">
        {wavInfo
          ? `${audioFileName ?? "WAV"} | ${wavInfo.duration.toFixed(3)}s | ${wavInfo.sampleRate} Hz | ${wavInfo.channels} ch | ${wavInfo.bitDepth} bit | ffmpeg not required`
          : warning ?? `${audioFileName ?? "audio"} | synthetic display waveform`}
      </div>
      <div className="time-axis">
        {ticks.map((tick) => <span key={tick}>{formatTime(tick)}</span>)}
      </div>
    </div>
  );
}

function parseWav(buffer: ArrayBuffer, peakCount: number): WavInfo {
  const view = new DataView(buffer);
  if (readAscii(view, 0, 4) !== "RIFF" || readAscii(view, 8, 4) !== "WAVE") {
    throw new Error("not a RIFF/WAVE file");
  }

  let offset = 12;
  let channels = 0;
  let sampleRate = 0;
  let bitDepth = 0;
  let audioFormat = 0;
  let dataOffset = -1;
  let dataSize = 0;

  while (offset + 8 <= view.byteLength) {
    const chunkId = readAscii(view, offset, 4);
    const chunkSize = view.getUint32(offset + 4, true);
    const chunkData = offset + 8;
    if (chunkId === "fmt ") {
      audioFormat = view.getUint16(chunkData, true);
      channels = view.getUint16(chunkData + 2, true);
      sampleRate = view.getUint32(chunkData + 4, true);
      bitDepth = view.getUint16(chunkData + 14, true);
    } else if (chunkId === "data") {
      dataOffset = chunkData;
      dataSize = chunkSize;
    }
    offset = chunkData + chunkSize + (chunkSize % 2);
  }

  if (!channels || !sampleRate || !bitDepth || dataOffset < 0 || dataSize <= 0) {
    throw new Error("missing WAV fmt/data chunk");
  }
  if (audioFormat !== 1 && audioFormat !== 3) {
    throw new Error(`unsupported WAV format ${audioFormat}`);
  }

  const bytesPerSample = bitDepth / 8;
  const frameCount = Math.floor(dataSize / (bytesPerSample * channels));
  const bucketSize = Math.max(1, Math.floor(frameCount / peakCount));
  const peaks: number[] = [];

  for (let bucket = 0; bucket < peakCount; bucket += 1) {
    const startFrame = bucket * bucketSize;
    const endFrame = bucket === peakCount - 1 ? frameCount : Math.min(frameCount, startFrame + bucketSize);
    let peak = 0;
    for (let frame = startFrame; frame < endFrame; frame += 1) {
      for (let channel = 0; channel < channels; channel += 1) {
        const sampleOffset = dataOffset + (frame * channels + channel) * bytesPerSample;
        peak = Math.max(peak, Math.abs(readSample(view, sampleOffset, bitDepth, audioFormat)));
      }
    }
    peaks.push(peak);
  }

  return {
    duration: frameCount / sampleRate,
    sampleRate,
    channels,
    bitDepth,
    peaks,
  };
}

function readSample(view: DataView, offset: number, bitDepth: number, audioFormat: number) {
  if (audioFormat === 3 && bitDepth === 32) return view.getFloat32(offset, true);
  if (bitDepth === 8) return (view.getUint8(offset) - 128) / 128;
  if (bitDepth === 16) return view.getInt16(offset, true) / 32768;
  if (bitDepth === 24) {
    const value = view.getUint8(offset) | (view.getUint8(offset + 1) << 8) | (view.getUint8(offset + 2) << 16);
    return ((value & 0x800000) ? value | 0xff000000 : value) / 8388608;
  }
  if (bitDepth === 32) return view.getInt32(offset, true) / 2147483648;
  throw new Error(`unsupported WAV bit depth ${bitDepth}`);
}

function readAscii(view: DataView, offset: number, length: number) {
  return Array.from({ length }, (_, index) => String.fromCharCode(view.getUint8(offset + index))).join("");
}

function peaksToBars(peaks: number[], compact: boolean) {
  const maxHeight = compact ? 42 : 86;
  return peaks.map((peak) => Math.max(6, Math.round(peak * maxHeight)));
}

function makeTicks(duration: number) {
  const count = 6;
  return Array.from({ length: count }, (_, index) => (duration / (count - 1)) * index);
}

function formatTime(time: number) {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time - minutes * 60);
  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}
