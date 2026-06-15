export type ReviewMode = "R0" | "R1" | "R2";

export type MarkerReviewStatus = "candidate" | "accepted" | "unclear" | "needs_retake" | "rejected";
export type ReviewStatus = "candidate" | "not_started" | "in_progress" | "accepted" | "unclear" | "needs_retake" | "rejected";
export type ReviewUnitStatus = "candidate" | "confirmed" | "needs_review" | "not_started" | "needs_retake" | "excluded" | "rejected";
export type SegmentStatus = "reviewed" | "pending" | "needs_review" | "rejected";
export type RenderStatus = "render_usable" | "reference_only" | "unclear" | "needs_retake" | "rejected";
export type Severity = "low" | "medium" | "high";

export type R0MarkerKey = "slate_start" | "slate_end" | "guqin_start" | "tail_end" | "next_slate_start";
export type R1MarkerKey = "pre_idle_end" | "gesture_start" | "render_anchor" | "tail_end";
export type R2MarkerKey = "phrase_start" | "phrase_end" | "breath_point" | "cadence" | "section_start" | "section_end" | "unclear_boundary";
export type R1AnchorType = "main_attack" | "gesture_start" | "context_first_attach";
export type R1PreAttackMusicPolicy = "keep_silence" | "preserve";
export type R1TailPolicy = "smart_fade_100ms" | "full_tail";
export type R1SegmentStatus = "candidate" | "render_usable" | "reference_only" | "unclear" | "needs_retake" | "rejected" | "excluded";

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

export interface R1Marker {
  marker_id: string;
  segment_id: string;
  marker_type: R1MarkerKey;
  marker_label_zh: string;
  time_s: number;
  source: "synthetic_candidate" | "human_adjusted" | "manual" | "derived_from_fixture";
  confidence?: number | null;
  review_status: MarkerReviewStatus;
  nudge_total_ms?: number;
  notes?: string;
}

export type R1MarkerSet = Partial<Record<R1MarkerKey, R1Marker>>;

export interface R1SegmentQC {
  render_usable: boolean;
  reference_only: boolean;
  unclear: boolean;
  needs_retake: boolean;
  rejected: boolean;
  reject_reason?: string;
  noise_issue?: boolean;
  click_issue?: boolean;
  tail_clipped?: boolean;
  attack_clipped?: boolean;
  slate_residue?: boolean;
  wrong_take?: boolean;
}

export interface SplitBatch {
  batch_id: string;
  display_name: string;
  segment_count: number;
  source: "synthetic_demo" | "real_split_root";
  review_only: true;
  production_grade: false;
}

export interface SplitSegment {
  segment_id: string;
  batch_id: string;
  take_id: string;
  file_name: string;
  relative_path: string;
  recording_session_id?: string;
  recording_id?: string;
  piece_id?: string;
  qinist_id?: string;
  recording_take_no?: string;
  batch_take_no?: string;
  script_id?: string;
  source_raw_audio?: string;
  source_split_audio?: string;
  event_id?: string;
  event_range?: string;
  gesture_id?: string;
  realization_variant?: "clean" | "context" | "retake" | "demo" | null;
  variant: "clean" | "context" | "retake" | "demo";
  duration_s: number;
  sample_rate?: number | null;
  bit_depth?: number | null;
  channels?: number | null;
  markers: R1MarkerSet;
  anchor_type: R1AnchorType;
  pre_attack_music_policy: R1PreAttackMusicPolicy;
  tail_policy: R1TailPolicy;
  segment_status: R1SegmentStatus;
  review_status: ReviewStatus;
  qc: R1SegmentQC;
  human_accepted?: boolean | null;
  reviewed_by?: string;
  reviewed_at?: string;
  notes?: string;
  synthetic_demo?: boolean;
  review_only: true;
  production_grade: false;
  not_sample_assets: true;
  not_render_executed: true;
  not_ml_training_data?: true;
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
  recording_session_id?: string;
  recording_id?: string;
  piece_id?: string;
  qinist_id?: string;
  batch_id?: string;
  recording_take_no?: string;
  batch_take_no?: string;
  script_id?: string;
  source_raw_audio?: string;
  event_id?: string;
  event_range?: string;
  gesture_id?: string;
  expected_sample_type?: string;
  markers: Marker<R0MarkerKey>[];
}

export interface ExportRow {
  file: string;
  group?: string;
  description: string;
  rule: string;
  scope?: string;
  updatedAt: string;
  actor?: string;
}

