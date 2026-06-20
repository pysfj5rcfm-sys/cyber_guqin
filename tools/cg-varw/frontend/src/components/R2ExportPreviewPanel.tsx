import { useMemo, useState } from "react";
import { buildR2PreviewTables, type R2ListeningReviewDraft, type R2PreviewTable } from "../utils/r2ExportPayload";
import type { ExportRow, ListeningReview, MarkerReviewStatus, PhraseDefinition, PhraseMarker, RenderPhraseAlignment, Section } from "../types/cgVarw";

const groups = ["全部", "句读结构", "版本对齐", "听评记录", "修订依据", "汇总"];

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
  onSaveProjectDraft,
  onExportCsv,
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
  onSaveProjectDraft?: () => void;
  onExportCsv?: () => void;
  onPreview?: (file: string) => void;
}) {
  const activeGroup = group ?? "全部";
  const visibleRows = activeGroup === "全部" ? rows : rows.filter((row) => row.group === activeGroup);
  const [focusedFile, setFocusedFile] = useState<string | null>(null);
  const previewTables = useMemo(
    () => buildR2PreviewTables({ sections, phrases, alignments, markers, review, preferredVersionByPhrase, listeningReviewByKey, activePhraseId, activeVersionId, preferredVersionId, boundaryStatus }),
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
        <div className="export-actions review-actions">
          <button className="primary-action" onClick={onSaveProjectDraft}>保存 draft</button>
          <button onClick={onExportCsv}>导出 CSV</button>
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

function PreviewCard({ row, table, focused, onPreview }: { row: ExportRow; table?: R2PreviewTable; focused: boolean; onPreview: () => void }) {
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

function fileKind(file: string) {
  return file.endsWith(".yaml") ? "YML" : "CSV";
}
