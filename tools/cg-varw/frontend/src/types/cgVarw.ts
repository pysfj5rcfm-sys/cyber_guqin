export type ReviewMode = "R0" | "R1" | "R2";

export type ReviewStatus = "accepted" | "unclear" | "needs_retake" | "rejected";
export type ReviewUnitStatus = "confirmed" | "needs_review" | "not_started" | "needs_retake" | "excluded";
export type SegmentStatus = "reviewed" | "pending" | "needs_review" | "rejected";
export type RenderStatus = "render_usable" | "reference_only" | "unclear" | "needs_retake" | "rejected";
export type Severity = "low" | "medium" | "high";

export type R0MarkerKey = "slate_start" | "slate_end" | "guqin_start" | "tail_end" | "next_slate_start";
export type R1MarkerKey = "pre_idle_end" | "gesture_start" | "render_anchor" | "tail_end";
export type R2MarkerKey = "phrase_start" | "phrase_end" | "breath_point" | "cadence" | "section_start" | "unclear_boundary";

export interface MockFlags {
  review_only: true;
  production_grade: false;
  training_value_class: string[];
}

export interface Marker<Key extends string = string> {
  id?: string;
  unitId?: string;
  key: Key;
  label: string;
  time: number;
  color: "green" | "blue" | "gold" | "purple" | "cyan" | "red";
  optional?: boolean;
  weak?: boolean;
  displayLabel?: boolean;
}

export interface ReviewUnit {
  id: string;
  sequence: number;
  unit_status: ReviewUnitStatus;
  source: "asr_candidate" | "manual";
  takeId: string;
  boundary_unlinked?: boolean;
  markers: Marker<R0MarkerKey>[];
}

export interface ExportRow {
  file: string;
  description: string;
  rule: string;
  updatedAt: string;
  actor?: string;
}

export interface VersionRow {
  id: "A" | "B" | "C" | "D" | "E";
  key: string;
  name: string;
  englishName: string;
  eventRange: string;
  rating: number;
  selected?: boolean;
}
