import type { ExportRow, Marker, MockFlags, R1MarkerKey } from "../types/cgVarw";

export const splitFlags: MockFlags = {
  review_only: true,
  production_grade: false,
  training_value_class: ["qinist_low_level_profile", "sample_alignment_profile"],
};

export const splitSegments = [
  { name: "T001_clean.wav", duration: "02:41.123", time: "2025-05-06 14:20", status: "已审" },
  { name: "T002_clean.wav", duration: "02:37.880", time: "2025-05-06 14:22", status: "待审" },
  { name: "T003_clean.wav", duration: "02:45.093", time: "2025-05-06 14:25", status: "待审", selected: true },
  { name: "T004_clean.wav", duration: "02:33.455", time: "2025-05-06 14:27", status: "需复核" },
];

export const splitMarkers: Marker<R1MarkerKey>[] = [
  { key: "pre_idle_end", label: "前置空白结束", time: 0.24, color: "green" },
  { key: "gesture_start", label: "动作起声", time: 0.82, color: "blue" },
  { key: "render_anchor", label: "渲染锚点", time: 1.58, color: "gold" },
  { key: "tail_end", label: "尾音结束", time: 2.55, color: "purple" },
];

export const splitExports: ExportRow[] = [
  { file: "reviewed_render_anchors.csv", description: "已审核的 render_anchor 清单（按批次 / 事件 / 文件）", rule: "仅包含四个分割级标记与 Anchor type、审核状态等", updatedAt: "2025-05-06 14:25:31" },
  { file: "split_marker_review.csv", description: "分割级标记审核记录（四标记明细）", rule: "每个文件一行：pre_idle_end / gesture_start / render_anchor / tail_end", updatedAt: "2025-05-06 14:25:31" },
  { file: "segment_qc_sheet.csv", description: "分段 QC 汇总表", rule: "审核状态、Anchor type、策略、时长、备注汇总", updatedAt: "2025-05-06 14:25:31" },
];
