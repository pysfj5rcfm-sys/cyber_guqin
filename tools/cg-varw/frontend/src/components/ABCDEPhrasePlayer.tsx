import type { MarkerReviewStatus, RenderPhraseAlignment, RenderVersion } from "../types/cgVarw";
import { markerReviewStatusLabels, markerReviewStatusTone } from "./reviewUi";

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
        <span>A/B/C/D/E 可听评；F 为待 E 听评后生成的预留槽位</span>
      </div>
      <div className="version-list">
        <div className="version-head">
          <span>版本</span><span>本句范围</span><span>边界状态</span><span>偏好</span><span>操作</span>
        </div>
        {versions.map((version) => {
          const alignment = alignmentByVersion.get(version.version_id);
          const selected = selectedVersionId === version.version_id;
          const preferred = preferredVersionId === version.version_id;
          const pending = version.playable === false || version.status === "pending" || version.alignment_available === false;
          return (
            <div key={version.version_id} className={`version-row ${selected ? "selected" : ""} ${pending ? "disabled" : ""}`} data-version-id={version.version_id}>
              <button className="version-main-button" title={version.disabled_reason || version.version_id} aria-disabled={pending} onClick={() => onSelect(version.version_id)}>
                <b className={`version-letter letter-${version.version_code}`}>{version.version_code}</b>
                <span>{version.version_code} {version.version_label_zh}<small>{pending ? "待 E 听评后生成" : version.version_label_en}</small></span>
              </button>
              <button className="version-range-button" title={version.disabled_reason || version.version_id} aria-disabled={pending} onClick={() => onSelect(version.version_id)}>
                {pending ? "pending / disabled" : formatAlignment(alignment)}
              </button>
              <span className={`unit-status status-${pending ? "muted" : statusTone(alignment?.review_status)}`} title={pending ? "pending" : alignment?.review_status ?? "candidate"}>{pending ? "待生成" : statusLabel(alignment?.review_status)}</span>
              <span>{preferred ? <b className="preferred-chip">偏好</b> : <span className="muted-inline">-</span>}</span>
              <span className="row-actions">
                <button aria-disabled={pending} onClick={() => onSetPreferred(version.version_id)}>{pending ? "不可设偏好" : "设为偏好"}</button>
                <button aria-disabled={pending} onClick={() => onPlay(version.version_id)}>{pending ? "待生成" : "播放"}</button>
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
  const startS = alignment.phrase_play_start_s ?? alignment.start_s;
  const endS = alignment.phrase_play_end_s ?? alignment.end_s;
  return `${alignment.phrase_id}: ${startS.toFixed(3)}-${endS.toFixed(3)}s`;
}

function statusLabel(status?: MarkerReviewStatus) {
  return markerReviewStatusLabels[status ?? "candidate"];
}

function statusTone(status?: MarkerReviewStatus) {
  return markerReviewStatusTone[status ?? "candidate"];
}
