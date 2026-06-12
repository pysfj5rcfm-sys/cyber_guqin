import type { MarkerReviewStatus, R1SegmentStatus, ReviewStatus, ReviewUnitStatus } from "../types/cgVarw";

export const markerReviewStatusLabels: Record<MarkerReviewStatus, string> = {
  candidate: "待确认",
  accepted: "已确认",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已排除",
};

export const markerReviewStatusTone: Record<MarkerReviewStatus, string> = {
  candidate: "not_started",
  accepted: "confirmed",
  unclear: "needs_review",
  needs_retake: "needs_retake",
  rejected: "excluded",
};

export const reviewStatusLabels: Record<ReviewStatus, string> = {
  not_started: "待确认",
  in_progress: "审校中",
  accepted: "已确认",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已排除",
};

export const unitReviewStatusLabels: Record<ReviewStatus, string> = reviewStatusLabels;

export const unitStatusLabels: Record<ReviewUnitStatus, string> = {
  candidate: "待确认",
  confirmed: "已确认",
  needs_review: "待复核",
  not_started: "待确认",
  needs_retake: "需重录",
  excluded: "已排除",
  rejected: "已排除",
};

export const segmentStatusLabels: Record<R1SegmentStatus, string> = {
  candidate: "待确认",
  render_usable: "渲染可用",
  reference_only: "仅供参考",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已拒绝",
  excluded: "排除单元",
};

export function formatClockTime(time: number, fallback = "00:00.000") {
  if (!Number.isFinite(time) || time < 0) return fallback;
  const minutes = Math.floor(time / 60);
  const seconds = time - minutes * 60;
  return `${String(minutes).padStart(2, "0")}:${seconds.toFixed(3).padStart(6, "0")}`;
}

export function formatAxisTime(time: number, duration: number) {
  if (!Number.isFinite(time) || time < 0) return "";
  if (Number.isFinite(duration) && duration > 0 && duration < 10) {
    return `${time.toFixed(1)}s`;
  }
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time - minutes * 60);
  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

export interface ReviewHeaderRows {
  title: string;
  identity: string;
  status: string;
  duration: string;
}

export function buildR0HeaderRows({
  sourceAudio,
  unit,
  marker,
  metadata,
  duration,
}: {
  sourceAudio: string;
  unit?: {
    id: string;
    sequence: number;
    takeId: string;
    sourceLabel: string;
    unitStatusLabel: string;
    reviewStatusLabel: string;
    completionLabel: string;
  };
  marker?: { label: string; key: string; time: number };
  metadata?: {
    sample_rate: number | null;
    bit_depth: number | null;
    channels: number | null;
  } | null;
  duration: number;
}): ReviewHeaderRows {
  if (unit) {
    return {
      title: `R0 Raw 审校：${sourceAudio}`,
      identity: `当前单元：${unit.id} / ${unit.sequence} / ${unit.takeId}`,
      status: `来源：${unit.sourceLabel}｜单元状态：${unit.unitStatusLabel}｜审核状态：${unit.reviewStatusLabel}｜${unit.completionLabel}`,
      duration: `时长：${formatClockTime(duration)}`,
    };
  }

  return {
    title: `R0 Raw 审校：${sourceAudio}`,
    identity: `当前文件：${formatAudioMetadata(metadata)}`,
    status: marker ? `当前标记：${marker.label} ${marker.key}｜${formatSeconds(marker.time)}` : "当前标记：未选择",
    duration: `时长：${formatClockTime(duration)}`,
  };
}

export function buildR1HeaderRows({
  batchId,
  fileName,
  eventId,
  segmentId,
  variant,
  reviewStatusLabel,
  segmentStatusLabel,
  coreAccepted,
  markerAccepted,
  duration,
}: {
  batchId: string;
  fileName: string;
  eventId?: string;
  segmentId: string;
  variant: string;
  reviewStatusLabel: string;
  segmentStatusLabel: string;
  coreAccepted: number;
  markerAccepted: number;
  duration: number;
}): ReviewHeaderRows {
  return {
    title: `R1 Split 审校：${batchId} / ${fileName}`,
    identity: `事件：${eventId ?? "未标注"}｜Segment ID：${segmentId}｜版本：${variant}`,
    status: `Segment 状态：${reviewStatusLabel}｜${segmentStatusLabel}｜核心${coreAccepted}/2 · 标记${markerAccepted}/4`,
    duration: `时长：${formatClockTime(duration)}`,
  };
}

function formatAudioMetadata(metadata: { sample_rate: number | null; bit_depth: number | null; channels: number | null } | null | undefined) {
  if (!metadata) return "未知采样信息";
  const sampleRate = metadata.sample_rate ? `${(metadata.sample_rate / 1000).toFixed(metadata.sample_rate % 1000 === 0 ? 0 : 1)}kHz` : "未知采样率";
  const bitDepth = metadata.bit_depth ? `${metadata.bit_depth}bit` : "未知位深";
  const channels = metadata.channels ? `${metadata.channels}ch` : "未知声道";
  return `${sampleRate} · ${bitDepth} · ${channels} · WAV`;
}

function formatSeconds(time: number) {
  return Number.isFinite(time) && time >= 0 ? `${time.toFixed(3)}s` : "未知时间";
}
