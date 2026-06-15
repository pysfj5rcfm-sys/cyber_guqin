import { useMemo, useState } from "react";
import type { ExportRow, ListeningReview, MarkerReviewStatus, PhraseDefinition, PhraseMarker, R2IssueType, RenderPhraseAlignment, Section, Severity } from "../types/cgVarw";

const groups = ["全部", "句读结构", "版本对齐", "听评记录", "修订依据", "汇总"];

type PreviewTable = {
  file: string;
  columns: string[];
  rows: Record<string, string>[];
};

type R2ListeningReviewDraft = {
  phrase_id: string;
  version_id: string;
  issue_type: R2IssueType[];
  severity: Severity;
  quick_judgement?: "good" | "usable" | "needs_revision" | "bad";
  comment: string;
  suggested_revision: string;
  reviewer: string;
  reviewed_at: string;
  updated_at?: string;
};

type PreferredVersionByPhrase = Record<string, string>;
type ListeningReviewByKey = Record<string, R2ListeningReviewDraft>;

export function R2ExportPreviewPanel({
  title,
  rows,
  group,
  sections,
  phrases,
  alignments,
  markers,
  review,
  preferredVersionByPhrase,
  listeningReviewByKey,
  activePhraseId,
  activeVersionId,
  preferredVersionId,
  boundaryStatus,
  onGroupChange,
  onSaveDraft,
  onExportAll,
  onExportPhrase,
  onPreview,
}: {
  title: string;
  rows: ExportRow[];
  group?: string;
  sections: Section[];
  phrases: PhraseDefinition[];
  alignments: RenderPhraseAlignment[];
  markers: PhraseMarker[];
  review: ListeningReview;
  preferredVersionByPhrase?: PreferredVersionByPhrase;
  listeningReviewByKey?: ListeningReviewByKey;
  activePhraseId: string;
  activeVersionId: string;
  preferredVersionId?: string;
  boundaryStatus: MarkerReviewStatus;
  onGroupChange?: (group: string) => void;
  onSaveDraft?: () => void;
  onExportAll?: () => void;
  onExportPhrase?: () => void;
  onPreview?: (file: string) => void;
}) {
  const activeGroup = group ?? "全部";
  const visibleRows = activeGroup === "全部" ? rows : rows.filter((row) => row.group === activeGroup);
  const [focusedFile, setFocusedFile] = useState<string | null>(null);
  const previewTables = useMemo(
    () => buildPreviewTables({ sections, phrases, alignments, markers, review, preferredVersionByPhrase, listeningReviewByKey, activePhraseId, activeVersionId, preferredVersionId, boundaryStatus }),
    [sections, phrases, alignments, markers, review, preferredVersionByPhrase, listeningReviewByKey, activePhraseId, activeVersionId, preferredVersionId, boundaryStatus],
  );
  const focusedRows = useMemo(() => {
    if (activeGroup === "全部") return [];
    if (!focusedFile) return visibleRows;
    return visibleRows.filter((row) => row.file === focusedFile);
  }, [activeGroup, focusedFile, visibleRows]);

  function changeGroup(nextGroup: string) {
    setFocusedFile(null);
    onGroupChange?.(nextGroup);
  }

  function previewFile(row: ExportRow) {
    if (row.group && row.group !== activeGroup) onGroupChange?.(row.group);
    setFocusedFile(row.file);
    onPreview?.(row.file);
  }

  return (
    <div className="export-panel r2-export-panel">
      <div className="export-header-row">
        <h2>{title}</h2>
        <div className="export-actions">
          <button className="primary-action" onClick={onSaveDraft}>保存 draft</button>
          <button onClick={onExportAll}>导出全部</button>
          <button onClick={onExportPhrase}>导出当前 phrase</button>
        </div>
      </div>
      <div className="export-tabs" role="tablist" aria-label="导出分类">
        {groups.map((item) => <button key={item} role="tab" className={activeGroup === item ? "active" : ""} onClick={() => changeGroup(item)}>{item}</button>)}
      </div>
      {activeGroup === "全部" ? (
        <div className="export-table-scroll">
          <table className="export-table">
            <thead>
              <tr>
                <th>文件名</th>
                <th>分组</th>
                <th>说明</th>
                <th>生成范围</th>
                <th>更新人</th>
                <th>更新时间</th>
                <th className="export-table-action-column">操作</th>
              </tr>
            </thead>
            <tbody>
              {visibleRows.map((row) => (
                <tr key={row.file}>
                  <td><span className="file-icon">{fileKind(row.file)}</span>{row.file}</td>
                  <td>{row.group ?? "全部"}</td>
                  <td>{row.description}</td>
                  <td>{row.scope ?? row.rule}</td>
                  <td>{row.actor ?? "mock_ui"}</td>
                  <td>{row.updatedAt}</td>
                  <td className="row-actions export-table-action-column">
                    <button title="预览该文件" onClick={() => previewFile(row)}>预览</button>
                    <button title="mock 下载动作">下载</button>
                    <button title="显示详情">详情</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className={`r2-export-preview-grid preview-count-${Math.min(focusedRows.length, 3)}`}>
          {focusedRows.map((row) => (
            <PreviewCard
              key={row.file}
              row={row}
              table={previewTables[row.file]}
              focused={focusedFile === row.file}
              onPreview={() => previewFile(row)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function PreviewCard({ row, table, focused, onPreview }: { row: ExportRow; table?: PreviewTable; focused: boolean; onPreview: () => void }) {
  const preview = table ?? { file: row.file, columns: ["file", "review_only", "production_grade"], rows: [{ file: row.file, review_only: "true", production_grade: "false" }] };
  return (
    <article className={`preview-card ${focused ? "is-focused" : ""}`}>
      <div className="preview-card-head">
        <h3><span className="file-icon">{fileKind(row.file)}</span>{row.file}</h3>
        <button onClick={onPreview}>预览</button>
      </div>
      <small>{row.group} · {row.scope ?? row.rule}</small>
      <div className="export-table-scroll">
        <table className="field-preview-table">
          <thead>
            <tr>{preview.columns.map((column) => <th key={column}>{column}</th>)}</tr>
          </thead>
          <tbody>
            {preview.rows.map((previewRow, index) => (
              <tr key={`${row.file}-${index}`}>
                {preview.columns.map((column) => <td key={column}>{previewRow[column] ?? ""}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  );
}

function buildPreviewTables({
  sections,
  phrases,
  alignments,
  markers,
  review,
  preferredVersionByPhrase,
  listeningReviewByKey,
  activePhraseId,
  activeVersionId,
  preferredVersionId,
  boundaryStatus,
}: {
  sections: Section[];
  phrases: PhraseDefinition[];
  alignments: RenderPhraseAlignment[];
  markers: PhraseMarker[];
  review: ListeningReview;
  preferredVersionByPhrase?: PreferredVersionByPhrase;
  listeningReviewByKey?: ListeningReviewByKey;
  activePhraseId: string;
  activeVersionId: string;
  preferredVersionId?: string;
  boundaryStatus: MarkerReviewStatus;
}): Record<string, PreviewTable> {
  const activePhrase = phrases.find((phrase) => phrase.phrase_id === activePhraseId) ?? phrases[0];
  const activeSection = sections.find((section) => section.section_id === activePhrase?.section_id) ?? sections[0];
  const activeAlignments = alignments.filter((alignment) => alignment.phrase_id === activePhraseId);
  const reviewDrafts = Object.values(listeningReviewByKey ?? {});
  const listeningRows = reviewDrafts.length > 0 ? reviewDrafts : [{
    phrase_id: activePhraseId,
    version_id: activeVersionId,
    issue_type: review.issue_type,
    severity: review.severity,
    quick_judgement: undefined,
    comment: review.comment,
    suggested_revision: review.suggested_revision ?? "",
    reviewer: review.reviewer,
    reviewed_at: review.reviewed_at,
    updated_at: review.reviewed_at,
  }];
  return {
    "phrase_structure_review.yaml": {
      file: "phrase_structure_review.yaml",
      columns: ["section_id", "section_label", "phrase_id", "phrase_label", "event_range", "marker_count", "review_only", "production_grade"],
      rows: phrases.map((phrase) => {
        const section = sections.find((item) => item.section_id === phrase.section_id);
        return {
          section_id: phrase.section_id,
          section_label: section?.section_label ?? "",
          phrase_id: phrase.phrase_id,
          phrase_label: phrase.phrase_label,
          event_range: phrase.event_range,
          marker_count: String(markers.filter((marker) => marker.phrase_id === phrase.phrase_id).length),
          review_only: "true",
          production_grade: "false",
        };
      }),
    },
    "phrase_boundary_decision.csv": {
      file: "phrase_boundary_decision.csv",
      columns: ["render_set_id", "version_id", "phrase_id", "section_id", "boundary_status", "phrase_start_s", "phrase_end_s", "breath_points_s", "cadence_point_s", "review_only", "production_grade"],
      rows: activeAlignments.map((alignment) => ({
        render_set_id: alignment.render_set_id,
        version_id: alignment.version_id,
        phrase_id: alignment.phrase_id,
        section_id: alignment.section_id,
        boundary_status: alignment.version_id === activeVersionId ? boundaryStatus : alignment.review_status,
        phrase_start_s: alignment.start_s.toFixed(3),
        phrase_end_s: alignment.end_s.toFixed(3),
        breath_points_s: alignment.breath_points_s.map((time) => time.toFixed(3)).join(";"),
        cadence_point_s: alignment.cadence_point_s?.toFixed(3) ?? "",
        review_only: "true",
        production_grade: "false",
      })),
    },
    "render_phrase_alignment.csv": {
      file: "render_phrase_alignment.csv",
      columns: ["render_set_id", "version_id", "phrase_id", "section_id", "event_range", "start_s", "end_s", "boundary_source", "review_status", "review_only", "production_grade"],
      rows: activeAlignments.map((alignment) => ({
        render_set_id: alignment.render_set_id,
        version_id: alignment.version_id,
        phrase_id: alignment.phrase_id,
        section_id: alignment.section_id,
        event_range: alignment.event_range,
        start_s: alignment.start_s.toFixed(3),
        end_s: alignment.end_s.toFixed(3),
        boundary_source: alignment.boundary_source,
        review_status: alignment.review_status,
        review_only: "true",
        production_grade: "false",
      })),
    },
    "listening_review.yaml": {
      file: "listening_review.yaml",
      columns: ["review_id", "render_set_id", "phrase_id", "section_id", "event_range", "active_version_id", "preferred_version_id", "quick_judgement", "issue_type", "severity", "comment", "suggested_revision", "review_only", "production_grade"],
      rows: listeningRows.map((item) => {
        const phrase = phrases.find((candidate) => candidate.phrase_id === item.phrase_id) ?? activePhrase;
        return {
        review_id: `R2_REVIEW_${item.phrase_id}_${item.version_id}`,
        render_set_id: review.render_set_id,
        phrase_id: item.phrase_id,
        section_id: phrase?.section_id ?? "",
        event_range: phrase?.event_range ?? "",
        active_version_id: item.version_id,
        preferred_version_id: preferredVersionByPhrase?.[item.phrase_id] ?? "",
        quick_judgement: item.quick_judgement ?? "",
        issue_type: JSON.stringify(item.issue_type),
        severity: item.severity,
        comment: item.comment,
        suggested_revision: item.suggested_revision,
        review_only: "true",
        production_grade: "false",
      };
      }),
    },
    "issue_list.csv": {
      file: "issue_list.csv",
      columns: ["review_id", "phrase_id", "version_id", "section_id", "issue_type", "severity", "review_only", "production_grade"],
      rows: listeningRows.flatMap((item) => item.issue_type.map((issue) => ({
        review_id: `R2_REVIEW_${item.phrase_id}_${item.version_id}`,
        phrase_id: item.phrase_id,
        version_id: item.version_id,
        section_id: (phrases.find((phrase) => phrase.phrase_id === item.phrase_id) ?? activePhrase)?.section_id ?? "",
        issue_type: issue,
        severity: item.severity,
        review_only: "true",
        production_grade: "false",
      }))),
    },
    "render_revision_log.yaml": {
      file: "render_revision_log.yaml",
      columns: ["revision_id", "render_set_id", "from_version_id", "to_version_id", "phrase_id", "section_id", "event_range", "change_type", "reason", "review_only", "production_grade"],
      rows: [{
        revision_id: `R2_REVISION_${activePhraseId}`,
        render_set_id: review.render_set_id,
        from_version_id: activeVersionId,
        to_version_id: "",
        phrase_id: activePhraseId,
        section_id: activePhrase?.section_id ?? "",
        event_range: activePhrase?.event_range ?? "",
        change_type: "other",
        reason: review.suggested_revision ?? "review-only evidence; no E/F render generated",
        review_only: "true",
        production_grade: "false",
      }],
    },
    "preferred_version_summary.csv": {
      file: "preferred_version_summary.csv",
      columns: ["render_set_id", "phrase_id", "section_id", "section_label", "preferred_version_id", "active_version_id", "review_only", "production_grade"],
      rows: phrases.map((phrase) => {
        const section = sections.find((item) => item.section_id === phrase.section_id) ?? activeSection;
        return {
        render_set_id: review.render_set_id,
        phrase_id: phrase.phrase_id,
        section_id: phrase.section_id,
        section_label: section?.section_label ?? "",
        preferred_version_id: preferredVersionByPhrase?.[phrase.phrase_id] ?? "",
        active_version_id: phrase.phrase_id === activePhraseId ? activeVersionId : "",
        review_only: "true",
        production_grade: "false",
      };
      }),
    },
  };
}

function fileKind(file: string) {
  return file.endsWith(".yaml") ? "YML" : "CSV";
}
