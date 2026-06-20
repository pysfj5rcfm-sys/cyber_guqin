import { useMemo, useState } from "react";
import type { ReactNode } from "react";

export function ReviewPrimarySelector<T>({
  title,
  items,
  selectedId,
  onSelect,
  getId,
  getSearchText,
  renderItem,
  placeholder,
  loading = false,
  error = "",
  emptyText = "没有可选项",
}: {
  title: string;
  items: T[];
  selectedId: string;
  onSelect: (item: T) => void;
  getId: (item: T) => string;
  getSearchText: (item: T) => string;
  renderItem: (item: T) => ReactNode;
  placeholder: string;
  loading?: boolean;
  error?: string;
  emptyText?: string;
}) {
  const [query, setQuery] = useState("");
  const normalizedQuery = query.trim().toLowerCase();
  const filteredItems = useMemo(
    () => normalizedQuery ? items.filter((item) => getSearchText(item).toLowerCase().includes(normalizedQuery)) : items,
    [getSearchText, items, normalizedQuery],
  );

  return (
    <section className="editor-section">
      <h3>{title}</h3>
      <div className="search-box">
        <span>⌕</span>
        <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={placeholder} />
      </div>
      <div className="file-list review-primary-list">
        {loading && <div className="list-state">正在加载...</div>}
        {error && <div className="list-state list-state-error">{error}</div>}
        {!loading && !error && filteredItems.length === 0 && <div className="list-state">{emptyText}</div>}
        {!loading && !error && filteredItems.map((item) => {
          const id = getId(item);
          return (
            <button key={id} className={selectedId === id ? "selected" : ""} onClick={() => onSelect(item)}>
              {renderItem(item)}
            </button>
          );
        })}
      </div>
    </section>
  );
}
