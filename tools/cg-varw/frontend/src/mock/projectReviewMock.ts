import type {
  ExportRow,
  ListeningReview,
  PhraseDefinition,
  PhraseMarker,
  R2IssueType,
  R2Piece,
  R2SafetyFlags,
  R2Session,
  RenderPhraseAlignment,
  RenderSet,
  RenderVersion,
  Section,
} from "../types/cgVarw";

export const r2SafetyFlags: R2SafetyFlags = {
  review_only: true,
  production_grade: false,
  not_render_executed: true,
  not_sample_assets: true,
  not_ml_training_data: true,
};

export const mockPieces: R2Piece[] = [
  { piece_id: "XWC", piece_title: "仙翁操", active_mvp: true, mock_only: false },
  { piece_id: "JK", piece_title: "酒狂", active_mvp: false, mock_only: true },
  { piece_id: "OLWJ", piece_title: "鸥鹭忘机", active_mvp: false, mock_only: true },
  { piece_id: "MHSN", piece_title: "梅花三弄", active_mvp: false, mock_only: true },
];

export const mockSessions: R2Session[] = [
  { recording_session_id: "RS_XWC_002_BAIYA_PILOT", label: "白牙 pilot / current session", current_project_session: true, mock_only: false },
  { recording_session_id: "DEMO_SESSION_001", label: "UI mock only", current_project_session: false, mock_only: true },
  { recording_session_id: "DEMO_SESSION_002", label: "UI mock only", current_project_session: false, mock_only: true },
];

export const renderSet: RenderSet = {
  render_set_id: "R2A_MOCK_XWC_BAIYA_001",
  project_id: "CG_VARW",
  recording_session_id: "RS_XWC_002_BAIYA_PILOT",
  piece_id: "XWC",
  piece_title: "仙翁操",
  qinist_id: "QINIST_002",
  render_stage: "mock",
  created_at: "2026-06-15T00:00:00+08:00",
  ...r2SafetyFlags,
};

export const sections: Section[] = [
  { section_id: "SECTION_01", section_label: "起首", event_range: "XWC_P01_N01_to_XWC_P02_N04", phrase_ids: ["PHRASE_01", "PHRASE_02"] },
  { section_id: "SECTION_02", section_label: "承接", event_range: "XWC_P03_N01_to_XWC_P04_N04", phrase_ids: ["PHRASE_03", "PHRASE_04"] },
  { section_id: "SECTION_03", section_label: "转合", event_range: "XWC_P05_N01_to_XWC_P06_N03", phrase_ids: ["PHRASE_05"] },
];

export const phrases: PhraseDefinition[] = [
  { phrase_id: "PHRASE_01", section_id: "SECTION_01", phrase_index: 1, phrase_label: "初起一息", event_range: "XWC_P01_N01_to_N03", start_event_id: "XWC_P01_N01", end_event_id: "XWC_P01_N03" },
  { phrase_id: "PHRASE_02", section_id: "SECTION_01", phrase_index: 2, phrase_label: "虚收", event_range: "XWC_P02_N01_to_N04", start_event_id: "XWC_P02_N01", end_event_id: "XWC_P02_N04" },
  { phrase_id: "PHRASE_03", section_id: "SECTION_02", phrase_index: 3, phrase_label: "承接短句", event_range: "XWC_P03_N02_to_N04", start_event_id: "XWC_P03_N02", end_event_id: "XWC_P03_N04" },
  { phrase_id: "PHRASE_04", section_id: "SECTION_02", phrase_index: 4, phrase_label: "回身", event_range: "XWC_P04_N01_to_N04", start_event_id: "XWC_P04_N01", end_event_id: "XWC_P04_N04" },
  { phrase_id: "PHRASE_05", section_id: "SECTION_03", phrase_index: 5, phrase_label: "收合", event_range: "XWC_P05_N01_to_XWC_P06_N03", start_event_id: "XWC_P05_N01", end_event_id: "XWC_P06_N03" },
];

