import type { ExportRow, Marker, MockFlags, R0MarkerKey } from "../types/cgVarw";

export const rawFlags: MockFlags = {
  review_only: true,
  production_grade: false,
  training_value_class: ["provenance_only", "split_tool_calibration"],
};

export const rawFiles = [
  { name: "RS_XWC_002_BAIYA_PILOT / batch01_raw.wav", meta: "2025-05-06 14:32:18 · 44.1kHz · 24bit · WAV", selected: true },
  { name: "RS_XWC_002_BAIYA_PILOT / batch02_raw.wav", meta: "2025-05-06 16:05:44 · 44.1kHz · 24bit · WAV" },
  { name: "RS_XWC_001_MVP_PILOT / sanman_batch01.m4a", meta: "2025-05-04 10:21:33 · 48kHz · 24bit · M4A" },
  { name: "RS_XWC_001_MVP_PILOT / sanman_batch02.m4a", meta: "2025-05-04 11:02:18 · 48kHz · 24bit · M4A" },
];

export const rawMarkers: Marker<R0MarkerKey>[] = [
  { key: "slate_start", label: "口播起始", time: 14.2, color: "green" },
  { key: "slate_end", label: "口播结束", time: 35.8, color: "blue" },
  { key: "guqin_start", label: "古琴起声（可选）", time: 62.487, color: "gold", optional: true },
  { key: "tail_end", label: "尾音结束（可选）", time: 114.6, color: "purple", optional: true },
  { key: "next_slate_start", label: "下一口播起始", time: 140.2, color: "cyan" },
];

export const rawExports: ExportRow[] = [
  { file: "reviewed_slate_anchor_manifest.csv", description: "整合后的口播与演奏锚点清单（人工复核后）", rule: "基于本页标记生成，只显示 mock 结果", updatedAt: "2025-05-06 14:55:21" },
  { file: "split_plan_from_raw_markers.csv", description: "基于 Raw 标记生成的分段切分计划", rule: "依据标记区间自动生成", updatedAt: "2025-05-06 14:55:21" },
  { file: "raw_marker_review.csv", description: "Raw 标记复核记录（含偏移与状态）", rule: "记录每个标记的时间、微调偏移、审核状态与备注", updatedAt: "2025-05-06 14:55:21" },
];
