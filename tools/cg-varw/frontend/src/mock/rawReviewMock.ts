import syntheticAsr from "../../../sample_workspace/raw_audio/demo_batch01_synthetic.asr_candidates.json";
import type { Marker, MarkerReviewStatus, MockFlags, R0MarkerKey, ReviewStatus, ReviewUnit, ReviewUnitStatus } from "../types/cgVarw";

type SyntheticCandidate = {
  unit_id: string;
  sequence: number;
  status: ReviewUnitStatus;
  take_id: string;
  markers: Record<R0MarkerKey, number>;
  boundary: {
    type: "next_slate_start" | "file_end";
  };
};

export const demoAudioUrl = "/sample_workspace/raw_audio/demo_batch01_synthetic.wav";
export const demoAudioFileName = syntheticAsr.audio_file;
export const demoRawDuration = syntheticAsr.duration_seconds;

export const requiredMarkerKeys: R0MarkerKey[] = ["slate_start", "slate_end", "next_slate_start"];
export const optionalMarkerKeys: R0MarkerKey[] = ["guqin_start", "tail_end"];

export const rawFlags: MockFlags = {
  synthetic_demo: true,
  review_only: true,
  production_grade: false,
  not_real_qinist_recording: true,
  not_sample_source: true,
  not_ml_training_data: true,
  training_value_class: ["review_only_fixture", "local_r0b_validation"],
};

export const rawFiles = [
  {
    name: `合成演示 / ${syntheticAsr.audio_file}`,
    meta: `${syntheticAsr.duration_seconds.toFixed(3)}s | ${syntheticAsr.sample_rate_hz / 1000}kHz | ${syntheticAsr.bit_depth}bit | WAV | review_only`,
    selected: true,
  },
];

export const markerLabels: Record<R0MarkerKey, string> = {
  slate_start: "口播起始",
  slate_end: "口播结束",
  guqin_start: "古琴起声",
  tail_end: "尾音结束",
  next_slate_start: "下一口播起始",
};

export const unitStatusLabels: Record<ReviewUnitStatus, string> = {
  candidate: "待确认",
  confirmed: "已确认",
  needs_review: "待复核",
  not_started: "待确认",
  needs_retake: "需重录",
  excluded: "已排除",
  rejected: "已排除",
};

export const unitReviewStatusLabels: Record<ReviewStatus, string> = {
  not_started: "待确认",
  in_progress: "审校中",
  accepted: "已确认",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已排除",
};

export const markerReviewStatusLabels: Record<MarkerReviewStatus, string> = {
  candidate: "待确认",
  accepted: "已确认",
  unclear: "待复核",
  needs_retake: "需重录",
  rejected: "已排除",
};

const markerColors: Record<R0MarkerKey, Marker<R0MarkerKey>["color"]> = {
  slate_start: "green",
  slate_end: "blue",
  guqin_start: "gold",
  tail_end: "purple",
  next_slate_start: "cyan",
};

const markerOrder: R0MarkerKey[] = ["slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"];

function unitMarkers(times: Record<R0MarkerKey, number>): Marker<R0MarkerKey>[] {
  return markerOrder.map((key) => ({
    key,
    label: markerLabels[key],
    time: times[key],
    color: markerColors[key],
    optional: optionalMarkerKeys.includes(key),
    source: "asr_candidate",
    review_status: "candidate",
    nudge_total_ms: 0,
    notes: "",
  }));
}

export const rawReviewUnits: ReviewUnit[] = (syntheticAsr.candidates as SyntheticCandidate[]).map((candidate) =>
  withDerivedUnitState({
    id: candidate.unit_id,
    sequence: candidate.sequence,
    unit_status: candidate.status === "excluded" ? "excluded" : "candidate",
    source: "asr_candidate",
    takeId: candidate.take_id,
    boundary_type: candidate.boundary.type,
    boundary_unlinked: false,
    markers: unitMarkers(candidate.markers),
  }),
);

export function markerStats(unit: ReviewUnit) {
  const accepted = (key: R0MarkerKey) => unit.markers.find((marker) => marker.key === key)?.review_status === "accepted";
  return {
    requiredAccepted: requiredMarkerKeys.filter(accepted).length,
    requiredTotal: requiredMarkerKeys.length,
    optionalAccepted: optionalMarkerKeys.filter(accepted).length,
    optionalTotal: optionalMarkerKeys.length,
  };
}