export const versions: RenderVersion[] = [
  { render_set_id: renderSet.render_set_id, version_id: "A_LITERAL", version_code: "A", version_label_zh: "直译谱面版", version_label_en: "Literal Dapu", version_role: "literal_dapu", audio_path: "mock://r2/A_LITERAL", duration_s: 108.4, waveform_preview: makeWave(0), mock_render: true, ...r2SafetyFlags },
  { render_set_id: renderSet.render_set_id, version_id: "B_PHRASE", version_code: "B", version_label_zh: "句法呼吸版", version_label_en: "Phrase Dapu", version_role: "phrase_dapu", audio_path: "mock://r2/B_PHRASE", duration_s: 106.3, waveform_preview: makeWave(1), mock_render: true, ...r2SafetyFlags },
  { render_set_id: renderSet.render_set_id, version_id: "C_QINIST_STYLE", version_code: "C", version_label_zh: "琴人风格版", version_label_en: "Qinist Style Dapu", version_role: "qinist_style_dapu", audio_path: "mock://r2/C_QINIST_STYLE", duration_s: 111.1, waveform_preview: makeWave(2), mock_render: true, ...r2SafetyFlags },
  { render_set_id: renderSet.render_set_id, version_id: "D_TEACHING", version_code: "D", version_label_zh: "教学诊断版", version_label_en: "Teaching Diagnostic Dapu", version_role: "teaching_diagnostic_dapu", audio_path: "mock://r2/D_TEACHING", duration_s: 113.7, waveform_preview: makeWave(3), mock_render: true, ...r2SafetyFlags },
  { render_set_id: renderSet.render_set_id, version_id: "E_REVIEWED", version_code: "E", version_label_zh: "听评修订版", version_label_en: "Reviewed Dapu", version_role: "reviewed_dapu", audio_path: "mock://r2/E_REVIEWED", duration_s: 107.8, waveform_preview: makeWave(4), mock_render: true, ...r2SafetyFlags },
];

const phraseStartByVersion: Record<string, number[]> = {
  PHRASE_01: [0.4, 0.2, 0.6, 0.3, 0.4],
  PHRASE_02: [16.8, 16.4, 17.2, 16.9, 16.6],
  PHRASE_03: [38.42, 39.08, 37.86, 40.12, 38.74],
  PHRASE_04: [63.52, 62.96, 65.04, 66.2, 63.4],
  PHRASE_05: [83.1, 81.94, 86.2, 88.12, 82.66],
};

const phraseLengthsByVersion: Record<string, number[]> = {
  PHRASE_01: [12.9, 13.4, 13.1, 14.2, 13.2],
  PHRASE_02: [17.3, 17.9, 18.1, 19.2, 17.5],
  PHRASE_03: [20.36, 21.82, 22.18, 23.46, 21.16],
  PHRASE_04: [16.92, 17.84, 18.96, 19.04, 17.62],
  PHRASE_05: [19.6, 20.4, 21.7, 22.5, 20.1],
};

export const phraseAlignments: RenderPhraseAlignment[] = phrases.flatMap((phrase) =>
  versions.map((version, versionIndex) => {
    const start_s = phraseStartByVersion[phrase.phrase_id][versionIndex];
    const length = phraseLengthsByVersion[phrase.phrase_id][versionIndex];
    return {
      render_set_id: renderSet.render_set_id,
      version_id: version.version_id,
      phrase_id: phrase.phrase_id,
      section_id: phrase.section_id,
      event_range: phrase.event_range,
      start_s,
      end_s: Number((start_s + length).toFixed(3)),
      breath_points_s: [Number((start_s + length * (version.version_code === "D" ? 0.42 : 0.38)).toFixed(3))],
      cadence_point_s: Number((start_s + length * 0.82).toFixed(3)),
      boundary_source: "mock",
      boundary_confidence: version.version_code === "D" ? "medium" : "high",
      review_status: phrase.phrase_id === "PHRASE_03" && version.version_code === "D" ? "unclear" : "candidate",
      reviewer: "mock_reviewer",
      reviewed_at: "2026-06-15T00:00:00+08:00",
      notes: "R2A phrase-aligned mock boundary; not rendered audio.",
    };
  }),
);

export const phraseMarkers: PhraseMarker[] = makePhraseMarkers("PHRASE_03", "B_PHRASE");

export const defaultListeningReview: ListeningReview = {
  review_id: "R2_REVIEW_PHRASE_03_B_001",
  render_set_id: renderSet.render_set_id,
  comparison_scope: "phrase",
  phrase_id: "PHRASE_03",
  section_id: "SECTION_02",
  event_range: "XWC_P03_N02_to_N04",
  active_version_id: "B_PHRASE",
  preferred_version_id: "B_PHRASE",
  issue_type: ["tail_short", "good"],
  severity: "medium",
  comment: "B 版句法呼吸最清楚；尾音略短，但整体保留为正向听评记录。",
  suggested_revision: "后续真实修订可在 cadence 后保留更完整尾音；R2A 不生成 E 版。",
  reviewer: "mock_reviewer",
  reviewed_at: "2026-06-15T00:00:00+08:00",
  training_usable: false,
  ...r2SafetyFlags,
};

