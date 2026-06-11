import type { ExportRow } from "../types/cgVarw";

export function ExportPanel({ title, rows }: { title: string; rows: ExportRow[] }) {
  return (
    <div className="export-panel">
      <h2>{title}</h2>
      <table>
        <thead>
          <tr>
            <th>输出文件</th>
            <th>说明</th>
            <th>生成规则</th>
            <th>更新人</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.file}>
              <td><span className="file-icon">CSV</span>{row.file}</td>
              <td>{row.description}</td>
              <td>{row.rule}</td>
              <td>{row.actor ?? "mock_ui"}</td>
              <td>{row.updatedAt}</td>
              <td className="row-actions"><button title="预览">◎</button><button title="下载">↓</button><button title="打开目录">□</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
