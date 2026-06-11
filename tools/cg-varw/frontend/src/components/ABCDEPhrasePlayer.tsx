import type { VersionRow } from "../types/cgVarw";

export function ABCDEPhrasePlayer({ versions, onSelect }: { versions: VersionRow[]; onSelect: (key: string) => void }) {
  return (
    <div className="version-list">
      <div className="version-head">
        <span>版本</span><span>名称</span><span>波形预览</span><span>本句范围（事件）</span><span>偏好评分</span><span>操作</span>
      </div>
      {versions.map((version) => (
        <button key={version.id} className={`version-row ${version.selected ? "selected" : ""}`} onClick={() => onSelect(version.key)}>
          <b className={`version-letter letter-${version.id}`}>{version.id}</b>
          <span>{version.name} / {version.englishName}<small>v1.0.0</small></span>
          <i className="mini-wave" />
          <span>{version.eventRange}</span>
          <span className="stars">{"★".repeat(version.rating)}{"☆".repeat(5 - version.rating)}</span>
          <span className="kebab">⋮</span>
        </button>
      ))}
    </div>
  );
}
