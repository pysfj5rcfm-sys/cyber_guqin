import type { ExportRow, Marker, MockFlags, R2MarkerKey, VersionRow } from "../types/cgVarw";

export const projectFlags: MockFlags = {
  review_only: true,
  production_grade: false,
  training_value_class: ["creative_dapu_review", "listening_feedback", "render_revision_learning"],
};

export const versions: VersionRow[] = [
  { id: "A", key: "A_LITERAL", name: "直译谱面版", englishName: "A Literal Dapu", eventRange: "XWC_P03_N02 → N04", rating: 2 },
  { id: "B", key: "B_PHRASE", name: "句法呼吸版", englishName: "B Phrase Dapu", eventRange: "XWC_P03_N02 → N04", rating: 4, selected: true },
  { id: "C", key: "C_QINIST_STYLE", name: "琴人风格版", englishName: "C Qinist Style Dapu", eventRange: "XWC_P03_N02 → N04", rating: 3 },
  { id: "D", key: "D_TEACHING", name: "教学诊断版", englishName: "D Teaching / Diagnostic Dapu", eventRange: "XWC_P03_N02 → N04", rating: 1 },
  { id: "E", key: "E_REVIEWED", name: "听评修订版", englishName: "E Reviewed Dapu", eventRange: "XWC_P03_N02 → N04", rating: 4 },
];

export const phraseMarkers: Marker<R2MarkerKey>[] = [
  { key: "phrase_start", label: "句头", time: 0, color: "green" },
  { key: "breath_point", label: "气口", time: 21.824, color: "blue" },
  { key: "section_start", label: "段落起", time: 0, color: "green" },
  { key: "cadence", label: "收束", time: 72.903, color: "gold" },
  { key: "unclear_boundary", label: "边界不明", time: 64.2, color: "red" },
  { key: "phrase_end", label: "句尾", time: 106.262, color: "purple" },
];

export const phraseExports: ExportRow[] = [
  { file: "phrase_structure_review.yaml", description: "整曲的句读结构与事件标注（人工复核）", rule: "基于本页标记与事件信息生成", actor: "qinist_01", updatedAt: "2025-05-06 15:32:18" },
  { file: "render_phrase_alignment.csv", description: "各版本句读对齐与偏移统计", rule: "基于 event_range 计算各版本句读偏移与时长", actor: "qinist_01", updatedAt: "2025-05-06 15:32:18" },
  { file: "phrase_boundary_decision.csv", description: "句读边界决策记录（含置信度与原因）", rule: "记录句读标记的来源、置信度与修订历史", actor: "qinist_01", updatedAt: "2025-05-06 15:32:18" },
  { file: "listening_review.yaml", description: "听评批注与问题记录（句级）", rule: "本页批注与问题类型汇总", actor: "qinist_01", updatedAt: "2025-05-06 15:32:18" },
  { file: "render_revision_log.yaml", description: "修订日志（版本变更与备注）", rule: "基于批注保存与版本选择动作记录", actor: "qinist_01", updatedAt: "2025-05-06 15:32:18" },
];
