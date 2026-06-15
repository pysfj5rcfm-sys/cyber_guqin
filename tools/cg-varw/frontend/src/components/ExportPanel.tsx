import type { ExportRow } from "../types/cgVarw";

export function ExportPanel({ title, rows }: { title: string; rows: ExportRow[] }) {
  return (
    <div className="export-panel">
      <h2>{title}</h2>
      <div className="export-table-scroll">
        <table className="export-table">
          <thead>
            <tr>
              <th>文件名</th>
              <th>说明</th>
              <th>生成规则</th>
              <th>更新人</th>
              <th>更新时间</th>
              <th className="export-table-action-column">操作</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.file}>
                <td><span className="file-icon">{row.file.endsWith(".yaml") ? "YML" : "CSV"}</span>{row.file}</td>
                <td>{row.description}</td>
                <td>{row.rule}</td>
                <td>{row.actor ?? "mock_ui"}</td>
                <td>{row.updatedAt}</td>
                <td className="row-actions export-table-action-column"><button title="预览">预览</button><button title="下载">下载</button><button title="详情">详情</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
