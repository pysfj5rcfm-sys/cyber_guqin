export function KeyValueList({ rows }: { rows: [string, string][] }) {
  return (
    <dl className="kv-list">
      {rows.map(([key, value]) => (
        <div key={key}>
          <dt>{key}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

export function SearchBox({ placeholder }: { placeholder: string }) {
  return <div className="search-box">⌕<input placeholder={placeholder} /></div>;
}
