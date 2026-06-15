import type { MarkerReviewStatus, RenderPhraseAlignment, RenderVersion } from "../types/cgVarw";

export function ABCDEPhrasePlayer({
  versions,
  alignments,
  selectedVersionId,
  preferredVersionId,
  onSelect,
  onSetPreferred,
  onPlay,
}: {
  versions: RenderVersion[];
  alignments: RenderPhraseAlignment[];
  selectedVersionId: string;
  preferredVersionId?: string;
  onSelect: (versionId: string) => void;
  onSetPreferred: (versionId: string) => void;
  onPlay: (versionId: string) => void;
}) {
  const alignmentByVersion = new Map(alignments.map((alignment) => [alignment.version_id, alignment]));
  return (
    <section className="version-switcher" aria-label="版本切换">
      <div className="section-title-row">
        <h2>版本切换 / 当前 phrase 对齐</h2>
        <span>点击 A/B/C/D/E 切换 active version；偏好版本单独设置</span>
      </div>
      <div className="version-list">
        <div className="version-head">
          <span>版本</span><span>本句范围</span><span>边界状态</span><span>偏好</span><span>操作</span>
        </div>
        {versions.map((version) => {
          const alignment = alignmentByVersion.get(version.version_id);
          const selected = selectedVersionId === version.version_id;
          const preferred = preferredVersionId === version.version_id;
          return (
            <div key={version.version_id} className={`version-row ${selected ? "selected" : ""}`} data-version-id={version.version_id}>
              <button className="version-main-button" title={version.version_id} onClick={() => onSelect(version.version_id)}>
                <b className={`version-letter letter-${version.version_code}`}>{version.version_code}</b>
                <span>{version.version_code} {version.version_label_zh}<small>{version.version_label_en}</small></span>
              </button>
              <button className="version-range-button" title={version.version_id} onClick={() => onSelect(version.version_id)}>
                {formatAlignment(alignment)}
              </button>
              <span className="unit-status status-needs_review" title={alignment?.review_status ?? "candidate"}>{statusLabel(alignment?.review_status)}</span>
              <span>{preferred ? <b className="preferred-chip">偏好</b> : <span className="muted-inline">-</span>}</span>
              <span className="row-actions">
                <button onClick={() => onSetPreferred(version.version_id)}>设为偏好</button>
                <button onClick={() => onPlay(version.version_id)}>播放</button>
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function formatAlignment(alignment?: RenderPhraseAlignment) {
  if (!alignment) return "未找到句读对齐";
  return `${alignment.phrase_id}: ${alignment.start_s.toFixed(3)}-${alignment.end_s.toFixed(3)}s`;
}

function statusLabel(status?: MarkerReviewStatus) {
  return {
    candidate: "待确认",
    accepted: "已确认",
    unclear: "待复核",
    needs_retake: "需重录",
    rejected: "已排除",
  }[status ?? "candidate"];
}
