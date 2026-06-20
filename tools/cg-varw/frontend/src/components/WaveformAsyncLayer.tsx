import { useEffect, useState } from "react";
import { AudioCanvas } from "./AudioCanvas";
import type { Marker } from "../types/cgVarw";

type WaveformState =
  | { status: "idle"; peaks: number[]; warning: string }
  | { status: "loading"; peaks: number[]; warning: string }
  | { status: "ready"; peaks: number[]; warning: string }
  | { status: "error"; peaks: number[]; warning: string };

interface WaveformPayload {
  peaks?: number[];
  waveform_supported?: boolean;
  warning?: string | null;
  fallback_reason?: string | null;
}

interface AudioMetadata {
  duration_s: number | null;
  sample_rate: number | null;
  bit_depth: number | null;
  channels: number | null;
  waveform_supported: boolean;
  warning?: string | null;
}

const waveformCache = new Map<string, WaveformState>();

export function WaveformAsyncLayer({
  audioId,
  waveformUrl,
  markers,
  duration,
  selectedKey,
  onSelect,
  audioFileName,
  metadata,
  compact = false,
}: {
  audioId: string;
  waveformUrl: string;
  markers: Marker[];
  duration: number;
  selectedKey?: string;
  onSelect?: (key: string) => void;
  audioFileName?: string;
  metadata?: AudioMetadata;
  compact?: boolean;
}) {
  const [state, setState] = useState<WaveformState>({ status: "idle", peaks: [], warning: "" });

  useEffect(() => {
    if (!audioId || !waveformUrl) {
      setState({ status: "idle", peaks: [], warning: "" });
      return;
    }

    const cacheKey = `${audioId}|${waveformUrl}`;
    const cached = waveformCache.get(cacheKey);
    if (cached) {
      setState(cached);
      return;
    }

    const controller = new AbortController();
    setState({ status: "loading", peaks: [], warning: "" });

    fetch(waveformUrl, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<WaveformPayload>;
      })
      .then((payload) => {
        if (controller.signal.aborted) return;
        const nextState: WaveformState = {
          status: "ready",
          peaks: payload.waveform_supported === false ? [] : payload.peaks ?? [],
          warning: payload.warning ?? payload.fallback_reason ?? "",
        };
        waveformCache.set(cacheKey, nextState);
        setState(nextState);
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        setState({ status: "error", peaks: [], warning: error instanceof Error ? error.message : String(error) });
      });

    return () => {
      controller.abort();
    };
  }, [audioId, waveformUrl]);

  return (
    <AudioCanvas
      markers={markers}
      duration={duration}
      compact={compact}
      selectedKey={selectedKey}
      onSelect={onSelect}
      audioFileName={audioFileName}
      metadata={metadata}
      waveformPeaks={state.peaks}
      waveformLoading={state.status === "loading"}
      waveformWarning={state.warning}
    />
  );
}
