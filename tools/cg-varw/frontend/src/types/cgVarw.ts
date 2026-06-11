export type ReviewMode = "R0" | "R1" | "R2";

export type MarkerReviewStatus = "candidate" | "accepted" | "unclear" | "needs_retake" | "rejected";
export type ReviewStatus = "not_started" | "in_progress" | "accepted" | "unclear" | "needs_retake" | "rejected";
export type ReviewUnitStatus = "candidate" | "confirmed" | "needs_review" | "not_started" | "needs_retake" | "excluded" | "rejected";
export type SegmentStatus = "reviewed" | "pending" | "needs_review" | "rejected";
export type RenderStatus = "render_usable" | "reference_only" | "unclear" | "needs_retake" | "rejected";
export type Severity = "low" | "medium" | "high";

export type R0MarkerKey = "slate_start" | "slate_end" | "guqin_start" | "tail_end" | "next_slate_start";
export type R1MarkerKey = "pre_idle_end" | "gesture_start" | "render_anchor" | "tail_end";
export type R2MarkerKey = "phrase_start" | "phrase_end" | "breath_point" | "cadence" | "section_start" | "unclear_boundary";

export interface MockFlags {
  synthetic_demo?: true;
  review_only: true;
  production_grade: false;
  not_real_qinist_recording?: true;
  not_sample_source?: true;
  not_ml_training_data?: true;
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
  source?: string;
  confidence?: number | null;
  review_status?: MarkerReviewStatus;
  nudge_total_ms?: number;
  notes?: string;
}

export interface ReviewUnit {
  id: string;
  sequence: number;
  unit_status: ReviewUnitStatus;
  review_status?: ReviewStatus;
  source: "asr_candidate" | "manual";
  takeId: string;
  boundary_type?: "next_slate_start" | "file_end";
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