export interface VersionRow {
  id: "A" | "B" | "C" | "D" | "E";
  key: string;
  name: string;
  englishName: string;
  eventRange: string;
  phraseRange?: string;
  rating: number;
  selected?: boolean;
}

export type R2VersionCode = "A" | "B" | "C" | "D" | "E";
export type R2VersionRole =
  | "literal_dapu"
  | "phrase_dapu"
  | "qinist_style_dapu"
  | "teaching_diagnostic_dapu"
  | "reviewed_dapu";
export type R2BoundarySource = "human_marked" | "imported" | "derived" | "mock";
export type R2BoundaryConfidence = "high" | "medium" | "low" | "unclear";
export type R2IssueType =
  | "too_fast"
  | "too_slow"
  | "tail_short"
  | "wrong_breath"
  | "too_mechanical"
  | "attack_abrupt"
  | "sample_mismatch"
  | "phrase_unclear"
  | "good"
  | "other";

export interface R2SafetyFlags {
  review_only: true;
  production_grade: false;
  not_render_executed: true;
  not_sample_assets: true;
  not_ml_training_data: true;
}

export interface R2Piece {
  piece_id: string;
  piece_title: string;
  active_mvp: boolean;
  mock_only: boolean;
}

export interface R2Session {
  recording_session_id: string;
  label: string;
  current_project_session: boolean;
  mock_only: boolean;
}

export interface RenderSet extends R2SafetyFlags {
  render_set_id: string;
  project_id: string;
  recording_session_id: string;
  piece_id: string;
  piece_title: string;
  qinist_id: string;
  render_stage: "mock";
  created_at: string;
}

export interface Section {
  section_id: string;
  section_label: string;
  event_range: string;
  phrase_ids: string[];
}

export interface PhraseDefinition {
  phrase_id: string;
  section_id: string;
  phrase_index: number;
  phrase_label: string;
  event_range: string;
  start_event_id: string;
  end_event_id: string;
}

export interface RenderVersion extends R2SafetyFlags {
  render_set_id: string;
  version_id: string;
  version_code: R2VersionCode;
  version_label_zh: string;
  version_label_en: string;
  version_role: R2VersionRole;
  audio_path: string;
  duration_s: number;
  waveform_preview?: number[];
  mock_render: true;
}

export interface RenderPhraseAlignment {
  render_set_id: string;
  version_id: string;
  phrase_id: string;
  section_id: string;
  event_range: string;
  start_s: number;
  end_s: number;
  breath_points_s: number[];
  cadence_point_s?: number;
  boundary_source: R2BoundarySource;
  boundary_confidence: R2BoundaryConfidence;
  review_status: MarkerReviewStatus;
  reviewer?: string;
  reviewed_at?: string;
  notes?: string;
}

export interface PhraseMarker {
  marker_id: string;
  render_set_id: string;
  version_id: string;
  phrase_id: string;
  marker_type: R2MarkerKey;
  marker_label_zh: string;
  time_s: number;
  source: R2BoundarySource;
  review_status: MarkerReviewStatus;
  nudge_total_ms: number;
  notes?: string;
}

export interface ListeningReview extends R2SafetyFlags {
  review_id: string;
  render_set_id: string;
  comparison_scope: "phrase";
  phrase_id: string;
  section_id: string;
  event_range: string;
  active_version_id: string;
  preferred_version_id?: string;
  issue_type: R2IssueType[];
  severity: Severity;
  comment: string;
  suggested_revision?: string;
  reviewer: string;
  reviewed_at: string;
  training_usable: boolean;
}

export interface RenderRevisionLog extends R2SafetyFlags {
  revision_id: string;
  render_set_id: string;
  from_version_id: string;
  to_version_id?: string;
  phrase_id: string;
  section_id: string;
  event_range: string;
  change_type: "timing" | "breath" | "tail" | "sample_selection" | "phrase_boundary" | "render_anchor" | "other";
  reason: string;
  based_on_review_id: string;
  accepted?: boolean;
}

export interface R2DraftPayload extends R2SafetyFlags {
  render_set_id: string;
  selected_phrase_id: string;
  selected_version_id: string;
  preferred_version_id?: string;
  phrase_markers: PhraseMarker[];
  phrase_alignments: RenderPhraseAlignment[];
  listening_review: ListeningReview;
  saved_at: string;
}