export const issueOptions: { key: R2IssueType; label: string }[] = [
  { key: "too_fast", label: "太快" },
  { key: "too_slow", label: "太拖" },
  { key: "tail_short", label: "尾音短" },
  { key: "wrong_breath", label: "气口错" },
  { key: "too_mechanical", label: "像拼接" },
  { key: "attack_abrupt", label: "音头突兀" },
  { key: "sample_mismatch", label: "样本不匹配" },
  { key: "phrase_unclear", label: "句读不清" },
  { key: "good", label: "很好" },
  { key: "other", label: "其他" },
];

export const phraseExports: ExportRow[] = [
  { file: "phrase_structure_review.yaml", group: "句读结构", description: "当前曲目的 section / phrase / marker 结构。", rule: "review-only mock contract", scope: "current piece", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
  { file: "phrase_boundary_decision.csv", group: "句读结构", description: "句头、句尾、气口、收束、边界状态等决策。", rule: "marker review status and notes", scope: "current phrase", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
  { file: "render_phrase_alignment.csv", group: "版本对齐", description: "A/B/C/D/E 每个 phrase 的 start/end 对齐。", rule: "per-version phrase ranges; no absolute-time switching", scope: "all mock phrases", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
  { file: "listening_review.yaml", group: "听评记录", description: "issue_type、severity、comment、preferred_version、suggested_revision。", rule: "good also saved as review record", scope: "current phrase", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
  { file: "issue_list.csv", group: "听评记录", description: "全曲问题清单。", rule: "semantic grouped summary", scope: "all mock phrases", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
  { file: "render_revision_log.yaml", group: "修订依据", description: "从听评到后续修订的依据；不自动生成 E/F。", rule: "revision evidence only", scope: "review-only", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
  { file: "preferred_version_summary.csv", group: "汇总", description: "每个 phrase 的偏好版本汇总。", rule: "semantic grouped summary", scope: "all mock phrases", actor: "mock_reviewer", updatedAt: "2026-06-15 00:00:00" },
];

export function getPhrase(phrase_id: string) {
  return phrases.find((phrase) => phrase.phrase_id === phrase_id) ?? phrases[2];
}

export function getSection(section_id: string) {
  return sections.find((section) => section.section_id === section_id) ?? sections[0];
}

export function getAlignment(phrase_id: string, version_id: string) {
  return phraseAlignments.find((item) => item.phrase_id === phrase_id && item.version_id === version_id) ?? phraseAlignments[0];
}

export function makePhraseMarkers(phrase_id: string, version_id: string): PhraseMarker[] {
  const alignment = getAlignment(phrase_id, version_id);
  const section = getSection(alignment.section_id);
  const markers = [
    marker("phrase_start", "句头", alignment.start_s, alignment),
    ...alignment.breath_points_s.map((time, index) => marker("breath_point", `气口 ${index + 1}`, time, alignment)),
    marker("cadence", "收束", alignment.cadence_point_s ?? alignment.end_s - 1.2, alignment),
    marker("phrase_end", "句尾", alignment.end_s, alignment),
  ];
  if (section.phrase_ids[0] === phrase_id) markers.unshift(marker("section_start", "段落起", alignment.start_s, alignment));
  if (section.phrase_ids[section.phrase_ids.length - 1] === phrase_id) markers.push(marker("section_end", "段落止", alignment.end_s, alignment));
  return markers;
}

function marker(marker_type: PhraseMarker["marker_type"], marker_label_zh: string, time_s: number, alignment: RenderPhraseAlignment, review_status: PhraseMarker["review_status"] = "candidate"): PhraseMarker {
  return {
    marker_id: `${alignment.phrase_id}_${alignment.version_id}_${marker_type}`,
    render_set_id: alignment.render_set_id,
    version_id: alignment.version_id,
    phrase_id: alignment.phrase_id,
    marker_type,
    marker_label_zh,
    time_s,
    source: "mock",
    review_status,
    nudge_total_ms: 0,
    notes: "R2A mock marker; not a render cut.",
  };
}

function makeWave(seed: number) {
  return Array.from({ length: 120 }, (_, index) => {
    const wave = Math.abs(Math.sin(index * 0.17 + seed) * 0.62 + Math.sin(index * 0.047 + seed * 0.7) * 0.38);
    return Number(Math.min(1, Math.max(0.08, wave)).toFixed(3));
  });
}