export function completionLabel(unit: ReviewUnit) {
  const stats = markerStats(unit);
  return `必填${stats.requiredAccepted}/${stats.requiredTotal} · 可选${stats.optionalAccepted}/${stats.optionalTotal}`;
}

export function deriveUnitReviewStatus(unit: ReviewUnit): ReviewStatus {
  if (unit.unit_status === "excluded" || unit.unit_status === "rejected") return "rejected";

  const requiredMarkers = requiredMarkerKeys
    .map((key) => unit.markers.find((marker) => marker.key === key))
    .filter(Boolean);
  const requiredAccepted = requiredMarkers.every((marker) => marker?.review_status === "accepted");
  if (requiredAccepted && requiredMarkers.length === requiredMarkerKeys.length) return "accepted";
  if (requiredMarkers.some((marker) => marker?.review_status === "needs_retake")) return "needs_retake";
  if (requiredMarkers.some((marker) => marker?.review_status === "unclear")) return "unclear";
  if (unit.markers.some((marker) => (marker.review_status && marker.review_status !== "candidate") || (marker.nudge_total_ms ?? 0) !== 0)) return "in_progress";
  return "not_started";
}

export function deriveUnitStatus(unit: ReviewUnit): ReviewUnitStatus {
  if (unit.unit_status === "excluded" || unit.unit_status === "rejected") return unit.unit_status;
  const reviewStatus = deriveUnitReviewStatus(unit);
  if (reviewStatus === "accepted") return "confirmed";
  if (reviewStatus === "needs_retake") return "needs_retake";
  if (reviewStatus === "not_started") return "candidate";
  return "needs_review";
}

export function withDerivedUnitState(unit: ReviewUnit): ReviewUnit {
  const review_status = deriveUnitReviewStatus(unit);
  return {
    ...unit,
    review_status,
    unit_status: deriveUnitStatus({ ...unit, review_status }),
  };
}

export function completedMarkerCount(unit: ReviewUnit) {
  return markerStats(unit).requiredAccepted;
}

export function buildRawExportPreview(units: ReviewUnit[]) {
  const normalized = units.map(withDerivedUnitState);
  const reviewedManifest = normalized
    .filter((unit) => unit.unit_status !== "excluded" && unit.unit_status !== "rejected")
    .map((unit) => {
      const times = markerTimes(unit);
      return {
        unit_id: unit.id,
        unit_status: unit.unit_status,
        review_status: unit.review_status ?? "not_started",
        take_id: unit.takeId,
        slate_start: times.slate_start ?? "",
        slate_end: times.slate_end ?? "",
        guqin_start: times.guqin_start ?? "",
        tail_end: times.tail_end ?? "",
        next_slate_start: times.next_slate_start ?? "",
      };
    });

  const rawMarkerReview = normalized.flatMap((unit) =>
    unit.markers.map((marker) => ({
      unit_id: unit.id,
      marker_key: marker.key,
      marker_label_zh: marker.label,
      marker_time: marker.time.toFixed(3),
      marker_status: marker.review_status ?? "candidate",
      nudge_total_ms: String(marker.nudge_total_ms ?? 0),
    })),
  );

  const splitPlan = normalized
    .filter((unit) => unit.unit_status !== "excluded" && requiredMarkerKeys.every((key) => unit.markers.find((marker) => marker.key === key)?.review_status === "accepted"))
    .map((unit) => {
      const times = markerTimes(unit);
      return {
        unit_id: unit.id,
        take_id: unit.takeId,
        planned_unit_start_s: times.slate_start ?? "",
        planned_unit_end_s: times.next_slate_start ?? "",
        planned_clean_start_s: times.guqin_start || times.slate_end || "",
        planned_clean_end_s: times.next_slate_start ?? "",
        not_executed: "true",
      };
    });

  return { reviewedManifest, rawMarkerReview, splitPlan };
}

function markerTimes(unit: ReviewUnit) {
  return Object.fromEntries(unit.markers.map((marker) => [marker.key, marker.time.toFixed(3)])) as Partial<Record<R0MarkerKey, string>>;
}
