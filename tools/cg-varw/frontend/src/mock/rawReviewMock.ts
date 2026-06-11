import type { Marker, MockFlags, R0MarkerKey, ReviewUnit, ReviewUnitStatus } from "../types/cgVarw";

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

export const markerLabels: Record<R0MarkerKey, string> = {
  slate_start: "口播起始",
  slate_end: "口播结束",
  guqin_start: "古琴起声",
  tail_end: "尾音结束",
  next_slate_start: "下一口播起始",
};

export const unitStatusLabels: Record<ReviewUnitStatus, string> = {
  confirmed: "已确认",
  needs_review: "待复核",
  not_started: "未开始",
  needs_retake: "需重录",
  excluded: "已排除",
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
    optional: key === "guqin_start" || key === "tail_end",
  }));
}

export const rawReviewUnits: ReviewUnit[] = [
  {
    id: "T001",
    sequence: 1,
    unit_status: "confirmed",
    source: "asr_candidate",
    takeId: "XWC_P01_N01",
    markers: unitMarkers({ slate_start: 4.8, slate_end: 11.4, guqin_start: 16.2, tail_end: 26.8, next_slate_start: 31.4 }),
  },
  {
    id: "T002",
    sequence: 2,
    unit_status: "confirmed",
    source: "asr_candidate",
    takeId: "XWC_P01_N02",
    markers: unitMarkers({ slate_start: 31.4, slate_end: 38.9, guqin_start: 44.6, tail_end: 54.2, next_slate_start: 48.2 }),
  },
  {
    id: "T003",
    sequence: 3,
    unit_status: "needs_review",
    source: "asr_candidate",
    takeId: "XWC_P01_N03",
    markers: unitMarkers({ slate_start: 48.2, slate_end: 56.8, guqin_start: 62.487, tail_end: 76.6, next_slate_start: 85.2 }),
  },
  {
    id: "T004",
    sequence: 4,
    unit_status: "not_started",
    source: "asr_candidate",
    takeId: "XWC_P01_N04",
    markers: unitMarkers({ slate_start: 85.2, slate_end: 92.3, guqin_start: 98.5, tail_end: 110.4, next_slate_start: 116.2 }),
  },
  {
    id: "T005",
    sequence: 5,
    unit_status: "confirmed",
    source: "asr_candidate",
    takeId: "XWC_P01_N05",
    markers: unitMarkers({ slate_start: 116.2, slate_end: 122.5, guqin_start: 128.8, tail_end: 138.6, next_slate_start: 143.1 }),
  },
  {
    id: "T006",
    sequence: 6,
    unit_status: "confirmed",
    source: "asr_candidate",
    takeId: "XWC_P01_N06",
    markers: unitMarkers({ slate_start: 143.1, slate_end: 148.2, guqin_start: 152.7, tail_end: 158.8, next_slate_start: 161.5 }),
  },
  {
    id: "T007",
    sequence: 7,
    unit_status: "needs_retake",
    source: "asr_candidate",
    takeId: "XWC_P01_N07",
    markers: unitMarkers({ slate_start: 161.5, slate_end: 166.1, guqin_start: 170.4, tail_end: 176.2, next_slate_start: 181.3 }),
  },
  {
    id: "T008",
    sequence: 8,
    unit_status: "not_started",
    source: "asr_candidate",
    takeId: "XWC_P01_N08",
    markers: unitMarkers({ slate_start: 181.3, slate_end: 186.5, guqin_start: 191.2, tail_end: 198.4, next_slate_start: 202.6 }),
  },
  {
    id: "T009",
    sequence: 9,
    unit_status: "confirmed",
    source: "asr_candidate",
    takeId: "XWC_P01_N09",
    markers: unitMarkers({ slate_start: 202.6, slate_end: 208.7, guqin_start: 214.1, tail_end: 222.8, next_slate_start: 226.4 }),
  },
  {
    id: "T010",
    sequence: 10,
    unit_status: "excluded",
    source: "asr_candidate",
    takeId: "XWC_P01_N10",
    markers: unitMarkers({ slate_start: 226.4, slate_end: 232.2, guqin_start: 237.5, tail_end: 244.3, next_slate_start: 248.1 }),
  },
];

export function completedMarkerCount(unit: ReviewUnit) {
  if (unit.unit_status === "not_started") return 0;
  if (unit.unit_status === "needs_review") return 4;
  return 5;
}

export function buildRawExportPreview(units: ReviewUnit[]) {
  const reviewedManifest = units
    .filter((unit) => unit.unit_status === "confirmed" || unit.unit_status === "needs_retake")
    .map((unit) => ({
      unit_id: unit.id,
      unit_status: unit.unit_status,
      take_id: unit.takeId,
      slate_start: unit.markers.find((marker) => marker.key === "slate_start")?.time.toFixed(3) ?? "",
      guqin_start: unit.markers.find((marker) => marker.key === "guqin_start")?.time.toFixed(3) ?? "",
    }));

  const rawMarkerReview = units.flatMap((unit) =>
    unit.markers.map((marker) => ({
      unit_id: unit.id,
      marker_key: marker.key,
      marker_time: marker.time.toFixed(3),
      unit_status: unit.unit_status,
      source: unit.source,
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
    }));

  return { reviewedManifest, rawMarkerReview, splitPlan };
}
