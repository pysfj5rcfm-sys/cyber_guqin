import syntheticAsr from "../../../sample_workspace/raw_audio/demo_batch01_synthetic.asr_candidates.json";
import type { Marker, MockFlags, R0MarkerKey, ReviewUnit, ReviewUnitStatus } from "../types/cgVarw";

type SyntheticCandidate = {
  unit_id: string;
  sequence: number;
  source: string;
  status: ReviewUnitStatus;
  take_id: string;
  markers: Record<R0MarkerKey, number>;
  boundary: {
    type: "next_slate_start" | "file_end";
    time: number;
    target_unit_id: string | null;
  };
};

export const demoAudioUrl = "/sample_workspace/raw_audio/demo_batch01_synthetic.wav";
export const demoAudioFileName = syntheticAsr.audio_file;
export const demoRawDuration = syntheticAsr.duration_seconds;

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
    name: `synthetic_demo / ${syntheticAsr.audio_file}`,
    meta: `${syntheticAsr.duration_seconds.toFixed(3)}s | ${syntheticAsr.sample_rate_hz / 1000}kHz | ${syntheticAsr.bit_depth}bit | WAV | review_only`,
    selected: true,
  },
];

export const markerLabels: Record<R0MarkerKey, string> = {
  slate_start: "slate start",
  slate_end: "slate end",
  guqin_start: "synthetic pluck start",
  tail_end: "tail decay end",
  next_slate_start: "next slate / file end",
};

export const unitStatusLabels: Record<ReviewUnitStatus, string> = {
  confirmed: "confirmed",
  needs_review: "needs review",
  not_started: "not started",
  needs_retake: "needs retake",
  excluded: "excluded",
};

const markerColors: Record<R0MarkerKey, Marker<R0MarkerKey>["color"]> = {
  slate_start: "green",
  slate_end: "blue",
  guqin_start: "gold",
  tail_end: "purple",
  next_slate_start: "cyan",
};

const markerOrder: R0MarkerKey[] = ["slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"];

function unitMarkers(times: Record<R0MarkerKey, number>, boundaryType: SyntheticCandidate["boundary"]["type"]): Marker<R0MarkerKey>[] {
  return markerOrder.map((key) => ({
    key,
    label: boundaryType === "file_end" && key === "next_slate_start" ? "file end" : markerLabels[key],
    time: times[key],
    color: markerColors[key],
    optional: key === "guqin_start" || key === "tail_end",
  }));
}

export const rawReviewUnits: ReviewUnit[] = (syntheticAsr.candidates as SyntheticCandidate[]).map((candidate) => ({
  id: candidate.unit_id,
  sequence: candidate.sequence,
  unit_status: candidate.status,
  source: "asr_candidate",
  takeId: candidate.take_id,
  boundary_type: candidate.boundary.type,
  markers: unitMarkers(candidate.markers, candidate.boundary.type),
}));

export function completedMarkerCount(unit: ReviewUnit) {
  if (unit.unit_status === "not_started") return 0;
  if (unit.unit_status === "needs_review") return 4;
  return 5;
}

export function buildRawExportPreview(units: ReviewUnit[]) {
  const reviewedManifest = units
    .filter((unit) => unit.unit_status === "confirmed" || unit.unit_status === "needs_retake" || unit.unit_status === "needs_review")
    .map((unit) => ({
      unit_id: unit.id,
      unit_status: unit.unit_status,
      take_id: unit.takeId,
      slate_start: unit.markers.find((marker) => marker.key === "slate_start")?.time.toFixed(3) ?? "",
      guqin_start: unit.markers.find((marker) => marker.key === "guqin_start")?.time.toFixed(3) ?? "",
      synthetic_demo: "true",
      review_only: "true",
    }));

  const rawMarkerReview = units.flatMap((unit) =>
    unit.markers.map((marker) => ({
      unit_id: unit.id,
      marker_key: marker.key,
      marker_time: marker.time.toFixed(3),
      unit_status: unit.unit_status,
      source: unit.source,
      boundary_type: unit.boundary_type ?? "next_slate_start",
    })),
  );

  const splitPlan = units
    .filter((unit) => unit.unit_status !== "excluded")
    .map((unit) => ({
      unit_id: unit.id,
      take_id: unit.takeId,
      not_executed: "true",
      not_recording_segments: "true",
      not_sample_assets: "true",
      not_sample_source: "true",
      not_ml_training_data: "true",
    }));

  return { reviewedManifest, rawMarkerReview, splitPlan };
}
