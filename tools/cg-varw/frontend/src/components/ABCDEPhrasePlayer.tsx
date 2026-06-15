import type { RenderPhraseAlignment, RenderVersion } from "../types/cgVarw";

export function ABCDEPhrasePlayer({
  versions,
  alignments,
  selectedVersionId,
  onSelect,
}: {
  versions: RenderVersion[];
  alignments: RenderPhraseAlignment[];
  selectedVersionId: string;
  onSelect: (versionId: string) => void;
}) {
  const alignmentByVersion = new Map(alignments.map((alignment) => [alignment.version_id, alignment]));
  return (
    <div className="version-list">
      <div className="version-head">
        <span>版本</span><span>名称</span><span>波形预览</span><span>本句范围</span><span>边界状态</span><span>操作</span>
      </div>
      {versions.map((version) => {
        const alignment = alignmentByVersion.get(version.version_id);
        return (
          <button key={version.version_id} className={`version-row ${selectedVersionId === version.version_id ? "selected" : ""}`} onClick={() => onSelect(version.version_id)}>
            <b className={`version-letter letter-${version.version_code}`}>{version.version_code}</b>
            <span>{version.version_label_zh} / {version.version_label_en}<small>{version.version_id}</small></span>
            <i className="mini-wave" />
            <span>{formatAlignment(alignment)}</span>
            <span>{alignment?.review_status ?? "candidate"}</span>
            <span className="kebab">⋮</span>
          </button>
        );
      })}
    </div>
  );
}

function formatAlignment(alignment?: RenderPhraseAlignment) {
  if (!alignment) return "no phrase alignment";
  return `${alignment.phrase_id}: ${alignment.start_s.toFixed(3)}-${alignment.end_s.toFixed(3)}s`;
}
