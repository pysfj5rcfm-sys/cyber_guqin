import type { ExportRow } from "../types/cgVarw";

export function ExportPanel({
  title,
  rows,
  group,
  onGroupChange,
  onSaveDraft,
  onExportAll,
  onExportPhrase,
}: {
  title: string;
  rows: ExportRow[];
  group?: string;
  onGroupChange?: (group: string) => void;
  onSaveDraft?: () => void;
  onExportAll?: () => void;
  onExportPhrase?: () => void;
}) {
  const groups = ["全部", "句读结构", "版本对齐", "听评记录", "修订依据", "汇总"];
  const visibleRows = group && group !== "全部" ? rows.filter((row) => row.group === group) : rows;
  return (
    <div className="export-panel">
      <div className="export-toolbar">
        <h2>{title}</h2>
        <div className="segmented compact-segmented">
          {groups.map((item) => <button key={item} className={(group ?? "全部") === item ? "active" : ""} onClick={() => onGroupChange?.(item)}>{item}</button>)}
        </div>
        <div className="action-row export-actions">
          <button onClick={onSaveDraft}>保存 draft</button>
          <button onClick={onExportAll}>导出全部</button>
          <button onClick={onExportPhrase}>导出当前 phrase</button>
          <button>打开导出目录</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>文件名</th>
            <th>分组</th>
            <th>说明</th>
            <th>生成范围</th>
            <th>更新人</th>
            <th>更新时间</th>
            <th>操作</th>
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
              <td className="row-actions"><button title="预览">预览</button><button title="下载">下载</button><button title="打开详情">详情</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function fileKind(file: string) {
  return file.endsWith(".yaml") ? "YML" : "CSV";
}
